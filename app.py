import json
import re
import shutil
import tempfile
import threading
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

import agent.loop as loop_module
from agent.prompts import SYSTEM_PROMPTS
from agent.tools import RepoTools, run_pytest
from fix import changed_files, make_diff

TASKS_DIR = Path("evals/tasks")
TOOL_NAMES = ["list_files", "read_file", "search", "edit_file", "run_tests"]

app = FastAPI(title="issue-agent")
jobs = {}
run_lock = threading.Lock()  # one agent run at a time (protects the free-tier quota)
_ctx = threading.local()


def make_tools(repo_path):
    """RepoTools that also record every call, so the page can show live progress."""
    tools = RepoTools(repo_path)
    job = _ctx.job
    for name in TOOL_NAMES:
        original = getattr(tools, name)

        def wrapper(*args, _orig=original, _name=name, **kwargs):
            out = _orig(*args, **kwargs)
            job["steps"].append({
                "tool": _name,
                "args": json.dumps(kwargs)[:200],
                "output": str(out)[:500],
            })
            return out

        setattr(tools, name, wrapper)
    return tools


loop_module.RepoTools = make_tools


class RunRequest(BaseModel):
    issue: str
    prompt: str = "v3"
    example: str | None = None
    code: str | None = None
    tests: str | None = None


def worker(job_id, original, work, issue, prompt, hidden_dir, work_root):
    job = jobs[job_id]
    _ctx.job = job
    try:
        with run_lock:
            loop_module.SYSTEM_PROMPT = SYSTEM_PROMPTS[prompt]
            result = loop_module.run_agent(str(work), issue)
        files = changed_files(original, work)
        job["diff"] = make_diff(original, work, files)
        job["summary"] = result["summary"]
        job["agent_steps"] = result["steps"]

        code, _ = run_pytest(work)
        if code >= 125:
            raise RuntimeError("Sandbox error: is Docker Desktop running?")
        job["tests_passed"] = code == 0

        if hidden_dir is not None:
            for f in hidden_dir.glob("test_*.py"):
                shutil.copy(f, work / f.name)
            hcode, _ = run_pytest(work)
            job["hidden_passed"] = hcode == 0
        job["status"] = "done"
    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)[:300]
    finally:
        shutil.rmtree(work_root, ignore_errors=True)


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/api/examples")
def examples():
    out = []
    for task in sorted(TASKS_DIR.iterdir()):
        if not task.is_dir():
            continue
        files = {p.name: p.read_text() for p in sorted((task / "repo").glob("*.py"))}
        out.append({"name": task.name, "issue": (task / "issue.txt").read_text(), "files": files})
    return out


@app.post("/api/run")
def start(req: RunRequest):
    if not req.issue.strip():
        raise HTTPException(400, "Describe the bug first.")
    if req.prompt not in ("v1", "v3"):
        raise HTTPException(400, "Unknown prompt version.")

    work_root = Path(tempfile.mkdtemp(prefix="issue_agent_"))
    original = work_root / "original"
    hidden_dir = None
    if req.example:
        if not re.fullmatch(r"\d\d_\w+", req.example) or not (TASKS_DIR / req.example).is_dir():
            raise HTTPException(404, "Unknown example.")
        task = TASKS_DIR / req.example
        shutil.copytree(task / "repo", original)
        if (task / "hidden").exists():
            hidden_dir = task / "hidden"
    else:
        if not (req.code and req.code.strip() and req.tests and req.tests.strip()):
            raise HTTPException(400, "Paste both your code and your tests.")
        original.mkdir()
        (original / "module.py").write_text(req.code)
        (original / "test_module.py").write_text(req.tests)
    work = work_root / "work"
    shutil.copytree(original, work)

    job_id = uuid.uuid4().hex[:8]
    jobs[job_id] = {
        "status": "running", "steps": [], "summary": "", "diff": "",
        "agent_steps": 0, "tests_passed": None, "hidden_passed": None, "error": "",
    }
    threading.Thread(
        target=worker,
        args=(job_id, original, work, req.issue, req.prompt, hidden_dir, work_root),
        daemon=True,
    ).start()
    return {"job_id": job_id}


@app.get("/api/jobs/{job_id}")
def job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "Unknown job.")
    return jobs[job_id]

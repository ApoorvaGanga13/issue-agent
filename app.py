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
RESULTS_DIR = Path("evals/results")
TRACES_DIR = Path("evals/traces")
TOOL_NAMES = ["list_files", "read_file", "search", "edit_file", "run_tests"]
RESULT_NAME = re.compile(r"^(?P<tag>.+)_(?P<ver>v\d+)_run(?P<run>\d+)\.json$")
TRACE_NAME = re.compile(r"^(?P<tag>[a-z]+)_(?P<ver>v\d+)_run(?P<run>\d+)_(?P<task>\d\d_\w+)\.json$")

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


@app.get("/api/results")
def results():
    """Summary of every saved benchmark run in evals/results."""
    groups = {}
    for f in sorted(RESULTS_DIR.glob("*_run*.json")):
        m = RESULT_NAME.match(f.name)
        if not m:
            continue
        data = json.loads(f.read_text())
        key = (m["tag"], m["ver"])
        g = groups.setdefault(key, {"tag": m["tag"], "version": m["ver"], "runs": [], "solved": 0, "total": 0})
        solved = sum(1 for r in data if r["solved"])
        g["runs"].append({"run": int(m["run"]), "solved": solved, "total": len(data)})
        g["solved"] += solved
        g["total"] += len(data)
    for g in groups.values():
        g["runs"].sort(key=lambda r: r["run"])
    return sorted(groups.values(), key=lambda g: (g["tag"], g["version"]))


def recorded_result(tag, version, run, task):
    f = RESULTS_DIR / f"{tag}_{version}_run{run}.json"
    if not f.exists():
        return None
    for r in json.loads(f.read_text()):
        if r["task"] == task:
            return r
    return None


def replay_diff(task, trace):
    """Re-apply the agent's successful edits to the original repo and diff the result."""
    original = TASKS_DIR / task / "repo"
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        work = Path(tmp) / "work"
        shutil.copytree(original, work)
        for e in trace:
            if e["type"] == "tool" and e["tool"] == "edit_file" and e["output"].startswith("Edit applied"):
                p = (work / e["args"]["path"]).resolve()
                if not p.is_relative_to(work.resolve()) or not p.is_file():
                    continue
                text = p.read_text()
                if text.count(e["args"]["old"]) == 1:
                    p.write_text(text.replace(e["args"]["old"], e["args"]["new"]))
        files = changed_files(original, work)
        return make_diff(original, work, files)


@app.get("/api/replay")
def replay(task: str, version: str):
    """A saved agent run for a task and prompt. Makes no API calls."""
    if version not in ("v1", "v3") or not re.fullmatch(r"\d\d_\w+", task):
        raise HTTPException(400, "Unknown task or prompt.")
    for f in sorted(TRACES_DIR.glob(f"*_{version}_run*_{task}.json")):
        m = TRACE_NAME.match(f.name)
        if not m:
            continue
        record = recorded_result(m["tag"], version, int(m["run"]), task)
        if record is None:
            continue
        trace = json.loads(f.read_text())
        steps = [
            {"tool": e["tool"], "args": json.dumps(e["args"])[:200], "output": e["output"][:500]}
            for e in trace if e["type"] == "tool"
        ]
        texts = [e["text"] for e in trace if e["type"] == "text"]
        summary = texts[-1] if texts else ""
        if record.get("tampered"):
            summary += "\n\n(The benchmark marked this run as failed because the agent edited the visible test files.)"
        return {
            "label": f"Saved run: {m['tag']} experiment, prompt {version}, run {m['run']}. No API calls were made.",
            "steps": steps,
            "summary": summary,
            "diff": replay_diff(task, trace),
            "agent_steps": record["steps"],
            "tests_passed": bool(record["visible_pass"]),
            "hidden_passed": bool(record["solved"]),
        }
    raise HTTPException(404, "No saved run for this bug and prompt.")

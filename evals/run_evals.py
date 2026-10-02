import json
import os
import shutil
import sys
import time
from pathlib import Path

sys.path.append(".")
from agent.loop import run_agent
from agent.prompts import PROMPT_VERSION
from agent.tools import run_pytest

TASKS_DIR = Path("evals/tasks")
WORK_DIR = Path("evals/_work")
OUT_DIR = Path("evals/results")
TRACE_DIR = Path("evals/traces")
RUNS = int(os.getenv("RUNS", "1"))
TAG = os.getenv("TAG", "batch")


def tests_pass(repo: Path) -> bool:
    code, out = run_pytest(repo)
    if code >= 125:
        raise RuntimeError(f"Sandbox error (exit {code}): {out[-300:]}")
    return code == 0


def tests_tampered(task: Path, repo: Path) -> bool:
    """True if the agent edited any visible test file (that would be cheating)."""
    for original in (task / "repo").glob("test_*.py"):
        if (repo / original.name).read_text() != original.read_text():
            return True
    return False


def run_once(run_number, prefixes):
    if WORK_DIR.exists():
        shutil.rmtree(WORK_DIR)
    WORK_DIR.mkdir(parents=True)

    results = []
    for task in sorted(TASKS_DIR.iterdir()):
        if not task.is_dir():
            continue
        if prefixes and not any(task.name.startswith(p) for p in prefixes):
            continue

        issue = (task / "issue.txt").read_text()
        repo = WORK_DIR / task.name
        shutil.copytree(task / "repo", repo)

        if tests_pass(repo):
            print(f"Skipping {task.name}: tests already pass")
            continue

        print(f"\n=== [{TAG} / {PROMPT_VERSION} / run {run_number}] {task.name} ===")
        start = time.time()
        try:
            out = run_agent(str(repo), issue)
            (TRACE_DIR / f"{TAG}_{PROMPT_VERSION}_run{run_number}_{task.name}.json").write_text(
                json.dumps(out["trace"], indent=2)
            )
        except Exception as e:
            print(f"\nERROR on {task.name}: {str(e)[:200]}")
            print("Run aborted. Finished runs are kept. Run the same command again later to continue.")
            sys.exit(1)
        seconds = round(time.time() - start, 1)

        tampered = tests_tampered(task, repo)
        visible_ok = tests_pass(repo)

        # Hidden tests are copied in only after the agent has finished
        hidden_dir = task / "hidden"
        if hidden_dir.exists():
            for f in hidden_dir.glob("test_*.py"):
                shutil.copy(f, repo / f.name)
            full_ok = tests_pass(repo)
        else:
            full_ok = visible_ok

        solved = full_ok and not tampered
        results.append({
            "task": task.name, "solved": solved, "visible_pass": visible_ok,
            "steps": out["steps"], "seconds": seconds,
            "tampered": tampered, "error": None,
        })
        print(f"-> {'SOLVED' if solved else 'FAILED'} in {seconds}s")
        time.sleep(10)  # be gentle with the free-tier rate limit

    return results


def main():
    prefixes = sys.argv[1:]  # e.g. python evals\run_evals.py 18 19 20
    OUT_DIR.mkdir(exist_ok=True)
    TRACE_DIR.mkdir(exist_ok=True)
    print(f"Tag: {TAG} | Prompt: {PROMPT_VERSION} | Runs: {RUNS} | Sandbox: {os.getenv('SANDBOX', 'off')}")

    for run_number in range(1, RUNS + 1):
        out_file = OUT_DIR / f"{TAG}_{PROMPT_VERSION}_run{run_number}.json"
        if out_file.exists():
            print(f"Run {run_number} already done, skipping ({out_file.name})")
            continue

        results = run_once(run_number, prefixes)
        out_file.write_text(json.dumps(results, indent=2))

        print(f"\n===== RUN {run_number} RESULTS =====")
        for r in results:
            if r["solved"]:
                mark = "PASS   "
            elif r["visible_pass"] and not r["tampered"]:
                mark = "OVERFIT"  # passes visible tests, fails hidden ones
            else:
                mark = "FAIL   "
            print(f"{mark} {r['task']:<28} steps={r['steps']}  {r['seconds']}s")
        solved = sum(r["solved"] for r in results)
        print(f"Solve rate: {solved}/{len(results)} = {100 * solved / max(len(results), 1):.0f}%")


if __name__ == "__main__":
    main()

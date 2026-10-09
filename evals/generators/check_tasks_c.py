import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TASKS_DIR = Path("evals/tasks")


def run_tests(repo):
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
        cwd=repo, capture_output=True, text=True, timeout=120,
    )
    return r.returncode


def copy_in(folder, repo, pattern="*"):
    for f in folder.glob(pattern):
        if f.is_file():
            shutil.copy(f, repo / f.name)


bad = 0
print(f"{'task':<22}{'buggy fails':<13}{'solution passes':<17}{'partial passes visible':<24}{'partial fails hidden':<22}")
for task in sorted(TASKS_DIR.iterdir()):
    if not (task / "solution").exists():
        continue
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as t:
        tmp = Path(t)

        buggy = tmp / "buggy"
        shutil.copytree(task / "repo", buggy)
        buggy_fails = run_tests(buggy) != 0

        solved = tmp / "solved"
        shutil.copytree(task / "repo", solved)
        copy_in(task / "solution", solved)
        copy_in(task / "hidden", solved, "test_*.py")
        solution_passes = run_tests(solved) == 0

        partial = tmp / "partial"
        shutil.copytree(task / "repo", partial)
        copy_in(task / "partial", partial)
        partial_visible = run_tests(partial) == 0
        copy_in(task / "hidden", partial, "test_*.py")
        partial_hidden_fails = run_tests(partial) != 0

    checks = [buggy_fails, solution_passes, partial_visible, partial_hidden_fails]
    mark = lambda ok: ("yes" if ok else "NO")
    print(f"{task.name:<22}{mark(buggy_fails):<13}{mark(solution_passes):<17}{mark(partial_visible):<24}{mark(partial_hidden_fails):<22}")
    if not all(checks):
        bad += 1

print("\nAll tasks are fair." if bad == 0 else f"\n{bad} task(s) have a problem. Do not run the benchmark yet.")
sys.exit(1 if bad else 0)

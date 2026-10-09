import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for task in sorted(Path("evals/tasks").glob("2[3-7]_*")):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        repo = Path(tmp) / "repo"
        shutil.copytree(task / "repo", repo)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=repo, capture_output=True, text=True)
        print(f"{task.name:<24} visible tests {'FAIL (good)' if r.returncode else 'PASS (bad, task is broken)'}")

import os
import subprocess
import sys
from pathlib import Path

IMAGE = "issue-agent-sandbox"


def run_pytest(repo, mode=None):
    """Run pytest on a repo. Returns (exit_code, output).

    mode "docker": inside a locked-down container (no network, read-only repo,
    limited memory/CPU/processes, 60 second limit).
    mode "off": directly on this machine.
    Exit codes 125 and above mean the sandbox itself failed, not the tests.
    """
    mode = mode or os.getenv("SANDBOX", "off")
    repo = Path(repo).resolve()
    if mode == "docker":
        cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "--memory", "512m", "--cpus", "1", "--pids-limit", "128",
            "-e", "PYTHONDONTWRITEBYTECODE=1",
            "-v", f"{repo}:/work:ro",
            "-w", "/work",
            IMAGE,
            "timeout", "60", "python", "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider",
        ]
    else:
        cmd = [sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider"]
    try:
        r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return 124, "Tests timed out"
    except FileNotFoundError:
        return 127, "docker was not found. Is Docker Desktop installed and running?"
    return r.returncode, (r.stdout + r.stderr)[-4000:]


class RepoTools:
    def __init__(self, repo_path: str):
        self.root = Path(repo_path).resolve()

    def _safe(self, rel: str) -> Path:
        p = (self.root / rel).resolve()
        if not p.is_relative_to(self.root):
            raise ValueError("Path escapes repo")
        return p

    def list_files(self, subdir: str = ".") -> str:
        base = self._safe(subdir)
        files = [str(p.relative_to(self.root)) for p in base.rglob("*")
                 if p.is_file() and ".git" not in p.parts]
        return "\n".join(sorted(files)[:200])

    def read_file(self, path: str) -> str:
        return self._safe(path).read_text()[:20000]

    def search(self, pattern: str) -> str:
        # Pure Python search, so it also works on Windows (no grep needed)
        results = []
        for p in self.root.rglob("*"):
            if p.is_file() and ".git" not in p.parts and p.suffix in {".py", ".md", ".txt", ".toml", ".cfg", ".json"}:
                try:
                    for i, line in enumerate(p.read_text().splitlines(), 1):
                        if pattern in line:
                            results.append(f"{p.relative_to(self.root)}:{i}: {line.strip()}")
                except UnicodeDecodeError:
                    continue
        return "\n".join(results[:100]) or "No matches"

    def edit_file(self, path: str, old: str, new: str) -> str:
        p = self._safe(path)
        text = p.read_text()
        if text.count(old) != 1:
            return f"Error: 'old' must match exactly once (found {text.count(old)})"
        p.write_text(text.replace(old, new))
        return "Edit applied"

    def run_tests(self, cmd: str = "") -> str:
        # The `cmd` argument is ignored: tests always run the same safe way.
        code, out = run_pytest(self.root)
        if code >= 125:
            return f"Sandbox error (exit {code}): {out}"
        if code == 124:
            out += "\n(Tests were stopped because they ran too long.)"
        return out

import subprocess
from pathlib import Path


class RepoTools:
    def __init__(self, repo_path: str):
        self.root = Path(repo_path).resolve()

    def _safe(self, rel: str) -> Path:
        p = (self.root / rel).resolve()
        if not str(p).startswith(str(self.root)):
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

    def run_tests(self, cmd: str = "python -m pytest -x -q") -> str:
        r = subprocess.run(cmd.split(), cwd=self.root, capture_output=True,
                           text=True, timeout=120)
        return (r.stdout + r.stderr)[-4000:]
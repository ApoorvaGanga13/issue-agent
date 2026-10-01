import argparse
import difflib
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.append(".")
from agent.loop import run_agent

SKIP = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}


def changed_files(before: Path, after: Path):
    changed = []
    for p in sorted(after.rglob("*")):
        rel = p.relative_to(after)
        if not p.is_file() or set(rel.parts) & SKIP:
            continue
        old = before / rel
        try:
            new_text = p.read_text()
            old_text = old.read_text() if old.exists() else ""
        except UnicodeDecodeError:
            continue
        if new_text != old_text:
            changed.append(rel)
    return changed


def make_diff(before: Path, after: Path, files):
    out = []
    for rel in files:
        old = (before / rel).read_text() if (before / rel).exists() else ""
        new = (after / rel).read_text()
        out.extend(difflib.unified_diff(
            old.splitlines(keepends=True), new.splitlines(keepends=True),
            f"a/{rel}", f"b/{rel}",
        ))
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description="Run the issue agent on a repo.")
    ap.add_argument("repo", help="path to the repository")
    ap.add_argument("issue", help="issue text, or a path to a .txt file")
    ap.add_argument("--apply", action="store_true",
                    help="copy the fixed files back into the original repo")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        sys.exit(f"Not a folder: {repo}")
    issue = Path(args.issue).read_text() if Path(args.issue).is_file() else args.issue

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        work = Path(tmp) / "repo"
        shutil.copytree(repo, work, ignore=shutil.ignore_patterns(*SKIP))

        result = run_agent(str(work), issue)
        files = changed_files(repo, work)
        diff = make_diff(repo, work, files)

        print("\n=== SUMMARY ===")
        print(result["summary"])
        print(f"\nSteps used: {result['steps']}")
        print(f"Files changed: {', '.join(map(str, files)) or 'none'}")
        print("\n=== DIFF ===")
        print(diff or "(no changes)")

        if args.apply and files:
            for rel in files:
                dest = repo / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(work / rel, dest)
            print(f"\nApplied {len(files)} file(s) to {repo}")
        elif files:
            print("\nNothing was changed in your repo. Re-run with --apply to keep the fix.")


if __name__ == "__main__":
    main()

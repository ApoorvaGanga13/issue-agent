import difflib
import json
import re
from collections import defaultdict
from pathlib import Path

PATTERN = re.compile(
    r"^(?:(?P<tag>[a-z]+)_)?(?P<ver>v\d+)_(?:run(?P<run>\d+)_)?(?P<task>\d\d_.+)\.json$"
)


def edit_size(old, new):
    """Lines changed by one edit. A one-line change counts as 2 (one removed, one added)."""
    n = 0
    for line in difflib.ndiff(old.splitlines(), new.splitlines()):
        if line.startswith("+ ") or line.startswith("- "):
            n += 1
    return n


rows = defaultdict(list)  # (tag, version, task) -> [(lines changed, edit calls), ...]
for f in sorted(Path("evals/traces").glob("*.json")):
    m = PATTERN.match(f.name)
    if not m:
        continue
    tag = m["tag"] or "early"
    total, edits = 0, 0
    for e in json.loads(f.read_text()):
        if e["type"] == "tool" and e["tool"] == "edit_file" and e["output"].startswith("Edit applied"):
            total += edit_size(e["args"].get("old", ""), e["args"].get("new", ""))
            edits += 1
    rows[(tag, m["ver"], m["task"])].append((total, edits))

for tag in sorted({k[0] for k in rows}):
    versions = sorted({k[1] for k in rows if k[0] == tag})
    tasks = sorted({k[2] for k in rows if k[0] == tag})
    print(f"\n=== {tag}: average lines changed per run (edit calls per run) ===")
    print(f"{'task':<28}" + "".join(f"{v:<16}" for v in versions))
    for t in tasks:
        line = f"{t:<28}"
        for v in versions:
            vals = rows.get((tag, v, t))
            if vals:
                lines = sum(a for a, _ in vals) / len(vals)
                calls = sum(b for _, b in vals) / len(vals)
                line += f"{lines:.1f} ({calls:.1f})".ljust(16)
            else:
                line += "-".ljust(16)
        print(line)

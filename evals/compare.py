import json
from pathlib import Path

# Add more runs here later, as "label": "path"
FILES = {
    "v1 run1": "evals/results_v1.json",
    "v1 run2": "evals/results_v1_run2.json",
    "v2 (leaky)": "evals/results_v2.json",
    "v3 run1": "evals/results_v3_run1.json",
}


def mark(r):
    if r["solved"]:
        return "PASS"
    if r["visible_pass"] and not r["tampered"]:
        return "OVERFIT"
    return "FAIL"


runs = {}
for label, path in FILES.items():
    p = Path(path)
    if p.exists():
        runs[label] = {r["task"]: r for r in json.loads(p.read_text())}
    else:
        print(f"(missing: {path})")

tasks = sorted({t for run in runs.values() for t in run})
labels = list(runs)

print()
print(f"{'task':<24}" + "".join(f"{l:<13}" for l in labels))
for t in tasks:
    row = f"{t:<24}"
    for l in labels:
        row += f"{mark(runs[l][t]) if t in runs[l] else '-':<13}"
    print(row)

print()
for l in labels:
    res = list(runs[l].values())
    solved = sum(r["solved"] for r in res)
    over = sum(
        1 for r in res
        if not r["solved"] and r["visible_pass"] and not r["tampered"]
    )
    steps = [r["steps"] for r in res if r["steps"]]
    avg = sum(steps) / len(steps) if steps else 0
    print(
        f"{l:<13} solved {solved}/{len(res)} = {100 * solved / len(res):.0f}%"
        f"   overfit {over}   avg steps {avg:.1f}"
    )

import json
import re
from collections import defaultdict
from pathlib import Path

groups = defaultdict(dict)  # (tag, version) -> {run number: results}
for f in sorted(Path("evals/results").glob("*_run*.json")):
    m = re.match(r"(.+)_(v\d+)_run(\d+)\.json", f.name)
    if not m:
        continue
    tag, version, run = m.group(1), m.group(2), int(m.group(3))
    groups[(tag, version)][run] = json.loads(f.read_text())

for (tag, version), runs in sorted(groups.items()):
    print(f"\n=== {tag} / prompt {version} ({len(runs)} runs) ===")
    rates = []
    per_task = defaultdict(list)
    for run, res in sorted(runs.items()):
        solved = sum(r["solved"] for r in res)
        rates.append(100 * solved / len(res))
        print(f"  run {run}: {solved}/{len(res)} = {rates[-1]:.0f}%")
        for r in res:
            per_task[r["task"]].append(r["solved"])
    print(f"  mean {sum(rates) / len(rates):.0f}%   range {min(rates):.0f}%-{max(rates):.0f}%")
    for task, vals in sorted(per_task.items()):
        print(f"    {task:<28} solved {sum(vals)}/{len(vals)} runs")

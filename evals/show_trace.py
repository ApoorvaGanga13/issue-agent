import json
import sys
from pathlib import Path

name = sys.argv[1]
path = Path("evals/traces") / (name if name.endswith(".json") else name + ".json")
trace = json.loads(path.read_text())

for entry in trace:
    if entry["type"] == "text":
        print(f"\n[step {entry['step']}] MODEL SAID:\n{entry['text']}")
    else:
        args = json.dumps(entry["args"])[:300]
        print(f"\n[step {entry['step']}] TOOL {entry['tool']}({args})")
        print("  ->", entry["output"][:400].replace("\n", "\n     "))

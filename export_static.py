import json
import sys
from pathlib import Path

from fastapi import HTTPException

import app as server

SRC = Path("static/index.html")
OUT = Path("docs/index.html")

SHIM = """(function () {
  const DATA = __DATA__;
  const realFetch = window.fetch.bind(window);
  function reply(body, status) {
    return Promise.resolve(new Response(JSON.stringify(body), {
      status: status || 200,
      headers: { "Content-Type": "application/json" },
    }));
  }
  window.fetch = function (input, init) {
    const url = new URL(String(input), "http://static.local");
    if (url.pathname === "/api/examples") return reply(DATA.examples);
    if (url.pathname === "/api/results") return reply(DATA.results);
    if (url.pathname === "/api/replay") {
      const key = url.searchParams.get("task") + "|" + url.searchParams.get("version");
      if (DATA.replays[key]) return reply(DATA.replays[key]);
      return reply({ detail: "No saved run for this bug and prompt." }, 404);
    }
    if (url.pathname === "/api/run") {
      return reply({ detail: "Live runs need the local server. Use the replay button here." }, 400);
    }
    return realFetch(input, init);
  };
})();"""

ANCHORS = {
    "script": "<script>",
    "head": "</head>",
    "error": '<p id="error" class="error"></p>',
    "lede": "Pick a benchmark bug or paste your own code and tests. A run usually takes under a minute.",
    "footer": "This page is a local demo. It executes test code, so it is not meant to be hosted publicly.",
}

html = SRC.read_text(encoding="utf-8-sig")
missing = [name for name, anchor in ANCHORS.items() if anchor not in html]
if missing:
    sys.exit("Could not find these spots in static/index.html, so nothing was exported: " + ", ".join(missing))

data = {"examples": server.examples(), "results": server.results(), "replays": {}}
for ex in data["examples"]:
    for version in ("v1", "v3"):
        try:
            data["replays"][ex["name"] + "|" + version] = server.replay(ex["name"], version)
        except HTTPException:
            pass

payload = json.dumps(data).replace("</", "<\\/")
shim = SHIM.replace("__DATA__", payload)

static_css = "<style>\n#run, #tab-own, #panel-own { display: none !important; }\n</style>\n</head>"
note = (
    '<p id="error" class="error"></p>\n'
    '          <p class="caption">This is the read-only copy of the demo. The replays are real saved runs '
    "and no API calls are made. To run the agent live, clone the repo.</p>"
)
html = html.replace("<script>", "<script>" + shim + "</script>\n<script>", 1)
html = html.replace("</head>", static_css, 1)
html = html.replace(ANCHORS["error"], note, 1)
html = html.replace(ANCHORS["lede"], "Pick a benchmark bug and replay a saved run of either prompt.", 1)
html = html.replace(
    ANCHORS["footer"],
    "This is a read-only copy that replays saved runs and makes no API calls. The live version runs on your own machine.",
    1,
)

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html, encoding="utf-8")
(OUT.parent / ".nojekyll").write_text("")
print(f"Wrote {OUT}: {len(data['examples'])} bugs, {len(data['replays'])} saved replays, {OUT.stat().st_size // 1024} KB")

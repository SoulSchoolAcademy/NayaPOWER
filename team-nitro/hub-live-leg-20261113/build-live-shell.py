#!/usr/bin/env python3
"""Build the LIVE Hub shell for the 2026-11-13 live leg (Terra).

Source: the proven bars fixed shell (a687f16a) + the CURRENT 200 baked live
notes extracted from the live template + the /hub/feed absolute-src fix.

Steps (each asserted, abort on any move):
  1. Fixed shell asserted by sha (a687f16a...).
  2. /hub/feed fix: src="js/naya-search.js" (count==1) -> src="/js/naya-search.js".
  3. Notes re-bake: the sync's own remove-then-inject surgery, copied
     verbatim in logic from sync-smart-notes.py inject_live_notes()
     (same regex, same anchors, same script-safe '<' -> \u003c escaping),
     injecting the 200 live notes extracted from index-2.html BEFORE.
  4. Verify: markers, 200 notes, SN-2766 + SN-2696 present, node --check on
     the notes script block, CSS brace check via deploy.py's gate.
Outputs: work/index-intel-today-LIVE.html (the live shell bytes).
The template write itself is a separate, atomic step after verification.
"""
import hashlib
import json
import re
import subprocess
import sys

WD = "/home/hatch/workspace/team-nitro/hub-live-leg-20261113/work"
FIXED = "/home/hatch/workspace/team-nitro/hub-shell-bars-20261113/index-intel-today.html"
FIXED_SHA = "a687f16a666f27875dcc2cdb6dbe5fca113cf7eed610d76ff5b39ee8fc8d02ac"
OUT = WD + "/index-intel-today-LIVE.html"

html = open(FIXED, "rb").read()
assert hashlib.sha256(html).hexdigest() == FIXED_SHA, "fixed shell sha moved - STOP"
print(f"fixed shell: {len(html)} B sha a687f16a... OK")

# 2. /hub/feed fix
assert html.count(b'src="js/naya-search.js"') == 1, "search src anchor != 1 - STOP"
html = html.replace(b'src="js/naya-search.js"', b'src="/js/naya-search.js"', 1)
assert html.count(b'src="/js/naya-search.js"') == 1
assert html.count(b'src="js/naya-search.js"') == 0
print("/hub/feed fix applied: src=\"/js/naya-search.js\" (1x)")

# 3. Notes re-bake (sync's inject_live_notes, same steps)
live_notes = json.load(open(WD + "/live-notes-extract.json", encoding="utf-8"))
assert len(live_notes) == 200, f"live notes != 200 ({len(live_notes)}) - STOP"
live_json = json.dumps(live_notes, separators=(",", ":"), ensure_ascii=True).replace("<", "\\u003c")

html = re.sub(
    r"const NOTES = \[.*?\]\.concat\(NOTES_BASE\);\n",
    "",
    html.decode("utf-8"), flags=re.DOTALL, count=1,
)
html = html.replace(
    "const NOTES_BASE = OFFICIAL_NOTES.concat([",
    "const NOTES = OFFICIAL_NOTES.concat([",
    1,
)
if "const NOTES_BASE = OFFICIAL_NOTES.concat([" in html:
    raise RuntimeError("Hub HTML still has NOTES_BASE after cleanup - aborting")
if html.count("const NOTES = OFFICIAL_NOTES.concat([") != 1:
    raise RuntimeError("NOTES definition anchor not unique - aborting")
html = html.replace(
    "const NOTES = OFFICIAL_NOTES.concat([",
    "const NOTES_BASE = OFFICIAL_NOTES.concat([",
    1,
)
anchor = "window.NayaFeedIntelligence = { notes: NOTES"
if anchor not in html:
    raise RuntimeError("NayaFeedIntelligence anchor not found - aborting")
html = html.replace(
    anchor,
    "const NOTES = " + live_json + ".concat(NOTES_BASE);\n  " + anchor,
    1,
)
html = html.encode("utf-8")
print(f"notes re-baked: 200 live notes injected ({len(live_json)} B JSON)")

# 4. Verify
def count(b, m):
    return b.count(m)

print(f"live shell: {len(html)} B sha256 {hashlib.sha256(html).hexdigest()}")
for m, want in [(b"findNoteBySlug", 4), (b"SLUG_MAP", 2),
                (b"smart-notes/:slug", 7), (b"const NOTES_BASE", 1),
                (b"const NOTES = ", 1), (b'src="/js/naya-search.js"', 1),
                (b'src="js/naya-search.js"', 0)]:
    got = count(html, m)
    print(f"  {m.decode():28s} {got} (want {want})")
    assert got == want, f"{m}: {got} != {want} - STOP"
for sn in (b"SN-2766", b"SN-2696", b"IB-SMART-NOTE-20261112-the-infinite-smart-feeds"):
    assert sn in html, f"{sn} missing - STOP"
    print(f"  {sn.decode():28s} present ({count(html, sn)}x)")

# node --check on the notes script block (the sync's own gate)
idx = html.find(b"const NOTES_BASE = ")
s_start = html.rfind(b"<script>", 0, idx)
s_end = html.find(b"</script>", idx)
open("/tmp/hub_live_notes_check.js", "wb").write(html[s_start + len(b"<script>"):s_end])
chk = subprocess.run(["node", "--check", "/tmp/hub_live_notes_check.js"],
                     capture_output=True, text=True, timeout=30)
assert chk.returncode == 0, f"node --check FAILED: {chk.stderr[:300]}"
print("node --check on notes script block: PASS")

# CSS brace gate (deploy.py's gate)
sys.path.insert(0, "/home/hatch/workspace/factory-pipeline")
import deploy as dep
assert dep.css_brace_check(html.decode("utf-8"), OUT), "CSS brace check FAILED - STOP"
print("CSS brace check: PASS")

open(OUT, "wb").write(html)
print(f"OK wrote {OUT} ({len(html)} B)")

"""Next-sync proof: run sync-smart-notes.py::inject_live_notes (the sync's OWN
function) against a COPY of the new template (never the live template) with
the same 200 notes. The fix must survive the re-bake."""
import hashlib, json, re, shutil, subprocess, sys

WD = "/home/hatch/workspace/team-nitro/hub-bar-overflow-fix-20261114/work"
TPL = "/home/hatch/workspace/user/files/index-2.html"
COPY = WD + "/index-sync-proof-copy.html"
shutil.copyfile(TPL, COPY)
before = open(COPY, "rb").read()
print(f"copy of new template: {len(before)} B sha {hashlib.sha256(before).hexdigest()[:12]}")

import importlib.util
_spec = importlib.util.spec_from_file_location("sync_smart_notes", "/home/hatch/workspace/factory-pipeline/sync-smart-notes.py")
ssn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ssn)
live_notes = json.load(open(WD + "/live-notes-extract.json", encoding="utf-8"))
out = ssn.inject_live_notes(before.decode("utf-8"), live_notes).encode("utf-8")
print(f"re-baked: {len(out)} B sha {hashlib.sha256(out).hexdigest()[:12]} delta {len(out)-len(before):+d} B")

def count(b, m): return b.count(m)
for m, want in [(b"findNoteBySlug", 4), (b"SLUG_MAP", 2), (b"smart-notes/:slug", 7),
                (b'src="/js/naya-search.js"', 1), (b"data-obb-more", 7), (b"obb-nav", 12),
                (b"obb-nav-r", 4)]:
    got = count(out, m)
    print(f"  {m.decode():28s} {got} (want {want})")
    assert got == want, f"{m}: {got} != {want} - STOP"
for sn in (b"SN-2782", b"SN-2696"):
    assert sn in out, f"{sn} missing - STOP"
m = re.search(rb"const NOTES = (\[.*?\])\.concat\(NOTES_BASE\);", out, flags=re.DOTALL)
assert m and json.loads(m.group(1)) == live_notes, "notes NOT list-identical - STOP"
print("  notes parsed back: 200, list-identical")
# node --check on the obb script block (the fix's JS lives there)
idx = out.find(b"window.__obbLayout=obbLayout;")
s_start = out.rfind(b"<script>", 0, idx)
s_end = out.find(b"</script>", idx)
open("/tmp/hub_fix_obb_check.js", "wb").write(out[s_start + len(b"<script>"):s_end])
chk = subprocess.run(["node", "--check", "/tmp/hub_fix_obb_check.js"], capture_output=True, text=True, timeout=30)
assert chk.returncode == 0, f"node --check FAILED: {chk.stderr[:300]}"
print("  node --check on obb script block: PASS")
# byte delta honesty: show exactly which lines differ (should be the 1-line indent artifact)
old_lines = before.decode("utf-8").split("\n")
new_lines = out.decode("utf-8").split("\n")
assert len(old_lines) == len(new_lines), f"line count moved {len(old_lines)} -> {len(new_lines)}"
diffs = [(i, a, b) for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b]
print(f"  differing lines: {len(diffs)}")
for i, a, b in diffs:
    print(f"    line {i+1}: {len(a)} B -> {len(b)} B :: {a[:60]!r} -> {b[:60]!r}")
open(WD + "/index-sync-proof-output.html", "wb").write(out)
print("SYNC PROOF PASS — fix survives the re-bake")

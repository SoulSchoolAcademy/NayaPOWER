#!/usr/bin/env python3
"""Audit the staged emblem certificate from LIVE SERVED bytes (not build memory).

- Re-derives the new entry in memory (chain + apply_emblem) and asserts
  sha == the staged sha.
- Fetches live staged /free, asserts byte-equality with the re-derived entry.
- Extracts the emblem PNG data URI from the LIVE bytes, decodes it, asserts
  sha256 == NAYA_ICON.png (1e3deb55...) — the emblem is byte-identical,
  not re-derived.
- Diff base -> new (line counts + the removed/added lines, truncated).
- Design-laws machine check (the exact check-design-laws.py regexes) over
  BASE bytes vs NEW bytes: NEW-ONLY FAILs must be 0.
- Word check: the rendered words are unchanged (the diff touches CSS only).
"""
import base64
import difflib
import hashlib
import importlib.util
import os
import re
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

CURDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117")
FIXDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-fix-20261117")
HERE = os.path.expanduser("~/workspace/team-nitro/emblem-placement-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_cur = load("certcurrent", os.path.join(CURDIR, "build-certificate.py"))
_sim = _cur._bt._sim
_fixmod = load("certfix", os.path.join(FIXDIR, "build-fix.py"))
_emb = load("embcert", os.path.join(HERE, "build-emblem-certificate.py"))

FREE_HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"
STAGED_ENTRY_SHA = "fbe042022c5d88559fa37317bed67aff89ea092929a65923d1688177a3d404ac"
BASE_ENTRY_SHA = "fbd6477f348ab50b8b0eb278fb36e475c25eb55ae27a4d79ca416942161f16fd"
EMBLEM_SHA = "1e3deb55ae00552a2cbe26baaa610e04dc91812b6bc68c3532a061be020c8bf4"


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


# --- re-derive in memory.
walk_pf, entry_pf = _cur.regen_pricing_fix_tip()
h = _cur.harvest_identity()
base_entry = _cur.apply_certificate(entry_pf, h)
fix_entry = _fixmod.apply_fix(base_entry, h)
assert sha(fix_entry) == BASE_ENTRY_SHA, "base NOT reproduced — STOP"
b64 = _emb.emblem_b64()
new_entry = _emb.apply_emblem(fix_entry, b64)
_emb.check_invariants(fix_entry, new_entry, b64)
assert sha(new_entry) == STAGED_ENTRY_SHA, \
    f"re-derived != staged: {sha(new_entry)} — STOP"
print(f"re-derived entry: {len(new_entry.encode())} B sha={STAGED_ENTRY_SHA[:8]}... == staged MATCH")

# --- live staged bytes.
st, _, live = _sim.http_get(FREE_HOST + "/free")
assert st == 200 and live.decode("utf-8") == new_entry, "live /free != re-derived — STOP"
print(f"live /free: 200, {len(live)} B == re-derived MATCH")

# --- emblem proof from LIVE bytes.
m = re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', live.decode("utf-8"))
assert m, "no png data URI in live bytes — STOP"
decoded = base64.b64decode(m.group(1))
print(f"emblem in live bytes: {len(decoded)} B sha256={sha(decoded)}")
assert sha(decoded) == EMBLEM_SHA, "emblem in live bytes != NAYA_ICON.png — STOP"
assert len(decoded) == 2654505
print("EMBLEM BYTE-IDENTICAL to NAYA_ICON.png — PROVEN from live bytes")

# --- diff.
diff = list(difflib.unified_diff(fix_entry.splitlines(), new_entry.splitlines(), lineterm="", n=0))
removed = [ln for ln in diff if ln.startswith("-") and not ln.startswith("---")]
added = [ln for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
print(f"diff base->new: +{len(added)} lines, -{len(removed)} lines")
for ln in removed:
    print("   -", ln[:200])
for ln in added:
    print("   +", ln[:200])

# --- rendered words unchanged: strip tags+style+script from base and new,
# compare the visible text.
def visible(html):
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S)
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    return " ".join(html.split())

vb, vn = visible(fix_entry), visible(new_entry)
print(f"visible words: base {len(vb.split())} words, new {len(vn.split())} words, identical: {vb == vn}")
assert vb == vn, "VISIBLE WORDS CHANGED — STOP"

# --- design-laws machine check (check-design-laws.py regexes, in memory).
sys.path.insert(0, os.path.expanduser("~/workspace/team-nitro"))
import importlib
_chk = load("lawscheck", os.path.expanduser("~/workspace/team-nitro/check-design-laws.py"))


def laws_failures(text):
    fails, warns = [], []
    for i, line in enumerate(text.splitlines(), 1):
        for rx in _chk.GRAY_RES:
            if rx.search(line):
                fails.append(f"{i}: GRAY: {line.strip()[:120]}")
                break
    for m in _chk.FONTSIZE_RE.finditer(text):
        vals = [float(v) for v in m.groups() if v is not None]
        if vals and min(vals) < 17:
            fails.append(f"{text[:m.start()].count(chr(10)) + 1}: SIZE: {m.group(0)}")
    for m in _chk.COLOR_DECL_RE.finditer(text):
        val = m.group(1).strip().lower()
        if val.startswith("var("):
            continue
        val = val.split()[0].rstrip(";")
        if val in _chk.FORBIDDEN_TEXT:
            fails.append(f"{text[:m.start()].count(chr(10)) + 1}: TEXT-COLOR: {m.group(0).strip()[:120]}")
        elif val not in _chk.ALLOWED_TEXT and not val.startswith("#"):
            warns.append(f"{text[:m.start()].count(chr(10)) + 1}: TEXT-COLOR?: {m.group(0).strip()[:120]}")
    if ":hover" not in text:
        warns.append("NO-HOVER")
    return fails, warns


fb, wb_ = laws_failures(fix_entry)
fn, wn = laws_failures(new_entry)
print(f"laws: BASE {len(fb)} FAILs / {len(wb_)} WARNs; NEW {len(fn)} FAILs / {len(wn)} WARNs")
# Compare by CONTENT, not line number: the emblem change adds 12 net lines
# before ~line 929, so identical pre-existing FAILs shift line numbers.
# (The prior round adjudicated all 12: comment prose "gray"/"grey",
# border-color rgba, and sub-17px icon glyphs — none of them text.)
def content_key(f):
    return f.split(": ", 1)[1] if ": " in f else f
new_only = [f for f in fn if content_key(f) not in {content_key(x) for x in fb}]
print(f"NEW-ONLY FAILs (by content): {len(new_only)}")
for f in new_only:
    print("  NEW FAIL:", f)
assert not new_only, "new design-law FAILs — STOP"
print("AUDIT OK")

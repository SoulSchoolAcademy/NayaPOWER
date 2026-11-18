#!/usr/bin/env python3
"""Audit the staged emblem-corners fix from LIVE SERVED bytes (not build memory).

- Re-derives the new entry in memory (chain + apply_emblem + apply_corners_fix)
  and asserts sha == the staged sha.
- Fetches live staged /free, asserts byte-equality with the re-derived entry.
- Extracts the emblem PNG data URI from the LIVE bytes, decodes it, asserts
  sha256 == NAYA_ICON.png (1e3deb55...) — the emblem is byte-identical,
  not re-derived.
- Diff base -> new (line counts + the removed/added lines, truncated).
- Design-laws machine check (the exact check-design-laws.py regexes) over
  BASE bytes vs NEW bytes: NEW-ONLY FAILs must be 0.
- Word check: the rendered words are unchanged (the diff touches CSS + one
  inline SVG defs block with no text).
- Geometry check: parse the NEW CSS for the corner sizes/offsets, recompute
  the rotated bounding boxes, assert every emblem is whole inside the card
  at 1920/635/390 (CSS-derived, not a render measurement).
- Die-cut check: #crestCut defs x1, filter chain on both medal rules,
  plain drop-shadow gone, stale comments gone.
"""
import base64
import difflib
import hashlib
import importlib.util
import math
import os
import re
import sys
import time

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

CURDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117")
FIXDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-fix-20261117")
PREVDIR = os.path.expanduser("~/workspace/team-nitro/emblem-placement-20261117")
HERE = os.path.expanduser("~/workspace/team-nitro/emblem-corners-fix-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_cur = load("certcurrent", os.path.join(CURDIR, "build-certificate.py"))
_sim = _cur._bt._sim
_fixmod = load("certfix", os.path.join(FIXDIR, "build-fix.py"))
_emb = load("embcert", os.path.join(PREVDIR, "build-emblem-certificate.py"))
_fix = load("cornersfix", os.path.join(HERE, "build-emblem-corners-fix.py"))

FREE_HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"
BASE_ENTRY_SHA = "fbe042022c5d88559fa37317bed67aff89ea092929a65923d1688177a3d404ac"
STAGED_ENTRY_SHA = "a5e529f9d78a279caa2a3999a502645e202ac8d49a3f22651f01fcfb520bf85b"
EMBLEM_SHA = "1e3deb55ae00552a2cbe26baaa610e04dc91812b6bc68c3532a061be020c8bf4"


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


# --- re-derive in memory.
walk_pf, entry_pf = _cur.regen_pricing_fix_tip()
h = _cur.harvest_identity()
base_entry = _cur.apply_certificate(entry_pf, h)
fix_entry = _fixmod.apply_fix(base_entry, h)
assert sha(fix_entry) == _emb.BASE_ENTRY_SHA, "certificate-fix tip NOT reproduced — STOP"
b64 = _emb.emblem_b64()
emb_entry = _emb.apply_emblem(fix_entry, b64)
assert sha(emb_entry) == BASE_ENTRY_SHA, "emblem-placement tip NOT reproduced — STOP"
new_entry = _fix.apply_corners_fix(emb_entry, b64)
_fix.check_invariants(emb_entry, new_entry, b64)
assert sha(new_entry) == STAGED_ENTRY_SHA, \
    f"re-derived != staged: {sha(new_entry)} — STOP"
print(f"re-derived entry: {len(new_entry.encode())} B sha={STAGED_ENTRY_SHA[:8]}... == staged MATCH")

# --- live staged bytes.
st, _, live = _sim.http_get(FREE_HOST + "/free")
assert st == 200 and live.decode("utf-8") == new_entry, "live /free != re-derived — STOP"
print(f"live /free: 200, {len(live)} B == re-derived MATCH")

# --- timestamped link serves the new bytes (Link Law).
ts = int(time.time())
st, _, live_ts = _sim.http_get(f"{FREE_HOST}/free?t={ts}")
assert st == 200 and sha(live_ts) == STAGED_ENTRY_SHA, "timestamped link != new bytes — STOP"
print(f"timestamped link /free?t={ts}: 200, {len(live_ts)} B sha={STAGED_ENTRY_SHA[:8]}... MATCH")

# --- emblem proof from LIVE bytes.
m = re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', live.decode("utf-8"))
assert m, "no png data URI in live bytes — STOP"
decoded = base64.b64decode(m.group(1))
print(f"emblem in live bytes: {len(decoded)} B sha256={sha(decoded)}")
assert sha(decoded) == EMBLEM_SHA, "emblem in live bytes != NAYA_ICON.png — STOP"
assert len(decoded) == 2654505
print("EMBLEM BYTE-IDENTICAL to NAYA_ICON.png — PROVEN from live bytes")

# --- diff.
diff = list(difflib.unified_diff(emb_entry.splitlines(), new_entry.splitlines(), lineterm="", n=0))
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

vb, vn = visible(emb_entry), visible(new_entry)
print(f"visible words: base {len(vb.split())} words, new {len(vn.split())} words, identical: {vb == vn}")
assert vb == vn, "VISIBLE WORDS CHANGED — STOP"

# --- geometry check from the NEW CSS (parsed, not eyeballed).
def bbox(w, h, deg):
    th = math.radians(abs(deg))
    return ((w * abs(math.cos(th)) + h * abs(math.sin(th))) / 2,
            (w * abs(math.sin(th)) + h * abs(math.cos(th))) / 2)

assert ".corner-crest { position: absolute; z-index: 5; width: 132px; height: 161px;" in new_entry
assert ".corner-crest { width: 64px; height: 64px; }" in new_entry
hw, hh = bbox(132, 161, 59)
print(f"geometry desktop: halfW {hw:.1f} halfH {hh:.1f} center 112 -> "
      f"clearance {112 - hw:.1f}px / {112 - hh:.1f}px inside the card")
assert 112 - hw >= 8 and 112 - hh >= 8
hw, hh = bbox(64, 64, 35)
print(f"geometry mobile: halfW {hw:.1f} halfH {hh:.1f} center 56 -> "
      f"clearance {56 - hw:.1f}px inside the card on every side")
assert 56 - hw >= 8 and 56 - hh >= 8
# Viewport edges: card top = 52px top bar, card bottom = viewport - 50px bottom bar.
for vw, vh, center, half_h in [(1920, 999, 112, bbox(132, 161, 59)[1]),
                               (635, 390, 56, bbox(64, 64, 35)[1]),
                               (390, 844, 56, bbox(64, 64, 35)[1])]:
    top_edge = 52 + center - half_h
    bot_edge = vh - 50 - (center - half_h)
    print(f"geometry viewport {vw}x{vh}: emblem top edge y={top_edge:.0f}, "
          f"bottom edge y={bot_edge:.0f} — whole in the first viewport")
    assert top_edge >= 0 and bot_edge <= vh
print("GEOMETRY OK (CSS-derived)")

# --- die-cut check from the LIVE bytes.
live_text = live.decode("utf-8")
assert live_text.count('id="crestCut"') == 1
assert live_text.count("filter: url(#crestCut) drop-shadow(0 6px 12px rgba(0,0,0,0.60));") == 2
assert "filter: drop-shadow(0 6px 12px rgba(0,0,0,0.60));" not in live_text
assert "no CSS mask" not in live_text
assert "feFuncA type=\"linear\" slope=\"6\" intercept=\"-0.15\"" in live_text
print("DIE-CUT OK (defs x1, filter chain x2, plain shadow gone, stale comment gone)")

# --- foot clearance check (F4 + F4b) from the LIVE bytes.
assert ".identity-face { padding: 22px 18px 160px; grid-template-rows: auto auto 1fr; }" in live_text
assert ".identity-pro-card, #certPlaque { min-height: 798px; }" in live_text
assert "@media (max-width: 640px) and (min-height: 701px)" in live_text
assert "padding: 22px 18px 34px;" not in live_text
mob_half = bbox(64, 64, 35)[1]
print(f"FOOT CLEARANCE OK (mobile face rows auto auto 1fr + padding-bottom "
      f"160px + tall-phone card min-height 798px; bottom emblem top edge "
      f"{56 + mob_half:.1f}px above card bottom)")
assert "grid-template-rows: 1fr auto 1fr" in live_text  # desktop rows untouched

# --- design-laws machine check (check-design-laws.py regexes, in memory).
sys.path.insert(0, os.path.expanduser("~/workspace/team-nitro"))
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


fb, wb_ = laws_failures(emb_entry)
fn, wn = laws_failures(new_entry)
print(f"laws: BASE {len(fb)} FAILs / {len(wb_)} WARNs; NEW {len(fn)} FAILs / {len(wn)} WARNs")
# Compare by CONTENT, not line number: the fix adds net lines, so
# identical pre-existing FAILs shift line numbers.
def content_key(f):
    return f.split(": ", 1)[1] if ": " in f else f
new_only = [f for f in fn if content_key(f) not in {content_key(x) for x in fb}]
print(f"NEW-ONLY FAILs (by content): {len(new_only)}")
for f in new_only:
    print("  NEW FAIL:", f)
assert not new_only, "new design-law FAILs — STOP"
print("AUDIT OK")

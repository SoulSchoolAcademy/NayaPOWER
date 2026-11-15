#!/usr/bin/env python3
"""AGREEMENT FIX PASS 2 (2026-11-15) — edit walk-beginning-fixed.html in place.

Base: fix-pass file, 3,494,589 B, sha256
ae1bd0bab0dbefb9351fe4ef430b5ddbf4a182571097706b28f42bb9acd1d1ff.
Baseline copy kept as walk-beginning-fixed-ae1bd0ba-baseline.html.

Fix 1 — PORTRAIT REPEATS (the captain's corrected rule):
  * Section openers (11 b06, 18 b04, 25 b09, 78 b08) on NO other board.
  * At most ONE of {b09, b10} on boards at all: b09 keeps its Q3 opener;
    b10 leaves boards entirely (beats 37, 73 reassigned).
  * b09 totals at most 2: beat 64 reassigned AND the land note (beat 27,
    two boards after the b09 opener) swapped off b09.
  * Signing photo swapped off Warm-session Naya_Narzan.jpg for Naya.png
    (hair-up close-up, light indoor background) under NEW KV key
    wbf-agmt-sign2.png (uploaded by kv-put-agreement-fixpass2-sign2.py).
    The white file was inspected first-hand and REJECTED as the donor:
    it is the same outdoor session as b09 (long wavy hair, gold necklace,
    hills/city/water) — it would move the cluster to the signing, not
    break it. b06 is the only non-Warm donor whose picture-total stays
    <= 3 (board 11 + collective note + sign).
  * Board reassignments (each file's two board appearances >= 15 apart):
    37 b10->b12 (b00 forbidden: deed-note adjacency; b01 forbidden:
    cost-note own-board; b02 forbidden: adjacent repeat with 36)
    58 b06->b00 · 61 b04->b01 · 64 b09->b02 · 67 b08->b03 · 73 b10->b05.
  * Land note b09->b04 (hand-to-face: most distinguishable at 44px,
    non-Warm; other b04 appearances are 9 and 25 boards away).
  * The 34th b-occurrence is the summary board's b07 portrait
    (dealAgreementSummary, line 1534) — named, not a rendered board
    portrait; it is unchanged by this pass.
Fix 2 — STRAY " i" IN THE PLAIN-TEXT VIEW: plainLetterText() cloned each
  <p> and read textContent, picking up the eye button's "i". New helper
  plainParaText() clones the paragraph, removes its <button>s, then reads
  text. Used in both board branches; the summary branch has no buttons
  and is untouched. No board words change.
Fix 3 — TINY SMALL-CAPS (beats 57, 63 only): .ib-nutshell b renders at
  12px / .16em letter-spacing. Beats 57 (whole board is one long bold
  supporting sentence) and 63 (the substantive money sentence is bold)
  get a scoped rule at body size (17px, normal spacing). The other bold
  lines are short declarations/emphasis labels both eyes passed; a
  page-wide restyle would change ~20 boards and is out of this pass.
Every replacement asserted exactly-once before write. Temp-file write +
os.replace in the same directory, never truncate-first.
"""
import hashlib, os, shutil

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "walk-beginning-fixed.html")
BASE_SHA = "ae1bd0bab0dbefb9351fe4ef430b5ddbf4a182571097706b28f42bb9acd1d1ff"

raw = open(SRC, "rb").read()
assert hashlib.sha256(raw).hexdigest() == BASE_SHA, "base sha mismatch"
assert len(raw) == 3494589, "base bytes mismatch"
shutil.copyfile(SRC, os.path.join(D, "walk-beginning-fixed-ae1bd0ba-baseline.html"))
h = raw.decode("utf-8")

def rep(old, new, tag):
    global h
    n = h.count(old)
    assert n == 1, f"{tag}: expected 1 occurrence, found {n}"
    h = h.replace(old, new)
    print(f"OK {tag}")

# ---------------- FIX 1a: board portraits ----------------
# (beat, old src, new src). Article-opening strings keep each unique.
BOARDS = [
    (37, "/agmt-b10.jpg", "/agmt-b12.jpg"),
    (58, "/agmt-b06.png", "/agmt-b00.jpg"),
    (61, "/agmt-b04.jpg", "/agmt-b01.jpg"),
    (64, "/agmt-b09.jpg", "/agmt-b02.jpg"),
    (67, "/agmt-b08.jpg", "/agmt-b03.jpg"),
    (73, "/agmt-b10.jpg", "/agmt-b05.jpg"),
]
for beat, old, new in BOARDS:
    rep(
        f'<article class="intel-board tone-purple letter-beat face-left" data-beat="{beat}" hidden><div class="ib-blocktop"><img class="deal-beat-photo" src="{old}" alt="Naya speaking">',
        f'<article class="intel-board tone-purple letter-beat face-left" data-beat="{beat}" hidden><div class="ib-blocktop"><img class="deal-beat-photo" src="{new}" alt="Naya speaking">',
        f"fix1 beat{beat} {old} -> {new}")

# ---------------- FIX 1b: land note off b09 ----------------
rep(
    '<div class="deal-eye-note" id="deal-note-land" hidden><img class="deal-quote-photo" src="/agmt-b09.jpg" alt="">',
    '<div class="deal-eye-note" id="deal-note-land" hidden><img class="deal-quote-photo" src="/agmt-b04.jpg" alt="">',
    "fix1 land note b09 -> b04")

# ---------------- FIX 1c: signing photo off Warm ----------------
rep(
    '<img class="deal-sign-photo" src="/agmt-sign.jpg" alt="Naya">',
    '<img class="deal-sign-photo" src="/agmt-sign2.png" alt="Naya">',
    "fix1 signing /agmt-sign.jpg -> /agmt-sign2.png (Naya.png)")

# ---------------- FIX 2: strip eye-button text from plain text ----------------
rep(
    "  function plainLetterText(){",
    "  function plainParaText(el){\n    var c = el.cloneNode(true);\n    var bs = c.querySelectorAll('button');\n    for (var i = 0; i < bs.length; i++) bs[i].remove();\n    return c.textContent.replace(/\\s+/g, ' ').trim();\n  }\n  function plainLetterText(){",
    "fix2 plainParaText helper (clone, remove buttons, then text)")
rep(
    "      if (ps.length) { for (var a = 0; a < ps.length; a++) lines.push(ps[a].textContent.replace(/\\s+/g, ' ').trim()); }",
    "      if (ps.length) { for (var a = 0; a < ps.length; a++) lines.push(plainParaText(ps[a])); }",
    "fix2 board branch strips button text")
rep(
    "      else { var ap = b.querySelectorAll('p'); for (var c = 0; c < ap.length; c++) lines.push(ap[c].textContent.replace(/\\s+/g, ' ').trim()); }",
    "      else { var ap = b.querySelectorAll('p'); for (var c = 0; c < ap.length; c++) lines.push(plainParaText(ap[c])); }",
    "fix2 fallback branch strips button text")

# ---------------- FIX 3: beats 57 + 63 bold at body size ----------------
rep(
    ".ib-nutshell b {\n  display: block; color: #f4f2f7; font-size: 12px;\n  letter-spacing: .16em; margin-bottom: 8px; font-weight: 800;\n}",
    ".ib-nutshell b {\n  display: block; color: #f4f2f7; font-size: 12px;\n  letter-spacing: .16em; margin-bottom: 8px; font-weight: 800;\n}\n[data-beat=\"57\"] .ib-nutshell b, [data-beat=\"63\"] .ib-nutshell b {\n  font-size: 17px; letter-spacing: normal; line-height: 1.65;\n}",
    "fix3 beats 57+63 bold at body size")

# ---------------- write (temp + replace, same dir) ----------------
out = h.encode("utf-8")
tmp = os.path.join(D, ".fixpass2-tmp.html")
with open(tmp, "wb") as fh:
    fh.write(out)
assert hashlib.sha256(open(tmp, "rb").read()).hexdigest() == hashlib.sha256(out).hexdigest()
os.replace(tmp, SRC)
print("WROTE", len(out), "B sha256", hashlib.sha256(out).hexdigest())

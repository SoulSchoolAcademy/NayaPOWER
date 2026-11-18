#!/usr/bin/env python3
"""Maker #2 — agreement intro layout follow-on (Shawn's eye 04:16Z).
Five changes to the /agreement file ONLY (base blob 5afcbc4a, 88,277 B):
 1. Center beat 1's picture (new CSS rule, scoped data-beat="1").
 2. Remove beat 1's diamond + THE OPENING / Hi, I'm Naya header (duplicate).
 3. Remove the voice line (line 295).
 4. Move the dots row + read-it-all link to below the letter (after #deckBody).
 5. Top becomes: title, play button, centred picture, letter. (Follows from 1-4.)
Writes the output file itself (never stdout-redirected). Verifies by sha.
"""
import hashlib

SRC = "/home/hatch/workspace/team-nitro/agreement-buttons-20261118/work/agreement2/agreement2-base.html"
OUT = "/home/hatch/workspace/team-nitro/agreement-buttons-20261118/work/agreement2/agreement2-new.html"
BASE_SHA = "14bd698cc1a666b665258a212a934d439a374733e2523d929c9f0e340a35c31f"

raw = open(SRC, "rb").read()
assert hashlib.sha256(raw).hexdigest() == BASE_SHA, "base sha mismatch"
assert len(raw) == 88277, "base size mismatch"
text = raw.decode("utf-8")
lines = text.split("\n")

# --- Edit 3: remove the voice line (base L295) ---
VOICE = '<p class="play-note">Her voice reads this aloud once the words are final &mdash; for now, read along with Naya.</p>'
assert text.count(VOICE) == 1, "voice line count != 1"
vi = next(i for i, l in enumerate(lines) if l == VOICE)
del lines[vi]

# --- Edit 2: remove beat 1's identity header (base L302) ---
IDENT = '<div class="ib-identity"><span class="ib-jewel" aria-hidden="true">&#9670;</span><div><span class="ib-kind">THE OPENING</span><h2 class="ib-title">Hi, I&#x27;m Naya</h2></div></div>'
assert text.count(IDENT) == 1, "identity substring count != 1"
bi = next(i for i, l in enumerate(lines) if l.startswith('<article class="intel-board letter-beat" data-beat="1"'))
assert IDENT in lines[bi], "identity not in beat 1 line"
assert lines[bi].count("THE OPENING") == 1
lines[bi] = lines[bi].replace(IDENT, "")
assert "THE OPENING" not in lines[bi]
assert lines[bi].count('<div class="ib-blocktop"><img class="deal-beat-photo"') == 1

# --- Edit 4: move the controls block (base L297-300) to below the letter ---
ci = next(i for i, l in enumerate(lines) if l.startswith('<div class="letter-controls" id="deckControls">'))
assert lines[ci + 1].startswith('<div class="letter-dots" id="deckDots"')
assert lines[ci + 2] == '<button class="letter-all" id="deckAll" type="button">or read the whole agreement at once</button>'
assert lines[ci + 3] == "</div>"
block = lines[ci:ci + 4]
del lines[ci:ci + 4]
# insertion point: the line closing #deckBody (right after the beat-47 article)
b47 = next(i for i, l in enumerate(lines) if l.startswith('<article class="intel-board letter-beat" data-beat="47"'))
assert lines[b47 + 1] == "</div>", "deckBody close not after beat 47"
assert lines[b47 + 2].startswith('<p class="foot-links">')
MOVE_NOTE = "<!-- AGREEMENT INTRO LAYOUT FOLLOW-ON #2 (2026-11-18, Shawn's eye 04:16Z): the dots + read-it-all row moved here from the top, below the letter — same ids, same handlers, same destinations. -->"
lines[b47 + 2:b47 + 2] = [MOVE_NOTE] + block

# --- Edit 1: center beat 1's picture (CSS, after the .lead photo rule, base L75) ---
ANCHOR = ".letter-beat.lead .deal-beat-photo{border-color:rgba(142,36,170,.7);box-shadow:0 0 22px rgba(142,36,170,.55),0 8px 20px rgba(0,0,0,.6)}"
ai = next(i for i, l in enumerate(lines) if l == ANCHOR)
CSS = [
    "/* AGREEMENT INTRO LAYOUT FOLLOW-ON #2 (2026-11-18, Shawn's eye 04:16Z):",
    "   beat 1's picture sits CENTRED — the play button above it is already",
    "   centred, so the picture aligns down the middle. Beat 1's blocktop now",
    "   holds only the portrait (its identity header was removed as a duplicate",
    "   of the letter's first line), and margin:auto centres the portrait in",
    "   both layouts: the desktop row (space-between + auto margins) and the",
    "   phone column at 640px (align-items:stretch + auto margins). Scoped to",
    "   data-beat=\"1\" only — the other portraits (beats 6, 10, 20, 42, 45) keep",
    "   their left flank. */",
    '.letter-beat[data-beat="1"] .deal-beat-photo{margin:0 auto}',
]
lines[ai + 1:ai + 1] = CSS

out = "\n".join(lines)
open(OUT, "w", encoding="utf-8").write(out)
print("wrote", OUT, len(out.encode("utf-8")), "bytes sha", hashlib.sha256(out.encode("utf-8")).hexdigest())

# THE EPIC ENGINE — the Factory's auto-format step
## Epic fold-in (Shawn's ruling, 2026-11-17 03:35Z — "make it one")

The Intelligent Block Epic formatting does NOT live as a standalone app. It
lives IN the Smart Factory as the auto-format step. The Factory survey asks
the questions we already know — mission, vision, goal, skill, plus the
walk's ten questions — the citizen walks through and answers, and those
answers produce the pages, formatted beautiful by the Epic engine. Anything
pasted in when they enter NayaNET — when they first get their pages, or when
they add a new page in the Factory — comes out beautiful because the pages
were already created beautiful. The standalone Epic page is retired as a
destination; its only surviving surface is the paste-anything engine inside
the Factory (and wherever pasting happens — the feed, the pages).

## The engine (stored here)

| | |
|---|---|
| File | `epic-auto-format.html` (this directory) |
| GitHub blob (full sha) | `3a4b0bf8b2e2f29fe5b956d5d6ca04e6f8c2baef` |
| Bytes | 81,357 |
| sha256 | `158d5e58504e915655f7955ac6c506ce1a514c1d572bc693d0d8fc40f9dbd045` |
| Source branch | `intelligent-block/epic-20261117` |
| Source commit | `3920de9f41dbd8bebb6b3faf442b99c92c39572c` |
| Source PR | #3390 (open, unmerged — its bytes are the harvest source; whether it merges or closes is Shawn's hand) |

Verified: the blob was re-read through the git blob API and byte-compared
(size + sha256 + git-blob sha all match the stored file). The local Epic
work copy (`~/workspace/team-nitro/intelligent-block-epic-20261117/
intelligent-block-epic.html`) is the same bytes. Nothing in the engine was
re-created, re-typed, or remade from a picture — the file IS the filed
bytes, copied into the Factory's vault shelf.

**FIX ROUND 2026-11-17 (fold-in fix, PR #3395): the stored engine is no
longer byte-identical to the Epic source.** The captain's eye failed the
survey proof page: the distiller's nutshell took the first 7 words and cut
4 of 10 headlines off mid-phrase ("in the", "and", "the new internet,",
"who"). The Factory's copy repairs `titleFrom` — the nutshell now ends at
a phrase boundary (a comma, semicolon, colon or dash, or just before a word
that opens a new clause), never mid-phrase, never with trailing
punctuation. That repair is the ONLY change to the engine bytes in this
round; the Epic branch (PR #3390) was not touched — the engine's home is
the Factory now, and the repair lives here, in the Factory's copy. The
table above is the FIXED engine (blob `3a4b0bf8…`, 81,357 B); the Epic
source stays blob `4319256d…`, 77,758 B.

What the engine is (from its own maker report + the code, read, not
assumed): the canonical slideshow (style block byte-identical to blob
`21d08a88`, `wireReveal`/`showSlide`/`setFormat` untouched) plus ONE epic
layer — the living digit tiles (Dashboard `miniTileHTML` +
`_osMiniNumHTML`, Deep Palette digits, lift + ignite on hover/tap, flip
into new values on change, slow orbit ring 60s ambient / 18s hover), the
best buttons (BTN-026 orbit buttons, whole-page), and the paste-anything
distiller (text → boards, nutshell first, one idea per board, max 3
sentences per board, max 3 boards; smart-note seam-strip; image BECOMES
the board, full-bleed, rimmed, lit). Its eye PASSED 03:34Z 2026-11-17
(paste text/note/image all beautiful, numbers alive, self-check 10/10).

## Known loose ends (carried forward, NOT silently fixed here)

From the Epic round, named in the brief and the maker report:

- "15/15" buttons is 14 rendered + 1 template string.
- `_osMiniNumHTML` trimmed, not byte-verbatim.
- `miniTileHTML` re-indented.
- A wrapped continuation starting with a capital or digit splits (the
  stop-word guard is a follow-on, not this round).

None of these were touched in the fold-in. If the checker finds one of them
biting in the Factory, that is a follow-on round with its own brief — never
a silent fix inside this one.

## How the builder uses it

`factory.py` carries the `EPIC` table (filename + blob sha + byte size +
sha256 + source branch/commit/PR) and two functions, mirroring the format
step exactly:

- `load_epic_bytes()` — reads the stored bytes, verifies size + sha256; a
  mismatch is a hard stop before the gate, before anything ships.
- `emit_epic(out_dir, receipt)` — writes the bytes verbatim into the build
  output dir on EVERY build, next to the two canonical formats. The receipt
  carries the `epic` entry (`label` + `vault` + source) on every build — a
  labeled, inventoried vault asset, like the formats.

A new engine version arrives ONLY as a new filed file from its own round —
never by editing the stored bytes in place. Replace the file, update the
`EPIC` table AND the row in `FORMATS.md` AND this file in the same pass,
re-run the verify below, and file.

## The survey — ten answers in, a beautiful page out

The `epic-survey` wiring (`factory.py`: `build_epic_survey_page()`; spec
`specs/epic-survey.json`; harness `epic-distill-harness.js`) is the second
half of the fold-in: the Factory survey wired to page production through
the engine.

**The survey is the walk's ten questions generalized.** The questions are
the walk's, verbatim (Q1 who you are · Q2 what you're into and why · Q3
vision · Q4 mission · Q5 motto · Q6 goal for your life · Q7 what you do ·
Q8 what you offer · Q9 what you're building and its goal · Q10 what kind
of space you want and who you want to meet there). The mapping is the
walk's own ("How these answers fill your pages" in
`NAYAS-EXAMPLE-ANSWERS-20261112.md`): About = Q1/Q2/Q5/Q6, the vision +
mission thread (Q3/Q4) runs through all three, Skills = Q7/Q8/Q9, and
the Space = Q10 alone. The skill is Q7 + Q8 — what they do and what they offer;
the walk has no separate skill question, and none was invented.

**The citizen in the proof is Naya herself.** The spec's answers are her
Warm & Plain (style A) answers, verbatim from
`NAYAS-EXAMPLE-ANSWERS-20261112.md` — the canonical example citizen.
Nothing in the proof is invented.

**The engine does the formatting — the builder never formats by itself.**
At build time the harness (`epic-distill-harness.js`) reads the stored
engine bytes, extracts the canonical + epic `<script>` blocks, evaluates
them in Node under a minimal DOM stub, and calls the engine's OWN
`distill()` + `boardHTML()` (+ `epicImageBoard()` for the image,
`_osMiniNumHTML()` for the tiles) with an export line appended INSIDE the
epic IIFE in memory only — the filed bytes are untouched. The builder
bakes the returned boards into the page. The builder writes no board, no
sentence split, no seam-strip of its own.

**The built page IS the engine page.** The survey proof page
(`out/epic-survey-proof.html`) is the engine file byte-identical except
for Factory work, each piece wrapped in a
`<!-- FACTORY EPIC FOLD-IN BEGIN x --> ... <!-- FACTORY EPIC FOLD-IN END x -->`
span (audit block in `<head>`; hero retitled to the citizen; dots extended
to the full deck; a deck-next button on the studio beat; the citizen's 7
beats after the studio beat; the 3 paste proofs baked into
`#epicResultsBody`; a provenance board; a wiring script for the baked
result buttons), plus three exact replacements (hero text, dots,
results-empty note) that the verifier reverses by fixed strings. The deck
is 10 beats — 3 from the engine, 7 from her answers (About 3, thread 1,
Skills 2, Space 1) — tones running the spectrum flow in order, never twice
in a row. The paste-anything studio stays LIVE in the page: pressing
"Make it beautiful" replaces the baked proofs with the citizen's own paste,
through the engine's own `makeBeautiful`.

**Verify (anyone, cold):**

```sh
cd ~/workspace/team-nitro/interface-factory
python3 factory.py specs/epic-survey.json --out out/epic-survey-proof.html --no-gate
python3 ../factory-epic-fold-in-20261117/verify_fix.py
```

`verify_fix.py` runs the fold-in checks plus the fix-round checks (all 10
deck headlines end at a phrase boundary; the lighthouse paste distills to
a complete headline; the provenance line stays true after a paste),
including the strip test: the built page minus every Factory span, with
the three replacements reversed, equals the stored engine bytes EXACTLY
(81,060 chars). A build whose insertions do not strip clean is a failed build. (The
fold-in round's `verify_foldin.py` checks the same shape against the OLD
engine values and no longer applies — the engine changed in the fix
round.)

## The design gate (honest status, not hidden)

The design gate (`design-gate.py`) is the factory-shell instrument. It
fails the PURE Epic engine itself — 13 failures on the maker's run, same
families (one-button DNA, board formula, press yield, light-text contrast,
Dashboard button absent, Honesty/sample) — and the engine still passed its
eye 03:34Z. The survey page fails 21. The delta is FOUR survey-only
families, not two — the maker's first accounting named two and missed two,
and the checker's re-run caught them. Counts are run-dependent, not stable
facts: the maker's logs read engine 13 / survey 21; the checker's full
re-runs (same gate binary, same files, same widths 1440/390) read engine
15 / survey 20 — the hover/press/scroll probes flip between runs. The
families, named:

1. **Board formula (§3e/§4.2)** — PASS on the engine, FAIL on the survey.
   The failing elements are the boards the builder baked and made visible
   (the paste-proof boards, the image board, the provenance section). The
   construction is the engine's own `.intel-board` (at rest it carries no
   box-shadow; it lights on `.rv-lit`/hover) — byte-identical, harvested
   verbatim. On the pure engine the check samples only the initially
   visible beat; on the survey page more boards are visible, so more are
   sampled. This is a property of the engine's boards, not of the fold-in,
   and fixing it would mean redesigning the engine's boards — out of scope
   here, a follow-on for the checker/captain to judge.
2. **Scroll-light (§4.0)** — PASS on the engine, FAIL on the survey.
   "Boards never lit on scroll." The deck is the official unfold: beats
   are hidden until revealed by Keep-reading (a click), not by scrolling.
   The survey page has 9 hidden beats where the engine has 2, so the
   gate's scroll probe finds more unlit boards. Same format, more beats —
   the gate's scroll assumption and the unfold's click reveal are in
   tension, and the tension is the format's, not this round's invention.
   (The checker's re-run also failed scroll-light on the pure engine at
   1440px, so the clean PASS-on-engine / FAIL-on-survey contrast does not
   hold every run — the probe is flaky.)
3. **Family** — FAIL on the survey at BOTH widths. The gate counts any
   `<section>` in `<main>` with ≥2 numbers or a stat-ish class as a stats
   surface, and a stats surface must match the factory's blessed parts.
   The Factory's OWN provenance board is `<section
   class="intel-board">` whose text ("10 boards in the deck — 3 from the
   engine, 7 from your answers. 3 pastes proved…") carries ≥2 numbers, so
   it counts — and it carries no blessed class (`tn-li`, `orbital`,
   `os-orb`…) → Family FAIL. Unlike board-formula and scroll-light
   (inherited engine properties), this one is caused by THIS round's own
   addition.
4. **Provenance** — FAIL on the survey at BOTH widths. Same board, same
   mechanism: a stats surface must state its truth in one line, and the
   provenance board's text carries no "ledger synced / sources live /
   data as of / truth:" line → Provenance FAIL. Also caused by this
   round's own provenance board.

The survey build therefore runs with `--no-gate`, per the precedent in
`FORMATS.md` ("if the design gate blocks the build, isolate the format
step with `--no-gate` — the format diffs are the proof, the gate is a
separate step"). The gate logs are kept in the maker work dir
(`gate-engine.log`, `gate-survey.log`) so the checker can see the
comparison instead of taking it on faith. Nothing about the gate was
hidden, weakened, or worked around in the builder — `factory.py` still
runs the gate by default for every build; the survey proof build passes
`--no-gate` explicitly and says so.

## What remains unproven

1. **Live render, desktop + phone.** The VM browsers are dead (Chromium
   SIGTRAP / Firefox SIGSEGV since 2026-11-12) — no in-VM render was
   possible. The checker must walk the staged link in a real browser:
   unfold the deck beat by beat, flip the numbers, open each paste door,
   paste plain text, a smart note, and an image, and call it broken if any
   of them does not come out beautiful. Run the staged engine link with
   `?selfcheck=1` and read its 10 lines.
2. **Staged-URL byte equality.** The staged fetch truncates through the
   egress proxy (the Epic round hit the same failure at 24,576 B). The
   git-blob re-read is the proof; the live leg re-verifies in-page.
3. **The eye.** Shawn's eye is the final gate; nothing here has been seen
   by him.
4. **The Phase 2 CLI re-run is DONE in this round** (it was owed from
   Phase 2): `factory.py specs/formats-test.json` re-run with the gate —
   GATE PASSED, both format diffs empty — before and after the fold-in
   edits. The formats step did not regress.

## Files on the branch (this round)

`TEAM-NITRO/interface-factory/` — `formats/epic-auto-format.html` (the
engine, verbatim) · `formats/EPIC.md` (this file) · `formats/FORMATS.md`
(Epic row + auto-format section) · `factory.py` (EPIC table, `emit_epic`,
survey wiring) · `epic-distill-harness.js` (build-time Node harness) ·
`specs/epic-survey.json` (the ten questions, answered by Naya).
`TEAM-NITRO/factory-epic-fold-in-20261117/epic-survey-proof.html` — the
built proof page, filed under the round's own dir (like the Epic round
filed its page) so the staged link exists. The local work dir
(`~/workspace/team-nitro/factory-epic-fold-in-20261117/`) holds the maker
report, `verify_foldin.py` (31 checks), the Epic blob re-read script, and
the two gate logs — the evidence behind this file, not the branch.

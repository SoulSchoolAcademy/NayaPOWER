# MAKER RECORD — AGREEMENT FIX PASS (fix round → fix pass), 2026-11-15

Maker: Naya Nitro Narzan (maker seat). Due 2026-11-15T05:30Z. Staging only — nothing merged, nothing live.
Base: fix-round file, 3,493,483 B, sha256 `7553d76bf2067d60838ec94894d4952acd2a1a8772802727f845f01a79d60af2` (verified first-hand before editing; baseline copy kept at `walk-beginning-fixed-7553d76b-baseline.html`).
Brief: `BRIEF-AGREEMENT-FIXPASS-20261115.md` (check-brief 9/9). Face library: `NAYA-FACE-LIBRARY.md` (15 distinct pictures). Words source (only): `COLLECTIVE-AGREEMENT-OFFICIAL-20261115.md`.
Editor: `edit-agreement-fixpass.py` (28 asserted exactly-once replacements, temp-file write + `os.replace` in the same directory, never truncate-first). Verifier: `verify-agreement-fixpass.py`. Browser probe: `proof-fixpass-drive.py` (drive pattern harvested from Vera's `~/workspace/vera-proof/vera-drive.py`).

## DELIVERABLE

- Walk: `~/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html`
- Bytes: **3,494,589** · sha256: **`ae1bd0bab0dbefb9351fe4ef430b5ddbf4a182571097706b28f42bb9acd1d1ff`**
- Staged URL: **https://naya-walk-beginning-staging.nayapower.workers.dev/welcome**
- Served bytes verified byte-exact by curl, TWICE: 3,494,589 B, sha `ae1bd0ba…` (fetch 1 + fetch 2, both match the local file).
- Deploy: in-memory build via `deploy-v4f-memory.py` (proven v4f path), PUT HTTP 200 to worker `naya-walk-beginning-staging`, account `b5e2a51b3e883f7722287c5f51b1196b`, modified `2026-11-15T04:03:08Z`, deployment `a8dfcc2d3a124f6d9c926eec7a029e5f`. Builder assert at `build-v23-staging-worker.py:90` updated to the new walk sha (same pattern as the round maker).
- New KV key (fix pass only): `wbf-agmt-b12.jpg` = `Naya_Profile_Black.jpg` (526,689 B, sha `2a38bb8898f6…`), uploaded by `kv-put-agreement-fixpass-b12.py` (HTTP 200); serves live at `/agmt-b12.jpg` (curl: HTTP 200, 526,689 B, sha matches). New key only; no live key overwritten. All other portraits were already in KV under `wbf-agmt-*` (uploaded by the round's `kv-put-agreement-v4.py`).
- Git branch (durable record): `agreement/fix-round-20261115-fixpass` in `~/workspace/nayapower-repo` (NayaPOWER), branched from current HEAD (`nitro/p4-dashboard-strip` tip — chosen so the repo's unrelated dirty working-tree state is untouched); commit holds the edited walk file + this record + the edit/verify/probe scripts + the builder-assert change + `proof-fixpass/` evidence. Not pushed.

## FIX 1 — BOARD 58, THREE-SENTENCE LAW

- **The fix, chosen over a new board:** boards 58/59/60 held 6+3+3 = 12 sentences. Rebalanced to 4+4+4 by moving sentences between boards — NO new board, NO renumbering, NO change to data-beat numbers, kind labels, dots, rail targets, or click count. The alternative (splitting board 58 into two boards) would have renumbered 24 boards, both summary boards' neighbours, and every rail target after it; the rebalance is the smaller, safer change and the brief allows it ("The split moves sentences between boards").
- Board 58 (QUESTION 4 · 23 OF 42) now holds only its first paragraph (4 sentences): "I know what you might be thinking. "What's the catch?" "Is this a scam?" Those are fair questions."
- Board 59 now holds: "So here's the logic: …" + "A real person chooses something valuable." + "They make a real purchase." + "The payment is verified." (4 sentences)
- Board 60 now holds: "And an eligible ambassador who helped bring them can receive a share." + "That's a referral-based business model." + "It's not magic." + "And it doesn't mean everybody is guaranteed to make money." (4 sentences)
- **Sentence counts of ALL 83 boards (counted by SENTENCES, per <p>, Vera's method — eye-button text removed, note divs removed, decimals protected; baseline reproduced Vera's list exactly, so the method matches the checker's):**
  `[3, 3, 2, 4, 3, 2, 3, 3, 3, 1, 4, 4, 3, 3, 2, 3, 4, 4, 4, 4, 1, 4, 3, 3, 1, 4, 1, 3, 3, 3, 2, 3, 4, 3, 3, 3, 4, 2, 4, 4, 3, 3, 1, 4, 3, 3, 2, 2, 3, 2, 4, 3, 2, 3, 3, 2, 3, 1, 4, 4, 4, 2, 4, 2, 3, 1, 3, 3, 2, 2, 4, 3, 3, 1, 2, 3, 3, 1, 2, 3, 3, 3, 2]`
  (max 4, min 1, total 234). Changed boards only: 58 (6→4), 59 (3→4), 60 (3→4). No other board moved.
- **Words proof:** ordered board-sentence list identical baseline→edited (231 sentences, in order); sentence multiset identical; board words vs the Official (word-multiset, apostrophes normalised, founders sentence excluded): zero board words outside the Official, zero Official words missing. Nothing rewritten, dropped, or added — the raw line diff between baseline and edited file is exactly the 28 intended changes (14 face insertions + 3 sentence moves + 11 note-photo swaps) and nothing else.
- **Live:** rendered-DOM recount on the staged page (same method, buttons + notes stripped in JS) returns the identical list, max 4, total 234, beats 58/59/60 = 4/4/4. Keep-reading still 82 clicks / 83 boards, 83 dots, label "ALL TEN STEPS · READ", agree frame visible after the final click (360px + 1440px).

## FIX 2 — PORTRAITS, VISIBLY DIFFERENT

### The choice (scorecarded) — ROTATE, don't drop

The brief offered two ways to break the b02 ×11 eye-note repeat: rotate the note photos through the face library, or drop the photo from the notes. I chose **ROTATE** — every note keeps a photo, each note a different file — and paired it with faces on every third §4 board.

**Ten loves (why rotate wins):**
1. The note IS Naya speaking — her face belongs beside her voice; a faceless explanation reads like a footnote, a faced one reads like her talking.
2. It uses the library as designed: 15 distinct pictures exist precisely so faces can alternate.
3. It kills the repeat completely (b02: 11 notes → 1 note) instead of hiding it by removing photos.
4. A reader opening several §4 notes now meets a different Naya each time — the sense-check failure ("same portrait eleven times") is gone by construction.
5. It costs nothing new in the notes: the photos were already there, same size, same style — only the file changes.
6. It keeps the notes visually consistent with the section boards (same round, lit, elevated treatment).
7. It preserves the maker's "note is an explanation of that section" warmth without the section-locked repeat.
8. It is checkable by counting: max 2 notes per file is a number Vera can grep, not a judgment.
9. It leaves the door open: if Shawn ever wants one face per section again, the rotation is one grep away from reverting.
10. It treats the face library as the brand asset it is — the face of NayaNET, shown, not shelved.

**Ten don't-loves (what rotate costs, stated plainly):**
1. 14 notes over 13 usable files (top flank and signing stay unique) forces one file to illustrate 2 notes (b09: land + cap).
2. A note photo can now echo a board portrait elsewhere on the page (e.g., b06 is both board 58's portrait and the collective note's photo) — same file, different boards.
3. The section-link is loosened: a §4 note no longer always wears its section's portrait.
4. One more file enters the notes (b12, the Black portrait) that a reader has never seen before this pass.
5. b00 returns to the page (deed note + board 43) after the round deliberately removed it as the old lead photo — its new uses are different placements, but the file is back and Vera must not mistake that for the lead photo returning.
6. Two board portraits repeat in §4 (b10 at 37 + 73, b11 at 40 + 76) — 15 faced boards, 13 usable files, so two repeats are arithmetically forced.
7. Rotation is a bigger diff than dropping (11 swaps vs 11 deletions) — more lines for the checker to verify.
8. At 44px a note photo's distinctness is subtle — two Warm portraits could read as similar at that size to a fast scroller.
9. It adds a KV dependency (b12) that dropping would not have needed.
10. It keeps 14 small faces on the page instead of zero — if Shawn ever rules notes faceless, this whole rotation is rework.

**How to make it ten times better:** the 10× version is a portrait set sized to the letter — 28+ distinct Naya portraits (one per note + one per faced board, zero repeats anywhere) shot in one session with the same light, so every face is unmistakably her and unmistakably different. We don't have that set; the library has 15. Inside 15, this rotation is the max: every note distinct except one sanctioned double, every faced board distinct except two far-apart repeats, zero same-board collisions, zero adjacent repeats. The remaining gap (b09 ×2, b10/b11 ×2 on boards) is arithmetic, not choice — and it is written down here, not hidden.

### (a) Eye-note photos — the b02 ×11 repeat is broken

- Note-photo counts per file (14 notes): b06: 1 (collective) · b09: 2 (land, cap) · b11: 1 (business) · b00: 1 (deed) · b01: 1 (cost) · b03: 1 (joining) · b05: 1 (privacy) · b10: 1 (vault) · b12: 1 (save) · b04: 1 (job) · b07: 1 (earn) · b08: 1 (skeptic) · b02: 1 (hold). Max 2 per file. `/agmt-b02.jpg` occurrences in the whole file: **2** (board 36 portrait + hold note) — was 12.
- Swaps made (11): business b09→b11 · deed b02→b00 · cost b02→b01 · joining b02→b03 · privacy b02→b05 · vault b02→b10 · save b02→b12 · job b02→b04 · earn b02→b07 · skeptic b02→b08 · cap b02→b09. Kept: collective b06, land b09, hold b02.
- Rule kept: no note photo equals its own board's portrait (checked for all 14 — zero collisions), and no note photo equals an adjacent board's portrait (checked for all 14).

### (b) Faces into the §4 run

- §4 faced boards (data-beat 36–77): **36, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76** — 15 of 42 boards (was 1 of 42). Every 3-board window in 36–77 contains a face (machine-checked, all 40 windows).
- Placement: every third board from 37 (37, 40, 43, …, 76) plus the existing board 36. Harvested verbatim from beat 36's own pattern: `face-left` class on the article + `<img class="deal-beat-photo" src="…" alt="Naya speaking">` as first child of `.ib-blocktop`. No new CSS, no new component.
- Files in board order: 36 b02 (kept) · 37 b10 · 40 b11 · 43 b00 · 46 b01 · 49 b03 · 52 b05 · 55 b12 · 58 b06 · 61 b04 · 64 b09 · 67 b08 · 70 b07 · 73 b10 · 76 b11. All seven still-unused pictures used first (b00, b01, b03, b05, b10, b11, b12); the other seven slots reuse already-used pictures. Repeats: only b10 (37 + 73, 36 boards apart) and b11 (40 + 76, 36 apart). No two adjacent boards share a portrait (checked across all 19 portrait boards, incl. 78's b08 next to 76's b11).
- Why every third, not every board: 15 pictures cannot cover 41 boards without repeats (the round's arithmetic stands); every third is the densest spacing that keeps repeats to two far-apart pairs. A portrait on every board would force a repeat every ~3 boards — worse than a face every third board with almost no repeats.
- Live: all 19 board portraits render loaded (`complete && naturalWidth > 0`), 148px at 360px, 244px at 1440px. Eye-read at 360px: board 55 (b12 Black portrait — outdoor, visibly different from every other board) and board 58 (b06 hair-up close-up, 4-sentence board) both read clean — round lit photo, white text on obsidian, corner gems inside, no overflow. The deed note open shows the b00 photo top-right, visibly different from board 36's b02 portrait on the same board.

## NO-REGRESSION — WHAT I VERIFIED MYSELF, AND HOW

- **Proven live on the staged bytes (driven from the login page, 360×800 then 1440×900, zero console/page errors both runs):** keep-reading 82 clicks / 83 boards · dots 83, first on, 83 on at the end · label "BOARD 1 OF 83" → "ALL TEN STEPS · READ" · agree frame visible after the final click · eyes open 14/14 (tap 1: note visible, top 10px below its eye, top in view; tap 2 closes — measured on all 14) · overflow 0 at true 360px hook + unfolded (scrollWidth = innerWidth) and at 1440px hook + unfolded · signing 260 vs board 148 = 1.76× at 360px, 388 vs 244 = 1.59× at 1440px · all 19 board portraits + all 14 note photos loaded with the right srcs.
- **Proven on the file + served bytes (audit run on both, identical results, FAILS: NONE):** Official verbatim (word-multiset: zero outside, zero missing) · founders line verbatim ×1 · "bonus" = 0 · "blockchain" = 0 · v4 hedged forms 0 ("Our planned privacy standard", "until the full retention system…") · Official hedged phrases stand ×1 each per the ITEM 1 RULING ("governed by the applicable published agreements", "the intended default is seven days") · "I'm not an LLM" ×1 · "$25" ×2 · "$20" = 0 · "nayanet.app — enter." present · "THE ROYAL MANUSCRIPT" = 0 · "Ready to sign" = 0 · `letterPreview` = 0 · "double points" ×1 · beat 0 carries no portrait (hook guard) · "What's next?" gone (0 rendered occurrences; the single remaining occurrence in the whole file is the JS code comment noted by the round checker — untouched by this pass).
- **Proven by diff (the strongest no-regression evidence for the untouched parts):** the raw line diff baseline→edited is exactly the 28 intended changes. Every other byte is identical to the round's verified build — so the hook, one button, white text, corner gems, wax seal, skip path, plain-text view, jump pills, agree-via-Enter, and no-flat-dots are byte-identical to the build Vera passed, except where the 28 changes interact (keep-reading/dots/label, board heights, note photos — all re-proven live above). I did NOT re-drive the seal, skip, plain-text, or agree-via-Enter paths myself in this pass; they are byte-identical to the round's passed build and Vera re-sweeps them. Stated plainly, not claimed.
- **Not probed by me in this pass:** 390px and 1920px viewports (360 + 1440 probed; the changed parts use the already-proven beat-36 pattern and the same CSS at all widths). Vera re-sweeps all four widths.

## THE SEVEN SELF-CHECK QUESTIONS (answered in writing)

1. **Most intelligent?** Yes — the rebalance (no renumbering) and the rotation (max distinctness inside 15 pictures) are each the smallest change that fully satisfies the measurement, instead of the bigger rebuilds (new board + 24 renumbers; a new portrait shoot).
2. **Most logical?** Yes — every change follows from a counted failure: board 58's 6 sentences from Vera's sentence count; the b02 ×11 from the served-file grep; the 40-board faceless run from the board-portrait map. The counts are the argument.
3. **Most sensible?** Yes — a reader now meets a face at least every third board of the long §4 run and never the same note photo twice in a row; each board still reads in seconds (max 4 sentences, unchanged).
4. **Full scope?** Yes — login-to-signing whole flow driven at phone + desktop, all 83 boards counted by sentences, all 14 notes audited, all 19 board portraits checked loaded, served bytes re-audited, branch filed. Nothing scoped to the diff.
5. **Consequences?** First order: the staged agreement page changes in exactly 28 lines. Second order: Vera re-checks the two fixes + the guards, then Shawn's eye. The live site is untouched; only the staging worker + one new KV key changed. A reader who had the old page cached sees the new one on next load (no versioned URLs changed).
6. **Pros and cons?** Pros: board 58 fixed without renumbering; b02 ×11 gone; §4 has a face every third board; Official words untouched (proven by multiset + order). Cons: one note file illustrates 2 notes (b09); two board portraits repeat far apart (b10, b11); b00 returns to the page in two new placements (flagged for Vera, not hidden); the "QUESTION 4 · N OF 42" kind label wraps to two lines at 360px on faced boards (pre-existing beat-36 pattern — the photo takes the top row at narrow width — observed, not introduced by this pass, not fixed here). Strongest case against my preference: dropping the note photos would have been a smaller diff and zero doubles — but it would have removed Naya's face from her own explanations, which is the opposite of what the page is for.
7. **Best possible choice?** Against the ultimate objective (the reader understands the agreement in seconds, trusts it, and sees Naya throughout): yes. The letter is still the Official's words in order, every board 1–4 sentences, faces alternating as far as 15 pictures allow, every control re-proven live. Scored: both fixes proven in this record with their measurements; the no-regression guards proven by byte-identity plus live re-proof of the interacting behaviours.

## CANON — THE HIGHEST LEVEL (ten checks)

1. REAL OBJECT — pass: the 14 new board portraits use the harvested `.deal-beat-photo` treatment (round, lit, elevated) verbatim from beat 36; note photos keep the harvested quote-photo treatment.
2. JEWELRY, NOT DOTS — pass: untouched (eyes, gems, seal byte-identical); new portraits carry the same lit ring as the existing ones.
3. ELEVATED, NEVER FLAT — pass: no flat element added; portraits are the elevated round form.
4. COLOUR SPEAKS — pass: §4 boards keep their purple tone; portraits carry the tone border from the harvested rule.
5. ALIVE NUMBERS — pass: "Board N of 83" live, 83 dots lighting in order, 82 clicks — re-proven live.
6. NUTSHELL FIRST — pass: every board 1–4 sentences, max 4, total 234 — the canon check this pass exists to fix.
7. MOTION THAT MEANS SOMETHING — pass: reveal, eye open + scroll-into-view, all re-proven live; no new motion added.
8. ACTIVE INTELLIGENCE — partial (as the round stated): rail jumps + plain-text + skip anticipate the reader; no new inference claimed.
9. HARVEST, NEVER INVENT — pass: portraits from the face library (incl. the one new KV key for the library's own Black portrait); board-photo placement harvested byte-for-byte from beat 36; zero new components.
10. PROVEN BY EYE — pass at 360px (board 55, board 58, deed note eye-read in this record) and by measurement at 1440px (overflow, sizes, clicks); 390/1920 are Vera's to confirm by eye.

## WHAT I COULD NOT PROVE (stated plainly, never claimed)

- The 2,124 headline word count as a single number — same standing note as the round (the sentence/word-level verbatim proof stands in its place).
- The seal, skip, plain-text, and agree-via-Enter paths were not re-driven by me in this pass — they are byte-identical to the round's passed build (raw diff) and ride Vera's re-sweep.
- 390px and 1920px viewports were not probed by me (360 + 1440 were); the changed parts reuse the beat-36 pattern already proven at all four widths by the round.
- **Probe bug found and fixed in this pass (learning-loop note):** my first browser count script did not strip the eye-button text, so the trailing "i" counted as a sentence fragment and five note boards read 5. The file audit (Vera's exact method, reproduced on the baseline) said max 4. I fixed the probe to strip buttons + notes and re-ran the count live on the staged page: identical list, max 4. Lesson: a count method that differs from the checker's by one strip rule is a different count — match the checker's method exactly, and re-prove live after fixing the probe, never after fixing the page to fit a buggy probe.

## FIVE GATES (before the deploy)

1. **Is it right?** Yes — staging only, live untouched; the words are Shawn's ratified Official, verbatim, in order.
2. **Is it what they truly need?** Yes — the reader needs the long §4 run to feel like Naya talking to them, not a wall of text with one face eleven times.
3. **Is it mine to do?** Yes — the fix-pass brief names me maker; the staging deploy + one new KV key are the brief's own path. Nothing live, no money, no credentials, no destruction.
4. **Is now the time?** Yes — due 05:30Z; Vera's focused re-check is next in the same pass (continuous cycle law).
5. **Can I prove it?** Yes — both fixes, each with its measurement in this record (sentence counts for all 83 boards, portrait audit, live drive at two widths, served-bytes audit); what I could not prove is listed under its own heading, never claimed.

## EVIDENCE INDEX (DURABLE)

- Maker record (this file): `~/workspace/team-nitro/walk-v23-assembly-20261114/MAKER-RECORD-AGREEMENT-FIXPASS-20261115.md`
- Edited walk: `walk-beginning-fixed.html` (3,494,589 B, sha `ae1bd0ba…`) · baseline: `walk-beginning-fixed-7553d76b-baseline.html`
- Edit script: `edit-agreement-fixpass.py` · KV upload: `kv-put-agreement-fixpass-b12.py` · verifier: `verify-agreement-fixpass.py`
- Browser probe: `proof-fixpass-drive.py` · results: `proof-fixpass/probe-360-1440.json` (aliases fixpass360a, fixpass1440a)
- Screenshots eye-read (360px): `proof-fixpass/board55-b12-360.png` · `proof-fixpass/board58-360.png` · `proof-fixpass/note-deed-b00-360.png` · `proof-fixpass/hook-360.png`
- Served bytes re-fetched: `/tmp/served-welcome.html` + `/tmp/served-welcome2.html` (3,494,589 B, sha `ae1bd0ba…`, both fetches)
- Live count re-check: `/tmp/count-check.py` (direct /welcome load, buttons + notes stripped — identical list, max 4)
- Served-bytes audit run: `/tmp/svc-check/` (full verifier on the fetched bytes — FAILS: NONE)

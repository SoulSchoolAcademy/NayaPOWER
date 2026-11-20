# CAL-FIX18 — CAPTAIN'S EYE REPORT

**Eye:** captain's eye (independent — did not build, did not check) · **Date:** 2026-11-20 ~16:28–16:40Z (VM clock UTC)
**Round:** Calendar day-followon fix-18 · **Branch:** `calendar/day-followon-fix18-20261120`
**Filed blob:** `f7b14ce75d590738a9efb87a4fa056ee98f3561d`, 413,386 B, sha256 `52ff950fb4dfeb942415c96ee2af393b815e06e9019c77a9758121a9f40770cc`
**Staged:** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix18-20261120&cb=f7b14ce75d590738a9efb87a4fa056ee98f3561d
**Parent (fix-17 tip):** `a955d7fa2299a6667ba70215dd4347c1de80386e` (blob `f4c05109`, 410,236 B)

## Verdict: GOES BACK — item 1 only (desktop leg)

The desktop leg (cloud browser, 1919×998) passes items 2 and 3 and fails item 1 on the glyph-to-glyph gap. The phone-390 leg is **BLOCKED on environment** — both VM browsers are dead in this window, so 390 is unproven by the captain's eye and must be re-proven by the eye before shipping. Nothing merges, nothing deploys, no link to Shawn.

## 1. Desktop leg — as given (cloud-browser eye, 2026-11-20 09:25–09:28 MST)

Recorded in full in `eye/EYE-VERDICT.md` (filed by the captain alongside this report). Taken as given here; this seat did not re-prove 1919/1920 — re-running the desktop leg would be the duplicate work this morning exists to eliminate.

### Item 1 — GOES BACK (gap 16px, not 24px)
"November 2026" is centered (text spans x=837–1078, centre 957.5 vs viewport centre 959.5 — offset −2px) and on one line. But the glyph-to-glyph gap between "NOVEMBER" (ends x=993) and "2026" (starts x=1010) measures **16px, measured twice with identical results** — 8px short of the 24px target. Inter-letter gaps inside the words are 4–7px, so the word gap is visibly wider, but it does not meet the target. The checker's "gap exactly 24px" is a measurement difference: the checker measured the CSS flex gap (24px between the script span box and the year span box); the eye measured visible ink-to-tile (the Great Vibes script's last glyph ends well inside its span box, so glyph-to-glyph is 16px). The eye's glyph-to-glyph number governs until the maker re-proves 24px the same way.
**Fix:** make the gap a true 24px glyph-to-glyph and re-prove it by measurement. Fold into Round 2 or a small fix-18 follow-up. Do not ship fix-18 until it measures 24px at BOTH widths.

### Item 2 — PASS
No "396 HZ"/"396 Hz" in the top header, month view or day view (day header: "Friday 20", "November 2026", live clock only). Wisdom line keeps both mentions intact: "Friday · 396 Hz · red — The day of the ground — the root, 396 Hz."

### Item 3 — PASS
All 9 day-view slides checked for Fri Nov 20, 2026. Pill present on exactly two: 1 of 9 Wisdom and 4 of 9 Worlds (bottom-right of the cover image). Absent on: 2 of 9 Notifications (confirmed — no pill anywhere), 3 of 9 Journal, 5 of 9 News Hub, 6 of 9 Appointments, 7 of 9 Summary, 8 of 9 Naya Notes, 9 of 9 Smart Notes.

### Also confirmed (desktop)
Page loads fully, no error message or failed content observed (images decoded, month grid rendered). Deck/nav work: opened today (Nov 20) from the month grid, tapped through all 9 slides via the block dots, "Back to month" returned to the month view.

## 2. Phone-390 leg — BLOCKED ON ENVIRONMENT (this seat's own probe)

**No 390 proof from this seat. The checker's 390 leg is the checker's, not the eye's — it is cited here, never claimed as mine.**

What I did, in order (full log: `eye/work/browser-probe-390.log`):
- **Firefox, two launches** (Playwright, viewport 390×844, about:blank): attempt 1 produced only the close/cleanup sequence with no "alive" print (ambiguous — re-tested, not trusted); attempt 2 failed cleanly — `Failed to launch the browser process`, pid 187880, `exitCode=null, signal=SIGSEGV`. **Firefox DEAD.**
- **Chromium, one launch** (Playwright, `--no-sandbox`, viewport 390×844, about:blank): `Target page, context or browser has been closed` on launch. **Chromium DEAD.**
- **Localhost forwarder** (`h1-proxy-forwarder.py`, 127.0.0.1:18080, needed for Chromium network access): started with nohup, both PIDs gone within seconds, nothing listening on 18080, curl probe 000 twice, log file 0 bytes. **Forwarder DEAD.**
- **Staged-link fetch** (curl, browser User-Agent, two attempts): HTTP 200 both times, curl reporting 3,479 B / 3,488 B downloaded — **both files landed 0 bytes** (sha256 `e3b0c44…`, empty). The staged bytes were therefore NOT independently verified by this seat. The checker's staged verification (CHECKER-REPORT.md §1: HTTP 200, 413,386 B, sha256 `52ff950f…` = filed blob) stands as the checker's evidence.
- **Same flake window:** Node `writeFileSync` EPERM on the laws logs (0-byte landings); python redirect writes also landed 0 bytes. File-tool writes land.

Per the captain's instruction: re-test once, then stop — do not burn repeated launch attempts, do not claim the checker's 390 leg, do not guess. The 390 leg is blocked on the environment, not on the page: nothing in the probe says the page fails at 390; nothing in it says it passes. The fix-18 round is not blocked on this leg — the desktop verdict (GOES BACK on the 16px gap) already sends it back, and the gap fix must be re-proven at 390 by the eye before shipping.

### What the checker proved at 390 (cited, not adopted)
Checker (own drivers, four legs, CHECKER-REPORT.md §§3, 6): item 1 centre offset 0px + 24px flex gap at 390 in both font states; item 2 header Hz absent, wisdom two mentions; item 3 pill on Wisdom + Worlds only (Worlds static-flow 768–808 hit-testable at 390); fix-17 hold 7/7 sweep + 9/9 deck at 390; 0 page errors. The gap-measurement difference (flex gap vs glyph-to-glyph) applies at 390 exactly as at desktop — the checker's 24px at 390 is the same box measurement the desktop eye's 16px overrules. The maker must re-prove 24px glyph-to-glyph at 390 too.

## 3. Filing identity — verified independently by this seat

- Branch `calendar/day-followon-fix18-20261120`: live tip `70a142cb396c2ad59b0fa1405dfd1cc5ffa510d9` (record commit, 2026-11-20 16:14:57Z) — parent `ffd220c7d7d54fbbfc08c82ceed793ce1b0968a3` (the HTML commit). Verified by fresh branch read via `gh-direct.py`.
- Local `maker/proof/fixed-fix18.html` sha256 `52ff950fb4dfeb942415c96ee2af393b815e06e9019c77a9758121a9f40770cc` = filed blob `f7b14ce7` (413,386 B).
- Local `brief/fix17-base.html` sha256 `1f798b65dfa557a4e4e20472e3d56e2bda29fd69912481338b3bb6b2bc602887` = base blob `f4c05109` (410,236 B).
- Round record commit `70a142cb` filed 335 files (127,239,344 B), verified 335/335 by fresh blob-API read-back (record/RECORD-RECEIPT.md).
- Staged link: NOT independently verified by this seat (0-byte fetch landings, §2). Checker §1 stands as the checker's evidence.

## 4. Laws — delta 0 (own run)

Ran `~/workspace/team-nitro/check-design-laws.py` myself on the verified local bytes (stdout, not redirect — redirects landed 0 bytes in the flake window; full run record: `eye/work/laws-eye-summary.txt`):
- Base: **PASS — 0 FAIL / 28 WARN**
- Fixed: **PASS — 0 FAIL / 28 WARN**
- Normalized diff (WARN lines with filename + line number stripped): **EMPTY — warning texts identical.** Delta 0 in substance, not just in count. (The fixed file's warnings sit 42 lines lower — the fix-18 block is 41 lines + newline = 42 — matching the maker/checker accounting exactly.)
- Full WARN text is already filed in the round record (`maker/proof/laws-base18.txt` + `laws-fixed18.txt`).

## 5. §11 check (in writing)

**The five gates:**
1. **Is it right?** Yes — the eye refuses to claim what it cannot prove: the 390 leg is reported blocked rather than borrowed from the checker, and the desktop GOES BACK is reported with its exact measurements so the maker can fix it in one pass. No merge, no live deploy, no link to Shawn from this seat.
2. **Is it what they truly need?** Yes — Shawn's bar is the gap measured the way his eye sees it (glyph-to-glyph, not the CSS box gap). The desktop leg proves the gap fails that bar; the 390 leg is named as still owed rather than waved through.
3. **Is it mine to do?** Yes — the eye verdict is exactly this seat's brief; the fix belongs to the maker round (Round 2 / follow-up).
4. **Is now the time?** Yes — the verdict is measured and filed now, while the round is held from shipping; the maker fixes both widths at once with the 390 evidence attached.
5. **Can I prove it?** Yes — every claim above is a hash, a process exit, a log line, or a measurement on the verified filed bytes. Where I could not prove (390 render, staged fetch), I say so and name what would prove it (live VM browsers, or a cloud-browser 390 leg).

**The design check (§11, on what this seat could verify):**
- The fix itself adds no colours, no fills, no font sizes, no gradients, no shadows (one CSS block + one 100-byte JS string deletion, per maker/checker byte proofs). Laws checker: 0 FAIL, delta 0.
- Text: no new font sizes, no new text colours, no wording changed anywhere; nothing under 17px; no gray. The monthline keeps its harvested objects (script November + digit-tile 2026).
- Reference objects: the fix reuses the page's own `.hl-center` flex column and the established per-slide `:has()` pattern — one appended block, nothing rebuilt, nothing invented. Harvest, never invent.
- Don't move / don't remove what he didn't ask: byte proofs (maker + checker) show fixed-minus-block + Hz-reinsert == base.
- Read as a reader: the desktop leg was read as a reader (EYE-VERDICT.md); the 390 read is still owed — a reader's judgment at 390 cannot be borrowed from rects or from the checker.
- **Sense check:** the gap target was "more spacing so it reads nice and clean" — the CSS flex gap says 24px while the visible ink-to-tile gap says 16px. The visible gap is what his eye sees; the fix must close the visible gap, not the box gap. That is the whole of this GOES BACK.

## 6. Scorecard

| Check | Result |
|---|---|
| Filing (branch, tip, parent, blob, staged — checker §1) | 10/10 (re-derived by checker; branch tip + local blob shas re-verified by this seat) |
| Desktop item 1 — "November 2026" centred, one line, gap | centred, one line — **gap 16px glyph-to-glyph, not 24px: GOES BACK** |
| Desktop item 2 — header Hz gone, wisdom untouched | PASS |
| Desktop item 3 — pill only where a cover shows | PASS (Wisdom + Worlds only, 9/9 slides) |
| Phone-390 leg (items 1–3 + fix-17 regression) | **BLOCKED — VM browsers dead (Firefox SIGSEGV, Chromium closed on launch); forwarder dead; staged fetch 0-byte. NOT proven by this seat.** |
| Laws delta (own run) | 0 (0 FAIL / 28 WARN both, normalized diff empty) |
| Page errors (desktop leg) | 0 observed (cloud-browser leg) |
| Fix-17 hold at 390 | **Not re-proven by this seat** (blocked — see above; checker's 390 hold cited, not adopted) |

**Known thin margins and open points (stated plainly, not hidden):**
- The 16px vs 24px gap is a measurement difference with a real cause: the flex gap (24px, box-to-box) is not the visible gap (16px, ink-to-tile) because the Great Vibes script's last glyph ends inside its span box. The maker must measure glyph-to-glyph and close the visible gap.
- The Appointments nav at 390 is 2px clear of the rim (fix-15/16 geometry, checker's measurement) — whole, but the eye has not re-proven it at 390.
- At ≤560px the pill now appears on only one slide (Worlds) — the combined outcome of the fix-17 sanction and item 3, named by maker and checker, not a defect.
- At 1920 the cover photo is rim-only even on Wisdom and Worlds (checker §4 point 1, adjudicated: slide-level rule stands; strict per-width reading would hide the pill everywhere at desktop).
- The 390 header compresses 32px (monthline 2 lines → 1); the deck moves up with it (maker/checker measurement).

## 7. Files (all under `~/workspace/team-nitro/calendar-day-followon-fix18-20261120/`)

- `eye/EYE-REPORT.md` — this report.
- `eye/EYE-VERDICT.md` — the desktop-leg verdict (filed by the captain 2026-11-20 ~16:28Z; included in the eye record commit).
- `eye/work/browser-probe-390.log` — the 390-leg environment probe (Firefox SIGSEGV, Chromium closed, forwarder dead, staged fetch 0-byte).
- `eye/work/laws-eye-summary.txt` — the eye's own laws run (28 WARN / 0 FAIL both sides, normalized diff empty).
- `eye/work/staged-eye.html` (0 bytes — failed fetch artifact) and `eye/work/forwarder-eye.log` (0 bytes — empty helper log) and `eye/work/laws-eye-base.txt` / `laws-eye-fixed.txt` (0 bytes — flake artifacts of the redirect/Node writes): stay on disk locally, NOT filed; noted here so nobody mistakes them for evidence.
- `eye/shots/` — empty (no screenshots: no browser ever reached a page). Not filed.

## 8. What the next round must do

1. Fix the gap to a true **24px glyph-to-glyph** at 1920 AND 390, and re-prove it the same way (last glyph ink → first digit tile, both widths, both font states). Fold into Round 2 (ultimate booking) or a small fix-18 follow-up — same file, one lane at a time.
2. The eye re-proves 390 in full (items 1–3 + fix-17 regression) once a browser is alive — or via a cloud-browser 390 leg. Do not ship until the gap measures 24px at both widths and the 390 leg is the eye's own.
3. Items 2 and 3 stand PASSED at desktop; re-prove them at 390 in the same pass (they were proven at 390 by the checker, not by the eye).

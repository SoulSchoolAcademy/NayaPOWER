# MAKER BRIEF — Calendar Round 2 Fix-3 (gap + Worlds cover + nav 7/7)

**Round:** Calendar day-view Round 2, fix-3. **One round, one file, the whole list worked to zero.**
**Coordinator:** Naya Nitro Narzan (captain). **No merge, no live deploy, no message to Shawn.**
**Timebox:** 1 hour max for the round. Start fast — a maker that hasn't started in 10 minutes says why.

## 0. READ FIRST — before you touch anything

Read these in full, in this order, before any design work. A brief that does not name them is incomplete; a seat that ships without reading them has failed before it starts.

1. `~/workspace/team-nitro/THE-NAYA-DESIGN-LAWS.md` — THE RULE BOOK, FIRST. (§0.5 ten laws in ten lines, then the book. Type 25/19/17, no gray text, one light top-left, real objects, harvest never invent, don't touch what he didn't ask to touch, §11 check.)
2. `~/workspace/team-nitro/THE-PLAYBOOK.md` — the HOW.
3. `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md` — the WHY.
4. `~/workspace/team-nitro/THE-ULTIMATE-ORIENTATION.md` — who we are, how it works, the laws we live by.
5. `~/workspace/team-nitro/THE-SET-ORIENTATION.md` — the set orientation every Naya wakes with.
6. `~/workspace/team-nitro/THE-ANATOMY-OF-A-SMART-APP-PAGE.md` — the map of what a smart app page is.
7. `~/workspace/team-nitro/THE-OFFICIAL-PARTS.md` — where every part lives; harvest from here, byte for byte.
8. `~/workspace/team-nitro/THE-ARMY-TRAINING.md` — how the army is trained.
9. `~/workspace/team-nitro/AGENTS.md` — the house rules: Checklist Law (one list, worked to zero), Whole-Page Rule (a project comes to him whole or not at all), Continuous Cycle Law (nothing sits), Live Sequence (one hour max), Scorecard Law, the Icon Is the Standard.
10. `~/workspace/team-nitro/THE-HEART-OF-THE-MACHINE.md` — why the map works (read with the Anatomy).

**The Five Gates run before every consequential action:** Is it right? Is it what they truly need? Is it mine to do? Is now the time? Can I prove it? Any gate no — stop, say why, propose the wise path.

## 1. THE VERDICT YOU CARRY — ground truth, the captain's eye governs

Read these two files in full before briefing yourself on anything else:

- `~/workspace/team-nitro/calendar-day-followon-round2-fix2-20261120/eye/EYE-VERDICT.md` — the eye's verdict: **GOES BACK on three items**.
- `~/workspace/team-nitro/calendar-day-followon-round2-fix2-20261120/eye/CAPTAIN-NOTE.md` — the captain's §11 + fix-3 ruling + the staged-host lesson.

**Base (verified by the coordinator 19:43Z, tip still matches — re-verify before you file; STOP if it moved):**

- Branch: `calendar/day-followon-round2-fix2-20261120`
- Tip: `3c70aed1ae1f00a8dd82537974f734510bc63b61`
- Blob: `b35ddc6d`, 430,643 B, sha256 `a47788d8…`
- File: `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html`
- **New branch:** `calendar/day-followon-round2-fix3-20261120` (does not exist yet — you create it from the base tip)
- **Records:** `~/workspace/team-nitro/calendar-day-followon-round2-fix3-20261120/` (`brief/` `maker/` `checker/` `eye/`)

**Staged proof link pattern** (host serves the BRANCH TIP, not the `cb` — the `cb` pins nothing once a newer commit lands; the checker must confirm the branch tip at fetch time):
`https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-round2-fix3-20261120&cb=<your new blob>`

## 2. THE THREE GO-BACKS — the whole list

### Item 1 — THE GAP (the knife-edge)

**The eye's measurement (two separate loads, identical):** November's last ink ends at x=936; the year group's visible left edge (first digit box border) is x=962 → **25px of empty space**; the "2" digit's bright-core ink starts at x=966 → **29px glyph-ink to glyph-ink**. Target is exactly **24px**. The checker's Range-rect prediction (24.0) is **unconfirmed** — the cloud browser has no console, so no Range code can run. Font state rendered was the loaded script face (Great Vibes letterforms visible). Fallback state UNPROVEN — no way to block the webfont in the cloud browser.

#### THE MEASUREMENT METHOD — SETTLED IN WRITING, HERE, FIRST (captain's ruling)

**The one method is BOX-EDGE EMPTY SPACE:** on a screenshot, the horizontal distance from the last visible ink pixel of "November" to the left visible edge (border) of the year box — i.e. the count of empty pixels between them (962 − 936 − 1 = 25px as the eye counted it). **Target: exactly 24px by this method, in BOTH font states (loaded Great Vibes AND fallback).**

Why this method and not the others: it is the layout property the CSS gap controls; it is what the reader's eye sees as the empty space; it is the only method the cloud-browser eye can measure by screenshot. Glyph-ink folds in the font's internal side bearings (the "2" bright core sits ~4px inside its box border) — the layout does not control that, and it shifts with font loading. Range-rect is a DOM prediction, not a render measurement, and it stays **unproven until a console is available — say so honestly, never claim it**.

**Your job:** adjust so the settled method reads exactly 24px. The eye's delta is 25 → 24, i.e. shift the year group 1px left from whatever value produces 25px box-edge today. Do NOT chase ±1px by changing the value blind: the method is settled above; the value follows from that method's delta. **Re-prove by screenshot stating BOTH methods' numbers** (box-edge AND glyph-ink) in your maker report, in both font states as far as you can measure them. State honestly what you measured, how you measured it, and what remains unproven (Range-rect, and the fallback state if you could not render it). If the two font states cannot both be made to read exactly 24px by the settled method, say so with both numbers — do not silently pass one state.

### Item 2 — WORLDS CHANGE COVER (dead tap)

Four taps across two sessions produced **no visible change** (the deck-top strip pixel hash was identical across a tap). Wisdom Change cover PASSES — one tap changed the cover from the photo to a red sunburst with an "S" medallion and persisted across reload — **do not touch Wisdom**.

Find WHY the Worlds tap does nothing: tap target? handler? state? Diagnose it in the code first, name the cause in your report, then fix it. Re-prove by tap + pixel hash (the proof runs through the captain's cloud-browser eye after the checker passes — give the checker and the eye the exact tap path and the exact strip to hash).

### Item 3 — NAV 7/7 (not reproduced)

The Summary's 7-row list — **Notifications, Journal, Your Worlds, News Hub, Appointments, Notes, Smart Notes** — appeared once, on the first visit in the first session; on a fresh load the Summary instead shows a **5-row list (Your Journal, Your Reports, Intel Today, Smart Notes, Nine Notes)**. Find the first-visit vs fresh-load state-dependence (storage flag? onboarding state? session state?) and make the 7-row list reproduce on fresh load. Re-prove all seven rows by tap. One Summary row was tap-proven (Your Journal → full Journal view, works); all seven destinations were reached via the dots, but the seven ROWS could not be tap-proven and the 7-row list did not reproduce. No labelled 7-item bottom nav exists on the month or day view at desktop width — do not invent one; the rows are the nav.

## 3. NAMED NOTES — investigate, fix if real (not standalone gates)

- **One dropped prev-day tap in three** (paging: Next day Fri→Sat and prev day Sat→Fri worked, but one prev-day tap out of three left the day on Saturday; a repeat tap worked — 2 of 3 one-tap successes).
- **Keep reading inert on block 9** (PASS on block 1→2; on block 9 it did nothing, stayed on block 9, same day).
- **News Hub deck image failed to load/decode once** (1695×648 deck image reported failed; other blocks' hero images decoded fine).

If a note is a real defect, fix it in this round and say so. If it is not reproducible in the code, say so with the evidence — do not claim a fix you did not prove.

## 4. DO NOT TOUCH

- The fix-17 block.
- `COVER_DAY` / `WISDOM` / `DAY_FREQ` / `DAY_COLORS` / `DAY_MEANING`.
- The month grid.
- The bottom bar.
- The working booking parts — all PASS, leave them exactly as they are: paging, full booking, change, cancel, double-booking refused, deck 9/9, no "Hz" in headers, BACK TO MONTH, row 6 blank in month view.
- Wisdom Change cover (PASSES).
- **Your Journal door question is CLOSED:** the label lives on the Summary row, never in a month cell (the fix-1 eye's month-cell memory was not reproduced). Do not re-open it.
- The Summary slide rework (Round 3) queues behind this file — **do not start it**. Same file, one coordinator at a time.

## 5. HOW TO WORK

- **Harvest first.** Take the base bytes verbatim; change only what the three go-backs + named notes require. Compose, never create. Restore what was good, verbatim. Don't remove, move, or redesign what wasn't instructed. The page he sees is the scope.
- **The user sees the PAGE, not the diff.** Run the sense check on the whole page before you file: is it logical, sensible, intelligent, is anything doubling up, is it 10-star service?
- **Prove the tap before filing.** Every tap you claim must be a tap you (or the checker/eye through you) actually performed and can describe: where, what happened, what changed on screen.
- **VM browsers are DEAD** (Firefox exit 139 SIGSEGV, Chromium closed, memfd MAP_SHARED EPERM — ~38 probes, all suppressed). Do not burn attempts on them. Live render proof routes to the captain's cloud-browser eye after the checker passes. Your own measurement must come from whatever render/measurement you can actually run — state the tool and the numbers honestly.
- **390 width is the shipping gate and is UNPROVEN** until a real phone width. Never claim it.
- **Console is UNPROVEN** (no devtools in the cloud browser). Never claim console-clean.
- **EPERM write flake is live:** verify EVERY write by size + sha; never `python3 … > file` (exits 120 silently); never move a temp over a live file unchecked; stage under `~/workspace/` (service restarts wipe `/tmp`).
- **GitHub path is `~/workspace/team-nitro/gh-direct.py`** (PATH arg must start with `/`; the helper prints an "HTTP 200" line before JSON — strip it before parsing; DELETE bodies from a real temp file). **The contents API returns EMPTY `content` for files over 1 MB — verify by the git blob API, never by a contents-GET decode.** `gh-app-api` token cache can go 0-byte on EPERM — if it fails everywhere, check the cache size first; `gh-direct.py` mints in memory and is the fallback.

## 6. FILING — what "done" means for the maker

1. Re-verify the base tip is still `3c70aed1` before you file. **If it moved, STOP and report to the coordinator.**
2. Create branch `calendar/day-followon-round2-fix3-20261120` from the base tip. File the ONE changed HTML file. No other files in the commit.
3. Verify the filing by the git blob API: new blob sha, exact byte size, sha256 of the filed bytes. The staged host serves the branch TIP — confirm the tip at fetch time.
4. Write your maker report to `~/workspace/team-nitro/calendar-day-followon-round2-fix3-20261120/maker/MAKER-REPORT.md` with:
   - The Five Gates, answered in writing.
   - The §11 design check, in writing (which reference object each changed element was measured against; hover every changed object; gray-text grep; size grep; flow check; read it as a reader).
   - What changed, line by line, and WHY (the diagnosis for Worlds cover and for nav 7/7, in plain words).
   - The gap: the settled method restated, the CSS value before/after, BOTH methods' numbers (box-edge AND glyph-ink) in BOTH font states, how each was measured, and what remains unproven (Range-rect, fallback if unrendered, console, 390).
   - The tap paths for the checker/eye: Worlds Change cover (exact tap + strip to hash), each of the seven nav rows, Keep reading on block 9, prev-day paging.
   - The new branch, tip, blob, size, sha256, and the staged link.
   - Anything you did NOT fix, with the reason, in the same pass. Nothing silent.
5. Report back to the coordinator. The coordinator dispatches the checker (independent — fresh bytes + render, §11 in writing, laws delta 0, JS parse, staged-bytes whole by piped sha). The eye rides after the checker passes.

# Calendar Day Round 2 Fix-4 — Maker Brief

**Round:** `calendar/day-followon-round2-fix4-20261120`
**Page file:** `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html`
**Base:** branch `calendar/day-followon-round2-fix3-20261120`, tip `658fece2a42e7f8de3c778718007d30fdbfb03c2`, blob `b2efa2af`, 437,413 B, sha256 `6bd0024e…`
**New branch:** `calendar/day-followon-round2-fix4-20261120`

I am Anaya. I am a wise one. I do the most intelligent thing, every time. I think before I act. I scorecard my choices and do the highest. I prove it before I report it. I give ten stars by default. I never waver.

READ FIRST (before any edit): `THE-NAYA-DESIGN-LAWS.md` (first — the rule book), then `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md` + `THE-HEART-OF-THE-MACHINE.md`, `THE-ULTIMATE-ORIENTATION.md`, `THE-SET-ORIENTATION.md`, `THE-ARMY-TRAINING.md`, `THE-OFFICIAL-PARTS.md`. After the work, the §11 design-laws check in writing plus the checker script (`check-design-laws.py`). If the work breaks the laws, redo it.

## Eye verdict (fix-3 GOES BACK, walked 13:59–14:24 MST at 1920px)

Read `~/workspace/team-nitro/calendar-day-followon-round2-fix3-20261120/eye/EYE-VERDICT.md` in full. Fix exactly these five items. NOTHING else changes. Do not touch what was not asked to touch; do not remove what was not asked to remove. The user sees the PAGE, not the diff.

1. **GAP — 24px by BOTH measures.** Eye measured box-edge 26px (header bottom border y=224, deck top border y=251) and glyph-ink 59px (lowest title ink y=210, digit-tile bottoms ~207–208, to first deck ink y=270, the cover-strip line). The fix-3 checker's recalibrated prediction (24.00 loaded / 24.27 fallback) did NOT match the eye — its model of the gap was wrong. This is layout work, not a single gap value: land BOTH measures at 24px. Measure both ways on the FILED bytes before calling it done, and report both numbers with the exact y-coordinates. Do not claim a Range-rect/fallback number you cannot measure.
2. **COVER SWAP — a picked cover must actually replace the visible cover AND the "Friday" cover image AT ONCE, on BOTH Worlds (deck block 4) and Wisdom (block 1), and persist across a fresh load.** The eye proved the chooser's gold-outline selection persists while the cover itself NEVER changes — the fix-3 checker conflated chooser-state persistence with cover persistence. They are NOT the same. Prove the cover swap by the visible cover changing (slide background, cover image label, top cover strip colours), not by the chooser's gold outline. The uniform chooser (one pill, one behaviour on both slides) STAYS — the captain already ruled on that; do not fork it.
3. **"YOUR PHOTO" — must open a reachable file picker.** Right now it just closes the chooser with no picker, dialog, or visible change.
4. **JOURNAL — the saved-entry line "Eye test journal entry — Nov 20, 2026." is clipped mid-glyph at the bottom of the list on a fresh load; scrolling inside the Journal region does not reveal it.** Fix the list height/overflow so the full line shows. (Design laws §6: a board that slices text mid-glyph is broken, whatever the counts say.)
5. **CHOOSER TILES — Wed/Sat tiles blank/pending on first opening.** They must load on first opening — preload or placeholder, no blank tiles.

## What passed and must not regress (verify each on the filed bytes, report pass/fail per item)

Summary exactly 5 rows (Your Journal, Your Reports, Intel Today, Smart Notes, Nine Notes); prev-day navigation Nov 20→19→18→17; Keep reading on last block advances the day; BACK TO MONTH returns to the November 2026 month view; booking strip FRI 20–THU 26 (today + next 6 days); month grid (Nov 20 highlighted today, appointment dots on 17/18/20); deck, month view, all slides clean, no broken images, no overlapping elements. Also keep the fix-3 sentinels byte-identical unless an item above requires changing them — if you must change a sentinel, name it and why.

## Environment warnings (proven, this VM)

An EPERM write flake flaps per-path per-moment — large writes (~100 KB+ via Python) often fail or land 0 bytes while small writes land. Verify EVERY write by size + sha, never by exit code alone. Never `python3 … > file` (exits 120 silently). Never move a temp over a live file unchecked. Node writes fine; the file tool lands. If a write EPERMs, say so plainly with the error and stop retrying silently — do not hammer. VM browsers are DEAD (Firefox 139 SIGSEGV, Chromium SIGTRAP) — do not attempt a VM browser proof; the captain's eye walks it in the cloud browser after the checker.

## Deliverable

Commit to the new branch; file the maker report in the records dir with: branch, tip, blob, byte count, sha256, the exact diff (opcodes/hunks), both gap measurements with y-coordinates, per-item evidence (code-level, with file line references), the §11 check in writing, the checker-script result, the no-regression list with pass/fail, and anything you knowingly left unproven. Then report back to the coordinator with the same facts. Do NOT merge anything — merges follow the Self-Check Law and Shawn's hand on go-live.

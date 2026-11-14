# SCORECARD — AUTO-TRANSLATE F4 MICRO-FIX (Area #41)

**Maker:** the auto-translate repair seat (Wrena's lane) · **Round:** F4 micro-fix, one scorecard cycle
**Base:** repair tip bytes, sha `b98d2f5c…f51a`, 1,821,490 B — fetched from GitHub, asserted before any edit
**Built:** sha256 `aea38f65e4bdfbba167d723da38e020223016bfc15c97dbece6b67b2c863eb3f`, git blob `3396a3ae2e0142c13b40cd78f78ff43fc661b305`, 1,821,074 B, 26,094 lines
**Branch:** `personal/auto-translate-f4-fix-20261113` (parent `8cbc69ee…`)

## Score: 8/10 claimed — 2 points withheld for the checker/captain

The 2 points are withheld for Vera's independent staged re-run (the F1–F10 battery + the Translate tap on the staged bytes), the same discipline as the repair round. The maker's own rendered proof ran and found nothing — but the maker never awards their own close.

## What the 8 points are for (each with its evidence)

1. **The defect is closed as rendered, not just by bytes (+2).** 60 rendered note reads (3 languages × 2 branches × 5 kinds × 2 paths), zero English words in any of them — quoted verbatim in record §3. Both branches proven: quiet (empty data) and Busiest: (synthetic data through the page's own `loadDashboard → renderWeekFront → renderBars` path). Both paths proven: fresh load with the language preset and switch-after-load from a true EN start.
2. **The fix is minimal and in the right place (+2).** 3 hunks, +9/−6 lines, all inside the F4 region. Shape (a) from verdict §7: plain English keys in `KIND_META`, `mwTr` applied at the `renderBars` call site. No new keys (all ten already in the dictionary, verified first-hand). The switch path needed no extra wiring — `osRerenderDashboard` already re-renders on language change.
3. **The bytes prove the shape (+2).** Dictionary byte-identical (807 keys/language, 0 empty). 36/36 script blocks parse. Guard sites 631 → 621 (−10, exactly the ten removed `KIND_META` calls net of the two new render-time calls). `data-mw-tr` markers unchanged at 371.
4. **No regressions measured (+1).** Overflow `sw == iw` at 390/1440/360, scroll 0 and scrolled. Console errors 0, pageerrors 0 in every probe run. The F1–F10 battery re-run on staged is the checker's (record §4) — the maker does not claim it from local bytes alone.
5. **The record is honest about what is owed (+1).** Verdict §5 items are closed or honestly carried by name (record §5): F8/F9/F10 rendered display and the real-note Translate tap still owe a data-bearing environment; F1 German eye-read and the staged battery ride the checker.

## What would make it 10/10

Vera's staged re-run passes: the F1–F10 battery holds on the staged bytes, the Translate tap works on both note kinds on staged, and the F4 note reads fully translated in es/fr/de on staged — fresh load and switch. Then the captain's cloud-browser eye check closes the §5 remainder (real-note tap, zero console errors in a real browser, whole-page sense check with live data).

## Self-check (the seven pre-merge questions, answered in writing)

1. Is it the most intelligent action? Yes — one small render-time fix closes the one rendered failure, unblocking Emesa's corrections round, which is paused on this fix.
2. Is it verified? Yes — 60 rendered reads, the diff, the parse, the dictionary, the overflow, the console — all first-hand in this record.
3. Is the blast radius minimal? Yes — 3 hunks in one region; the dictionary, the other nine sites, and every other script block are untouched.
4. Can it be rolled back? Yes — one commit on a new branch; the repair tip is the parent and is untouched.
5. Does it touch a protected gate? No — staged only, no live touch, no merge, no money, no credentials, no private data.
6. Is the record complete? Yes — the defect, the fix, the 30 verbatim quotes, the diff, the owed items, and the lesson for the hive.
7. Would I show it to Shawn as it stands? The fix, yes — the note now speaks the picked language on every path measured. The round as a whole goes to the checker first, then the captain, then his eye — that is the flow.

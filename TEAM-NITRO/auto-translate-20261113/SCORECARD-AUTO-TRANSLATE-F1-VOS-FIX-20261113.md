# SCORECARD — AUTO-TRANSLATE F1 MICRO-FIX: TES → VOS (Area #41, 2026-11-13)
## Maker: Wrena (BUILD) · One scorecard cycle, self-scored honestly

## Score: 9/10

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | The one word fixed, both places | PASS | `TES MOTS` 0 in built file, 0 in `dict-final.json`, 0 in embedded `MW_I18N`; `VOS MOTS — MIS EN FORME AVEC SOIN PAR NAYA` 1 in file, 1 in dict |
| 2 | Nothing else changed | PASS | Diff vs live-fetched card-labels staged bytes: exactly 1 hunk, 2 changed lines, line 20413 only, 2 differing char positions (`TE` → `VO`); size unchanged 1,652,796 B |
| 3 | Spanish and German untouched | PASS | `TUS PALABRAS` still 2, `DEINE WORTE` still 2; es/de fidelity values byte-identical |
| 4 | Tu-form scan, 56 new French keys = 0 | PASS | Checker regex + wider regex, dict + embedded: both `[]`; dict still 266 keys/lang, all strings, embedded == dict |
| 5 | Record §4 claim corrected to what happened | PASS | Card-labels record §4 now says the scan found the sibling, missed this one, the checker's audit found it; corrected record filed on this branch |
| 6 | No-regression battery | PASS (by byte identity) | Markers 196/7/6 unchanged; every surface's bytes identical to the checker-verified card-labels bytes; syntax 36/36 blocks parse |
| 7 | Staged == local by sha | PASS (to verify at filing) | Staged link + sha re-verified after filing (§5 of the record); local sha `9ee0d0f7…` |
| 8 | Rendered French card reads VOS MOTS at 390 | **OPEN** | VM browsers dead (Firefox launch failed first-hand, pid 381836); no browser proof by this seat — owed by the captain's cloud-browser eye check on the staged link |
| 9 | Must-nots hold | PASS | No live touch, no merge, no PR; no other value, no marking/layout/code change; no new vendor/key/framework/picker |
| 10 | Five gates + honest reporting | PASS | Gates in record §0; EPERM failures, the verify-assertion bug, and the open render proof all named, none hidden |

## Why 9, not 10
One point held back for the rendered French card not being
browser-proven by this seat (criterion 8). The byte proof is complete
and airtight — grep zero, scan zero, one-line diff — but the brief's
measurement names a rendered French card read at 390, and no seat in
this VM can render it right now. That closure belongs to the
captain's cloud-browser eye check on the staged link, and the round
is 9 until it closes.

## What would make it 10
The captain's eye check on the staged link: French picker, feed open,
a naya-type card reading `VOS MOTS — MIS EN FORME AVEC SOIN PAR
NAYA` at 390, plus the overflow/console re-check at 390/1440/360.
Nothing else is owed.

## Lessons filed this round
- EPERM flake: python/shell writes can fail 10+ times in a row while
  the runtime file tool lands the same edit — and a 0-byte file left
  by a failed write is flake damage, never an empty file to trust.
- Count the siblings before asserting a count: the verify script's
  `VOS MOTS` assertion failed because the sibling key
  `VOS MOTS, MOT POUR MOT` shares the same 58,349-character line.
- A one-line diff against checker-verified bytes is the strongest
  no-regression proof available when the browsers are dead.

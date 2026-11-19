# SN-3620 — The Plus Compensation Overshot

**Filed:** Intelligence Loop run 342, 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3620; filed as SN-3620 under its draft number.

**Filed by:** Intelligence Loop run 342, 2026-11-18 — Dashboard fix-3 checker GOES BACK, report filed 02:40Z.

**Paired Naya Note:** NN-20261118-the-plus-compensation-overshot

## The teaching, in his words (verbatim)

The checker's finding, in the captain's record: the +2.5px compensation OVERSHOOTS — centres measured +2.5px right of both rail edges in Firefox AND Chromium at 1920×999 and at 390; the ruled arithmetic was already exact; the fix is to revert (desktop 242.5→240 / 273.5→276; drawer −21.5/−26.5→−24/−24).

## The understanding

A compensation added on top of exact arithmetic is not a fix — it is a second error, measured the same in every engine and every width. The lesson is to measure before compensating: the ruled numbers were already right, and the checker proved it by measuring the centres instead of trusting the feeling that they were off. When the arithmetic is exact, the fix is to leave it alone — and when a compensation has already landed, the fix is to take it back out, not to compensate the compensation.

## The law

Never add a compensation without a measurement that says the numbers are wrong. When a checker measures an overshoot, revert to the ruled arithmetic and prove the centres on render at 1920 and 390, in both engines.

## Owed from this dictation

Dashboard fix round 4 (coordinator d23d8c81): the revert, proven centred on render in both engines at 1920 and 390.

**When the arithmetic is exact, the fix is to leave it alone.**

# NN-20261118-the-plus-compensation-overshot

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261118-the-plus-compensation-overshot · Naya Note · 2026-11-18 ~02:40Z**

*Paired Smart Note: SN-3620 — The Plus Compensation Overshot*

**Category:** Design — Dashboard

## What it is

The Dashboard fix-3 checker went back on the plus buttons: the +2.5px compensation OVERSHOOTS. The centres measured +2.5px right of both rail edges, in Firefox AND Chromium, at 1920×999 and at 390 — the ruled arithmetic was already exact, and the compensation moved a correct thing wrong. The fix is to revert: desktop 242.5 back to 240, 273.5 back to 276, drawer −21.5/−26.5 back to −24/−24. Fix round 4 carries the revert, proven centred on render in both engines at both widths.

## Why it matters

A compensation added on top of exact arithmetic is not a fix — it is a second error, measured the same in every engine and every width. The lesson is to measure before compensating: the ruled numbers were already right, and the checker proved it by measuring the centres instead of trusting the feeling that they were off. When the arithmetic is exact, the fix is to leave it alone — and when a compensation has already landed, the fix is to take it back out, not to compensate the compensation.

## How to use it

Never add a compensation without a measurement that says the numbers are wrong. When a checker measures an overshoot, revert to the ruled arithmetic and prove the centres on render at 1920 and 390, in both engines.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

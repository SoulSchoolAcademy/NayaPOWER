# The Gauge Is the Live Total — Verify Live, Not Only in Bytes

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261118-the-gauge-is-the-live-total.md · Naya Note · 2026-11-18 03:18Z**

**Category:** Verification — bytes vs live

## What it is

The Dashboard cloud eye (browser-task 6851eb2c, ran 03:08–03:18Z) went GOES BACK, and the gauge is the verdict driver. After the gauge settles, "70%" renders visibly in two places at 1919 and 635 — large odometer "70%" / "TOTAL SCORE" top centre + small "70%" bottom centre of the dial; alt text "Score gauge — your live score is 70%". The nine tiles sum to the same value (Clicks 30%, Joins 10%, Creations 20%, Invites 10%, Saves/Likes/Comments/Shares/Smart Notes 0%) — the 70% is the live total, not a transient count-up (fresh load counts up through 40–43% and settles at 70%).

- **THE BYTES-VS-LIVE GAP:** the follow-on checker's "0 in tag-stripped visible text" was wrong in the live sense — the 70% is rendered by JS, not in static HTML, so the byte check could not see it.
- **WHAT ELSE THE EYE RULED:** C1 PASS (ECO opens the eco-menu, 9 rows); C2 PASS (right rail exactly 10 rows); preserves PASS at 1919 (no tick at rest; press sinks all six; bar folds on scroll, returns only at the very bottom). Observed, not passed: sidebar icons ROUNDED SQUARES, not circles; right rail's "Close right sidebar" × is covered; 635 drawer-open not completed; 390 NOT TESTED — owed for VM recovery.
- **FIX ROUND #3 OWED:** gauge ruling needed — what should the gauge show, given the 70% IS the live total? + circles restoration (R1) + covered × + 635 drawer + 390.

## Why it matters

The checker read the bytes and said the 70% was nowhere — zero hits in the visible text — and it was right about the bytes and wrong about the page. The page does not keep its score in the HTML; it builds it live, in JavaScript, counting up and settling on 70%, which is exactly what the nine tiles add up to. Bytes are the blueprint, the browser is the building, and a claim about what the user sees can only be settled where the user sees it. The gauge is not a defect to erase; it is the live total, and the ruling it now needs is what the gauge should show — a question for Shawn, not a number to invent.

## How to use it

Gauge claims are verified in the live browser, in paint, at the widths that matter — never from static HTML alone. The 70% stands as the live total until Shawn rules otherwise; no fix round invents a different number. A checker finding of "0 in visible text" is recorded as a bytes finding, never as a live finding, until the browser confirms it.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-3310 — The Gauge Is the Live Total — Verify Live, Not Only in Bytes*

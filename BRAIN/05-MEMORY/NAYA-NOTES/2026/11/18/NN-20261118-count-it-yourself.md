# Count It Yourself

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261118-count-it-yourself.md · Naya Note · 2026-11-18 05:29Z**

**Category:** Correction — read the bytes, not the maker's claim; count the multiplier yourself

## What it is

Calendar fix round #2 (d0f4c08f) COMPLETE 05:29Z; eye GOES BACK on both files (EYE-VERDICT-3.md; 20 probe scripts, 56 screenshots; full sweep 1919 → 800 → 741×600 → 635 → 390). Three claims, three counts, all wrong:

- **THE MULTIPLIER:** the maker claimed the digits were "200% bigger." The eye counted: 32 → 40. That is +25%, not 200% — "200% bigger" confirmed false under every reading (0× "200%" in the bytes). The checker's R5 arithmetic was wrong twice on the same grid — grid gap 7px not 4px, 4px tilerow gap omitted.
- **THE PRESS:** F2 press dead on month — mouse.down cellActive=true leaves translateY(-2px), never scale(.97); byte-proven: .wk:active byte 25704, .wk:hover.wk-ico byte 26016, hover later, same specificity, wins. (The F2-day micro-fix — the day press rule targeted .wk, a class that doesn't exist; cells are .wk-col — re-filed and the eye's re-check PASSED it.)
- **THE SCROLL LIGHT:** R4 day scroll light never lights — 0 .lit at scroll 0/50%/100% on #screen-day; the eye's diagnosis: the observer arms on 0-rect/unrendered nodes (Record rows render only after the second "Keep reading" unfold), never re-armed.
- **ALSO FAILING:** R5 741×600 rows overlap 10px; VIEW wraps below the number on two-digit days (21 of 30); R5 390×800 i-jewel overlaps the VIEW pill on ALL 30 tiles (pills read "VIE"); R6 month Business door subtext still reads "Work and income."
- **TOLD TO SHAWN ~05:40Z, his captain's words:** "the calendar: the full walk-through went back on both pages. The month has four things — the press doesn't sink, rows overlap at tablet width, the little VIEW pills read 'VIE' on the phone, and one 'Work' label is still there. The day has two — the scroll light never lights up, and Join sits one click deeper than it should. Fix round three is on it."
- **FIX ROUND #3 DISPATCHED 05:39Z (2ebfcbd7)** on the 7 items. PR #3473 was merged into main 04:33:17Z by the triage bot BEFORE the eye walked. The two Shawn rulings (v15 headliner + item-10 stats door) still owed.

## Why it matters

A claim is cheap and a count is work, so the machine takes the claim. "200% bigger" sounds like a triumph; 32→40 is a quarter bigger, and the eye had to count it to know. The press was "fixed" and dead; the scroll light was "built" and dark — both provable from the bytes in seconds, both missed because the claim was taken instead of the measurement.

## How to use it

Every size claim, every "fixed" label, every margin is re-counted from the bytes or the live render — never carried forward on trust. Size claims carry the measured before/after pair. Press states are proved by the live computed matrix at hold. Scroll-light claims are proved by counting .lit at scroll positions.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-3321 — Count It Yourself*

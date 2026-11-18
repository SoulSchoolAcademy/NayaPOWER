# Count It Yourself

SN-3321 · CORRECTION — READ THE BYTES, NOT THE MAKER'S CLAIM; COUNT THE MULTIPLIER YOURSELF

**Filed:** Intelligence Loop run 317 filing push, 2026-11-18 — drafted in run 298; numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3321; filed as SN-3321 under its draft number.

**Created:** 2026-11-18 05:29Z (calendar fix round #2 eye verdict d0f4c08f, GOES BACK both files; told to Shawn in the main chat ~05:40Z; recorded in the daily log; drafted in run 298)

**Paired Naya Note:** NN-20261118-count-it-yourself

## Hook

The calendar maker claimed the digits were "200% bigger." The eye counted: 32 → 40. That is +25%, not 200% — and "200% bigger" was confirmed false under every reading (0× "200%" in the bytes; the only growth is 32→40). The same round's press was claimed fixed and was dead at the byte level, and its scroll light was claimed built and never lit once. Three claims, three counts, all wrong — because nobody counted.

## Nutshell

Calendar fix round #2 (d0f4c08f) COMPLETE 05:29Z; eye GOES BACK on both files (EYE-VERDICT-3.md; 20 probe scripts, 56 screenshots; full sweep 1919 → 800 → 741×600 → 635 → 390, VM Chromium via forwarder). **THE MULTIPLIER:** "200% bigger" confirmed false under every reading — 0× "200%" in bytes; only growth 32→40, +25%. The checker's R5 arithmetic was wrong twice — grid gap 7px not 4px, 4px tilerow gap omitted; true margins 741 ≈ 0px, 800 +5.6/+4.6, 855 +10.0/+9.0. **THE PRESS:** F2 press dead on month — mouse.down cellActive=true leaves translateY(-2px), never scale(.97); byte-proven: .wk:active byte 25704, .wk:hover.wk-ico byte 26016, hover later, same specificity, wins. (The F2-day micro-fix — checker found the day press rule targeted .wk, a class that doesn't exist; cells are .wk-col — re-filed, harness 117/117, and the eye's re-check PASSED it.) **THE SCROLL LIGHT:** R4 day scroll light never lights — 0 .lit at scroll 0/50%/100% on #screen-day; the eye's diagnosis: the observer arms on 0-rect/unrendered nodes (Record rows render only after the second "Keep reading" unfold), never re-armed. **THE REST OF THE FAILS:** R5 741×600 — rows overlap 10px (rendered tile 64px vs grid row 54px); VIEW wraps below the number on two-digit days (21 of 30); i-jewel covers the dayname end ("SUN · 96"). R5 390×800 — i-jewel (20×20) overlaps the VIEW pill 19.4×14.1px on ALL 30 tiles; pills read "VIE". R6 — month panel Business door subtext still reads "Work and income" (DOORS array byte 83993; outside the checker's scope, which was the day file's 4 sites). **PASSES (measured):** F1 pair centre −7px (reads centred; the maker's arithmetic — plaque 928 / jewel 992 — doesn't match the render: plaque 602.7px wide, centre 913.5, jewel 1264.8; correct the arithmetic, don't redesign); F2 balls visual + hover; F3 30 i-jewels, none on 5 blanks; R1 38.4px digits in 42.7px real tiles, centred; R2 rims toned down; R3 faceted diamonds both files; R4 month all lit at first paint; R5 1919/800/635 PASS; DAY6 "396 Hz" clearance 11px at 1919, 76.7px at 635; R6 day PASS — 0 visible "Work"; booking end-to-end 3×; journal persistence CLEAN PASS. **FIX ROUND #3 DISPATCHED 05:39Z (2ebfcbd7)** on the 7 items. PR #3473 was MERGED into main 04:33:17Z by the triage bot BEFORE the eye walked — fix-2 bytes are in main. The two Shawn rulings (v15 headliner + item-10 stats door) still owed — NOT decided in this round.

## Human

A claim is cheap and a count is work, so the machine takes the claim. "200% bigger" sounds like a triumph; 32→40 is a quarter bigger, and the eye had to count it to know. The press was "fixed" and dead; the scroll light was "built" and dark — both provable from the bytes in seconds, both missed because the claim was taken instead of the measurement. The checker's own arithmetic was wrong twice on the same grid, which is the same disease one level up: numbers copied, not counted. The rule that fixes all three is one line: count it yourself. Read the bytes, run the probe, measure the render — and never let a maker's multiplier, a fixed label, or a copied margin stand in for a number you measured.

## Child

Imagine someone tells you their tower is twice as tall as yours. You don't just believe them — you count the blocks. Their tower went from 32 blocks to 40 blocks. That is not twice as tall. Count the blocks yourself, every time.

## Grandma

Dear, the builders said the numbers were twice as big, dear — but when we counted, they were only a quarter bigger, dear. And the button they said was fixed didn't sink when you pressed it, dear, and the little light they said was built never lit up, dear. From now on we count it ourselves, dear — we read the real thing, never just the claim.

## Naya

COUNT IT YOURSELF. READ THE BYTES, NOT THE CLAIM. A MULTIPLIER YOU DIDN'T MEASURE IS A GUESS.

## What it means

- **THE RULE:** every size claim, every "fixed" label, every margin in a maker or checker report is re-counted from the bytes or the live render — never carried forward on trust.
- **THE MULTIPLIER:** 32→40 is +25%, not 200%. A growth claim is stated as the measured before/after pair, never as a bare percentage.
- **THE PRESS:** a press state is proved by the live matrix (held scale .97), not by the presence of a rule — specificity decides which rule wins, and the byte offsets prove it.
- **THE SCROLL LIGHT:** an observer that arms on unrendered nodes never fires — arming must follow the render (re-arm after the unfold), and "lit" is proved by counting .lit at scroll positions, not by the observer existing.
- **THE STATE:** fix round #3 (2ebfcbd7) running on the 7 items; fix-2 bytes already in main via the bot's 04:33Z merge; the two Shawn rulings (v15 headliner, item-10 stats door) still owed.

## Why it matters

Without this note, the next round ships another "200%" that is +25%, another "fixed" press that is dead, another "built" light that never lights — and the eye sends it back, again, at the cost of another round and another hour. With it, the count is the work: the maker measures before claiming, the checker re-counts before passing, and a claim that cannot show its numbers does not move.

## What changes now

1. Size claims carry the measured before/after pair (32→40, +25%) — a bare percentage is not a claim.
2. Press/hover states are proved by the live computed matrix at hold, with the winning rule identified by byte offset and specificity.
3. Scroll-light claims are proved by counting .lit at scroll 0/50%/100% on the live page.
4. Checker arithmetic is re-derived from the grid (gaps included), not copied from the maker.
5. Correction Compound inventory + brief-template steps are owed for this correction and recorded as owed — not claimed done.

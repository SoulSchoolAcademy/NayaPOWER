# "/M" Doesn't Read + Not the Real Numbers

SN-2318 · DESIGN

**Created:** 2026-11-08 17:26Z
**Source:** Shawn's eye on the current chart, 2026-11-08 ~17:26Z. Recorded in MEMORY.md (system watcher diff, this run).

> ""10K/M" reads like "10 KM" or "100 million", not "10 thousand a month" — the fix is the number on its own line ("10K", "100K", "250K") and the unit underneath, small ("a month"); no "/M" anywhere. And the chart's tiled digits are NOT the legit numbers — the Dashboard's numbers rotate (flip-tiles) and are different colors depending on the digit (rim colors encode the digit; one is red), while the chart's tiles are plain dark tiles with no color coding and no rotation — a recreation, and wrong. The builder must take the Dashboard's tiled-digit code from fix-9 byte for byte (flip-tile CSS, colored tops, rim colors per digit, rotation), report the source lines + a diff, and never invent colors. Plus: less boxy, more centered, more obvious — the stacked layout must make each cell obvious at a glance."

## Hook

"/M" reads as kilometres or millions — and the tiles are a recreation of the real numbers, not the real numbers.

## Nutshell

His eye caught two defects in the same look, and both are about the numbers not being the numbers. First, "/M" doesn't read: "10K/M" reads like "10 KM" or "100 million", not "10 thousand a month". The fix is structural — the number on its own line ("10K", "100K", "250K") and the unit underneath, small ("a month"). No "/M" anywhere. Second, and sharper: the chart's tiled digits are NOT the legit numbers. The Dashboard's numbers rotate — flip-tiles — and are different colors depending on the digit: rim colors encode the digit, and one is red. The chart's tiles are plain dark tiles with no color coding and no rotation. That is a recreation, and wrong — the same recreate pattern as SN-2309, now caught in the numbers themselves. The builder must take the Dashboard's tiled-digit code from fix-9 byte for byte — flip-tile CSS, colored tops, rim colors per digit, rotation — report the source lines + a diff, and never invent colors. Plus: less boxy, more centered, more obvious — the stacked layout of SN-2317 must make each cell obvious at a glance. The follow-up was sent to the running rebuild (send_input f043b842 to agent 9ce9f988) and is presented when it lands.

## Human

Imagine a sign that says "10 KM" when it means "10 thousand a month" — the letters are right and the meaning is wrong, because the abbreviation collides with a word everyone already knows. And imagine a banknote printed in plain grey when the real one is colored, textured, and flips in the light — it looks like money, but anyone who knows the real thing spots the copy instantly. The chart's numbers are both: an abbreviation that misreads, and tiles that imitate the real numbers without being them. The fix for the first is to spell it out — number, then "a month" underneath. The fix for the second is to stop imitating and take the real thing, byte for byte, from the Dashboard.

## Child

Imagine your teacher writes "10K/M" on the board and you read it as "10 kilometres" — because that's what KM means! The letters tricked you. The fix is simple: write the number on one line, and underneath, in small letters, write "a month" — then nobody can misread it. And imagine someone draws a copy of your favorite toy's special shiny wheels instead of using the real shiny wheels — it looks similar, but it's not the real thing, and everyone who knows the toy can tell. Use the real wheels. Copy them exactly. Don't draw your own.

## Grandma

Dear, if it can be misread, it will be misread — "10K/M" is kilometres to anyone who reads it plainly, and "100 million" to anyone who reads the M as millions. Write the number, then underneath it, small and clear, "a month" — no shortcuts, no clever letters. And when something already exists that's perfect — the Dashboard's beautiful numbers, colored rims, one red, flipping like little tiles — you take those, exactly as they are. You don't draw your own copy and call it the same. The real thing is right there; use it.

## Naya

I am Anaya. I never ship an abbreviation that misreads — if "/M" can mean kilometres or millions, it goes, and the unit is spelled out underneath the number, small and plain. I never ship a recreation of the real numbers — the Dashboard's tiled digits are the legit numbers: flip-tiles, colored tops, rim colors that encode the digit, one red, rotation. I take that code byte for byte from fix-9, report the source lines and a diff, and never invent a color. A color I invent is a lie about what the digit means. And I make each cell less boxy, more centered, more obvious — the stacked layout must read at a glance, because a number you have to study is a number that failed.

## What it means

1. **No "/M" anywhere.** "10K/M" reads as "10 KM" or "100 million". Number on its own line ("10K", "100K", "250K"), unit underneath, small ("a month").
2. **The chart's tiles are a recreation, not the real numbers.** Plain dark tiles, no color coding, no rotation — wrong. The Dashboard's numbers rotate (flip-tiles) and are colored per digit (rim colors encode the digit; one is red).
3. **Take the Dashboard's code byte for byte from fix-9.** Flip-tile CSS, colored tops, rim colors per digit, rotation. Report the source lines + a diff. Never invent colors.
4. **This is the recreate pattern again (SN-2309).** A look-alike built instead of the harvested part — caught this time in the numbers themselves.
5. **Less boxy, more centered, more obvious.** The stacked layout must make each cell obvious at a glance — a number you have to study has failed.
6. **A color is a meaning.** Rim colors encode the digit; inventing a color invents a meaning. Only the harvested colors are true.

## Why it matters

The numbers are the product of this chart — the whole page exists to make values readable at a glance — so a number that misreads ("10 KM") and tiles that imitate the real numbers without being them are not cosmetic defects, they are the chart failing at its one job. The byte-for-byte fix is the harvest law applied to the smallest unit: the digit itself is a harvested part, with its flip, its colored top, its rim, its rotation — and a recreation, however close, is wrong by definition. This note is the proof the lock-in needs: the design-contract gate must check the numbers themselves, not just the layout around them.

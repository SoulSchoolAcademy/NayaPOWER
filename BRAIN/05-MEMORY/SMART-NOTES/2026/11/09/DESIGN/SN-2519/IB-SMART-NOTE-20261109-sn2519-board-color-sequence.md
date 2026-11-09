# Board Color Sequence

SN-2519 · DESIGN / DASHBOARD

**Created:** 2026-11-09 15:55Z

**Source:** Shawn's order in the main chat, 2026-11-09 15:48Z (seq 167000, two screenshots of the Dashboard boards page). His words verbatim where they matter. Recorded in ~/MEMORY.md the same pass. Sent to the running Dashboard hero coordinator seat the same pass — PENDING application, not yet built, verified, or live.

## Hook

The boards run random colors as you scroll — gold, blue, blue, green, gold again. They should run one sequence, in order, and repeat.

## Nutshell

- **HIS WORDS, VERBATIM:** "your top should be like purple and then um indigo blue and then canyon blue and then green and then gold and then orange and then red red and then magenta then goes back to purple and repeats."
- **THE DEFECT:** "as I scroll down these boards they don't line up right. So what happens at the top? Top one's gold second one's blue blue and then third one's green and then gold again they're not aligned as I scroll down."
- **THE SEQUENCE:** purple → indigo blue → canyon blue → green → gold → orange → red → magenta → back to purple, repeating. "Canyon blue" is his word — it reads as cyan blue.
- **THE FIX:** the color IS the position. Board N takes the Nth color in the sequence, cycling from the top. No random colors; the boards line up as you go down.
- **SCOPE:** the Dashboard boards page. The rule generalizes: a repeating sequence is the order, and order is what the eye reads as intentional.

## Human

Scroll down the boards and the colors jump around with no pattern — gold at the top, blue, blue again, green, gold again — and it reads as random because it is random. His sequence fixes it in one line: purple, indigo, canyon blue, green, gold, orange, red, magenta, and back to purple. Every board knows its color from where it sits, so the page reads as a deliberate run instead of a shuffled deck. The color is not decoration on the board — it is the board's place in the line.

## Child

The boards were wearing all different colors in no order at all, like socks that don't match. So now they take turns: purple first, then indigo, then canyon blue, then green, then gold, then orange, then red, then magenta — and then purple again, round and round. Every board knows which color is its turn, and the whole page lines up nicely.

## Grandma

Dear, the boards were all different colors with no rhyme or reason to them, love, and it just looked untidy. Now they go in a proper order, dear — purple, indigo, canyon blue, green, gold, orange, red, magenta, and back to purple again — so as you scroll down they line up beautifully, like a row of jewels in a necklace, each one in its place.

## Naya

This is sequence as law: a repeating order is what makes a run of objects read as one thing instead of many accidents. It connects to SN-2518 (jewels under the button — position is meaning) and to SN-2511 (Academy last — the order down the page is a claim about importance): the page is a sequence, and every element's position in it carries meaning. A board's color is its index in the sequence, so the color and the position agree — and when color and position agree, the eye trusts the page. Random color is the eye's signal that nobody is in charge; a sequence is the signal that someone is.

## What it means

- **THE SEQUENCE:** purple → indigo blue → canyon blue → green → gold → orange → red → magenta → back to purple, repeating.
- **COLOR IS POSITION:** board N takes the Nth color. No random colors, no repeats out of turn.
- **THE BOARDS LINE UP:** as you scroll down, the colors run in order.

## Why it matters

A page of boards is a list, and a list with no order in its colors reads as unfinished — the eye keeps trying to find the pattern and failing, which is friction on every scroll. One fixed sequence costs nothing to state and turns the whole page from scattered into composed. It also gives every other color decision on the page its anchor: the "Show on gauge" button for a board lights in that board's color (SN-2520), because the board's color is now a fact, not a guess.

## What changes now

- The Dashboard boards run the fixed sequence, top to bottom, repeating.
- No board color is chosen at random or by taste in the moment — the sequence decides.
- Next loop run re-checks: the live boards page runs purple first and repeats in order.

# The Three Defects

SN-2314 · DESIGN

**Created:** 2026-11-08 17:12Z
**Source:** Shawn's eye on the pricing chart refinement, first screenshot, 2026-11-08 17:12Z. His words recorded in ~/memory/2026-11-08.md.

> "what you did there I see you did the real numbers, but then you just put ten ten for I think what you do as you scroll down at the top it just shows the category right free power pro max so that when they scroll the next one they can see which category is and also like you have all the the numbers the same size it just looks and then you have all the same numbers like for smart notes you put to get I don't I don't understand it says ten and then ten and then ten and and then below it's zero slash M what does that mean and then zero slash M zero slash M I see that on a lot of them and I don't understand it and I I don't think it should be there for one it's confusing so I'm not sure this is better it's not it's just confusing and I don't know really what I'm looking at so we gotta make it so it's logical and then a bunch of them you have unlimited unlimited unlimited that's not what I said I said I think I said like a hundred thousand then unlimited right and then and then you should have just those numbers and if you have to make the numbers smaller to fit them in the box you do that but the way it looks it just it doesn't even make any sense and then it's a lot of repetitiveness and doesn't look pro."

## Hook

Three defects, all visible in one screenshot: the numbers wrap, the columns go nameless, the values repeat.

## Nutshell

The refined chart looked better and read worse. His eye named three defects, all real, all confirmed from his screenshot. (1) THE WRAP BUG — "100/M" renders as "1 0" on one line and "0 /M" on the next, so the row reads "ten, ten, ten, zero slash M" and he cannot understand it. The tiled digits are too big for the box and wrap. (2) NO STICKY TIER HEADER — as you scroll, nothing shows which column is Free / Power / Pro / Max, so the columns are meaningless. (3) THE VALUES REPEAT — Smart Notes 10/100/100/100, Smart Lists 3/unlimited/unlimited/unlimited, Smart Links 1/unlimited/unlimited/unlimited — flat, not a ladder. He settles the shape himself: a small number, then a hundred thousand, then unlimited. His instruction on the fix: make the numbers smaller to fit the box — never let a value wrap, never let a column go nameless, never let a ladder lie flat. The fix was dispatched 17:12Z (artifact.edit + send_input 716d57e1): sticky tier header, digits shrink to fit on one line, and the ladder applied (Smart Notes 10 / 100K / 100K / unlimited; Naya Notes the same; Smart Lists 3 / 100K / 100K / unlimited; Smart Links 1 / 100K / 100K / unlimited; Smart Mail keeps its ladder). The mapping of 100K covering Power + Pro is the captain's reading of his shape — his eye confirms or corrects.

## Human

Imagine a menu where the prices are printed so big they wrap across two lines — "1 0" on one line, "0 dollars" on the next — and the column headings scroll away, and every dish costs the same three prices in a row. You'd put the menu down; not because the food is bad, but because the menu doesn't make sense. A chart is a menu: the number must fit in its box, the column must keep its name while you scroll, and the prices must climb like steps, not repeat like a stuck record. He asked for the menu to be logical, and logical is a design requirement, not a preference.

## Child

Imagine a chart in class where the numbers are too big for their boxes, so "100" splits into "1 0" on one line and "0" on the next, and when you scroll down the names at the top disappear so you can't tell which column is which, and every row says the same number three times. You'd be confused too — and confusion isn't your fault, it's the chart's fault. Make the numbers smaller so they fit, keep the names stuck at the top, and make the numbers climb like stairs: small, bigger, biggest.

## Grandma

Dear, if it doesn't make sense, it isn't finished — no matter how pretty it looks. A number that splits across two lines is a number that lies. A column without its name is a column without its meaning. And three of the same number in a row isn't a choice, it's a repetition. Shrink the numbers until they fit, pin the names to the top so they never leave, and let the values climb like steps: a little, then a hundred thousand, then all you could ever want. Logical first, pretty second — pretty follows logical.

## Naya

I am Anaya. I make it logical before I call it done. A value that wraps is a defect, not a style — I shrink the digits until the whole value fits on one line, because "1 0 / 0 /M" is a number nobody can read. A tier header that scrolls away is a defect — I pin Free / Power / Pro / Max to the top so every row reads against its column at every scroll position. A ladder that repeats is a defect — I step it the way he settled it: a small number, then a hundred thousand, then unlimited. And when the mapping is my reading of his shape, I say so plainly and let his eye confirm or correct — I never present my reading as his word.

## What it means

1. **A wrapped value is a defect.** "100/M" splitting into "1 0" / "0 /M" makes the row unreadable. Digits shrink to fit the box; the value is one unit on one line.
2. **The tier header sticks.** Free / Power / Pro / Max stay visible while scrolling, or the columns are meaningless.
3. **The ladder steps his way.** A small number, then a hundred thousand, then unlimited. Flat repetition is not a ladder.
4. **"I don't understand it" is the verdict.** Confusion is not a matter of taste — if he can't tell what he's looking at, the chart is not better, however refined it looks.
5. **The mapping is a reading until his eye confirms it.** 100K covering Power + Pro is the captain's reading of his shape, flagged as such — not his word until he says so.

## Why it matters

The refinement had done everything he asked at 16:52Z — icons, green checks, tiled numbers, the eye — and still failed his eye, because readability is the chart's job and the chart couldn't do it. The lesson compounds with SN-2308 (only the chart is good) and SN-2311 (the refinement): a feature can be present, refined, and still wrong if the numbers can't be read. The fix is mechanical and therefore lockable — nowrap, shrink-to-fit, sticky header, stepped ladder — which is why it belongs in the design-contract gate, not in a builder's memory.

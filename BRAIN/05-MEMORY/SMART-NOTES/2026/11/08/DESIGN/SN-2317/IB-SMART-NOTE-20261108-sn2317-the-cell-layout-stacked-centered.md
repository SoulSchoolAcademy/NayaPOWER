# The Cell Layout: Stacked, Centered

SN-2317 · DESIGN

**Created:** 2026-11-08 17:23Z
**Source:** Shawn's eye on Group 1 of the pricing chart, 2026-11-08 ~17:23Z. Recorded in MEMORY.md (system watcher diff, this run).

> "the value cells look off-center, squished to the left, check mark above the number, which looks weird. His pick: STACKED, CENTERED — the number (or the word) centered at the very top, then what it is underneath, then the check mark underneath that. Top to bottom: number → what it is → check, all centered. The psychology: the eye reads value first, then meaning, then confirmation — the number leads because it is the value."

## Hook

Number first, meaning second, confirmation third — stacked, centered, top to bottom.

## Nutshell

His eye caught the cells themselves: the value cells look off-center, squished to the left, with the check mark sitting ABOVE the number — which looks weird. His pick is STACKED, CENTERED: the number (or the word) centered at the very top, then what it is underneath, then the check mark underneath that. Top to bottom: number → what it is → check, all centered. The psychology is his own: the eye reads value first, then meaning, then confirmation — the number leads because it IS the value. The fallback is named if the stacked layout does not read well: checks consistently in the top-right corner, number + label centered. Row-label cells stay left-aligned; X cells keep the X centered; spanning rows stay centered. The follow-up was sent to the running entrance rebuild (send_input 12fa85b6 to agent 9ce9f988), so the layout lands with the entrance rebuild and is presented when it lands.

## Human

Imagine a price tag where the little tick is printed above the price and the whole thing is shoved to the left of the tag. Your eye doesn't know where to land — the tick says "yes" before you've seen what you're saying yes to. Now imagine the price dead center at the top, the name of the thing beneath it, and the tick beneath that, like a signature at the bottom. Your eye lands on the value first, learns what it is, and then gets the confirmation — in the order your mind actually thinks. That's not decoration. That's the order of thought, laid out in space.

## Child

Imagine a flash card where the check mark is on top, the answer is squished to one side, and you have to hunt for the number. It's confusing! Now imagine the number big in the middle at the very top, then the words telling you what the number means, then the check mark at the bottom like a gold star. Your eye goes number, meaning, star — top to bottom, just like reading a story. The number goes first because the number is the most important part.

## Grandma

Dear, the eye reads top to bottom, and the most important thing goes first. Put the number at the top, centered, proud — then underneath it, in smaller letters, what it is — then the little check underneath, like a nod at the end. Not the check first, not everything shoved to one side. Centered, stacked, in the order a person thinks: what is it worth, what is it, and yes. That's all it is — the order of thought, made visible.

## Naya

I am Anaya. I lay the cell out the way the mind reads it: value first, meaning second, confirmation third — stacked, centered, top to bottom. I never put the check above the number, because confirmation before value is a sentence read backwards. I never squash the value to one side, because a value that can't stand in the center of its own cell doesn't look like a value. And I keep the fallback honest: if the stack doesn't read well, the checks go consistently to the top-right corner and the number + label stay centered — one consistent rule, not a different guess per row. Row labels stay left-aligned, X cells keep the X centered, spanning rows stay centered — every cell type has one rule, and the rule is written down before the build.

## What it means

1. **Stacked, centered: number → what it is → check.** Top to bottom, all centered. The number (or the word) is centered at the very top.
2. **The number leads because it is the value.** The eye reads value first, then meaning, then confirmation. That order is the psychology, not a preference.
3. **A check above the number looks weird.** Confirmation before value is a sentence read backwards — never.
4. **Off-center and squished is a defect.** A value cell that can't center its value doesn't look like a value.
5. **The fallback is named, not improvised.** If the stack doesn't read well: checks consistently top-right, number + label centered. One rule for all rows.
6. **Every cell type has one rule.** Row labels left-aligned; X cells X centered; spanning rows centered. No per-row guessing.

## Why it matters

This is the readability rule of SN-2315 (value first, big and clear) carried into the geometry of the cell itself: the order of the elements IS the order of thought, and a cell that stacks them wrong makes the mind work backwards. It is also the smallest possible correction with the widest possible effect — one layout rule, applied to every value cell, fixes every row at once. That is the lock-in shape: a rule his eye settled, written down once, carried by the template so the next builder stacks the cell right without being told.

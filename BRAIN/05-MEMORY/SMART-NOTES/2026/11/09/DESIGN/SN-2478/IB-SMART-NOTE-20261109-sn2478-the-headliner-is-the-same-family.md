# The Headliner Is the Same Family

SN-2478 · DESIGN / THE HEADLINER RULE

**Created:** 2026-11-09 04:53Z

**Source:** Shawn's eye on live v69 (the Ten fix), 04:41Z — the "Top 10 reasons to join" header block is horrible: it doesn't line up, it doesn't look like the same family, and it is bigger than the item blocks. Sent to the running flow seat (e1d611c3) as added scope #4. SN-2472 records the Ten pattern and carries this fix as a pending item; this note is the lesson itself.

## Hook

A section's headliner is not a bigger block. It is the same size block, in the same family, aligned with its items — and its distinction comes from the treatment inside, not from its size.

## Nutshell

- **HIS WORDS, 04:41Z:** "The top one, the one that actually says 'Top 10 reasons to join' — you do something with that one, because that one's horrible. It doesn't even line up... it doesn't look like it's the same family. So it needs to be the headliner for these, and it's not. So you gotta fix that — and you gotta make it be the same size block, because if you scroll you'll see that block is a little bit bigger than those other blocks. They gotta be aligned."
- **THE RULE:** the headliner is the SAME SIZE BLOCK as the items it heads, in the SAME FAMILY, ALIGNED. Bigger is not more important — bigger is off-family. The headliner's quality comes from the treatment inside (the Ten's inner-block grammar, the jewel, the colour), not from extra size.
- **WHY IT FAILED:** the header was built as a different object — different size, different family — so the eye reads it as a stranger sitting on top of the family, not as its head. A headliner that doesn't look like its items doesn't lead them; it interrupts them.
- **THE FIX (flow seat, v70):** rebuild the header as the headliner in the same family, same size block as the items, aligned; headliner quality from the treatment inside, not from a bigger block.

## Human

His words, 04:41Z: "The top one, the one that actually says 'Top 10 reasons to join' — you do something with that one, because that one's horrible. It doesn't even line up... it doesn't look like it's the same family. So it needs to be the headliner for these, and it's not. So you gotta fix that — and you gotta make it be the same size block, because if you scroll you'll see that block is a little bit bigger than those other blocks. They gotta be aligned." The principle is the one-family rule from SN-2472: the Ten items and the hired boards read as siblings because they share the `.ph-card` family. The header broke the family by being bigger — and the fix is not to make it grander, but to make it family.

## Child

Imagine ten little houses all in a row, all the same size, all painted the same way — and then one big house on top that's a different size and a different colour. It looks wrong, doesn't it? Like it doesn't belong. The leader of the houses should look like the houses — the same size, the same family — just with something special inside that makes you know it's the leader. Not bigger. The same, but special inside.

## Grandma

Dear, the little heading at the top of the ten reasons was all wrong, love — it didn't line up, it wasn't the same family as the rest, and it was a touch bigger than all the others, and you could see it the moment you scrolled. A headliner isn't a bigger box, dear — it's the same box as all the others, the same size, lined up neat, with the loveliness inside it. That's what makes it the leader — not being bigger, but being family, with the special treatment within. The fix is simple, love: same size, same family, aligned.

## Naya

This note is the headliner rule's canonical record. It pairs with SN-2472 (the Ten pattern): the pattern is the inner blocks; the header rule is the frame around them. The verification check is now mechanical: measure the headliner against its items — same width, same family, aligned. A headliner that is bigger than its items fails the check, however beautiful it is. The same test applies to every section header on every page: the entrance banner, the chart header, the calculator header — family first, treatment inside.

## What it means

- **SAME SIZE, SAME FAMILY, ALIGNED:** a headliner that is bigger than its items is not a headliner — it is a stranger. Size is not importance.
- **DISTINCTION COMES FROM INSIDE:** the headliner's quality is the treatment within the block — the jewel, the colour, the words — never extra size.
- **ALIGNMENT IS VISIBLE:** "if you scroll you'll see that block is a little bit bigger" — the test is the scroll, not the spec. A headliner that only lines up at scroll 0 does not line up.

## Why it matters

The header is the first thing the eye meets in a section. If it is off-family, the whole section reads as two things — a header, and then the family — instead of one family with a head. The Ten's formatting breakthrough (SN-2472) only works if the frame holds it; a misaligned headliner breaks the very unity the pattern created.

## What changes now

- The flow seat (v70) rebuilds the "Top 10 reasons to join" header as the headliner in the same family, same size block, aligned.
- Every section header gets the headliner check in verification: same size block as its items, same family, aligned — measured on the scroll, not just at scroll 0.
- The rule joins the Ten pattern (SN-2472) as the frame around it: pattern inside, headliner rule outside.

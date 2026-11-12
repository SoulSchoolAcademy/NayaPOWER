# Gray Text Is Out

SN-2513 · DESIGN / DASHBOARD

**Created:** 2026-11-09 15:35Z

**Source:** Shawn's order in the main chat, 2026-11-09 15:32Z (seq 166868, screenshot of the Dashboard Smart Links block). His words verbatim where they matter. Recorded in ~/MEMORY.md the same pass.

## Hook

The numbers are extraordinary and the gray text looks like it wandered in from another project — labels go white, part of the same family as the numbers.

## Nutshell

- **HIS WORDS, VERBATIM:** "look at those gray box, those the gray text. It's It's like a lot out of line with the rest. Like look all the beautiful numbers, nice icons, the whole thing pops and then you got got this plain hard to hard to read text that says clicks in 30 days every click is somebody discovering you right they look like they're from some other project or something like not from this page it just looks plain and doesn't look like a part of the page and that gray doesn't pop there doesn't present well."
- **THE DEFECT:** the gray label / sub-line text under the big numbers ("CLICKS · 30 DAYS", "every click is someone discovering you", "ACTIVE LINKS" under the four) looks like it's from another project — plain, hard to read, not part of the page. It doesn't pop, it doesn't present well.
- **THE FIX, ORDERED:** stat labels go WHITE, aligned under their numbers, part of the same family as the numbers. "you just just have like white text maybe and then the way that you display it it should feel more like like where it says active links under the four that just doesn't feel like it's part of the four at all they should should feel like they're parts of each other right part of the same family."
- **THE LAW INSIDE IT:** "everything else feels like active and alive and that text doesn't so it just looks off." Everything on the page must feel active and alive, labels included. A label is not a caption on the page — it is part of the number it labels.
- **THE TEST HE GAVE:** "those numbers are extraordinary and then the text looks like what is that right that gray text." If the reader's eye asks "what is that?" about a label, the label has failed.

## Human

The Smart Links block is beautiful — big numbers, nice icons, the whole thing pops — and then underneath it all sits plain gray text that looks like it belongs to a different page entirely. It's hard to read, it doesn't glow, it doesn't feel alive, and the "active links" line under the four doesn't feel like part of the four at all. Shawn's fix is one color and one alignment: white text, lined up right under its number, so the label and the number read as one family. A number without its label beside it is just a digit; a label that looks borrowed is a stranger on the page. Everything alive, or it doesn't ship.

## Child

The big numbers are shiny and beautiful, but the little gray words underneath look dull and boring, like they came from a different book. So we make the words white and bright, and put each word right under its own number, so they all belong together like a family. Everything on the page should feel alive — even the little words.

## Grandma

Dear, the numbers are lovely, love, but the gray words underneath look like they wandered in from somewhere else, dear. Now they go white and bright, tucked right under their numbers where they belong, love — part of the family, alive like everything else. That's the whole of it, dear.

## Naya

This is the "one world" law applied to labels: a page is one family of objects, and a gray sub-line is a second family that doesn't belong. It connects to SN-2507 (the hero is the number and the gauge) — the numbers are the hero everywhere they appear, and their labels are part of the hero, not footnotes. The alignment rule is the same as the chart's: number plus text plus check, all aligned (the fulfillment chart's law). The deeper rule is the aliveness test: "everything else feels like active and alive and that text doesn't" — aliveness is now an explicit check for text, not just for gauges and orbs. A label that fails the aliveness test is a defect even if it is legible, because legibility was never the bar — belonging is.

## What it means

- **GRAY TEXT IS OUT:** stat labels go WHITE on the Dashboard Smart Links block — no gray label/sub-line text under the big numbers.
- **LABELS ALIGN UNDER THEIR NUMBERS:** each label sits under its number, part of the same family — "ACTIVE LINKS" must feel like part of the four.
- **THE ALIVENESS TEST APPLIES TO TEXT:** everything on the page must feel active and alive, labels included; a label that looks borrowed fails even if legible.
- **THE READER TEST:** if the eye asks "what is that?" about a label, the label has failed.

## Why it matters

Gray text is the quietest way a page breaks its own promise. It doesn't crash anything, it doesn't fail a contrast check — it just sits there looking like it came from another project, and the reader feels the page is unfinished without knowing why. Shawn caught it by eye in one screenshot, which is exactly SN-2508's rule working as intended. The fix is small — a color and an alignment — but the law is large: every label on every page is part of the family it labels, and the aliveness test now covers text as well as objects.

## What changes now

- The Dashboard Smart Links block loses its gray labels: white text, aligned under the numbers, same family.
- The aliveness test extends to labels: a label that doesn't feel active and alive is a defect, not a style choice.
- The Dashboard fix-9 / Smart Links work carries this order; the proof is his eye on the block, labels white and aligned.
- Next loop run re-checks: the Smart Links block shows white labels under the numbers, part of the same family.

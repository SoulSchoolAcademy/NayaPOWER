# Value Impact · What All Humans Want · The Naya Way
**Filed:** 2026-11-07 (fix7n.py + fix7n2.py). **Source:** Shawn's dictation, Addition 19 (2026-11-07 02:43Z), added as an addendum to the instruction set. Smart Note: "Build on Solid Ground — Relentless Persistence to Ten Stars, the Page That Sells the Page, and the Land That Won't Stay Cheap."
**Where it goes:** the demo section (a way line after the `.demo-sub`); the value section (§10) — a way line before the feed block, an Impact object + a Wants object after the Template Insight; the close (§13) — a wide wants frame as the last child of the `.close-frames` grid.

## The Naya Way (the build method + the hostess identity)
She is more than smart — she is a WISE ONE. She thinks BEFORE she acts, deliberates, and takes the most intelligent route — the obvious best choice. The best possible action. The highest percentage choice. The Triple A choice. The ten-out-of-ten choice. The page embodies it: the demo's three questions ARE her deliberation (she asks, she thinks, then the world appears as the obvious best choice), and the hostess presents as a Wise One, not a smart tool.
- **Demo way line** (`.demo-way`, after the `.demo-sub`): "◆ She asks. She thinks. Then your world appears — the obvious best choice."
- **Value way line** (`.value-way`, before the feed block): "◆ More than smart — wise. She thinks before she acts. The demo proved it: she asked, she thought, your world appeared."
- **NOT in the hero** — the hero is at exact fit and cannot take another line (see the regression below). The page PROVES the wise-one identity by demonstrating, not by claiming it.

## The Impact (his voice — his positioning, NEVER a researched claim)
**Value Impact object** (`.value-impact`, after the Template Insight): "A game changer." / "This will be a game changer — it will impact more people than anyone can imagine, the highest impact of any technology ever in history. In this century, right now, today, in this time, in this age — the one to be remembered. The one with the biggest impact, saving us from ourselves, because it empowers us all the way through." Carried as his positioning, in his words — never presented as a researched claim or a measured fact.

## What All Humans Want (the deepest why — value AND close)
The list carried plainly, not softened, not shortened into a slogan — the list IS the why. Nine items, grouped as dictated: to learn · to earn · to grow · to have a way to pay their bills and pay their rent and eat · an assistant to trust in, that we can believe in, that's truly solid, that helps us and automates everything for us, push-button simple · to be acknowledged, loved, appreciated, valued, respected · to have valuable things · to produce valuable things · to have a Naya that produces value and intelligence for them, creates beautiful things for them, and helps them have success in life.
- **Value (§10):** a `.wants` object after the Impact object — the list (`.wants-list`, gold ◆ bullets) + "This is what she gives you."
- **Close (§13):** a `.close-frame--wide` (grid-column 1/−1; the list in 2 columns on desktop, 1 column on phone) — the list + "This is why you're here." The final reason.

## Max Power Mode (the working mode)
Perpetual persistence, performing, productive, profound, potent power — activated to the max level. THINK FIRST, then act. Always. Deliberate, then act, the obvious best choice at every step. Max power is not speed without thought — it is full power WITH thought first. Recorded in the build report; it governed this pass.

## The hero regression (found by the self-check, fixed the same pass — fix7n2)
fix7n's anchor for the demo-way line matched the HERO's `.demo-starter` (line 1283 sits inside `.banner-top` — the demo section starts at line 1319). The way line landed in the hero and pushed its CTA below the fold (hero 1,118/1,079 at 1920, 905/843 at 390; run5 `heroCtaVisible: false` at 390). fix7n2 moved the line out of the hero and into the demo section (after the `.demo-sub`) — net 0 bytes. After the move (run6): hero 1,079/1,079 at 1920 (CTA bottom 1,063), 843/843 at 390 (CTA bottom 794, `heroCtaVisible: true`). Lesson: anchor on the section, not on a class name shared by two sections.

## Verification
Screenshots viewed by eye: `r7f3-1920-demoway2.png` (the way line under the demo-sub, the hero above it clean), `r7f3-1920-value4.png` (Impact + wants objects, clean), `r7f3-390-value4.png` (wants object, clean), `r7f3-1920-closewants.png` (wide wants frame, 2-column split, clean), `r7f3-390-closewants.png` (wide wants frame, single column, clean). 0 errors at 1920 + 390.

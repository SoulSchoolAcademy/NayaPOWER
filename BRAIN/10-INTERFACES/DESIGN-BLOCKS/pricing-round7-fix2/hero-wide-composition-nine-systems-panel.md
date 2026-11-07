# Hero — Wide Composition · Nine-Systems Panel (F16 + F18)
**Filed:** 2026-11-07 (fix2, fixb + fixc). **Source:** the blind re-proof of fix1, §6 (Addition 20 §6 — the withdrawn-9 pattern: an 880px column floating in black at 1920) + Addition 16 step 1 (the welcome greeting, F18). The nine system names are harvested from the Academy page (the nine orbs, same names — SN-2076's nine systems); the panel is a NEW composition of existing content (gold-bordered chips), not a new component.
**Where it goes:** the hero (`.banner-head`), as the last child — an `<aside class="hero-systems">` ("NINE SYSTEMS, ALREADY INSIDE", nine chips: Personality, Brain, Notes, Lead Mode, Law, Scorecarding, Language, Design, Coder) + the note "The same nine that run the demo below — already inside, already working."

## The composition (wide)
At `min-width:1440px` the band is a flex row: copy left (flex 1), panel right (400px, `flex:0 0 400px`), `max-width:1760px`. At 1920 the band spans 80–1840px; the copy's sub/mission have `max-width:none` at wide widths so the column anchors the viewport instead of floating in black. Below 1440px the panel hides (`display:none` at ≤1439px) and the hero is unchanged from fix1.

## The greeting (F18)
`<p class="hero-greet"><span class="way-gem">◆</span> Hello, I'm Naya.</p>` after the H1 — white text, gold ◆ marker (L5: gold on the marker, never in the words). CORRECTION ON THE RECORD: the fix1 build report's claim that the greeting is "carried VERBATIM in the sub" is FALSE — the sub carries the mothership/supercharger lines, not "Welcome to Naya. The future is now." Grep of fix1: "Hello, I'm Naya" 0×, "Welcome to Naya" 0×.

## The grid bug (found and fixed the same pass — fixb)
A CSS grid `grid-row:1/-1` on the aside resolved before the band's implicit rows existed, spilling the copy children (sub, CTA) into column 2 and making the band 871px tall. Replaced with a flex row + a `.hero-copy` wrapper div around the 9 copy children. Lesson: never `1/-1` against implicit rows; wrap the flow first.

## Verification
Self-check `r7f2x-selfcheck.py` (run 2): hero 1,079/1,079 at 1920 (band 640–1021, panel 660–1017, greeting 742–766, CTA 961–1017), 843/843 at 390 (greeting 222–245, panel hidden, CTA bottom 838 — 5px slack). Screenshots viewed by eye: `r7f2x-1920-hero.png`, `r7f2x-390-hero.png`. 0 errors at all 8 widths.

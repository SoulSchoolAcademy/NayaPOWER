# Deck Slide — The Page Is a Deck
**Filed:** 2026-11-07 (pricing round 7 fix1, Addition 9 / Part 8). **Status:** filed object, the page's presentation system (13 slides).
**Source:** NEW in this pass (the Viewport Rule). Each major section is a full-viewport slide (min-height 100vh; 100svh on phone). Scroll snapping locks each section into view; no straddling, no cut content, nothing hidden under the sticky bar (the bar is in-flow, `position:static`, so it can never cover a locked slide). Long sections (chart, Top 10) scroll INSIDE their slide, then the page snaps on. Reduced motion turns snapping off (the deck unrolls to a normal document); keyboard moves slide to slide; the snap never traps the user or fights the wheel.
**The arrival settle (fix7f + fix7j):** the settle was softened to 350ms (opacity .85, 8px rise, 0.2% scale) and then the translateY was REMOVED — the deck probe measured +9px snap offsets, and the root cause was the settle's translateY(8px) shifting the snap while the slide was mid-transition (offsetTop was exact; the transform was the +9). Now the arrival is opacity + scale(.998) only (the slide grows toward the viewer). Deck probe after fix7j: all 13 stops within 1px of exact multiples of 1,080 (1920) / 844 (390) — the 1px is the scale .998 residual. Document height at 1920 is exactly 14,040px (13 × 1,080).
```css
.slide{height:100vh; height:100svh; overflow-y:auto; scroll-snap-align:start; scroll-snap-stop:always; box-shadow:inset 0 1px 0 rgba(255,255,255,.07);}
.js-deck .slide{opacity:.85; transform:scale(.998); transition:opacity .35s ease, transform .35s ease;}
.js-deck .slide.arrived{opacity:1; transform:none;}
```

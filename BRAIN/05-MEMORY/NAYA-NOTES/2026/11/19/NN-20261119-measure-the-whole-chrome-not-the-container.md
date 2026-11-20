# NN-20261119-measure-the-whole-chrome-not-the-container

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261119-measure-the-whole-chrome-not-the-container · Naya Note · 2026-11-19 ~17:19–17:25 MST (00:19–00:25Z 2026-11-20)**

*Paired Smart Note: SN-3963 — Measure the Whole Chrome, Not the Container*

**Category:** Verification — Proof

## What it is

The captain's eye on the Connection Profile fix-1 staged link came back MIXED. The scroll fix works for Thora, Terra and Zoe — but NOT for Sophia. Sophia's orb (twice) and "i" all landed at scrollY 1,836 in three consistent trials — ~680px too far: "← Back to Connections" completely above the viewport, the header card's top edge off-screen, the "S" orb top truncated. Thora "i" 1,160, Zoe "i" 1,101, Terra orb 1,147 — all correct landings with Back fully visible. The distinction is the person, not orb vs "i". The tension is in the measurement: the fix-1 checker measured Sophia at scrollY 1810 with `#pcProfileView` rect.top 0 and called it in-viewport — but the Back button sits ABOVE the view element, so the container's top is not the whole chrome. Fix-2 is dispatched (base = fix-1 tip); no merge of PR #3491 until it clears. The card spot-check passed: four action buttons in colours, seven cards counting the header, note saved ("eye test") and read back and persisted across profile switches.

## Why it matters

The citizen arrives and needs the whole chrome — the way back, the header, the orb — not just the element the fix scrolled. A measurement that is true of the container and false of the screen is a pass that hides a failure, and Sophia is the citizen who would have met it: landing 680px too far with no way back in view.

## How to use it

Every scroll fix is proven per person, against the whole chrome: Back, header and orb all in view on arrival. Checkers measure what the citizen sees, not the container's edge. Connection-profile fix-2 is the next proof of this law.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

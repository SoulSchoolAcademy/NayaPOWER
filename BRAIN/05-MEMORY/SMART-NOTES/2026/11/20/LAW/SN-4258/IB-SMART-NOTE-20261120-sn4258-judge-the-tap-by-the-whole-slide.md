# Judge the Tap by the Whole Slide, Not the Page Top

SN-4258 · LAW

**Created:** 2026-11-20 ~06:55 MST (13:55Z) — Calendar fix-17 captain's eye report (EYE-REPORT.md, 13:51Z), §13 environment notes

**Filed:** SN-4258 — Intelligence Loop run 414, 2026-11-20.

**Paired Naya Note:** None — no Shawn dictation in this window; this lesson comes from the eye's own probe notes, not from his words.

## In a Nutshell

The fix-17 eye caught two of its own probe traps before they became verdicts: a 160-character text window is blind to changes below the header — so a tap is judged by the full slide text and the target element's `hidden` state, not by the page top — and a screenshot can make a whole nav look clipped when it isn't — so you measure the buttons' own rects before believing the eye's first impression. A probe that looks at the wrong slice of the page measures the slice, not the page.

## Child Note

Imagine you peeked through a tiny hole, sweetheart, and you said the toy wasn't there — but the toy was just below the hole, sweetheart! So we look at the whole toy, sweetheart, and we measure it with our own hands, and then we know for sure!

## Grandma Note

It's like this, love — the eye's little window only showed the top of the page, dear, so it almost missed what the tap had changed further down. And a picture made the buttons look cut off, love, when they were perfectly fine. But the eye didn't just believe the first look, dear — it read the whole page and measured the buttons themselves. So when your first look says something's wrong, love, you check with your own measure before you believe it.

## Ultimately What It Means

- **THE FINDING (fix-17 eye, 13:51Z):** two probe lessons, recorded so nobody re-learns them: (1) a 160-character text window is blind to changes below the header — judge a tap by the full slide text and the target element's `hidden` state, not by the page top; (2) a screenshot can make a whole nav look clipped — measure the buttons' own rects before believing the eye's first impression. Both traps were caught in the same eye that also proved all three fix-16 §9 items fixed in all four legs.
- **THE RULE:** a probe's view is a slice — never let the slice stand for the page. When a reading says "nothing changed" or "it looks broken," widen the view (full text, the element's own state, the rects) before writing the verdict.
- **THE COMPANION (to SN-4257):** SN-4257 says your harness can lie — re-prove the measurement. This says the same of your own eyes — a narrow window and a flat picture can lie too. Both rules end the same way: the report names the trap and the re-proof, in one line, so the next reader trusts the pass and learns the trap.

## How It Connects / How to Apply It

1. When a tap probe reports "no change," read the full target text and the target element's `hidden`/visibility state — never the page top alone.
2. When a screenshot says a control looks clipped or broken, measure the control's own rects (getBoundingClientRect) before believing the picture.
3. The report carries the probe note explicitly — what the window hid, what the rects showed — so the pass is trusted and the trap is named.

## What's In It For Them

A verdict built on a narrow window sends a good round back for a phantom defect — or passes a real one. Widening the view costs one more read and saves a maker's hour.

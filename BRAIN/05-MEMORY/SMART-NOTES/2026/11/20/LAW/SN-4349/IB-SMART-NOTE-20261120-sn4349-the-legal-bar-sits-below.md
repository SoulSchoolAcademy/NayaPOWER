# SN-4349 — The Legal Bar Sits Below, Quiet, Never Sticky

**Category:** LAW — the legal bar lives just below the frame in the page flow; 2026-11-20 ~16:17–16:18 MST

*Paired Naya Note: NN-20261120-the-legal-bar-sits-below — the verbatim record of his correction.*

**Filed:** SN-4349 — Intelligence Loop run 433, 2026-11-20. His correction on the cd1ea809 call, recorded in MEMORY.md. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

The legal bar sits just below the frame, in the page flow. Scroll down, see it, click any link if you want — that's it. It must not overtake the page, must not be sticky, and does not have to show in the top fold. Below is fine.

## The Lesson

The bar was already right once — "you had that nice spot for the legal pages bar below when you just scroll down. It was there. On one of them nicely" — and then it vanished from the screen while still existing in the code. Verified in the live v27 bytes: `.legalbar` is there, slim strip, all ten links present, but it does not show when scrolling down — the frame likely never scrolls to it. The fix is visibility, not content: the links are all there, the bar is not. And the placement rules are his, exact: below the frame in the flow; small, slim, quiet, never overtaking the page; never fixed to the viewport; above the fold only if it fits naturally, never forced. With his caution riding on it: "But don't miss anything up" — don't mess anything else up while fixing it.

## Why It Matters

A legal bar that exists in code and not on screen is the same as no legal bar — the citizen scrolling down finds nothing to click. And a bar that overtakes the page or sticks to the viewport stops being a quiet row of links and starts being the page.

## How to Use It

On the agreement: the bar stays exactly as built — same ten links, same slim strip — moved only so it is reachable by scrolling, just below the frame, in the flow, never sticky. Prove it by scrolling the served page, not by reading the source: if the scroll does not reach it, the fix is not done.

## His Order, As Recorded

> "the legal, you had that nice spot for the legal pages bar below when you just scroll down. It was there. On one of them nicely, but. You don't have it there."

> "They scroll down they see the bar, they can click any of them if they want that's it. Don't have it overtake it. Don't have it be sticky. It doesn't even have to show in the top fold. If they scroll down it's there and they can it just just below is fine right? Like or there's enough room to stick it there and be above the fold I think."

> "But don't miss anything up"

## Owed from This Dictation

- The agreement fix build: legal bar reachable by scrolling below the frame, all ten links working, not sticky.

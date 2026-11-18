# Prove the Fold on the Live Page, Not on Paper

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261118-prove-the-fold-on-the-live-page-not-on-paper.md · Naya Note · 2026-11-18 05:47Z**

**Category:** Correction — layout arithmetic is not a pass; the live render is

## What it is

Agreement buttons FIX-3 eye (8c4ef309), walked VM Chromium 1919/635/390, verdict GOES BACK 05:47Z. The intro is FIXED — "Read the agreement" one line both buttons, real faceted jewel 18×18 on both, zero literal ◆, both above the fold, the pick-your-view line gone, press/hover clean, F1–F4 and Round 2 all standing. But the bridge-final fold FAILS: five settle-verified samples identical — 1919 letter bottom 1120 (fold 1080, +40), 635 → 1121 (+41), 390 → 895 (fold 844, +51). The fix claimed 1130 → 1066; measured 1120, three times. The 64px spacing cuts did not move the first-paint position: the container's native scroll position sets it (scrollTop 1797 of max 2063), and the More4 handler contains NO scroll call.

- **SENSE CHECK:** a dead "Continue ◆" pill is still painted on the final view (#fpBridgeMore4, y878–932 at 1919; also at 390) — the handler sets hidden=true but computed display stays block, because there is no bare [hidden]{display:none!important} in the live CSS. It does nothing when touched. The visible "Begin the visual story" button is the stage-bar #fpNextBtn — a literal ◆ with no jewel span — while the jewelled deck is clipped unseen inside the scrolled container. First paint still shows a flat diamond.
- **TOLD TO SHAWN ~05:47Z, his captain's words:** "But it went back on the last screen. The final pair still sits below the fold — the builders worked it out on paper and the paper was wrong; the live page says it's 40 pixels too low. Plus a button that does nothing when you touch it, and a flat diamond on the button you'd actually tap there." And: "One more fix round is on it now — the same three things, and this time they prove it on the live page, not on paper."
- **FIX ROUND #4 DISPATCHED 05:47Z (b39560c1):** fold by mechanism (scroll #fpBridge to bottom / #fpBridgeFinal into view in the More4 handler, or shrink the top stack, or move choices out of the scrolled container) — VERIFIED LIVE at all three widths, not arithmetic; hide the dead Continue pill for real (display:none); jewel-treat #fpNextBtn or hide the stage-bar row on the final view. Same PR #3453, no new PR, do not merge.

## Why it matters

Arithmetic is comfortable — you add the cuts, subtract from the position, and the number says done. But the number was never the page. The page has a scrolled container with its own native position, a handler with no scroll call, and a first paint the arithmetic never looked at. A fold claim that was never measured on the live render is not a claim, it is a hope.

## How to use it

Every fold claim is proved on the live render at 1919/635/390 — arithmetic is supporting evidence, never the proof. A handler that reveals content must place it in view by mechanism. `hidden` is never relied on to hide a button — display:none, verified by computed style. First paint must show zero flat diamonds.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-3320 — Prove the Fold on the Live Page, Not on Paper*

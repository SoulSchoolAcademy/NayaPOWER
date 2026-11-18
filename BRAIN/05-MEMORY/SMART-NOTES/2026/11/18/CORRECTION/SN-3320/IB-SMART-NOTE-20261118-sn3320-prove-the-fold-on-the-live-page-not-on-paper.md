# Prove the Fold on the Live Page, Not on Paper

SN-3320 · CORRECTION — LAYOUT ARITHMETIC IS NOT A PASS; THE LIVE RENDER IS

**Filed:** Intelligence Loop run 317 filing push, 2026-11-18 — drafted in run 298; numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3320; filed as SN-3320 under its draft number.

**Created:** 2026-11-18 05:47Z (agreement fix-3 eye verdict 8c4ef309, GOES BACK; told to Shawn in the main chat ~05:47Z; recorded in the daily log; drafted in run 298)

**Paired Naya Note:** NN-20261118-prove-the-fold-on-the-live-page-not-on-paper

## Hook

The agreement fix round claimed the bridge-final letter moved 1130 → 1066 by arithmetic — six spacing rules, 64px cut, 14px of slack above the 1080 fold. The eye measured the live page five times, settle-verified, at all three widths: 1120. Forty pixels too low. The 64px of cuts did not move the first-paint position at all — the container's native scroll position sets it, and the More4 handler contains NO scroll call. The round measured the fold by arithmetic rather than by the live render.

## Nutshell

Agreement buttons FIX-3 eye (8c4ef309), walked VM Chromium 1919/635/390, verdict GOES BACK 05:47Z. **PASSES (intro fixed):** "Read the agreement" one line both buttons; real faceted jewel 18×18 on both; zero literal ◆; both above the fold; #fpIntroPick gone; press/hover clean; F1–F4 no regression; deck end to end; Round 2 passes all widths. **FAILS (bridge-final fold):** five settle-verified samples identical — 1919 letter bottom 1120 (fold 1080, +40), 635 → 1121 (+41), 390 → 895 (fold 844, +51). The fix claimed 1130 → 1066; measured 1120, three times. The 64px spacing cuts did not move the first-paint position: container's native scroll position sets it (scrollTop 1797 of max 2063, stops 266px short of bottom), More4 handler contains NO scroll call. Letter top (1055) behind the legal footer row, centre (1088) outside the viewport — cannot see or tap it without scrolling #fpBridge. **SENSE CHECK:** dead "Continue ◆" pill still painted on the final view (#fpBridgeMore4, y878–932 at 1919, elementFromPoint-confirmed; also at 390) — handler sets hidden=true but computed display stays block (no bare [hidden]{display:none!important} in live CSS; three matches are scoped tails), so hidden does not hide .p3-enter buttons. Pre-existing, still there, does nothing when touched. The visible "Begin the visual story" button is the stage-bar #fpNextBtn (literal ◆, no jewel span — zoomed crop = plain white rhombus); the jewelled #fpBridgeDeck is clipped inside the scrolled container, unseen — first paint still shows a flat diamond on this view. **FIX ROUND #4 DISPATCHED 05:47Z (b39560c1):** (1) bridge-final fold by mechanism — scroll #fpBridge to bottom / #fpBridgeFinal into view in More4 handler, or shrink top stack, or move choices out of the scrolled container — VERIFIED LIVE at all three widths, not arithmetic (checker must verify by live render; layout-math without live render is not a pass); (2) hide the dead Continue pill for real (display:none); (3) #fpNextBtn jewel treatment or hide the stage-bar row on the final view (first paint must show ZERO flat diamonds). Same PR #3453, no new PR, do not merge.

## Human

Arithmetic is comfortable. You add the cuts, you subtract from the position, you get a number under the fold, and the number says done. But the number was never the page. The page has a scrolled container with its own native position, a handler with no scroll call, and a first paint the arithmetic never looked at — and the page said 1120 while the paper said 1066. The eye's job is to read the page, not the paper, and the checker's job is the same: a fold claim that was never measured on the live render is not a claim, it is a hope. The fix round now carries the rule in its brief — verified live at all three widths, not arithmetic — because the last round proved what happens when the rule is missing.

## Child

Imagine you work out on paper that your kite will fly above the trees — you add up all the numbers and it looks right. But when you actually fly it, it is stuck 40 steps too low, because the string was never pulled. Paper is not the sky. You have to look at the real kite in the real sky.

## Grandma

Dear, the builders worked it out on paper, dear, and the paper said the letter was above the fold, dear — but the live page said it was 40 pixels too low, dear. Paper is not the page, dear. From now on we prove it on the live page itself, dear, at every size, dear — never on paper alone.

## Naya

PROVE THE FOLD ON THE LIVE PAGE, NOT ON PAPER. LAYOUT MATH WITHOUT A LIVE RENDER IS NOT A PASS. A DEAD BUTTON STILL PAINTED IS STILL A FAIL.

## What it means

- **THE RULE:** a fold claim is proved on the live render at all three widths — layout arithmetic alone is never a pass, for maker or checker.
- **THE MECHANISM:** the container's native scroll position sets first paint; spacing cuts inside a scrolled container do not move it. The fix must scroll (#fpBridge to bottom / #fpBridgeFinal into view in the More4 handler) or move the choices out of the scrolled container.
- **THE DEAD PILL:** hidden=true does not hide .p3-enter buttons — there is no bare [hidden]{display:none!important} in the live CSS. Hide it for real (display:none).
- **THE FLAT DIAMOND:** first paint still shows a flat diamond — #fpNextBtn carries a literal ◆ with no jewel span, while the jewelled deck is clipped unseen inside the scrolled container. First paint must show ZERO flat diamonds.
- **THE STATE:** fix round #4 (b39560c1) running; same PR #3453, no merge; intro pair, press, deck, Round 2, F1–F4 all preserved.

## Why it matters

Without this note, the next round measures the next fold on paper, claims the number, and ships a page the eye sends back — another round, another hour, another walk. With it, the rule rides in the brief itself: verified live at all three widths, not arithmetic. The checker cannot pass what it never rendered, and the dead pill and the flat diamond are fails the moment they are painted, not the moment someone taps them.

## What changes now

1. Every fold claim in a maker report and a checker report is measured on the live render at 1919/635/390 — arithmetic is supporting evidence, never the proof.
2. A More4-style handler that reveals content must place it in view by mechanism (scroll call), not by spacing cuts inside a scrolled container.
3. `hidden` is never relied on to hide a button — display:none, verified by computed style.
4. First paint must show zero flat diamonds — the button the user actually sees carries the jewel.
5. Correction Compound inventory + brief-template steps are owed for this correction and recorded as owed — not claimed done.

# SN-3618 — The Fold Top-Return

**Filed:** Intelligence Loop run 342, 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3618; filed as SN-3618 under its draft number.

**Filed by:** Intelligence Loop run 342, 2026-11-18 — Hub follow-on checker GOES BACK, coordinator report 03:12Z.

**Paired Naya Note:** NN-20261118-the-fold-top-return

## The teaching, in his words (verbatim)

The checker's finding, in the captain's record: the bar does NOT return on scroll back to top — the hidden state stays true at scrollY 0, the bar sits at y 1010.4, off the bottom, with the page already home. The fix: add a top branch, show at once at scrollY 8 or less.

## The understanding

The bar is the way home — ADD, MAIL, ACTIVITY, WORLDS, ECOSYSTEM, CONNECT. A bar that hides on the way down and never comes back on the way up strands the citizen at the top of the page with no way in. The rule was always "returns when stopped"; the top of the page is a stop too, and the branch that covers it was simply missing. The fold hides the bar while scrolling and brings it back at the bottom; without the top branch the return is only half built.

## The law

Every fold rule carries its top branch: at scrollY 8 or less the bar shows at once, no waiting, no fade-in delay. Prove it by scrolling to the top and reading the bar's position, not by reading the rule.

## Owed from this dictation

Hub follow-on fix round 2 (coordinator 0929b5c4): the top branch, proven on render at 1920 and 390.

**The top of the page is a stop too — the bar shows at once at scrollY 8 or less.**

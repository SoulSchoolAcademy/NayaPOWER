# NN-20261118-the-fold-top-return

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261118-the-fold-top-return · Naya Note · 2026-11-18 ~03:12Z**

*Paired Smart Note: SN-3618 — The Fold Top-Return*

**Category:** Design — Bottom Bar

## What it is

The Hub follow-on checker went back on the fold: the bottom bar does NOT return on scroll back to top. The hidden state stays true at scrollY 0 — the bar sits at y 1010.4, off the bottom, with the page already home. The fix: add a top branch that shows the bar at once at scrollY 8 or less. The fold hides the bar while scrolling and brings it back at the bottom; without the top branch, a citizen who scrolls home has no bar at all.

## Why it matters

The bar is the way home — ADD, MAIL, ACTIVITY, WORLDS, ECOSYSTEM, CONNECT. A bar that hides on the way down and never comes back on the way up strands the citizen at the top of the page with no way in. The rule was always "returns when stopped"; the top of the page is a stop too, and the branch that covers it was simply missing.

## How to use it

Every fold rule carries its top branch: at scrollY 8 or less the bar shows at once, no waiting, no fade-in delay. Prove it by scrolling to the top and reading the bar's position, not by reading the rule.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

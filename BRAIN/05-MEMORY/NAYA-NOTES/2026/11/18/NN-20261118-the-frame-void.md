# NN-20261118-the-frame-void

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261118-the-frame-void · Naya Note · 2026-11-18 ~03:12Z**

*Paired Smart Note: SN-3619 — The Frame Void — A Data URI in a Custom Property Never Paints*

**Category:** Design — Frame

## What it is

The Hub follow-on checker went back on the frame: the frame image NEVER paints. The 2.2 MB data URI sits in a custom property, `--frame-img`, and the property computes to an empty string — background-image none — in the base and in the kept filing alike. The eye's ~200px void is an unpainted band, not a height problem. The crop also slices the centre pendant (re-measured bright to row ~237, not ~209). The fix: put the background-image with the data URI directly on the bands and sides, restore the bands to 1672/300, and do not cut the pendant. And the KEEP/REPLACE ruling that rides with it: fix forward from the KEPT filing — do NOT swap to the alternate, which fails "starts folded" and has no corner control.

## Why it matters

A frame that never paints is not a small defect — the whole kingdom frame is the look of the system, and a 200px void at the top of the Hub is the first thing his eye meets. The cause is exact and mechanical: a data URI inside a custom property does not survive as a background-image. And the ruling matters as much as the fix: the kept filing is the base, the alternate is out, so the fix round builds on the right file and does not reopen a settled choice.

## How to use it

Never carry a data-URI image through a custom property into a background-image — put the image directly on the element. When an eye finds a void, check whether the image paints at all before measuring heights. And when a keep/replace ruling is made, the fix round builds forward from the kept filing only.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

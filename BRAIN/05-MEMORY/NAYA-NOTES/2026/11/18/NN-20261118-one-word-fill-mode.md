# NN-20261118-one-word-fill-mode

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261118-one-word-fill-mode · Naya Note · 2026-11-18 ~03:5xZ**

*Paired Smart Note: SN-3629 — One Word — Fill Mode 'both' Holds the Bar Up Forever*

**Category:** Design — The Bottom Bar

## What it is

The Personal phase-2 fix round 2 checker verdict: GOES BACK on one defect — item 5(f): the bottom bar never hides in render at landing, mid-scroll, or bottom, at 1920 and 390, even though `body.os-bottom-hidden` is present and the hide rule matches. Root cause proven: `.notif-bar { animation: notifUp .55s … both; }` — fill mode `both` holds the final keyframe forever and overrides the non-`!important` hide rule; the harvested Dashboard and Hub sources use `backwards`, Personal is the odd one out (pre-existing in round 1). The fix is one word: `both` → `backwards` (or `!important` on the hide rule). Everything else passed. Fix round 3 (one word, same branch from tip `e7dac868`, re-check item 5(f) only in render at 1920/390) was recommended, not yet dispatched at the time of filing.

## Why it matters

A one-word difference between the harvested source and the copy is the whole defect — the bar that never hides breaks the official behaviour (pop up once when stopped at the bottom, never sticky) on the page Shawn is about to see. The lesson is mechanical: an animation's fill mode outranks a hide rule, so a copy that changes one word changes the behaviour. Harvest means byte for byte — including the fill mode.

## How to use it

When a harvested rule carries an animation, copy the fill mode with it — `backwards`, never `both`, where the element must hide. When a hide rule fails in render while the class is present and the rule matches, check the animation's fill mode first: `both` holds the final keyframe forever and will beat a non-`!important` hide. Fix round 3 is one word on the same branch, re-checked in render at 1920 and 390.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

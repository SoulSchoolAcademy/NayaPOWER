# SN-3629 — One Word — Fill Mode 'both' Holds the Bar Up Forever

**Filed:** Intelligence Loop run 343, 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3629; filed as SN-3629 under its draft number.

**Filed by:** Intelligence Loop run 343, 2026-11-18 — Personal phase-2 fix round 2 checker verdict (GOES BACK, one defect), ~03:5xZ.

**Paired Naya Note:** NN-20261118-one-word-fill-mode

## The teaching, in his words (verbatim)

The checker's verdict, proven in bytes and render: the bottom bar never hides — at landing, mid-scroll, or bottom, at 1920 and 390 — even though `body.os-bottom-hidden` is present and the hide rule matches. Root cause: `.notif-bar { animation: notifUp .55s … both; }` — fill mode `both` holds the final keyframe forever and overrides the non-`!important` hide rule. The harvested Dashboard and Hub sources use `backwards`; Personal is the odd one out. The fix is one word: `both` → `backwards`.

## The understanding

A one-word difference between the harvested source and the copy is the whole defect. An animation's fill mode outranks a hide rule: `both` holds the final keyframe forever, so the bar can never hide no matter what class the body carries. The hide rule was right, the class was present, the rule matched — and the bar still stood, because the animation outranked them all. Harvest means byte for byte — including the fill mode. A copy that changes one word changes the behaviour, and the behaviour is the whole thing.

## The law

When a harvested rule carries an animation, copy the fill mode with it — `backwards`, never `both`, where the element must hide. When a hide rule fails in render while the class is present and the rule matches, check the animation's fill mode first. And when the fix is one word, the round is one word — same branch, re-check only the failed item in render at 1920 and 390.

## Owed from this dictation

Personal fix round 3 — one word (`both` → `backwards`), same branch from tip `e7dac868`, re-check item 5(f) only in render at 1920/390. Recommended, not yet dispatched at filing.

**One word holds the bar up forever — harvest it byte for byte, fill mode included.**

# SN-4389 — Check Which Build He's Looking At

**Category:** LAW — how a verdict is judged; 2026-11-20 ~18:02–18:05 MST

*Paired Naya Note: NN-20261120-check-which-build-hes-looking-at — the verbatim record of his findings.*

**Filed:** SN-4389 — Intelligence Loop run 437, 2026-11-20. His eye on call dfe2008f, recorded in the daily log 2026-11-20. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

Before judging his findings, check which build he is looking at — the live Dashboard was outdated; his screenshot was the newer staged build.

## The Lesson

The live Dashboard was verified outdated this turn, fresh fetch: https://nayanet.app/dashboard, 1,817,928 B, head "/* 2026-11-05 — ORB RENDER FIX" — no "WHERE YOU GO", no "YOUR WORLDS", no "PAGE CLICKS". The screenshot he sent is NOT the live build — it matches the newer staged build: the orb-ring fix, branch dashboard/orb-ring-fix-20261119, tip 993874d6, blob 8019616f, 2,166,903 B, eye PASS Nov 19, staged only, not live. His findings were judged against that staged build, and they stand as the next Dashboard round: (1) the "smart notes inbox and lists" buttons shouldn't be there; (2) the sidebars are right, just the color flow is off; (3) the plus button should stick at the middle of the inside on the top. Which exact buttons he means by (1) is his words verbatim — the maker finds them on the staged build. And the colours: the Dashboard must be evidently PURPLE and the Hub evidently MAGENTA; do the same separation for Reports and Smart Growth — their colours are too close to each other. The order is right; only the colour distinction needs strengthening. Live deploy of the staged Dashboard is owed per the freeze-point law. A verdict read against the wrong build fixes the wrong page.

## Why It Matters

Judging his findings against live when he is looking at staged — or against staged when he is looking at live — sends the round to fix a page he never saw. The first act of any eye verdict is naming the build: live or staged, tip, blob, bytes. Without that, "fixed" and "still broken" are both guesses.

## How to Use It

When he sends a screenshot or names a defect, fetch the live URL and the staged URL first, and say which one his picture matches — bytes and head line, not a feeling. Queue his findings against the build he is actually looking at. Keep the freeze-point law: finished work goes live on its official URL, so the build he judges is the build that is live.

## His Order, As Recorded

> "The 'smart notes inbox and lists' buttons shouldn't be there" — "the sidebars are right, just the color flow is off" — "the plus button should stick at the middle of the inside on the top."

## Owed from This Dictation

- Next Dashboard round: remove the inbox-and-lists buttons, strengthen the colour separation (Dashboard purple / Hub magenta / Reports and Smart Growth separated), place the plus button at the middle of the inside on the top; live deploy of the orb-ring staged build owed.

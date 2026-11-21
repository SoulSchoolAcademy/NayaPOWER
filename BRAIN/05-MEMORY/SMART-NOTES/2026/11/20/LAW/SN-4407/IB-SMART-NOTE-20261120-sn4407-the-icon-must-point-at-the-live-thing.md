# SN-4407 — The Icon Must Point at the Live Thing

**Category:** LAW — an icon that points at a dead address is a dead icon; 2026-11-20 ~18:50 MST

*Paired Naya Note: NN-20261120-the-icon-must-point-at-the-live-thing — the verbatim record of the icon fixes.*

**Filed:** SN-4407 — Intelligence Loop run 438, 2026-11-20. Icon fixes on call dfe2008f, recorded in the daily log 2026-11-20. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

The AI Score icon points at alscore.nayapower.workers.dev, the Academy icon at academy.nayanet.app — an icon that points at a dead address is a dead icon.

## The Lesson

AI Score icon → https://alscore.nayapower.workers.dev (was pointing at dead app.nayanet.technology — nothing answers there). Academy icon → academy.nayanet.app. Double-checked fresh ~18:50 MST: alscore.nayapower.workers.dev = 200, 101,798 B, sha 585efaf7…; app.nayanet.technology = 0 bytes, dead; academy.nayanet.app = 200, 97,562 B, sha 379b174c… (Academy live, exact match). An icon is a promise that the thing behind it is there. A citizen tapping the AI Score icon and getting nothing does not think "the address changed" — they think the feature is broken, or the system is broken, and they stop tapping. The fix is not a new icon; it is the icon pointing at the live thing, proven by a fresh fetch before the fix is called done. The home rule change queues behind these two icon fixes (coordinator abc3e850, running) — the order matters: the icons point right first, then the routing learns membership.

## Why It Matters

Icons are the citizen's map of the network. A dead destination behind a live icon is worse than no icon at all — it teaches the citizen that tapping leads nowhere, and an untrusted map is a map that stops being used. Every icon's destination is checked the same way every deploy is: fresh fetch, bytes and sha, or it is not live.

## How to Use It

When an icon is placed or fixed, fetch its destination fresh and match it against the live thing before calling it done. When a destination dies, move the icon to the live address in the same pass — never leave a live icon pointing at a dead address. Record the dead address too, so nobody points anything at it again.

## His Order, As Recorded

> "AI Score icon → https://alscore.nayapower.workers.dev. Academy icon → academy.nayanet.app."

## Owed from This Dictation

- Icon fixes ride coordinator abc3e850 (running); home rule (member detection) queues behind them.
- app.nayanet.technology answers nothing — nothing may point at it again.

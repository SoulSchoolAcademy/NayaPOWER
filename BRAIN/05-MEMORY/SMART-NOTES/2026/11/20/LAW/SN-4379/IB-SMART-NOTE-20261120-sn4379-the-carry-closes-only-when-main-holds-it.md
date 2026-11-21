# SN-4379 — The Carry Closes Only When Main Holds It

**Category:** LAW — how a fix becomes permanent; 2026-11-20 ~17:43 MST

*Paired Naya Note: NN-20261120-the-carry-closes-only-when-main-holds-it — the record of the merge landing.*

**Filed:** SN-4379 — Intelligence Loop run 436, 2026-11-20. The merge landing recorded in the daily log 2026-11-20; it closes the carry item run 434 opened and run 435 left owed. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

A live-only fix is not a fix — it is a fix waiting to be reverted. The carry closes only when main holds the same bytes as live.

## The Lesson

The portal button fix went live first (worker v76 → v77, ~17:16 MST) — but main's union file still held the old handler, so a future merge could have brought the old button back. The carry closed that gap: one line, verbatim, onto branch `portal/agreement-button-carry-main-20261120` (commit `626859ee`, parent main HEAD `e64c2dec`), the seven questions all answered YES in writing, the captain's independent double-check passed, and the merge landed (commit `f5fde7c0`, now main HEAD, 00:44:17Z) — verified by fresh read-back: main ref, parents, tree, file blob `578d3573…`, old handler 0×, new handler 1×, `/agreement` 5×. The button fix is in main for good; no future merge can bring the old button back. The merge followed the Self-Check Law — maker checks three times and answers the seven questions in writing, captain double-checks, maker merges — and no force was used on main's ref even when main advanced three times mid-step and the first attempt failed HTTP 422 "not a fast forward."

## Why It Matters

Without the carry, the next merge of main's union file would have silently restored the old button, and nobody would have known until he tapped it. The smallest carry — one line, ten bytes — is what makes a live fix permanent. Live and main are two versions of the same truth, and they must agree.

## How to Use It

Carry every live fix into main the same way: the smallest verbatim change, diff scope proven line by line (here line 3916 only, −10 B), the seven questions answered in writing, the captain's double-check, the merge verified by fresh read-back after. Never force-update main's ref. Never call the carry done before the merge lands — and never leave a live fix with its carry owed.

## His Order, As Recorded

> The Self-Check Law, his standing order: maker checks three times and answers the seven questions in writing, captain double-checks, maker merges.

## Owed from This Dictation

- Nothing owed on the portal button carry — the merge landed and the item is closed. The standing work: every future live fix carries the same way, the same pass.

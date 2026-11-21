# SN-4425 — Prove the Arithmetic, Find the True Cause

**Category:** LAW — a checker that disproves, not just fails; 2026-11-20 ~19:45 MST

*Paired Naya Note: NN-20261120-prove-the-arithmetic-find-the-true-cause — the record of the Hub light-up checker in the daily log.*

**Filed:** SN-4425 — Intelligence Loop run 440, 2026-11-20. Hub light-up round checker verdict, recorded in the daily log 2026-11-20. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

Prove the arithmetic. Find the true cause. A claim with wrong numbers, or a fix for a cause that isn't the cause, goes back — even when the rest passes.

## The Lesson

Hub light-up round (coordinator `2bb1f7f5`): the code passed — four colours in rest/hover/lit, jewel icons, nothing else touched. The checker still sent it GOES BACK, on two points, and on both points it didn't just say "wrong" — it proved it:

1. The 390px slack arithmetic was wrong. True slack is 0–8px at the boundary, not the maker's claimed ~34px — the badge margin-left of 8px ×2 was missed. And "no collision by construction" on desktop was overstated: minmax permits overflow.
2. The cut zero's true cause was unidentified. The maker's clip mechanism was disproven: the tile is 28px under border-box, not 32px, and the button has no fixed height so overflow:hidden can't clip. The 22px change was harmless but unproven.

The repair (coordinator `a1affcae`, branch `hub/button-lightup-repair-20261120`) carries the honest instruction: correct the arithmetic (fix a real 390 collision if the numbers show one), find the zero's TRUE cause from the file's rules and fix that — or mark the zero eye-only honestly. A number that is wrong is not a rounding error; a cause that is wrong is not a fix. When the cause cannot be found, the honest mark is "eye-only," not a plausible mechanism.

## Why It Matters

Wrong arithmetic ships a collision at 390px — the phone width he judges everything at. A fix for the wrong cause ships a change that does nothing while the cut zero stays cut, and the next person reads the mechanism as true and builds on it. The checker that disproves — with the numbers, from the file's own rules — is what stops both. "Harmless but unproven" is not a pass; it is a repair ticket with the proof attached.

## How to Use It

Every claim in a round carries its arithmetic, shown: the numbers, the rule they come from, the boundary they hold at. A checker redoes the arithmetic from the file, not from the maker's message. A fix names its cause from the file's rules and proves the mechanism — or it says plainly "cause unidentified, eye-only" and goes back as a repair, not forward as done.

## His Order, As Recorded

> No direct dictation — the lesson is from the checker's verdict, recorded in the daily log 2026-11-20: "390px slack arithmetic wrong — true slack is 0–8px at the boundary, not the maker's claimed ~34px" and "Cut zero's true cause unidentified — maker's clip mechanism disproven."

## Owed from This Dictation

- Hub light-up repair round running (coordinator `a1affcae`) — correct the arithmetic, find the zero's true cause, or mark it eye-only honestly. The loop watches for its verdict.

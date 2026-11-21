# SN-4369 — Copy the Sibling Verbatim

**Category:** LAW — fix the odd one out by copying what already works; 2026-11-20 ~17:05 MST

*Paired Naya Note: NN-20261120-copy-the-sibling-verbatim — the verbatim record of his law.*

**Filed:** SN-4369 — Intelligence Loop run 435, 2026-11-20. His law on call f3737da1, recorded in MEMORY.md. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

When one button in a family goes somewhere the others do not, do not redesign the button. Copy the sibling that already goes to the right place, verbatim, and change nothing else.

## The Lesson

The portal's bottom button — the footer's `Read the collective agreement ◆` — opened the walk's in-page agreement stage, the old presentation, and never left the page. He caught it: "when you click that you click that link it doesn't go there right now it goes somewhere else... when they click the collective agreement button at the bottom of that page it actually goes to the collective agreement page. Because right now it goes to the old one, right?" The other three agreement buttons in the same file already went to `/agreement`. The fix was exactly one line — `window.location.href='/agreement';` — copied verbatim from the siblings. Same label, same style, same position. Live within the hour (worker v76 → v77, fresh-fetch verified). The sibling is the pattern; copying it cannot drift from the house, because the sibling IS the house. A seat that invents a new handler for a problem the file already solved is doing extra work to get a worse answer.

## Why It Matters

Every family of controls has a right answer already living in it. The odd one out is the defect, and the siblings are the proof of what right looks like — no design meeting, no new pattern, one line. But a fix that lives in only one copy of the file is half a fix: main's union file is a different version, and a future merge could revert it. The copy has to land in both places, or the next merge undoes the hour.

## How to Use It

Find the sibling that already goes to the right place. Copy its destination verbatim. Change nothing else. Verify from live bytes (fresh fetch + sha), then carry the same line into every other copy of the file — and say so plainly if the carry is still owed.

## His Order, As Recorded

> "when you click that you click that link it doesn't go there right now it goes somewhere else... when they click the collective agreement button at the bottom of that page it actually goes to the collective agreement page. Because right now it goes to the old one, right?"

## Owed from This Dictation

- Carry-into-main: the one-line fix into main's union file (blob `78be56cf…`, 1,172,149 B) — dispatched branch-only (coordinator ce71d0e1), no merge. Until it lands, a merge of main's file over the live path reverts the fix.

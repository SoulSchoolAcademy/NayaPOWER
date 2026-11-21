# SN-4430 — The Frame Can Lie — Check the Body

**Category:** DESIGN — the chrome can render fine while the content is blank; 2026-11-20 ~20:30 MST

*Paired Naya Note: NN-20261120-the-frame-can-lie-check-the-body — the verbatim record of his screenshot and the memory record.*

**Filed:** SN-4430 — Intelligence Loop run 441, 2026-11-20. His screenshot ~20:30 MST (call c071d78d), recorded in the memory record. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

A board can look right and say nothing. Title, frame and nav buttons present, body entirely blank — the frame lied, and only his eye caught it.

## The Lesson

His screenshot, ~20:30 MST (call c071d78d, his local file `Collective Agreement (9).html`): the How You Get Paid board renders empty. Title present. Frame present. Nav buttons present. The body is entirely blank — no text at all on the board. A separate defect from the last board not showing, found in the same look.

The frame is the easiest thing to check and the least informative: it renders from the shell, which is shared and healthy, while the body renders from the board's own content, which is where the failure lives. A check that confirms "the board loaded" by seeing its title and its buttons has proven the shell, not the board. An empty body is the quietest failure there is — nothing errors, nothing clips, nothing looks broken at a glance. It only looks wrong to a reader who expects words and finds none, which is exactly his eye: he reads the board, he does not scan the chrome.

## Why It Matters

Every board in the agreement exists to be read — the whole presentation is words and pictures, and a board with no words is a board with no reason to exist. The How You Get Paid board is also one of the boards that has to carry the mission: it is where a joiner learns what they get. Blank, it says the opposite of everything the agreement says. And it sat there, blank, while rounds reported the deck checked — because the checks confirmed the frame, not the body.

## How to Use It

Check the body, not the frame: every board check reads the board's own text — count the words, read the first line, confirm the content rendered — never only that the title and nav are present. A board with zero words is a failure, not a pass, and it is filed as one. When a screenshot shows a board, read what is inside the frame before judging the frame itself.

## His Order, As Recorded

> (His screenshot, 20:30 MST — no spoken words recorded; the board speaks for itself: title, frame and nav buttons present, body entirely blank.)

## Owed from This Dictation

- How You Get Paid board renders empty — fix owed (handed to the Expert Agent with the last-board fix during call c071d78d).
- Last board still not showing on laptop — see SN-4430 "Told Fixed Is Not Fixed."

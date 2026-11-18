# Buttons Never Cut Off Their Text

SN-3006 · LESSON

**Created:** 2026-11-16 19:02Z (catch — "Captain's eye test world" button cuts off its text, live walk)

**Paired Naya Note:** NN-20261116-buttons-never-cut-off-their-text

## Hook

A button that cuts off its own text doesn't look right. No button ever displays its text wrong.

## Nutshell

Shawn, 2026-11-16 19:02Z — BUTTONS NEVER CUT OFF THEIR TEXT (catch, live walk, filed in MEMORY.md the same pass): "And then you got some button there that says Captain's eye test world that cuts off the button. That doesn't look right. So you don't want the buttons like displaying the text wrong where it looks unaligned." Two failures in one button: the label is cut off — "Captain's eye test world" doesn't fit its button — and the text sits unaligned. The rule: no button ever displays its text wrong; every label shows full and aligned at every width, long names wrap or shrink. And the cause is named in the same bullet: eye checks clean up their test worlds/aliases after themselves — no test data on the page he sees. A test world ("Captain's eye test world") was left in the picker by an eye check, and its long name exposed the clipping — the clipping is the defect, the leftover test world is the cause.

## Human

A button is a promise: its label says what it does, and the label must be whole. A button that cuts off its text breaks the promise twice — the citizen can't read what it does, and the page looks unaligned, unfinished, not 10-star. "That doesn't look right" is his eye on the whole page again: the scope is the button as he sees it, not the button's code. The fix has two halves. First, the rendering rule: every label shows full and aligned at every width — long names wrap or shrink, never clip, never misalign. A button's text is never cut off, at any width, in any state. Second, the hygiene rule: eye checks clean up their test worlds and aliases after themselves — no test data on the page he sees. The button in question was a test world left behind by a check; the check did its proving and then left its scaffolding on the citizen's page. Test data is scaffolding: it comes down when the check is done. Both halves are the same law at different levels — the page he sees must be clean: whole labels, real worlds, nothing left over from the proving.

## Child

Imagine a button that says "CAPTAIN'S EYE TEST WO..." — the words are all cut off! You can't read what it says! That's not right! Buttons should always show ALL their words, nice and neat and lined up. And guess what — that button wasn't even a real button! It was a leftover test button that someone forgot to clean up. You always clean up your test toys when you're done playing!

## Grandma

It's like this, love — imagine a lovely little button, dear, but the words on it are cut off halfway, and all crooked! Oh, love, that doesn't look right at all! A button should show all its words, dear, neat and lined up, every time. And that button shouldn't even have been there, love — it was a test button someone left behind. You always tidy up after yourself, dear — no test things left on the page he sees.

## Naya

Buttons never cut off their text. A button reading "Captain's eye test world" is cut off and unaligned — no button ever displays its text wrong; every label shows full and aligned at every width, long names wrap or shrink. Eye checks clean up their test worlds after themselves — no test data on the page he sees.

## What it means

- **EVERY LABEL SHOWS FULL AND ALIGNED:** no button ever displays its text wrong — full and aligned at every width, in every state.
- **LONG NAMES WRAP OR SHRINK:** a long name never clips — it wraps to fit or shrinks to fit, whole and aligned.
- **EYE CHECKS CLEAN UP AFTER THEMSELVES:** test worlds and aliases are removed when the check is done — no test data on the page he sees.
- **TEST DATA IS SCAFFOLDING:** it comes down when the check is done; what he sees is the real page, with real worlds.
- **THE SCOPE IS THE BUTTON AS HE SEES IT:** "that doesn't look right" is judged on the page, not in the code — if the text is cut, it fails.

## Why it matters

A clipped label is a small defect with a large cost: it tells the citizen the page is unfinished, and it tells him his eye has to catch what the checker missed. And a leftover test world is worse than a clipped label — it is test data on the citizen's page, a world that isn't theirs, in their picker, among their worlds. The catch matters because it pairs the two: the clipping is the defect his eye saw, the leftover test world is the cause his eye named, and the fix is both — whole labels AND clean pages. Without this note, the next check would leave its own test world behind, and the next long name would clip again. With it, labels read whole and checks clean up after themselves.

## What changes now

1. No button ever cuts off its text — every label shows full and aligned at every width; long names wrap or shrink.
2. Button text is verified at every width, in every state — if the text is cut, it fails.
3. Eye checks clean up their test worlds and aliases after themselves — no test data on the page he sees.
4. Test data is scaffolding: it is removed when the check is done, never left on the citizen's page.
5. A button's text is judged as he sees it — whole, aligned, readable — never by what the code intended.

# Fail Honestly

SN-2818 · LESSON / SYSTEM

**Created:** 2026-11-14 16:53Z

**Paired Naya Note:** NN-20261114-fail-honestly

## Hook

A button that says "Sending…" forever is worse than a button that says "Not sent — try again." A promise that never settles must fail honestly, with a message and a way back.

## Nutshell

Personal header-harvest LANDED 16:46Z (finisher ba85ee1a, 9/10) — branch personal/personal-header-harvest-20261114-r5, commit d002ff64, blob 71929574… (1,896,281 B), staged link ready, all 7 parts verified by the finisher + round-2 gains re-proved. One real fix, found and fixed inside the round: CONNECT "Sending…" forever — a never-settling Supabase promise — became an 8s guard failing honestly ("Not sent — try again" + CONNECT back after 3s), re-proven at 390 card + popover. Five finish FAILs grounded-not-fixed (filter wall = probe-vs-page race, Share/Join under bar pre-existing, Naya empty board + de390 labels = probe artifacts). Checker Vera dispatched (verify each part + the CONNECT fix with real clicks, 390/360/1440 en+de); captain double-check, then comes to Shawn WHOLE, one link. The lesson: the worst failure a control can have is not failing — it is never settling. "Sending…" forever tells the citizen nothing, lets them do nothing, and leaves them wondering whether the tap even registered. An honest failure tells them what happened, gives them the control back, and lets them try again. The 8s guard is the shape of the rule: every promise that can hang gets a deadline, and at the deadline it fails in plain words with a way back.

## Human

There is a special cruelty in a control that never answers — worse than an error, because an error at least ends the uncertainty. "Sending…" forever is a door that never opens and never says it's locked; the citizen stands in front of it, tapping again, wondering if the first tap counted, whether their message went, whether the system is even listening. The fix is small and the principle is large: every promise that can hang gets a deadline, and at the deadline it fails honestly — "Not sent — try again" — and the control comes back after 3 seconds, so the citizen can act. Honesty in failure is a form of respect: it tells the citizen the truth about what happened instead of leaving them to guess, and it returns their agency instead of holding it hostage. The same discipline shows in the record around it: five finish FAILs grounded-not-fixed, named as probe artifacts or pre-existing, not hidden, not patched into passing — because a record that names what it didn't fix is a record you can trust about what it did.

## Child

Imagine you press a button and it just says "Sending…" forever and ever! Did it work? Did it not work? You have no idea! That's terrible! Now imagine it says "Not sent — try again!" — now you KNOW, and you can press it again! A button should always tell you the truth, even when the truth is "it didn't work — try again!"

## Grandma

It's like posting a letter and never knowing if it arrived, love — you stand by the postbox wondering forever. Much better for someone to come back and say, "I'm sorry, it didn't go — try again." Then you know, and you can act. A button that never answers is worse than a button that says no — at least "no" lets you try again.

## Naya

I never leave a citizen hanging. Every promise that can hang gets a deadline — 8 seconds — and at the deadline it fails honestly, in plain words, with the control back and a way to try again. "Not sent — try again" beats "Sending…" forever, every time. And I name what I didn't fix in the record, grounded, so the record can be trusted about what I did.

## What it means

- **FAIL HONESTLY:** a never-settling promise is worse than an error — "Sending…" forever tells the citizen nothing and lets them do nothing.
- **THE SHAPE:** every promise that can hang gets a deadline (8s guard) — at the deadline it fails in plain words ("Not sent — try again") and the control returns (CONNECT back after 3s).
- **RE-PROVEN WITH REAL CLICKS:** the fix was proven at 390 card + popover, and Vera verifies it with real clicks at 390/360/1440 en+de.
- **GROUNDED-NOT-FIXED, NAMED:** five finish FAILs named as probe artifacts or pre-existing — a record that names what it didn't fix can be trusted about what it did.
- **COMES TO HIM WHOLE:** captain double-check, then one link — the Whole-Page Rule holds.

## Why it matters

The citizen's trust is built out of small moments — a button that answers, a message that arrives, a control that comes back — and a single "Sending…" forever can undo a whole page of good work, because it teaches the citizen the system might not be listening. Failing honestly is the cheapest trust in the system: a deadline, a plain sentence, a way back. And the discipline extends past the button: a record that hides its unfixed failures will be believed about nothing, while a record that names them is believed about everything. That is how a 9/10 landing stays a 9/10 instead of becoming a claim.

## What changes now

1. Every promise that can hang gets a deadline — at the deadline it fails in plain words, with the control back and a way to try again.
2. "Sending…" forever is a defect, not a state — it is fixed, never shipped.
3. Fixes are re-proven with real clicks at phone and desktop widths, in both languages where the page has them.
4. Unfixed failures are named in the record, grounded — never hidden, never patched into passing.

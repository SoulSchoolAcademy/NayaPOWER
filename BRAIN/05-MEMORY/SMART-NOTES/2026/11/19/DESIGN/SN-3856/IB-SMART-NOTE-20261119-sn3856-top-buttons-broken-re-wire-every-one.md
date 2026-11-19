# SN-3856 — Top Buttons Broken: Re-Wire Every One

**Filed:** Intelligence Loop run 381, 2026-11-19 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3856; drafted and filed in run 381.

**Filed by:** Intelligence Loop run 381, 2026-11-19 — Shawn, ~15:08 MST (22:08Z), live call, his eye on the Personal mirror top bar; byte evidence from the captain's check of the staged mirror file (10,418,275 B).

**Paired Naya Note:** NN-20261119-top-buttons-broken-re-wire-every-one

## The teaching, in his words (in substance, as recorded)

Clicking About / Message (and others on the top bar) — some don't work, they used to work before, now they don't. They all need to work and go to the right pages. Byte evidence: the top buttons are wired through `data-os-go` attributes (about / skills / people / growth / myworld) with only 8 `onclick=` in the whole 10MB file; Share and Message carry NO routing attribute at all; there is no `showAbout`, no `goToHub`, no `openMyWorld` function anywhere in the bytes; the "Go to the Hub" label is set by JS on the join button, not markup. The routing that reads those attributes is what makes them work — on this page it doesn't land. How it happened (best read, maker to confirm): the mirror moved the Hub's feed into Personal and the top buttons' routing didn't survive the move — the buttons are there, their destinations aren't.

## The understanding

A button that doesn't go anywhere is a promise the page breaks in the person's hand — and these used to work, so the person remembers them working. The move that brought the Hub's feed into Personal dropped the routing; the fix is not a new button set but the destinations restored, every one proven by a click.

## The law

Every top button works and goes to its right page — Message, About, My World, Skills, Connections, Invite, Share, Go to the Hub. A button without a destination is a defect; a move that drops routing is a move undone until the routing lands. Prove every button by clicking it.

## Owed from this dictation

Rides the next Personal round with the other walk fixes. The round re-wires every top button and proves each one by clicking it.

**Every button goes somewhere — proven by a click.**

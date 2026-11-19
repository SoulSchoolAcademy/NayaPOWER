# NN-20261119-top-buttons-broken-re-wire-every-one

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261119-top-buttons-broken-re-wire-every-one · Naya Note · 2026-11-19 ~15:08 MST (22:08Z 2026-11-19)**

*Paired Smart Note: SN-3856 — Top Buttons Broken: Re-Wire Every One*

**Category:** Design — Personal

## What it is

On the live call, Shawn's eye: clicking About / Message (and others on the top bar) — some don't work, they used to work before, now they don't. They all need to work and go to the right pages. Byte evidence (captain checked the staged mirror file, 10,418,275 B, 15:08 MST): the top buttons are wired through `data-os-go` attributes (about / skills / people / growth / myworld) with only 8 `onclick=` in the whole 10MB file; Share and Message carry NO routing attribute at all; there is no `showAbout`, no `goToHub`, no `openMyWorld` function anywhere in the bytes; the "Go to the Hub" label is set by JS on the join button, not markup. The routing that reads those attributes is what makes them work — on this page it doesn't land. How it happened (best read, maker to confirm): the mirror moved the Hub's feed into Personal and the top buttons' routing didn't survive the move — the buttons are there, their destinations aren't. The round re-wires every top button (Message / About / My World / Skills / Connections / Invite / Share / Go to the Hub) to its right page and proves each one by clicking it.

## Why it matters

A button that doesn't go anywhere is a promise the page breaks in the person's hand — and these used to work, so the person remembers them working. The move that brought the Hub's feed into Personal dropped the routing; the fix is not a new button set but the destinations restored, every one proven by a click.

## How to use it

Rides the next Personal round with the other walk fixes. The round re-wires every top button to its right page and proves each one by clicking it — Message, About, My World, Skills, Connections, Invite, Share, Go to the Hub.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

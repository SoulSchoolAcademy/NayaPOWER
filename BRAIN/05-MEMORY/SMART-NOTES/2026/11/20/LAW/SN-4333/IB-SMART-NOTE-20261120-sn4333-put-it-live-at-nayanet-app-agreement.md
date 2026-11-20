# SN-4333 — Put It Live at nayanet.app/agreement

**Category:** LAW — the go-live order; the address itself was the bug; 2026-11-20 ~15:19–15:21 MST

*Paired Naya Note: NN-20261120-put-it-live-at-nayanet-app-agreement — the verbatim record of his order.*

**Filed:** SN-4333 — Intelligence Loop run 431, 2026-11-20. His direct order, recorded in MEMORY.md. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

Put the agreement live at nayanet.app/agreement. He spelled it out piece by piece — nayanet.app / app slash / the agreement — after the voice path garbled it as "ninenet". That address is the order, and the address itself is where the bug lives: today it serves Hub bytes, not the agreement.

## The Lesson

The deploy map (`~/workspace/team-nitro/go-live-20261118/MAP-DEPLOY-PATH.md`, 2026-11-18) found the root behind the whole preview-vs-page mismatch: nayanet.app/agreement today serves HUB bytes (4,694,134 B, sha 6163d8e5...), NOT the agreement — the hub worker's custom domain + SPA fallback answers /agreement with the Hub's index.html. Making /agreement serve the agreement needs a route + worker change (the map's recipe: an /agreement branch on the nayanet worker + routing change; or a dedicated zone route to a worker serving the new build). A page can be finished and still not be live if the address points at the wrong page.

## Why It Matters

Only the address he opens counts. The preview looking right is not the page being live — and a finished build sitting on a staging link is not the agreement at nayanet.app/agreement. The order closes that gap: same build, live, at the address he named.

## How to Use It

Fix round first, then deploy: the v24 build goes back (its visible audio block pushes "Let's Go" out of the console on desktop; the inside slide images are still unproven), so do not deploy v23 while its fix is in flight. When the finished build lands, deploy it to nayanet.app/agreement by the map's recipe, then verify by opening the address itself. Team-nitro house rules ride with it: Checklist Law, Whole-Page Rule, Continuous Cycle, Live Sequence — the finished build goes live whole, proven on the page he sees.

## His Order, As Recorded

> "You should just put it on nayanet app agreement. That way it's live."

## Owed from This Dictation

- The fix round: "Let's Go" back in the console + prove every slide's picture renders.
- The deploy to nayanet.app/agreement, verified by opening the address — no clock-time promise was given for "When?".
- The Drive file he sent (the good-version file) has still NOT landed from this side — do not claim it was retrieved or compared.

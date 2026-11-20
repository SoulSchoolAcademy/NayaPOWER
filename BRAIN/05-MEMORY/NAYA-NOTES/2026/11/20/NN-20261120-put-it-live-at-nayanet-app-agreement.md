# NN-20261120-put-it-live-at-nayanet-app-agreement

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261120-put-it-live-at-nayanet-app-agreement · Naya Note · 2026-11-20 ~15:19–15:21 MST**

*Paired Smart Note: SN-pending — Put It Live at nayanet.app/agreement (takes the next free number at filing)*

**Category:** Law — the go-live order; the address itself was the bug

**Status:** Filed in run 431. His direct order, recorded in MEMORY.md.

## What it is

**GO LIVE — HIS DIRECT ORDER (~15:19 MST).** Put the agreement live at nayanet.app/agreement. "You should just put it on nayanet app agreement. That way it's live." He spelled it out piece by piece (nayanet.app / app slash / the agreement) after the voice path garbled it as "ninenet". This direct order governs this page's go-live.

**DEPLOY MAP FOUND (~15:20 MST).** `~/workspace/team-nitro/go-live-20261118/MAP-DEPLOY-PATH.md` (2026-11-18). Decisive fact: nayanet.app/agreement today serves HUB bytes (4,694,134 B, sha 6163d8e5...), NOT the agreement — the hub worker's custom domain + SPA fallback answers /agreement with the Hub's index.html. Making /agreement serve the agreement needs a route + worker change (map's recipe: /agreement branch on the nayanet worker + routing change; or a dedicated zone route to a worker serving the new build).

**V24 COMPLETED BUT GOES BACK (~15:21 MST).** Builder fde6a620 completed 22:21:28Z. Assets proven intact (27 JPEGs decode, welcome.m4a AAC 4:18). BUT the builder's own attestation: (1) inside slide images NOT proven displaying — every capture shows only the cover screen, the slide screen was never opened, slide image listed [hidden]; (2) REGRESSION on desktop: the new visible audio block pushes "Let's Go" out of the console. Public link still serves v23. Sent back for a fix round 15:21Z (Let's Go back in the console + prove every slide's picture renders). The finished build goes live when it lands; do not deploy v23 while its fix is in flight.

## Why it matters

Only the address he opens counts. The preview looking right is not the page being live, and a finished build on a staging link is not the agreement at nayanet.app/agreement.

## How to use it

Fix round first, then deploy by the map's recipe, then verify by opening nayanet.app/agreement itself.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

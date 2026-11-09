# Sync Partial + Hub Workers.dev 404 — The Live Hub Serves

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261109-sync-partial-hub-workers-dev-404 · Naya Note · 2026-11-09 20:14Z**

**Category:** Finding — Live Check / Hub

## What it is

His live check, 20:14Z Nov 9 — recorded from his words as given:

- sn-sync synced SN-2570/2571, heartbeat written, then the service restarted mid-run during the Hub redeploy — deploy outcome unknown.
- "I checked live myself: nayanet.app home 200, feed-live.json 200 with 691 cards, SN-2570 AND SN-2571 present — the live Hub IS serving and both notes ARE live (the worker's 'live Hub not serving' was wrong for the live domain)."
- "What IS down: hub.nayapower.workers.dev returns 404 (error 1042, route disabled) — the staging address only, does not touch nayanet.app. Needs a one-call re-enable (POST …/subdomain {"enabled": true}) on the next Hub deploy pass."

## Why it matters

A worker said the live Hub was not serving. He checked live himself, with his own eyes — and the truth was the opposite on the address that matters. The live Hub IS serving: home 200, feed 200 with 691 cards, both notes live. What is down is only the staging address, and no citizen touches it. His eye is the proof, and a machine's claim does not survive it. The fix is one call, riding on the next Hub deploy pass — not its own emergency.

## How to use it

- Never claim "the Hub is down" from the staging address — the live check is nayanet.app, his eye first.
- The workers.dev re-enable (POST …/subdomain {"enabled": true}) rides on the next Hub deploy pass; that pass closes with a live check that says so.
- The sync partial is timing, not loss: SN-2570/2571 synced and are live.
- A restart mid-redeploy must leave a visible, checkable outcome — "deploy outcome unknown" is the gap to close.

---

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*His live check on the sync partial and the Hub workers.dev 404 — filed as a Naya Note under the official template — three outputs: what it is, why it matters, how to use it. Paired Smart Note: **SN-2575 — Sync Partial + Hub Workers.dev 404 — The Live Hub Serves, the Staging Address Does Not**.*

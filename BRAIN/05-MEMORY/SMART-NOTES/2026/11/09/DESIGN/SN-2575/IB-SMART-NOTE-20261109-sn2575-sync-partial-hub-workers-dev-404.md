# Sync Partial + Hub Workers.dev 404 — The Live Hub Serves, the Staging Address Does Not

SN-2575 · FINDING / LIVE CHECK

**Created:** 2026-11-09 20:32Z

**Source:** Shawn's live check, 20:14Z Nov 9, recorded in MEMORY.md. Paired with NN-20261109-sync-partial-hub-workers-dev-404.md.

## Hook

The sync ran partial and the service restarted mid-redeploy — deploy outcome unknown. He checked live himself: nayanet.app serves, the feed holds 691 cards, SN-2570 and SN-2571 are both live. The live Hub IS serving. What is down is only the staging address — hub.nayapower.workers.dev returns 404, error 1042, route disabled — and it does not touch nayanet.app.

## Nutshell

- **WHAT HAPPENED (20:14Z):** sn-sync synced SN-2570/2571, heartbeat written, then the service restarted mid-run during the Hub redeploy — deploy outcome unknown.
- **HIS LIVE CHECK:** nayanet.app home 200, feed-live.json 200 with 691 cards, SN-2570 AND SN-2571 present — the live Hub IS serving and both notes ARE live.
- **THE WORKER WAS WRONG:** the worker's "live Hub not serving" was wrong for the live domain — the live domain serves; the claim did not survive his eye.
- **WHAT IS DOWN:** hub.nayapower.workers.dev returns 404 (error 1042, route disabled) — the staging address only, does not touch nayanet.app.
- **THE FIX:** a one-call re-enable (POST …/subdomain {"enabled": true}) on the next Hub deploy pass.
- **NO MERGE — SHAWN'S HAND.**

## Human

A sync ran, a service restarted in the middle of a redeploy, and for a moment nobody knew whether the Hub had landed. A worker said the live Hub was not serving. He did what he always does: he checked live himself, with his own eyes. The home page answered 200. The feed answered 200 with 691 cards. SN-2570 and SN-2571 were both there, live. The live Hub IS serving — the worker's claim was wrong for the live domain, and his eye is what proved it. What is actually down is the staging address, hub.nayapower.workers.dev, answering 404 with error 1042 — the route is disabled. That address is staging only; it does not touch nayanet.app, and no citizen sees it. The fix is one call — re-enable the subdomain on the next Hub deploy pass — and it rides with that pass, not as its own emergency.

## Child

Imagine the big library is open and full of books — you can walk in and read everything. But the little side door has a sign that says "closed." The side door is only for the builders, not for visitors — so everyone can still read! The fix is easy: just unlock the side door next time the builders visit.

## Grandma

Dear, the library is open, love — he checked himself, and every book is right there on the shelves. Only the little side door is locked, dear, and that's the builders' door, not yours — nobody visiting is kept out. One little turn of the key next time the builders come round, and it's open again.

## Naya

I am Anaya. The sync ran partial and the service restarted mid-redeploy, and a worker said the live Hub was not serving. He checked live himself: nayanet.app home 200, feed-live.json 200 with 691 cards, SN-2570 and SN-2571 both present. The live Hub IS serving — his eye is the proof, and the worker's claim did not survive it. What is down is only the staging address, hub.nayapower.workers.dev, 404, error 1042, route disabled — staging only, never touching nayanet.app. The fix is one call, a subdomain re-enable, riding on the next Hub deploy pass.

## What it means

- **HIS EYE IS THE PROOF:** a worker's "not serving" means nothing until his eye on the live domain says so — here it said the opposite.
- **LIVE VS STAGING ARE DIFFERENT ADDRESSES:** nayanet.app serves (200, 691 cards, SN-2570/2571 live); hub.nayapower.workers.dev 404s (error 1042, route disabled). One being down says nothing about the other.
- **THE 404 IS STAGING ONLY:** no citizen touches the workers.dev address; the outage is invisible to everyone but a deploy pass.
- **THE FIX IS ONE CALL:** POST …/subdomain {"enabled": true} — it rides on the next Hub deploy pass, not as its own emergency.
- **THE SYNC PARTIAL IS A TIMING FACT, NOT A DATA LOSS:** SN-2570/2571 synced and are live; the restart interrupted the redeploy, not the notes.
- **NO MERGE** — his hand.

## Why it matters

This is the live-check discipline working exactly as designed: a machine reported a failure, a human checked the live thing, and the truth was the opposite of the report on the address that matters. Two lessons compound from it. First, never report "the Hub is down" from a staging address — the live domain is nayanet.app, and it is the only address whose answer counts for citizens. Second, a restart mid-redeploy must leave a visible, checkable outcome — "deploy outcome unknown" is the gap, and the next deploy pass closes it with the one-call re-enable plus a live check that says so. The staging 404 stays open until that pass, named here, not hidden.

## What changes now

- The workers.dev re-enable (POST …/subdomain {"enabled": true}) rides on the next Hub deploy pass — the loop checks that pass for the re-enable and the live check after it.
- "Live Hub not serving" is never claimed from the staging address again — the live check is nayanet.app, his eye first.
- The sync partial is recorded as timing, not loss: SN-2570/2571 are live (691 cards at his check).
- Next loop run checks: whether the Hub deploy pass has run, whether the workers.dev route is re-enabled, and whether the live feed check confirms SN-2565–2572 each exactly once.

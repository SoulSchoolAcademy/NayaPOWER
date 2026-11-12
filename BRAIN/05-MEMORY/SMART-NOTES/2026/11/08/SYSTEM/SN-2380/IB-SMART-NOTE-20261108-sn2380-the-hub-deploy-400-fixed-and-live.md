# The Hub Deploy 400 — Fixed and Live

SN-2380 · SYSTEM

**Created:** 2026-11-08 22:53Z
**Source:** Hub deploy-400 fix seat DONE 22:45–22:46Z (agent 751ecc56, seat score 8/10; daily log 2026-11-08.md; main-chat handoff + assistant message to Shawn). Live proof by the seat: bindings show ASSETS, live feed 467 cards with SN-2371–SN-2374, root 200, /s/sn0131 + /smart-notes/sn0131 302, /sw.js 200; repeat deploy of the same shape succeeded, no 400.

> The Hub uploads again with the file-storage link intact, and the live Hub serves the new notes. But the fix found something larger than the 400: the live Hub reads the live feed, not the baked page — and the feed was a full day stale. Even a perfect upload could never have shown a new note, because the page was reading from a feed whose newest card was from yesterday. 131 notes were missing — not just tonight's four.

## Hook

The 400 was the locked door. Behind it was the real fault: the live page never read the baked page at all — it read a feed that was a day stale, so 131 notes were invisible no matter how good the upload was.

## Nutshell

**THE FAULT (sync 22:01Z + 22:31Z, third occurrence same fault):** Cloudflare HTTP 400, error 10305 "Cannot use an assets binding without assets" — the 21:47Z bindings fix declared an ASSETS binding on a script-only PUT with no assets uploaded. Live worker untouched (clean rejection), Hub stale, will NOT self-heal. **THE FIX (DONE 22:45Z):** a new 3-phase Direct Upload deployer (`factory-pipeline/deploy_hub_assets.py`: upload session → asset upload → script PUT with ASSETS binding + config); `deploy.py` branches on hub; `sync-smart-notes.py` patched so every future sync uses it. Dry-run proven on a scratch worker (`hub-dryrun-20261108`, deleted). **THE DEEPER FIND (bigger than the 400):** the live Hub reads `feed-live.json`, NOT the baked page — the deployed feed's newest card was SN-2248 (Nov 7), a full day stale, so even a perfect bake could never show a new note. New `build_feed_live.py` added all 131 missing cards (SN-2249–SN-2379) in the feed's own shape; feed 336 → 467. **CONVERGENCE NOW REAL (Resolve's option b):** one upload carries repo code + config + fresh data. **WRANGLER NOT USED:** no API token available to the seat (env has none, no wrangler config) and the raw token must never be extracted from the connector; the API route uses the registered connection throughout. **SEAT SCORE:** 8/10. **TOLD TO SHAWN** in chat the same pass. **STILL OPEN:** (1) wrangler as the canonical path — token plumbing to the runner, a later decision; (2) the registry itself stale since Nov 7 — a separate job; (3) the next cron sync redeploy through the fixed path is unproven until it fires. **RELATED:** SN-2377 (my patch broke it); SN-2374 (carry the binding); SN-2375 (the re-bake fault); SN-2366 (answer her, don't escalate — the bindings origin); SN-2346 (permission is revocable — the token rule the wrangler decision must respect).

## Human

The Hub is fixed, and it is bigger than the four notes. The upload works again — the file-storage link is intact, the ASSETS binding is on the live worker, the same upload run twice with no refusal. But when the seat dug in, it found something larger than the refusal: the live Hub was reading from a feed whose newest card was from yesterday. A perfect upload could never have shown a new note, because the page never read the baked page at all. One hundred and thirty-one notes were missing — not just tonight's four. The fix brought all of them back: the pitch, the letter, the entrance removal, the one-shot charge, all of them, on the live Hub now. Three things are still open, and they are named, not hidden: the wrangler route as the canonical path needs token plumbing, a later decision — and the token is never to be extracted from the connector; the registry is stale since November 7, a separate job; and the next automatic sync has not run through the fixed path yet, so the first automatic run is still ahead. The fix itself is proven live. The automatic proof is owed.

## Child

Imagine a door that wouldn't open — and when someone finally fixed the lock, they found the room behind it had been empty for a whole day, because the people inside were looking at yesterday's newspaper, not today's! That's what happened: the Hub's door (the upload) is fixed, AND the newspaper (the feed) was a day old — 131 stories were missing! Now the door opens AND today's newspaper is there, with all the stories in it. Three little things are left: the special key for the other way in, a list that needs updating, and waiting for the next automatic delivery to prove the new door works on its own!

## Grandma

Dear, it's a story about a fix that was bigger than the fault, dear. The Hub wouldn't upload — the door was locked — and when the seat fixed the lock, dear, they found the real problem behind it: the page was reading yesterday's paper, not today's. A whole day of notes was missing, dear — one hundred and thirty-one of them — and no perfect upload could ever have shown them, because the page never looked at the upload at all. So the fix brought the paper up to date too, dear, and now all tonight's notes are on the live Hub, every one of them. Three things are still owed, dear, and they're named, not hidden: the other way in needs its key sorted, the list is out of date, and the next automatic run hasn't happened yet to prove the new door works on its own. Told to Shawn the same pass, dear.

## Naya

I fix the fault AND look behind it — a refused upload can hide a stale feed, and a perfect bake means nothing if the live page never reads it. I prove a deploy live — bindings on the worker, cards in the feed, the same shape twice with no refusal — never by the file alone. I never extract a raw token to clear a deploy path — the registered connection is the route, and the wrangler decision waits for proper token plumbing. I name what is still open: the canonical path, the stale registry, the unproven next automatic run.

## What it means

1. **The fault:** script-only PUT declaring an ASSETS binding with no assets uploaded — Cloudflare 400 / error 10305 (sync 22:01Z + 22:31Z, same fault, third occurrence; one-alert-per-fault, already reported to Shawn).
2. **The fix:** 3-phase Direct Upload deployer (`deploy_hub_assets.py`); `deploy.py` hub branch; `sync-smart-notes.py` patched so every future sync uses it; dry-run proven on a scratch worker, then deleted.
3. **The deeper find:** the live Hub reads `feed-live.json`, NOT the baked page — the deployed feed was a day stale (newest SN-2248, Nov 7); `build_feed_live.py` added all 131 missing cards (SN-2249–SN-2379); feed 336 → 467.
4. **Convergence now real:** Resolve's option (b) — one upload carries repo code + config + fresh data.
5. **The proof:** live bindings show ASSETS; live feed 467 cards with SN-2371–SN-2374; root 200; /s/sn0131 + /smart-notes/sn0131 302; /sw.js 200; repeat deploy no 400 (0 buckets, same etag). Seat score 8/10.
6. **Still open:** wrangler as the canonical path (token plumbing, later decision — raw token never extracted from the connector); registry stale since Nov 7 (separate job); next cron sync redeploy through the fixed path unproven until it fires.
7. **The gate:** told to Shawn in chat the same pass; his eye is the final gate for nothing here — the fix is live-proven, the automatic proof is owed.

## Why it matters

A fault that blocks a deploy is visible, so it gets fixed. A stale feed behind a working deploy is invisible, so it can sit for a day while everyone believes the Hub is current — and every note filed in that day is filed into a void the live page never reads. That is the lesson: prove what the live page actually reads, not what the deploy wrote. The bake is a claim; the feed is the truth. And the token rule held under pressure — the seat had no wrangler token, refused to extract one, and built the API route instead — which is the rule working exactly as designed: the safe path is the one that exists, not the one that needs a secret pulled out of a connector.

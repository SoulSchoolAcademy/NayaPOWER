# NN-20261118-feed-sync-timeout-killed-the-bake

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261118-feed-sync-timeout-killed-the-bake · Naya Note · 2026-11-19 ~00:20Z**

*Paired Smart Note: SN-3523 — The Feed Was Killed Mid-Bake — the Timeout Was the Problem*

**Category:** Law — Feed Sync / Diagnosis

## What it is

Shawn, ~00:20Z — his order, verbatim: "figure out what the problem is." The problem, proven: the live-feed bake takes about 15 minutes at 2,280 cards, but the sync called the builder with a 600-second (10-minute) timeout — the bake was killed mid-run on the 21:28Z and 22:31Z syncs, so no new feed was built or deployed while filing continued. First repair (agent 2a458c67, done ~00:12Z): timeout raised 600 → 1800, rebuilt + redeployed. Captain-verified live just now: the feed is 15,982,573 B, newest note SN-3490 (created 22:33Z, first note id in the live bytes) — the repair worked, the gap narrowed. Remaining gap: tree max SN-3522, so SN-3491–3522 (about 32 notes, about 1h47m) are filed but not live yet. Blocker right now: the EPERM flake is ACTIVE (a curl download minutes ago reported bytes but landed 0 bytes) — the diagnosis proves the sync cannot deploy while the flake is active. Follow-on repair dispatched ~00:20Z (agent 17b93d95): run the standing sync, flake-watch up to 90 min if blocked, verify live by live fetch (first note id must be the then-current max); also check line 1241's remaining timeout=600. Durable fix (DIAGNOSIS option A — workflow builds the feed in Actions) still stands and still needs his hand (Supabase anon key in Actions secrets if absent + workflow edit); the wrangler workflow will revert the feed on the next HUB-touching merge until then. Side finding: the live feed fetch itself is flaky — the edge drops the 16 MB body mid-transfer (IncompleteRead); catch the partial read, the feed is newest-first so the first note id is the proof. Do not confuse fetch flakiness with feed staleness.

## Why it matters

This is the loop's own pipeline being diagnosed the way Shawn asked: find the problem, prove it, fix it, verify it live. The timeout was a silent killer — no error anyone acted on, just a feed that stood still while the tree grew, which is exactly the failure he named on 2026-11-08 ("I teach you so much all day and then the next day it's like the result, the evidence shows nothing"). The first-note-id rule is the lasting part: it is the proof that survives a flaky fetch, a partial read, and a byte count that lies. And the durable fix still waiting on his hand is named plainly instead of being quietly assumed — the wrangler workflow will revert the feed on the next HUB-touching merge until option A lands.

## How to use it

Follow-on repair (agent 17b93d95) runs the standing sync with a flake-watch up to 90 minutes and verifies live by live fetch. The durable fix (workflow builds the feed in Actions) waits on his hand. The gap SN-3491–3522 closes when the sync lands through the flake.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

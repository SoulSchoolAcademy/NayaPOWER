# SN-3523 — The Feed Was Killed Mid-Bake — the Timeout Was the Problem

**Filed:** Intelligence Loop run 336, 2026-11-19 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3523; filed as SN-3523 under its draft number.

**Filed by:** Intelligence Loop run 336, 2026-11-19 — Shawn's order + the proven cause of the stale live feed, ~00:20Z. The feed-sync diagnosis, filed as MEMORY.md records it.

**Paired Naya Note:** NN-20261118-feed-sync-timeout-killed-the-bake

## The teaching, in his words (verbatim)

"figure out what the problem is"

## The understanding

He asked for the problem to be figured out, and the problem was figured out — proven, not guessed. The live-feed bake takes about 15 minutes at 2,280 cards, but the sync called the builder with a 600-second (10-minute) timeout: the bake was killed mid-run on the 21:28Z and 22:31Z syncs, so no new feed was built or deployed while filing continued. That is why the tree kept growing and the live feed stood still — the notes were filed, the feed was never baked. The first repair (agent 2a458c67, done ~00:12Z) raised the timeout 600 → 1800, rebuilt and redeployed; the captain verified live just now — the feed is 15,982,573 B, newest note SN-3490 (created 22:33Z, first note id in the live bytes). The repair worked; the gap narrowed. The remaining gap: tree max SN-3522, so SN-3491–3522 (about 32 notes, about 1h47m) are filed but not live yet. The blocker right now is the EPERM flake, ACTIVE — a curl download minutes ago reported bytes but landed 0 bytes — and the diagnosis proves the sync cannot deploy while the flake is active. The follow-on repair (agent 17b93d95, dispatched ~00:20Z) runs the standing sync, flake-watches up to 90 minutes if blocked, verifies live by live fetch (first note id must be the then-current max), and checks line 1241's remaining timeout=600. The durable fix (DIAGNOSIS option A — the workflow builds the feed in Actions) still stands and still needs his hand (Supabase anon key in Actions secrets if absent + workflow edit); the wrangler workflow will revert the feed on the next HUB-touching merge until then. And a side finding that saves the next misdiagnosis: the live feed fetch itself is flaky — the edge drops the 16 MB body mid-transfer (IncompleteRead). Catch the partial read; the feed is newest-first, so the first note id is the proof. Do not confuse fetch flakiness with feed staleness.

## The law

A timeout must exceed the work it guards: the bake takes about 15 minutes at 2,280 cards, so a 600-second timeout kills it mid-run and the feed stands still while filing continues. Verify live by the first note id in the live bytes — never by a fetch that can lie, and never by a byte count alone. A partial fetch is fetch flakiness, not feed staleness: catch it and read the first note id.

## Owed from this dictation

Follow-on repair (agent 17b93d95, dispatched ~00:20Z): run the standing sync, flake-watch up to 90 minutes, verify live by live fetch (first note id = then-current max), check line 1241's remaining timeout=600. Durable fix (workflow builds the feed in Actions) still needs his hand. The gap SN-3491–3522 closes when the sync lands through the flake.

**The bake takes as long as it takes — the timeout obeys the bake, never the other way round.**

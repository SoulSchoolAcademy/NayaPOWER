# Naya Intelligence Board V1 — World Model projection

**Status:** candidate, read-only code on review branch. Not production-proven. No merge/dispatch/deploy authority.

## In a nutshell

One continuously *refreshable* operating picture for cold Nayas and humans: what is currently reported, why it matters, what is unknown, and where to go for real decisions. This is an orientation projection, NOT a new canonical state store or a substitute for the mission feed.

## The canonical path (do not duplicate)

Live GitHub / mission #2154 / team #2175 / ledger #2396
→ existing [World Model](../tools/world_model.py) (facts + section freshness)
→ [Intelligence Board](../tools/intelligence_board.py) (read-only human/JSON projection)
→ existing [Compass](../tools/nayas_guide.py), [value calculus](../kernel/value_calculus.py), current LAW gate for a consequential action
→ independently verified outcomes / existing Smart Note and successor loops.

The Board reports the mission text as **SOURCE_REPORTED**, not proven. A section must pass the *existing* World Model `section_usable` gate; stale, partial or missing data becomes UNKNOWN/READ_MORE. The cached law/briefing section NEVER creates permission. An issue-comment lane state is an observation, not a mutex or authoritative lease. Ledger metadata does NOT prove causality. One snapshot does NOT prove what changed.

## Use

After the already-existing World Model refresh (do not invent a second poller):

```sh
python3 tools/world_model.py refresh
python3 tools/intelligence_board.py --format markdown
python3 tools/intelligence_board.py --format json
python3 -m unittest discover -s tests -p 'test_intelligence_board.py' -v
```

World Model cache default: `~/.naya/world-model.json`. Supply `--world-model PATH` for local fixtures or nondefault machines.

Exit 0 = mission + exact main tip usable as current *orientation*. Exit 2 = READ_MORE. **Neither means authorized or safe to ACT**. Other sections can independently remain UNKNOWN/PARTIAL; inspect the `freshness` map before using them.

## What this first slice DOES

- Uses the one existing World Model and its freshness contract.
- Answers: nutshell, how it connects, current tip/mission, source-reported priority rows, PR counts only if complete, lanes (nonexclusive), laws (orientation only), links, proof limits, and one safe next read.
- Produces human Markdown and machine JSON without a second truth store.
- Fails closed when mission or tip is stale, malformed, or unavailable.
- Contains local falsifiers for missing/stale/partial inputs, authority confusion and fabricated proof.

## What it DOES NOT claim

- It has not created an always-running service, scheduled polling or automatic GitHub posting.
- It has not independently verified a learning claim, interpreted a full mission history, nor measured a source-state delta.
- It has not connected to the Hub user interface or deployed code.
- It does not override the #2459 merge hold or protocol ratification/LAW.
- It does not automatically score options or invoke ACT.

## Next smallest authorized wiring slice

Have the existing World Model/dispatcher owner call this read-only renderer **after its existing refresh**; publish the same output to the existing #2175 coordination/activation path via the pre-existing publishing identity, with deduplication, freshness watermark, rate limits, and update-in-place or capped history. This should NOT require a new GitHub workflow or another store.

Acceptance requires one fresh source event → updated snapshot → Board JSON/Markdown → subsequent cold worker reads it → Compass derives the authorized next decision from current evidence. Show the timestamps, links and exact source SHA; stale/partial/403 input must never turn green. Independent verifier checks those bytes and stops on conflicting ownership.

**Owner alignment:** World Model/Compass Naya 5, interfaces #1870, live mission #2154 and team #2175; coordinate before wiring. Merge only after the current queue hold is lifted, independent checks pass and the governing merge rule permits it.

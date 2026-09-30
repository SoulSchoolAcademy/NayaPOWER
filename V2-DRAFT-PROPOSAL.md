# Pre-registration v2 — DRAFT proposal (not witnessed, not frozen)

**Status: DRAFT ONLY.** This document proposes the mechanical shape of a future
pre-registration v2. It does **not** witness v2, does **not** mutate v1, and
does **not** authorize any re-commit, promotion, or execution. Real v2 values
can only be computed at re-commit time from live data through the governed
path. Everything below is a draft of the *procedure* plus worked examples on
fixtures — never the real block identities.

## Why v2 exists (the only legitimate reason)

v1 remains byte-for-byte immutable. v2 exists solely because the approved
capability-carry repair changes persisted block content: a re-committed block
carrying `content.capabilities` has a different content hash (and, from a new
event id, a different block id) than the v1-pinned revision. v2 re-pins the
new identities. v2 must represent **the same pre-registered experimental
intent after a documented infrastructure repair** — not a better-looking
experiment. Task instances, rubric, thresholds, hypotheses, order, and seed
are carried unchanged.

## Derivation rules (deterministic, to be executed at re-commit)

1. **Block id:** `intelligent_block_id = 'IB-' || regexp_replace(p_event_id, '[^A-Za-z0-9_-]', '-', 'g')`
   (minted by `nayanet_intelligence_commit` from the NEW event id — therefore
   not knowable until the governed re-commit; never invented here).
2. **Content hash (registry scheme, as v1):**
   `sha256(canonical_json(content))` with `sort_keys=True`,
   `separators=(',',':')`, `ensure_ascii=False`.
3. **Capability delta:** adding the validated `capabilities` array is the ONLY
   content change vs the v1 revision; the hash delta is deterministic and
   attributable solely to that key.

### Worked fixture example (illustrative, not real blocks)

Content `{lesson, topic, category}` (fixture text):

- without capabilities → `e74245c023a6d0f86e5324bfcf40896941395ea762c9650a102c2da9a44ca66f`
- with `capabilities: ["governance_triage"]` →
  `96a5ddc115a9177b22dfaf5fda826a12357a6a4e664775570c4d26a8bd12c9a0`

Same procedure, same code → same hashes. At re-commit, substitute the real
persisted content objects.

## Predecessor link schema (immutable v1 → draft v2)

Each v2 draft entry MUST carry:

```json
{
  "v1_block_id": "IB-SMART-NOTE-20260930-sn013-decision-efficiency",
  "v1_content_hash": "2a534acea3882a352ba27a3d46d42253d37d7aeb93cebe806a1bb60aee450037",
  "v2_block_id": "<minted at re-commit; DRAFT: not yet known>",
  "v2_content_hash": "<computed at re-commit per §2; DRAFT: not yet known>",
  "change_reason": "capability-carry repair changed persisted content (added content.capabilities=[\"governance_triage\"]); no task/rubric/threshold change",
  "supersedes": "v1_block_id",
  "v1_preserved": "byte-for-byte; frozen/v1/* untouched"
}
```

v1 frozen references (carried, not recomputed here):

- treatment: `IB-SMART-NOTE-20260930-sn013-decision-efficiency` /
  `2a534acea3882a352ba27a3d46d42253d37d7aeb93cebe806a1bb60aee450037`
- negative-transfer: `IB-SMART-NOTE-20260930-sn014-compounding-imperative` /
  `318b7a0682f6a5b9d3fe41531c01773d00fae653c2e49d3170fa23a5838a0441`

## Explicit non-goals

- No v2 witnessing happens on this branch.
- No re-commit of SN-013/SN-014 (production data change — separate governed phase).
- No promotion, no state change, no execution authorization.
- The supersede RPC is the governed revision path for production, but it is
  **not invoked** during this branch build (repair now, production revision
  later — separate phases).

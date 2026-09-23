# 2026-09-23 — GAP-002 Intelligent Block Index Projection Repair

**STATUS:** IMPLEMENTED / BUILD VERIFIED / LIVE BROWSER PROOF RUNNING  
**OBJECTIVE:** Make the canonical Intelligent Block persist as one object and arrive at the Hub with truth, authority, provenance, lifecycle, value, and integrity intact.

## Finding

The canonical Intelligent Block already exists in the persistence model and is carried by the Smart Note transaction boundary.

The missing deterministic boundary was the Intelligence Index → Hub projection:

1. `nayanet_intelligent_blocks` rows were indexed.
2. Their metadata did **not** carry the complete `intelligent_block_v1` envelope.
3. The Hub PIS loader explicitly excluded `nayanet_intelligent_blocks` rows.
4. Therefore the Hub could truthfully display a generic event while losing the canonical Block projection.

## Repair

Added:

`supabase/migrations/20260923010000_repair_intelligent_block_index_projection_v1.sql`

The existing index trigger now preserves:

- canonical Intelligent Block V1 envelope;
- identity/event ID;
- source event IDs;
- evidence references;
- schema version;
- source context;
- provenance;
- privacy state;
- truth;
- authority;
- value;
- lifecycle;
- integrity/hash.

No new store or retrieval architecture was introduced.

Updated:

`NAYANET/HUB/src/data/pis.ts`

The canonical PIS loader now admits:

`nayanet_intelligent_blocks`

as an authoritative persistent intelligence source.

## Verification

Hub Quality Gate passed on the resulting canonical HEAD:

- Run: 35876692290
- Result: SUCCESS

The existing live Smart Note and authenticated browser acceptance workflows were automatically triggered from the same canonical HEAD and remain in progress while this note is recorded.

## Architectural result

The intended chain is now:

```
SMART NOTE / SOURCE
→ INTELLIGENT EVENT
→ INTELLIGENT BLOCK
→ PERSISTENCE
→ INTELLIGENCE INDEX
→ PIS RETRIEVAL
→ HUB INTELLIGENT BLOCK
→ PROOF / ACTION
→ LEARNING
```

The Hub does not create a second Block.

It receives the canonical Block projection.

## Remaining proof boundary

Build success is not treated as runtime proof.

The remaining acceptance is:

```
LIVE PERSISTED INTELLIGENT BLOCK
→ AUTHENTICATED RETRIEVAL
→ HUB RENDER
→ EXACT TRUTH / PROVENANCE / HASH OBSERVATION
```

If that browser proof passes, GAP-002 is closed at the tested scope.


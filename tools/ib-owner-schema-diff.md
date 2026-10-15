# IB owner-field schema-diff spec — w187 Naya Beta

Shawn's law: **IB owners = NAYA** — ownership is binary: a block without a
named Naya has no accountable owner. w186 audit (tip ba6263870425):
0/563 capture files + 0/631 projection entries + 0/1261 REAL-TREE dicts name
an owner. This wave delivers the field + the projection-index backfill;
capture schema and REAL-TREE are spec'd below for the next worker.

## Field definition (all three targets)

| key | type | required | values |
|-----|------|----------|--------|
| `owner` | string | yes | named Naya seat, e.g. `Naya Beta`. Matches `^Naya [A-Z][A-Za-z]+( [A-Z][A-Za-z]+)*$`. Never a human, never blank. |
| `owner_source` | string | yes | how assigned: `capture:explicit` \| `capture:captured_by` \| `backfill:provenance:<field>` \| `backfill:area-keyword:<AREA>` \| `backfill:fallback-KNOW` — every assignment auditable, every fallback revisable. |

Default chain (`resolve_ib_owner(capture, block)` in tools/smart_note_v2.py):
explicit capture["owner"] → "Naya <Seat>" named in source.captured_by /
provenance_note / source_reference / context → area-keyword match on
category/topic/subtopic/title → fallback `Naya Beta` (KNOW owns the
projection registry). Owner never gates retrieval — it gates accountability.

## Target (a) — IB-SMART-NOTE capture schema — SPEC (not yet built)

Add `owner` (+ optional `owner_source`) to the capture file envelope in
`.naya/capture/*.json`. Writer: the capture path in tools/smart_note_v2.py
(the capture dict is assembled before `update_registry`). Capture files are
writer-emitted; make `owner` a writer-emitted field defaulted by
`resolve_ib_owner` at capture time, overridable by an explicit `owner` in
the incoming capture request. Do NOT re-emit the 618 historical captures
(their owners live in the projection index after this wave's backfill);
capture schema governs new captures going forward.

## Target (b) — projection-index entry schema — BUILT w187

- Writer: `_update_registry_locked` in tools/smart_note_v2.py now emits
  `owner` + `owner_source` on every new entry (via `resolve_ib_owner`).
- Backfill: `python3 tools/backfill_ib_owner.py [--apply]` — one-writer
  (`registry_transaction`), fail-closed verify inside the transaction:
  every entry gets a valid owner; `corpus_manifest_hash` recomputed via the
  single hashing authority; non-owner entry content proven byte-identical
  (canonical sha256 before==after); identity sets unchanged. Applied w187:
  632/632 entries owned, stripped-content sha match TRUE, manifest
  534d02d2420a → 28703ca17fbd.
- Envelope schema string deliberately NOT bumped (`v1` → `v1.1` is owed):
  tests/test_smart_note_v2.py:527 + the reader at tools/smart_note_v2.py:835
  pin the `v1` envelope. Bumping rides a validator wave WITH test updates.

## Target (c) — BRAIN index block schema (REAL-TREE.json file dicts) — SPEC

REAL-TREE.json `files[]` dicts are `{blob_sha, path, size}` (1260 at tip;
schema `naya.brain.real_tree.v1`), written by tools/regenerate_brain_index.py.
Options for the next worker: (1) add `owner` per file dict resolved from the
smart-note projection index (join on path) with fallback KNOW; (2) keep the
file dicts ownerless and declare the projection index the single ownership
authority (SPOT: one place owns the truth — recommends (2), since file dicts
are content-addressed inventory, not intelligence blocks). Shawn's intent is
IB ownership, not file ownership — (2) likely wins, but it needs his
framework's explicit call, not a guess.

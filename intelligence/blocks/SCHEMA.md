# Intelligent Blocks — Schema v1.1 (CANONICAL CONTRACT)

An **Intelligent Block (IB)** is the atomic unit of learning in NayaPOWER.
One block = one distilled principle, with its source, its proof, when it
applies, how verified it is, and where it is heading (text → briefing → code).

**v1.1 is the canonical contract** (P0-A reconciliation, 2026-10-11). It unifies:
- the file-based authoring schema (v1.0), and
- the persisted machine-canonical envelope
  (`kernel/supabase_intelligent_blocks.py` `CANONICAL_BLOCK_FIELDS`).

Per protocol `BRAIN/04-INTELLIGENCE/0005-...-PROTOCOL-V1.md` §6 and §16:
the persisted envelope is authoritative for identity, owner, scope/privacy,
provenance, epistemic state, type, and version. The file form carries all of
those so any file-authored block round-trips into persistence without loss.

Blocks live in `intelligence/blocks/` as one JSON file per block.
`intelligent_block_id` is the primary machine identity (persisted-style IDs,
e.g. `IB-TEAM-20261011-law-one-divine-oneness`). Legacy sequential `IB-NNNN`
IDs are accepted on read (normalized from `id`) and recorded in
`provenance.aliases`; new blocks use persisted-style IDs.

## Fields

| Field | Type | Required | Authority | Meaning |
|---|---|---|---|---|
| `intelligent_block_id` | string | yes | persisted | Primary machine identity |
| `block_id` | string/null | yes | persisted | Row identity; null until persisted |
| `schema_version` | string | yes | — | `"1.1"` |
| `title` | string | yes | shared | Short human name |
| `purpose` | string | yes | new (§6) | Why preserve this? May be empty for legacy, but new blocks should fill it |
| `principle` | string | yes | file | **One sentence, plain words.** Maps to `content.lesson` on export |
| `owner_id` | string | yes | persisted | **Must be `NAYA`** (Shawn's word 2026-10-11: Naya owns all blocks). Empty or any other value fails validation loudly |
| `owner_scope` | string | yes | persisted | **REQUIRED.** One of `PRIVATE`/`TEAM`/`COLLECTIVE`/`PUBLIC` |
| `block_type` | string | yes | persisted | e.g. `GOVERNED_INTELLIGENCE`, `PRINCIPLE`, `LESSON` |
| `source` | object | yes | file | Human-readable `who`/`when`/`context`; seeds provenance |
| `provenance` | object | yes | persisted | **REQUIRED non-empty dict.** Machine provenance |
| `source_event_ids` | array | yes | persisted | Linked capture event IDs; `[]` until linked |
| `evidence` | array | yes | file | Rich items: `kind`/`ref`/`note`. `evidence_refs` derived on export |
| `applicability` | object | yes | file | Rich `topics[]`/`situations`/`decisions` |
| `applicable_scope` | string | yes | persisted | Coarse scope string |
| `understanding_state` | string | yes | persisted | `CANDIDATE`/`VERIFIED`/`SUPERSEDED`/`DEPRECATED` |
| `status` | string | yes | persisted | `DRAFT`/`DURABLE`/`SUPERSEDED`/`ARCHIVED` |
| `verification_status` | string | yes | file | `UNVERIFIED`/`APPLIED`/`BEHAVIOR-CHANGE-PROVEN`/`COMPOUNDED` |
| `status_history` | array | yes | file | Every status change: `status`, `at`, `note` |
| `graduation` | object | yes | file | `stage` (`text`/`briefing`/`code-gate`), `next_step`, `enforced_by` |
| `authority_implications` | string | yes | new (§6) | What authority is required to use this? |
| `conflicts` | array | yes | new (§6) | Unresolved conflicts/uncertainty; `[]` if none |
| `supersedes_block_id` | string/null | yes | persisted | Canonical supersession link (row ID or IB ID) |
| `superseded_by_block_id` | string/null | yes | persisted | Canonical supersession link |
| `version` | integer | yes | persisted | Incremented on persist; starts at 1 |
| `created_at` | string | yes | shared | ISO-8601 UTC |
| `updated_at` | string | yes | shared | ISO-8601 UTC, bumped on every change |

## Epistemic state mapping (lossless both directions)

| `verification_status` | `understanding_state` | `status` |
|---|---|---|
| `UNVERIFIED` | `CANDIDATE` | `DRAFT` |
| `APPLIED` | `CANDIDATE` | `DURABLE` |
| `BEHAVIOR-CHANGE-PROVEN` | `VERIFIED` | `DURABLE` |
| `COMPOUNDED` | `VERIFIED` | `DURABLE` + `provenance.successor_reuse_proven: true` |

`SUPERSEDED` status overrides: the file ladder position is recovered from
`provenance.file_status_history`. Validation rejects disagreements.

## Verification statuses (in order)

1. **`UNVERIFIED`** — captured but not yet used.
2. **`APPLIED`** — injected at decision time and acted on.
3. **`BEHAVIOR-CHANGE-PROVEN`** — measured behavioral delta with receipts.
4. **`COMPOUNDED`** — survived a cold-start cycle.

A block moves up only with evidence. Never moves down except by supersession.

## Graduation stages (in order)

1. **`text`** — exists as a document.
2. **`briefing`** — injected into every agent's briefing at wake.
3. **`code-gate`** — enforced by code.

## Owner semantics (Shawn's word, 2026-10-11 22:34Z — GRAND-TODO P0)

- `owner_id` is **`NAYA`** on every block. NAYA is the collective system.
- No individual owns a block — not Shawn (he explicitly declined per-block
  ownership), not any seat, not any human. Validation fails closed on any
  other `owner_id` value.
- `owner_id` is immutable for a block's life; superseding blocks also carry `NAYA`.
- Ownership is **operational, not titular**: NAYA's authority is exercised
  only through the verification/promotion gates below. No single agent may
  mutate a block's standing on their own authority.
- Provenance carries the receipt: `provenance.owner_assigned` records who
  said it (Shawn's word, 2026-10-11 22:34Z), when, and the declination of
  per-block ownership.

## Promotion gate

Because the owner is the collective (never an individual), promotion actions
— advancing `verification_status` (`ib update`) or advancing the graduation
stage (`ib graduate`) — require a **gate receipt**:

1. A receipt is attached as evidence first (`ib evidence ...` — capture is
   always open and ungated).
2. The promotion cites that receipt's `ref` with `--gate <ref>`.
3. The cited `ref` must match an evidence item already on the block.

Without a matching gate receipt the action **fails closed**: nonzero exit,
block file untouched. The gate receipt is recorded in the status-history
entry as `gate_receipt`. Downgrades stay refused (supersede instead).

Machine-enforced in `intelligence/tools/ib.py::_require_gate`; contract
semantics in `intelligence/tools/ib_reconcile.py` (`SYSTEM_OWNER`).

## Rules

- IDs are never reused. Deleted blocks are forbidden — supersede instead.
- `principle` is one sentence. No jargon.
- Evidence is receipts, not claims.
- `owner_id` must be `NAYA`; `owner_scope`, `provenance` are REQUIRED —
  export raises without them, mirroring
  `kernel/supabase_intelligent_blocks.py::from_row`.
- `REGISTRY.json` is generated (`ib reindex`), never hand-edited.
- Validate with `ib validate`, `pytest tests/test_intelligent_blocks.py`,
  and `pytest intelligence/tools/test_ib_reconcile.py`.
- Round-trip contract: `from_persisted_row(to_persisted_row(block))` preserves
  identity, owner, privacy, provenance, evidence refs, state, graduation,
  supersession, purpose, authority implications, and conflicts — **losslessly**,
  including the rich file-form detail: evidence kind/type + per-item
  explanatory notes (`provenance.evidence_detail`), detailed applicability
  (`provenance.applicability_detail`), and status history
  (`provenance.file_status_history`). #2386 closed 2026-10-11: the exporter now
  emits everything the importer expects; tampered detail fails closed
  (ValueError), rows persisted before #2386 import via documented ref/empty
  fallbacks (rich fields are never invented).
  See `intelligence/tools/ib_reconcile.py`.

# IB Identity Reconciliation — Field Mapping P0-A

**Date:** 2026-10-11
**Tip:** `230b397ac449d8904e06c65a8a2027b862882fb2`
**Status:** ANALYSIS → BUILD

## The two schemas

**A. File-based** (`intelligence/blocks/SCHEMA.md` v1.0, PR #2375):
Authoring surface. 14 top-level fields. Sequential `IB-NNNN` IDs.

**B. Persisted** (`kernel/supabase_intelligent_blocks.py` `CANONICAL_BLOCK_FIELDS`):
Runtime machine-canonical. 20 fields. `block_id` + `intelligent_block_id`.

**C. Protocol envelope** (`BRAIN/04-INTELLIGENCE/0005-...-PROTOCOL-V1.md` §6):
Human-ratified. 19 required answerable questions.

## Complete field mapping

| # | Concept (§6) | Persisted (B) | File-based (A) | Verdict |
|---|---|---|---|---|
| 1 | IDENTITY | `block_id` (row) + `intelligent_block_id` (e.g. `IB-NAYA-NODE-0001-0001`) | `id` (`IB-0001` sequential) | **MISMATCH** — incompatible ID schemes; file has no `block_id` |
| 2 | PURPOSE | implicit in `content` | implicit in `title` | **GAP** — neither has explicit purpose field |
| 3 | OWNER | `owner_id` **REQUIRED** (raises if empty) | — | **MISSING in A** — file blocks have no owner |
| 4 | SCOPE/PRIVACY | `owner_scope` **REQUIRED** (e.g. `PRIVATE`), `applicable_scope` | `applicability.topics/situations/decisions` (no privacy) | **MISSING in A** — no privacy boundary |
| 5 | TYPE | `block_type` (e.g. `GOVERNED_INTELLIGENCE`) | — | **MISSING in A** |
| 6 | MEANING | `content.lesson` (lesson text in content dict) | `principle` (one sentence) + `title` | **SHAPE MISMATCH** — same meaning, different containers |
| 7 | SOURCE LINEAGE | `provenance` **REQUIRED** non-empty dict + `source_event_ids` array | `source` {who, when, context} | **SHAPE MISMATCH** — no event IDs in A; no who/when in B's provenance contract |
| 8 | EPISTEMIC STATE | `understanding_state` (CANDIDATE/VERIFIED/…) + `status` (DURABLE/SUPERSEDED/…) | `verification_status` (UNVERIFIED/APPLIED/BEHAVIOR-CHANGE-PROVEN/COMPOUNDED) | **VOCAB MISMATCH** — two different state machines |
| 9 | FRESHNESS | `created_at`, `updated_at`, `version` | `created_at`, `updated_at`, `status_history[]` | **COMPLEMENTARY** — A richer history, B has version counter |
| 10 | APPLICABILITY | `applicable_scope` | `applicability` {topics[], situations, decisions} | **A RICHER** — B's scope is coarser |
| 11 | RELATIONSHIPS | separate relationship objects (lineage) | `supersedes`/`superseded_by` only | **A NARROWER** — only supersession, no support/depend/refine/contradict |
| 12 | EVIDENCE | `evidence_refs` | `evidence[]` {kind, ref, note} | **A RICHER** — B's refs are pointers only |
| 13 | CONFLICTS/UNCERTAINTY | — | — | **GAP in both** — no explicit conflicts field |
| 14 | AUTHORITY | via grants + RLS (external) | — | **MISSING in A** — no authority implications field |
| 15 | VERIFICATION | `understanding_state` | `verification_status` + `status_history` | overlap with #8 |
| 16 | SUPERSESSION | `supersedes_block_id`, `superseded_by_block_id` (row IDs) | `supersedes`, `superseded_by` (IB-IDs) | **NAME + TARGET MISMATCH** — different field names, different ID spaces |
| 17 | USAGE/OUTCOME | — | — | **GAP in both** |
| 18 | BEHAVIORAL EFFECT | — (implicit) | implicit in `BEHAVIOR-CHANGE-PROVEN` | **IMPLICIT in both** |
| 19 | SUCCESSOR EFFECT | — (implicit) | implicit in `COMPOUNDED` | **IMPLICIT in both** |
| — | GRADUATION | — | `graduation` {stage, next_step, enforced_by} | **A-ONLY** — valuable, keep |

## Critical losses on round-trip (A → B)

If a file-based block is persisted without reconciliation, these are **LOST**:
1. `owner_id` — B **raises ValueError** without it. File blocks cannot persist at all.
2. `owner_scope` — B **raises ValueError** without it. Same.
3. `provenance` — B **raises ValueError** if empty. File `source` doesn't satisfy the dict contract.
4. Privacy boundary — file blocks have no scope; persisting them would default to whatever the receiver assumes (danger: private-as-public or public-as-private).
5. `block_type` — defaults to `GOVERNED_INTELLIGENCE`, possibly wrong.
6. Epistemic state — `BEHAVIOR-CHANGE-PROVEN` has no B equivalent; mapping is lossy.
7. Graduation stage — dropped entirely (no B field).

## Critical losses on round-trip (B → A)

If a persisted block is projected to file form without reconciliation:
1. `block_id` (row identity) — dropped; supersession chains break.
2. `owner_id` / `owner_scope` — dropped; re-persist would fail or misattribute.
3. `understanding_state`/`status` — mapped lossily to `verification_status`.
4. `source_event_ids` — dropped; lineage severed.
5. `version` — dropped.

## Design decision: the canonical contract

Per protocol §6 ("Existing persistence/schema fields remain authoritative where they are more specific")
and §16 ("Supabase/receiver-owned Intelligent Block identity and provenance remain machine-canonical"):

- **B (persisted) is authoritative** for: identity (`intelligent_block_id` + `block_id`),
  owner, scope/privacy, provenance, epistemic state, type, version.
- **A (file-based) is authoritative** for: authoring ergonomics, graduation path,
  status history detail, evidence richness, applicability detail.
- **The canonical contract = B's required fields + A's valuable additions.**
  No third schema. The file form is extended to v1.1 to carry everything B requires,
  so any file-authored block round-trips into persistence without loss.

Field authority table (canonical contract v1.1):

| Field | Authority | Notes |
|---|---|---|
| `intelligent_block_id` | B | Primary machine identity. File form adopts B's ID scheme. |
| `block_id` | B | Row identity; null until persisted (file-authored blocks get it on commit). |
| `owner_id` | B | REQUIRED. File form must carry it. |
| `owner_scope` | B | REQUIRED. `PRIVATE`/`TEAM`/`COLLECTIVE`/`PUBLIC`. |
| `block_type` | B | Default `GOVERNED_INTELLIGENCE`. |
| `title` | shared | Human name. |
| `principle` | A | One-sentence meaning → maps to `content.lesson` on persist. |
| `content` | B | Persisted container; file form generates from principle+title on export. |
| `provenance` | B | REQUIRED dict. File form carries it alongside human `source`. |
| `source` | A | Human-readable {who, when, context}; feeds provenance on export. |
| `source_event_ids` | B | Array; empty until linked. |
| `understanding_state` | B | Epistemic state machine (see mapping). |
| `status` | B | Lifecycle: `DRAFT`/`DURABLE`/`SUPERSEDED`/… |
| `verification_status` | A | 4-state ladder; maps to/from understanding_state (see mapping). |
| `status_history` | A | Kept; feeds version/audit on export. |
| `version` | B | Integer; incremented on persist. |
| `applicable_scope` | B | Coarse scope; derived from applicability on export. |
| `applicability` | A | Rich {topics, situations, decisions}; kept. |
| `evidence` | A | Rich array; `evidence_refs` derived on export. |
| `evidence_refs` | B | Pointer array; derived from evidence on export. |
| `supersedes_block_id` etc. | B | Canonical names; file form adopts B's names. |
| `graduation` | A | Kept (A-only value). |
| `authority_implications` | NEW | §6 #14; added to v1.1 (was missing in both). |
| `conflicts` | NEW | §6 #13; added to v1.1 (was missing in both). |
| `purpose` | NEW | §6 #2; added to v1.1 (was implicit in both). |
| `created_at`/`updated_at` | shared | ISO-8601 UTC. |

### Epistemic state mapping (lossless both directions)

| File `verification_status` | Persisted `understanding_state` | Persisted `status` |
|---|---|---|
| `UNVERIFIED` | `CANDIDATE` | `DRAFT` |
| `APPLIED` | `CANDIDATE` | `DURABLE` |
| `BEHAVIOR-CHANGE-PROVEN` | `VERIFIED` | `DURABLE` |
| `COMPOUNDED` | `VERIFIED` | `DURABLE` (+ `successor_reuse_proven: true` in provenance) |

Reverse mapping uses `status` + provenance flags to disambiguate.
`SUPERSEDED` status overrides all (from `superseded_by_*` non-null).

### ID scheme

File form adopts B's `intelligent_block_id` scheme. Sequential `IB-NNNN` becomes
a **legacy alias** recorded in `provenance.aliases`. New file blocks use
`IB-<SCOPE>-<YYYYMMDD>-<slug>` (matching persisted convention, e.g.
`IB-SMART-NOTE-20261008-sn0632-...`). The 20 seed blocks keep their `IB-NNNN`
as primary file ID with a migration that assigns canonical persisted-style IDs
on first commit — recorded bidirectionally so neither form loses the link.

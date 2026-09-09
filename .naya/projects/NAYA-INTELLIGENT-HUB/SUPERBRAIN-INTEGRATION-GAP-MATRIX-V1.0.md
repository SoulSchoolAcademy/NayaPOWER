# NAYANET SUPERBRAIN — INTEGRATION GAP MATRIX
## Version 1.0

**Purpose:** map the NayaNET Superbrain contract against the existing NayaPOWER implementation so we extend one system instead of creating competing infrastructure.

**Evidence rule:** this matrix reports repository/document evidence. Runtime-proven status is only claimed where the repository's current evidence supports it.

| Capability | Existing NayaPOWER evidence | Decision | AAA requirement / next proof |
|---|---|---|---|
| Canonical identity | Note Events use stable event IDs; validation enforces identity | KEEP | Add/verify any missing object types without changing event identity |
| Time/date organization | Canonical event store is YEAR/MONTH/DAY/HOUR; timezone-aware timestamps are required | KEEP + EXTEND | Normalize multi-time fields where applicable and prove point-in-time reconstruction |
| Primary memory store | `.naya/memory/events/` is explicitly canonical | KEEP | Do not create another notes/memory root |
| Smart Notes / Note Events | `smart_notes_v3.py`, event index, verification receipt model | KEEP + EXTEND | Complete runtime proof and benchmark duplicate/update/supersession behavior |
| Exact retrieval | Existing runtime supports exact ID/title/subject matching | KEEP | Benchmark exact lookups and explicit user references |
| Lexical retrieval | Existing BM25/lexical scoring exists | KEEP | Benchmark precision/recall and phrase behavior |
| Semantic retrieval | Existing TF-IDF similarity exists; vector adapter is optional future capability | KEEP + EXTEND | Add embeddings only if benchmark evidence shows meaningful gain |
| Query expansion | Existing aliases/concept/query expansions exist | KEEP + EXTEND | Expand terminology systematically without polluting canonical content |
| Metadata | Existing events carry project, type, tags, aliases, concepts, status, source, verification, etc. | KEEP + EXTEND | Establish one canonical metadata schema and validation coverage |
| Hierarchy | Chronological event paths plus semantic project/domain concepts are documented | KEEP + EXTEND | Build derived semantic views without duplicating events |
| Relationships | Relationship-aware retrieval and typed event relationships already exist | KEEP + EXTEND | Strengthen graph index/traversal and bounded expansion tests |
| Relevance | Existing scoring combines exact, lexical, TF-IDF, authority, lifecycle, recency, and relationship boost | KEEP + EXTEND | Add task-intent, scope, permission, and temporal-fit evaluation |
| Scope/project boundaries | Project is a first-class Superbrain concept; privacy/federation laws exist | KEEP + EXTEND | Prove pre-delivery scope filtering with adversarial cross-project fixtures |
| Permissions | Permission/collective intelligence architecture is documented | EXTEND + VERIFY | Runtime enforcement must be proven before production claims |
| Provenance | Source and evidence fields plus verification/promotion boundaries exist | KEEP + EXTEND | Benchmark source-to-claim traceability |
| Authority | NayaPOWER defines separate conduct and reality authority hierarchies | KEEP | Ensure retrieval never promotes retrieved text into authority |
| Lifecycle | ACTIVE/CANONICAL/HISTORICAL/SUPERSEDED/CONFLICTED/STALE states exist | KEEP + EXTEND | Add/verify archive and explicit current-state resolution behavior |
| Supersession/conflict | Existing validation and retrieval account for supersession/conflict | KEEP + EXTEND | Run adversarial stale/conflict/supersession suite |
| Summarization | CIS and report generation exist; progressive context is specified | EXTEND | Implement source-linked summary/detail expansion as a first-class retrieval stage |
| Context assembly | Boot protocol and Smart Brain OS define tiered selective loading | KEEP + EXTEND | Prove smallest-sufficient-context behavior with benchmark cases |
| Auditability | Git history, event metadata, receipts, and promotion boundaries exist | KEEP + EXTEND | Standardize material-change audit record and verification receipt coverage |
| Outbox/external delivery | Smart Note sharing architecture defines external delivery boundaries | KEEP + VERIFY | Prove confirmed delivery and retry semantics where runtime is available |
| CIS compounding | Daily/period intelligence architecture and generators exist | KEEP + VERIFY | Complete A→B→C runtime compounding proof |
| Cross-tool continuity | Model-independent operating contract and restore protocol exist | KEEP + VERIFY | Fresh-Naya behavioral acceptance plus real-checkout runtime receipts |
| Index rebuildability | Event index is derived from canonical events by `smart_notes_v3.py` | KEEP + EXTEND | Add benchmark proving rebuild does not alter canonical event truth |
| Retrieval benchmark | Benchmark categories are specified but full runtime proof remains open | BUILD NEW (benchmark only) | Create executable curated benchmark; do not create a new memory system |
| Production runtime proof | Current state records execution-boundary blockers | REPAIR / PROVE | Obtain authorized real-checkout execution and exact-SHA evidence |

## Critical integrity finding

The existing `.naya/memory/RETRIEVAL-MANIFEST.json` currently references `.naya/memory/INDEX.json` and `.naya/memory/notes/`, while the canonical Bootstrap and `smart_notes_v3.py` identify `.naya/memory/events/` and `events/INDEX.json` as the primary memory path. This is a **configuration-consistency defect** that should be repaired before declaring the retrieval architecture airtight.

## What we should NOT build

- a second `NayaNotes` store;
- a second Smart Note/event store;
- a second competing retrieval runtime;
- a separate vector-only memory system;
- an independent Hub-specific brain;
- a visual graph as a substitute for data primitives;
- duplicate copies of events for every semantic category.

## AAA execution sequence

1. Repair manifest/source-path inconsistency.
2. Establish one canonical metadata schema and validation coverage.
3. Add or strengthen scope/permission filtering at retrieval boundaries.
4. Build the executable retrieval benchmark.
5. Run exact/lexical/semantic/relationship/time/lifecycle/permission tests.
6. Run adversarial stale/conflict/supersession/project-isolation cases.
7. Prove summary → detail → primary-source traceability.
8. Prove A→B→C compounding and successor retrieval.
9. Perform fresh-Naya behavioral acceptance.
10. Only then score the Superbrain as runtime-proven AAA.

## Governing principle

> **DO NOT REBUILD THE BRAIN. MAKE THE EXISTING BRAIN COHERENT, COMPLETE, TESTABLE, RETRIEVABLE, PERMISSION-AWARE, TIME-AWARE, AND PROVABLY USEFUL.**

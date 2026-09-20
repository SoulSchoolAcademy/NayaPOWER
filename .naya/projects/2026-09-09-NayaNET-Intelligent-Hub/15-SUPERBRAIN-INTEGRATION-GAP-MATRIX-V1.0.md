# NAYANET SUPERBRAIN — INTEGRATION GAP MATRIX
## Version 1.0

**Purpose:** map the new Superbrain contract against the existing NayaPOWER implementation so we complete one system rather than create competing infrastructure.

| Capability | Current evidence | Decision | AAA requirement |
|---|---|---|---|
| Canonical identity | Stable Note Event IDs and validation exist | KEEP | Extend only for missing object types |
| Time/date | YEAR/MONTH/DAY/HOUR event store and timezone-aware timestamps exist | KEEP + EXTEND | Prove multi-time-field reconstruction |
| Primary memory | `.naya/memory/events/` is canonical | KEEP | No second memory root |
| Smart Notes | `smart_notes_v3.py`, event index, receipts | KEEP + VERIFY | Complete runtime and duplicate/supersession tests |
| Exact search | Exact ID/title/subject matching exists | KEEP | Benchmark |
| Lexical search | BM25/lexical scoring exists | KEEP | Benchmark precision/recall |
| Semantic search | TF-IDF similarity exists | KEEP + EXTEND | Add vectors only if evidence shows benefit |
| Metadata | Project/type/tags/aliases/concepts/status/source/verification fields exist | EXTEND | One validated schema |
| Hierarchy | Chronological store + semantic project/domain model | KEEP + EXTEND | Derived semantic views, no event duplication |
| Relationships | Typed relationships + relationship-aware reranking exist | EXTEND | Stronger graph index and bounded traversal tests |
| Relevance | Exact + lexical + TF-IDF + authority + lifecycle + recency + relationship scoring exists | EXTEND | Add task-intent/scope/permission/temporal evaluation |
| Scope | Project is first-class; privacy/federation laws exist | EXTEND + VERIFY | Adversarial project-isolation tests |
| Permissions | Architecture is documented | EXTEND + VERIFY | Runtime enforcement proof required |
| Provenance | Source/evidence/verification/promotion boundaries exist | KEEP + EXTEND | Source-to-claim benchmark |
| Lifecycle | Active/canonical/historical/superseded/conflicted/stale states exist | KEEP + EXTEND | Verify current-state resolution and archive behavior |
| Conflict handling | Existing conflict/supersession logic exists | EXTEND + VERIFY | Adversarial stale/conflict tests |
| Summarization | CIS/report generation exists | EXTEND | Source-linked progressive summary/detail retrieval |
| Context assembly | Boot + Smart Brain OS define selective loading | KEEP + VERIFY | Prove smallest-sufficient-context behavior |
| Auditability | Git history, metadata, receipts, promotion boundaries | KEEP + EXTEND | Standard material-change audit coverage |
| Outbox | Smart Note sharing architecture defines external delivery boundaries | KEEP + VERIFY | Prove confirmation/retry semantics |
| CIS compounding | Daily/period intelligence architecture exists | KEEP + VERIFY | Complete A→B→C runtime proof |
| Cross-tool continuity | Model-independent restore/continuity contracts exist | KEEP + VERIFY | Fresh-Naya acceptance + real-checkout receipts |
| Index rebuild | Event index is derived from canonical events | KEEP + VERIFY | Prove deterministic rebuild |
| Retrieval benchmark | Test categories specified; full execution remains open | BUILD NEW (benchmark only) | Executable curated benchmark; no new memory system |
| Production proof | Current state records execution-boundary blockers | REPAIR / PROVE | Exact-SHA runtime evidence |

## Critical integrity defect found

`.naya/memory/RETRIEVAL-MANIFEST.json` previously pointed at `.naya/memory/INDEX.json` and `.naya/memory/notes/`, while the canonical Bootstrap and runtime identify `.naya/memory/events/` and `events/INDEX.json` as the primary memory path. The manifest has now been repaired to point to the canonical event store and retrieval runtime.

## Do not build

- another notes/memory store;
- another Smart Note/event store;
- another retrieval runtime;
- a vector-only brain;
- a Hub-specific competing Superbrain;
- duplicate event copies for semantic browsing;
- a visual graph before the underlying primitives are trustworthy.

## AAA execution order

1. Repair/validate canonical metadata consistency.
2. Strengthen scope/permission enforcement at retrieval boundaries.
3. Build and execute the retrieval benchmark.
4. Run exact/lexical/semantic/relationship/time/lifecycle tests.
5. Run adversarial conflict/supersession/project-isolation tests.
6. Prove summary → detail → primary-source traceability.
7. Prove A→B→C compounding and successor retrieval.
8. Perform fresh-Naya behavioral acceptance.
9. Only then claim runtime-proven AAA.

> **DO NOT REBUILD THE BRAIN. MAKE THE EXISTING BRAIN COHERENT, COMPLETE, TESTABLE, RETRIEVABLE, PERMISSION-AWARE, TIME-AWARE, AND PROVABLY USEFUL.**

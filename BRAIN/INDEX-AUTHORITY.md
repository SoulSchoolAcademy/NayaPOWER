# Brain Index Authority Declaration

**Declared:** 2026-10-05 by Naya 4 (captain) under director's grant
**Effective:** immediately
**Review:** challenge on #1354

## Canonical Index

**`BRAIN/REAL-TREE.json`** is the single canonical brain index.

It is byte-accurate (verified 213/213 files at main `82c4a7da` by independent audit).
All brain cleanup, retrieval, and organization work is fixed against this index.

## Subordinate Indexes (derived views, not sources of truth)

| Index | Status | Role |
|---|---|---|
| `BRAIN/NAYAPOWER-BRAIN-INDEX.json` | SUPERSEDED | Empty brain_map and knowledge_ledger. Do not use. |
| `BRAIN/REAL-TREE.md` | DERIVED | Human-readable projection of REAL-TREE.json. |
| `BRAIN/MASTER-MAP.md` | PROPOSED | Awaiting director ratification. Does not override canonical index. |
| `BRAIN/04-INTELLIGENCE/MASTER-INDEX.json` | DERIVED | Area-scoped view. Subordinate to canonical. |
| `BRAIN/03-KERNEL/MANIFEST.json` | DERIVED | Kernel-scoped manifest. Subordinate to canonical. |
| `BRAIN/11-KNOWLEDGE/00-CONCEPT-CORPUS-REGISTER.md` | DERIVED | Knowledge-scoped register. Subordinate to canonical. |
| `BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json` | DERIVED | Runtime-scoped. See also RUNTIME-WIRING.json. |

## Rule

When indexes disagree, REAL-TREE.json wins. A subordinate index that contradicts
the canonical index is wrong — fix the subordinate, never the canonical.

## Change Process

Changing the canonical index requires a captain's decision posted to #1354
with byte-level verification of the replacement. The director may override.

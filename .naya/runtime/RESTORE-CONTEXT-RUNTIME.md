# Naya Power — Restore Context Runtime

**Status:** CANONICAL RUNTIME CAPABILITY  
**Version:** 1.0  
**Purpose:** Reconstruct usable Naya Power context from current repository reality, canonical state, and temporally valid Smart Notes.

## Contract

`restore_context.py` implements the first complete continuity loop:

```text
BOOT
→ LOAD CONSTITUTION / MANIFEST
→ LOAD CURRENT STATE
→ OBSERVE REPOSITORY REALITY
→ VALIDATE MEMORY CONTRACTS
→ APPLY TEMPORAL / SUPERSESSION FILTERS
→ RETRIEVE RELEVANT SMART NOTES
→ SURFACE CONFLICTS / STALE MEMORY
→ SYNTHESIZE CURRENT STATE
→ IDENTIFY NEXT BEST ACTION
```

## Commands

```text
python .naya/runtime/restore_context.py restore
python .naya/runtime/restore_context.py restore "memory continuity"
python .naya/runtime/restore_context.py restore --at "2026-08-23T20:00:00-07:00"
python .naya/runtime/restore_context.py checkpoint
python .naya/runtime/restore_context.py handoff
```

## Truth rules

1. Repository reality is observed from Git when available; it is not inferred from memory.
2. Current verified state outranks historical memory.
3. Superseded and stale notes do not become current truth merely because they are relevant.
4. Historical restore is temporal reconstruction, not a claim that the current repository equals the historical state.
5. Structural validation failure produces `UNKNOWN`, never false `VERIFIED`.
6. The runtime emits machine-readable output so CI and future tooling can consume the same contract.

## Restore modes

- **RESTORE-STANDARD** — current state + repository reality + relevant memory + next action.
- **RESTORE-TIME** — the same reconstruction constrained to a requested timestamp, including the latest Git commit at or before that point.
- **CHECKPOINT** — persist a compact integrity-hashed restore snapshot.
- **HANDOFF** — persist a continuation packet for a fresh execution instance.

## Deliberate boundary

This version intentionally uses deterministic lexical/alias/relationship retrieval already present in the Smart Notes runtime. It does **not** pretend to provide vector retrieval, external model orchestration, or live customer deployment. Those remain explicit future capabilities.

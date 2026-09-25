# NayaPOWER Brain Rehabilitation Receipt — 2026-09-25

**Status:** REPAIRED / VERIFICATION PENDING
**Latest main HEAD at receipt update:** `a9b2c5b5bdea487a0233f9f54c233dd351f3973f`
**Initial repair source HEAD:** `08d961c2e7b8a91f119234f1901f8b6518870dcf`
**Scope:** `.naya/memory/` canonical-memory boundary and related Smart Note / Intelligent Block runtime contracts.

## Executed repairs

1. Removed repository-side IB allocation from `.naya/runtime/smart_note_transaction.py`.
2. Required the live canonical receiver to supply `intelligent_block_id` before canonical Smart Note projection persistence.
3. Removed the local `identity_cursor` projection from the registry writer.
4. Added regression tests for receiver-owned IB identity and memory-surface enforcement.
5. Added machine enforcement against local IB allocation, identity cursors, and legacy IB registry references on the active memory surface.
6. Demoted duplicate project-intelligence Smart Note/IB contract copies to non-authoritative derived projections.
7. Classified the pre-fresh-start archaeology and migration map as historical/non-executable.
8. Classified the in-memory Smart Ledger SmartNote factory as legacy compatibility/test machinery, not canonical durable intelligence.
9. Confirmed cold restore resolves canonical IBs through `.naya/memory/smart-notes/REGISTRY.json` and `smart_notes_v3.retrieve_canonical_ibs(...)`, not legacy note filenames.
10. Aligned `smart_note_enforcement.py` with the canonical HUMAN/CHILD/GRANDMA/NAYA/MACHINE perspective contract; the stale SHAWN/NAYA/MACHINE requirement is removed.

## Source-of-truth findings

- Canonical durable intelligence: Intelligent Block.
- Smart Note: human-readable projection of the canonical IB.
- IB identity: allocated only by live receiver `v7-smart-note-canonical`.
- Canonical repository projection: `.naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md`.
- Canonical registry: `.naya/memory/smart-notes/REGISTRY.json`.
- Event lineage: `.naya/memory/events/`; it is not a competing intelligence store.
- Canonical repository retrieval: `.naya/memory/smart_notes_v3.py::retrieve_canonical_ibs`.
- Cold restore: `.naya/runtime/restore_context.py` imports and calls canonical IB retrieval.
- Current operational truth: `.naya/control-plane/STATE.json`, `BLOCKS.json`, `MAP.json`, `PROOF.json`, `BATON.json`.

## Inventory snapshot

- Active `.naya/memory/` tree: 213 files, including 200+ historical event/compatibility/test artifacts and the canonical Smart Note surface.
- Active `.naya/runtime/` tree: 154 files.
- Canonical active Smart Note registry contains `IB-000001` and `IB-000002`.
- Legacy corpus is quarantined under `.naya/memory/archive/legacy-pre-2026-09-25/`.

## Tests / verification

### Authored
- `.naya/tests/test_smart_note_canonical_resolver.py`
  - receiver-assigned IB is required before persistence;
  - local IB allocator is forbidden.
- `.naya/memory/test_verify_memory_surface.py`
  - active memory cannot reintroduce local IB allocation or a legacy registry;
  - registry must declare live receiver identity authority.

### Repository CI
**NOT EXECUTED against the repaired HEAD in this execution environment.** The connected GitHub surface exposed the workflows and prior run results, but no independent local/Codex execution environment was available and the main-push workflow results for the repaired merge were not observable at receipt time.

Prior run observed before this repair:
- `verify-canonical-ib-retrieval` on prior HEAD `1a3e8dab645df38fd6daa439f9af035b6442953d`: SUCCESS.
- `verify-memory-runtime-focused` on prior HEAD `1a3e8dab645df38fd6daa439f9af035b6442953d`: SUCCESS.

Those prior results do **not** prove the repaired HEAD.

## Remaining contradictions / UNKNOWNs

1. Full executable test suite for the repaired HEAD remains UNKNOWN.
2. Full semantic classification of every one of the 154 runtime files remains UNKNOWN; the canonical restore/retrieval/Smart Note paths and the identified high-risk compatibility modules were inspected.
3. The Smart Note enforcement representation boundary is now aligned to the canonical HUMAN/CHILD/GRANDMA/NAYA/MACHINE contract; executable verification of that repaired HEAD remains UNKNOWN.
4. Production receiver/database registry versus repository registry parity remains UNKNOWN; repository registry is a projection/index, not authority.
5. Positive owner-authenticated production retrieval/deep-link/reload proof for the real production IB remains blocked until the legitimate owner session is available.
6. Behavioral cold-Naya takeover remains UNKNOWN; structural cold-successor proof does not establish independent fresh-LLM behavior.

## Security boundary

No credential, token, impersonation, synthetic authority grant, or private-data bypass was used.

## Next executable action

Run the focused canonical memory/IB tests against current `main` HEAD `a9b2c5b5bdea487a0233f9f54c233dd351f3973f`. If the first failure is in the canonical memory surface, repair only that bounded defect and rerun. If focused tests pass, run the Smart Note enforcement tests and continue the cold-start/retrieval proof without creating another Smart Note format or store.

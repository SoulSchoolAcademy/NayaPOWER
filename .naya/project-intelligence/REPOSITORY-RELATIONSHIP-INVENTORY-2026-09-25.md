# Repository Relationship Inventory - 2026-09-25

## Purpose
Evidence record for surgical consolidation toward the locked AAA NayaPOWER/NayaNET tree.

## Current truth
- Live repository HEAD: `4e04b048042b47ab152c2179c8745a2a5bf8516d` on `main`.
- Canonical Product Tree / Room Matrix / Data Flow is already on `main`.
- Working tree remains intentionally dirty: the GitHub dispatch receipt-revision fix and recent proof/intelligence artifacts are preserved.
- Historical product generations are not treated as canonical merely because they exist locally.

## High-confidence duplicate finding: P8/P9
- `NayaPOWER-P8` contained 2,843 files; `NAYAPOWER/NayaPOWER-P9` contained 2,726 files.
- Every P9 non-generated file had a corresponding repository-root path.
- P9 had 11 paths absent from root: five `.pytest_cache` entries plus six old smart-note verification/test files. Those six are not present in the current root and are therefore identified as stale snapshot-only tests, not silently reclassified as current.
- P8 had 117 extra paths versus P9; inspection showed these were Python/test `__pycache__` artifacts.
- P8/P9 differed on 14 substantive paths. The differences showed P9 carrying newer control-plane/Hub/deep-link state than P8; the repository root is newer again and contains additional current changes absent from P9.
- Conclusion: P8 and P9 were redundant nested working snapshots, not independent canonical implementations.

## Legacy product candidates
- `NAYANET/E01-ULTIMATE-ENTRANCE/` - ARCHIVE per canonical map; 3 historical files; referenced by historical successor/corpus records. Preserve provenance.
- `NAYANET/E01-WELCOME/` - ARCHIVE per canonical map; referenced by Team Naya historical records. Preserve until archive/reference reconciliation.
- `NAYANET/E02-INTELLIGENT-HUB/`, `E02-INTELLIGENT-HUB-AAA/`, `E02-INTELLIGENT-HUB-CLOUDFLARE/`, `E03-INTELLIGENT-HUB/` - historical/alternate Hub generations with live references. No blind deletion.
- `NAYANET/HUB-ROOM-SYSTEM/` - CONSOLIDATE; active room contracts are referenced by tests/handoffs.
- `NAYANET/UNIVERSAL-AGENT-INTERFACE/` - CONSOLIDATE; current release workflows and Smart Door reconciliation depend on it.

## Root scratch
- 158 untracked `_...` files were inventoried. Many contain diagnostics/proof scripts and Smart Note/receipt references; no mass deletion is authorized by evidence yet.
- Generated `node_modules`, `supabase/.temp`, and the remaining `.tmp-wave-browser` are separate disposable candidates; `.tmp-wave-browser` previously had an active file lock.

## Executed mutation
- Removed redundant `NayaPOWER-P8` and `NAYAPOWER/NayaPOWER-P9` nested snapshots.
- Verification immediately after removal: `P8_EXISTS=False`, `P9_EXISTS=False`; HEAD remained `4e04b048042b47ab152c2179c8745a2a5bf8516d`.

## One next action
Reconcile the six stale P8/P9-only smart-note tests and the legacy Hub/room/interface references against the canonical tree, then execute the next highest-confidence consolidation without deleting unique proof or intelligence.
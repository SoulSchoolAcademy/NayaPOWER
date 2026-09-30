# NayaPOWER Brain Reconciliation Ledger — f648833b

**Status:** ACTIVE BASELINE  
**Reconciled:** 2026-09-30  
**Basis main:** `3205327d37a9e040fd830d29f568e2b473651dd0`  
**Purpose:** Declare the machine-verified BRAIN domain classification used by `tools/regenerate_brain_index.py`. This ledger prevents inventory drift from being silently normalized.

## Current classification

| Domain | Files |
|---|---:|
| 00-SPEC | 15 |
| 01-GOVERNANCE | 3 |
| 02-ARCHITECTURE | 5 |
| 03-KERNEL | 27 |
| 04-INTELLIGENCE | 23 |
| 05-MEMORY | 18 |
| 06-PROOF | 10 |
| 07-LEARNING | 2 |
| 08-SUCCESSION | 2 |
| 09-EVOLUTION | 2 |
| 10-INTERFACES | 5 |
| 11-KNOWLEDGE | 7 |
| 12-ENGINEERING | 23 |
| 90-OPERATIONS | 10 |
| 99-ARCHIVE | 1 |
| ROOT | 5 |
| **TOTAL** | **158** |

## Reconciliation note

The 90-OPERATIONS count is **10** because the durable `0005-LIVE-NAYA-MASTER-BATON-2026-09-30.md` was intentionally added as the portable cold-successor operating baton. The change is structural and therefore must be reflected in the declared classification rather than ignored by the generator.

The ledger is a classification baseline, not a semantic authority source. It does not promote proof state, authority, or production status. Live evidence and constitutional governance remain authoritative.

**Invariant:** a real BRAIN file addition/removal/edit that changes the inventory must cause regeneration to fail until the classification is deliberately reconciled.

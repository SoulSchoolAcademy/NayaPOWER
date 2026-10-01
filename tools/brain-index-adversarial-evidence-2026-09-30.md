# Brain index generator — adversarial self-test evidence

**Date:** 2026-09-30
**Generator:** `tools/regenerate_brain_index.py` (with pointer-integrity validation)
**Test script:** `tools/test_brain_index_adversarial.sh`
**Basis:** scratch clones of main at `0567ee0` — nothing here touched the real working tree.

```
### CASE 0: positive control — clean tree must pass
PASS: clean tree --check exits 0
OK: index layer matches git tree (157 files)
---
### CASE A: dangling pointer in MASTER-INDEX.json must fail exit 2
error: pointer integrity check failed:
  dangling pointer (declared): BRAIN/04-INTELLIGENCE/MASTER-INDEX.json field 'object_contract' -> 'BRAIN/04-INTELLIGENCE/0001-DOES-NOT-EXIST-V1.md' (not in git tree at HEAD)
A dangling pointer in the index layer fails the run — fix the pointer, do not force.
PASS: dangling pointer fails exit 2 naming file+field+target
---
PASS: dangling pointer fails --check with exit 2
---
### CASE B: skewed domain count must fail exit 2
error: domain counts do not match the reconciliation ledger table:
  git:    {'00-SPEC': 15, '01-GOVERNANCE': 3, '02-ARCHITECTURE': 5, '03-KERNEL': 27, '04-INTELLIGENCE': 23, '05-MEMORY': 18, '06-PROOF': 10, '07-LEARNING': 2, '08-SUCCESSION': 2, '09-EVOLUTION': 2, '10-INTERFACES': 5, '11-KNOWLEDGE': 7, '12-ENGINEERING': 23, '90-OPERATIONS': 9, 'ROOT': 5}
  ledger: {'00-SPEC': 15, '01-GOVERNANCE': 3, '02-ARCHITECTURE': 5, '03-KERNEL': 27, '04-INTELLIGENCE': 23, '05-MEMORY': 18, '06-PROOF': 10, '07-LEARNING': 2, '08-SUCCESSION': 2, '09-EVOLUTION': 2, '10-INTERFACES': 5, '11-KNOWLEDGE': 7, '12-ENGINEERING': 23, '90-OPERATIONS': 9, '99-ARCHIVE': 1, 'ROOT': 5}
A real BRAIN/ change landed — update EXPECTED_DOMAIN_COUNTS deliberately, do not force.
PASS: count skew fails exit 2 with count message
---
### CASE C: undeclared new pointer field must fail via backstop scan
error: pointer integrity check failed:
  dangling pointer (backstop scan): BRAIN/NAYAPOWER-BRAIN-INDEX.json field 'some_future_pointer' -> 'BRAIN/12-ENGINEERING/9999-NOT-HERE-V1.md' (not in git tree at HEAD)
A dangling pointer in the index layer fails the run — fix the pointer, do not force.
PASS: undeclared pointer fails exit 2 via backstop scan
---
=== RESULT: 5 passed, 0 failed ===
```

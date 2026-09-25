# Canonical Memory Enforcement Repair — 2026-09-25

## Purpose

Record the first causal repair after the canonical Smart Note organization failure was identified.

## Defect reproduced

The canonical-memory auditor introduced on 2026-09-25 contained two defects:

1. It extracted the IB identity from the wrong path segment. For
   `.naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md`
   the IB is path segment index 8, not 9.
2. It treated historical Smart Note projections under
   `.naya/memory/archive/` as active canonical violations.

The first defect made a valid canonical projection fail its own validation. The second made legitimate historical memory fail the active-memory audit.

## Repair

- Corrected IB path extraction from segment 9 to segment 8.
- Explicitly exempted the historical archive boundary from active canonical-projection enforcement.
- Tightened the outside-root Smart Note signature so ordinary documentation is not mistaken for a canonical Smart Note merely because it mentions Smart Note headings.
- Added regression coverage for canonical identity/path correctness and archive classification.

## Evidence

Test changes committed first:
- `912721f35cd4d5f5c0e511d3229301e0b1c2d8db`
- `db5038c748192860c8edd6c995514efa25252cb8`

Implementation repair:
- `029483d281cc3a0469fa67f33cfa61a69c479c40`

Canonical auditor:
`.naya/runtime/canonical_memory_organization.py`

Regression tests:
`.naya/tests/test_canonical_memory_organization.py`

CI:
`.github/workflows/verify-canonical-intelligence-organization.yml`

## Truth state

**IMPLEMENTED — verification pending.**

The connected GitHub status surface currently reports no commit statuses for the repair commit. Therefore this record does not claim CI PASS.

## Architectural lesson

A written rule is insufficient when a validator can contradict the rule it is meant to enforce.

The canonical memory boundary must itself be correct, tested, and fail-closed.

## Remaining P0

Do not create a repository Smart Note for a new lesson until the live canonical receiver has issued the immutable IB identity.

Next causal boundary:

**real meaningful lesson → live receiver → receiver-issued IB → canonical persistence → index → projection → retrieval → verification**

No local IB allocation. No GitHub-documentation substitution for runtime intelligence.

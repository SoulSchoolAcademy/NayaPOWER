# Proof Contract V1

**Status:** CANONICAL BUILD CONTRACT

## Purpose
Separate what exists from what has been independently demonstrated.

## Evidence states
`UNKNOWN → EXERCISED → VERIFIED → PRODUCTION_PROVEN`

These states are not interchangeable.

## Required proof receipt
`claim_id, subject_id, test_id, environment, source_revision, actor, inputs, expected_result, observed_result, evidence_refs[], verifier, verdict, timestamp`.

## Laws
- Documentation is not behavioral proof.
- A harness is not proof unless it exercises the real declared boundary.
- VERIFIED requires evidence sufficient for the declared scope.
- PRODUCTION_PROVEN requires current production/browser/runtime evidence.
- Conflicting or missing evidence yields UNKNOWN/BLOCKED, never PASS.

## Acceptance
Every critical race gate maps to a current receipt and an independent verification step.

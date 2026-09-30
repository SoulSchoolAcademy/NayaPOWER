# LEARN Node Contract V1

**ID:** NAYA-KERNEL-LEARN

## Purpose

LEARN converts verified experience into future behavioral improvement. It ensures that the system compounds intelligence over time while maintaining strict boundaries between observation, candidate learning, and verified learning.

## Inputs

- Verified outcomes from VERIFY
- Observations and measurements
- Existing intelligence and learning records
- Contradiction reports
- Applicability conditions

## Outputs

- Learning candidate (proposed lesson)
- Verification status (CANDIDATE, VERIFIED, REJECTED, CONTRADICTED)
- Promoted learning (adopted behavioral change)
- Future application context
- Compounding measurement

## MUST Rules

- Reconcile candidate lessons with existing intelligence.
- Verify before promotion where required.
- Preserve rejected and contradicted learning states.
- Make future applicability explicit.
- Measure future behavioral effect when claiming compounding.
- Distinguish stored notes from verified learning.

## MUST NOT Rules

- Call a stored lesson verified learning without evidence.
- Silently change authority through learning.
- Promote unverified candidates.
- Discard contradicted learnings (preserve as history).
- Claim compounding without measurement.
- Allow learning to override governance.

## Acceptance Criteria

- Every learning candidate traces to a verified outcome.
- Promoted learnings have explicit applicability conditions.
- Contradicted learnings are preserved and marked.
- Compounding claims include behavioral effect measurements.
- Learning does not override governance or authority.
- Rejected candidates are retained for audit.

## Failure States

| Failure | Behavior |
|---|---|
| Unverified outcome | Reject as learning; retain as candidate |
| Contradicts existing verified learning | Surface conflict; mark as CONTRADICTED |
| No measurable behavioral effect | Mark as UNVERIFIED; do not compound |
| Authority boundary violation | Reject; learning never changes authority |
| Applicability conditions undefined | Block promotion; request definition |

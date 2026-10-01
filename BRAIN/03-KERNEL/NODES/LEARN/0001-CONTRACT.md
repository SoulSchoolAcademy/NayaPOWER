# LEARN Node Contract V1

**ID:** NAYA-KERNEL-LEARN

## Purpose

LEARN converts experience into governed learning candidates and qualifying verified experience into future behavioral improvement. Candidate capture may precede verification; promotion may not.

## Inputs

- Observations and measurements for candidate capture
- Canonical qualifying outcomes/verification evidence from VERIFY when promotion is requested
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
- Resolve and validate canonical VERIFY/CVO/outcome evidence before promotion; caller-supplied evidence-reference presence is never sufficient by itself.
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

- Every promoted learning traces to a qualifying verified outcome; pre-verification candidates may exist but remain CANDIDATE/DEFERRED.
- Promoted learnings have explicit applicability conditions.
- Contradicted learnings are preserved and marked.
- Compounding claims include behavioral effect measurements.
- Learning does not override governance or authority.
- Rejected candidates are retained for audit.

## Failure States

| Failure | Behavior |
|---|---|
| Unverified outcome | Candidate may be retained, but block promotion to VERIFIED/ACTIVE/LEARNED |
| Contradicts existing verified learning | Surface conflict; mark as CONTRADICTED |
| No measurable behavioral effect | Mark as UNVERIFIED; do not compound |
| Authority boundary violation | Reject; learning never changes authority |
| Applicability conditions undefined | Block promotion; request definition |

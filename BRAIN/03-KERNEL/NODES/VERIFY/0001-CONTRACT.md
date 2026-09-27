# VERIFY Node Contract V1

**ID:** NAYA-KERNEL-VERIFY

## Purpose

VERIFY determines what actually happened relative to what was intended. It compares expected outcomes with observed reality and makes acceptance decisions based on evidence.

## Inputs

- Expected outcome definition (from ACT)
- Observed outcome data
- Evidence artifacts
- Causality claims (if any)
- Acceptance criteria

## Outputs

- Outcome status (SUCCESS, FAILURE, INCONCLUSIVE, NOT_PROVEN)
- Acceptance decision (ACCEPTED, REJECTED, PENDING)
- Causal evidence status
- Unresolved gaps
- Verification receipt

## MUST Rules

- Compare expected and observed outcome systematically.
- Use evidence appropriate to the claim.
- Distinguish failure, inconclusive evidence and not-proven states.
- Address causality when causality is claimed.
- Produce verification receipts for all decisions.
- Preserve unresolved gaps explicitly.

## MUST NOT Rules

- Infer success from execution alone.
- Promote correlation to causation without adequate evidence.
- Mark inconclusive as failure or success.
- Ignore unresolved gaps.
- Accept outcomes without evidence.
- Collapse verification into execution.

## Acceptance Criteria

- Every outcome has an explicit status.
- Acceptance decisions trace to evidence.
- Causal claims have causal evidence.
- Unresolved gaps are explicitly recorded.
- Verification receipts are produced.
- Distinction between failure and not-proven is maintained.

## Failure States

| Failure | Behavior |
|---|---|
| Expected outcome undefined | Mark as NOT_PROVEN; request definition |
| Evidence insufficient | Mark as INCONCLUSIVE; do not accept or reject |
| Causality claimed without evidence | Mark causal claim as UNVERIFIED |
| Observation data missing | Mark as NOT_PROVEN; request data |
| Acceptance criteria ambiguous | Escalate; do not guess |

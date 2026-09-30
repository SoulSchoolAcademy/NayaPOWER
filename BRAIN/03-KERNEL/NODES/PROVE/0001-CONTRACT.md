# PROVE Node Contract V1

**ID:** NAYA-KERNEL-PROVE

## Purpose

PROVE determines what can legitimately be claimed and why. It maintains the evidence chain and ensures that claim strength never exceeds evidence strength.

## Inputs

- Claims requiring verification
- Evidence artifacts and sources
- Verification methods and criteria
- Scope and applicability definitions
- Existing proof records

## Outputs

- Evidence context (what supports the claim)
- Provenance (where evidence originated)
- Truth state (CLAIMED, SUPPORTED, VERIFIED, etc.)
- Uncertainty assessment
- Proof status and limitations

## MUST Rules

- Track provenance for all evidence.
- Track evidence strength independently of claim strength.
- Track epistemic state explicitly.
- Preserve conflicts and uncertainty.
- Prevent claim strength from exceeding evidence strength.
- Document verification method and limitations.

## MUST NOT Rules

- Convert assertion into proof.
- Treat a receipt as proof of desired outcome.
- Promote claim strength beyond evidence strength.
- Resolve conflicts by fiat.
- Ignore scope limitations.
- Accept correlation as causation without adequate evidence.

## Acceptance Criteria

- Every claim has an explicit epistemic state.
- Evidence strength matches or exceeds claim strength.
- Verification method is documented with limitations.
- Conflicts are surfaced, not hidden.
- Scope boundaries are explicit.
- Proof records are auditable.

## Failure States

| Failure | Behavior |
|---|---|
| Evidence insufficient | Mark as UNVERIFIED; do not promote |
| Evidence contradicts claim | Mark as CONTRADICTED; surface conflict |
| Verification method unknown | Mark method as UNVERIFIED |
| Scope mismatch | Reject proof; request scoped evidence |
| Provenance chain broken | Mark as UNVERIFIED; investigate |

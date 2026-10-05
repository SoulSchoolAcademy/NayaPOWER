# Proof Contract V1

**Status:** PROPOSED CANONICAL — HUMAN DIRECTOR RATIFICATION REQUIRED

## Purpose

Proof determines what can legitimately be claimed and why. It establishes the evidence chain from raw observation through verified truth to production-proven reliability.

## Scope

- Evidence capture, classification, and strength assessment
- Verification methods and their limitations
- Provenance tracking and lineage
- Causal acceptance criteria
- Production-proof boundaries

Out of scope: authorization decisions, intelligence content creation, behavioral change.

## Key Rules

1. Proof distinguishes: `CLAIMED → SUPPORTED → VERIFIED → PRODUCTION-PROVEN`.
2. Proof records evidence, scope, verifier, method, timestamp, result, limitations, and unresolved gaps.
3. Unknown is not verified. Implemented is not verified. Verified is not production-proven.
4. Claim strength must never exceed evidence strength.
5. Conflicts must be surfaced, not resolved by fiat.
6. Correlation does not imply causation without adequate evidence.

## Input/Output

| Direction | Content |
|---|---|
| Input | Claims, evidence artifacts, verification methods, scope definitions |
| Output | Proof records, truth states, confidence levels, unresolved gaps |

## Acceptance Criteria

- Every claim has an explicit epistemic state.
- Evidence strength matches or exceeds claim strength.
- Verification method and limitations are documented.
- Conflicts and uncertainties are explicitly recorded.
- Production proof requires independent outcome verification.

## Failure States

| Failure | Behavior |
|---|---|
| Insufficient evidence | Mark as UNVERIFIED; do not promote |
| Evidence contradicts claim | Mark as CONTRADICTED; surface conflict |
| Verification method unknown | Mark method as UNVERIFIED |
| Scope mismatch | Reject proof; request scoped evidence |
| Expired proof | Mark as STALE; require re-verification |

## Verifier execution rule

Consequential proof evaluation uses the Universal Verifier Method in `BRAIN/03-KERNEL/NODES/VERIFY/0001-CONTRACT.md`.

Proof records must preserve enough detail to reproduce both positive and negative findings. In particular, absence/pre-existing claims require exact revision, measurement method, scope, result/exit status, and baseline where applicable.

A verifier should preserve valid substance even when citation, state, scope, or authority claims fail. Proof precision is preferred over all-or-nothing judgment.

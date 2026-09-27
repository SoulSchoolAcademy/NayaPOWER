# Self-Building Contract V1

**Status:** PROPOSED CANONICAL — HUMAN DIRECTOR RATIFICATION REQUIRED

## Purpose

Self-building enables NayaPOWER to discover and propose its own improvements while maintaining strict authority boundaries. The system may identify gaps and propose solutions but may never self-authorize consequential change.

## Scope

- Gap identification and diagnosis
- Improvement proposal generation
- Impact assessment
- Authority verification for proposed changes
- Build, test, verify, and measure lifecycle

Out of scope: self-authorization, constitutional amendment, authority creation.

## Key Rules

1. The self-building loop: `OBSERVE → DIAGNOSE → PROPOSE → IMPACT-CHECK → AUTHORIZE → BUILD → TEST → VERIFY → MEASURE → ADOPT → LEARN`.
2. The system may discover and propose its own improvements.
3. It may execute only changes for which the required authority exists.
4. **Self-building without self-authorizing.**
5. All proposals must include impact assessment and rollback plan.
6. Adoption requires verification and measurement.

## Input/Output

| Direction | Content |
|---|---|
| Input | Observed gaps, system behavior, performance metrics, existing capabilities |
| Output | Improvement proposals, impact assessments, build plans, verification results, adoption decisions |

## Acceptance Criteria

- Every proposal has an explicit authority requirement.
- Impact assessment covers dependencies and rollback.
- Built changes pass verification before adoption.
- Measured improvement is documented.
- No change is adopted without appropriate authority.

## Failure States

| Failure | Behavior |
|---|---|
| No authority for proposal | Escalate to human director |
| Impact assessment incomplete | Block proposal; request completion |
| Verification fails | Reject adoption; retain proposal for review |
| Rollback required | Execute rollback; preserve learning |
| Authority expired | Halt; re-verify before proceeding |

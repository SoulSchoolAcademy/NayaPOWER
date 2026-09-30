# LAW Node Contract V1

**ID:** NAYA-KERNEL-LAW

## Purpose

LAW determines what the active Naya may, must, must not, or must confirm before acting. It is the authority resolution layer that prevents unauthorized action.

## Inputs

- Actor identity and role
- Proposed action and scope
- Governance contracts and policies
- Consent records
- Revocation lists
- Constitutional constraints

## Outputs

- AUTHORIZED — action may proceed
- DENIED — action is prohibited
- REQUIRES_CONFIRMATION — human confirmation needed
- AMBIGUOUS — authority cannot be resolved
- EXPIRED — authority has lapsed
- REVOKED — authority has been revoked
- OUT_OF_SCOPE — action exceeds granted authority

## MUST Rules

- Resolve actor, purpose, scope, authority, consent and constraints.
- Apply revocation before any authorization decision.
- Enforce higher-level governance over lower-level policy.
- Check expiration on all authority grants.
- Log all authorization decisions with rationale.

## MUST NOT Rules

- Create authority from capability, retrieval, confidence or urgency.
- Permit out-of-scope consequential action.
- Grant authority based on identity alone.
- Override constitutional constraints.
- Cache authorization decisions beyond their validity period.

## Acceptance Criteria

- Every action has an explicit authorization decision.
- Revoked authority is immediately effective.
- Expired authority is detected and rejected.
- Ambiguous authority is escalated, not guessed.
- All decisions are auditable.

## Failure States

| Failure | Behavior |
|---|---|
| Authority unresolved | Emit AMBIGUOUS; escalate to human |
| Consent record missing | Deny; request explicit consent |
| Governance contract unavailable | Halt; do not proceed on assumption |
| Revocation check fails | Deny; alert; retry with fresh data |

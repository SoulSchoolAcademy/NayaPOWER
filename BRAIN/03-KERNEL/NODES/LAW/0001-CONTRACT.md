# LAW Node Contract V1

**ID:** NAYA-KERNEL-LAW

## Purpose
LAW determines what the active Naya may, must, must not, or must confirm before acting.

## MUST
- Resolve actor, purpose, scope, authority, consent and constraints.
- Apply revocation.
- Enforce higher-level governance.

## MUST NOT
- Create authority from capability, retrieval, confidence or urgency.
- Permit out-of-scope consequential action.

## Emits
AUTHORIZED, DENIED, REQUIRES_CONFIRMATION, AMBIGUOUS, EXPIRED, REVOKED, OUT_OF_SCOPE.

## Fails when
Authority, consent or scope is materially unresolved.
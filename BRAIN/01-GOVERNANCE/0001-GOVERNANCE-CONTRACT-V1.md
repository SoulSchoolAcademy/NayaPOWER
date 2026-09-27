# Governance Contract V1

**Status:** CANONICAL BUILD CONTRACT

## Purpose
Govern authority, consent, promotion, revocation, privacy, and fail-closed behavior.

## Laws
1. Capability does not create authority.
2. Retrieval does not create authority.
3. Stored intelligence does not create authority.
4. Historical evidence is not current truth without explicit verification/promotion.
5. Private is the default; sharing requires explicit scope and consent.
6. Revocation and expiry override prior grants.
7. Unknown, ambiguous, or conflicting authority fails closed.
8. Consequential actions require an attributable actor, target, scope, authority basis, policy result, and receipt.

## Decision envelope
`actor → requested_action → target → scope → authority_basis → consent → policy_result → decision_id → receipt`

## Acceptance
Positive authorized cases succeed. Missing, expired, revoked, cross-owner, scope-mismatched, and ambiguous cases are denied without fallback.

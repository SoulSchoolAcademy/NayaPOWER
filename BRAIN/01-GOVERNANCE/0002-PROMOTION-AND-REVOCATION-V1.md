# Promotion & Revocation V1

**Status:** CANONICAL BUILD CONTRACT

## Promotion
`CANDIDATE → VERIFIED → PROMOTED`

Promotion requires declared evidence, verification reference, owner/scope, provenance, version, acceptance criteria, and authority. UNKNOWN is never promoted.

## Revocation
`PROMOTED → REVOKED` removes eligibility for active use while preserving historical lineage. Reinstatement requires a new version and explicit promotion.

## Receipt
`object_id, prior_state, new_state, actor, authority_basis, evidence_refs[], verification_ref, timestamp, reason`.

## Fail-closed
Missing evidence, authority, scope, provenance, verification, or unresolved contradiction blocks transition.

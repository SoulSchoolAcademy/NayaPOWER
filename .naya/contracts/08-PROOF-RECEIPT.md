# Contract 08 — Proof / Receipt V1

**Owns:** evidence semantics, receipts, and verification claims.  
**Does not own:** creating the underlying intelligence or granting authority.

## Proof chain

**REQUEST → AUTHORIZATION → EXECUTION → PERSISTENCE → RECEIPT → RETRIEVAL → VERIFICATION**

A missing boundary remains missing in the claim.

## Truth states

The system MUST distinguish: CLAIMED / OBSERVED / IMPLEMENTED / TESTED / VERIFIED / PRODUCTION-PROVEN / UNKNOWN / BLOCKED / PENDING / CONFLICTED.

No state may be promoted by wording alone.

## Receipt minimum

A consequential receipt SHOULD identify request, actor, authority/scope, source/target, action, relevant IDs, timestamp, version/ref where applicable, observed result, success criterion, verification method, evidence references, unknowns, and recovery/next action if failed.

## Evidence rule

**Reasoned → Untested → Tested → Verified → Production-safe/proven**

The evidence determines the tier.

## Causal verification

Correlation MUST NOT be called causation. Causal claims require an explicit causal-evidence boundary appropriate to the claim.

## Failure

The first deterministic failure MUST be preserved. A later success cannot erase a failed prerequisite.

## Acceptance

- Untested implementation cannot be reported verified.
- Workflow success cannot be reported runtime success without runtime evidence when runtime is the boundary.
- Verified repository artifact cannot be called production-proven without production evidence.
- Failed dependent step cannot yield false overall PASS.
- Unsupported causal claim remains unproven.
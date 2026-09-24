# NayaNET compound-intelligence v35 -> v36 portable authorization patch

Status: NON-PRODUCTION SPECIFICATION ONLY
Production Edge Function inspected: nayanet-compound-intelligence
Production version: 35
Production source SHA-256: 77940b934c2f1f0b8249c97b73f63ed782631407e62e81194813be6960d489cd

## Exact v35 execution seam

1. POST body enters Deno.serve.
2. Non-exempt action reaches commitIntelligence().
3. commitIntelligence() calls requireGovernedIntelligenceAuthorization().
4. That function validates the ordinary ExecutionAuthorization and live authority grant.
5. commitIntelligence() then calls record(..., executionAuthorization).
6. record() calls the existing nayanet_record_cognition_event RPC with p_execution_authorization.
7. The RPC persists the existing receipt/evidence path.

## v36 minimum change

Do not add an authority issuer. Do not replace the RPC. Do not add a receipt table.

Before the existing record() call for INTELLIGENCE_COMMIT:

- require body.portable_authorization to be an object;
- require body.portable_authorization_artifact_hash;
- recompute SHA-256 over the exact canonical serialized portable artifact;
- require the supplied hash to match;
- verify the portable artifact signature with the configured issuer public key;
- resolve the artifact authority_id through the existing nayanet_validate_authority_grant RPC;
- require the resolved subject_id to equal the authenticated user;
- require artifact action_type=INTELLIGENCE_COMMIT;
- require artifact permission=intelligence_commit;
- require artifact target=NayaNET;
- require artifact repository=SoulSchoolAcademy/NayaPOWER;
- require artifact commit_sha to equal the source SHA supplied to this execution;
- require the ordinary execution_authorization fields to equal the signed artifact authorization fields;
- only after every check passes, call the existing record() function.

The record() call must receive the exact artifact and artifact hash in receipt evidence, while preserving p_execution_authorization unchanged.

## Required receipt evidence

The existing JSONB evidence object is extended in-place:

{
  ...existingEvidence,
  "portable_authorization": <exact request artifact>,
  "portable_authorization_artifact_hash": <verified SHA-256>
}

No schema/table migration is required.

## Fail-closed rule

Any missing, malformed, unsigned, wrongly signed, expired, revoked, hash-mismatched, authority-mismatched, actor-mismatched, decision-mismatched, action-mismatched, target-mismatched, permission-mismatched, repository-mismatched, or source-SHA-mismatched artifact MUST stop before nayanet_record_cognition_event is invoked.

## Important trust-root boundary

v36 still needs a durable issuer public-key trust root. An ephemeral workflow-generated key is suitable only for non-production testing and MUST NOT be treated as the production trust root.

## Non-production proof requirement

The v36 candidate must prove:
request -> portable artifact hash -> signature verification -> existing authority validation -> ordinary authorization binding -> existing record() -> receipt evidence artifact/hash

No production deployment or live intelligence_commit is part of this patch.

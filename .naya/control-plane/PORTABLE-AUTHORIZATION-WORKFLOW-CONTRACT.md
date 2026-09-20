# Portable-Authorization Workflow Contract (NAYA POWER Test #12)

STATUS: CONTRACT ONLY — NOT WIRED. No production workflow may deploy, mutate,
dispatch, or push simply because the file below exists. This document does not
create authority and never will.

AUTHORITY LAW: capability does not create authority. A workflow token
(`GITHUB_TOKEN`, `CLOUDFLARE_API_TOKEN`, `VERCEL_TOKEN`), repository write
permission, `workflow_dispatch`, push triggers, the string `RELEASE_CANONICAL_HUB`,
release/decision/action IDs, claims, and receipts provide capability ONLY. The
ONE authority source remains:

    UniversalExecutionGate -> canonical registry -> canonical governance
    kernel -> gate-issued ExecutionAuthorization -> portable artifact.

## The future workflow MUST do everything below BEFORE any side effect

"Side effect" includes: `git push`, `wrangler deploy`, `vercel deploy`, a
GitHub release mutation, or any other consequential action. If any step fails
or is skipped, the job MUST exit non-zero without executing the side effect.

1. RECEIVE the portable authorization.
   The artifact arrives as a workflow_dispatch input / build artifact / secure
   out-of-band transfer. Its schema MUST be `naya/portable_authorization/v1`.

2. VERIFY PROVENANCE.
   Ed25519-verify the artifact signature against the PINNED public key found in
   the repository (`.naya/runtime/portable-authorization-public-key.hex`).
   A workflow token, input string, or "authorized_by" field is NEVER a
   substitute for this step.

3. VERIFY BINDING.
   Recompute `_execution_binding_hash(authority_id, decision_id, action_id,
   action_type, target, actor_id, scope, permission)` and require it to equal
   the artifact's `binding_hash`.

4. VERIFY EXPIRY.
   Require `issued_at <= now < expires_at`, `validated_at == issued_at`, and the
   artifact TTL <= the configured maximum.

5. VERIFY REVOCATION / CURRENT AUTHORITY.
   Re-read `.naya/governance/authority-registry.json` from the canonical branch;
   require the authority_id to be present, its grant fingerprint to equal the
   artifact's `authority_fingerprint`, and `permits(actor, permission, scope, now)`
   to hold (covers revoked / expired / modified grants).

6. VERIFY REPOSITORY.
   Require artifact `repository == well-known repository` AND the artifact
   `target` to begin with the same repository binding.

7. VERIFY COMMIT.
   For deployments, require artifact `commit_sha == the exact commit being
   deployed` AND the checkout to be at that commit.

8. VERIFY TARGET.
   Require `artifact.target == deploy_target(...)/repo_mutation_target(...)`
   computed from the workflow's intended action, byte-for-byte.

9. VERIFY ENVIRONMENT.
   `target_environment` MUST be `preview` or `production` and MUST equal the
   artifact's `environment`.

10. VERIFY EXACT MUTATION/DEPLOYMENT SCOPE.
    For mutations, artifact `change_set` MUST equal the exact path set the job
    is allowed to touch; the job MUST reject anything outside it.

11. ENTER THE EXECUTION BOUNDARY.
    Run `portable_boundary_release(...)` or `portable_boundary_repo_mutation(...)`
    from `.naya/runtime/portable_authorization.py`; require `allowed == True`.

12. ONLY THEN PERMIT THE SIDE EFFECT.
    The side effect executes strictly under `permissions: contents: read` plus
    the single scoped secret that the *specific* action needs, and only for the
    artifact-bound target.

## Invariants

- The runner holds ONLY the pinned public key. It can verify; it can never sign.
- No step may be skipped because "the token is present" or "it was approved".
- Replay is bounded by expiry + exact-target binding; any reuse for a different
  action/target/environment/repository/worker/commit/change-set is REFUSED.
- If the registry cannot be loaded, the job fails closed.
- If the pinned public key is absent, the job fails closed.
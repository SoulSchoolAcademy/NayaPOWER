# NAYAPOWER TORCH 63 — EXECUTION BRIDGE

**Status:** IMPLEMENTED / CREDENTIAL-GATED / DISPATCH NOT YET PROVEN
**Date:** 2026-09-12
**Repository:** SoulSchoolAcademy/NayaPOWER
**Branch:** main
**Latest source commit:** `ea06d56d375e8ac03a22a28d5ae2fd7ed418b98e`

## Mission

Remove the external execution bottleneck between Naya and the canonical NayaNET Hub deployment workflow without bypassing governance, source binding, or independent verification.

## Exact architecture

`NAYA → AUTHORIZED SUPABASE EDGE FUNCTION → GITHUB WORKFLOW_DISPATCH → CANONICAL WORKFLOW → BUILD → CLOUDFLARE → PUBLIC RUNTIME → INDEPENDENT VERIFICATION → SUPABASE EXECUTION RECEIPT → DIRECT ACTIVITY FEED → NAYA`

## What was actually done

1. Inspected current Supabase Edge Functions rather than assuming the previously observed historical function list was still current.
2. Confirmed the current project exposes four functions; no existing GitHub-dispatch bridge was present in the current active list.
3. Created server-side Edge Function `nayanet-github-dispatch` with JWT verification enabled.
4. Implemented exact SHA validation, explicit approval validation, deployment reason validation, authenticated-user binding, idempotency lookup, GitHub ref/commit preflight, canonical `workflow_dispatch`, and durable execution receipt writing.
5. Added the bridge source to the repository under `NAYANET/EXECUTION-BRIDGE/nayanet-github-dispatch/`.
6. Deployed bridge version 2 to Supabase after correcting the import-map deployment configuration.

## Protected boundaries

- Canonical Hub deployment remains `.github/workflows/deploy-nayanet-hub-canonical-v2.yml`.
- The bridge does not build or deploy the Hub itself.
- The bridge does not write the Activity Feed through GitHub Actions.
- No public runtime mutation is performed merely by creating the bridge.
- GitHub credentials are never logged or written to repository source.
- No deployment receipt is claimed until GitHub accepts dispatch and downstream runtime verification provides evidence.

## Credential boundary

The bridge currently supports a server-side `GITHUB_TOKEN` or `GITHUB_ACTIONS_TOKEN`. The secret value is intentionally not observable through the available management surface.

If neither exists at runtime, the bridge records a BLOCKED execution receipt with:

`GITHUB_DISPATCH_CREDENTIAL_NOT_OBSERVABLE`

This is an intentional fail-closed state, not a deployment failure.

## Current evidence

- Supabase function `nayanet-github-dispatch` exists and is ACTIVE at version 2.
- Repository source exists at the canonical bridge path.
- Current repository source commit is `ea06d56d375e8ac03a22a28d5ae2fd7ed418b98e`.
- The canonical workflow requires exact 40-character SHA, explicit approval, governance-kernel authorization, build checks, Cloudflare deployment, explicit 100% promotion, and independent public-runtime verification.
- No real canonical Hub deployment was dispatched by this torch.
- No false deployment receipt was created.

## Remaining blocker

**P0 — CREDENTIAL + INVOCATION PROOF**

The next execution must:

1. establish that the server-side GitHub dispatch credential is actually available to the bridge;
2. invoke the bridge with the exact current main SHA, explicit approval, and a unique idempotency key;
3. observe the resulting GitHub workflow run;
4. prove build → Cloudflare → 100% promotion → public runtime → runtime source SHA/assets/markers;
5. persist the final execution receipt;
6. write the corresponding Activity Feed event directly through the operational system;
7. return the verified result to Naya;
8. create the single next execution action.

If the credential is unavailable, do not fake progress. Record the exact blocked boundary and continue by solving the credential/invocation boundary rather than redesigning the deployment system.

## Next action

**Activate and prove the server-side GitHub dispatch boundary for `nayanet-github-dispatch`, then execute one real canonical Hub deployment against the exact current `main` SHA.**

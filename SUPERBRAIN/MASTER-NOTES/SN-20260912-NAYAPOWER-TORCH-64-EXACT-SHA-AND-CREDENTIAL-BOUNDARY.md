# NAYAPOWER TORCH 64 — EXACT-SHA BINDING + CREDENTIAL BOUNDARY

**Status:** EXACT-SHA HARDENED / BRIDGE ACTIVE / CREDENTIAL EXTERNAL
**Date:** 2026-09-12
**Repository:** SoulSchoolAcademy/NayaPOWER
**Branch:** main
**Current HEAD at handoff:** `867f4399be3e4c5fb6d7d75fafd82fc0225d464e`
**Supabase function:** `nayanet-github-dispatch`
**Supabase function version:** 3
**Bridge source commit:** `c51af7c7bc56f0c47feedde3cc806327ab84cfcc`

## Mission

Complete the execution path:

`NAYA → AUTHORIZED SUPABASE EDGE FUNCTION → GITHUB WORKFLOW_DISPATCH → CANONICAL WORKFLOW → BUILD → CLOUDFLARE → PUBLIC RUNTIME → INDEPENDENT VERIFICATION → SUPABASE EXECUTION RECEIPT → DIRECT ACTIVITY FEED → NAYA`

## Torch 64 execution

### Completed

1. Re-read the live bridge source instead of relying on prior summaries.
2. Hardened the bridge so the requested deployment SHA must equal the exact current `main` branch tip before GitHub workflow dispatch.
3. Added fail-closed receipt/error handling for:
   - `CURRENT_MAIN_SHA_NOT_OBSERVABLE`
   - `REQUESTED_SHA_NOT_CURRENT_MAIN`
4. Redeployed `nayanet-github-dispatch` successfully as Supabase version 3 after correcting the import-map path.
5. Re-resolved the repository's current `main` SHA after the write; current observed value is `867f4399be3e4c5fb6d7d75fafd82fc0225d464e`.
6. Confirmed the canonical deployment workflow remains the sole build/deploy authority and already performs exact checkout, build, Cloudflare deploy, explicit 100% promotion, and independent public-runtime verification.

## Protected boundaries

- Never dispatch a stale or merely historical commit.
- Never bypass the canonical deployment workflow.
- Never expose or log GitHub credentials.
- Never claim deployment success without GitHub acceptance and downstream runtime evidence.
- Never use GitHub Actions as the Activity Feed writer.
- Never fabricate a receipt.

## Remaining P0 boundary

The Edge Function expects a server-side GitHub dispatch credential in one of:

- `GITHUB_TOKEN`
- `GITHUB_ACTIONS_TOKEN`

The available Supabase management surface does not expose secret values or provide a secret-write action. The credential therefore cannot be activated from the current Naya tool surface without an external administrative action.

Supabase's current documentation confirms production Edge Function secrets are configured through the Dashboard's Edge Function Secrets management or the Supabase CLI, and are available to functions as environment variables. Secrets must not be committed to Git or exposed to browsers.

## Exact next action

**Activate one least-privilege server-side GitHub dispatch credential for `nayanet-github-dispatch`, without placing the credential in repository source, then invoke the function with the exact current `main` SHA and explicit approval.**

After activation, immediately:

1. resolve the exact current `main` SHA again;
2. invoke the bridge with that SHA, `EXPLICIT_APPROVAL_GRANTED`, a deployment reason, and unique idempotency key;
3. observe the resulting workflow run;
4. verify exact source → build → artifact → Cloudflare → 100% version → public runtime → runtime source SHA/assets/markers;
5. finalize the Supabase execution receipt;
6. write the Activity Feed event directly through the operational system;
7. update machine state only from independent evidence;
8. return to Naya;
9. create Torch 65 with one next action.

## Human action required

The only external action currently required is secure secret configuration in Supabase. Do not send the credential in chat. Configure it directly in the Supabase project as a server-side Edge Function secret.

## Truth state

`IMPLEMENTED → EXACT-SHA HARDENED → CREDENTIAL-GATED → DISPATCH NOT YET PROVEN`

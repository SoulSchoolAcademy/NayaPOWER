# 🔐 Two-Real-User Owner-Isolation Proof Attempt — 2026-09-19

**STATUS: NOT-PROVEN / BLOCKED AT AUTHENTICATED TEST-IDENTITY PROVISIONING**

## Mission

Execute the complete A/B owner-isolation matrix through the real deployed client/runtime boundary:

Smart Notes → Cognition → Smart Ledger → Intelligence Index → Learning → Reports → Spaces.

Required proof standard: two independent legitimate authenticated identities, each creating and accessing owned objects, followed by cross-owner read/mutate denial tests.

## Repository truth at execution start

- Local HEAD: `4dc7044955574f9dd9b968747d6a5d2a54be93e1`
- Remote `origin/main`: `66cdf4ee1c08061aa0bae44d2b217256a3f13f65`
- Working tree: dirty with substantial pre-existing/staged/untracked work.
- No reset, stash, delete, or overwrite was performed.

## Work performed

1. Refreshed `origin/main` before testing.
2. Inspected the deployed/repository owner-isolation surface.
3. Confirmed the existing isolated Smart Note workflow is syntax/E2E oriented but does **not** provision two independent Supabase identities.
4. Confirmed live owner-scoped RLS observations from the preceding production audit:
   - Smart Notes
   - Cognition
   - Intelligence Index
   - Smart Ledger
   - Learning Evidence / Learner State
   - Reports
   - Spaces
5. Attempted to identify a legitimate existing repository test-identity/credential provisioning path. No provisioned A/B identity mechanism was available through the accessible repository/workflow surface.
6. Did **not** fabricate users, fake `auth.uid()`, use service-role credentials as a browser identity, or convert a client-side filter/RLS policy inspection into behavioral PASS.

## Required A/B matrix

| Surface | A create/read/mutate own | B create/read/mutate own | A denied from B | B denied from A | Status |
|---|---|---|---|---|---|
| Smart Notes | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT-PROVEN |
| Cognition | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT-PROVEN |
| Smart Ledger | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT-PROVEN |
| Intelligence Index | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT-PROVEN |
| Learning | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT-PROVEN |
| Reports | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT-PROVEN |
| Spaces | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT-PROVEN |

## Evidence classification

- **OBSERVED:** server-side owner-scoped RLS policies exist on the inspected domain surfaces.
- **OBSERVED:** the live runtime has the required Smart Note → Cognition / Ledger / Index projection architecture.
- **NOT-PROVEN:** two independent real authenticated identities can each exercise their own complete transaction.
- **NOT-PROVEN:** cross-owner reads are rejected through the actual authenticated client/runtime boundary.
- **NOT-PROVEN:** cross-owner mutations are rejected through the actual authenticated client/runtime boundary.
- **BLOCKED:** legitimate A/B test identity provisioning/credentials are not available to this execution lane.

## Exact closure condition

This item becomes **PROVEN** only after two legitimate authenticated test identities are provisioned through the authorized identity/test-secret boundary and the complete A/B create/read/mutate matrix executes against the deployed runtime, with causal object IDs, authenticated identity IDs, allowed operations, denied operations, and server-observed results recorded.

**No synthetic identity or fabricated credential was used.**

## Continuation

Provision two legitimate authenticated test identities through the authorized secret/provisioning runner, then execute the complete A/B matrix through the deployed client/runtime and append the resulting proof to the Team Naya Activity Feed.


## 2026-09-19 — Authorized provisioning bridge implemented

The missing execution bridge is now implemented on branch `proof/two-user-owner-isolation`.

### Secure runtime design

- `.github/workflows/verify-two-user-owner-isolation.yml` is manual-dispatch only.
- `SUPABASE_SERVICE_ROLE_KEY` is consumed only from the GitHub Actions encrypted secret store.
- No service-role key, test password, access token, or client credential is committed to Git.
- The runner generates fresh A/B passwords in process memory.
- The runner creates two confirmed Supabase Auth users through the Auth Admin API.
- The runner signs both users in through the normal client token endpoint.
- All seven-surface operations after sign-in use the individual user access tokens, so RLS evaluates the real `auth.uid()` for A and B.
- The generated credentials are never written to the proof artifact.
- The two test identities remain available after the run so the recorded authenticated IDs remain meaningful for audit/replay.

### Matrix runner

`scripts/verify-two-user-owner-isolation.mjs` creates independent A/B objects and verifies:

- Smart Notes: authenticated create/read/mutate plus cross-owner denial.
- Cognition: authenticated create/read/mutate plus cross-owner denial.
- Learning: authenticated evidence and learner-state create/read/mutate plus cross-owner denial.
- Reports: authenticated create/read/mutate plus cross-owner denial.
- Spaces: authenticated create/read/mutate plus cross-owner denial.
- Intelligence Index: authenticated owner projection retrieval and cross-owner isolation.
- Smart Ledger: authenticated owner projection retrieval and cross-owner isolation.
- Index/Ledger write attempts are treated as projection-boundary checks because the live policies expose them as read-only projections.

### Current ruling

- **IMPLEMENTED:** authorized provisioning/runtime bridge.
- **IMPLEMENTED:** seven-surface authenticated A/B matrix runner.
- **NOT-PROVEN:** GitHub Actions execution has not yet occurred because the encrypted `SUPABASE_SERVICE_ROLE_KEY` has not been supplied to the repository's secret store through an authorized channel.
- **NOT-PROVEN:** final A/B PASS until the workflow produces the signed proof artifact.

The final proof must come from the workflow artifact, not from this document.

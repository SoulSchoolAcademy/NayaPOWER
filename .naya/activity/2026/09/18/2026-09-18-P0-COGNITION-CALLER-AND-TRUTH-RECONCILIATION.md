# P0 — Production Cognition Caller + Truth Reconciliation

**Date:** 2026-09-18  
**Repository:** `SoulSchoolAcademy/NayaPOWER`  
**Execution branch:** `naya/p0-production-cognition-wiring-2026-09-18`

## Mission

Continue P0 without waiting for protected test credentials:

- trace the real production cognition caller;
- wire the canonical Hub to the governed Assistant runtime;
- reconcile the dated issue-classification snapshot with the live issue surface;
- distinguish local workspace state from GitHub canonical main;
- preserve the authenticated A/B ownership proof as NOT PROVEN until a legitimate protected identity exists.

## Executed

### 1. Production caller traced

The canonical Hub `2026 09 17 NAYANET HUB.html` loads:

`/assistant-runtime.js?v=20260918-r7`

Before this change, `NayaAssistantRuntime.retrieve()` and `record()` existed but had no application caller.

The Hub now has a canonical cognition bridge:

- Personal Intelligence selection invokes `NayaAssistantRuntime.retrieve()`.
- Existing Save actions invoke `NayaAssistantRuntime.record()`.
- The bridge refuses unauthenticated operations.
- The bridge never supplies or overrides `user_id`.
- Supabase Auth remains the identity source.
- Database RLS remains the security boundary.

### 2. Canonical cognitive engine tightened

`scripts/nayanet-cognitive-engine.js` previously retrieved remote cognition by project only.

Remote initialization and remote search are now additionally scoped to the authenticated session owner.

This is defense-in-depth and caller alignment; it is not a substitute for server-side RLS.

### 3. Historical classification reconciled

The 61-row issue classification dated 2026-09-17 is preserved as a historical inventory.

The Cold-Naya index now explicitly distinguishes:

- historical classification owner: Issue #245;
- current execution focus: governed Assistant-lane cognition wiring and authenticated ownership proof.

The navigation test now validates that distinction rather than falsely treating the dated 61-issue snapshot as the current GitHub issue count.

### 4. Local/GitHub divergence recorded

The local workspace was observed at:

- local HEAD: `4dc7044955574f9dd9b968747d6a5d2a54be93e1`
- local `origin/main`: `0a97c30b70e49a530094cc39869b05444ae2c858`
- local branch: 25 commits ahead / 891 commits behind.

The local workspace contains extensive unmerged work and cannot be treated as a clean mirror of GitHub main.

The canonical P0 implementation was therefore made against a fresh GitHub-main branch instead of blindly merging the divergent local workspace.

## Live database truth

The live `public.nayanet_cognition_events` table was independently inspected.

Current policy:

`nayanet_cognition_events_owner`

- RLS enabled: true
- policy command: ALL
- USING: `user_id = auth.uid()`
- WITH CHECK: `user_id = auth.uid()`

This proves configured server-side ownership enforcement.

It does **not** prove two-principal behavioral isolation.

## NOT PROVEN

The following remain intentionally unclaimed:

1. legitimate protected Assistant-lane test identity;
2. authenticated User A transaction;
3. authenticated User B transaction;
4. A cannot retrieve B;
5. B cannot retrieve A;
6. authenticated positive lifecycle against the deployed Assistant runtime;
7. behavioral learning.

## Protected next action

Provision the authorized Assistant-lane test identity through the protected `assistant-cloudflare-production` mechanism, then execute the real two-principal retrieval proof and consume its secret-free receipt into the canonical proof surface.


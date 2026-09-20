# Activity 004 — Name-First Authentication Adapter Execution

**Date:** 2026-09-18
**Mission:** Connect the existing NayaNET name/alias identity surface to the existing authenticated Supabase cognition boundary without creating a second identity or persistence system.

## Verified source truth

- `WelcometoNayaNET.html` is name-first and stores the entered name in browser session state before entering the identity bridge.
- `NAYANET Login bridge page` derives/accepts the NayaNET alias and previously persisted browser-local identity values before entering the Hub.
- The production Supabase project already contains `members`, `nayanet_profiles`, cognition state/events, and the existing Hub session adapter.
- `auth.users.id` is the canonical authenticated user identifier used by the existing data model.
- `nayanet_profiles` is currently empty in production at time of inspection; no second profile system was introduced.
- Current production `auth.users` inspection showed permanent users only; no anonymous users were present at inspection time.
- Supabase documentation confirms anonymous sign-in creates an authenticated Supabase user without requiring email/password/PII, but recovery across a cleared browser/device requires later identity linking.

## Changes executed

1. Added `NAYANET/name-first-auth-adapter.js`.
2. Adapter establishes/reuses a persistent Supabase session with `signInAnonymously()` when no session exists.
3. Adapter writes non-sensitive display identity into Supabase user metadata.
4. Adapter upserts the existing `members` row using `auth.users.id`.
5. Adapter upserts the existing `nayanet_profiles` row using the same member/user identity.
6. Adapter preserves the NayaNET alias as an application namespace, not an email address.
7. Added `identity.html` as the name-first bridge route using the adapter and routing to `NAYAHUB.html` rather than Academy.
8. Added source-contract/anonymous-auth verification workflow.
9. Corrected the workflow's false-positive email/password source assertion.
10. Added a behavior-neutral adapter change to retrigger verification.

## Current execution evidence

- Canonical source branch advanced to commit `6ffca7e4799df814e00d39e8076f161c75b69ff7` during this execution.
- Existing Smart Note verification workflow continued to execute successfully on the new commit.
- The newly added name-first verification workflow has not yet produced a GitHub Actions run; therefore anonymous-auth availability is **NOT YET VERIFIED**.
- Production database inspection found zero anonymous users at inspection time. This is evidence of absence of prior anonymous users, not proof that the provider is disabled.
- `welcome.nayanet.app` could not be source-verified through the available public fetch path; exact live deployment/route mapping remains unresolved.
- Root Vercel project status currently reports a Vercel build-rate-limit failure on the repository deployment, so the new root `identity.html` cannot be treated as live production evidence from that deployment alone.

## Architectural ruling

The obsolete email/password proof is superseded. The canonical lifecycle proof must be:

`Welcome → name → NayaNET alias → authenticated session → auth.users → members/profile → Intelligent Hub → Smart Note → persist → retrieve → fresh context`

The name/alias layer is application identity metadata. Supabase Auth supplies the authenticated security boundary. Existing cognition persistence remains authoritative.

## Installed-app rule

`valid persisted NayaNET session → Intelligent Hub`

`no valid session → Welcome`

Academy is not an authentication destination.

## Blockers

1. Live Welcome deployment/source mapping is not yet proven.
2. Anonymous-auth provider availability is not yet proven by a completed runtime probe.
3. Cross-origin session continuity between the Welcome origin and the canonical Hub origin still requires an explicit deployment/route decision and runtime verification; browser local storage is origin-scoped.

## Protected

- No duplicate identity database.
- No duplicate cognition persistence system.
- No email credential fabricated for NayaNET users.
- Existing Intelligent Hub visual surface is not redesigned.
- Existing production Cloudflare Hub remains the authorized Hub runtime.

## Next executable sequence

1. Obtain/verify the exact live Welcome deployment mapping.
2. Verify anonymous-auth provider availability through an authorized runtime execution surface.
3. If enabled, run the adapter against the real Welcome origin.
4. Verify `auth.users → members → nayanet_profiles` creation with the same UUID.
5. Verify authenticated Hub session restoration.
6. Execute Smart Note capture.
7. Retrieve the same intelligence in an independent fresh context.
8. Verify installed-app routing behavior.
9. Record receipts and update canonical control-plane evidence only after observed verification.

# Activity 005 — NayaNET Name-First Runtime Continuation

**Date:** 2026-09-18
**Mission:** Continue the real NayaNET human lifecycle to the furthest executable verified boundary without creating a parallel identity, authentication, persistence, cognition, Activity, or routing system.

## Observed source/runtime architecture

- Canonical repository: SoulSchoolAcademy/NayaPOWER.
- Live main was resolved during this execution; subsequent source commits advanced the branch after the previously recorded production receipt, so historical production evidence is not promoted as current proof.
- The canonical Cloudflare Hub deployment workflow is .github/workflows/deploy-nayanet-intelligent-hub.yml.
- The production worker target is sparkling-shape-7ae5 at https://sparkling-shape-7ae5.smartnetpodcast.workers.dev.
- The deployment workflow explicitly binds NAYANET/name-first-auth-adapter.js and identity.html into the Hub deployment.
- The production deployment also installs 2026 09 17 NAYANET HUB.html as the canonical presentation baseline and assistant-runtime.js as the runtime bridge. Therefore those two artifacts, not the unused React presentation path, are the decisive production runtime surface.
- The Welcome source WelcometoNayaNET.html is a separate origin and redirects successful name entry to the canonical Hub identity.html route. Browser storage is origin-scoped, so the clean session boundary is authentication on the Hub origin.

## Name-first path verified at source level

WelcometoNayaNET.html
→ name captured
→ canonical Hub identity.html
→ NayaNETNameFirstAuth.establish(name, alias)
→ existing Supabase Auth
→ existing members
→ existing nayanet_profiles
→ canonical Hub
→ existing Assistant cognition runtime
→ existing Smart Note capture/persistence boundary

No email address is generated for the NayaNET identity layer. The alias remains an application namespace/address.

## Existing persistence boundary observed

Production schema inspection confirms the existing authoritative tables include:

- public.members keyed by auth.users.id
- public.nayanet_profiles keyed by member_id
- public.nayanet_notes
- public.nayanet_project_cognition_state
- public.nayanet_cognition_events
- public.nayanet_intelligence_index
- public.nayanet_execution_receipts

No new identity database or persistence database was introduced.

## Authentication blocker — observed

A real production Supabase Auth invocation against the project returned:

- HTTP 422
- error_code: anonymous_provider_disabled
- message: Anonymous sign-ins are disabled

Therefore:

**SUPABASE_ANONYMOUS_AUTH = BLOCKED**

Supabase's current documentation confirms that signInAnonymously() creates a real authenticated user with a UUID and is_anonymous=true, while using the authenticated Postgres role. citeturn2search0turn2search4

## Production lifecycle status

Not promoted to PASS. The following remain unverified because the required anonymous session cannot currently be created:

1. real anonymous session
2. real auth.users.id
3. same UUID in members.id
4. same UUID in nayanet_profiles.member_id
5. Hub IdentityProvider attribution
6. authenticated Personal Intelligence retrieval
7. real Smart Note transaction
8. persistence observation
9. fresh independent browser context
10. same-human/same-intelligence continuity
11. installed-app valid-session routing
12. installed-app no-session routing

## Additional source finding

The repository contains a React Hub implementation, but the canonical Cloudflare deployment workflow replaces the generated dist/index.html with the timestamped canonical presentation baseline before deployment. The React identity/session files therefore are not the decisive production routing surface. No production claim was based on those unused React changes; temporary source-only routing edits were reverted to preserve source/runtime parity.

## Architectural ruling

The correct production path remains:

Welcome → canonical Hub identity.html → name/alias → Supabase anonymous Auth → existing identity/member/profile → canonical Hub → existing cognition runtime → Smart Note → persistence → fresh-context retrieval

No cross-origin refresh-token handoff is introduced.
No email/password substitute is introduced.
No Academy authentication destination is introduced.
No duplicate persistence system is introduced.

## Next authorized action

Enable Supabase Auth → Anonymous Sign-ins for project dahisasgpfvziswqvmvm. Then rerun the real name-first runtime gate and continue automatically through member → profile → Hub → cognition → Smart Note → persistence → fresh context → PWA routing.

Until that setting is enabled, the correct evidence state is BLOCKED, not PASS.

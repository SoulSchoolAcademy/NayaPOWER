# 005 — Name-First Runtime Auth Gate

Date: 2026-09-18
Active block: TORCH-59-MACHINE-TRUTH-RESTORATION
Canonical branch: main
Observed HEAD at record time: 8e94c601fa3efabe6828857f34ef0117de3850d5

## Mission
Complete the real NayaNET human lifecycle without creating another identity, authentication, persistence, cognition, Activity, or routing system.

## Executed
1. Inspected the canonical name-first adapter and existing Hub IdentityProvider.
2. Confirmed the existing Hub uses persistent Supabase Auth session state and maps user metadata into the canonical identity model.
3. Rewired the existing NayaNET Login bridge to the single `NayaNETNameFirstAuth` adapter.
4. Rewired canonical `identity.html` to the same adapter and the canonical Hub root `/`.
5. Replaced the Hub email/password AuthPanel with the existing adapter-driven name/alias entry; no second authentication implementation was introduced.
6. Loaded the single adapter from the canonical Hub entrypoint.
7. Preserved the existing Hub build path while adding build-time copies of the single adapter and identity route into the deployed asset set.
8. Added a real Supabase anonymous-auth runtime gate to the existing primary verification workflow.
9. Executed that gate through GitHub Actions run 35386929663 against the then-current main commit.
10. Retrieved the complete job log and observed the actual Supabase response.
11. Queried production schema constraints: `members.id` is the Auth UUID foreign key/primary key; `nayanet_profiles.member_id` is the Auth UUID foreign key/primary key; `nayanet_profiles.smart_id` is unique.
12. Queried existing triggers and confirmed `nayanet_notes` already feeds the existing intelligence index through `nayanet_index_intelligence_row`; no parallel persistence path was created.
13. Verified the current Supabase project is ACTIVE_HEALTHY.
14. Verified the public `welcome.nayanet.app` surface resolves to `shiny-wave-dd48.nayanet.workers.dev` and is visually the repository's Welcome surface, while its deployment source is not exposed by the canonical NayaPOWER repository.
15. Verified the canonical Hub runtime is `https://sparkling-shape-7ae5.smartnetpodcast.workers.dev/` and that the latest Vercel project deployment is the React Hub build, not the public Welcome surface.
16. Changed the repository Welcome source so its existing name entry and Auto-Login hand off to the canonical Cloudflare Hub identity route rather than creating a local identity boundary.
17. Changed `identity.html` so successful establishment enters the canonical Cloudflare Intelligent Hub origin rather than looping back through the Welcome origin.
18. Changed the single adapter to surface the exact production configuration blocker as `ANONYMOUS_AUTH_DISABLED`.
19. Extended the canonical Hub deployment trigger so changes to the single identity adapter and `identity.html` are deployed with the Hub rather than silently remaining source-only.
20. Deployed the current Hub source to Cloudflare successfully: release `8e94c601fa3efabe6828857f34ef0117de3850d5`, Cloudflare Version ID `d739a21a-a5e4-4deb-bad0-3e7d2601cff5`; live artifact verification passed and confirmed the canonical presentation.

## Runtime evidence
The real Auth endpoint invocation returned:

`HTTP 422`

`error_code: anonymous_provider_disabled`

`msg: Anonymous sign-ins are disabled`

This is a genuine production configuration blocker. Anonymous authentication is therefore **NOT AVAILABLE / BLOCKED**, not PASS.

GitHub Actions source gates before the runtime call passed:
- PIS projection PASS (40 events)
- persistent PIS adapter source PASS
- name-first source contract PASS

The auth gate then failed closed, so downstream build/typecheck/control-plane steps in that run were skipped.

## Architectural ruling
The name-first application boundary is now aligned to the existing Supabase Auth identity boundary, but the production Supabase project must explicitly enable anonymous sign-ins before the requested lifecycle can be executed. Supabase's current documentation confirms anonymous sign-ins are a supported Auth mode for authenticated, email-less experiences and must be enabled in project Auth settings.

No email address was fabricated. No email/password fallback was used. No second identity or persistence system was introduced.

## Production routing truth still unresolved
The public `welcome.nayanet.app` domain currently resolves to a Cloudflare Worker surface that is not demonstrably the same deployed artifact as the canonical repository Welcome source. The live Welcome Worker is confirmed as the public front door, but its deployment source is not exposed by NayaPOWER. The repository source is now prepared to hand the human directly into the canonical Cloudflare Hub identity route; production deployment of that Welcome source remains outside the verified NayaPOWER deployment path. The canonical Hub production runtime remains the authorized Cloudflare Intelligent Hub release path. The latest deployment is verified production-proven for the deployed source commit; the name-first lifecycle itself remains blocked at Auth configuration.

## Protected state
- Canonical Hub visual surface remains protected.
- Canonical Supabase tables remain the persistence boundary.
- Canonical IdentityProvider remains the Hub session authority.
- No Academy authentication destination.
- No synthetic email identity.
- No duplicate persistence, Activity, cognition, or baton system.

## Current blockers
1. `SUPABASE_ANONYMOUS_AUTH = BLOCKED: anonymous_provider_disabled` — the actual production Auth endpoint returned HTTP 422.
2. The public Welcome Worker deployment source/control plane is not connected to NayaPOWER's verified GitHub deployment path, so repository changes to `WelcometoNayaNET.html` are not yet proven live at `welcome.nayanet.app`.
3. Because Anonymous Auth is disabled, no real Auth UUID/member/profile/session/cognition lifecycle can be honestly executed yet.

## Next executable action
1. Enable Supabase Auth > Anonymous sign-ins for project `dahisasgpfvziswqvmvm` using the authorized project-admin surface.
2. Re-run the existing real `/auth/v1/signup` runtime gate and require a real anonymous `auth.users.id` + access token + `is_anonymous=true`.
3. Immediately execute the same-session provisioning proof into `members` and `nayanet_profiles`.
4. Then continue the authenticated Hub cognition/Smart Note/fresh-context proof without introducing any new identity architecture.

## Verification rule
Do not promote lifecycle status until the runtime evidence exists for:

`NAME → ALIAS → AUTH SESSION → AUTH.USER → MEMBER → PROFILE → HUB IDENTITY → INTELLIGENCE → SMART NOTE → PERSIST → RETRIEVE → FRESH CONTEXT → SAME HUMAN → SAME INTELLIGENCE`

## Continuation
The next Naya must resume from this exact blocker, not from the older email/password test path.

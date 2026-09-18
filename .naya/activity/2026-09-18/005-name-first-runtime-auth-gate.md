# 005 — Name-First Runtime Auth Gate

Date: 2026-09-18
Active block: TORCH-59-MACHINE-TRUTH-RESTORATION
Canonical branch: main
Observed HEAD at record time: 6e91e27d22b55b593c05b5627b9d771cba0148eb

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
The public `welcome.nayanet.app` domain currently resolves to a Cloudflare Worker surface that is not demonstrably the same deployed artifact as the canonical repository Welcome source. The repository's `WelcometoNayaNET.html` routes to `identity.html`, while the exact live Worker source/deployment mapping remains unverified. The canonical Hub production runtime remains the authorized Cloudflare Intelligent Hub release path.

## Protected state
- Canonical Hub visual surface remains protected.
- Canonical Supabase tables remain the persistence boundary.
- Canonical IdentityProvider remains the Hub session authority.
- No Academy authentication destination.
- No synthetic email identity.
- No duplicate persistence, Activity, cognition, or baton system.

## Current blocker
`SUPABASE_ANONYMOUS_AUTH = BLOCKED: anonymous_provider_disabled`

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

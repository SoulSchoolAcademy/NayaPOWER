# Lead Naya Session — Production Truth Map / Action 01

DATE: 2026-09-19
MISSION: Establish the production truth map for Communication + Organization before implementation.
OWNER: Lead Naya
STATUS: ACTION 01 COMPLETE / SUBSYSTEM NOT VERIFIED

## DONE

Inspected the live Supabase project `dahisasgpfvziswqvmvm`, current production Edge Functions, relevant database tables/RLS/functions, canonical Hub source, relationship feature specifications, and repository source search.

Updated the Lead Naya Master Execution Directive with the full cold-start context, live findings, boundary matrix, completed Action 01 report, and the complete Action 02 execution directive.

Master directive commit:
`27335e6048c31f13c365d1272fdb0c7e0a888ae7`

Master directive:
`NAYA-TEAM/2026/09/19/2026-09-19__LEAD-NAYA-MASTER-HANDOFF-COMMUNICATION-ORGANIZATION.md`

## PROOF

Live production findings:

- `nayanet_spaces`: 1 row.
- `v7_connection_requests`: 0 rows.
- `v7_mail_threads`: 64 rows.
- `v7_mail_members`: 128 rows.
- `v7_mail_messages`: 64 rows.
- `nayanet_cognition_events`: 123 rows.
- `nayanet_smart_ledger`: 94 rows.
- `nayanet_intelligence_index`: 353 rows.
- `nayanet_execution_receipts`: 125 rows.
- `nayanet_execution_outcomes`: 0 rows.
- `nayanet_intelligence_publications`: 0 rows.

Existing production relationship primitive:
`v7_connection_requests`

Observed RLS:
- requester may insert own request;
- requester or target may read;
- target may update.

Existing production identity/profile layers:
- `members`
- `nayanet_profiles`
- `v7_profiles`

Existing production Space:
- `nayanet_spaces`
- owner-only RLS observed.

Critical absence:
No dedicated public table matching Space membership was found in the live table inventory.

Existing Smart Mail:
- `nayanet-smart-mail` v12;
- ACTIVE;
- JWT required;
- send requires authority grant validation;
- real message persistence and receiver verification exist.

Critical communication gap:
The inspected Smart Mail implementation does not itself prove that Space-derived relationship eligibility is required before sending.

Cloudflare:
Repository search did not establish a source/build/deployment map. Therefore Cloudflare parity remains UNKNOWN, not failed and not verified.

## DECISION

1. Do not create a new `connections` table yet.
2. Do not create a contact database.
3. Do not immediately create a Space-membership table.
4. Reconcile existing identity/profile and membership substrate first.
5. Treat `v7_connection_requests` as an existing relationship primitive requiring reconciliation, not automatically as the final connection graph.
6. Reuse existing Mail, authority, event, intelligence and Ledger infrastructure.
7. Preserve the canonical Hub visual baseline.
8. Cloudflare remains unverified until source → build → deployed runtime is mapped.

## NOT PROVEN

- canonical identity/profile owner;
- canonical Space membership;
- authenticated JOIN;
- connection establishment;
- accepted connection-request semantics;
- Smart List person/connection membership;
- relationship-gated Smart Mail;
- relationship revocation;
- two-user isolation for this subsystem;
- Cloudflare source/build/runtime parity.

## WHY THIS MATTERS

The entire subsystem depends on one causal chain:

DISCOVERY → SPACE → JOIN → MEMBERSHIP → CONNECTION → COMMUNICATION / LIST → ACTIVITY → LEDGER

The current highest-risk boundary is:

**JOIN → MEMBERSHIP**

If that boundary is invented incorrectly, every downstream surface becomes a competing truth.

## NEXT — FULL MASTER DIRECTIVE

Execute **Action 02 — Canonical Identity + Space Membership Reconciliation** from the Lead Naya Master Execution Directive.

The successor must:

1. inspect repository source and migrations for members/profiles/Space/member/join/leave/participant/membership;
2. inspect live foreign keys, indexes, constraints, triggers, functions, RLS and grants;
3. establish AUTH USER → MEMBER → PROFILE → PUBLIC IDENTITY;
4. determine whether a generic or hidden membership primitive already exists;
5. determine Space discovery/view/JOIN/INVITE/LEAVE/REVOKE semantics;
6. determine membership visibility and RLS;
7. determine JOIN idempotency and event provenance;
8. determine whether Space membership establishes relationship eligibility;
9. reconcile `v7_connection_requests` before creating any relationship storage;
10. document the exact canonicality decision;
11. update Your Connections, Smart Spaces, Job 04, Team Naya and the master directive;
12. if membership is genuinely absent, design—but do not blindly deploy—the smallest canonical membership model;
13. finish with DONE / PROOF / NOT PROVEN / DECISION / BLOCKERS / NEXT.

No relationship/contact schema may be invented before this reconciliation is complete.

# ACTION 02 — IDENTITY + SPACE MEMBERSHIP RECONCILIATION

**Date:** 2026-09-19  
**Owner:** Lead Naya  
**Repository:** SoulSchoolAcademy/NayaPOWER  
**Supabase:** dahisasgpfvziswqvmvm

## DONE

Completed live identity/profile/Space/membership reconciliation against the production Supabase schema, RLS, foreign keys, indexes, triggers, migrations, RPC inventory, Smart Mail v12 source, and canonical Hub HTML.

Canonical identity:
- `auth.users.id = members.id`
- 291 auth users / 291 members
- zero auth↔member mismatches

Canonical profile:
- `nayanet_profiles.member_id → members.id`
- 83 live profiles
- zero orphan profiles
- `v7_profiles` has 0 live rows and is not the populated relationship profile substrate

Canonical Space:
- `nayanet_spaces`
- owner `owner_member_id → members.id`
- visibility `private | shared`
- owner-only RLS
- one live Space
- Space insert/update projects to Smart Ledger through `nayanet_space_to_ledger()`

Membership:
- no dedicated Space membership/participant table
- no Space JOIN/LEAVE/INVITE RPC
- no membership FK/index/state machine/policy
- `v7_mail_members` is thread membership only

**MEMBERSHIP CANONICALITY BLOCKED — NO EXISTING SUBSTRATE FOUND**

No production schema was changed.

## PROOF

- `members.id` FK → `auth.users.id`
- `nayanet_profiles.member_id` PK/FK → `members.id`
- `nayanet_spaces.owner_member_id` FK → `members.id`
- `nayanet_spaces` trigger → `nayanet_space_to_ledger()`
- live candidate-table inventory contains no Space membership table
- live Space-related function inventory contains no JOIN/LEAVE/INVITE function
- Smart Mail v12 authenticates the bearer session and uses the authenticated UUID for sender/receiver
- canonical Hub HTML contains visual Connections/Mail/Space-oriented UI but no direct Supabase/auth/Space/Mail runtime wiring

## NOT PROVEN

- membership schema/runtime
- Space discovery for non-owners
- JOIN/LEAVE/INVITE
- participant visibility
- connection establishment from membership
- relationship revocation
- Smart List person membership
- relationship-gated Smart Mail
- two-user lifecycle
- Cloudflare parity

## DECISION

Use:
- **Identity:** `auth.users.id = members.id`
- **Member:** `public.members`
- **Profile:** `public.nayanet_profiles`
- **Legacy profile:** `public.v7_profiles` (empty compatibility layer)
- **Space:** `public.nayanet_spaces`
- **Mail identity:** `auth.users.id / members.id`
- **Membership:** absent; implementation waits for relationship reconciliation

Do not create duplicate identity/profile/contact stores.

## BLOCKERS

Canonical Space membership is missing. Before implementing it, Action 03 must reconcile `v7_connection_requests` so membership does not create a second relationship graph.

## NEXT

**ACTION 03 — CANONICAL RELATIONSHIP SUBSTRATE RECONCILIATION**

Reconcile `v7_connection_requests` across live schema, RLS, migration history, available source references, accepted/rejected semantics, and Space-derived relationship semantics. Determine whether it is request-only legacy state or part of the canonical relationship graph. Then define the exact relationship state machine and provenance required for Action 04 membership implementation.

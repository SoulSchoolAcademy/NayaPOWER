# ACTION 04 — REAL JOIN / MEMBERSHIP SUBSTRATE

**Date:** 2026-09-19  
**Owner:** Lead Naya  
**Supabase:** dahisasgpfvziswqvmvm

## DONE

The missing canonical Space membership substrate was implemented in production and captured in source migrations.

Created:
- `public.nayanet_space_members`
- current membership states: active / left / revoked
- roles: owner / member
- unique Space+member constraint
- explicit membership provenance
- RLS for self and active members of shared Spaces
- owner-membership backfill/trigger
- `nayanet_join_space(uuid)`
- `nayanet_leave_space(uuid)`
- shared-Space discovery SELECT policy
- JOIN/LEAVE cognition-event recording through the existing event substrate

Source migrations:
- `supabase/migrations/20260919170000_nayanet_space_membership_v1.sql`
- `supabase/migrations/20260919170500_nayanet_space_membership_provenance_v1.sql`
- `supabase/migrations/20260919171000_nayanet_space_membership_provenance_runtime_v1.sql`

## PROOF

Live production after migration:
- membership table exists
- RLS enabled
- active membership count = 1
- existing Space owner is backfilled as active owner membership
- join/leave functions are SECURITY DEFINER and executable by authenticated role
- shared Space discovery policy exists
- private Space join by unrelated member is denied with `SPACE_JOIN_NOT_ALLOWED`
- transactional database-level test of shared JOIN → duplicate JOIN → LEAVE → duplicate LEAVE completed and rolled back, so no synthetic test state remains

## NOT PROVEN

- browser/Edge authenticated human JOIN against the deployed Hub
- non-owner discovery through current Hub UI
- two real human users
- current Cloudflare runtime parity
- connection establishment after membership
- relationship-gated Mail
- Smart List
- revocation across all downstream surfaces

## DECISION

Space membership is now canonical:
`nayanet_space_members(space_id, member_id)`.

Membership is participation state, not permanent Connection and not authority.

JOIN is explicit and idempotent. LEAVE is explicit. Membership events use the existing cognition/event substrate.

## BLOCKERS

The remaining runtime blocker is the lack of a current authenticated browser proof for the new JOIN path. The database contract itself is deployed and tested at the transaction/RLS layer.

## NEXT

ACTION 05 — CANONICAL CONNECTION / SAVE-CONNECTION PROJECTION.

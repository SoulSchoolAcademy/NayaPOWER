# ACTION 05 — YOUR CONNECTIONS / SAVED RELATIONSHIP PRIMITIVE

**Date:** 2026-09-19  
**Owner:** Lead Naya

## DONE

Implemented the canonical durable saved-Connection primitive after Action 03 proved no existing durable Connection store existed.

Created:
- `public.nayanet_connections`
- owner-scoped RLS
- explicit source Space provenance
- active/revoked state
- unique owner→connected relationship
- `nayanet_save_connection(target, space)`
- `nayanet_revoke_connection(target)`
- cognition-event recording for save/revoke

## PROOF

Transactional authenticated-role database test:
- actor and target were distinct real member IDs.
- a shared Space membership was created only inside the transaction.
- SAVE CONNECTION succeeded.
- repeated SAVE returned `ALREADY_CONNECTED` against the same persisted identity.
- transaction rolled back, leaving no synthetic production connection.

The primitive requires an active shared Space between actor and target. It does not infer relationship from similarity.

## NOT PROVEN

- current Hub Connections UI wired to these RPCs
- browser-authenticated save/revoke
- mutual connection acceptance
- Smart Mail relationship gate
- Smart List projection
- Cloudflare parity

## DECISION

Your Connections is now a projection over `nayanet_connections`, not a duplicate contact store.

Membership does not auto-create a Connection.

Connection is not authority.

## NEXT

Action 06 must reconcile and implement Smart List plus bind Smart Mail relationship eligibility without replacing the authority system.

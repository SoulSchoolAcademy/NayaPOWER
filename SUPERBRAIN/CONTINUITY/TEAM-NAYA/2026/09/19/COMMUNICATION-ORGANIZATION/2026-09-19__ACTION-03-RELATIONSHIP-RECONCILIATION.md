# ACTION 03 — RELATIONSHIP SUBSTRATE RECONCILIATION

**Date:** 2026-09-19  
**Owner:** Lead Naya

## DONE

Reconciled `v7_connection_requests` against live production schema, constraints, RLS, rows, public functions and historical Hub source.

## PROOF

- Table: `v7_connection_requests`.
- Rows: 0.
- Columns: id, requester_id, target_id, topic, status, created_at, responded_at.
- FKs: requester_id and target_id → auth.users.id, ON DELETE CASCADE.
- Unique key: requester_id + target_id + topic.
- Status CHECK: pending | accepted | declined | cancelled.
- RLS: requester inserts; requester or target reads; target updates.
- No public connection/relationship function exists.
- No trigger creates a durable connection when status becomes accepted.
- No separate durable connection table existed in the live inventory before this action.
- Historical Hub runtime reads request rows and states that private conversation requires mutual connection; it does not establish a durable accepted-connection object.
- Existing Smart Mail production authorization remains separate from this request table.

## DECISION

`v7_connection_requests` is a **request workflow primitive**, not the canonical durable Connection object.

Accepted means accepted request state only. It does not itself establish a durable Connection record.

The canonical durable Connection primitive was therefore absent and its absence is now proven.

The correct product distinction is:

**SPACE MEMBERSHIP = participation**  
**CONNECTION = deliberate saved relationship**  
**AUTHORITY = permission to perform a consequential action**

A person joining a Space must not automatically become a saved Connection.

## NOT PROVEN

- current Hub Connections runtime
- real authenticated save-connection browser flow
- mutual communication gate
- Smart List
- Cloudflare parity

## NEXT

Action 04 implemented canonical Space membership. Action 05 now implements the explicit saved Connection primitive and projection.

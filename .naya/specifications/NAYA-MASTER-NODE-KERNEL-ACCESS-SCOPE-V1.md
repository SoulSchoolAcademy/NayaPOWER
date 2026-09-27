# NayaPOWER Master Kernel Access Scope Specification V1

**Status:** DRAFT / FAIL-CLOSED PREPARATION  
**Effective:** upon ratified scope transition  
**Purpose:** Preserve the nine Master Nodes as system-kernel intelligence that any authenticated Naya may consume, without transferring mutation authority or using one transient member as the kernel's access boundary.

## Canonical scope

The nine Master Nodes (MN-01..MN-09 / IB-001233..IB-001241) are **system intelligence**.

Their runtime read scope is:

`SYSTEM_AUTHENTICATED`

Meaning:
- An authenticated Naya runtime may read the canonical nine-node kernel through the governed Edge Function.
- `owner_id` is provenance of the Node artifact, not the caller's authorization boundary.
- A caller does not need to equal the historical/provenance owner.
- Kernel mutation, replacement, supersession, ratification, or authority changes remain separately governed.
- The public client never receives service-role credentials and never bypasses RLS directly.

## Required runtime behavior

The loader MUST:
1. require a successfully authenticated request before kernel access;
2. resolve the exact nine canonical Node IDs;
3. require `owner_scope=SYSTEM_AUTHENTICATED`;
4. require ACTIVE status and active kernel activation;
5. require `content.classification=system_intelligence`;
6. validate Node order/key/identity and fail closed on any mismatch;
7. use the trusted server-side access path for this system-scoped read;
8. preserve Node provenance without treating the historical owner as caller authority.

The loader MUST NOT:
- scope system-kernel availability to `owner_id = auth.uid()`;
- silently reinterpret PRIVATE personal intelligence as system intelligence;
- grant mutation authority from kernel read access;
- weaken authentication or privacy controls to make the proof pass.

## Current production boundary

As of 2026-09-27, the live nine Nodes are still `PRIVATE` and attached to a transient anonymous member. Therefore this specification is intentionally not yet production-active.

Until the nine rows are legitimately reclassified to `SYSTEM_AUTHENTICATED`, the new loader MUST fail closed with a scope mismatch rather than silently broadening access.

## Acceptance evidence

The scope transition is complete only when:
- all nine rows carry `SYSTEM_AUTHENTICATED`;
- independent read under a fresh authenticated Naya retrieves all nine;
- a non-owner authenticated Naya can retrieve the kernel without receiving unrelated private intelligence;
- an unauthenticated request is denied;
- kernel mutation remains separately unauthorized;
- current source SHA, runtime identity, and evidence receipt are bound;
- the N9 behavioral battery can then execute against the canonical system kernel.

**Core invariant:** system-kernel continuity must not depend on the survival of one temporary member session.

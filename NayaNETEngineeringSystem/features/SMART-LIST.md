# Smart List — Engineering Specification

## What / why
Smart Lists are the human-controlled organization layer over canonical intelligence. They group references without duplicating Smart Notes. One note may belong to many lists.

## Human interface
Provide **Saved / Favorites / My Lists**. Users can create, rename, describe, add/remove items, multi-select, reorder, archive/delete, search and use a collection elsewhere. The UI should make privacy and share scope explicit.

Deletion semantics: deleting a list removes the list and memberships, not the underlying notes. Removing an item removes membership only. Deleting a note follows the canonical note deletion policy and updates references.

## Front end requirements
- List index and list detail routes.
- Create/edit/delete flows.
- Multi-select and bulk add/remove.
- Drag/reorder where manual order is supported.
- Search across lists and contents.
- Save/favorite controls from Feed and source views.
- Share/use actions guarded by authorization.
- Empty/error/loading/unauthorized states.

## Back end requirements
- List object + separate membership relationship.
- Stable list IDs and owner/scope.
- Membership records containing list ID, target ID, added_by, added_at and order where needed.
- Item-level authorization on reads and sharing.
- No copied Smart Note bodies as a parallel canonical store.
- Idempotent membership mutations.
- Events for meaningful create/update/share/delete actions.

## Data / API contract
Conceptual objects: `smart_list(id, owner_id, name, description, visibility, status, created_at, updated_at)` and `smart_list_membership(list_id, target_id, added_by, added_at, position, source)`. Exact database/API names must follow existing implementation.

## Connections
`Feed → Save/Favorite → Lists`; `Lists → Mail/Share/Spaces`; `Your Connections → canonical people/relationship references`; `Space membership → connection context → Lists`.

A Smart List may contain canonical intelligence and eligible people/connections. Person entries reference canonical identity/relationship state; they do not copy profile or relationship data. Removing list membership does not remove the connection. `Today/Reports → list activity/patterns`; `Ledger → consequential organization/share evidence`.

## Relationship-system verification
Prove that a person/connection can be added to a List without duplicating identity, that removing List membership does not remove the connection, and that revoked/removed relationships cannot be used to bypass communication or intelligence authorization.

## Verification
Create list; add the same note to two lists; prove no note duplication; remove membership without deleting note; delete list while note remains; refresh retrieval; share a list containing a protected note and prove protected content is not leaked.

## Current state
**DEFINED** by `.naya/07`; runtime implementation requires inspection.

## Gap / next action
Inspect existing list/save/favorite implementation and reconcile it with canonical membership and privacy semantics.

## Source authority
`.naya/2026-09-11-NAYAPOWER-07-SMART-LISTS-SMART-NOTE.md`; `.naya/2026-09-11-NAYAPOWER-03-WHAT-ARE-SMART-NOTES-SMART-NOTE.md`; `.naya/2026-09-12-NAYAPOWER-46-IDENTITY-PRIVACY-PUBLICATION-CONTRACT.md`.


## COMPLETION CHECKLIST — 2026-09-19

- [x] Source contract identified
- [x] .naya authority identified
- [x] Specification defined
- [ ] Existing list/save/favorite implementation mapped
- [ ] Canonical store identified
- [ ] Membership persistence proven
- [ ] Owner isolation proven
- [ ] Share protection proven
- [ ] Source → build → runtime parity proven
- [x] Dated activity record exists
- [x] One next action recorded

**Current state:** DEFINED. See [2026-09-19 activity](../ACTIVITY/2026/09/19/SMART-LIST.md).


## ACTION 06 EXECUTION — 2026-09-19

No prior live List/Favorite/Saved/Collection/Group person-organization primitive was found. Canonical List storage is now:
- `nayanet_smart_lists` — owner + name
- `nayanet_smart_list_members` — List → canonical `nayanet_connections`

Server RPCs:
- `nayanet_create_smart_list`
- `nayanet_add_connection_to_list`
- `nayanet_remove_connection_from_list`

RLS is owner-scoped. List membership cannot create or delete a Connection. Removing a List entry only removes organization state.

Transactional authenticated-role proof passed for add + duplicate add; no test state persisted.

Current state: **IMPLEMENTED SUBSTRATE / HUB RUNTIME UNPROVEN**.

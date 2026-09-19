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
`Feed → Save/Favorite → Lists`; `Lists → Mail/Share/Spaces`; `Connections → optional relationship context`; `Today/Reports → list activity/patterns`; `Ledger → consequential organization/share evidence`.

## Verification
Create list; add the same note to two lists; prove no note duplication; remove membership without deleting note; delete list while note remains; refresh retrieval; share a list containing a protected note and prove protected content is not leaked.

## Current state
**DEFINED** by `.naya/07`; runtime implementation requires inspection.

## Gap / next action
Inspect existing list/save/favorite implementation and reconcile it with canonical membership and privacy semantics.

## Source authority
`.naya/2026-09-11-NAYAPOWER-07-SMART-LISTS-SMART-NOTE.md`; `.naya/2026-09-11-NAYAPOWER-03-WHAT-ARE-SMART-NOTES-SMART-NOTE.md`; `.naya/2026-09-12-NAYAPOWER-46-IDENTITY-PRIVACY-PUBLICATION-CONTRACT.md`.

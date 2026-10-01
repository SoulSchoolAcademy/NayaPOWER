# Your Connections — Builder Spec (AI)

**Status:** PROPOSED. **Route:** `hub/connections`. **Accent:** magenta. **Build order:** 6.

## Shell contract

Sidebar + Naya rail unchanged; center swaps. `hub/connections?kind=&selected=`.

## Component tree

1. `ConnectionsHero` — title + `KindTabs` (PEOPLE/AGENTS/SYSTEMS/ORGANIZATIONS/PROJECTS) + `PersonSearch`.
2. `Constellation` — relationship map visualization (orientation aid; zoomable; selection-driven, not decoration).
3. `FocusCard` — selected entity: name, relationship, shared intelligence, recent interaction, common projects, important context, last activity, next relevant action.
4. `Requests` — pending invitations with context.

## Data bindings

- Entities ← governed connection records (kind-filtered). Focus ← record + shared items + recent interactions + permission basis.

## States

- `loading`, `empty_kind` (honest per kind), `no_selection` (prompt to select), `offline` (cached with stamp).

## Interactions

- Kind tab → re-query. Node select → focus card. Search → jump to entity.
- Message → Mail compose to them. Shared items → linked records. Invite to space → space picker.
- Accept/Decline → record update + receipt.

## Design tokens

Magenta threads/markers on obsidian; nodes as star-points with presence glow; focus card as the visual anchor.

## Acceptance

Map never the only content (focus card always present); permissions enforced in UI (no hidden-data leakage); requests show context before decision; 9.0+.

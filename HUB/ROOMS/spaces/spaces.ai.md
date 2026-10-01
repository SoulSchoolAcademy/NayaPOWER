# Smart Spaces — Builder Spec (AI)

**Status:** PROPOSED. **Route:** `hub/spaces`, chamber `hub/spaces/<space>`. **Accent:** purple. **Build order:** 9.

## Shell contract

Sidebar + Naya rail unchanged; center swaps. Chamber switching stays in-room.

## Component tree

1. `SpacesHero` — title + `ChamberSwitcher` + "New space."
2. `ChamberView` — `ChamberTabs` (Boards/Members/Activity) + tab content.
3. `BoardsTab` — the chamber's shared intelligence boards.
4. `MembersTab` — members with roles; invite/manage.
5. `ActivityTab` — chamber-scoped activity stream.
6. `SharingRules` — visible rule panel.

## Data bindings

- Spaces ← governed space records (membership, rules). Chamber content ← space-scoped intelligence (strictly isolated per space).

## States

- `loading`, `no_spaces` (onboarding), `no_access` (honest: "You're not a member"), `offline` (cached with stamp).

## Interactions

- New space → name/seal/invite flow → chamber created + receipt.
- Invite → invitation (governed) → member accepts → receipt. Role change / remove → consequence stated → receipt.
- Sharing rules edit → versioned + visible.
- Leave space → confirm with consequence → access revoked + receipt.

## Design tokens

Purple seals/markers; chambers feel like small Hubs (reuse room grammar at smaller scale).

## Acceptance

Cross-chamber isolation tested (no leakage); leave revokes for real; rules always visible; 9.0+.

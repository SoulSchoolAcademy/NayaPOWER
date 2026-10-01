# Smart Lists — Builder Spec (AI)

**Status:** PROPOSED. **Route:** `hub/lists`, list view `hub/lists/<list>`. **Accent:** yellow — frame-ticks and markers only (restrained). **Build order:** 7.

## Shell contract

Sidebar + Naya rail unchanged; center swaps.

## Component tree

1. `ListsHero` — title, lane-count overview, "New list."
2. `ListShelf` — collections as gallery frames (name, count, cover note).
3. `ActionLanes` — NOW / NEXT / WAITING / QUESTIONS / IDEAS / OPPORTUNITIES / COMPLETED.
4. `ActionItem` — title, WHY-THIS-IS-HERE line, pointer seal or task state, move/annotate/complete.
5. `SaveToList` (global) — picker modal invoked from any card anywhere.

## Data bindings

- Lists ← user collections (pointers to intelligence objects + native tasks). WHY lines ← dependency analysis or user annotation.

## States

- `loading`, `empty_lane` ("Nothing waiting. Good."), `empty_shelf` (onboarding: create first list).

## Interactions

- Drag or lane-picker moves items; annotate edits the why-line; complete asks for outcome link.
- SaveToList modal: searchable list picker → pointer added → toast.
- Share list → Connect preview → consent.

## Design tokens

Yellow restraint is law: ticks, markers, the WHY-line's left rule. Lanes calm, generous spacing.

## Acceptance

Pointers never duplicate content (verify: edit source, list reflects); why-lines real; completed items outcome-linked; 9.0+.

# Smart Spaces — AI Builder Spec

**Read first:** parent Hub contracts + FUNCTIONAL-SPEC + DESIGN-CONTRACT.

## Intent
Implement Space as governed context, not storage duplication. Active Space must affect real queries/interpretation and persist visibly across Hub rooms.

## Build order
1. Preserve shared Hub shell and Naya context.
2. Implement ORIENTATION → CURRENT STATE → INTELLIGENCE → ACTION → PROOF.
3. Build signature instrument before secondary controls.
4. Bind controls to governed runtime or honest unavailable states.
5. Preserve canonical object identity across handoffs.
6. Implement full state matrix.
7. Prove keyboard, responsive, reduced-motion, performance and continuity.

## Required components / views
- SpaceGallery
- SpacePortal
- ActiveSpaceIndicator
- SpaceHome
- SpacePurpose
- KeyIntelligence
- MembersConnections
- ProjectsGoalsRules
- SpaceActivity
- ScopedRoomLinks
- SpaceSwitcher

## Primary causal actions
- ENTER_SPACE
- CREATE_SPACE
- INVITE_CONNECT
- SET_PRIVACY_SHARING
- LINK_INTELLIGENCE
- OPEN_SPACE_FEED
- OPEN_SPACE_REPORT
- OPEN_SPACE_LISTS
- OPEN_SPACE_MAIL
- OPEN_MEMBERS
- ASK_NAYA_IN_SPACE
- ARCHIVE_LEAVE_IF_GOVERNED

## Data / runtime
Canonical context/Space membership + scoped intelligence + consent/privacy/runtime enforcement. Space projections query the same underlying intelligence IDs.

## Anti-patterns
- folder-only metaphor
- separate database per Space
- duplicated rooms inside rooms
- hidden context switch
- privacy label without enforcement

## Acceptance proof
- active Space changes real scoped results
- Space context persists across room navigation
- identity/Space scope remains visible
- privacy/share labels match enforcement
- same object IDs survive context views
- switching/leave/archive behaves safely

Independent review required.

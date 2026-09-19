# Smart Spaces — Engineering Specification

## What / why
Smart Spaces are NayaNET's topic-centered human interaction and collaboration environments. They are where people discover one another, communicate live/asynchronously, post, comment, share intelligence and build collective understanding.

## Human interface
A Space should show its topic, creator, membership/visibility, current participants/activity and available interaction modes. A prominent **+ Create Smart Space** action should be available from meaningful intelligent contexts where supported. Inside: live chat, posts, comments/replies, intelligence sharing and authorized Smart Mail actions.

## Front end requirements
- Space discovery/index.
- Space detail with topic and membership state.
- Create Space from Note/topic/board/team.
- Join/decline/leave flows.
- Live chat and asynchronous post/comment/reply surfaces.
- Share intelligence with explicit scope.
- Save participant as Connection.
- Smart Mail-to-Space action where authorized.
- Activity/invitation presentation.
- Loading/error/unauthorized/membership states.

## Back end requirements
- Space object + membership model.
- Origin/source references when created from intelligent context.
- Visibility and membership rules.
- Authorized interaction persistence.
- Activity events for relevant actions.
- Notification/invitation eligibility based on recent relevant interaction, privacy and notification settings.
- Item-level authorization for shared intelligence.
- AI-agent participation only under explicit authority.

## Data / API contract
Conceptual Space: `space_id, creator_id, topic/source_refs, name, description, visibility, membership_policy, created_at, status`. Membership and interaction records remain separate. Exact schemas/routes follow existing contracts.

## Connections
`Note/topic → Space`; `Space → Feed activity`; `Space → membership → Your Connections`; `Connections → Smart Mail / Smart List`; `Space → Mail`; `Space → Share`; `Space → collective intelligence candidates`; `Ledger → consequential events`.

## Relationship boundary

**JOIN is the primary social action.** INVITE is optional. A person may be surfaced as relevant without being contacted or joined automatically. Joining establishes participation in the Space's defined relationship boundary; it does not grant unrelated private-data or intelligence access. A connection projection must preserve the source Space/membership provenance.

## Important distinctions
`comment ≠ truth`; `like ≠ verification`; `consensus ≠ verification`; `membership ≠ private-data access`; `interest ≠ consent`. Creating an invitation from interaction signals does not automatically join someone or authorize messaging.

## Verification
Create Space from real source; prove source link; join/decline; post/comment/chat; verify activity projection; save participant; share authorized intelligence; test unauthorized intelligence; test membership removal/revocation; verify AI participation respects authority.

## Current state
**DEFINED** by `.naya/12` and `.naya/47`; exact runtime implementation remains to be reconciled with the source.

## Gap / next action
Inspect the current Space/activity/messaging implementation and establish the smallest complete authenticated Space lifecycle proof.

## Source authority
`.naya/2026-09-11-NAYAPOWER-12-SMART-SPACES-SMART-NOTE.md`; `.naya/2026-09-12-NAYAPOWER-47-SMART-SPACE-CONTRACT.md`; `.naya/2026-09-12-NAYAPOWER-43-SMART-FEED-ACTIVITY-PROJECTION-CONTRACT.md`; `.naya/2026-09-12-NAYAPOWER-44-DIRECT-ACTIVITY-EVENT-WRITE-ARCHITECTURE.md`.


## COMPLETION CHECKLIST — 2026-09-19

- [x] Source contract identified
- [x] .naya authority identified
- [x] Live Space primitives identified
- [ ] Deployed Space UI mapped
- [ ] Complete authenticated lifecycle proven
- [ ] Membership/revocation proven
- [ ] Activity projection proven
- [ ] Intelligence sharing authorization proven
- [ ] AI participation authority proven
- [ ] Source → build → runtime parity proven
- [x] Dated activity record exists
- [x] One next action recorded

**Current state:** FOUNDATION; not LIVE VERIFIED. See [2026-09-19 activity](../ACTIVITY/2026/09/19/SMART-SPACES.md).

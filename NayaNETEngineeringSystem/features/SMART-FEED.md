# Smart Feed — Engineering Specification

## What / why
Smart Feed is the living visual intelligence layer of the Hub. It presents three distinct streams: Activity, Personal Intelligence, Collective Intelligence. It surfaces useful intelligence without becoming canonical storage.

## Human interface
Primary Hub destination with an unmistakable stream selector: **ACTIVITY / PERSONAL / COLLECTIVE**. Support Smart Tabs/search as volume grows. Each item should make clear: what it is, why it appears, who can see it, source, verification state where relevant, and available actions. Actions may include open source, save/favorite, list, share, comment/reply/like on collective items, and Space-related actions where authorized.

States: loading, empty, populated, stale, error, unauthorized. Personal feed must not expose public-social mechanics merely because it is private.

## Front end requirements
- Feed route and navigation wired to canonical Hub.
- Stream selector with correct privacy context.
- Feed item component capable of source/provenance/state badges.
- Pagination/infinite loading without duplicate items.
- Smart Tab/category controls and search integration.
- Action menus respect authority.
- Optimistic actions reconcile against server response.
- Explain Naya-generated summaries versus source material.

## Back end requirements
- Authorized retrieval of Activity/Personal/Collective projections.
- Activity projection from canonical events; do not duplicate canonical intelligence.
- Stable item IDs and source references.
- Ranking inputs may include recency, relevance, novelty, relationship/context, explicit preferences, importance, verification and permissions.
- Popularity/engagement must not become truth.
- Item-level authorization before return.
- Idempotent save/favorite/share/interactions.
- Event emission for meaningful mutations.

## Data / API contract
Conceptual read model: `id, stream, source_type, source_id, actor/owner, event_at, created_at, visibility, verification_state, content_projection, relationship_refs, available_actions`. Exact schema must reuse existing feed/activity contracts.

Conceptual endpoints: `GET /feed?stream=...`, `GET /feed/tabs`, `POST /feed/:id/save`, `POST /feed/:id/favorite`, interaction endpoints as authorized. These are design targets, not claims that these routes already exist.

## Connections
`Smart Notes → Feed`; `events → Activity`; `Smart Share → Collective`; `Smart Lists/Library/Search/Today/Reports → discovery`; `Smart Spaces/Connections/Mail → actions`; `Ledger/Evidence → provenance`.

## Verification
Prove real authenticated retrieval; personal/private isolation; collective publication rules; source drill-down; save/list/share persistence; fresh retrieval; duplicate prevention; unauthorized second-user denial; source/build/runtime parity.

## Current state
**DEFINED** by `.naya/08` and reinforced by 43/44/45/49/50. Runtime completeness is not inferred from definition.

## Gap / next action
Inspect current Hub feed implementation and map each required stream/action to actual source/API/runtime before modifying code.

## Source authority
`.naya/2026-09-11-NAYAPOWER-08-INTELLIGENT-SMART-FEED-SMART-NOTE.md`; `.naya/2026-09-12-NAYAPOWER-43-SMART-FEED-ACTIVITY-PROJECTION-CONTRACT.md`; `.naya/2026-09-12-NAYAPOWER-44-DIRECT-ACTIVITY-EVENT-WRITE-ARCHITECTURE.md`; `.naya/2026-09-12-NAYAPOWER-50-INTELLIGENT-SEARCH-RETRIEVAL-CONTRACT.md`.

# 03 — Intelligence, Event and Data Contracts

## Canonical object rule
The system distinguishes **content → information → intelligence → learning → wisdom**. A product projection is not automatically canonical.

## Core object families
- **Smart Note:** durable meaningful intelligence event.
- **Feed Activity:** time-sensitive projection/event; not necessarily durable intelligence.
- **Smart List:** collection/reference over canonical objects; membership is its own relationship.
- **Smart Mail:** intentional message-delivery object referencing canonical intelligence where attached.
- **Smart Space:** topic-centered interaction environment with membership and communication state.
- **Smart Share:** explicit sharing operation and resulting scope/receipt.
- **Ledger Event:** integrity/provenance/evidence record for meaningful system events.
- **Today:** derived daily synthesis referencing source objects/events.
- **Report:** derived longer-period synthesis referencing source objects/events.

## Minimum common metadata
Where applicable, objects/events should provide stable ID, actor/owner/scope, created_at/updated_at or event_at, visibility/privacy state, provenance/source references, status, and relationships. Exact schemas must reuse existing contracts when present.

## Relationship model
```text
SMART NOTE ──member-of──> SMART LIST
SMART NOTE ──projected-to──> SMART FEED
SMART NOTE ──summarized-by──> TODAY / REPORT
SMART NOTE ──shared-via──> SMART SHARE
SMART NOTE ──discussed-in──> SMART SPACE
CONNECTION ──receives──> SMART MAIL
ACTION ──produces──> EVENT / RECEIPT / LEDGER RECORD
EVENT ──contributes-to──> INTELLIGENCE
```

## Event envelope
Conceptual shape:
```text
id
actor_id
actor_type
authority_scope
event_type
target_type
target_id
source_type/source_id
occurred_at
created_at
correlation_id / lineage where required
result_state
provenance
```
This is a contract checklist, not permission to create duplicate event systems.

## Front-end contract
Each screen must consume a documented read model/API. Mutations must return enough information to reconcile UI state and display success/failure. The UI must distinguish source content, Naya-generated synthesis, activity, and verified state.

## Back-end contract
- Validate schemas at boundaries.
- Resolve canonical object before mutation.
- Enforce authority/privacy server-side.
- Preserve stable references rather than copying intelligence.
- Emit idempotent events for meaningful state transitions.
- Maintain provenance/lineage where required.
- Make derived views reproducible from canonical inputs where practical.

## Derived surfaces
Today, Reports, Feed, Tabs and other views may cache/materialize projections for performance, but the design must identify their canonical inputs and invalidation/rebuild behavior. A derived summary must never silently become the new source of truth.

## Search/retrieval
Search is a retrieval mechanism over authorized canonical objects and projections. Search ranking is not truth. Retrieval must preserve privacy and provenance.

## Source authority
01–58 system directive; `.naya/2026-09-11-18-35-NAYAPOWER-32-MASTER-SYSTEM-ARCHITECTURE.md`; `.naya/2026-09-12-NAYAPOWER-39-CROSS-SYSTEM-EVENT-CONTRACT.md`; `.naya/2026-09-12-NAYAPOWER-42-SMART-NOTE-INTELLIGENT-BLOCK-DATA-CONTRACT.md`; `.naya/2026-09-12-NAYAPOWER-43-SMART-FEED-ACTIVITY-PROJECTION-CONTRACT.md`; `.naya/2026-09-12-NAYAPOWER-44-DIRECT-ACTIVITY-EVENT-WRITE-ARCHITECTURE.md`.

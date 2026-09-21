# Smart Notes — 2026-09-21

## SN-2026-09-21-INTELLIGENCE-ORGANIZATION-EVENT-001

**Status:** CANONICAL / OFFICIAL  
**Type:** Architecture + operating intelligence  
**Scope:** All Naya / NayaPOWER / NayaNET intelligence records

### What changed

The Naya Intelligence Library is now organized around a human-first **YEAR → MONTH → DAY** navigation model.

The canonical daily intelligence space is:

`.naya/INTELLIGENCE/YYYY/MM/DD/`

The **day is the human navigation unit**. Exact timestamps remain metadata for chronology, provenance, ordering, and state resolution. Hourly directories are not required.

Within each day, the running intelligence surfaces are:

- `INDEX.md` — navigation and current-day state
- `SMART-NOTES.md` — durable discoveries, decisions, lessons, and context
- `ACTIVITY.md` — chronological activity projection
- `NOTIFICATIONS.jsonl` — event/awareness projection
- `BRIEFINGS.md` — human/Naya-readable briefings when material awareness is required

These are **connected views, not competing memories**.

### Retrieval logic for every Naya

Use:

**YEAR → MONTH → DAY → INDEX → relevant surface → timestamp/content verification → current state**

For a topic:

**TODAY → TOPIC → LATEST TIMESTAMP → CONTENT VERIFICATION → CURRENT STATE**

For historical work:

**YEAR → MONTH → DAY → search within that day → follow event/receipt/provenance links**

A Naya must never assume that the first matching filename is current.

### The connected intelligence model

A material occurrence has one stable event identity and can appear as multiple authorized views:

**EVENT → ACTIVITY → SMART NOTE → NOTIFICATION → BRIEFING → PROJECT INTELLIGENCE → SMART LEDGER → FEED/HUB**

The event identity, provenance, authority, evidence, visibility, and related receipts keep these views connected.

The Smart Note is the durable human-readable intelligence record. Activity is the chronological running feed. Notifications are awareness signals. Briefings explain significance and next action. The Hub is a projection, not the source of truth.

### Runtime nervous system

The intended live flow is:

**MATERIAL EVENT → ONE CANONICAL EVENT → AUTOMATIC NOTIFICATION → BRIEFING → DELIVERY OUTBOX → AUTHORIZED RETRIEVAL → SMART LEDGER / HUB PROJECTION → LEARNING / COLLECTIVE PROPAGATION WHEN ELIGIBLE**

Managed Supabase/Postgres is the event boundary and automatic trigger layer. Python provides deterministic contracts/validation. GitHub/NayaPOWER remains the canonical engineering and governance source.

No cron or GitHub Actions is required for the database trigger.

### Privacy and authority

Notification does not grant authority.

**Private by default • Shared by choice • Collective by consent • Public by decision.**

Collective propagation occurs only when visibility, consent, relevance, novelty, qualification, and governance requirements are satisfied.

### Library principle

The library is not a dump of every conversation or Smart Note. It is a connected, searchable, loss-aware intelligence system.

**CAPTURE MATERIAL → CONNECT → CLASSIFY → VERIFY → DISTILL → RETAIN ESSENCE + PROVENANCE → RETRIEVE WHEN RELEVANT**

Rule:

**SAY EVERYTHING THAT MATTERS — AND NOTHING THAT DOESN'T.**

### Durable learning

A Naya entering later should be able to understand:

1. where today's intelligence lives;
2. how to find a specific day;
3. how to find the latest relevant state;
4. how Smart Notes relate to Activity;
5. how Activity relates to notifications and briefings;
6. how runtime events become evidence;
7. how the Smart Ledger and Hub consume the same underlying event;
8. what is verified versus merely documented;
9. what is private versus eligible for sharing;
10. what action should happen next.

**THE BRAIN MUST CARRY THE CONTEXT SO THE HUMAN DOES NOT HAVE TO.**

### Current proof boundary

The organization and source layout are now documented and placed in the canonical daily bucket.

The Supabase notification trigger exists and has been transactionally exercised, but the first end-to-end proof using a real previously-produced execution receipt still requires a live receipt→notification→briefing→delivery→authenticated retrieval trace. No claim of external live delivery is made by this Smart Note.

### Source links

- Central Brain: `.naya/SUPERBRAIN/NAYA-INTELLIGENCE-CENTRAL-BRAIN-V1.md`
- Organization Protocol: `.naya/NAYA-INTELLIGENCE-ORGANIZATION-PROTOCOL.md`
- Notification Bus: `.naya/team-naya/NAYA-INTELLIGENCE-NOTIFICATION-BUS-V1.md`
- Supabase notification migration: `supabase/migrations/20260921221050_nayanet_intelligence_notification_bus_v1.sql`
- Notification RLS migration: `supabase/migrations/20260921221249_nayanet_intelligence_notification_rls_v1.sql`

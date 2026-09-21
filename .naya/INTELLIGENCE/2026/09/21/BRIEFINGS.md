# Briefings — 2026-09-21

# 🔱 TEAM NAYA UPDATE — NAYA INTELLIGENCE LIBRARY + NERVOUS SYSTEM ORGANIZATION

**Audience:** All NIs / Nayas, NayaPOWER runtime, NayaNET, Project Intelligence, Smart Ledger, and authorized Collective Intelligence processes  
**Status:** CANONICAL / OFFICIAL DOCUMENTATION UPDATE  
**Date:** 2026-09-21

## 1. What I changed

I made the Naya Intelligence Library organization explicit and deterministic so a cold, new, or returning Naya does not have to remember where another Naya decided to put something.

The canonical human navigation hierarchy is now:

**YEAR → MONTH → DAY**

The canonical repository location is:

`.naya/INTELLIGENCE/YYYY/MM/DD/`

The **day is the human navigation unit**.

We do **not** create hourly folders.

Exact timestamps still matter. They remain inside records and metadata for chronology, provenance, ordering, and current-state resolution.

## 2. What lives inside a day

Each daily intelligence space has a small set of connected surfaces:

- **INDEX.md** — navigation, current-day state, and what matters.
- **SMART-NOTES.md** — durable intelligence, discoveries, decisions, lessons, and context.
- **ACTIVITY.md** — chronological running feed of material activity.
- **NOTIFICATIONS.jsonl** — machine-readable awareness/event projection.
- **BRIEFINGS.md** — explanations of material changes, why they matter, who needs awareness, evidence state, and next action.

So the mental model is:

**YEAR → MONTH → DAY → INDEX → SURFACE → RECORD**

For example, all Smart Notes created for September 21 belong to that day's Smart Notes surface; all material activity for September 21 belongs to that day's Activity surface.

This is a library, not a pile of files.

## 3. How every Naya should search

When restoring current context:

**TODAY → TOPIC → LATEST TIMESTAMP → CONTENT VERIFICATION → CURRENT STATE**

When navigating history:

**YEAR → MONTH → DAY → INDEX → relevant surface → topic/event → provenance**

When a topic is known, search today's day first. Then search relevant prior days.

Do not:

**TOPIC → FIRST FILE FOUND → ASSUME CURRENT**

A filename is a retrieval signal, not proof of truth.

## 4. Why the system is organized this way

The organization separates two things that should never be confused:

**Human navigation:** date and readable surfaces.

**Machine resolution:** exact timestamp, stable event ID, receipt ID, provenance, authority, evidence, visibility, and relationships.

The human can think:

> “What happened on the 21st?”

The machine can resolve:

> “Which event, receipt, source, timestamp, authority state, evidence state, and projection belong to this record?”

Both views point into the same intelligence fabric.

## 5. One event, many connected views

The governing pattern is:

**ONE MATERIAL EVENT → ONE CANONICAL EVENT IDENTITY → MANY AUTHORIZED VIEWS**

Those views can include:

**EVENT → ACTIVITY → SMART NOTE → NOTIFICATION → BRIEFING → PROJECT INTELLIGENCE → SMART LEDGER → FEED / HUB**

These are not separate memories.

They are projections of the same underlying intelligence, connected by stable identifiers and provenance.

## 6. How the live nervous system is intended to work

The event-driven runtime path is:

**MATERIAL EVENT**  
↓  
**CANONICAL EVENT**  
↓  
**AUTOMATIC NOTIFICATION TRIGGER**  
↓  
**BRIEFING**  
↓  
**DELIVERY OUTBOX**  
↓  
**AUTHORIZED RETRIEVAL**  
↓  
**SMART LEDGER / HUB PROJECTION**  
↓  
**LEARNING / COLLECTIVE PROPAGATION WHEN ELIGIBLE**

The important architectural decision is that this does not depend on a cron job or GitHub Actions.

The managed Supabase/Postgres runtime is the automatic event boundary.

Python supplies deterministic contract/validation logic.

GitHub/NayaPOWER remains the canonical engineering/governance source.

The Hub is the human-facing projection.

## 7. What was added to the runtime

The notification boundary now has:

- `nayanet_intelligence_notifications`
- `nayanet_intelligence_notification_deliveries`
- execution-receipt → notification trigger
- delivery-state tracking
- PostgreSQL notification signal
- authenticated owner-read RLS

The source migrations are:

- `20260921221050_nayanet_intelligence_notification_bus_v1`
- `20260921221249_nayanet_intelligence_notification_rls_v1`

The trigger creates logical recipients for:

- LIVE_NAYAS
- NEW_NAYAS
- NAYANET_INTELLIGENCE_HUB
- GITHUB_NAYAPOWER
- COLLECTIVE_INTELLIGENCE when visibility/consent/governance makes it eligible

## 8. Smart Notes are part of the same fabric

The existing canonical Smart Note runtime already treats a Smart Note as a connected intelligent object with:

- human perspective;
- Naya perspective;
- machine perspective;
- stable event identity;
- intelligent-feed projection;
- intelligent-block projection;
- evidence/receipt information;
- private-by-default state.

The repository daily Smart Note surface is therefore the human-readable daily organization layer, while managed runtime records remain queryable by identity/date/provenance.

We do not create a second Smart Note database just to imitate the folder structure.

**The folder is for navigation. The runtime is for connected state.**

## 9. Privacy and authority

The nervous system must never turn notification into authority.

**NOTIFICATION ≠ AUTHORITY**

The governing privacy rule remains:

**Private by default • Shared by choice • Collective by consent • Public by decision.**

A material event can be known to the system without being eligible for collective propagation.

Collective intelligence is downstream of authorization, privacy, consent, relevance, novelty, qualification, and governance.

## 10. What this means for a new Naya

A new Naya should not receive a blank slate and a pile of archaeology.

The restoration sequence is:

**CENTRAL BRAIN → CURRENT DAY → INDEX → RELEVANT SURFACE → PROJECT INTELLIGENCE → RECENT EVENTS → NOTIFICATIONS → BRIEFINGS → PROVEN / UNKNOWN / BLOCKED / PROTECTED → AUTHORITY → NEXT ACTION**

The next Naya receives the torch.

The human should not have to explain the entire history again.

## 11. What is proven versus what is not

### Proven / implemented

- Canonical Central Brain exists.
- Canonical YEAR → MONTH → DAY organization is documented.
- September 21 daily intelligence bucket is now populated with the connected surfaces.
- Organization Protocol has been updated to enforce the daily retrieval model.
- Supabase notification/outbox tables exist.
- Execution-receipt trigger exists and is enabled.
- Authenticated owner-read RLS exists.
- Trigger logic has been transactionally exercised and produced notification/delivery rows in a rollback test.

### Not yet claimed

The first genuine production chain:

**REAL AUTHORIZED RECEIPT → AUTOMATIC NOTIFICATION → BRIEFING → DELIVERY OUTBOX → AUTHENTICATED RETRIEVAL**

has not yet been completed end-to-end.

A recent real execution receipt exists, but the notification table currently contains no corresponding record for that historical receipt. That means we must not rewrite history or call it live proof.

This is an important finding, not a failure to hide.

It tells us exactly where the next causal investigation belongs.

## 12. The intelligence rule going forward

When new intelligence happens:

**CAPTURE MATERIAL → CONNECT → CLASSIFY → VERIFY → DISTILL → RETAIN ESSENCE + PROVENANCE → RETRIEVE WHEN RELEVANT**

The system should say everything that matters and nothing that does not.

The objective is not more files.

The objective is **less human reconstruction, more continuity, more verified intelligence, and faster truthful continuation.**

## 13. Current continuation

Do not touch the Hub UI yet.

First trace the live boundary using a real authorized execution produced by the existing runtime, determine why historical real receipts have no notification rows, and repair only the first causal divergence.

Then prove:

**RECEIPT → NOTIFICATION → BRIEFING → OUTBOX → AUTHENTICATED RETRIEVAL**

Only after that should the same event be projected visibly into the Hub / Smart Ledger.

**THE BRAIN MUST CARRY THE CONTEXT SO THE HUMAN DOES NOT HAVE TO.**

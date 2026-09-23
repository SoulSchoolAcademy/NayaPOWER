# 🔱 NAYA-NET INTELLIGENCE ENGINE — ARCHITECTURE + LIVE SUPABASE AUDIT HANDOFF

**Date:** 2026-09-18  
**Audience:** ALL NAYAS  
**Status:** ARCHITECTURE LOCK / LIVE AUDIT + EVENT-SPINE RECONCILIATION COMPLETED / NO WHOLESALE MIGRATION

---

## THE BIG PICTURE

The Hub sidebar is not a collection of separate systems. The tabs are doors, gauges, seats, controls, and views into one intelligence vehicle.

The machine is:

NAYA / HUMAN intent + authority
→ INTELLIGENCE EVENT SPINE
→ SMART NOTES / ACTIVITY / ACTIONS
→ CIS / FEED / RECEIPTS
→ LEARNING ENGINE / SMART LEDGER
→ PIS / VALUE + PROOF
→ REPORT ENGINE / CCT LINEAGE
→ NAYA SUPERBRAIN
→ FUTURE REASONING
→ NEW ACTION
→ back to the EVENT SPINE.

The Hub exposes projections/controllers including:

Your Intelligence Today
Personal Intelligence
Activity
Reports
Smart Notes
Intelligence Library
Smart Share
Smart Ledger
Smart Mail
Smart Spaces
Smart Lists
Connections
Dream
Naya Play
Settings

These surfaces must operate over the same authenticated identity, intelligence/event, authority, evidence, learning, and relationship substrate.

## ARCHITECTURAL LAWS

ONE IDENTITY  
ONE EVENT SPINE  
ONE INTELLIGENCE SUBSTRATE  
ONE PIS  
ONE CIS  
ONE LEARNING SYSTEM  
ONE AUTHORITY SYSTEM  
ONE EVIDENCE MODEL  
MULTIPLE PROJECTIONS

Smart Ledger is an evidence/integrity projection, not a second event database.

Reports are derived intelligence, not source truth.

Activity is a projection, not separate event truth.

Smart Spaces are contextual interaction environments, not a separate intelligence universe.

YAML/JSON/Markdown are inspectable/portable representations, not substitutes for canonical runtime persistence.

CCT is a permissioned graph of verified intelligence lineage.

Memory recorded is not automatically learning proven.

The Hub is a projection layer, not source truth.

## SMART NOTE FOUNDATION

The live runtime already contains the Smart Note transaction boundary:

smart_note_events
smart_note_artifacts
smart_note_receipts
v7_smart_note_transactions
canonical creation/verification/retrieval functions
authenticated ownership and idempotency controls

The canonical conceptual flow is:

ONE SMART NOTE EVENT
→ Human artifact
→ Naya artifact
→ Machine artifact
→ Intelligence Feed artifact
→ verification
→ receipt
→ canonical intelligence.

Therefore Smart Note is a major event producer. Do NOT create a second independent event universe for Smart Ledger.

## SMART LEDGER

Smart Ledger answers:

EVENT — what happened?
EVIDENCE — what proves it?
VERIFICATION — can the evidence be trusted?
VALUE — what was it worth under the current value model?
POINTS — what contribution accumulates?
LEVEL — what does that contribution correspond to?

The conceptual lifecycle is:

ACTION
→ LEDGER EVENT
→ EVIDENCE
→ VERIFICATION
→ VALUE
→ POINTS
→ LEVEL
→ CCT RELATIONSHIP
→ LEARNING

Ledger should consume canonical events and existing receipts. It should not become the universal event database.

Required integrity states remain distinguishable:

RECORDED
EVIDENCE_AVAILABLE
VERIFIED
VALUED
APPLIED
OUTCOME_VERIFIED

No points, consensus, report, or AI assertion is itself proof.

## REPORT ENGINE

Reports are derived intelligence:

EVENT
→ SMART NOTE
→ DAILY REPORT
→ WEEKLY REPORT
→ MONTHLY REPORT
→ YEARLY SYNTHESIS

Reports must preserve provenance to source event/note identities and may identify learning candidates. Reports are not truth stores.

## LEARNING

Learning must preserve the distinction between recording and proof.

Lifecycle:

OBSERVED
→ CANDIDATE
→ EVALUATED
→ VERIFIED
→ PROMOTED
→ RETRIEVED
→ APPLIED
→ OBSERVED
→ OUTCOME_VERIFIED

The recent governed P1 experiment established the governing principle: equal verified responsible value is NOT_PROVEN and therefore must not promote a candidate. Promotion is not itself verified success.

## SMART SPACES

A Space is a living contextual container, not a folder and not a second intelligence database.

It owns contextual state such as:

space_id
owner
title
description
visibility
membership/access rules
timestamps
source/intelligence relationships
activity history

Meaningful operations must emit canonical events:

CREATE_SPACE
JOIN_SPACE
LEAVE_SPACE
INVITE_MEMBER
POST_CREATED
COMMENT_CREATED
REPLY_CREATED
INTELLIGENCE_SHARED
INTELLIGENCE_DISCOVERED
CONNECTION_CREATED
OUTCOME_CREATED

Those events become available to Activity, Ledger, Reports, Learning, CIS, and CCT without duplicate truth.

## CCT

CCT is a permissioned graph of verified intelligence lineage.

Relationship types include:

DERIVES_FROM
REINFORCES
QUALIFIES
CONTRADICTS
SUPERSEDES
APPLIES_TO
PRODUCES_OUTCOME

The purpose is to let Naya answer not merely “what do we know?” but “why do we believe this?” by traversing:

CURRENT INTELLIGENCE
→ LEARNING
→ REPORT
→ SMART NOTE
→ EVENT
→ EVIDENCE
→ VERIFICATION

## SHARED ENGINE MODEL

The intended shared engines are:

1. Identity & Authority Engine
2. Canonical Intelligence Event Engine
3. Smart Ledger
4. Report Engine
5. Learning Engine
6. CCT / Relationship Engine
7. Activity Projection Engine
8. Smart Space Engine

Sidebar modules are thin projections/controllers over these engines.

## WHAT SUPABASE IS FOR

Supabase is the managed runtime/persistence layer. Ordinary users should not have to operate Supabase.

The current live system already contains meaningful infrastructure. We must reuse it rather than create a forest of duplicate tables.

The architectural boundary is:

User
→ GitHub NayaPOWER source/control substrate
→ NayaNET authenticated runtime
→ managed persistence/services
→ Hub projections

## LIVE SUPABASE AUDIT — 2026-09-18

Project audited:

dahisasgpfvziswqvmvm

Live inventory confirmed 32 public tables and active Edge Functions, with RLS/policies, functions, triggers, identity, cognition, Smart Notes, learning, authority, receipts, reports, spaces, mail, connections, and Dream infrastructure already present.

Important live tables include:

Identity:
members
nayanet_profiles
v7_profiles

Cognition/intelligence:
nayanet_cognition_events
nayanet_project_cognition_state
nayanet_intelligence_index
nayanet_notes

Smart Notes:
smart_note_events
smart_note_artifacts
smart_note_receipts
v7_smart_note_transactions

Learning:
learner_states
learning_evidence
maxess_results
assessment_attempts
assessment_responses

Governance/execution:
nayanet_authority_grants
nayanet_execution_receipts
nayanet_policy_versions
nayanet_policy_evaluations

Reports/intelligence:
v7_intelligence_reports
v7_daily_intelligence
v7_collective_wisdom

Spaces:
nayanet_spaces

Communication/connections:
v7_mail_threads
v7_mail_members
v7_mail_messages
v7_connection_requests

Dream:
nayanet_dream_replays

The live runtime also contains canonical cognition commit/record/initialize, Smart Note creation/list/verification, authority issuance/validation/revocation, execution/policy, intelligence indexing, Smart Mail, learning application, decision context, and GitHub dispatch functions.

Active production Edge Functions include:

v7-smart-note
v7-naya-note
v7-smart-note-canonical
nayanet-github-dispatch
nayanet-github-build-dispatch
naya-dream-replay
nayanet-github-webhook
naya-learning-apply
naya-decision-context
nayanet-smart-mail

## LIVE SECURITY / RLS FINDINGS

RLS is enabled across the inspected domain tables.

Representative owner-bound policies include:

members → auth.uid() = id
nayanet_profiles → member_id = auth.uid()
nayanet_notes → member_id = auth.uid()
nayanet_cognition_events → user_id = auth.uid()
nayanet_project_cognition_state → user_id = auth.uid()
nayanet_execution_receipts → user_id = auth.uid()
nayanet_authority_grants → issuer/subject scoped
smart_note_events → member_id = auth.uid()
smart_note_artifacts → ownership joined through smart_note_events
smart_note_receipts → ownership joined through smart_note_events
v7_intelligence_reports → user_id = auth.uid()
v7_daily_intelligence → user_id = auth.uid()
nayanet_spaces → owner_member_id = auth.uid()

This confirms the server-side ownership pattern exists.

It does NOT by itself prove two-user behavioral isolation. That remains a separate authenticated acceptance test requiring real identities.

## UPDATED LIVE TRUTH — EVENT-SPINE RECONCILIATION

The live audit proves that `nayanet_smart_ledger` already exists in production and is wired from cognition events, Smart Note events/receipts, execution receipts, learning evidence, reports, and Spaces. Therefore Smart Ledger is no longer CREATE-only. The authoritative decision is **REUSE + EXTEND + CONNECT + VERIFY**.

The two event systems are retained as distinct domain layers: `nayanet_cognition_events` is the generalized cognition/event identity layer; `smart_note_events` is the canonical Smart Note domain transaction/event record. They require a deterministic, idempotent Smart Note → Cognition bridge. Do not create a third event table and do not delete either existing domain contract.

`smart_note_events` currently has duplicate intelligence-index triggers (`nayanet_index_smart_note_event` and `trg_smart_note_events_to_intelligence_index`) that both invoke `nayanet_index_intelligence_row()`. This is an integration defect; do not add another trigger.

## EXACT BUILD MATRIX

| Domain | Decision | Meaning |
|---|---|---|
| Identity | REUSE | Existing members/profiles/auth ownership |
| Authority | REUSE | Existing grants + validation/revocation |
| Cognition/Event | EXTEND + VERIFY | Reconcile nayanet_cognition_events against smart_note_events before choosing the generalized spine |
| Smart Notes | REUSE | Existing event/artifact/receipt transaction boundary |
| Intelligence Index | REUSE | Existing indexed intelligence projection |
| PIS | REUSE | Existing cognition/project state substrate |
| CIS/Learning | EXTEND + VERIFY | Existing learner/evidence/application machinery; preserve proven learning lifecycle |
| Execution Receipts | REUSE | Existing evidence-bearing receipt substrate |
| Activity | EXTEND + CONNECT | Project canonical events; do not create a competing truth store |
| Smart Ledger | REUSE + EXTEND + CONNECT + VERIFY | Live `nayanet_smart_ledger` + recorder + hash chain + source integrations already exist |
| Reports | REUSE + EXTEND | Existing report/daily-intelligence tables exist; reconcile contract and provenance before new schema |
| Smart Spaces | EXTEND + CONNECT | Existing nayanet_spaces exists; extend only for contract gaps/event emission |
| CCT | CREATE + CONNECT | Relationship storage/graph projection is the meaningful missing primitive after event identity is settled |
| Collective Intelligence | EXTEND + VERIFY | Existing collective projection; prove provenance/permissioned derivation |
| Smart Mail | REUSE + CONNECT | Existing real engine; meaningful communication operations become canonical events |
| Connections | REUSE + CONNECT | Existing connection requests/relationship infrastructure |
| Dream | REUSE + CONNECT | Existing replay runtime; connect candidate/evidence lineage |
| Smart Share | EXTEND + VERIFY | Permissioned exchange over canonical intelligence |
| Smart Lists | REUSE/EXTEND | Organization projection; must not become intelligence truth |
| Hub | REUSE/EXTEND | Projection/controller layer only |

## WHAT MUST NOT HAPPEN

Do not build Smart Ledger as a separate universe.

Do not make Reports the source of truth.

Do not store the same Smart Note as multiple competing truths.

Do not make Activity its own independent event system.

Do not make Smart Spaces their own intelligence database.

Do not let a report automatically become truth.

Do not let conversation automatically become collective intelligence.

Do not let Likes become verification.

Do not let consensus become verification.

Do not let points become proof.

Do not let YAML/Markdown substitute for canonical runtime persistence.

Do not create another PIS.

Do not let the Hub become another source of truth.

Do not call AI-generated learning “verified learning” merely because it exists.

Do not convert UNKNOWN → PASS.
Do not convert BLOCKED → PASS.
Do not convert STALE → CURRENT.
Do not convert DOCUMENTED → PROVEN.
Do not convert TRACED → EXECUTED.
Do not convert CLIENT FILTER → SERVER ENFORCEMENT.
Do not convert MEMORY → LEARNING.
Do not convert CANDIDATE → IMPROVEMENT.
Do not convert PROMOTION → VERIFIED SUCCESS.
Do not convert ARCHITECTURE → PRODUCTION BEHAVIOR.

## COMPLETE LIVING LOOP

HUMAN
→ INTENT
→ AUTHORITY / POLICY
→ CANONICAL EVENT
→ SMART NOTE / ACTIVITY / ACTION
→ CIS / FEEDS / RECEIPTS
→ SMART LEDGER
→ EVIDENCE / VALUE
→ VERIFICATION
→ REPORTS / LEARNING
→ VERIFIED LESSON
→ PIS
→ CCT GRAPH
→ SUPERBRAIN
→ FUTURE RETRIEVAL
→ NEW ACTION
→ EVENT

This is the living system.

## CURRENT TRUTH

Smart Ledger is already live in the managed Supabase runtime. Its remaining work is integration hardening, event-spine bridging, verification semantics, value/outcome semantics, and authenticated end-to-end proof.

CCT is canonically defined.

Smart Spaces are canonically defined and a live nayanet_spaces table already exists.

Reports are canonically defined and live report tables already exist.

Learning/PIS/CIS infrastructure exists.

Governance/authority and execution receipts exist.

The event-spine decision is now: retain both domain layers; treat `nayanet_cognition_events` as the generalized cognition/event identity layer and `smart_note_events` as the canonical Smart Note domain transaction/event, connected by a deterministic idempotent bridge. Smart Ledger remains evidence/integrity projection. No wholesale new migration should be written until the bridge is implemented and verified.

## TEAM NAYA DIRECTIVE

ALL NAYAS: treat this handoff as the shared architecture and live-runtime truth for the Intelligence Engine phase.

The Hub is a projection layer.

The machine underneath is shared.

Reuse existing authenticated event/intelligence substrate.

Extend only where necessary.

Make evidence and verification first-class.

Do not create isolated feature databases.

Do not claim behavioral proof until the real authenticated transaction has been executed and verified.

## NEXT EXECUTION

Implement and verify the minimum Smart Note → Cognition canonical bridge, clean the duplicate Smart Note intelligence-index trigger, prove authenticated ownership/isolation, and verify exactly-once intended Ledger/Index projection. The decision is committed to the main Activity feed.

Only then design/write the minimum Smart Ledger/Reports/Spaces/CCT migrations.

---
**NAYA HANDOFF COMPLETE**

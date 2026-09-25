> **2026-09-25 RECONCILIATION:** The authoritative Smart Note / Intelligent Block contract is `.naya/codex/CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-SYSTEM-V1.md`. This project-intelligence document is preserved as a derived architecture projection and must not define a competing identity, registry, storage path, or lifecycle.

# INTELLIGENT EVENT V1 — CANONICAL CONTRACT — DERIVED PROJECT PROJECTION

STATUS: DERIVED PROJECT PROJECTION — NON-AUTHORITATIVE
VERSION: V1
EFFECTIVE: 2026-09-21

## Purpose

An Intelligent Event is the canonical record of a meaningful occurrence in the intelligence lifecycle.

It is broader than Smart Note creation. An event may represent something created, discovered, connected, corrected, verified, understood, distilled, delivered, applied, measured, learned, questioned, answered, superseded, or otherwise changed in a way that can create or preserve human value.

The event ledger is the temporal spine of NayaNET intelligence.

## Core distinction

**INTELLIGENT EVENT = WHAT HAPPENED**

**INTELLIGENT BLOCK = WHAT IS CURRENTLY UNDERSTOOD ABOUT IT**

An event can exist before understanding exists. Understanding can be revised by later events. An Intelligent Block may be derived from one event or many events.

## Canonical lifecycle

EXPERIENCE
→ CAPTURE
→ IDENTIFY
→ VERIFY
→ UNDERSTAND
→ CONNECT
→ DISTILL
→ VALUE
→ RETAIN / LET GO OF WORKING DETAIL
→ APPLY
→ OUTCOME
→ LEARN
→ NEW EVENT

Not every event must traverse every state synchronously. The event remains the historical fact/provenance anchor while downstream understanding evolves.

## Event classes

- CREATE — something was intentionally created.
- DISCOVER — something previously unknown or unnoticed was found.
- OBSERVE — a meaningful state or occurrence was observed.
- CONNECT — a meaningful relationship was established.
- QUESTION — an unresolved question was identified.
- ANSWER — a question received a candidate or verified answer.
- CORRECT — prior understanding was corrected.
- VERIFY — evidence established or rejected a claim.
- UNDERSTAND — a concept reached a defined understanding state.
- DISTILL — useful meaning was compressed without losing required truth/provenance.
- NOTIFY — meaningful intelligence was surfaced to an authorized recipient.
- DELIVER — intelligence reached its intended delivery boundary.
- APPLY — understanding was used in an action.
- OUTCOME — an observable consequence occurred.
- LEARN — an outcome changed durable understanding or future behavior.
- MEASURE — an observable metric was recorded.
- RETAIN — intelligence was deliberately preserved for future use.
- RELEASE — working detail was deliberately allowed to leave active context while provenance remains recoverable.
- SUPERSEDE — a newer verified understanding replaces an older active understanding.
- HANDOFF — successor context and next action were created.
- REJECT — a candidate understanding, action, or claim was rejected with reason/evidence.
- SYSTEM — a governed system event that materially affects intelligence continuity.

## Required event identity

Every canonical event MUST have:

- event_id
- event_type
- occurred_at
- recorded_at
- actor_type
- actor_identity or privacy-safe actor reference
- owner_scope
- source
- source_identity
- causal_parent_event_ids when known
- evidence_refs when applicable
- status
- provenance
- value assessment
- understanding state
- retention state
- created_by / execution identity
- schema_version

## Provenance

Provenance MUST distinguish:

- where the event originated;
- what system recorded it;
- what evidence supports it;
- what transformation produced any derived intelligence;
- what source HEAD / runtime / workflow identity applies when technical execution is involved.

No derived intelligence may erase the provenance of its source events.

## Evidence states

- UNVERIFIED
- PARTIALLY_VERIFIED
- VERIFIED
- REJECTED
- SUPERSEDED
- UNKNOWN

Unknown is not success.

## Value model

An event may carry structured value dimensions:

- human_benefit
- usefulness
- helpfulness
- relevance
- urgency
- consequence
- effort_avoided
- risk_reduced
- confidence
- harm
- cost
- uncertainty

Value is not a decorative score. It exists to help determine what should be surfaced, retained, applied, or distilled.

The governing objective remains:

**HIGHEST RESPONSIBLE VERIFIED HUMAN VALUE**

No value claim overrides safety, authority, privacy, provenance, or verification.

## Understanding state

- CAPTURED
- CONTEXTUALIZED
- INTERPRETED
- VERIFIED
- DISTILLED
- APPLIED
- LEARNED

An event can be captured without being understood.

## Human question protocol

Naya should first attempt to answer or resolve uncertainty from existing authorized intelligence.

Ask the human only when ambiguity is consequential or the human's intent/authority is genuinely required.

Default interaction rule:

- ask up to 3 high-leverage questions at a time;
- never exceed 10 unresolved questions in one interaction unless the human explicitly requests an interview/questionnaire;
- read the inferred understanding back to the human;
- expose material assumptions;
- let the human correct the model;
- record consequential corrections as events.

## Retention / release

**RELEASE IS NOT DELETION.**

When intelligence has been understood and no longer needs active working detail, Naya may release the detail from active context while retaining the minimum provenance and recoverability required by policy.

Retention decisions MUST distinguish:

- active_working
- durable_understanding
- historical_provenance
- superseded
- releasable_detail
- deletion_authorized

Never silently erase the causal history required to verify a claim.

## Event relationship rules

1. One event may produce zero, one, or many Intelligent Blocks.
2. One Intelligent Block may summarize, reconcile, or depend on many events.
3. An event does not become false because its interpretation changes.
4. A later verified event may supersede an earlier understanding without erasing the earlier event.
5. Notifications, learning records, applications, and outcomes are all legitimate event classes.
6. Event identity must remain stable across projection, retrieval, reload, and successor consumption.
7. Duplicate delivery must not create duplicate canonical events when idempotency applies.
8. Capability does not create authority.
9. Transport, persistence, retrieval, understanding, learning, and application remain separately provable boundaries.

## Minimum acceptance

A production implementation of INTELLIGENT_EVENT_V1 must prove:

- stable event identity;
- durable persistence;
- provenance;
- evidence linkage;
- causal relationships where available;
- authorized retrieval;
- event-to-understanding linkage;
- idempotency where required;
- retention/release semantics;
- successor reconstruction.

## Non-goals

This contract does not require every raw system log to become an Intelligent Event.

The event ledger records **meaningful intelligence events**, not arbitrary telemetry.

> Capture broadly enough to preserve intelligence. Distill aggressively enough to preserve attention. Never lose the truth path.

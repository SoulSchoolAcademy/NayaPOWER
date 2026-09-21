# Naya Intelligence Communication Protocol V1

**Status:** CANONICAL / OFFICIAL  
**Effective:** 2026-09-21  
**Relationship:** Implements the Notification Bus and Canonical Intelligence Record Layout.

## 1. Core principle

NayaNET communication is event-driven.

It is NOT a cron requirement, polling requirement, or GitHub Actions requirement.

The desired contract is:

**IF A HAPPENS → EMIT ONE CANONICAL EVENT → TRIGGER COMMUNICATION → CREATE BRIEFING → DELIVER TO AUTHORIZED RECIPIENTS → RECORD DELIVERY → PROCESS ELIGIBLE INTELLIGENCE**

The implementation may use serverless events, webhooks, database triggers, queues, or another event-driven mechanism. The transport is replaceable; the contract is not.

## 2. Communication is intelligence flow

A notification is not merely an alert.

It is a structured communication carrying enough context for another Naya to understand the event without asking the original Naya to repeat the explanation.

The canonical communication sequence is:

**EVENT → AWARENESS → BRIEFING → UNDERSTANDING → INTELLIGENCE PROCESSING → GOVERNED PROPAGATION**

## 3. Trigger contract

A trigger MUST:

1. recognize a defined material event;
2. assign a stable event ID;
3. capture occurrence time;
4. identify source Naya/runtime;
5. establish project/mission scope;
6. create the canonical event before downstream projection;
7. determine visibility and required awareness;
8. create the briefing;
9. dispatch authorized projections;
10. record delivery state;
11. enqueue/process eligible intelligence propagation.

A trigger MUST NOT grant authority merely because an event occurred.

## 4. Event classes

At minimum:

- NAYA_JOINED
- INTELLIGENCE_CREATED
- ACTIVITY_CREATED
- ACTION_TRIGGERED
- ACTION_COMPLETED
- ACTION_BLOCKED
- VERIFICATION_FAILED
- GOVERNANCE_CHANGED
- HANDOFF_CREATED

## 5. Briefing contract

Every notification that requires awareness SHOULD provide:

**WHAT HAPPENED**  
A concise factual description.

**WHY IT HAPPENED**  
The causal or initiating context, clearly distinguishing evidence from inference.

**WHY IT MATTERS**  
The consequence or relevance.

**WHAT CHANGED**  
The state transition.

**WHO / WHAT NEEDS TO KNOW**  
Recipients or systems determined by scope.

**RECOMMENDATION / NEXT ACTION**  
A recommendation, if warranted. A recommendation is not an instruction unless separately authorized.

**AUTHORITY STATE**  
Whether authority changed, remained unchanged, or requires review.

**EVIDENCE STATE**  
Known/observed/verified/inferred/uncertain/etc.

**SOURCE EVENT**  
Stable event ID and canonical location.

**DELIVERY STATE**  
Pending/partial/delivered/failed.

## 6. Recipient model

A message can target:

- one Naya;
- current live Nayas;
- newly entering Nayas;
- a project intelligence context;
- the human;
- NayaNET Intelligence Hub;
- authorized Collective Intelligence processing.

Recipient selection is governed by visibility, scope, consent, authority, relevance, and required awareness.

## 7. New-Naya rule

A new Naya MUST receive the relevant current notification stream during context restoration before consequential work.

The restoration stream should include material changes since its checkpoint, unresolved work, governance changes, required-awareness events, and relevant handoffs.

## 8. Collective propagation

Eligible notifications may enter the intelligence-processing flow:

**NOTIFICATION → CLASSIFY → CHECK PRIVACY/CONSENT → CHECK NOVELTY → EXTRACT LEARNING → VERIFY/QUALIFY → RETAIN PERSONAL/PROJECT INTELLIGENCE → OPTIONAL COLLECTIVE CANDIDATE → GOVERNED SHARING**

No private event becomes collective merely because it was successfully delivered.

## 9. Idempotency

The same canonical event MUST NOT create duplicate intelligence merely because a delivery is retried.

Delivery retries operate on the same event ID.

## 10. Failure

If a projection fails:

- the canonical event remains durable;
- delivery state becomes PARTIAL or FAILED;
- the failure becomes visible;
- retry remains possible;
- the event itself is not rewritten as though it never occurred.

## 11. No silent fragmentation

A Naya MUST NOT invent a new storage location for a new Smart Note, Activity record, Notification, or Briefing when the canonical daily location applies.

If a specialized system requires another representation, that representation MUST reference the canonical event rather than silently becoming a competing record.

## 12. Human experience

The communication should feel like:

> **“You're it. Here's what happened. Here's why. Here's what changed. Here's what you need to know. Here's what happens next.”**

This is awareness and continuity—not noise.

## 13. Constitutional boundaries

Communication never overrides:

- platform/safety/legal constraints;
- NayaPOWER constitutional law;
- explicit human authority;
- governance/authority registry;
- privacy/consent;
- evidence requirements.

**NOTIFICATION != AUTHORITY**

## 14. Canonical flow

**MATERIAL EVENT**
→ **CANONICAL EVENT**
→ **DAILY INTELLIGENCE RECORD**
→ **BRIEFING**
→ **AUTHORIZED DELIVERY**
→ **DELIVERY RECEIPT**
→ **INTELLIGENCE PROCESSING**
→ **PROJECT / PERSONAL / COLLECTIVE PROJECTION**
→ **NEXT NAYA**

This is the official NayaNET communication contract.

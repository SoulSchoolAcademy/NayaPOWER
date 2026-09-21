# NayaNET Intelligence Grammar Reconciliation — 2026-09-21

STATUS: EXECUTED RECONCILIATION PASS
SOURCE: LIVE main repository inspection
CANONICAL GRAMMAR:
IDENTITY → TIME → TYPE → SUBJECT → RELATIONSHIP → EVIDENCE → STATE → VALUE → ACTION → OUTCOME → LEARNING → SUCCESSOR

## Executive finding

The existing NayaNET system already contains most of the required grammar, but the dimensions are distributed across specialized truth/projection layers rather than one universal record.

The strongest existing backbone is:

Smart Note domain record
→ Cognition Event
→ Execution Receipt
→ Smart Ledger
→ Notification
→ Learning Evidence / Learner State
→ Project Intelligence state / bridge / successor

This is not a reason to create another event store.

The reconciliation identifies one material architectural gap:

INTELLIGENT BLOCK V1 is currently a durable representation inside Smart Note transaction payloads (v7_smart_note_transactions.intelligent_block), not a clearly first-class, independently addressable reusable understanding object with its own canonical lifecycle/retrieval contract.

The smallest next architectural move is therefore not a new event ledger. It is to close the Event → Block boundary using the existing canonical event identity and existing persistence/index/retrieval machinery.

## 1. Smart Notes

Primary sources:
- smart_note_events
- smart_note_artifacts
- smart_note_receipts
- v7_smart_note_transactions

| Dimension | Existing implementation | Assessment |
|---|---|---|
| IDENTITY | smart_note_events.id; transaction idempotency_key; canonical event ID propagated into artifacts/transaction | FIT |
| TIME | created_at; receipt created_at / verified_at | FIT |
| TYPE | SMART_NOTE event type; artifact types HUMAN/NAYA/MACHINE/INTELLIGENCE_FEED | FIT |
| SUBJECT | subject with fallback from human content | FIT |
| RELATIONSHIP | event/artifact/receipt linkage and canonical event ID | FIT |
| EVIDENCE | verification receipt, artifact URLs, evidence JSON | FIT |
| STATE | Smart Note status plus verification receipt status | FIT |
| VALUE | mainly downstream Ledger/value structures | PARTIAL |
| ACTION | capture/create operation and receipt action | FIT THROUGH RECEIPT |
| OUTCOME | verification and downstream execution/outcome records | FIT THROUGH RECEIPT |
| LEARNING | downstream learning evidence/cognition linkage | FIT THROUGH LEARNING |
| SUCCESSOR | Project Intelligence/handoff machinery | PARTIAL |

Important identity finding: current v7_create_smart_note propagates one UUID into the human/Naya/machine/feed/block/evidence/hub payloads, and the later Smart Note → Cognition → Execution Receipt boundary uses that Smart Note UUID as the Cognition event_id. Older migration history used smart_note:<uuid>; this is historical identity lineage and should not become a second current identity scheme.

## 2. Cognition Events

Primary source: nayanet_cognition_events

| Dimension | Existing implementation | Assessment |
|---|---|---|
| IDENTITY | row id + stable event_id | FIT |
| TIME | created_at, updated_at | FIT, but no separate canonical occurred_at |
| TYPE | type, classification | FIT |
| SUBJECT | title, content, project_id | FIT |
| RELATIONSHIP | parent_event_id, receipt_id, metadata lineage | FIT |
| EVIDENCE | source_hash, receipt linkage, metadata; Ledger evidence downstream | FIT / DISTRIBUTED |
| STATE | status, confidence | FIT |
| VALUE | receipt/Ledger/outcome rather than fully native | PARTIAL / DISTRIBUTED |
| ACTION | cognition action plus receipt/operation | FIT THROUGH EXECUTION |
| OUTCOME | receipt and outcome records | FIT THROUGH EXECUTION |
| LEARNING | learning payload and learning evidence | FIT THROUGH LEARNING |
| SUCCESSOR | successor/handoff machinery elsewhere | PARTIAL / DISTRIBUTED |

Finding: Cognition is already the generalized event identity substrate. Do not replace it.

## 3. Execution Receipts

Primary source: nayanet_execution_receipts

| Dimension | Existing implementation | Assessment |
|---|---|---|
| IDENTITY | receipt id + per-user/project revision | FIT |
| TIME | created_at | FIT |
| TYPE | action | FIT |
| SUBJECT | project_id, action, expected_result | FIT |
| RELATIONSHIP | event IDs, authority, policy, cognition linkage | STRONG FIT |
| EVIDENCE | evidence JSON | STRONG FIT |
| STATE | status | STRONG FIT |
| VALUE | value JSON + independent outcomes | STRONG FIT |
| ACTION | action | STRONG FIT |
| OUTCOME | observed_result + execution_outcomes | STRONG FIT |
| LEARNING | learning JSON | FIT |
| SUCCESSOR | Project Intelligence owns continuation | CORRECT SEPARATION |

The independent execution outcome contract is a strong fit with the value model because verified value is independently recorded rather than self-scored by execution policy.

## 4. Intelligence Notifications

Primary sources:
- nayanet_intelligence_notifications
- nayanet_intelligence_notification_deliveries

| Dimension | Existing implementation | Assessment |
|---|---|---|
| IDENTITY | notification id + unique event_id + source receipt/cognition IDs | STRONG FIT |
| TIME | occurred_at, created_at, canonical_day | STRONG FIT |
| TYPE | event_type | STRONG FIT |
| SUBJECT | summary, why_it_matters, what_changed | STRONG FIT |
| RELATIONSHIP | source receipt/cognition, caused_by, delivery rows | STRONG FIT |
| EVIDENCE | evidence_state + source lineage | FIT |
| STATE | delivery, propagation, authority, evidence states | STRONG FIT |
| VALUE | why_it_matters, recommendation, changed state | FIT |
| ACTION | recommendation/delivery action | FIT |
| OUTCOME | delivery state | FIT |
| LEARNING | source event/receipt owns learning | CORRECT SEPARATION |
| SUCCESSOR | recommendation + recipient set; formal successor elsewhere | PARTIAL / CORRECT SEPARATION |

The notification bus is already event-driven from execution receipts. No new notification event store is warranted.

## 5. Learning Evidence

Primary sources:
- learning_evidence
- learner_states
- naya-learning-apply

| Dimension | Existing implementation | Assessment |
|---|---|---|
| IDENTITY | evidence id + target id | FIT |
| TIME | created_at + learner-state update | FIT |
| TYPE | level/status/verification method | FIT |
| SUBJECT | target_id, claim | STRONG FIT |
| RELATIONSHIP | source_event_id, target, replay, learner state | STRONG FIT |
| EVIDENCE | verification method, provenance, observed value | STRONG FIT |
| STATE | status + E0–E7 level | STRONG FIT |
| VALUE | observed value / later usefulness | PARTIAL |
| ACTION | apply verified learning | FIT |
| OUTCOME | learner state update + cognition event | FIT |
| LEARNING | canonical learning object | STRONG FIT |
| SUCCESSOR | future decision/context consumes learner state | FIT THROUGH SUCCESSOR |

This is already a governed learning object, not merely a note.

## 6. Project Intelligence

Primary sources:
- nayanet_project_intelligence_state
- nayanet_intelligence_operations
- nayanet_project_intelligence_bridge
- nayanet-compound-intelligence
- .naya/control-plane/*
- .naya/project-intelligence/*
- NAYA/ACTIVITY/*

| Dimension | Existing implementation | Assessment |
|---|---|---|
| IDENTITY | project, packet, receiver, receipt, successor IDs | STRONG FIT |
| TIME | event/receipt/bridge/activity timestamps | STRONG FIT |
| TYPE | operations, bridge, proof, learning, handoff classes | FIT |
| SUBJECT | project, frontier, current state, next action | STRONG FIT |
| RELATIONSHIP | packet → receiver event → receipt → continuation → successor | STRONG FIT |
| EVIDENCE | proof registry, bridge evidence, receipts | STRONG FIT |
| STATE | proven/unknown/blocked/protected/current state | STRONG FIT |
| VALUE | mission, north star, value contracts | FIT |
| ACTION | canonical current next action | STRONG FIT |
| OUTCOME | execution/verification proofs | STRONG FIT |
| LEARNING | durable lessons + learning evidence | STRONG FIT |
| SUCCESSOR | explicit continuation/successor lineage | STRONG FIT |

Project Intelligence is correctly the orchestration/continuity layer, not the raw event ledger.

## 7. Activity

Primary source: NAYA/ACTIVITY/

Activity is the human-readable operational projection of the same causal system.

| Dimension | Existing implementation | Assessment |
|---|---|---|
| IDENTITY | dated activity record + event/receipt/run IDs | FIT |
| TIME | dated directory and timestamps | STRONG FIT |
| TYPE | activity/proof/failure/learning/handoff sections | FIT |
| SUBJECT | project/frontier/work item | FIT |
| RELATIONSHIP | linked runs, jobs, commits, artifacts, events, receipts | STRONG FIT |
| EVIDENCE | exact run/job/commit/artifact identities | STRONG FIT |
| STATE | current/failed/proven/blocked/unknown | STRONG FIT |
| VALUE | reason/impact/next action | FIT |
| ACTION | next action | STRONG FIT |
| OUTCOME | actual observed result | STRONG FIT |
| LEARNING | WHAT WE LEARNED | STRONG FIT |
| SUCCESSOR | successor action/handoff | STRONG FIT |

Activity should remain a projection, not a competing database.

## 8. Smart Ledger

The Smart Ledger is the strongest existing cross-record integrity layer.

It references existing truth stores rather than replacing them:
Smart Notes, Cognition Events, Execution Receipts, Intelligence Reports, Learning Evidence, Smart Spaces, and other governed sources.

It already supplies:
- ledger identity;
- source table/source ID;
- parent chain;
- event time;
- evidence refs;
- verification;
- value;
- outcome;
- learning refs;
- privacy;
- status;
- hash lineage;
- supersession/qualification references.

This means the 12-dimensional grammar can be connected without collapsing specialized records into one mega-table.

## 9. What is duplicated?

Intentional duplication:
- identities belong to different objects in the causal graph;
- timestamps belong to different object lifecycles;
- evidence is retained at source and referenced by projections;
- status can differ legitimately across objects (for example event verified while notification delivery is pending).

Dangerous duplication:
- canonical event identity. Historical migrations show more than one Smart Note → Cognition event-ID convention.

Rule:
One meaningful occurrence → one canonical Intelligent Event identity. Projection objects may have their own IDs, but must retain the canonical event relationship.

## 10. What is missing?

### Material gap #1 — first-class Intelligent Block

The Smart Note pipeline already creates an intelligent_block payload, but inspection found no dedicated intelligent_blocks persistence/retrieval surface in the current migration set.

INTELLIGENT_BLOCK_V1 requires:
- stable block identity;
- subject identity;
- version/status;
- owner scope;
- source event IDs;
- evidence/provenance;
- understanding state;
- value context;
- applicable scope;
- supersession;
- durable reuse;
- authorized retrieval;
- successor comprehension.

### Material gap #2 — occurred_at versus recorded_at

Cognition centers on created_at/updated_at while INTELLIGENT_EVENT_V1 distinguishes when something happened from when it was recorded. Adjacent layers contain enough timestamp information to preserve much of this distinction, but it is not uniformly canonicalized.

This is a contract gap, not yet proof that every table needs a new column.

### Material gap #3 — distributed value/evidence semantics

Important value/evidence dimensions are distributed across Cognition, Receipt, Outcome, and Ledger. This is acceptable if canonical relationships permit reconstruction without custom archaeology.

### Material gap #4 — notification semantics

The notification bus already distinguishes underlying event, notification, and delivery outcome well enough. No new store is needed.

## 11. What already fits?

All 12 dimensions already exist somewhere in the system.

The problem is not absence of intelligence primitives.

The problem is distributed canonical relationships and the Event → Block boundary.

## 12. Smallest next architectural move

DO NOT:
- create a parallel Intelligent Event table;
- replace Cognition Events;
- replace Smart Notes;
- replace Execution Receipts;
- replace Smart Ledger;
- replace Learning Evidence;
- redesign Project Intelligence;
- redesign the Hub;
- flatten everything into one universal table.

DO:
Close one boundary:

CANONICAL INTELLIGENT EVENT → CANONICAL INTELLIGENT BLOCK

using the existing Smart Note/Cognition identity and existing persistence/index/retrieval machinery.

The first proof should be:

CREATE meaningful event
→ VERIFY event
→ DERIVE Intelligent Block
→ PERSIST Block
→ RETRIEVE Block
→ SHOW source event/evidence
→ RELOAD / fresh context
→ RETRIEVE again
→ prove same Block identity
→ record learning/successor.

## 13. Decision

RECONCILIATION RESULT:
- Smart Notes: FIT
- Cognition Events: FIT / needs explicit canonicalization of a few contract dimensions
- Execution Receipts: STRONG FIT
- Notifications: STRONG FIT
- Learning Evidence: STRONG FIT
- Project Intelligence: STRONG FIT
- Activity: STRONG FIT
- Smart Ledger: STRONG CONNECTIVE FIT
- Intelligent Event V1: already substantially implemented by existing machinery
- Intelligent Block V1: representation exists; first-class lifecycle/retrieval remains the smallest material gap

ARCHITECTURAL CONCLUSION:

NayaNET does not need more storage. It needs clearer object boundaries and stronger canonical relationships.

The existing system is already close to the intended intelligence grammar.

Next move:
Make the existing Intelligent Block real as a first-class reusable understanding object, without creating a second event system.

## Successor

Inspect the existing Smart Note transaction/block payload and intelligence-index/retrieval machinery to determine the smallest concrete persistence + retrieval boundary needed to make INTELLIGENT_BLOCK_V1 first-class, then implement and prove exactly one event → block → evidence → retrieval chain.

No Hub redesign.
No parallel event store.
No broad schema rewrite.
Stop at the first deterministic failure.

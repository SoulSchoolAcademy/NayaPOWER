# NAYA POWER — GITHUB APP BRIDGE & COMMUNICATION SPECIFICATION V1

DATE: 2026-09-12
STATUS: CANONICAL INTEGRATION SPECIFICATION V1
NUMBER: 53
AUTHORITY: SUBORDINATE TO CONSTITUTION, GOVERNANCE, HUMAN AUTHORITY, ARCHITECTURE, AND #39–#52
ROLE: DEFINE THE GITHUB ↔ SUPERBRAIN ↔ INTELLIGENT HUB COMMUNICATION BRIDGE

---

## 1. PURPOSE

The Intelligent Hub must not depend on conversational relay or fragile GitHub Actions as its primary Activity Feed transport.

The intended architecture is:

**GITHUB / SUPERBRAIN → GITHUB APP BRIDGE → CANONICAL EVENT / ADAPTER LAYER → INTELLIGENT HUB**

and, where authorized:

**INTELLIGENT HUB → CANONICAL USER EVENT → GITHUB APP / ADAPTER → SUPERBRAIN / GITHUB**

The GitHub App is therefore an integration bridge, not the source of truth and not the Hub itself.

---

## 2. ROLES

### GitHub / Superbrain

Authoritative engineering and intelligence source for repository-backed work, canonical documents, machine state, execution records, and applicable intelligence.

### GitHub App

Authenticated integration actor that receives authorized GitHub events, reads permitted repository state, and delivers normalized events to the NayaNET integration boundary.

It must operate with least privilege.

### Adapter / Event Layer

Normalizes source-specific events into the canonical event envelope defined by #39 and applies the contracts in #45.

### Intelligent Hub

Human-facing receiver/projection layer. It renders authorized intelligence into Smart Notes, Intelligent Blocks, Activity, Personal, and Collective feeds and emits user actions back into the canonical event system.

### Persistence / Ledger

Durably records canonical events, provenance, state transitions, authorization, publication state, and verification evidence according to the applicable contracts.

---

## 3. NON-NEGOTIABLE ARCHITECTURE

**The Hub does not scrape GitHub.**

**GitHub Actions are not the default Activity Feed writer.**

**The GitHub App is not the canonical intelligence database.**

**The Hub is not the canonical source of repository truth.**

**A GitHub webhook receipt is not proof that a downstream projection succeeded.**

Every consequential flow must preserve:

**SOURCE → EVENT → NORMALIZE → AUTHORIZE → PERSIST → PROJECT → OBSERVE → VERIFY**

---

## 4. GITHUB APP RESPONSIBILITIES

The production GitHub App should be capable of:

1. receiving authorized repository webhook events;
2. authenticating webhook origin;
3. identifying repository, branch, commit, actor, event type, and timestamp;
4. reading permitted repository content when required for context;
5. reading permitted commit/workflow metadata when required;
6. emitting normalized canonical events;
7. correlating source events with existing event IDs/idempotency keys;
8. reporting delivery failures;
9. supporting replay/recovery where safe;
10. never silently dropping consequential events;
11. respecting least-privilege permissions;
12. exposing enough evidence to verify delivery without exposing secrets.

The App should not receive permissions unrelated to these responsibilities.

---

## 5. REQUIRED WEBHOOK EVENT CLASSES

Initial event classes should include, as applicable to actual connected infrastructure:

- push / commit;
- branch/reference changes;
- pull request lifecycle;
- workflow execution;
- workflow completion;
- deployment events;
- release events;
- issue/project events when intentionally integrated;
- repository configuration events only when explicitly required.

Unsupported events must be ignored or quarantined explicitly, never interpreted by guesswork.

---

## 6. CANONICAL EVENT ENVELOPE

Each accepted source event must be normalized into the #39 event identity model and retain at minimum:

- event_id;
- source_system;
- source_event_id / delivery_id;
- event_type;
- repository / source identity;
- branch/ref where applicable;
- commit SHA where applicable;
- actor identity where authorized;
- occurred_at;
- received_at;
- correlation_id;
- idempotency_key;
- authority/scope;
- provenance;
- evidence references;
- verification state;
- privacy/publication classification;
- processing state;
- projection targets.

The exact field names remain subordinate to #39's final implementation contract.

---

## 7. DELIVERY MODEL

Preferred flow:

**GITHUB EVENT → VERIFIED WEBHOOK RECEIPT → NORMALIZER → AUTHORIZATION → EVENT STORE → ADAPTERS → SMART NOTE / PIS → FEED PROJECTIONS → HUB**

A failed projection must not erase the source event.

A duplicate webhook must not create duplicate intelligence.

A missing downstream acknowledgment must remain observable as incomplete/unknown rather than being silently treated as success.

---

## 8. SECURITY

The production bridge must use:

- webhook signature verification;
- encrypted transport;
- secret storage outside source code;
- least-privilege GitHub App permissions;
- explicit installation/repository scope;
- authenticated downstream service communication;
- authorization checks before private projection;
- auditability of consequential bridge operations;
- secret and token non-disclosure in Hub content;
- revocation/disable handling.

No private key, webhook secret, token, credential, or signing material belongs in the repository.

---

## 9. IDEMPOTENCY AND ORDERING

The bridge must tolerate retries.

The same source delivery must resolve to one logical canonical event identity.

Where source ordering matters, the system must preserve or explicitly represent ordering metadata.

Out-of-order delivery must not create false chronology.

The system should support:

**RECEIVED → ACCEPTED → NORMALIZED → PERSISTED → PROJECTED → VERIFIED**

with explicit failure/blocked/unknown states.

---

## 10. TWO-WAY COMMUNICATION

The architecture is bidirectional, but authority is not symmetric.

Hub user actions may create canonical user events only within authorized scope.

A Hub action must not directly mutate protected repository state merely because the technical connection exists.

Where a Hub action requires GitHub mutation, the flow is:

**HUB ACTION → AUTHORIZATION → CANONICAL EVENT → GITHUB APP / AUTHORIZED MUTATION → GITHUB OBSERVATION → VERIFICATION → HUB UPDATE**

Capability never substitutes for authority.

---

## 11. ACTIVITY FEED RULE

The Activity Feed is a projection of canonical events and verified state.

The GitHub App may supply source events to the event system, but the event system is responsible for the Activity projection.

This prevents GitHub from becoming a UI-specific feed database and prevents GitHub Actions from becoming the default baton-passing mechanism.

---

## 12. FAILURE AND RECOVERY

The bridge must distinguish:

- rejected event;
- invalid signature;
- unauthorized source;
- duplicate event;
- normalization failure;
- persistence failure;
- adapter failure;
- projection failure;
- verification failure;
- unavailable downstream service;
- retryable failure;
- permanently blocked operation.

No failure may be converted into a successful-looking Hub notification.

Recovery must be idempotent and evidence-backed.

---

## 13. OBSERVABILITY

Production operation requires a bridge health surface that can answer:

- Is the App installed?
- Which repositories/scopes are connected?
- Are webhooks arriving?
- Are signatures valid?
- Are events being accepted?
- Are events being persisted?
- Are adapters processing?
- Are feed projections succeeding?
- What is delayed?
- What is failed?
- What is blocked?
- What is unknown?
- When was the last verified successful end-to-end event?

The Hub should expose truthful connection state without exposing sensitive credentials.

---

## 14. INSTALLATION CONTRACT

The actual GitHub App must be created and installed outside the repository's source files through the appropriate GitHub administration surface.

Repository documentation must record only non-secret configuration facts needed for operation, such as:

- App identity/name;
- approved repository scope;
- webhook endpoint;
- subscribed event classes;
- required permissions;
- deployment target;
- health-check endpoint;
- rotation/revocation procedure.

Secrets and private keys remain outside GitHub source.

If the required external GitHub App administration surface is unavailable to the executing Naya, that specific installation step is **BLOCKED_EXTERNAL_ADMIN** and must not be fabricated as complete.

---

## 15. IMPLEMENTATION ORDER

P0:

1. establish actual Hub backend/API boundary;
2. establish event persistence;
3. establish secure identity/authorization;
4. create/configure GitHub App;
5. establish signed webhook receiver;
6. normalize GitHub events into #39;
7. persist and deduplicate;
8. connect adapters/PIS;
9. project Activity Feed;
10. independently verify end-to-end delivery.

P1:

11. two-way authorized actions;
12. replay/recovery console;
13. richer source subscriptions;
14. advanced observability.

---

## 16. DEFINITION OF DONE

The bridge is production-proven only when a real authorized GitHub event can be independently traced:

**GITHUB SOURCE → VERIFIED WEBHOOK → CANONICAL EVENT → PERSISTENCE → ADAPTER/PIS → SMART NOTE / INTELLIGENT BLOCK → ACTIVITY PROJECTION → HUB OBSERVATION → VERIFIED RECEIPT**

and, for an authorized reverse flow:

**HUB ACTION → CANONICAL EVENT → GITHUB APP → GITHUB MUTATION → GITHUB OBSERVATION → VERIFIED RESULT → HUB UPDATE**

A diagram, configuration file, webhook registration, successful HTTP response, or GitHub Action alone does not prove this chain.

---

## 17. CURRENT TRUTH

KNOWN:

- The repository is `SoulSchoolAcademy/NayaPOWER`.
- The Intelligent Hub source exists as the V7 monolithic HTML artifact.
- #39 defines the cross-system event contract concept.
- #44 defines direct Activity event writing as a required architecture.
- #45 defines Hub event/PIS adapter integration.
- #51 and #52 require exact runtime verification.

UNKNOWN:

- The production Hub backend/API implementation.
- The production event store/database.
- The actual GitHub App installation.
- The production webhook endpoint.
- The production identity provider/session service.
- The exact live Hub runtime parity.

These unknowns are implementation work, not reasons to invent infrastructure.

---

## 18. OPERATING LAW

**CONNECT THE SYSTEMS. DO NOT CONFUSE THE SYSTEMS.**

GitHub is a source and engineering system.

The GitHub App is a bridge.

The canonical event layer is the transport/integrity boundary.

The Superbrain/PIS is intelligence.

The Intelligent Hub is the human-facing living projection and action environment.

The system succeeds when these layers cooperate without collapsing their responsibilities.

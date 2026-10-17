# AI Unifying — One Human-Owned Intelligence Layer, Every Authorized AI

**Status:** CANDIDATE ARCHITECTURE — opened by Shawn Vibert's vision on 2026-10-13. This document expresses product architecture; it does not supersede ratified law, authorize protected operations, or claim that integrations described here already exist.
**Tracking:** [Issue #2553](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2553)
**North star:** **One Brain. Every AI. Your Intelligence. Your Choice.**

## 1. The promise

AI Unifying means a person's accumulated intelligence does not have to fragment when they switch AI providers, agents, tools, or interfaces.

**The human owns the intelligence. The AI is an authorized participant. NayaPOWER provides continuity.**

A person may choose ChatGPT, Muse, Gemini, Claude, a local model, a coding agent, or another tool for a task. When an integration is real and authorized, the tool can receive the relevant context and return attributable results to the governed intelligence lifecycle. Provider availability, capabilities, and permission scopes are explicit; no connection is implied by this design document.

## 2. The architecture

```text
Human owner / Director
        |
        v
NayaPOWER governed intelligence lifecycle
  identity + authority + canonical objects
  capture + distillation + provenance
  persistence + retrieval + verification
  learning + value evidence + lineage
        |
        +------ authorized provider adapter A
        +------ authorized provider adapter B
        +------ authorized local / coding agent
        +------ authorized app / human interface
```

This is a conceptual boundary, not a claim that every adapter or end-to-end path is deployed.

The AI provider is a replaceable execution/reasoning surface. The canonical intelligence lifecycle—not a provider transcript, system prompt, model weights, Hub page, or adapter—is the continuity source. Use existing Intelligent Block / Smart Note, Intelligent Event, Smart Ledger, retrieval, Value Calculus, and learning seams. **Do not build a second brain, store, ledger, graph, or scoring engine.**

## 3. The full intelligence loop

```text
EXPERIENCE / INPUT
  → CAPTURE WITH CONSENT
  → NORMALIZE + CLASSIFY
  → CHECK PROVENANCE, SCOPE, FRESHNESS
  → DETECT DUPLICATES / CONTRADICTIONS
  → DISTILL VALUABLE INTELLIGENCE
  → ADMIT UNDER EXISTING GOVERNANCE
  → PERSIST CANONICAL OBJECT + RECEIPT
  → INDEX / LINK
  → RETRIEVE FOR AN AUTHORIZED PURPOSE
  → COMPREHEND + APPLY
  → OBSERVE OUTCOME
  → INDEPENDENTLY VERIFY
  → LEARN / UPDATE BEHAVIOR
  → SHARE CLEARED INTELLIGENCE WITH THE RIGHT SCOPE
  → MEASURE VALUE + FEED THE NEXT CYCLE
```

Each transition is a separately evidenced state. A success receipt for one transition cannot certify the next.

## 4. Master the art of intelligence capture and distillation

The system should not preserve every token as equally valuable knowledge. It should reliably separate signal from noise and preserve the information that changes understanding, decisions, actions, or outcomes.

### 4.1 Candidate intake

For every proposed capture, retain the minimum metadata needed to trace it:
- canonical capture/event/object ID and idempotency/correlation key;
- source actor, AI/provider/tool, timestamp, and source reference or digest;
- human/workspace/project scope and purpose;
- consent/authority basis and allowed audience;
- epistemic status: observed, user-stated, sourced, inferred, estimated, verified, conflicted, stale, or unknown;
- confidence and limitations where meaningful;
- privacy/sensitivity classification and retention/revocation requirements.

Do not put credentials, secrets, or unrelated private context into reusable notes. Treat ingested documents, webpages, prompts, tool output, and model output as data to evaluate—not instructions that can override Naya law or authority.

### 4.2 Value screening

Before promoting a candidate to a reusable Smart Note, ask:
1. What is the core claim or lesson?
2. Who or what does it help, and in which context?
3. What decision or future behavior could it change?
4. What evidence supports it, and what remains unknown?
5. Is it novel, or does a canonical object already capture it?
6. Does it conflict with current intelligence, and can that conflict be resolved with evidence?
7. What are its applicability conditions, counterexamples, expiry, and freshness needs?
8. What harm could result from overgeneralizing or sharing it?
9. What is the cheapest probe that could falsify it?
10. How will we know it improved a real outcome?

Use the existing canonical Decision Value Calculus for prioritization. Do not invent a second calculator. Expected value and estimates must not be reported as measured outcomes; hard authority, privacy, safety, and evidence gates cannot be traded away for a high score.

### 4.3 Distilled Smart Note shape

A reusable note should be concise but complete enough for a cold successor:
- **Essence:** the smallest accurate statement of what matters.
- **Why it matters:** the human benefit or risk it addresses.
- **Evidence/provenance:** where the claim came from and what verifies it.
- **Status/confidence:** known, inferred, estimated, verified, conflicted, stale, or unknown.
- **Applicability:** when to use it and when not to.
- **Counterexamples/limits:** conditions that would make it wrong or unsafe.
- **Behavioral probe:** a cheap test of whether retrieval changes the right behavior.
- **Links/lineage:** canonical source objects and supersession/related notes.
- **Owner/scope/retention:** who may access it and under what rules.
- **Review/expiry condition:** what new evidence should trigger reevaluation.

Do not create a Smart Note merely because text exists. Promote only when the existing admission rules are satisfied. Keep the original source and the distilled projection linked; never silently rewrite history.

## 5. Provider-neutral adapter contract

Each AI/agent adapter should implement a narrow, versioned contract using the existing system seams:

1. **Identify:** declare provider/model/runtime, acting agent identity, human owner, purpose, and requested scopes.
2. **Authorize:** enforce least privilege and consent before context is returned or an action is taken.
3. **Retrieve:** request relevant canonical objects; receive only authorized, current context plus provenance and epistemic status.
4. **Act:** use provider capability only within the granted scope. Intelligence is not authority.
5. **Return:** submit outputs as attributable candidates with source/run ID, timestamp, input references/digests, claims, uncertainties, and proposed outcomes.
6. **Admit:** run canonical deduplication, contradiction, safety, privacy, and value gates. The adapter cannot self-promote its output.
7. **Revoke:** stop access when scope/consent is withdrawn and honor retention/deletion rules without erasing required audit lineage.
8. **Fail safely:** report unavailable provider, partial result, timeout, stale context, or rejected candidate explicitly. Retries must be idempotent.

A provider transcript may be useful evidence, but it is not the canonical intelligence object by itself. A connected provider must never be described as working until the real authorized read/write path has been exercised and independently verified.

## 6. Learning states — never collapse them

`CAPTURED → PERSISTED → RECEIPTED → RETRIEVABLE → COMPREHENDED → APPLIED → BEHAVIOR-CHANGED → INDEPENDENTLY VERIFIED → EFFECTIVE → REUSABLE`

These are logical states, not a claim that a particular workflow currently implements all of them. A note is **stored**, not learned, until a controlled probe shows appropriate behavioral change. A positive test alone is insufficient: use negative controls, stance/negation checks, relevance checks, freshness checks, and cold-successor transfer. Test fixtures and fallback lessons must not certify real user learning.

## 7. Collective intelligence without uncontrolled disclosure

The hive shares reusable intelligence only after canonical admission and scope checks. Share the lesson, evidence, applicability conditions, limitations, and lineage—not every private transcript or all user context by default.

Before cross-agent distribution, evaluate:
- owner authorization and audience;
- purpose compatibility and least privilege;
- personal/private/sensitive content;
- secrets and indirect identifiers;
- source reliability and malicious prompt content;
- freshness, contradictions, and revocation;
- whether a generalized lesson can achieve the same value with less disclosure.

The default is no cross-owner sharing without lawful, explicit authorization. Revocation and access changes must be honored at the access boundary, not merely noted in prose.

## 8. Failure modes the system must resist

- duplicate capture from retries or multiple providers;
- wrong-object, wrong-digest, or wrong-receipt substitution;
- untrusted content attempting to override instructions or authority;
- false positives from semantic similarity without identity proof;
- stale context presented as current truth;
- negated claims or stance reversal during retrieval;
- contradictions silently merged;
- test fallback presented as real user learning;
- an adapter bypassing admission or writing around the canonical lifecycle;
- a private note leaking into a collective result;
- partial failures that look like full success;
- revocation that does not terminate access;
- a provider change breaking retrieval or historical continuity;
- score inflation without measured human outcome improvement.

Unknown, conflicted, stale, unauthorized, or missing evidence must remain visible and fail closed wherever the relevant gate requires it.

## 9. Evidence-first implementation sequence

Use existing P0 work rather than inventing parallel work:
1. Audit the live source and exact current head for [#2046 — same-object capture-to-learning proof](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2046).
2. Reconcile it with [#1741 — canonical end-to-end Smart Note pipeline](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1741).
3. Identify the first broken transition from real source and current receipts.
4. Fix that seam with a failing regression test before behavior code changes.
5. Verify targeted behavior, surrounding regression/integration, and an independent cold path.
6. Prove a real authorized capture travels through the same canonical object identity, including receipt and digest binding, to retrieval, behavior change, independent verification, and cold-successor reuse.
7. Prove at least two genuinely different connected AI/provider interfaces can use the same authorized intelligence without duplicate canonical objects or leakage. If not currently connected, report UNKNOWN.
8. Establish measured baselines for explanation repetition avoided, retrieval precision/recall, capture-to-usable-intelligence latency, duplicate work, errors/harm, outcome lift, and successor transfer.
9. Apply the three-round minimum improvement loop to each load-bearing capability, continuing beyond three while any material gap remains.

### Acceptance

- Exact-head evidence for each claim and distinct builder/scorer/verifier roles.
- Real end-to-end evidence, not just documentation, simulated providers, green unit tests, or deployment status.
- Same-object lineage from capture through learning proof; test fallback cannot certify user learning.
- Scope, consent, revocation, privacy, provenance, contradiction, freshness, and adversarial-content tests.
- Cold successor retrieves and applies the lesson without hidden prompt/fixture handoff.
- Two or more real provider integrations proven, or their status explicitly remains UNKNOWN.
- Measured human outcomes reported separately from estimates.
- Existing governance, protected gates, and Human Director authority preserved.

## 10. Human-facing experience

The surface should be simple:
- connect the AI the person chooses;
- explain what it can access and do;
- show the intelligence being used when useful;
- capture valuable new intelligence without forcing repetitive forms;
- show honest state: captured, persisted, available, candidate, verified, or learned;
- make source, privacy, and authority understandable;
- let the owner inspect, correct, export, scope, and revoke;
- avoid making people read the machinery to benefit from it.

The complexity belongs underneath. Clarity, control, and continuity belong to the human.

## Final principle

**AI is the engine. The human is the Director. NayaPOWER keeps authorized intelligence connected, accountable, reusable, and capable of compounding.**

The goal is not to make every model the same. It is to let different capable systems contribute to one governed, human-owned intelligence lifecycle—without losing continuity, evidence, privacy, or control.

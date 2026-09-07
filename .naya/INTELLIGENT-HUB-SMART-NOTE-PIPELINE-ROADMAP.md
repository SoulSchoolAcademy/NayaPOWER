# NayaNET Intelligent Hub — Smart Note + Daily Intelligence Pipeline Roadmap

**Status:** ACTIVE EXECUTION PLAN  
**Date:** 2026-09-07  
**Scope:** NayaNET Intelligent Hub ↔ Smart Notes ↔ Daily Intelligence Report ↔ GitHub synchronization

## 1. North Star

Build one reliable end-to-end intelligence pipeline in which a real intelligence event can move from Naya into the durable Smart Note system and then into the Intelligent Hub without duplicate systems, lost state, guessed data, or presentation shortcuts.

**Target flow:**

`Human/Naya event → Smart Note recognition → canonical Smart Note → durable GitHub record → authorized transport/trigger → Intelligent Hub ingestion → existing Hub presentation → historical storage → verification/receipt`

The Hub is the receiver/presentation layer. GitHub is durable source/operating context. The transport between them must be explicit and independently testable; a GitHub commit by itself is not evidence that the live Hub has received or rendered the event.

## 2. Current Truth — What Is Already Established

### Smart Note side

- `.naya/SMART-NOTE-PROTOCOL.md` is the current canonical Smart Note execution protocol.
- The current canonical model is **one Smart Note = one intelligence event / one node**.
- The event contains five perspectives: **AI/Naya, Human, Machine, Child, Grandma**.
- The protocol requires: GITHUB FIRST → READ → UNDERSTAND → RESTORE RELEVANT INTELLIGENCE → CAPTURE → EXTRACT → CLASSIFY → RELATE → TIMESTAMP → WRITE → VALIDATE → VERIFY → RECEIPT → INDEX → INTELLIGENT FEED → PIS WHEN AUTHORIZED → CIS → NEXT ACTION.
- A known execution lesson is already captured: do not repeat a known blocker without first applying the known solution.

### Hub side

- `NAYANETHUBONE.html` exists as a working Hub source artifact and is the file Shawn has identified for surgical Hub work.
- A separate `CLOUDFLARE-INTELLIGENT-HUB-V7/` deployment/runtime area also exists.
- Existing Hub work includes Smart Notes/feed presentation, Your Intelligence Today, Daily Intelligence Report, Smart Share, and GitHub/Sync Intelligence concepts.

### Critical integration truth

The repository currently contains **multiple Hub-related artifacts and deployment paths**. The current build/deploy arrangement is not yet proven to establish one unambiguous chain from `NAYANETHUBONE.html` → deployed runtime → Smart Note ingestion. This must be resolved before declaring the pipeline ready.

The existing Smart Note/Hub pipeline documentation also reflects an older four-representation model in places. It must not override the newer canonical five-perspective protocol.

## 3. Readiness Verdict Right Now

### Receiver: NOT YET RELEASE-READY

The Hub has substantial receiving/presentation pieces, but readiness is **not proven** until each of these is demonstrated against the actual current source/runtime:

1. One authoritative Hub artifact is identified.
2. The deployed runtime is proven to be built from that artifact.
3. The Hub has one defined Smart Note ingestion contract.
4. The ingestion contract accepts the canonical one-event/five-perspective Smart Note shape.
5. The Hub renders that event in the intended Smart Note board/feed format.
6. Historical persistence and retrieval are preserved.
7. Duplicate ingestion is prevented.
8. A real Daily Intelligence Report can be rendered beautifully in the intended Hub location.
9. The receiver can be independently observed after a source event is written.

### Sender: PARTIALLY READY, NOT YET PROVEN END-TO-END

GitHub can persist Smart Note artifacts, and repository automation exists, but **GitHub write → trigger → Hub receive → render** is not yet independently proven as one working transaction.

A GitHub commit is therefore currently an **observed durable write**, not proof of Hub delivery.

## 4. Priority Order

### Priority 0 — Source / Deployment Authority Lock

Before changing the pipeline, establish exactly which Hub file is authoritative for production and which deployment path serves it.

**Deliverable:** one explicit source → build → deployment → runtime chain.

**Release gate:** no duplicate/competing Hub HTML source is allowed to silently become authoritative.

### Priority 1 — Finish the Hub Receiver Experience

Mold the Hub first, exactly as Shawn requested, so it is ready before the engines are turned on.

Finish and verify:

- Smart Note boards/cards and five-perspective presentation.
- Intelligent Feed behavior.
- Your Intelligence Today as the intelligence/highlights layer, not a second Smart Notes feed.
- Daily Intelligence Report presentation and historical navigation.
- Smart Share placement.
- Search/history behavior.
- Empty/loading/error states for real incoming intelligence.
- Duplicate-event handling.
- Responsive presentation.

**Release gate:** a manually supplied canonical Smart Note and a manually supplied Daily Intelligence Report payload can both be rendered correctly without modifying the receiver during the test.

### Priority 2 — Define the Receiver Contract

Write the exact machine contract the Hub accepts.

It must define:

- event identity
- event type
- timestamp
- source
- five perspectives
- title/summary/body fields actually rendered
- metadata
- authorization/privacy state
- idempotency key
- update/version semantics
- historical placement
- error behavior

**Release gate:** one sample event can be validated before ingestion.

### Priority 3 — Build the Sender/Transport

Choose and implement one authoritative transport route. The desired behavior is:

`Smart Note created → canonical GitHub artifact committed → trigger fires → receiver endpoint/ingestion path receives event → event is persisted/registered → Hub updates`

The trigger mechanism must be explicit. Options may include GitHub Actions calling a secure ingestion endpoint or another already-supported repository event mechanism. Do not add a second competing transport if an existing supported path can be used.

**Release gate:** a controlled test commit produces exactly one receiver ingestion event.

### Priority 4 — Connect Daily Intelligence Report

Treat the Daily Intelligence Report as a separate intelligence product built from the same underlying intelligence pipeline, not as another Smart Notes feed.

Target chain:

`Real intelligence → Smart Notes / intelligence records → Daily Intelligence Report generation → report persistence → Hub report layer → historical report navigation`

The report must be visually finished before production automation is enabled.

**Release gate:** Today, Yesterday, This Week, and This Month can be navigated and the report is rendered from real stored data.

### Priority 5 — End-to-End Test

Run one real event through the entire system.

Test command:

> “Hey, make a Smart Note about this.”

Expected behavior:

1. Naya recognizes Smart Note intent.
2. Naya restores the canonical protocol and relevant known intelligence.
3. Naya creates exactly one Smart Note event.
4. The event contains the five required perspectives.
5. The canonical event is written to GitHub.
6. The authorized trigger/transport fires.
7. The Hub receives the event.
8. The Hub renders it in the intended Smart Note presentation.
9. The event is retrievable through the intended history/search path.
10. No duplicate event/feed/control is created.
11. Evidence is captured for each transition.

**Release gate:** complete chain verified, not inferred.

### Priority 6 — Lock the Official Activation Protocol

Only after the real Hub test succeeds should the final **Smart Notes ↔ Intelligent Hub Activation Protocol** be written/locked.

That document should describe proven behavior, not intended behavior.

## 5. Verification Model

Every pipeline test must distinguish:

- **OBSERVED** — the source/event was seen.
- **CAPTURED** — the Smart Note was created.
- **PERSISTED** — the canonical artifact exists in GitHub.
- **TRIGGERED** — the integration automation actually fired.
- **RECEIVED** — the Hub ingestion layer accepted the event.
- **RENDERED** — the event visibly appears in the Hub.
- **RETRIEVABLE** — the event can be found again.
- **VERIFIED** — independent evidence confirms the expected behavior.
- **RECEIPTED** — the durable receipt records the verified transition.

Never collapse these into a single claim of “sync successful.”

## 6. Failure Rule

If any stage fails:

**STOP → INSPECT → DIAGNOSE → SEARCH KNOWN SOLUTIONS → TRY THE SAFEST SUPPORTED ROUTE → VERIFY → RECORD THE LESSON → CONTINUE**

Do not repeatedly retry the same failed route. Protect the current working source.

## 7. Definition of Done

The Smart Note + Intelligent Hub pipeline is ready only when all of the following are true:

- One authoritative Hub source is locked.
- Source → build → deployment → exact public runtime parity is proven.
- Hub receiver contract is defined and implemented.
- Smart Note five-perspective data is accepted without transformation that loses meaning.
- GitHub persistence is working.
- GitHub trigger/transport is working.
- Hub ingestion is working.
- Smart Note presentation is finished.
- Daily Intelligence Report presentation is finished.
- Historical intelligence is working.
- Duplicate protection is working.
- Search/retrieval is working.
- A real Smart Note completes the full pipeline.
- A real Daily Intelligence Report completes its pipeline.
- Independent observation verifies the live result.
- Only then is the integration activation protocol locked.

## 8. Execution Doctrine

**We build the receiver first. Then the contract. Then the sender/trigger. Then the connection. Then we test the complete pipeline. Then we write the final activation protocol from what actually works.**

No redesign. No parallel intelligence systems. No duplicate Smart Notes feed. No guessed triggers. No declaration of success without runtime evidence.

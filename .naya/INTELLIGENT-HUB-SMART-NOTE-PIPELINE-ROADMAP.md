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

### Hub source inspection — newly established

The authoritative working source is:

`NAYANETHUBONE.html` on `main`

Current blob SHA at inspection: `6d66d57afd19d67e06aa7755d4fffba40858c983`.

The source is a substantial V7 HTML application, but the inspection found several **receiver-readiness blockers that must be resolved before automation is enabled**:

1. The current source contains multiple additive/refinement layers that compete for the same feed, action, quote, navigation, and intelligence behaviors.
2. The source currently contains older four-perspective presentation in multiple places: Human / Naya / Machine / Intelligent Feed. This must be aligned to the canonical five-perspective Smart Note model without creating a second event system.
3. The source currently persists browser-local Smart Notes but does not yet expose one canonical external ingestion boundary for an incoming GitHub Smart Note event.
4. The current source has no proven server-side receive → persist → render path for a new GitHub event.
5. The current Daily Intelligence layer is primarily local/browser synthesis and does not yet provide the required stored Today / Yesterday / Week / Month historical report model.
6. The source currently contains multiple action implementations and overlays; Personal and Collective action ordering must be normalized to one underlying action system.
7. Inline Collective comments are not yet implemented as the required directly-attached comment surface.
8. Five-star ranking is not yet implemented as the required visible selectable five-star control on the note itself.
9. Smart Share is not yet proven in the required sidebar position immediately beneath Your Intelligence Today.
10. Smart Spaces is not yet established above Smart Mail, while an older `Naya Lists` concept exists in an additive layer and must not become a competing product name.
11. Smart Mail still contains the `NEW` badge.
12. Settings still exposes Smart Notes automatic and an Intelligence Layer toggle, contrary to the receiver contract.
13. The obsolete “Your life creates intelligence every day…” message exists in generated/rendered paths and must be removed at its source, not merely hidden.
14. The greeting currently falls back to Canada when locale/country information is unavailable, which violates the country-truth rule. Locale is not sufficient proof of physical country.

### Deployment/source authority — newly established

There is currently more than one Hub deployment path:

- `NAYANETHUBONE.html` is the user-designated authoritative source.
- `.github/workflows/build-nayanethub-current.yml` builds `NAYANETHUB.html`, not `NAYANETHUBONE.html`, and performs source mutations during CI.
- `.github/workflows/deploy-v7-intelligent-hub.yml` deploys the separate `CLOUDFLARE-INTELLIGENT-HUB-V7/index.html` artifact.
- `CLOUDFLARE-INTELLIGENT-HUB-V7/worker.js` serves that separate artifact and injects `v7-intelligence-distribution.js`.
- `CLOUDFLARE-INTELLIGENT-HUB-V7/v7-smart-note-runtime.js` represents another Smart Note runtime boundary and currently uses an older four-representation transaction model.

Therefore the source → artifact → deployment → exact runtime chain is **not yet one authoritative chain**. This is a release-blocking receiver issue, not a cosmetic issue.

The current build workflow also validates for `nh-greeting-script`, while the inspected `NAYANETHUBONE.html` contains a different welcome runtime identifier. That mismatch must be resolved before the build can be considered trustworthy.

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
7. Duplicate ingestion is prevented by a stable event/idempotency identity.
8. A real Daily Intelligence Report can be rendered beautifully in the intended Hub location.
9. The receiver can be independently observed after a source event is written.
10. Invalid, unauthorized, malformed, duplicate, and replayed events fail safely without corrupting existing intelligence.
11. Receive processing is observable through explicit lifecycle states rather than a vague “synced” claim.

### Sender: PARTIALLY READY, NOT YET PROVEN END-TO-END

GitHub can persist Smart Note artifacts, and repository automation exists, but **GitHub write → trigger → Hub receive → render** is not yet independently proven as one working transaction.

A GitHub commit is therefore currently an **observed durable write**, not proof of Hub delivery.

## 4. Priority Order

### Priority 0 — Source / Deployment Authority Lock

Before changing the pipeline, establish exactly which Hub file is authoritative for production and which deployment path serves it.

**Deliverable:** one explicit source → build → deployment → runtime chain using `NAYANETHUBONE.html` as the source of truth.

**Release gate:** no duplicate/competing Hub HTML source is allowed to silently become authoritative.

### Priority 1 — Finish the Hub Receiver Experience

Mold the Hub first, exactly as Shawn requested, so it is ready before the engines are turned on.

Finish and verify:

- Smart Note boards/cards and **five-perspective** presentation.
- Intelligent Feed behavior.
- Personal / Collective modes using the existing feed/event architecture.
- One canonical action system with Personal `Favorite → Save → Share` and Collective `Love → Rank → Comment → Save → Share`.
- Five visible selectable stars.
- Inline Collective comments beneath the relevant note.
- Your Intelligence Today as the intelligence/highlights layer, not a second Smart Notes feed.
- Daily Intelligence Report presentation and historical navigation.
- Smart Share placement.
- Smart Spaces / Smart Lists / Smart Mail naming and placement.
- Human-readable Settings.
- Dynamic greeting and truthful country detection.
- Obsolete message removal at its source/render path.
- Search/history behavior.
- Empty/loading/error states for real incoming intelligence.
- Duplicate-event handling.
- Invalid/replay/unauthorized event handling.
- Responsive presentation.

**Release gate:** a manually supplied canonical Smart Note and a manually supplied Daily Intelligence Report payload can both be rendered correctly without modifying the receiver during the test.

### Priority 2 — Define the Receiver Contract

Write the exact machine contract the Hub accepts.

The receiver contract must define:

- `event_id`
- `event_type`
- `timestamp`
- `source`
- `project/context`
- `title/summary`
- the five perspectives: `ai_naya`, `human`, `machine`, `child`, `grandma`
- tags/type/metadata actually rendered
- authorization/privacy state
- stable `idempotency_key`
- event version/update semantics
- historical placement
- receipt/lifecycle state
- validation rules
- rejection/error behavior
- duplicate/replay behavior
- forward/backward compatibility rules

**Receiver lifecycle:**

`RECEIVED → VALIDATED → ACCEPTED → PERSISTED → RENDERABLE → RENDERED → RETRIEVABLE → VERIFIED → RECEIPTED`

Failures must remain explicit, e.g. `REJECTED`, `DUPLICATE`, `UNAUTHORIZED`, `MALFORMED`, or `FAILED`, rather than being represented as success.

**Release gate:** one sample event can be validated before ingestion, one duplicate can be rejected idempotently, and one malformed/unauthorized event can be rejected without changing stored intelligence.

### Priority 3 — Establish the Receiver Ingestion Boundary

The Hub must have exactly one canonical ingestion boundary for Smart Notes.

The boundary must accept the canonical event, validate it, enforce authorization/privacy, enforce idempotency, persist it using the existing intelligence architecture, and hand it to the existing Hub rendering pipeline.

The receiver boundary must **not** create a second Smart Notes database, second feed, or second event schema.

The preferred architectural shape is:

`POST/authorized receive → validate → canonical event store → existing Smart Notes/Intelligent Feed renderer`

The final transport mechanism may be an authenticated Cloudflare Worker endpoint, existing supported backend endpoint, or another already-authorized route. The choice must be based on the repository's actual supported infrastructure, not guesswork.

**Release gate:** a controlled canonical event can enter the receiver boundary and become visible without editing the Hub manually.

### Priority 4 — Build the Sender/Transport

Only after the receiver is ready and its contract is locked, choose and implement one authoritative transport route. The desired behavior is:

`Smart Note created → canonical GitHub artifact committed → trigger fires → receiver endpoint/ingestion path receives event → event is persisted/registered → Hub updates`

The trigger mechanism must be explicit. Options may include GitHub Actions calling a secure ingestion endpoint or another already-supported repository event mechanism. Do not add a second competing transport if an existing supported path can be used.

**Release gate:** a controlled test commit produces exactly one receiver ingestion event.

### Priority 5 — Connect Daily Intelligence Report

Treat the Daily Intelligence Report as a separate intelligence product built from the same underlying intelligence pipeline, not as another Smart Notes feed.

Target chain:

`Real intelligence → Smart Notes / intelligence records → Daily Intelligence Report generation → report persistence → Hub report layer → historical report navigation`

The report must be visually finished before production automation is enabled.

**Release gate:** Today, Yesterday, This Week, and This Month can be navigated and the report is rendered from real stored data.

### Priority 6 — Establish Full Receiver Error/Replay Safety

Before enabling the sender, test the receiver against:

- valid event
- duplicate event
- replay of an already processed event
- malformed payload
- missing required perspective
- wrong event type
- unauthorized/private event
- future/unknown event version
- update to an existing event
- transport retry
- partial persistence failure

The receiver must fail closed where authorization or identity is uncertain and must never silently create a second intelligence event.

**Release gate:** failure behavior is deterministic, observable, and does not damage existing intelligence.

### Priority 7 — End-to-End Test

Run one real event through the entire system.

Test command:

> “Hey, make a Smart Note about this.”

Expected behavior:

1. Naya recognizes Smart Note intent.
2. Naya restores the canonical protocol and relevant known intelligence.
3. Naya creates exactly one Smart Note event.
4. The event contains the five required perspectives.
5. The canonical event is written to GitHub.
6. The authorized trigger/transport fires exactly once.
7. The Hub receiver validates and accepts the event.
8. The Hub persists the canonical event.
9. The Hub renders it in the intended Smart Note presentation.
10. The event is retrievable through the intended history/search path.
11. Your Intelligence Today reflects it without becoming a duplicate feed.
12. The Daily Intelligence Report can consume it from the same underlying intelligence architecture.
13. No duplicate event/feed/control/report is created.
14. Evidence is captured for each transition.

**Release gate:** complete chain verified, not inferred.

### Priority 8 — Lock the Official Activation Protocol

Only after the real Hub test succeeds should the final **Smart Notes ↔ Intelligent Hub Activation Protocol** be written/locked.

That document should describe proven behavior, not intended behavior.

## 5. Verification Model

Every pipeline test must distinguish:

- **OBSERVED** — the source/event was seen.
- **CAPTURED** — the Smart Note was created.
- **PERSISTED** — the canonical artifact exists in GitHub.
- **TRIGGERED** — the integration automation actually fired.
- **RECEIVED** — the Hub ingestion layer accepted the event.
- **VALIDATED** — the payload passed schema, authorization, and idempotency checks.
- **RENDERED** — the event visibly appears in the Hub.
- **RETRIEVABLE** — the event can be found again.
- **VERIFIED** — independent evidence confirms the expected behavior.
- **RECEIPTED** — the durable receipt records the verified transition.

Never collapse these into a single claim of “sync successful.”

## 6. Failure Rule

If any stage fails:

**STOP → INSPECT → DIAGNOSE → SEARCH KNOWN SOLUTIONS → TRY THE SAFEST SUPPORTED ROUTE → VERIFY → RECORD THE LESSON → CONTINUE**

Do not repeatedly retry the same failed route. Protect the current working source.

If the same execution route fails three times, stop automatic retries and document the failure count, learning, and safest alternative route.

## 7. Definition of Done

The Smart Note + Intelligent Hub pipeline is ready only when all of the following are true:

- One authoritative Hub source is locked: `NAYANETHUBONE.html`.
- Source → build → deployment → exact public runtime parity is proven.
- One receiver ingestion boundary is defined and implemented.
- Receiver contract is defined and implemented.
- Smart Note five-perspective data is accepted without transformation that loses meaning.
- Authorization/privacy enforcement is working.
- Stable event identity/idempotency is working.
- GitHub persistence is working.
- GitHub trigger/transport is working.
- Hub ingestion is working.
- Smart Note presentation is finished.
- Personal/Collective action behavior is one coherent system.
- Five-star ranking and inline comments are working.
- Your Intelligence Today is a highlights/report layer backed by the same intelligence records.
- Daily Intelligence Report presentation is finished.
- Historical intelligence is working.
- Historical Daily Intelligence Reports are working.
- Duplicate/replay/error handling is working.
- Search/retrieval is working.
- A real Smart Note completes the full pipeline.
- A real Daily Intelligence Report completes its pipeline.
- Independent observation verifies the live result.
- Only then is the integration activation protocol locked.

## 8. Execution Doctrine

**We finish and verify the receiver first. Then we lock the receiver contract. Then we establish the single ingestion boundary. Then we build the sender/trigger. Then we connect the two. Then we test the complete pipeline. Then we write the final activation protocol from what actually works.**

No redesign. No parallel intelligence systems. No duplicate Smart Notes feed. No guessed triggers. No silent fallback to browser-local data when a real incoming event is expected. No declaration of success without runtime evidence.

**Current execution rule:** The receiver is not “ready” merely because the page looks complete. It is ready only when a valid canonical five-perspective Smart Note can enter through the defined boundary, survive validation/idempotency/privacy checks, persist through the existing architecture, render in the Hub, remain retrievable, and produce observable evidence of that path.

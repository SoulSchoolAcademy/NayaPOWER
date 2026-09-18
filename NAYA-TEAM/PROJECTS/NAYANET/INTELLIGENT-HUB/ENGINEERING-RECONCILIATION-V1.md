# Intelligent Hub — Engineering Reconciliation V1

**STATUS:** EXECUTABLE
**DATE:** 2026-09-18

## Objective
Reconcile the V2 Intelligent Hub blueprint against contracts #40–#58 and current repository/runtime implementation. Convert each material mismatch into a bounded engineering task.

## Source truth inspected
- Protected root Hub: `2026 09 17 NAYANET HUB.html`
- React Hub: `NAYANET/HUB/`
- Assistant/Cloudflare release: `.github/workflows/assistant-cloudflare-hub-release.yml`
- React/Vercel release: `.github/workflows/deploy-nayanet-intelligent-hub.yml`
- Blueprint: `NAYA-TEAM/PROJECTS/NAYANET/INTELLIGENT-HUB/README.md`
- Contracts: #40–#58 under `.naya/`

## Key finding
The repository currently has two credible Hub lanes. The root HTML is the protected Assistant/Cloudflare release artifact. The React lane contains structured routes, identity/session code, PIS loading and typed SmartFeedBoard behavior and has a separate Vercel deployment workflow. Until their roles are explicitly reconciled, builders can improve different Hubs.

## Task queue

### IH-01 — Reconcile Hub source/runtime authority
Inventory all current Hub artifacts and deployment workflows; identify the intended canonical implementation; classify the other lane as retained implementation, migration source, experimental, historical, superseded, or dead only when evidence supports it; bind one authoritative verification path.

**Acceptance:** cold Naya can name one canonical source → build → deployment → runtime → verification path without inference.

### IH-02 — Convert the protected visual contract into executable UI behavior
Map #40's required Intelligent Block, three feeds, Naya presence, actions, living depth, semantic layers and responsive requirements to actual runtime elements. Preserve the protected visual baseline while replacing decorative behavior with real behavior.

### IH-03 — Prove canonical intelligence identity
Take one canonical event/Smart Note through event → PIS → IntelligentEvent → Intelligent Block → feed. Preserve stable identity, timestamp, provenance, privacy and verification state. Prove no copied object becomes a second truth.

### IH-04 — Prove real feed projections
For Activity, Personal and Collective, prove source event, authorization, projection and rendering separately. Feed switching alone is not proof.

### IH-05 — Move consequential Hub actions to canonical writes
The React SmartFeedBoard currently persists favorites, saves, reactions, comments, links and Space state to localStorage. Treat that only as client cache/optimistic state. Completion of a consequential action must depend on the canonical authorized event/write boundary and a truthful result.

### IH-06 — Prove PIS → Hub provenance
Create/receive one fresh intelligence event and prove it reaches PIS, is retrieved by the Hub, renders with source/event identity and current truth state, and remains traceable.

### IH-07 — Prove Smart Link lifecycle
Create a canonical link, resolve it from a clean session, enforce private/public visibility, and show truthful invalid/revoked behavior. Never put secrets in URLs.

### IH-08 — Make the Hub honestly living
Create an authorized test event after Hub load. Observe live delivery without refresh, or expose truthful DEGRADED/REFRESH state when no realtime transport exists. Never infer realtime from animation.

### IH-09 — Make search canonical and authorized
Replace local-only matching as the source of truth with authorized retrieval over canonical intelligence. Preserve stable identity and truth state. Distinguish no results from retrieval failure.

### IH-10 — Reconcile release/runtime truth
Prove exact source commit → build artifact → deployment → public runtime → independent observation. The two existing workflows must not leave two silently competing production meanings.

### IH-11 — Execute #52 full acceptance
Run the current-head journey: welcome → identity → Hub → intelligence → action → canonical event → Activity → Smart Note → evidence → verification → continuation, including failure cases and responsive runtime checks.

### IH-12 — GitHub bridge vertical slice
Prove one authenticated GitHub event enters the canonical event layer, is normalized, persisted, projected to Activity, and observed in the Hub. A webhook receipt alone is insufficient.

### IH-13 — Hub-visible continuity
Expose canonical current state, evidence and exactly one next action in the Hub/Today experience, with a successor-ready record for the next Naya.

### IH-14 — Production identity/PWA entry
Replace prototype-only identity establishment and Academy handoff with the authoritative identity/session boundary. Prove first activation, returning-session restore, invalid-session handling, and correct Hub entry.

### IH-15 — Trust-loop proof
Independently verify one complete transaction: human intent → Naya understanding → authorized action → actual execution → observation → evidence → human visibility → learning → next action. Record the receipt and state update.

## Completion law
Every task must reach:
**IMPLEMENTED → TESTED → OBSERVED → INDEPENDENTLY VERIFIED → RECORDED → STATE UPDATED → SUCCESSOR READY.**

No task may create a competing event store, memory system, queue, authority system, or second Hub source of truth.

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


## IH-01 EXECUTION RECEIPT — 2026-09-18

**RESULT: CLOSED / RECONCILED**

Repository evidence resolved the apparent source conflict under the existing higher-authority Hub routing contract. No Hub source was promoted and no protected artifact was modified.

### Classification
- **CURRENT / PROTECTED:** `2026 09 17 NAYANET HUB.html`
- **ACTIVE REFERENCE:** `NAYANET/HUB/` React/Vite implementation
- **HISTORICAL / CONFLICTING RELEASE DOCS:** `NAYANET/HUB/CANONICAL-RELEASE-STATUS-2026-09-09.md`, `NAYANET/HUB/RELEASE-MARKER.md`
- **HISTORICAL / REFERENCE:** older standalone Hub versions, E02/E03 artifacts and legacy live Hub copies identified by repository inventory
- **PROJECTION / EVIDENCE:** generated build output, runtime copies and runtime-target metadata

### Binding
The canonical operating path is now explicitly:

**CURRENT PROTECTED FREEZE → NEW VERSIONED CANDIDATE → VERIFY → REGRESSION CHECK → COMMIT → HANDOFF → SHAWN ACCEPTS → PROMOTE FREEZE**

The React implementation remains available as engineering reference. It cannot redefine the current Hub merely by being more structured, deployable, or technically sophisticated.

### Acceptance
A cold Naya can now determine the current Hub, protected artifact, reference implementation, historical material, editing rule, and promotion path without conversational archaeology.

### Next
**IH-02 — convert the protected visual contract into verified real UI behavior, using a new versioned candidate and leaving the protected freeze point untouched.**


## IH-02 EXECUTION RECEIPT — 2026-09-18

**RESULT: IMPLEMENTATION RECONCILED / VERSIONED CANDIDATE CREATED**

### Visual / experience contract reconciliation

The protected Hub already contains substantial proven visual DNA: obsidian foundation, atmospheric illumination, strong typography, dimensional controls, semantic color, Smart Note/intelligence layers, Naya presence, search, feed lenses, responsive behavior, and progressive intelligence presentation.

The React lane contains the stronger typed/application structure: route ownership, identity context, PIS retrieval, typed `IntelligentEvent`, and the canonical `SmartFeedBoard`. It also exposes the critical truth boundary: several user actions currently persist only to browser `localStorage`, and Ask Naya / Related Intelligence / Smart Space are not yet verified as production-backed capabilities.

Therefore IH-02 does **not** promote the React lane and does **not** edit the protected freeze. The first candidate preserves the protected visual/experience baseline and makes the interaction truth explicit.

### Versioned candidate

**Candidate:** `2026 09 17 NAYANET HUB V2.html`

The candidate is derived from the protected freeze point and adds an explicit **IH-02 INTERACTION TRUTH** surface. It is a candidate only; it is not the current freeze and is not production-proven.

### Interaction classification

| Required interaction | Classification | Truth boundary |
|---|---|---|
| Navigation / route switching | REAL | Candidate navigation is operational, but destination completeness is not yet proven. |
| Search intelligence | REAL | Searches currently loaded candidate intelligence only. |
| Feed lens switching | REAL | Lens state changes; canonical backend projection is not yet proven. |
| Open Intelligent Block | REAL | Opens the established intelligent-board presentation. |
| Favorite | PARTIAL | Browser-local persistence; no canonical write proof. |
| Save | PARTIAL | Browser-local persistence; no canonical write proof. |
| Like / Love | PARTIAL | Browser-local state; no canonical event/write proof. |
| Rate / Rank | PARTIAL | Browser-local state; no verified ledger/curation write. |
| Comment | PARTIAL | Browser-local state; no verified canonical communication write. |
| Share | PARTIAL | Native/clipboard share exists; governed Smart Share lifecycle is not proven. |
| Ask Naya | DEMO | Deterministic contextual answers; not a verified production Naya service. |
| Related Intelligence | DEMO | Static related references; canonical graph resolution not proven. |
| Create Smart Space | DEMO | Local draft behavior; canonical Space lifecycle not proven. |
| Apply / Use | PARTIAL | Data-driven guidance exists; governed action execution is not connected. |
| Trust / provenance / privacy | REAL | Existing fields are surfaced without fabricating missing evidence. |
| Responsive desktop/mobile | REAL | Responsive behavior is implemented and preserved. |
| Keyboard/focus/accessibility | PARTIAL | Accessibility hooks exist; complete audit remains outstanding. |
| Authoritative persistence | PARTIAL | Persistence boundary is explicit but not yet canonical for Hub actions. |
| Activity receipt from Hub action | MISSING | No proven automatic canonical Activity event for every substantive UI action. |
| Authenticated identity lifecycle | PARTIAL | Present in React reference; not established by this standalone candidate. |
| Production runtime equivalence | MISSING | Candidate requires build/deploy/independent runtime verification. |

### Engineering consequence

The candidate is now the **visual/experience comparison surface** for IH-03+. It must not be treated as current Hub authority until independently verified and explicitly accepted.

The highest-value remaining mismatch is no longer visual ambiguity. It is **canonical intelligence identity and persistence**: one real event must survive event → PIS → Hub → interaction without becoming a local-only copy.

### IH-02 acceptance

- Protected freeze untouched.
- New versioned candidate created.
- Visual DNA preserved rather than replaced.
- React implementation inspected as the engineering reference.
- Every required interaction has a truthful REAL / PARTIAL / DEMO / MISSING classification.
- No second renderer, event store, memory system, queue, or authority system created.
- Candidate explicitly remains non-canonical until acceptance.

### NEXT ACTION

**IH-03 — prove one canonical intelligence identity end-to-end: canonical event → PIS → IntelligentEvent → Intelligent Block → feed, preserving stable event ID, timestamp, provenance, privacy and verification state.**

# NayaNET — INTELLIGENT HUB

**BLUEPRINT STATUS:** VERIFIED
**BLUEPRINT VERSION:** V2 — 2026-09-18
**ROLE:** Human-facing living intelligence environment; not a dashboard or source of truth.

## 1. WHAT IT IS
Human-facing living intelligence environment; not a dashboard or source of truth.

## 2. PRIMARY JOB
Render canonical intelligence/events into understandable, actionable blocks and feeds. Core journey: current intelligence → understand → act → verify → continue.

## 3. SYSTEM BOUNDARY
Inputs: canonical events, Smart Notes, PIS, activity, identity/permissions. Outputs: Hub views/actions/receipts. Reuse existing Intelligent Event/Block architecture.

## 4. HUMAN EXPERIENCE / PRESENTATION
Visual: obsidian/black surfaces, living depth, restrained semantic edge light, strong typography, responsive desktop/mobile. Every major action must be real.

## 5. CONNECTIONS
Must connect to Smart Feed, Today, Notes, Reports, Lists, Connections, Spaces, Mail, Share, Activity, Search and Naya presence.

## 6. 01–58 DEEP-DIVE SOURCES
This blueprint is distilled from the corresponding NayaPOWER 01–58 intelligence/contracts and the current repository implementation. Relevant 01–58 areas: **Must connect to Smart Feed, Today, Notes, Reports, Lists, Connections, Spaces, Mail, Share, Activity, Search and Naya presence.**.

## 7. ENGINEERING RULES
- Inspect current repository/runtime before changing implementation.
- Reuse canonical NayaPOWER primitives; do not create a competing store, event system, memory system, queue, or authority system.
- Preserve stable identity, timestamps, provenance, privacy and truth state.
- Separate **canonical source → event → projection → presentation → interaction**.
- Capability never creates authority.
- Activity is a projection; Smart Notes are intelligence; the Hub is presentation; the Ledger is evidence/integrity.
- Unknown remains UNKNOWN. Documentation is not runtime proof.
- Builder ≠ Judge: the implementer does not certify its own work.
- Preserve valuable existing Hub behavior and evolve surgically unless evidence requires reconstruction.

## 8. ACCEPTANCE CONTRACT
A production-ready implementation must demonstrate:
1. Real source/data ownership is identified.
2. The feature has a single clear boundary and does not duplicate another system.
3. Identity, permissions and visibility are enforced at the appropriate boundary.
4. Timestamps and stable IDs survive every projection.
5. The human can understand what the feature is, why it exists, and what action is available.
6. Actions are real, not decorative.
7. Failure is visible and recoverable.
8. Source → execution → observed behavior → verification is proven.
9. Evidence and the next action are recorded.
10. A cold Naya can continue without conversational archaeology.

## 9. CURRENT GAP
**40,41,42,43,45,48,49,50,51,52,54,55,56,57,58**

## 10. ONE NEXT ACTION
**40,41,42,43,45,48,49,50,51,52,54,55,56,57,58**

## 11. SYSTEM POSITION
NayaNET is one connected product, not 19 independent applications:

**NayaPOWER → canonical intelligence/events/state → NayaNET Intelligent Hub → human/Naya action → verified outcome → new intelligence → continuation.**

This area is therefore a **capability/view within that system**, not an independent authority or database.

## 12. DO NOT BUILD
- A second source of truth.
- A parallel event store.
- A parallel Smart Note or memory system.
- A new authority ladder.
- A feature that only looks complete in the UI.
- A duplicate copy of canonical intelligence merely for presentation.

## 13. DEFINITION OF DONE
**IMPLEMENTED → TESTED → OBSERVED → INDEPENDENTLY VERIFIED → CONNECTED → RECORDED → STATE UPDATED → SUCCESSOR READY.**

Where the area is human-facing, add **LIVE VERIFIED** before calling the runtime complete.


# Engineering Reconciliation — Intelligent Hub V1
**DATE:** 2026-09-18  
**STATUS:** OPEN — implementation does not yet fully match the blueprint

## Repository truth
There are two materially different Hub implementation lanes: the protected root `2026 09 17 NAYANET HUB.html`, released by `.github/workflows/assistant-cloudflare-hub-release.yml`, and the React application under `NAYANET/HUB/`, released by `.github/workflows/deploy-nayanet-intelligent-hub.yml` to Vercel. This is the primary #41/#51/#55 mismatch. No deletion is implied; classify first.

## Contract reconciliation
| Contract | Current evidence | State | Executable task |
|---|---|---|---|
| #40 | Protected root HTML has substantial living-depth UI, Intelligent Blocks, feeds, Naya, search and responsive behavior | PRESENT / PARTIAL | IH-02: map every required interaction to a real governed behavior |
| #41 | Root HTML and React Hub are both credible implementation lanes | MISMATCH | IH-01: establish one canonical source/runtime lane and classify the other |
| #42 | React has typed `IntelligentEvent`/SmartFeedBoard; root HTML renders nine-layer intelligence presentation | PARTIAL | IH-03: prove one stable intelligence identity from canonical event through PIS/block/feed |
| #43 | React exposes personal/activity/collective lenses; root HTML exposes feed controls | PARTIAL | IH-04: prove authorized projections from canonical events, not UI-only switching |
| #44 | Canonical event primitives exist, but React SmartFeedBoard persists actions to localStorage | MISMATCH | IH-05: make consequential Hub action completion depend on canonical event persistence |
| #45 | PIS loader/generated feed and event/runtime primitives exist | PARTIAL | IH-06: prove fresh event → PIS → Hub with provenance/truth state |
| #48 | Identity/link concepts exist; end-to-end authorized resolution is not proven | UNPROVEN | IH-07: prove create → clean-session resolve → privacy enforcement |
| #49 | No single observed realtime transaction is established | UNKNOWN | IH-08: prove event → live UI update or truthful DEGRADED/REFRESH state |
| #50 | React query dispatch/local matching exists | PARTIAL | IH-09: connect retrieval to authorized canonical intelligence and distinguish empty/failure |
| #51/#55 | Cloudflare deploys root HTML while Vercel deploys React; historical artifacts remain | MISMATCH | IH-10: reconcile source → build → deployment → runtime → verification |
| #52 | Runtime scripts cover substantial UI but not the complete 21-step journey | PARTIAL | IH-11: execute current-head end-to-end acceptance |
| #53 | GitHub bridge infrastructure exists, but Hub consumption is not proven as one production transaction | UNKNOWN | IH-12: prove GitHub event → canonical event → Activity → Hub |
| #54/#57 | State/handoff and Team Naya continuity exist; Hub-facing continuation is not proven | PARTIAL | IH-13: expose current state, evidence and one next action from canonical records |
| #56 | React identity exists; contract identifies localStorage/query-name prototype and Academy redirect | MISMATCH | IH-14: replace prototype identity establishment with authoritative identity/session → Hub |
| #58 | Evidence/runtime pieces exist, but full trust loop is not observed as one transaction | PARTIAL | IH-15: independently verify one complete governed Hub trust loop |

## Engineering order
**IH-01 → IH-02 → IH-03 → IH-05 → IH-06 → IH-04 → IH-10 → IH-07 → IH-09 → IH-08 → IH-11 → IH-12 → IH-13 → IH-14 → IH-15**

Do not parallelize source/runtime authority work. Do not create another Hub, event store, memory system, queue, or authority system.

## IH-01 acceptance
A cold Naya must be able to identify one canonical Hub source, its build path, deployment workflow, runtime URL, authoritative verification script, and the explicit status of the other implementation lane. Classification precedes retirement.

## Current engineering score
**Blueprint readiness:** 9.5/10  
**Implementation alignment:** 6.5/10  
**Complete runtime proof:** UNKNOWN  
**Primary blocker:** competing credible source/deployment lanes.

## Single next action
**Execute IH-01: reconcile the protected root HTML lane and React `NAYANET/HUB` lane into one explicit canonical Hub source → build → deployment → runtime → verification path, without deleting either lane until its role is proven.**


## IH-02 IMPLEMENTATION RECONCILIATION — 2026-09-18

**STATUS:** CLOSED — VERSIONED CANDIDATE CREATED

The protected `2026 09 17 NAYANET HUB.html` visual baseline was reconciled against the active React reference implementation. The protected file was not edited.

### Candidate

`2026 09 17 NAYANET HUB V2.html`

This is a versioned visual/experience candidate, not the current freeze and not production-proven.

### Truth classification

- **REAL:** navigation, search over available intelligence, feed-lens state switching, Intelligent Block opening, trust/provenance/privacy display, responsive behavior.
- **PARTIAL:** Favorite, Save, Like/Love, Rate/Rank, Comment, Share, Apply/Use, accessibility, authoritative persistence, authenticated identity lifecycle.
- **DEMO:** Ask Naya, Related Intelligence, Create Smart Space.
- **MISSING:** automatic canonical Activity receipt from substantive Hub actions; production runtime equivalence.

The classification is intentionally conservative: **REAL means implemented behavior, not production proof.**

### Engineering meaning

The visual contract is now represented by a safe versioned candidate while the React lane remains the engineering reference. The next work is not another visual redesign. It is proving the canonical intelligence path and replacing local/demo behavior with governed connections where the repository already provides the necessary primitives.

### IH-02 → IH-03

**Next:** prove one canonical intelligence identity from **canonical event → PIS → IntelligentEvent → Intelligent Block → feed**, preserving stable identity, timestamp, provenance, privacy and verification state.

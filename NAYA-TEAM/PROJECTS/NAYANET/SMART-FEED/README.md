# NayaNET — SMART FEED

**BLUEPRINT STATUS:** PARTIAL
**BLUEPRINT VERSION:** V2 — 2026-09-18
**ROLE:** Living presentation layer for Activity, Personal Intelligence, and Collective Intelligence.

## 1. WHAT IT IS
Living presentation layer for Activity, Personal Intelligence, and Collective Intelligence.

## 2. PRIMARY JOB
Show the right intelligence in the right context without becoming storage. Distinguish event, intelligence, presentation and interaction.

## 3. SYSTEM BOUNDARY
Inputs: canonical events/PIS/Smart Notes; filters: permission, visibility, relevance, time, verification. Outputs: feed projections and real interactions.

## 4. HUMAN EXPERIENCE / PRESENTATION
Three clear modes: Activity = what happened/is happening; Personal = private intelligence; Collective = explicitly shared intelligence. Intelligent Blocks are the visual primitive.

## 5. CONNECTIONS
Connect to Notes, PIS, Activity, Search, Tabs, Lists, Share, Spaces, Connections and Reports.

## 6. 01–58 DEEP-DIVE SOURCES
This blueprint is distilled from the corresponding NayaPOWER 01–58 intelligence/contracts and the current repository implementation. Relevant 01–58 areas: **Connect to Notes, PIS, Activity, Search, Tabs, Lists, Share, Spaces, Connections and Reports.**.

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
**8,39,40,42,43,45,46,49,50,57,58**

## 10. ONE NEXT ACTION
**8,39,40,42,43,45,46,49,50,57,58**

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

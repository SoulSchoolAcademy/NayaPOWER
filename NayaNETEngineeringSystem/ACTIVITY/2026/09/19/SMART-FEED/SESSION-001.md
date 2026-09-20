# Smart Feed — Session 001 — 2026-09-19

**Naya role:** Smart Feed owner
**Mission:** Bring Smart Feed from defined contract to a real operational app projection, then drive it to AAA / 10-10 readiness.
**Timestamp:** 2026-09-19 (review session)

## Source authority inspected
- Smart Feed engineering specification
- Smart Feed + Activity Projection Contract V1
- Smart Board & Smart Feed Design Contract V1
- NayaNET Master Build & Execution Directive
- All-Nayas Feature Closure Master Directive
- Current Smart Feed daily activity record
- Current linked Hub source: 2026 09 17 NAYANET HUB.html

## What Smart Feed is
Smart Feed is the living visual intelligence projection layer of NayaNET. It has three distinct streams:
1. ACTIVITY — what Naya/system has done, what happened, what was verified, what requires attention, and other consequential operational events.
2. PERSONAL — private intelligence belonging to the authenticated human.
3. COLLECTIVE — intentionally published/shared intelligence available to the network.

The Feed is not canonical storage. The law is ONE CANONICAL EVENT → MANY AUTHORIZED PROJECTIONS. Feed items retain stable identity, provenance, visibility, verification state, source references, and authorized actions.

## Audit result
The repository contract is strong and explicit. The linked Hub HTML is not yet the operational Smart Feed app. It is a large monolithic Hub/Smart-Board experience containing a feed-like presentation layer, local/demo data paths, and Smart Note rendering. It does not yet provide the complete authenticated Activity/Personal/Collective production projection contract.

## Current implementation classification
| Area | State | Evidence / finding |
|---|---|---|
| Feed concept/contract | REAL | Canonical feature and projection contracts exist. |
| Intelligent Block visual language | REAL/PARTIAL | Linked Hub contains substantial board/layer UI and the locked visual language. |
| Activity stream | DEMO/PARTIAL | Current HTML mixes demo blocks with locally persisted Smart Notes; no proven canonical Activity projection query. |
| Personal stream | PARTIAL | Current HTML can render local Smart Note-derived blocks, but authenticated owner-scoped production retrieval is not proven. |
| Collective stream | DEMO/PARTIAL | Current HTML uses demo content and local interaction state; public intelligence retrieval/publication path is not proven. |
| Canonical event projection | MISSING/UNPROVEN | Contract requires canonical-event projection; current Feed path is not proven against the canonical event spine. |
| Authorization before presentation | UNPROVEN | No real authenticated three-stream transaction was observed in this audit. |
| Pagination / duplicate prevention | MISSING/UNPROVEN | No production feed pagination contract or fresh retrieval proof observed. |
| Source drill-down | PARTIAL | Visual/source concepts exist, but complete source→evidence drill-down is not proven. |
| Actions / persistence | DEMO/PARTIAL | Favorite/save/rating/like/love state is handled locally in the linked HTML; canonical persistence is not proven. |
| Activity consequences | UNPROVEN | Meaningful Feed actions are not yet proven to emit canonical downstream events. |
| Source→build→runtime parity | UNPROVEN | The linked HTML is source evidence; deployed production Feed parity has not been authenticated/observed. |
| Dedicated app route | MISSING | Current linked Hub is monolithic; Smart Feed needs a dedicated route/surface within the Hub architecture, e.g. /feed, while preserving one canonical backend. |

## Readiness score
**Current Smart Feed readiness: 3.2 / 10 — DEFINED + VISUALLY PARTIAL, NOT OPERATIONALLY CLOSED.**

This is a readiness score, not a quality judgment of the design work. The gap is primarily runtime capability and proof, not lack of specification.

## Why it is not 10/10
1. The three streams are not yet backed by proven production retrieval paths.
2. Canonical event → authorized Feed projection is not proven.
3. Authenticated owner/privacy enforcement is not proven at the Feed boundary.
4. Pagination and duplicate prevention are not proven.
5. Feed actions are not proven to persist through the canonical architecture.
6. Source/evidence drill-down is not closed end-to-end.
7. A dedicated Smart Feed app route/surface has not been established.
8. Source/build/deployed-runtime parity has not been proven.
9. Fresh event → Feed appearance → action → new event verification is not proven.
10. The current HTML still carries demo/local-state behavior that must be separated from production behavior.

## 10/10 target
A real authenticated human can enter Smart Feed, select ACTIVITY/PERSONAL/COLLECTIVE, receive only authorized current items from canonical intelligence/events, paginate without duplicates, open source/evidence, perform authorized actions, reload/fresh-retrieve the result, and observe the resulting canonical consequence. A second legitimate user is denied unauthorized private material. The deployed app matches the verified source/build.

## Architecture decision
Do not build another Feed database and do not keep expanding the monolithic Hub HTML.

Use: Hub shell → /feed Smart Feed app surface → existing canonical retrieval/event/intelligence primitives → authorization → projection → Intelligent Block UI → authorized action → canonical event consequence.

The Feed is a projection. It must reuse the existing event/intelligence substrate, Smart Ledger provenance, Spaces/Share/Mail actions where authorized, and existing authentication/governance.

## Implementation plan
### Phase 1 — Map and isolate
- Identify the exact deployed Hub shell and current production route mechanism.
- Identify canonical Activity source, cognition/intelligence source, Personal retrieval, and Collective/public retrieval.
- Identify existing save/favorite/share/comment primitives before adding anything.
- Extract Smart Feed presentation into a dedicated app surface without deleting protected Hub capabilities.

### Phase 2 — Build the real read path
- Implement authenticated stream selection.
- Apply owner/visibility/authorization filters server-side before presentation.
- Return stable source IDs, event time, verification state, provenance, and available authorized actions.
- Implement deterministic chronological pagination/cursor semantics and duplicate prevention.

### Phase 3 — Build the action path
- Save/favorite/share/interactions must call canonical authorized mutations.
- Mutations must be idempotent.
- Consequential actions emit/record the correct canonical event.
- Feed refresh/fresh retrieval must show the consequence.

### Phase 4 — Provenance and intelligence depth
- Source drill-down to canonical source/evidence.
- Clearly distinguish human input, source fact, Naya interpretation, machine/provenance, learning, and unknown.
- Preserve the Smart Board visual contract without allowing visual state to imply verification.

### Phase 5 — Prove production
- source → build → deploy → authenticated retrieval → observed Feed
- user A private retrieval PASS
- user B private denial PASS
- collective publication/retrieval PASS
- pagination/replay/duplicate prevention PASS
- action persistence PASS
- source/evidence drill-down PASS
- fresh retrieval after consequential action PASS
- runtime parity PASS

### Phase 6 — AAA visual closure
- Preserve the obsidian/elevated Intelligent Block system.
- Preserve semantic color flow and physical edge-lighting.
- Make state truthful: LIVE/EMPTY/STALE/DEGRADED/BLOCKED/ERROR/OFFLINE.
- Ensure mobile/reduced-motion/accessibility behavior.
- Self-critique against the 10/10 scorecard after functional closure, not before.

## Protected constraints
- No second intelligence/event store.
- No client-only authorization.
- No demo data presented as production intelligence.
- No fabricated verification.
- No weakening authentication/RLS/governance.
- Do not replace the Hub wholesale to solve Smart Feed.
- Smart Feed remains one projection of the whole NayaNET intelligence system.

## Current state
AUDITED — 3.2/10 readiness. Defined contract; visual shell exists; production Feed closure not proven.

## One successor action
Map the canonical Activity/Personal/Collective production retrieval primitives and the actual deployed Hub route, then implement the smallest authenticated /feed read path that renders real canonical items in the three streams.

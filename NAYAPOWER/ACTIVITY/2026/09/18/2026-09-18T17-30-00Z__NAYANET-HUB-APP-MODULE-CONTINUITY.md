# NayaNET Intelligent Hub — Application Continuity Directive

**Timestamp:** 2026-09-18T17:30:00Z
**Project:** NayaNET
**Surface:** Intelligent Hub
**Canonical visual source:** `2026 09 17 NAYANET HUB.html`

## Decision

The September 17 handcrafted Hub is the canonical product and visual baseline. It must not be discarded or replaced by a new generic dashboard.

The Hub will be converted from a static presentation into a functioning authenticated application by preserving its existing DOM/design language, layout, buttons, feed, navigation, Smart Board composition, Personal Intelligence, Collective Intelligence, Activity, search, and Naya/Human/Machine perspectives while connecting those surfaces to Naya Power runtime services.

## Why

The user already has a visual/product language he considers correct. The engineering problem is not to invent a new interface. The problem is to make the existing interface real, persistent, authenticated, intelligent, and continuously connected to Naya Power.

## Application model

`Welcome → Login → Intelligent Hub → modules → Naya Power runtime`

The Hub is the authenticated destination inside NayaNET. Academy and other destinations become modules/linked surfaces rather than a mandatory intermediate gateway.

## Module boundary

1. **Hub Shell** — preserves the canonical composition and responsive behavior.
2. **Primary Navigation** — preserves existing navigation and page concepts.
3. **Intelligence Feed** — preserves Collective / Personal / Activity feed controls.
4. **Smart Boards** — preserves the existing block/layer presentation.
5. **Search** — becomes a projection/query surface over available intelligence.
6. **Naya Perspective** — preserves the existing Naya card and actions.
7. **Authentication Boundary** — establishes the authenticated NayaNET member session.
8. **Cognition Boundary** — persists and retrieves intelligence through the governed runtime.
9. **Continuity Boundary** — carries current mission, state, evidence, and next action forward.

## Runtime rule

The UI is a projection of intelligence. It is not a competing memory authority.

Canonical runtime truth remains in Naya Power / the canonical event and cognition stores. Human-facing Activity and Smart Notes remain projections and durable intelligence views.

## Acceptance criterion

No visual replacement. No generic React dashboard substitution. A change is successful only when the existing Hub remains recognizable while the real authenticated runtime begins powering its existing surfaces.

## Immediate implementation sequence

`canonical HTML → application module boundaries → authenticated session → Personal Intelligence retrieval → live feed projection → Smart Note persistence → verified continuation`


## Activity

**Type:** Architecture decision + implementation handoff
**Status:** ACTIVE
**Authority:** User-directed product architecture

The current activity state is that the canonical visual Hub is now the product baseline and the engineering task is applicationization, not redesign. Existing surfaces are to be preserved and connected to governed runtime boundaries.

**Current next action:** wire the existing Personal Intelligence/feed surface to the authenticated cognition boundary, observe real retrieval, and verify the result on the deployed Hub.

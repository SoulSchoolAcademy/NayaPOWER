# 🔱 Naya — Complete App Build Standard V1

**Status:** PROPOSED REUSABLE DESIGN / ENGINEERING INTELLIGENCE  
**Source intelligence:** SN-019 — Complete the App Doctrine  
**Applies to:** apps, websites, dashboards, Hubs, mobile/desktop interfaces and multi-page products.

## North Star

**PLAN THE WHOLE → BUILD THE WHOLE → PROVE THE WHOLE.**

A shell is infrastructure, never the finished product.

A vertical slice is a calibration/reference implementation, never permission to abandon the remaining declared scope.

## The completion system

Every substantive application build MUST maintain one machine-readable completion matrix covering:

- journeys;
- routes/pages/rooms;
- shared shell/navigation;
- design system;
- runtime/data owners;
- primary actions and causal paths;
- state matrix;
- cross-surface handoffs;
- responsive behavior;
- accessibility;
- performance;
- reliability/offline/recovery;
- proof;
- deployment/source parity.

Legal surface states:

`NOT_STARTED → SPEC_READY → DESIGN_READY → IMPLEMENTED → TESTED → INTEGRATED → INDEPENDENTLY_VERIFIED → PRODUCTION_PROVEN`

No lower state may be described as a higher state.

## Scope law

**Smallest effective slice controls BUILD ORDER, not PRODUCT SCOPE.**

Once the Human Director has declared the application scope, the task remains open until every required surface and whole-app journey reaches the applicable closure state or one true authority/external blocker is recorded.

Do not silently shrink scope to whatever was easiest to finish.

## Beautiful-interface law

Every surface is designed as an individual experience while inheriting one coherent civilization:

`PURPOSE → HUMAN OUTCOME → HIERARCHY → COMPOSITION → MATERIAL → LIGHT → TYPE → ICON → COLOR → MOTION → STATE → PROOF`

A new screen must pass:
- three-second orientation;
- clear primary action;
- unmistakable product identity;
- semantic state honesty;
- causal completeness;
- responsive identity;
- accessible control;
- performance discipline;
- anti-generic test;
- independent visual review.

Reuse primitives. Do not reuse one composition for every page.

## Non-regression law

When a surface passes its current quality gate, record a baseline:
- source SHA;
- screenshots or deterministic visual reference where available;
- route and state;
- interaction acceptance;
- accessibility/performance evidence;
- score.

Later work MUST prove it preserves or improves that baseline.

A cleaner refactor that makes the user experience worse is a regression.

## Function law

For every visible control:

`CONTROL → HUMAN INTENT → AUTHORITY/SCOPE → CAPABILITY → RUNTIME → OBSERVATION → UI STATE → EVIDENCE`

If the path does not exist, either build it or render the exact honest unavailable/blocked/unknown state.

## Whole-app integration law

A page can pass locally while the application still fails.

Required whole-app journeys must test:
- entry/onboarding;
- navigation/back/forward/reload;
- canonical object identity across surfaces;
- search/retrieval;
- persistence/return session;
- authorization/refusal;
- context changes;
- error/offline/recovery;
- responsive/mobile;
- accessibility;
- deployment parity.

## Scorecard law

Use the product's canonical scorecard. For NayaNET Hub: D1–D8.

Builder self-score is diagnostic. Independent re-score closes quality gates.

Target 10. Near-perfect Human Director bar 9.5. Known material gaps stay visible in the completion matrix.

## Successor law

Every execution ends with either:
- **TERMINAL:** declared application scope is closed with evidence; or
- **SUCCESSOR-READY:** the matrix shows exactly what is complete, what remains, why, and the next failing gate.

The next Naya resumes from the first failing gate without asking the Human Director to rediscover ordinary missing work.

## Final command

**Never hand the Human Director a porch and call it a house. Finish the declared product, protect what is already excellent, and make every iteration leave less burden and more capability behind.**

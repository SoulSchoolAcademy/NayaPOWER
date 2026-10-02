# NayaNET Hub Chassis + Canonical Room Socket - Implementation Receipt V1

**Status:** IMPLEMENTED + LOCAL BROWSER-VERIFIED; NOT MERGED; NOT DEPLOYED; NOT PRODUCTION-PROVEN; NOT INDEPENDENTLY VERIFIED
**Human Director:** Shawn Vibert
**Execution branch parent:** `naya4/room-01-main-stage-v2@babae0b42009dbae847b21dcc1de5e56922d1964`
**Canonical main restored before implementation:** `10190133505f4ba03cd029d18cf6f650affeeb9c`
**Main/app merge base:** `a67fc180306c3ebf616c8d02c0e0c11570276ce4`
**Current main repin before evidence close:** `d9e6b32fa097a9abd026523652a5e423a7e08d06` - only canonical Brain-index repair files changed since the implementation-start pin; no HUB files changed.

## Objective

Establish one machine-readable room contract and one shared room socket inside the existing Hub production-app lane, without creating another Hub, shell, runtime, authority model, intelligence store, or receipt system.

The Hub remains a projection over governed NayaPOWER intelligence.

## What changed

1. Added `HUB/app/js/room-contract.js`.
2. Removed the duplicate hard-coded room registry from `runtime.js`; runtime navigation identity now derives from the room contract.
3. Added `HUB/app/js/room-socket.js` as the single UI projection seam.
4. Routed shared room loads through `roomSocket.query(...)`.
5. Routed Library search through `roomSocket.search(...)`.
6. Routed Feed/Main Show query, search, canonical retrieval, and governed action through the same socket.
7. Bound Hub room lifecycle to `roomSocket.enter(...)`.
8. Exposed read-only contract/socket introspection through `window.NayaHub`.
9. Added browser assertions proving the contract, socket, eleven-room registry, Feed lifecycle, canonical/app route distinction, and Feed query path exist on rendered bytes.
## Canonical contract fields

Every room contract exposes identity, route, human purpose/question, canonical object types, source of truth, dependencies, allowed actions, authority, primary query, universal state model, evidence/provenance, contextual Naya, semantic color, composition, responsive behavior, accessibility, continuity, and proof.

The contract records current-main machine-room metadata from `HUB/NAYANET-SMART-APP-ROOMS-V1.json@1.0.2`.

The implementation deliberately records both `canonical_route` (for example `/feed`) and `app_route` (for example `/hub/feed`). That distinction is evidence, not a silent reconciliation.

## Reference room

**Feed / current Main Show implementation** is the reference room for this rung because it currently has the strongest complete UI causal path:

governed room query -> canonical object projection -> Ask Naya/search -> canonical retrieval/evidence -> governed action -> returned consequence/receipt state -> return continuity.

This is a reference implementation only. It does not resolve whether Feed is canonically identical to Hub Home.

## Local proof

- `git diff --check` - PASS.
- JavaScript syntax checks for every modified/new app JS file - PASS (`SYNTAX_OK`).
- `python tools/verify_hub_app_completion.py` - PASS: matrix consistent; 11 rooms; 0 production-proven; overall IN_PROGRESS.
- `node HUB/app/tests/browser-smoke.mjs` against local exact working bytes - PASS, exit code 0.
- Browser smoke includes desktop/mobile rendering plus the new room-contract/socket assertions.
- PR #1338 Hub App Completion Gate run `37037730392` - SUCCESS.
- PR #1338 Collective Chain Readiness run `37037730371` - SUCCESS.
- Remote browser artifact `hub-browser-qa` id `11240443104`, digest `sha256:f1a0f6cb8f234bbd3e3ed356656631d59291ea35ee7d874c254f15181cc55af2`.
- Kernel Tests run `37037730493` - BLOCKED only at stale-parent Brain-index check; Node and pytest steps PASS. Current main `d9e6b32...` already contains the canonical index repair, so this is inherited branch divergence rather than Hub-socket failure.
## Truth boundary

This work proves the shared UI seam exists and renders/behaves under the browser fixture/runtime harness.

It does **not** prove the live production NayaPOWER runtime artery, production deployment/source parity, all room backend capabilities, independent verification, Human Director approval, or final design-law ratification.

## Material authority conflict preserved

Current canonical `main` and the active application lane do not currently agree on all shell/Home semantics.

Current-main machine/living contracts specify a distinct Intelligent Hub Home/Main Show at `/hub`, Smart Feed as a separate room at `/feed`, and shell components including LEFT_RAIL, TOP_CONTEXT_BAR, GLOBAL_SEARCH, MAIN_WORKSPACE, NAYA_PRESENCE.

The active Main Show branch currently implements Feed as the Main Show/home behavior at `/hub/feed`, with two corner controls plus two drawers and Feed omitted from the room drawer.

PR #1331 remains candidate/open, not silently ratified. Therefore this rung does not change shell/Home semantics. The socket is intentionally shell-neutral, and canonical/app route differences stay explicit until authority is reconciled.

## Regression posture

Existing Hub visual/interaction behavior was preserved. No second runtime or store was added. The socket delegates to the existing `runtime-live.js` boundary and stores only bounded UI lifecycle trace, not intelligence truth.

## Exact next action

Reconcile the current-main Hub Home/shell authority with the active two-drawer Feed/Main Show implementation. Once that decision is canonical, close **Today** as the next reference consumer using the same canonical object identity/socket and prove Feed -> Today continuity without route/title guessing.

## Evidence law

DOCUMENTED != IMPLEMENTED
IMPLEMENTED != VERIFIED
VERIFIED != PRODUCTION-PROVEN
UNKNOWN != PASS
BLOCKED != PASS

# NAYA ACTION 002 — APPDEPLOY CANONICAL HUB FRESHNESS

**Date:** 2026-09-15  
**Action:** `NAYA-ACTION-002-APPDEPLOY-CANONICAL-HUB-FRESHNESS`  
**Status:** VERIFIED  
**Current main HEAD at execution:** `7dd17a81f5d2c58aa8e0fc37b2a92131b51c1df8`

## MISSION

Make Naya Power progressively better at carrying verified intelligence forward so the next Naya starts from truth rather than stale or inferred state.

## WHAT CHANGED

The AppDeploy NayaNET canonical Hub source mirror was pinned to the exact latest `main` commit instead of an older checkpoint.

Previous source reference:
`65e5578d24369da8975bfaf2741ad433295dad84`

New source reference:
`7dd17a81f5d2c58aa8e0fc37b2a92131b51c1df8`

The mirror retained its fail-closed canonical identity checks.

## APPDEPLOY EVIDENCE

- App: `nayanet-canonical-hub-source-mirror-tqp22y`
- URL: `https://nayanet-canonical-hub-source-mirror-tqp22y.v2.appdeploy.ai/`
- Snapshot: `1789509766843`
- Deployment status: `ready`
- Frontend errors: none reported
- Backend errors: none reported
- Deployed `src/main.ts` directly inspected and confirmed the new immutable GitHub commit reference.

## CANONICAL HUB INSPECTION

The actual current React Hub source contains the canonical `AppShellV3`, ten-item intelligence navigation, `SmartFeedBoard`, Primary Intelligence loading, and existing intelligence-object architecture.

This exposed an important architectural boundary: the AppDeploy application is currently a **static source mirror**, while the canonical repository also contains a richer React Hub implementation. These two surfaces must not be silently treated as equivalent.

## VERIFICATION BOUNDARY

**Verified:**

- current `main` HEAD resolved;
- canonical React Hub source inspected;
- AppDeploy source reference updated to current `main`;
- AppDeploy deployment reached READY;
- deployed source reference inspected directly.

**Not verified:**

- independent browser rendering of the public URL;
- desktop/mobile interaction;
- production equivalence;
- full React Hub deployment through this AppDeploy target.

A web fetch of the public AppDeploy URL failed at the retrieval layer with a cache-miss fetch error; that is not treated as evidence that the runtime is down.

## MACHINE-READABLE LESSON

> A runtime can be healthy and ready while serving stale project state. Runtime provenance must bind the deployed source reference to an exact current canonical commit before runtime claims are meaningful.

## SECONDARY ARCHITECTURAL LESSON

The static canonical HTML mirror and the canonical React Hub are distinct implementation surfaces. The next execution must reconcile the AppDeploy target with the actual React Hub rather than assuming that updating a static HTML reference completes the runtime migration.

## CURRENT STATE

The AppDeploy target is source-fresh relative to `main` for the static mirror, but it is **not yet proven to be the actual canonical React Hub runtime**.

## NEXT

Build the smallest complete AppDeploy React artifact that preserves the existing `AppShellV3`, `SmartFeedBoard`, Primary Intelligence, and canonical ten-item navigation; deploy it to the existing AppDeploy target; then verify desktop/mobile behavior and record exact runtime evidence.

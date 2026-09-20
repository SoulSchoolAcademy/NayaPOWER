# Durable Lesson — Production Parity + Measurement Boundaries

**Provenance event:** DI-20260919-CURRENT-HEAD-CLOUDFLARE-BROWSER-PROOF-001
**Date:** 2026-09-19 local / 2026-09-20 UTC
**Status:** VERIFIED → PROMOTED

## Canonical evidence

- Current main HEAD at proof dispatch: `bd5201e7252e744cea876beaf50f41b7bf541fef`.
- Cloudflare Hub release run: `35492451804` — SUCCESS.
- Canonical Worker: `sparkling-shape-7ae5`.
- Runtime parity: exact current-main source deployed and live artifact identity/source parity verified.
- Browser baseline: desktop + mobile PASS.
- Canonical React Hub: marker `NAYANET-HUB-REACT-CANONICAL`, authenticated name-first identity, canonical sidebar, Smart Feed rendered, private workspace verified.
- Smart Feed action matrix: favorite/save/like/love/rating/comments/share persisted and retrieved; unauthorized persistence blocked with `AUTH_REQUIRED`.
- Smart Note E2E on the same current main HEAD: run `35491124160`, `SMART_NOTE_E2E=PASS`, authoritative persistence/privacy/provenance/CIS/PIS/Intelligent Block/cold-Naya checks PASS.
- Smart Ledger integration: run `35460477460`, `SMART_FEED_LEDGER_INTEGRATION=VERIFIED`, with machine proof artifact uploaded.

## Distilled lesson

**Production claims are source-scoped claims, not repository-HEAD assumptions.** When claim-relevant Hub source changes, older deployment/browser evidence becomes stale or unknown until the exact current source is redeployed and re-observed.

**Measurement boundaries are part of correctness.** Browser proof must observe the actual state transition and retrieve the persisted identity/receipt; timing assumptions are not evidence.

## Durable home classification

**PROCEDURE + MACHINE CONTRACT / TEST**

This lesson is reusable across every Hub surface and should be enforced by release/parity and browser-acceptance gates rather than treated as a one-off note.

## Promotion decision

**PROMOTED** to durable intelligence. No governance or authority mutation was performed.

## Successor instruction

For every new Hub vertical transaction:

**HUMAN ACTION → AUTHORITY → CANONICAL RUNTIME → PERSISTENCE → RECEIPT → EXACT RETRIEVAL → OBSERVATION → VERIFICATION**

Never inherit production proof from an older deployment when claim-relevant source scope has changed.

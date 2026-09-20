# E06 Maxis Fidelity Learning

**Date:** 2026-08-19
**Category:** LEARNING / PROBLEM / SOLUTION
**Keywords:** E06, Naya Supercharger, Maxis, MAXESS, component fidelity, actual components, icon system, board system, source audit, rendered verification, visual fidelity, source of truth
**Aliases:** MaxIS fidelity, Maxis-native, reuse approved components, do not imitate Maxis, source fidelity

## Context
E06 Naya Supercharger was being rebuilt after a material failure: the candidate visually approximated Maxis/Human Maximus components instead of proving direct reuse of the approved component/code source.

## Durable Lesson
When an approved product component exists, reuse the approved component instead of recreating an approximation. Source fidelity is part of visual correctness.

For E06 specifically, the execution must distinguish between:
- using the established HMC/MAXESS visual language;
- reusing an existing approved implementation from E01/E02;
- and directly reusing the exact Maxis component/code supplied by the product source.

These are not equivalent claims.

## Evidence
- `docs/HMC-MAXIMUS-BUTTON-AND-ICON-SYSTEM.md` defines the authoritative Human Maximus/MAXESS icon and control language and explicitly says approved button/icon families should be reused product-wide.
- `E01-SECTION-01-WORKING.html` contains the current proven Orb + Orbital Bead implementation.
- The active E06 artifact was rebuilt on 2026-08-19 under commit `ac274678c1debd152c060545abf293b37836cab4`.
- The active repository asset directory currently documents canonical Naya source URLs but does not contain binary Naya image files.
- The exact supplied Maxis component source requested for literal reuse was not independently locatable in the active repository during this execution. Therefore exact Maxis-component fidelity remains a verification item, not a claim.

## Required Behavior
1. Audit the repository before every E06 visual rebuild.
2. Locate and evidence-map the exact approved Maxis source before claiming direct reuse.
3. If the exact source is unavailable, explicitly mark it UNKNOWN/BLOCKED rather than silently recreating it and calling it reused.
4. Render the artifact before scoring visual quality.
5. Ask: WHY IS THIS NOT A 10?
6. Repair root causes, then re-render and re-score.

## Why It Matters
A premium product feels like one intelligent system. Recreated approximations can look plausible in source while still feeling wrong in the rendered experience. The visitor's perception of continuity, quality, and trust depends on actual component fidelity.

## Related Paths
- `E06-SECTION-06-WORKING.html`
- `docs/MAXESS-E06-NAYA-SUPERCHARGER-ULTIMATE-EXECUTION-PROMPT.md`
- `docs/E06-NAYA-SUPERCHARGER-CONTENT-SPEC.md`
- `docs/HMC-MAXIMUS-BUTTON-AND-ICON-SYSTEM.md`
- `E01-SECTION-01-WORKING.html`
- `E02-SECTION-02-WORKING.html`
- `docs/MAXESS-COMPONENT-OWNERSHIP-REGISTRY.md`

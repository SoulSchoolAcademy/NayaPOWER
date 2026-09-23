# E02 NayaNET 10 → Canonical NAYANET/HUB Reconciliation

**Date:** 2026-09-10
**Status:** RECONCILED AT ARCHITECTURAL SOURCE BOUNDARY; BEHAVIORAL PROOF IN PROGRESS

## 1. Authority decision

`NAYANET/HUB/` is the only current production source authority for the NayaNET Intelligent Hub.

The registered production workflow is `.github/workflows/deploy-nayanet-hub-canonical-v2.yml`, and it builds from `NAYANET/HUB`, deploys to `aged-art-7c12`, promotes the created Worker version to 100%, and independently verifies the public runtime.

No second E02 deployment path is permitted.

## 2. E02 source reconciliation finding

The current `SoulSchoolAcademy/NayaPOWER` main tree does not contain an `E02-INTELLIGENT-HUB-CLOUDFLARE/` source directory, and the connected GitHub repository search did not return an E02 source artifact. Therefore this reconciliation does **not** invent or copy a missing source tree.

The surviving E02/NayaNET-10 design intent already recorded in the repository is treated as a **reference contract**, not as a competing codebase.

## 3. Preserved E02 / NayaNET-10 design intent

The canonical React Hub must preserve and continue to improve these reference traits:

- 250px-class cockpit navigation and strong spatial hierarchy;
- white command/search surface;
- deep-grape Naya action treatment;
- dimensional/atmospheric depth;
- large readable hierarchy;
- tactile interactive states;
- responsive behavior;
- Smart Feed as the primary intelligence surface;
- Human / Child / Grandma / Naya / Machine perspectives;
- What We Learned / What It Means / What To Do;
- provenance, trust and verification;
- Favorite / Save / Create Space;
- contextual Ask Naya;
- Connect / related intelligence.

These requirements are already represented in the canonical Hub release contract and the current `AppShellV3`, `App.tsx`, Smart Feed, and v10/v11/v12 style layers.

## 4. What is explicitly rejected

- No parallel E02 deployment authority.
- No standalone HTML promoted over the React Hub.
- No legacy Superbrain/operator UI inside the user-facing Hub.
- No claim that visual equivalence is proven by source inspection alone.
- No claim that E02 runtime behavior is proven until the exact canonical runtime is independently observed.

## 5. Verification boundary

The production release gate remains:

`SOURCE SHA → BUILD ARTIFACT → CLOUDFLARE VERSION → 100% PROMOTION → PUBLIC RUNTIME → INDEPENDENT OBSERVATION`

The behavioral gate is separate:

`CURRENT MAIN → SUPERBRAIN SUITE → A→B→C COMPOUNDING → BEHAVIORAL RECEIPT`

## 6. Current conclusion

**Source authority:** NAYANET/HUB — RECONCILED.

**E02 as independent production source:** NOT PRESENT IN CURRENT MAIN — therefore no competing authority is created.

**E02 design intent:** retained as a reference contract and mapped into the canonical Hub.

**Visual proof:** still requires human/browser acceptance against the exact public runtime.

**Behavioral Superbrain proof:** triggered from current main; final CI result must be observed before promotion from TESTED to VERIFIED.

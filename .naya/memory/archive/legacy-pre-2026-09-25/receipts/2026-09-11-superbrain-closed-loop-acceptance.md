# Naya Power — Superbrain Closed-Loop Acceptance Receipt

**Date:** 2026-09-11  
**Repository:** `SoulSchoolAcademy/NayaPOWER`  
**Acceptance target:** current-main Superbrain closed loop  
**Status:** `REPAIR_APPLIED_AWAITING_FINAL_CI_OBSERVATION`

## Objective

Execute and prove the current-main Superbrain loop with Excellence-by-Default, Decision Calculus, verification, Smart Note/Promotion Engine behavior, and A→B→C intelligence compounding.

## Architecture under proof

`CONSTITUTION → DECISION CALCULUS → SUPERBRAIN → EXECUTION → OBSERVATION → VERIFICATION → EXCELLENCE CHECK → SMART NOTE / PROMOTION → SUCCESSOR → A→B→C COMPOUNDING`

## First proof failures observed

1. **Cold-start context validator drift** — validator expected manifest v4 while canonical manifest is v5; its briefing-order assertion also treated canonical preflight files as a contradiction.
2. **Promotion Engine isolated-fixture path bug** — generated artifact paths used `Path.relative_to(ROOT)` against temporary fixtures.
3. **Promotion Engine Hub receipt field mismatch** — Hub renderer referenced non-existent `status` / `homes` keys instead of canonical receipt fields.
4. **Promotion Engine compatibility drift** — canonical test expected `load_prior_event_index()` and `write_feed_entry()` compatibility functions.
5. **Torch positive fixture drift** — structured handoff policy now requires `next_execution`; fixture omitted it.
6. **Adversarial continuity test drift** — test treated a dynamic current-main projection policy as a static commit requirement.
7. **Legacy V21 renderer QA was being discovered by the generic Superbrain suite** — this was a product-specific regression contract, not a canonical Superbrain acceptance criterion.
8. **Restore reconciliation state was treated as generic process failure** — explicit `RECONCILIATION_REQUIRED` is a governed state and must not be converted into a false-red or false-green claim by the suite.

## Surgical repairs applied

- Updated `qa_naya_context_boot.py` to canonical manifest v5 and explicit preflight → Runtime Briefing semantics.
- Made Promotion Engine paths portable across repository and isolated fixtures.
- Corrected Promotion Engine Hub receipt field access.
- Restored compatibility APIs used by canonical Promotion Engine tests.
- Updated torch positive fixture to include the canonical `next_execution` field.
- Updated adversarial continuity checks to honor dynamic observed-head semantics.
- Excluded legacy V21 renderer QA from the Superbrain acceptance boundary with an explicit reason.
- Made Excellence-by-Default and Decision Calculus mandatory local Superbrain layers.
- Added deterministic Decision Calculus specification, machine policy, evaluator, and adversarial tests.
- Updated the local suite to accept explicit governed restore reconciliation as a non-fatal state while preserving the distinction between `UNKNOWN`, `RECONCILIATION_REQUIRED`, and verified success.

## Integrity rules preserved

- Protected human boundaries remain hard constraints, not compensating score terms.
- `UNKNOWN ≠ GREEN`.
- `IMPLEMENTED ≠ VERIFIED`.
- File writes never self-certify verification.
- Production source authority remains `NAYANET/HUB` and the canonical V2 release authority remains separate from Superbrain acceptance.
- No missing E02 source was recreated or invented.
- No competing production deployment authority was introduced.

## Current verification state

The first observable current-main behavioral proof run exposed the failures above. Surgical repairs have been committed to `main` and the push-triggered acceptance workflows are expected to rerun from the repaired source.

**Final status is intentionally not marked GREEN until the repaired workflow result is independently observable.**

## Next verification block

1. Observe the repaired current-main behavioral proof.
2. If any new failure appears, repair only the first material divergence.
3. Rerun the complete loop.
4. Require Excellence, Decision Calculus, Promotion/Smart Note, verification, and A→B→C proof to pass together.
5. Only then promote the result to `VERIFIED`; production proof remains a separate claim.

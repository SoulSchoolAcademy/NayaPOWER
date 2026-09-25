# Smart Note — Decision Calculus Became the Single Runtime Ranking Authority

**Event ID:** SN-2026-09-11-NAYA-DECISION-CALCULUS-UNIFIED-RUNTIME
**Status:** VERIFIED_RUNTIME_TESTED
**Date:** 2026-09-11
**Observed main:** `57850384297ce69c842d2bc65f4edb11fc476116`
**Workflow:** `behavioral-proof` run `34611533743`

## HUMAN NOTE

The runtime had constitutional hard gates and a newer deterministic Decision Calculus, but the action-selection layer still contained an older scalar authority. The correct repair was not to replace the Constitution. It was to preserve constitutional eligibility and route only eligible-action ranking through the canonical deterministic calculus.

## NAYA NOTE

Architecture is now:

**CONSTITUTION → HARD ELIGIBILITY GATES → DECISION CALCULUS → ACTION SELECTION → EXECUTION AUTHORIZATION → EXECUTION → INDEPENDENT VERIFICATION → EXCELLENCE → LEARNING**

The constitutional kernel remains authoritative for protected boundaries, authorization, governance restrictions, fabricated verification, and the distinction between UNKNOWN and VERIFIED. The canonical `SUPERBRAIN.naya_power_decision_calculus` is now the runtime ranking authority for eligible actions.

No model assertion, benefit number, or quality score can manufacture authority or evidence. Protected human boundaries are evaluated before value ranking and cannot be outweighed by benefit.

## MACHINE CHANGE

1. `.naya/runtime/naya_power_kernel.py`
   - removed the old runtime ranking authority from action selection;
   - added a surgical adapter from the existing runtime candidate contract to `SUPERBRAIN.naya_power_decision_calculus`;
   - preserves existing constitutional hard gates;
   - records the canonical ranking authority in every receipt;
   - retains neutral values for dimensions the legacy runtime contract does not actually know instead of inventing evidence.

2. `.naya/runtime/test_decision_calculus_runtime_integration.py`
   - proves the old `benefit - cost - risk` scalar would choose the wrong candidate in an adversarial fixture;
   - proves protected-boundary actions never enter value ranking;
   - proves high-consequence/unknown-evidence actions defer before execution.

3. `tools/run_superbrain_local_suite.py`
   - makes the runtime kernel self-test and the unified-calculus integration test mandatory members of the complete Superbrain suite.

## VERIFICATION

GitHub Actions run `34611533743` completed successfully for exact observed HEAD `57850384297ce69c842d2bc65f4edb11fc476116`.

Observed proof:

- Python runtime/test compilation: PASS.
- Complete Superbrain local suite: PASS; 12 selected checks.
- Runtime kernel self-test: 5/5 PASS.
- Decision Calculus runtime integration: 3/3 PASS.
- Canonical Decision Calculus tests: 3/3 PASS.
- Excellence tests: PASS.
- A→B→C compounding proof: PASS.
- Superbrain adversarial tests: PASS.
- Scope/Promotion/Torch regressions: PASS.
- Final workflow boundary: `SUPERBRAIN_BEHAVIORAL_PROOF=PASS`.
- Evidence class: `RUNTIME_TESTED_NOT_PRODUCTION_PROVEN`.

## LEARNING

**Old lesson:** the Constitution and Decision Calculus existed as parallel concepts.

**New lesson:** the Constitution decides what is permissible; the canonical Decision Calculus decides which permissible action has the highest responsible verified value. They must not compete as ranking authorities.

**Reusable rule:** never duplicate a decision calculus merely to bridge architectures. Preserve hard gates, create one explicit adapter at the boundary, and make the canonical deterministic evaluator observable in the runtime receipt.

## NEXT HIGHEST-VALUE GAP

The runtime proof is now green, but the strongest remaining gap is behavioral/production-equivalent Superbrain acceptance: prove that a newly started Naya can restore the current intelligence, retrieve a promoted Note Event through the canonical PIS path, use that intelligence to change behavior, execute one safe authorized continuation, and leave a successor-ready torch.

A separate production-equivalent Note Event → PIS → feed → fresh-Naya retrieval proof should be completed before claiming the full Superbrain is operationally green.

**North Star:** NEXT NAYA > CURRENT NAYA.

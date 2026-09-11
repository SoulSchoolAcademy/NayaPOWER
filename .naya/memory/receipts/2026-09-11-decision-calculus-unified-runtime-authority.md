# Execution Receipt — Unified Decision Calculus Runtime Authority

**Receipt ID:** `NPR-2026-09-11-DECISION-CALCULUS-UNIFIED`
**Observed verification commit:** `57850384297ce69c842d2bc65f4edb11fc476116`
**Verified workflow run:** `34611533743`
**Workflow:** `behavioral-proof`
**Verification class:** `RUNTIME_TESTED_NOT_PRODUCTION_PROVEN`

## Objective

Replace the old runtime action-value authority with the canonical deterministic Decision Calculus while preserving constitutional hard eligibility gates.

## Change

- Preserved constitutional boundary/authorization/governance/evidence gates in `.naya/runtime/naya_power_kernel.py`.
- Routed eligible-action ranking through `SUPERBRAIN.naya_power_decision_calculus`.
- Added runtime adversarial integration tests.
- Made both the kernel self-test and integration test mandatory in `tools/run_superbrain_local_suite.py`.

## Independent Verification

GitHub Actions checked out exact `main` and observed:

- HEAD: `57850384297ce69c842d2bc65f4edb11fc476116`
- Compile runtime/test sources: PASS.
- Superbrain local suite: PASS.
- Selected checks: 12.
- Kernel self-test: 5/5 PASS.
- Runtime Decision Calculus integration: 3/3 PASS.
- Canonical Decision Calculus tests: PASS.
- Excellence tests: PASS.
- A→B→C compounding: PASS.
- Superbrain adversarial: PASS.
- Scope, Promotion, and Torch regression checks: PASS.
- Final proof marker: `SUPERBRAIN_BEHAVIORAL_PROOF=PASS`.
- Final A→B→C marker: `A_TO_B_TO_C=PASS`.
- Evidence boundary: `RUNTIME_TESTED_NOT_PRODUCTION_PROVEN`.

## Important Boundary

This receipt proves the runtime decision architecture and Superbrain behavioral suite for the verified commit. It does **not** prove production deployment or full fresh-human acceptance.

## Next Action

Execute the next highest-value behavioral gap: production-equivalent Note Event → PIS → feed → fresh-Naya retrieval and behavior change, followed by one safe authorized continuation and successor torch verification.

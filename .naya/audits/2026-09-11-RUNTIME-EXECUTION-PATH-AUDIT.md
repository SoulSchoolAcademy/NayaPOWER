# NayaPOWER Runtime Execution-Path Audit

Date: 2026-09-11

## Mission

Build and verify NayaPOWER as the model-agnostic constitutional governance layer governing the relationship between human authority, machine intelligence, and consequential action.

## Current audit checkpoint

Source of truth: GitHub `SoulSchoolAcademy/NayaPOWER` `main`

Current audited HEAD: `8d095e3c0e9c836eb16f9781b8c9e561c743f3da`

Runtime execution status: UNVERIFIED

Foundation status: UNVERIFIED

This audit is source-level evidence only. It does not establish runtime success, CI success, production truth, or Foundation GREEN.

## Canonical runtime boundary

`AUTHORITY REGISTRY -> GOVERNANCE CONTRACT -> ACTION ELIGIBILITY -> VALUE RANKING -> ACTION PLAN -> AUTHORIZED HOST EXECUTION -> OBSERVATION -> VERIFICATION -> SCORECARD / OSCAR -> CONTINUATION`

## Findings

### 1. Canonical Naya runtime selection

`ActionCandidate.eligible()` delegates governed eligibility to `evaluate_governance(...)`; `rank_candidates(...)` and `choose_next_action(...)` use that governed path. The Authority Registry is required and scope is checked against the registered authority.

**Result:** No source-level bypass observed in the canonical Naya runtime selection path.

### 2. Host Executor

`HostExecutorBridge` remains an execution boundary and does not create an alternate authority hierarchy.

**Result:** No alternate authority source observed inside Host Executor.

### 3. Runtime call-site coverage

Known runtime constructor/call-site searches remain incomplete because the available GitHub code-search interface does not reliably index known symbols.

**Result:** Exhaustive repository-wide runtime call-site coverage remains UNKNOWN.

### 4. Authority scope

The current deterministic comma/semicolon token scope model remains unchanged. No evidence currently demonstrates a false authorization, collision, ambiguity, or bypass requiring a redesign.

**Decision:** Preserve current scope semantics pending concrete evidence.

### 5. Human-authorized deployment boundary

`.github/workflows/authorized-vercel-release.yml` remains a separate explicit human-authorized publication control plane with exact commit binding, verification, project binding, approval, and default-deny release authorization.

**Classification:** Deliberate separate control plane, not an observed Naya action-selection bypass.

### 6. Active workflow inventory and side-effect sweep

The current `.github/workflows/` directory was inspected at the audited main lineage. The active workflow set includes:

- `deployment-governance.yml`
- `naya-power-runtime-tests.yml`
- `torch-pass-gate.yml`
- `authorized-vercel-release.yml`
- `apply-maxess-result-bridge.yml`
- `build-integrated-results.yml`
- `build-aiscore-app-bridge.yml`
- `2026-09-08-10-05-apply-nayanet-hub-surgical-patch.yml`

The following historical workflows are explicitly retired and are read-only/manual-only:

- `2026-09-08-canonical-hub-release-dispatch.yml`
- `2026-09-08-nuclear-right-rail-fix.yml`
- `2026-09-08-repair-main-feed-and-strip-garbage.yml`
- `2026-09-08-surgical-right-rail-removal.yml`

The retired workflows have `workflow_dispatch` only, `contents: read`, and no mutation or deployment command.

The read-only automated gates (`deployment-governance.yml`, `naya-power-runtime-tests.yml`, `torch-pass-gate.yml`) have no repository write permission and no deployment mutation boundary.

The authorized Vercel workflow is the deliberate human-authorized deployment control plane.

### 7. Repository-mutation bypasses previously found

Three automatic repository-mutation workflows were previously identified and surgically closed:

- `.github/workflows/apply-maxess-result-bridge.yml`
- `.github/workflows/build-integrated-results.yml`
- `.github/workflows/build-aiscore-app-bridge.yml`

Each now requires `workflow_dispatch`, explicit `approval`, and `EXPLICIT_APPROVAL_GRANTED` before mutation/push.

### 8. New repository-mutation bypass found during exhaustive workflow sweep

`.github/workflows/2026-09-08-10-05-apply-nayanet-hub-surgical-patch.yml` was found to have:

- automatic `push` trigger on `main`
- `contents: write`
- invocation of `scripts/2026-09-08-10-05-NAYANET-HUB-RIGHT-SIDEBAR-AND-FEED-SURGICAL-PATCH.py`
- source-file mutation of `2026 09 08 9:59 NAYANET HUB`
- `git commit`
- `git push`

The invoked script was inspected and confirmed to perform a real source mutation by reading the target HTML, injecting the CSS/JavaScript patch when the marker is absent, and writing the target file back.

This is a genuine consequential automation boundary outside the canonical Naya governance runtime.

### 9. Surgical repair of NayaNET Hub mutation bypass

The workflow was changed to:

- `workflow_dispatch` only
- explicit `approval` input
- `EXPLICIT_APPROVAL_GRANTED` job gate
- unchanged surgical patch script and verification behavior
- guarded commit/push behavior preserved

The deployment governance regression suite was extended to include this workflow and assert that it, along with the three previously repaired repository-mutating bridge workflows, remains manual-only and explicitly approved.

**Result:** The fourth observed automatic repository-mutation bypass is closed at its trigger boundary at source level.

## Boundary classifications

| Boundary | Classification | Evidence-based disposition |
|---|---|---|
| Canonical Naya runtime | GOVERNED RUNTIME | Registry + Governance Contract + eligibility path |
| Authorized Vercel release | HUMAN-AUTHORIZED CONTROL PLANE | Exact SHA + approval + verification + default deny |
| Deployment governance | READ-ONLY / NON-CONSEQUENTIAL | Read permissions; governance tests only |
| Runtime tests | READ-ONLY / NON-CONSEQUENTIAL | No write/deployment capability |
| Torch-Pass | READ-ONLY / NON-CONSEQUENTIAL | Read permissions; continuity verification + receipt artifact |
| Three bridge mutation workflows | HUMAN-AUTHORIZED CONTROL PLANE | Manual dispatch + explicit approval |
| NayaNET Hub surgical patch | HUMAN-AUTHORIZED CONTROL PLANE | Repaired to manual dispatch + explicit approval |
| Four legacy 2026-09-08 workflows | RETIRED | Manual-only, read-only, no mutation/deployment capability |

## Protected decisions

- Preserve fail-closed Registry behavior.
- Do not restore `registry=None` as a permissive path.
- Do not create a second authority hierarchy.
- Capability != Authority.
- Invalid != Zero Value.
- Do not redesign Registry scope without evidence.
- Do not permit automatic repository mutation merely because it is deterministic.
- Do not infer runtime verification from source inspection.
- Do not manufacture Actions triggers.
- Do not modify read-only or retired workflows merely because they exist.

## Verification boundary

Still UNKNOWN:

- runtime unit-test execution
- governance negative-test execution
- deployment governance test execution
- Torch-Pass execution
- continuity validator execution
- receipt generation
- artifact upload
- exact-head production/runtime parity
- Foundation GREEN

The available commit-associated workflow-run interface does not provide sufficient exact-head execution evidence, and no workflow dispatch operation is available through the current connector surface.

## Current exact-head evidence

Main was re-resolved after the NayaNET Hub workflow repair and regression-test update.

Current exact HEAD: `8d095e3c0e9c836eb16f9781b8c9e561c743f3da`.

The repaired NayaNET Hub mutation workflow and expanded regression test are on `main`.

## Next highest-value action

1. Re-resolve `main` and confirm the exact SHA after the latest audit commit if one is added.
2. Fetch the repaired NayaNET Hub workflow, runtime-test workflow, and Torch-Pass workflow at that exact SHA.
3. Check legitimate exact-head workflow/status interfaces.
4. Confirm the full active-workflow side-effect sweep remains clean at the resulting SHA.
5. If genuine runtime evidence appears, inspect the complete execution and identify FIRST TRUE FAILURE from actual evidence.
6. Continue from the first real failure only; do not manufacture execution evidence.

## Audit verdict

**CANONICAL NAYA RUNTIME GOVERNANCE PATH: NO OBSERVED BYPASS**

**AUTOMATIC REPOSITORY-MUTATION BYPASSES: 4 FOUND; 4 SURGICALLY CLOSED AT SOURCE LEVEL**

**DEPLOYMENT CONTROL PLANE: EXPLICIT HUMAN AUTHORIZATION / DEFAULT DENY**

**ACTIVE WORKFLOW SIDE-EFFECT SWEEP: SOURCE-LEVEL COVERAGE COMPLETED FOR CURRENT INVENTORY**

**EXHAUSTIVE RUNTIME CALL-SITE COVERAGE: UNKNOWN**

**RUNTIME EXECUTION: UNVERIFIED**

**FOUNDATION: UNVERIFIED**

**FIRST TRUE FAILURE: UNKNOWN**

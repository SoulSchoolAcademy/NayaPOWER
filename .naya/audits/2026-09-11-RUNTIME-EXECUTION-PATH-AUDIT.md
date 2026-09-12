# NayaPOWER Runtime Execution-Path Audit

Date: 2026-09-11

## Mission

Build and verify NayaPOWER as the model-agnostic constitutional governance layer governing the relationship between human authority, machine intelligence, and consequential action.

## Current audit checkpoint

Source of truth: GitHub `SoulSchoolAcademy/NayaPOWER` `main`

Current audited HEAD: `21dd0cf81f21bc737e4fd74854db8e9cb8141280`

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

### 6. Repository-mutation bypasses previously found

Two automatic repository-mutation workflows were surgically closed:

- `.github/workflows/apply-maxess-result-bridge.yml`
- `.github/workflows/build-integrated-results.yml`

Both now require `workflow_dispatch`, explicit `approval`, and `EXPLICIT_APPROVAL_GRANTED` before mutation/push.

### 7. New repository-mutation bypass found at this checkpoint

`.github/workflows/build-aiscore-app-bridge.yml` was found to have:

- automatic `push` trigger
- `contents: write`
- source mutation of `AIScoreMAXESS code`
- commit and `git push`

This was a genuine consequential automation boundary outside the canonical Naya governance runtime.

### 8. Surgical repair of AIScore bypass

The workflow was changed to:

- `workflow_dispatch` only
- explicit `approval` input
- `EXPLICIT_APPROVAL_GRANTED` job gate
- explicit branch checkout
- unchanged deterministic bridge build behavior
- guarded commit/push behavior

The deployment governance regression suite was extended to include `build-aiscore-app-bridge.yml` and assert that all three repository-mutating bridge workflows remain manual-only and explicitly approved.

**Result:** The newly observed automatic AIScore repository-mutation bypass is closed at its trigger boundary at source level.

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

`main` was re-resolved after the AIScore workflow repair and regression-test update.

Current exact HEAD: `21dd0cf81f21bc737e4fd74854db8e9cb8141280`.

The repaired AIScore workflow and expanded regression test are on `main`.

## Next highest-value action

1. Re-resolve `main`.
2. Fetch runtime-test and Torch-Pass workflows at the exact resulting HEAD.
3. Inspect every remaining active workflow with write permissions, deployment commands, external side effects, workflow chaining, or automatic event triggers.
4. Inspect executable scripts invoked by those workflows for consequential mutation/execution.
5. Classify each boundary as governed, deliberately human-authorized, retired, or concrete bypass.
6. Repair only concrete bypasses.
7. Add deterministic regression coverage for every repaired bypass.
8. Re-resolve `main`.
9. Check all legitimate exact-head workflow/status interfaces.
10. If genuine runtime evidence appears, inspect the complete execution and identify FIRST TRUE FAILURE from actual evidence.

## Audit verdict

**CANONICAL NAYA RUNTIME GOVERNANCE PATH: NO OBSERVED BYPASS**

**AUTOMATIC REPOSITORY-MUTATION BYPASSES: 3 FOUND; 3 SURGICALLY CLOSED AT SOURCE LEVEL**

**DEPLOYMENT CONTROL PLANE: EXPLICIT HUMAN AUTHORIZATION / DEFAULT DENY**

**EXHAUSTIVE ACTIVE-WORKFLOW / CALL-SITE COVERAGE: UNKNOWN**

**RUNTIME EXECUTION: UNVERIFIED**

**FOUNDATION: UNVERIFIED**

**FIRST TRUE FAILURE: UNKNOWN**

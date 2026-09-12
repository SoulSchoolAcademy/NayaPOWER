# NayaPOWER Runtime Execution-Path Audit

Date: 2026-09-11

## Mission

Build and verify NayaPOWER as the model-agnostic constitutional governance layer governing the relationship between human authority, machine intelligence, and consequential action.

## Audit baseline

Source of truth: GitHub `SoulSchoolAcademy/NayaPOWER` `main`

Audit starting HEAD: `adf9953ac7ad448fa9b5d0245bf0829e419c5b06`

Runtime execution status: UNVERIFIED

Foundation status: UNVERIFIED

This audit is source-level evidence only. It does not establish runtime success, CI success, production truth, or Foundation GREEN.

## Scope inspected

The canonical runtime boundary identified in the current source state is:

`AUTHORITY REGISTRY -> GOVERNANCE CONTRACT -> ACTION ELIGIBILITY -> VALUE RANKING -> ACTION PLAN -> AUTHORIZED HOST EXECUTION -> OBSERVATION -> VERIFICATION -> SCORECARD / OSCAR -> CONTINUATION`

Relevant runtime and control-plane components inspected:

- `SUPERBRAIN/runtime/naya_power_runtime.py`
- `SUPERBRAIN/runtime/mission_state_store.py`
- `SUPERBRAIN/runtime/governance_contract.py`
- `SUPERBRAIN/runtime/host_executor.py`
- `SUPERBRAIN/runtime/quality_gate.py`
- `SUPERBRAIN/runtime/continuation_prompt.py`
- runtime unit-test modules
- `.github/workflows/naya-power-runtime-tests.yml`
- `.github/workflows/torch-pass-gate.yml`
- `.github/workflows/authorized-vercel-release.yml`
- `.github/workflows/apply-maxess-result-bridge.yml`
- `.github/workflows/build-integrated-results.yml`
- `.naya/runtime/release_authorization.py`
- `.naya/runtime/deployment_governance_test.py`
- `.naya/control-plane/DEPLOYMENT-GOVERNANCE.json`
- `.naya/governance/NAYA-AUTHORITY-REGISTRY-V1.json`

## Findings

### 1. Canonical runtime action selection reaches the governance contract

`ActionCandidate.eligible()` delegates governed eligibility to `evaluate_governance(...)` and then preserves the existing dependency/protected-scope/authorization gates.

`rank_candidates(...)` only ranks candidates that pass eligibility.

`choose_next_action(...)` uses the same governed candidate-selection path.

**Result:** No source-level bypass was observed in the canonical Naya runtime selection path.

### 2. Canonical Authority Registry is required for governed selection

The governance contract fails closed when no Registry is supplied.

The contract also requires:

- authority identifier
- registered authority
- active authority
- requested scope matching the registered scope

`MissionStateStore` passes its configured Registry through `LeadModeEngine` into `choose_next_action(...)`.

**Result:** The previous Registry-omission permissive path is closed at the governance boundary.

### 3. Capability does not grant authority

Capability is evaluated independently from authority registration and constitutional eligibility.

A capable action with no registered authority remains ineligible.

**Result:** No capability-to-authority escalation was observed in the canonical runtime governance path.

### 4. Host Executor is not an alternate authority source

`HostExecutorBridge` consumes the selected plan and acts as an execution boundary. It does not create or replace the constitutional authority hierarchy.

The selection decision remains upstream in the governed Lead Mode path.

**Result:** No second authority source was observed inside Host Executor.

### 5. Direct production constructors / alternate runtime selection paths

Repository search for direct constructor/call-site patterns for `MissionStateStore`, `LeadModeEngine`, `choose_next_action`, and `HostExecutorBridge` returned no indexed results outside the already-known runtime/test surfaces.

This is useful negative evidence, but it is **not exhaustive repository proof** because the available GitHub code-search interface did not return indexed matches for these runtime symbols even where the known source files contain them.

Therefore:

**Exhaustive repository-wide runtime call-site coverage remains UNKNOWN.**

No architecture change is justified solely from the absence of search results.

### 6. Canonical Registry duplication

The governed runtime consumes the Authority Registry as a supplied canonical registry object and does not define a competing authority hierarchy in the Governance Contract.

**Result:** No second authority hierarchy was observed in the inspected Naya runtime boundary.

### 7. Scope model

The current scope model uses deterministic matching against registered scope strings, including comma/semicolon-delimited scope tokens.

No evidence was found proving that this representation is currently unsafe or ambiguous enough to justify a Registry redesign.

**Decision:** Preserve the current scope model pending concrete evidence of a false authorization, collision, ambiguity, or bypass.

### 8. Governance gates

The machine-checkable decision contract explicitly gates Registry presence, authority registration/status, scope, capability, constitutional eligibility, objective, consequence, reversibility, risk, evidence, verification, stopping, responsible-value eligibility, human-decision requirement, and explicit decision state.

The decision result includes deterministic per-gate checks.

Invalid, unauthorized, unsafe, unverifiable, or unjustified candidates are excluded rather than assigned a zero value and allowed to compete.

### 9. Deployment is a separate, explicitly human-authorized control-plane side effect

`.github/workflows/authorized-vercel-release.yml` is a consequential deployment boundary, but it is not an AI action-selection path. It is explicitly invoked and requires exact commit binding, target environment, canonical project binding, verification evidence, release reason, authorized actor, timestamp, and explicit approval. The deployment policy is default-deny.

`.naya/runtime/release_authorization.py` fails closed when those release conditions are not satisfied.

**Classification:** This is a distinct human-authorized publication boundary, not an observed bypass by Naya intelligence. It should remain separate from Host Executor unless constitutional evidence later requires unification.

### 10. Real repository-mutation bypasses were found outside the canonical runtime

Two active GitHub workflows were found to mutate repository source and push commits automatically from repository events:

1. `.github/workflows/apply-maxess-result-bridge.yml`
   - previously triggered from `push` to `main` and pull requests
   - had `contents: write`
   - executed a source mutation script
   - committed and pushed the resulting mutation

2. `.github/workflows/build-integrated-results.yml`
   - previously triggered from `push` to `main`
   - had `contents: write`
   - mutated the complete Results artifact
   - committed and pushed the resulting mutation

These were **real consequential automation paths outside the Naya governance contract**. They did not reach `ActionCandidate.eligible()`, the canonical Authority Registry, or Host Executor.

### 11. Surgical repair applied to the mutation bypasses

Both workflows were changed to:

- `workflow_dispatch` only
- explicit `approval` input
- `EXPLICIT_APPROVAL_GRANTED` required
- job-level approval gate
- retain their intended deterministic mutation behavior when explicitly invoked

The automatic `push` / pull-request mutation triggers were removed. No runtime governance was weakened.

A deterministic regression test was added to `.naya/runtime/deployment_governance_test.py` to enforce that these repository-mutating workflows remain manual-only and explicitly approved.

**Result:** The observed automatic repository-mutation bypasses are surgically closed at their trigger boundary.

## Architectural conclusion

The canonical Naya runtime action-selection path remains governed and fail-closed at the source level.

A separate human-authorized deployment control plane remains intentionally distinct.

Two additional repository-mutating automation paths were identified as consequential side-effect boundaries that bypassed the canonical governance runtime. They were repaired by removing automatic event triggers and requiring explicit workflow dispatch plus explicit approval.

This is a concrete source-level governance repair, not activity for activity's sake.

The principal remaining source-level uncertainty is **exhaustive repository call-site coverage** because the available GitHub code-search interface cannot reliably enumerate all symbol references.

## Protected decisions

- Preserve fail-closed Registry behavior.
- Do not restore `registry=None` as a permissive path.
- Do not create a second authority hierarchy inside the Naya runtime.
- Do not treat capability as authority.
- Do not treat invalid as zero-value.
- Do not redesign the Registry scope model without evidence.
- Do not permit automatic repository mutation merely because a workflow is deterministic.
- Do not infer runtime verification from source inspection.
- Do not manufacture Actions triggers.

## Verification boundary

The following remain UNKNOWN until genuine exact-head execution evidence exists:

- runtime unit-test execution
- governance negative-test execution
- Torch-Pass execution
- continuity validator execution
- receipt generation
- artifact upload
- exact-head production/runtime parity
- Foundation GREEN

## Current exact-head evidence

After the repairs, `main` resolved to `efb29876e1819d0002bb09ec87a85a45a00f8792` at the latest audit checkpoint.

The runtime and Torch-Pass workflow definitions were present at that exact commit.

The available commit-associated workflow-run interface returned no runs for that exact SHA because that interface currently filters to pull-request-triggered runs. This absence is not evidence that no push-triggered run exists.

Combined commit status exposed only a Vercel status, currently `pending`, and no canonical Torch-Pass status.

Therefore no runtime success or failure is claimed.

## Next highest-value action

1. Re-resolve `main` after the latest regression-test/audit changes.
2. Capture the exact current SHA.
3. Fetch the runtime-test and Torch-Pass workflow definitions at that exact SHA.
4. Check every legitimate exact-head workflow/status interface available.
5. If a genuine execution appears, inspect the complete run and identify the FIRST TRUE FAILURE from actual logs.
6. If no execution evidence appears, do not manufacture a trigger. Continue source-level inspection of remaining active workflows and runtime entry points for consequential mutation or execution boundaries.
7. Repair only concrete bypasses and add deterministic regression coverage.

## Audit verdict

**CANONICAL NAYA RUNTIME GOVERNANCE PATH: NO OBSERVED BYPASS**

**AUTOMATIC REPOSITORY-MUTATION BYPASSES: 2 FOUND AND SURGICALLY CLOSED**

**DEPLOYMENT CONTROL PLANE: EXPLICIT HUMAN AUTHORIZATION / DEFAULT DENY**

**EXHAUSTIVE CALL-SITE COVERAGE: UNKNOWN**

**RUNTIME EXECUTION: UNVERIFIED**

**FOUNDATION: UNVERIFIED**

**FIRST TRUE FAILURE: UNKNOWN**

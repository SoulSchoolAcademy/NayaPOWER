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

Relevant runtime components inspected/known from the current source state:

- `SUPERBRAIN/runtime/naya_power_runtime.py`
- `SUPERBRAIN/runtime/mission_state_store.py`
- `SUPERBRAIN/runtime/governance_contract.py`
- `SUPERBRAIN/runtime/host_executor.py`
- `SUPERBRAIN/runtime/quality_gate.py`
- `SUPERBRAIN/runtime/continuation_prompt.py`
- their runtime unit-test modules
- `.github/workflows/naya-power-runtime-tests.yml`
- `.github/workflows/torch-pass-gate.yml`
- `.naya/governance/NAYA-AUTHORITY-REGISTRY-V1.json`

## Findings

### 1. Action selection reaches the governance contract

`ActionCandidate.eligible()` delegates governed eligibility to `evaluate_governance(...)` and then preserves the existing dependency/protected-scope/authorization gates.

`rank_candidates(...)` only ranks candidates that pass eligibility.

`choose_next_action(...)` uses the same governed candidate-selection path.

**Result:** No source-level bypass was observed in the canonical selection path.

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

**Result:** No capability-to-authority escalation was observed in the canonical governance path.

### 4. Host Executor is not an alternate authority source

`HostExecutorBridge` consumes the selected plan and acts as an execution boundary. It does not create or replace the constitutional authority hierarchy.

The selection decision remains upstream in the governed Lead Mode path.

**Result:** No second authority source was observed in Host Executor.

### 5. Direct production constructors / alternate selection paths

Repository search for direct constructor/call-site patterns for `MissionStateStore`, `LeadModeEngine`, `choose_next_action`, and `HostExecutorBridge` returned no indexed results outside the already-known runtime/test surfaces.

This is useful negative evidence, but it is **not exhaustive repository proof** because the available GitHub code-search interface did not return indexed matches for these runtime symbols even where the known source files contain them.

Therefore:

**Exhaustive repository-wide call-site coverage remains UNKNOWN.**

No architecture change is justified solely from the absence of search results.

### 6. Canonical Registry duplication

The governed runtime consumes the Authority Registry as a supplied canonical registry object and does not define a competing authority hierarchy in the Governance Contract.

The Registry documentation now distinguishes source enforcement from runtime execution verification.

**Result:** No second authority hierarchy was observed in the inspected runtime boundary.

### 7. Scope model

The current scope model uses deterministic matching against registered scope strings, including comma/semicolon-delimited scope tokens.

No evidence was found in this source audit proving that this representation is currently unsafe or ambiguous enough to justify a Registry redesign.

A structured authority-domain model may ultimately be stronger, but introducing one without a demonstrated defect would violate Adaptive Reconstruction + Surgical Evolution.

**Decision:** Preserve the current scope model pending concrete evidence of a false authorization, collision, ambiguity, or bypass.

### 8. Governance gates

The current machine-checkable decision contract explicitly gates:

- Registry presence
- registered authority
- active authority
- scope match
- capability
- constitutional eligibility
- objective
- consequence
- reversibility
- risk
- evidence readiness
- verification requirement
- stopping condition
- responsible-value eligibility
- human-decision requirement
- explicit decision state

The decision result includes deterministic per-gate checks.

Invalid, unauthorized, unsafe, unverifiable, or unjustified candidates are excluded rather than assigned a zero value and allowed to compete.

## Architectural conclusion

No concrete consequential-action bypass was identified in the inspected canonical runtime path.

The principal remaining source-level uncertainty is not a demonstrated bypass; it is **exhaustive repository call-site coverage** because the available GitHub code-search interface cannot reliably enumerate all symbol references.

Accordingly, no runtime architecture was weakened or redesigned.

## Protected decisions

- Preserve fail-closed Registry behavior.
- Do not restore `registry=None` as a permissive path.
- Do not create a second authority hierarchy.
- Do not treat capability as authority.
- Do not treat invalid as zero-value.
- Do not redesign the Registry scope model without evidence.
- Do not infer runtime verification from source inspection.

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

Current known status evidence before this audit did not expose a canonical exact-head Torch-Pass result; combined status exposed Vercel success only.

## Next highest-value action

Re-resolve `main` after this audit commit, capture the exact new HEAD, and inspect every legitimate available exact-head workflow/status interface. If a genuine runtime execution appears, inspect the complete run and identify the first actual failure. If no execution evidence appears, do not manufacture a trigger; preserve UNKNOWN and continue the source-level audit by inspecting any newly discoverable runtime entry points/adapters/factories.

## Audit verdict

**SOURCE-LEVEL GOVERNANCE PATH: NO OBSERVED BYPASS**

**EXHAUSTIVE CALL-SITE COVERAGE: UNKNOWN**

**RUNTIME EXECUTION: UNVERIFIED**

**FOUNDATION: UNVERIFIED**

**FIRST TRUE FAILURE: UNKNOWN**

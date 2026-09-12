# NayaPOWER Runtime Execution-Path Audit

Date: 2026-09-11

## Mission

Build and verify NayaPOWER as the model-agnostic constitutional governance layer governing the relationship between human authority, machine intelligence, and consequential action.

## Current audit checkpoint

Source of truth: GitHub `SoulSchoolAcademy/NayaPOWER` `main`

Current audited HEAD: `eb5aa407abe9ea730bd02383d6961da7103ad248`

Runtime execution status: VERIFIED for the current exact-head runtime conformance suite

Torch-Pass status: VERIFIED for the current exact-head Torch-Pass gate

Deployment governance status: VERIFIED for the current exact-head deployment-governance gate

Foundation / production status: UNVERIFIED

This audit distinguishes source evidence, exact-head CI evidence, and production/runtime parity. A green source gate does not by itself establish production truth.

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

`.github/workflows/authorized-vercel-release.yml` remains the canonical explicit human-authorized publication control plane with exact commit binding, verification, project binding, approval, and default-deny release authorization.

`vercel.json` now explicitly sets `git.deploymentEnabled` to `false`, matching the deployment-governance contract and preventing automatic Vercel Git deployments. Vercel's current documentation/support guidance confirms this setting disables automatic Git deployments. citeturn2search0turn2search3

**Classification:** Deliberate human-authorized control plane.

### 6. Active workflow inventory and side-effect sweep

The current `.github/workflows/` inventory was inspected through direct directory evidence plus direct file inspection. The consequential workflow set now resolves to:

Active governed/control-plane workflows:

- `deployment-governance.yml`
- `naya-power-runtime-tests.yml`
- `torch-pass-gate.yml`
- `authorized-vercel-release.yml`
- `apply-maxess-result-bridge.yml`
- `build-integrated-results.yml`
- `build-aiscore-app-bridge.yml`
- `2026-09-08-10-05-apply-nayanet-hub-surgical-patch.yml`

Retired workflows:

- `2026-09-08-canonical-hub-release-dispatch.yml`
- `2026-09-08-nuclear-right-rail-fix.yml`
- `2026-09-08-repair-main-feed-and-strip-garbage.yml`
- `2026-09-08-surgical-right-rail-removal.yml`
- `deploy-canonical-hub-vercel.yml`
- `deploy-nayanet-e03-foundation.yml`

The retired workflows are manual-only/read-only and contain no consequential mutation or deployment execution.

The read-only automated gates have no repository write permission and no direct deployment mutation boundary.

### 7. Repository-mutation bypasses

Four automatic repository-mutation bypasses were found and surgically closed:

- `.github/workflows/apply-maxess-result-bridge.yml`
- `.github/workflows/build-integrated-results.yml`
- `.github/workflows/build-aiscore-app-bridge.yml`
- `.github/workflows/2026-09-08-10-05-apply-nayanet-hub-surgical-patch.yml`

Each now requires manual dispatch and explicit approval before mutation/push.

The NayaNET Hub patch workflow's invoked script was inspected and confirmed to perform a real source mutation, so this was a genuine consequential automation boundary rather than a cosmetic workflow finding.

### 8. Automatic deployment bypasses

Two additional consequential deployment workflows were discovered during the direct side-effect sweep:

- `.github/workflows/deploy-canonical-hub-vercel.yml`
- `.github/workflows/deploy-nayanet-e03-foundation.yml`

Both previously reacted to repository pushes and executed Vercel deployment commands without an explicit human authorization gate.

These were concrete deployment-governance bypasses because the constitutional deployment boundary is human authority -> appropriate deployment control plane -> authorized deployment -> verification.

Both were surgically retired and now contain only `workflow_dispatch`, `contents: read`, and an explicit retirement notice pointing to the canonical human-authorized release boundary.

The deployment-governance regression suite subsequently passed at the exact resulting HEAD.

### 9. Continuity validator first true failure and repair

The first exact-head Torch-Pass failure was observed at commit `56c35fd306b062f9d06a241e8d5b094d1e1038a6`.

The Torch-Pass behavioral tests passed, but the canonical continuity validator failed on six real contract errors:

- three canonical historical event IDs lacking the timestamp component expected by the validator
- three successor-contract errors, including missing `completed_work` and `verified_evidence` in the canonical Smart Note successor

The historical event identities were preserved exactly. They were not rewritten or lowercased. The validator was surgically made compatible with the canonical historical date-only identity form, while retaining the timestamped form for new producers.

The Smart Note successor was surgically aligned to the validator's canonical field names (`Completed Work`, `Verified Evidence`).

At the resulting exact HEAD, Torch-Pass returned GREEN.

### 10. Deployment-governance first true failure and repair

At exact HEAD `47a885142da63718583253e5da2772fbb35a5394`, the deployment-governance gate exposed a real stale control-plane assumption: `deployment_governance_test.py` required `vercel.json.git.deploymentEnabled == false`, but the current `vercel.json` had no `git` section.

This was repaired by explicitly adding:

```json
"git": {
  "deploymentEnabled": false
}
```

The next exact-head deployment-governance execution then exposed two real automatic Vercel deployment workflows, which were subsequently retired as described above.

A later run exposed only a false-positive marker in the retired canonical-Hub workflow name/echo text; that marker was surgically renamed without weakening the deployment test.

The resulting exact-head deployment-governance gate is GREEN.

## Boundary classifications

| Boundary | Classification | Evidence-based disposition |
|---|---|---|
| Canonical Naya runtime | GOVERNED RUNTIME | Registry + Governance Contract + eligibility path; exact-head runtime tests GREEN |
| Authorized Vercel release | HUMAN-AUTHORIZED CONTROL PLANE | Exact SHA + approval + verification + default deny |
| Automatic Vercel Git deployment | DENIED | Explicit `git.deploymentEnabled=false` |
| Deployment governance | READ-ONLY / NON-CONSEQUENTIAL | Exact-head gate GREEN |
| Runtime tests | READ-ONLY / NON-CONSEQUENTIAL | Exact-head conformance suite GREEN |
| Torch-Pass | READ-ONLY / NON-CONSEQUENTIAL | Exact-head continuity gate GREEN |
| Four repository mutation workflows | HUMAN-AUTHORIZED CONTROL PLANE | Manual dispatch + explicit approval |
| NayaNET Hub surgical patch | HUMAN-AUTHORIZED CONTROL PLANE | Manual dispatch + explicit approval |
| Six legacy deployment/fix workflows | RETIRED | Manual-only/read-only/no consequential execution |

## Protected decisions

- Preserve fail-closed Registry behavior.
- Do not restore `registry=None` as a permissive path.
- Do not create a second authority hierarchy.
- Capability != Authority.
- Invalid != Zero Value.
- Do not redesign Registry scope without evidence.
- Do not permit automatic repository mutation merely because it is deterministic.
- Do not permit automatic deployment merely because a deployment is technically possible.
- Do not infer production verification from CI success.
- Do not manufacture Actions triggers.
- Do not modify read-only or retired workflows merely because they exist.
- Preserve canonical historical event identities exactly; repair validator compatibility instead of rewriting identity.

## Exact-head verification evidence

Current exact HEAD: `eb5aa407abe9ea730bd02383d6961da7103ad248`.

Exact-head runtime conformance suite:

- check: `runtime-tests`
- conclusion: `success`
- run: `34672011454`
- job: `103495009728`

Exact-head Torch-Pass:

- check: `torch-pass-enforcement`
- conclusion: `success`
- run: `34672011444`
- job: `103495009994`

Exact-head deployment governance:

- check: `deployment-governance`
- conclusion: `success`
- run: `34672011445`
- job: `103495009762`

Combined legacy commit status at this exact HEAD is `pending` with zero legacy status entries. The authoritative evidence for the governed gates is the exact-head check-run evidence above.

## Remaining verification boundary

Still UNKNOWN:

- production deployment parity
- live NayaNET runtime parity
- Foundation GREEN
- exhaustive repository-wide runtime constructor/call-site coverage
- production behavior outside the exact-head CI contracts

The available GitHub connector still does not expose a workflow-dispatch operation. No artificial trigger was created.

## Audit verdict

**CANONICAL NAYA RUNTIME GOVERNANCE PATH: NO OBSERVED SOURCE-LEVEL BYPASS**

**AUTOMATIC REPOSITORY-MUTATION BYPASSES: 4 FOUND; 4 SURGICALLY CLOSED**

**AUTOMATIC DEPLOYMENT BYPASSES: 2 FOUND; 2 RETIRED**

**DEPLOYMENT CONTROL PLANE: HUMAN AUTHORIZATION / DEFAULT DENY**

**EXACT-HEAD RUNTIME CONFORMANCE: GREEN**

**EXACT-HEAD TORCH-PASS: GREEN**

**EXACT-HEAD DEPLOYMENT GOVERNANCE: GREEN**

**PRODUCTION / FOUNDATION: UNVERIFIED**

**CURRENT FIRST TRUE FAILURE: NONE OBSERVED AFTER THE LATEST REPAIRS**

**EXHAUSTIVE RUNTIME CALL-SITE COVERAGE: UNKNOWN**

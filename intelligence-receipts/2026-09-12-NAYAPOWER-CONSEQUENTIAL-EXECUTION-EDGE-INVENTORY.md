# NayaPOWER Consequential Execution Edge Inventory — 2026-09-12

**STATUS:** ACTIVE / PARTIALLY VERIFIED  
**PURPOSE:** Record actual consequential execution surfaces and whether they cross the canonical NayaPOWER Governance Kernel.

## Constitutional rule

Every consequential execution path currently in scope must cross the canonical Governance Kernel before authorization/execution. Specialized controls may remain, but they must not become competing authorization systems.

## Confirmed surfaces inspected

| Surface | Consequential action | Previous control | Kernel status | Action taken |
|---|---|---|---|---|
| `.github/workflows/authorized-vercel-release.yml` | Deploy exact NayaNET artifact to Vercel | Release authorization + exact SHA + project binding + live verification | ROUTED | Release authorization now delegates final admission to canonical kernel; bounded expiry |
| `.naya/runtime/release_authorization.py` | Permit/deny Vercel release | Fail-closed release gate | ROUTED | Canonical kernel gate added after existing release checks |
| `.naya/memory/smart_note_enforcement.py` | Admit consequential Smart Note capture | Smart Note evidence/persistence/receipt enforcement | ROUTED | Existing enforcement preserved behind kernel admission |
| `build-aiscore-app-bridge.yml` | Write/push AIScore bridge | Explicit manual approval | ROUTED | Added canonical workflow kernel gate |
| `apply-maxess-result-bridge.yml` | Write/push MAXESS bridge | Explicit manual approval | ROUTED | Added canonical workflow kernel gate |
| `build-integrated-results.yml` | Write/push integrated Results artifact | Explicit manual approval | ROUTED | Added canonical workflow kernel gate |
| `2026-09-08-10-05-apply-nayanet-hub-surgical-patch.yml` | Write/push NayaNET Hub artifact | Explicit manual approval | ROUTED | Added canonical workflow kernel gate |
| `intelligence-promotion.yml` | Persist promoted intelligence projections | Automatic push + write/push | HARDENED | Automatic mutation disabled; explicit dispatch + kernel gate required |
| `execute-maxess-section01.yml` | Mutate MAXESS Section 01 checkpoint | Automatic branch push + write | HARDENED | Automatic mutation disabled; explicit dispatch + kernel gate required |
| `maxess-result-hydration.yml` | Mutate E01–E04 result artifacts | Automatic main push + write | HARDENED | Automatic mutation disabled; explicit dispatch + kernel gate required |

## Confirmed bypasses and repairs

### Bypass #1 — intelligence promotion

`intelligence-promotion.yml` persisted intelligence state from an automatic `push` event with `contents: write` and `git push`, without the canonical kernel.

**Repair:** retained the trigger as an observation/activation event, but the mutating job now requires explicit `workflow_dispatch` approval and `.naya/control-plane/workflow_gate.py` admission.

### Bypass #2 — MAXESS Section 01

`execute-maxess-section01.yml` had an automatic branch push trigger, write permission, and direct product mutation/push without the canonical kernel.

**Repair:** retained the trigger for detection/activation, but the mutating job now requires explicit dispatch approval and kernel admission.

### Bypass #3 — MAXESS Result Hydration

`maxess-result-hydration.yml` had an automatic main push trigger, write permission, and direct mutation of E01–E04 without the canonical kernel.

**Repair:** retained the trigger for detection/activation, but the mutating job now requires explicit dispatch approval and kernel admission.

## Kernel adapter

Created `.naya/control-plane/workflow_gate.py`.

The adapter does not duplicate constitutional rules. It constructs canonical authority + decision objects and calls `GovernanceKernel().gate(...)` with explicit actor, purpose, permission, scope, evidence, bounded one-hour authority, non-delegability, and risk dimensions.

## Targeted tests

- `tests/test_governance_kernel.py`
- `tests/test_smart_note_enforcement.py`
- `tests/test_execution_edge_kernel_coverage.py`
- `.naya/runtime/deployment_governance_test.py`

The execution-edge coverage suite now covers the known repository mutation workflows and verifies that the automatic mutation paths require explicit dispatch plus the canonical adapter.

## Remaining frontier

The repository contains additional build/deploy/execute/hydration workflows that have not all been individually inspected. Their presence is not treated as proof of bypass, and their safety is not claimed.

Continue inspecting workflows and code paths involving:

- `git push`
- external deployment commands
- mutation APIs
- credential-backed side effects
- branch/ref mutation
- artifact publication
- scheduled/queued execution
- agent/tool execution

## Evidence boundary

Source-level routing is verified by GitHub read-back. Exact repository test execution remains **UNVERIFIED** while GitHub Actions is paused and the local environment lacks the repository/network execution context.

No source inspection is promoted to runtime PASS.

## Current truth

> **The canonical Governance Kernel now governs multiple real consequential paths, and three additional automatic mutation bypasses have been identified and surgically closed. Universal coverage across every consequential execution edge remains UNVERIFIED.**

## Next action

Continue the repository-wide execution-edge inventory. Inspect the remaining build/deploy/execute/hydration workflows and credential-backed boundaries; route every confirmed consequential edge through the canonical kernel, add targeted fail-closed tests, obtain executable evidence when available, update the matrix/receipt, and continue until no in-scope consequential path remains outside the kernel.

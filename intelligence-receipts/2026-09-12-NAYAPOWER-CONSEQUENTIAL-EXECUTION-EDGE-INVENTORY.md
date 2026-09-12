# NayaPOWER Consequential Execution Edge Inventory — 2026-09-12

**STATUS:** ACTIVE / PARTIALLY VERIFIED  
**PURPOSE:** Record actual consequential execution surfaces and whether they cross the canonical NayaPOWER Governance Kernel.

## Constitutional rule

Every consequential execution path currently in scope must cross the canonical Governance Kernel before authorization/execution. Specialized controls may remain, but they must not become competing authorization systems.

## Confirmed surfaces inspected

| Surface | Consequential action | Pre-existing control | Kernel status | Action taken |
|---|---|---|---|---|
| `.github/workflows/authorized-vercel-release.yml` | Deploy exact NayaNET artifact to Vercel | Release authorization + exact SHA + project binding + live verification | **ROUTED** | Release authorization now delegates final admission to canonical kernel; authorization receives bounded expiry |
| `.naya/runtime/release_authorization.py` | Permit/deny Vercel release | Fail-closed release gate | **ROUTED** | Canonical kernel gate added after existing release checks |
| `.naya/memory/smart_note_enforcement.py` | Admit consequential Smart Note capture | Smart Note evidence/persistence/receipt enforcement | **ROUTED** | Existing enforcement preserved and placed behind kernel admission |
| `.github/workflows/build-aiscore-app-bridge.yml` | Write/push AIScore bridge | Explicit manual approval | **ROUTED** | Added canonical workflow kernel gate |
| `.github/workflows/apply-maxess-result-bridge.yml` | Write/push MAXESS bridge | Explicit manual approval | **ROUTED** | Added canonical workflow kernel gate |
| `.github/workflows/build-integrated-results.yml` | Write/push integrated Results artifact | Explicit manual approval | **ROUTED** | Added canonical workflow kernel gate |
| `.github/workflows/2026-09-08-10-05-apply-nayanet-hub-surgical-patch.yml` | Write/push NayaNET Hub artifact | Explicit manual approval | **ROUTED** | Added canonical workflow kernel gate |
| `.github/workflows/intelligence-promotion.yml` | Persist promoted intelligence projections | Previously automatic `push` trigger + write/push | **HARDENED** | Automatic mutation disabled; persistent promotion now requires explicit workflow dispatch approval + canonical kernel gate |

## First confirmed bypass

`intelligence-promotion.yml` was the first newly confirmed consequential bypass after the kernel foundation work.

It had `contents: write`, a `push` trigger on `main`, generated persistent intelligence state, and performed `git push` without crossing the canonical kernel. The existing workflow tests covered several manual mutation workflows but did not classify this automatic intelligence-promotion path as a kernel-governed mutation.

### Surgical repair

The workflow now:

1. retains its existing intelligence promotion logic;
2. retains the push trigger as an observation/activation event;
3. refuses to execute the mutating job for automatic push events;
4. requires explicit `workflow_dispatch` approval;
5. crosses `.naya/control-plane/workflow_gate.py`;
6. only then runs the existing promotion tests/build/persistence steps.

This preserves the promotion implementation while removing silent consequential mutation.

## Kernel adapter

Created:

`.naya/control-plane/workflow_gate.py`

This is a thin adapter. It does not duplicate constitutional rules. It constructs the canonical decision and authority objects and calls:

`GovernanceKernel().gate(...)`

The adapter uses bounded one-hour workflow authority, explicit actor/permission/purpose/scope, evidence, risk dimensions, and non-delegable authority.

## Remaining inventory frontier

The repository contains additional workflows with build/deploy/execute semantics that have not all been individually inspected yet. Their presence is not treated as proof of bypass, and their safety is not claimed.

The next inventory pass must inspect the remaining workflows named by the repository tree, especially:

- deployment/build workflows;
- MAXESS execution/hydration workflows;
- Hub build/deploy workflows;
- score hydration workflows;
- any workflow containing `git push`, external deployment commands, mutation APIs, or credential-backed side effects.

## Evidence boundary

Source-level routing is verified by GitHub read-back. Exact repository test execution remains **UNVERIFIED** while the GitHub Actions execution path is paused and the local environment lacks the repository/network execution context.

No source inspection is promoted to runtime PASS.

## Current truth

> **The canonical Governance Kernel now governs multiple real consequential paths, including deployment authorization, Smart Note admission, AIScore mutation, MAXESS mutation, integrated Results mutation, Hub mutation, and persistent intelligence promotion. Universal coverage across every consequential execution edge remains UNVERIFIED.**

## Next action

Continue the repository-wide execution-edge inventory until every consequential mutation/deployment/tool boundary is either:

`KERNEL-ROUTED` → targeted test → evidence

or:

`EXPLICITLY-DEFERRED / BLOCKED` with a recorded reason.

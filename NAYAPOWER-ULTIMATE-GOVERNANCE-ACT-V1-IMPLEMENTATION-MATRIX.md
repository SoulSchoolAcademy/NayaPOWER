# NayaPOWER Ultimate Governance Act V1 — Implementation Matrix

**DATE:** 2026-09-12  
**STATUS:** LIVE IMPLEMENTATION / EVIDENCE TRACKING  
**CANONICAL ACT:** `NAYAPOWER-ULTIMATE-GOVERNANCE-ACT-V1.md`

## Evidence rule

This matrix distinguishes constitutional intent from implementation and proof.

- **IMPLEMENTED** = a repository implementation exists.
- **TESTED** = an automated test exists and is wired into the canonical enforcement path.
- **VERIFIED** = execution evidence has been observed for the relevant exact revision.
- **UNVERIFIED** = implementation/test exists but the required execution evidence has not yet been observed.
- **DEFERRED** = responsible testing requires an environment or capability not currently available.

No UNVERIFIED or DEFERRED item is treated as SAFE or RELEASE_READY.

## P0 Requirement → Implementation → Test → Evidence → Deferred

| Requirement | Implementation | Test | Evidence | Deferred / Gap |
|---|---|---|---|---|
| Canonical constitutional law | `NAYAPOWER-ULTIMATE-GOVERNANCE-ACT-V1.md` | Governance reconciliation + regression work | Source exists on `main` | Constitutional effectiveness remains unverified until implementation is exercised end-to-end |
| Constitutional precedence | Act §§2, 28 | Adversarial precedence test required in kernel suite | Act is canonical source | Lower-layer injection tests still need implementation |
| Human authority | `Authority` in `.naya/governance/governance_kernel.py` | Missing, wrong actor, wrong scope, revoked/expired tests | Kernel implementation + tests committed | Full production authority registry integration remains |
| Authority registry | `AuthorityRegistry` in governance kernel | Registry primitive exists; direct resolution test still required | Registry primitive implemented | Canonical persistent registry and mutation governance remain |
| Canonical Decision Object | `DecisionObject` in governance kernel | Valid/incomplete decision behavior covered by gate tests | Machine-readable contract implemented | Universal execution-path adoption remains |
| Epistemic integrity | `Epistemic` + uncertainty gate | UNKNOWN/ASSUMED blocking test; VERIFIED ordering test | Kernel tests implemented | Full evidence provenance typing remains |
| Risk governance | `Risk` with `UNCERTAINTY × CONSEQUENCE × IRREVERSIBILITY` | High-risk verification test + risk validation | Kernel implementation exists | Full threshold calibration against real actions remains |
| Least necessary power | `necessary_power` / `requested_power` + subset enforcement | Excess-power adversarial test | Kernel test implemented | Binding to every real tool permission remains |
| Governance state | `GovernanceState` + `_ALLOWED_TRANSITIONS` + `transition()` | Valid-path, invalid promotion, and terminal STOP tests | Kernel state machine implemented | Runtime executor integration remains |
| Pre-action gate | `evaluate()` | Valid and fail-closed decision tests | Kernel gate wired into Smart Brain CI | Universal consequential execution interception remains |
| Verification law | `VerificationPlan` + observation/verification assertion | VERIFIED-without-observation negative test | Kernel test implemented | Independent runtime observation remains |
| Receipt requirements | `receipt_requirements()` | Success/block receipt requirement test | Kernel implementation + test | Canonical receipt persistence/integration remains |
| STOP / REFUSE / ASK / DEFER / ESCALATE | Decision/state enums + terminal STOP transition | STOP terminal-state test; negative paths | Kernel representation and STOP behavior implemented | Full executor integration remains |
| Retry law | Act §20 | First-failure/new-information tests required | Constitutional rule exists | Automated retry-policy enforcement remains |
| Obvious defect prevention | Act §21 | Defect fixtures required | Constitutional rule exists | Automated broad defect audit remains |
| Quality as correctness | Act §22 | Quality/release gate tests required | Constitutional rule exists | Product-level quality gate remains |
| Resource stewardship | Act §23 | Cost/power budget tests required | Constitutional rule exists | Runtime resource accounting remains |
| No dead end / continuity | Act §§24–26 + existing mandates | Handoff/next-action tests required | Existing constitutional law exists | Runtime handoff contract enforcement remains |
| Smart Note + Receipt Law | Existing Smart Note runtime + event store | Existing Smart Brain/Smart Note tests | Canonical event/index enforcement active | Full four-representation Hub runtime proof remains |
| Privacy boundaries | Existing permission-scope enforcement | Existing adversarial permission tests | Permission-scope gate exists | Full public/runtime privacy proof remains |
| Adversarial resistance | Act §27 | Existing permission tests + governance adversarial expansion | Partial | Prompt injection, authority spoofing, memory leakage, tool bypass suites remain |
| Governance of governance | Act §28 | Amendment/provenance tests required | Constitutional rule exists | Automated amendment authorization/version gate remains |
| Failure → learning | Act §29 | Failure receipt/repair tests required | Constitutional rule exists | Automated learning linkage remains |
| Constitutional testing loop | Act §30 | Smart Brain enforcement workflow | Workflow exists and is wired | Exact post-repair run evidence pending |
| Test now / test later | Act §31 | This matrix | Deferred categories explicitly separated | Public autonomous/cross-provider/long-horizon tests deferred |
| NayaPOWER self-proving ground | Act §32 | Smart Brain workflow + governance kernel gate | Governance kernel is now wired into canonical Smart Brain gate | End-to-end Intelligent Hub construction proof remains |
| Superbrain compounding | Act §33 + existing memory architecture | Event/index/continuity tests | Existing memory architecture | Full multi-Naya compounding proof remains |
| Release/runtime parity | Act §17 | Exact-SHA source→artifact→deployment→runtime tests required | No runtime evidence currently observed for latest governance changes | Runtime/deployment chain remains UNVERIFIED |

## Current execution state

### Repaired Smart Brain ordering

The stale-index failure was repaired by moving the existing derived-index rebuild to immediately after checkout and before the permission/Smart Brain validation gate. The surgical repair is commit:

`a37ca7e09cbe633616d9485b878f7ecdd77c02eb`

### Governance kernel establishment

The first canonical governance control-plane implementation was then added and wired into the Smart Brain enforcement workflow:

- `.naya/governance/governance_kernel.py`
- `.naya/governance/test_governance_kernel.py`
- `.github/workflows/smart-brain-v3-enforcement.yml`

The kernel currently enforces explicit authority, actor/action/scope matching, revoked/expired authority fail-closed behavior, epistemic uncertainty blocking, risk-sensitive verification, least-power containment, explicit governance state transitions, terminal STOP behavior, and receipt requirements.

The latest source revisions are on `main`. **Automated execution evidence for the latest governance commits is still required before declaring these gates VERIFIED.**

## Highest-value remaining implementation sequence

1. Obtain and inspect the first Smart Brain v3 Enforcement run for the latest `main` revision.
2. Apply FIRST NEW FAILURE ONLY repair discipline.
3. Verify the canonical governance kernel gate in the actual run.
4. Establish the persistent authority registry and mutation rules.
5. Bind consequential tool/workflow execution paths to the kernel rather than merely testing the kernel in isolation.
6. Add universal provenance/receipt emission and validation.
7. Add adversarial suites for authority spoofing, memory/authority confusion, handoff leakage, prompt injection, tool bypass, premature success claims, and constitutional precedence bypass.
8. Add automated amendment governance so constitutional law cannot be silently self-modified.
9. Prove exact source → artifact → deployment → runtime parity wherever runtime exists.
10. Use the resulting governed system to build and verify the Intelligent Hub as the practical NayaPOWER proving ground.

## Constitutional status rule

> **A written rule is intent. An implementation is behavior. A test is evidence. Runtime observation is stronger evidence. Independent validation is stronger still.**

Therefore:

**NayaPOWER Ultimate Governance Act V1 = CANONICAL / IMPLEMENTATION IN PROGRESS / NOT YET FULLY PROVEN.**

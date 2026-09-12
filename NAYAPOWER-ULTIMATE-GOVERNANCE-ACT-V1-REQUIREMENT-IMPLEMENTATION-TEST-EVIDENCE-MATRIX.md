# NayaPOWER Ultimate Governance Act V1 — Requirement → Implementation → Test → Evidence → Deferred Matrix

**DATE:** 2026-09-12  
**STATUS:** CANONICAL EXECUTION MATRIX / V1 HARDENING BASELINE  
**PURPOSE:** Convert the Ultimate Governance Act from constitutional text into an executable, testable, evidence-producing system.

> **Evidence rule:** UNVERIFIED is never equivalent to SAFE. Source inspection is not runtime proof.

| ID | Constitutional requirement | Implementation target | Current evidence | Status | Deferred / gap |
|---|---|---|---|---|---|
| GOV-001 | NayaPOWER is the governance layer, not the intelligence | Constitution + startup precedence + kernel identity | Mandates, Runtime Constitution, kernel contract | VERIFIED/DOCUMENTED | Runtime attestation across public systems |
| GOV-002 | Human authority is separate from capability | Authority object + registry + kernel gate | Kernel validates actor, holder, purpose, permission, status, revocation and expiry | IMPLEMENTED/PARTIAL | Universal authority lifecycle |
| GOV-003 | Protected human boundaries | Boundary policy + enforcement gates | Constitutional requirement + kernel boundary gate slot | PARTIAL | Machine-checkable boundary registry |
| GOV-004 | Truth states | Epistemic schema + promotion rules | Runtime Constitution + kernel transition controls | IMPLEMENTED/PARTIAL | Full epistemic state machine |
| GOV-005 | Responsible Verified Value | Value/decision contract | Act + kernel value/evidence fields | PARTIAL | Full value evaluation harness |
| GOV-006 | Least necessary power | Permission/scope evaluator | Kernel required-permission check | PARTIAL | Required-vs-granted power evaluator |
| GOV-007 | Risk = uncertainty × consequence × irreversibility | Canonical risk engine | Kernel implements deterministic R0–R5 routing | IMPLEMENTED/PARTIAL | Universal routing + R4 enforcement |
| GOV-008 | Consequential pre-action decision contract | Canonical decision object + kernel gate | Kernel requires all decision fields; multiple real mutation paths cross it | IMPLEMENTED/PARTIAL | Every consequential executor |
| GOV-009 | Fail closed | Hard execution gate | Validator + kernel authority/decision validation | VERIFIED for tested paths | Full ecosystem coverage |
| GOV-010 | Explicit governance states | Canonical state machine | Kernel rejects tested illegal transitions | IMPLEMENTED/PARTIAL | Universal state ownership |
| GOV-011 | Intended ≠ executed ≠ observed ≠ verified | Verification contract + independent observer | Kernel chain defined; independent observation remains separate | IMPLEMENTED/PARTIAL | Independent verification provider |
| GOV-012 | Source → build → deployment → runtime parity | Release audit contract | Release path now crosses kernel; exact runtime remains separate proof | IMPLEMENTED/PARTIAL | Broader runtime matrix |
| GOV-013 | Provenance and receipts | Smart Note + kernel receipts | Kernel receipts + Smart Note + deployment evidence paths | IMPLEMENTED/PARTIAL | Every consequential mutation receipt |
| GOV-014 | STOP/REFUSE/ESCALATE | Kernel halt + decision outcomes | Halt blocks continuation; halt clearing requires authorization | IMPLEMENTED/PARTIAL | Cross-system async propagation |
| GOV-015 | No retry without new information | Retry policy | Constitutional law documented | DOCUMENTED/PARTIAL | Runtime retry guard |
| GOV-016 | Obvious defect prevention | Pre-delivery quality gate | Constitutional principle | DOCUMENTED | Implement quality gate |
| GOV-017 | Quality is correctness | Universal quality evaluator | Existing standards | PARTIAL | Canonical evaluator |
| GOV-018 | Resource stewardship | Cost model | Doctrine exists | DOCUMENTED/PARTIAL | Executable cost policy |
| GOV-019 | Cheapest reliable validation first | Validation planner | Constitutional requirement | DOCUMENTED | Planner |
| GOV-020 | Minimum sufficient action | Surgical-change gate | Adaptive Reconstruction + Surgical Evolution | DOCUMENTED/PARTIAL | Automated delta audit |
| GOV-021 | No dead end | Continuation contract | Continuous Action + No Dead End Law | VERIFIED/DOCUMENTED | Runtime behavioral score |
| GOV-022 | Continuity without authority leakage | Handoff schema | Explicit kernel authority rather than memory-derived authority | PARTIAL | Permission inheritance tests |
| GOV-023 | Multi-Naya governance | Separate intelligence/authority model | Kernel actor-bound authority | DOCUMENTED/PARTIAL | Multi-runtime harness |
| GOV-024 | Adversarial resistance | Constitutional adversarial suite | Existing P0 harness + kernel + execution-edge guards | PARTIAL | Compound attacks |
| GOV-025 | Constitutional amendment governance | Versioned amendment protocol | Act + kernel constitutional binding | DOCUMENTED/PARTIAL | Protected constitutional paths |
| GOV-026 | Failure produces learning | Failure → lesson → regression → retest | Kernel receipts preserve failure/repair/next action | PARTIAL | Universal learning contract |
| GOV-027 | NayaPOWER is first proving ground | Dogfood governance | Kernel now governs multiple real repository mutation paths | IMPLEMENTED/PARTIAL | Full end-to-end proof |
| GOV-028 | Superbrain compounds intelligence, not authority | Intelligence/event schema + authority separation | Intelligence promotion mutation now requires explicit authority + kernel | IMPLEMENTED/PARTIAL | Machine-enforced handoff boundary |
| GOV-029 | Smart Notes produce linked representations + receipt | Smart Note runtime protocol | Smart Note admission now crosses kernel | IMPLEMENTED/PARTIAL | Full Hub runtime proof |
| GOV-030 | Privacy by choice | Privacy/sharing state | Constitutional privacy law | DOCUMENTED/PARTIAL | Universal runtime enforcement |
| GOV-031 | Governance is proportional | Risk-tiered control depth | Kernel routes R0–R5 | IMPLEMENTED/PARTIAL | Full control-depth enforcement |
| GOV-032 | Public/extreme tests deferred until environment exists | Deferred-test registry | Deferred/unverified distinction preserved | VERIFIED/DOCUMENTED | Public/runtime availability |

## CURRENT KERNEL COVERAGE — 2026-09-12

### Confirmed kernel-routed consequential edges

1. Vercel release authorization → `.naya/runtime/release_authorization.py` → Governance Kernel.
2. Smart Note admission → Governance Kernel → existing Smart Note evidence enforcement.
3. AIScore bridge mutation → `workflow_gate.py` → Governance Kernel.
4. MAXESS bridge mutation → `workflow_gate.py` → Governance Kernel.
5. Integrated Results mutation → `workflow_gate.py` → Governance Kernel.
6. NayaNET Hub mutation → `workflow_gate.py` → Governance Kernel.
7. Intelligence promotion → automatic mutation disabled; explicit dispatch → `workflow_gate.py` → Governance Kernel.
8. MAXESS Section 01 checkpoint → automatic mutation disabled; explicit dispatch → `workflow_gate.py` → Governance Kernel.
9. MAXESS Result Hydration → automatic mutation disabled; explicit dispatch → `workflow_gate.py` → Governance Kernel.

### Confirmed bypasses surgically closed

**Bypass #1:** `intelligence-promotion.yml` performed persistent intelligence mutation from an automatic `push` event with `contents: write` and `git push` without the kernel.

**Repair:** automatic event retained as an observation/activation trigger; mutating job requires explicit workflow dispatch approval and kernel admission.

**Bypass #2:** `execute-maxess-section01.yml` performed branch mutation from an automatic push trigger with write permission and no kernel gate.

**Repair:** automatic event retained as trigger/observation; mutating job now requires explicit workflow dispatch approval and kernel admission.

**Bypass #3:** `maxess-result-hydration.yml` performed mutation of E01–E04 from an automatic main push with write permission and no kernel gate.

**Repair:** automatic event retained as trigger/observation; mutating job now requires explicit workflow dispatch approval and kernel admission.

## Canonical adapter

`.naya/control-plane/workflow_gate.py`

The adapter creates explicit authority and decision objects and calls `GovernanceKernel().gate(...)`. Workflow authority is bounded, non-delegable, actor-bound, purpose-bound, permission-bound, and scope-bound.

## Targeted test artifacts

- `tests/test_governance_kernel.py`
- `tests/test_smart_note_enforcement.py`
- `tests/test_execution_edge_kernel_coverage.py`
- `.naya/runtime/deployment_governance_test.py`

Exact repository execution remains **UNVERIFIED** while GitHub Actions is paused and the local environment lacks repository execution/network context.

# P0 — IMPLEMENT NOW

The canonical kernel foundation is implemented. The remaining P0 gap is universal execution-edge coverage plus executable proof.

- Canonical constitutional authority: IMPLEMENTED/PARTIAL
- Canonical decision contract: IMPLEMENTED/PARTIAL
- Authority model: IMPLEMENTED/PARTIAL
- Evidence/verification chain: IMPLEMENTED/PARTIAL
- State machine: IMPLEMENTED/PARTIAL
- STOP/halt: IMPLEMENTED/PARTIAL
- Receipt: IMPLEMENTED/PARTIAL
- Test harness: IMPLEMENTED/PARTIAL / execution UNVERIFIED

# P1 — HARDEN

- Complete repository-wide execution-edge inventory.
- Risk-tier approval/verification enforcement.
- Least-privilege evaluator.
- Protected-boundary registry.
- Independent verification provider.
- Obvious-defect quality gate.
- Cost-aware action selection.
- Retry guard.
- Multi-Naya permission isolation.
- Prompt-injection/authority-spoofing suite.
- Goodhart/goal-substitution suite.
- Stale/contradictory state suite.
- Cold-start/restore/handoff suite.

# P2 — PUBLIC / RUNTIME VALIDATION

When the required environments exist: long-running autonomy, public Internet adversarial conditions, cross-provider testing, agent-to-agent interaction, long-horizon persistence, external-system boundaries, authorization escalation, and independent validation.

These are future evidence requirements, not safety claims.

# RELEASE GATES

Do not claim full proof until every P0 control has implementation + targeted test + durable evidence, known bypasses are repaired/accepted, consequential paths cross the kernel, authority does not silently propagate, STOP dominates continuation, runtime parity is proven where applicable, failure produces learning where applicable, NayaPOWER governs itself in representative work, and independent review occurs where practical.

## CURRENT RELEASE LANGUAGE

> **NayaPOWER Ultimate Governance Act V1 is a constitutional governance design and implementation target under active testing and hardening.**

Not: “NayaPOWER is proven safe.”

## CURRENT RECEIPTS

- `intelligence-receipts/2026-09-12-NAYAPOWER-GOVERNANCE-KERNEL-V1-RECEIPT.md`
- `intelligence-receipts/2026-09-12-NAYAPOWER-CONSEQUENTIAL-EXECUTION-EDGE-INVENTORY.md`

## KEY IMPLEMENTATION COMMITS

- `44c8efb6cc59d354c6ae96241cdfc68ac39a45ee` — workflow kernel adapter
- `ac22582822568774ab31a5bdcd2021c1c61a8183` — release kernel routing
- `b09b5d4d51b7eecace905aff9bb7d782e87ce585` — bounded release authorization
- `c250126cd8333059d1b05946a2cd9202aa89137b` — AIScore routing
- `975c4f7757e97c9505a14cf9215d3c528a27e797` — MAXESS bridge routing
- `d88030b1868bac02c2ed7614be2205aece03d627` — integrated Results routing
- `a6258bacfe82fc404ee3f280f724bad6a0063998` — Hub routing
- `f87c7a611999fc2e5bdcdaa146aa7de233563c6f` — intelligence promotion repair
- `0a66651b8ad29422fe18bf38c10c9deffef23f66` — MAXESS Section 01 repair
- `1a1a580baddb67435066916d07e45e3ddeec98f9` — MAXESS hydration repair
- `1d0f7a07b0edef77e0e21eee64f5849e8f40fa29` — execution-edge tests

## NEXT EXECUTION

**NEXT ACTION:** Continue inspecting the remaining build/deploy/execute/hydration workflows and credential-backed side effects. For each confirmed consequential edge: route through the canonical kernel → targeted fail-closed test → executable evidence → receipt → matrix → next bypass. Stop only when every in-scope consequential edge is kernel-routed or explicitly DEFERRED/BLOCKED.

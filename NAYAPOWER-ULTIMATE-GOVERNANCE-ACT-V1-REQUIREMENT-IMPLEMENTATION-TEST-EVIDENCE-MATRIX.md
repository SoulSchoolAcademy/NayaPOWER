# NayaPOWER Ultimate Governance Act V1.1 — Requirement → Implementation → Test → Evidence → Deferred Matrix

**DATE:** 2026-09-12  
**STATUS:** CANONICAL EXECUTION MATRIX / V1.1 HARDENING BASELINE  
**ACT:** `NAYAPOWER-ULTIMATE-GOVERNANCE-ACT-V1.1.md`  
**PURPOSE:** Convert the Ultimate Governance Act from constitutional text into an executable, testable, evidence-producing system.

> **Evidence rule:** UNVERIFIED is never equivalent to SAFE. Source inspection is not runtime proof.

## V1.1 DELTA — WHAT CHANGED

V1.1 preserves the V1 constitutional foundation and makes the highest-value governance gaps explicit:

1. One canonical Governance Kernel is the mandatory consequential execution boundary.
2. No workflow, agent, model, memory system, connector, tool, runtime, scheduler, delegated actor, or downstream executor may create an alternative consequential path that bypasses or substitutes for the kernel.
3. Capability, credentials, write access, and workflow-dispatch capability do not constitute authority.
4. Authority is non-serializable/non-inheritable by default; delegation requires explicit authorization.
5. Governance applicability is determined by policy/kernel, not by the actor performing the action.
6. Verification claims must identify the observed boundary and supporting evidence.
7. STOP must dominate retries, queued, delegated, scheduled, downstream, and persistent work where technically controllable.
8. Requested power, necessary power, granted power, and actual power used are distinct governance quantities.
9. Compound adversarial attacks are explicitly required.
10. Constitutional paths themselves are protected governance surfaces.
11. Proof-state language is standardized: VERIFIED / IMPLEMENTED / PARTIAL / DOCUMENTED / UNVERIFIED / DEFERRED / BLOCKED.
12. NayaPOWER dogfooding is an explicit proving objective: governed Nayas must eventually build, verify, and improve the Intelligent Hub without human micromanagement of every consequential step.

## REQUIREMENT MATRIX

| ID | Constitutional requirement | Implementation target | Current evidence | Status | Deferred / gap |
|---|---|---|---|---|---|
| GOV-001 | NayaPOWER is the governance layer, not the intelligence | Constitution + startup precedence + kernel identity | Act V1.1 + Runtime Constitution + kernel contract | IMPLEMENTED/PARTIAL | Runtime attestation across public systems |
| GOV-002 | Human authority is separate from capability | Authority object + persistent registry + kernel gate | Kernel validates explicit actor-bound authority; workflow adapter no longer mints authority | IMPLEMENTED/PARTIAL | Universal authority lifecycle, revocation/delegation evidence |
| GOV-003 | Protected human boundaries | Boundary policy + machine-checkable enforcement gates | Act + kernel boundary gate slot | PARTIAL | Canonical boundary registry + broad runtime enforcement |
| GOV-004 | Truth states | Epistemic schema + promotion rules | Runtime Constitution + kernel transition controls | IMPLEMENTED/PARTIAL | Universal legal transition enforcement |
| GOV-005 | Responsible Verified Value | Value/decision contract | Act + kernel value/evidence fields | PARTIAL | Full value evaluation harness |
| GOV-006 | Least necessary power | Permission/scope evaluator | Kernel required-permission check | PARTIAL | Required-vs-granted-vs-used power evaluator |
| GOV-007 | Risk = uncertainty × consequence × irreversibility | Canonical risk engine | Kernel implements deterministic R0–R5 routing | IMPLEMENTED/PARTIAL | Universal routing + stronger R4/R5 enforcement |
| GOV-008 | Consequential pre-action decision contract | Canonical decision object + kernel gate | Kernel requires decision fields; multiple real mutation paths cross it | IMPLEMENTED/PARTIAL | Prove every in-scope consequential executor |
| GOV-009 | Fail closed | Hard execution gate | Kernel authority/decision validation + workflow adapter tests | VERIFIED for tested paths | Full ecosystem coverage |
| GOV-010 | Explicit governance states | Canonical state machine | Kernel rejects tested illegal transitions | IMPLEMENTED/PARTIAL | Universal state ownership |
| GOV-011 | Intended ≠ executed ≠ observed ≠ verified | Verification contract + independent observer | Kernel chain defined; exact runtime observation remains separate | IMPLEMENTED/PARTIAL | Independent verification provider |
| GOV-012 | Source → build → deployment → runtime parity | Release audit contract | Release path crosses kernel; exact runtime proof remains separate | IMPLEMENTED/PARTIAL | Broader runtime matrix |
| GOV-013 | Provenance and receipts | Smart Note + universal consequential receipts | Kernel receipts + Smart Note/deployment evidence paths | IMPLEMENTED/PARTIAL | Every consequential mutation receipt |
| GOV-014 | STOP/REFUSE/ESCALATE | Kernel halt + decision outcomes + downstream propagation | Kernel halt blocks continuation in tested path | IMPLEMENTED/PARTIAL | Cross-system async propagation |
| GOV-015 | No retry without new information | Retry policy + attempt record | Constitutional law + V1.1 retry record requirement | DOCUMENTED/PARTIAL | Runtime retry guard |
| GOV-016 | Obvious defect prevention | Pre-delivery quality gate | Constitutional requirement | DOCUMENTED | Implement executable quality gate |
| GOV-017 | Quality is correctness | Universal quality evaluator | Existing standards + Act | PARTIAL | Canonical evaluator |
| GOV-018 | Resource stewardship | Cost model | Doctrine exists | DOCUMENTED/PARTIAL | Executable cost policy |
| GOV-019 | Cheapest reliable validation first | Validation planner | Constitutional requirement | DOCUMENTED | Planner |
| GOV-020 | Minimum sufficient action | Surgical-change gate | Adaptive Reconstruction + Surgical Evolution | DOCUMENTED/PARTIAL | Automated authorized-delta vs actual-delta audit |
| GOV-021 | No dead end | Continuation contract | Continuous Action + No Dead End Law | VERIFIED/DOCUMENTED | Runtime behavioral score |
| GOV-022 | Continuity without authority leakage | Handoff schema + non-inheritance rule | Explicit kernel authority rather than memory-derived authority | PARTIAL | Permission inheritance/leakage tests |
| GOV-023 | Multi-Naya governance | Separate intelligence/authority model | Kernel actor-bound authority | DOCUMENTED/PARTIAL | Multi-runtime harness |
| GOV-024 | Adversarial resistance | Constitutional adversarial suite | Existing P0 harness + kernel + execution-edge guards | PARTIAL | Compound attacks and full bypass corpus |
| GOV-025 | Constitutional amendment governance | Versioned amendment protocol + protected path | Act V1.1 protected constitutional path | DOCUMENTED/PARTIAL | Machine-enforced protected mutation path |
| GOV-026 | Failure produces learning | Failure → lesson → regression → retest | Kernel receipts preserve failure/repair/next action | PARTIAL | Universal learning contract |
| GOV-027 | NayaPOWER is first proving ground | Dogfood governance | Kernel governs multiple real repository mutation paths | IMPLEMENTED/PARTIAL | Full end-to-end proof |
| GOV-028 | Superbrain compounds intelligence, not authority | Intelligence/event schema + authority separation | Intelligence promotion requires explicit authority + kernel | IMPLEMENTED/PARTIAL | Machine-enforced handoff boundary |
| GOV-029 | Smart Notes produce linked representations + receipt | Smart Note runtime protocol | Smart Note admission crosses kernel | IMPLEMENTED/PARTIAL | Full Hub runtime proof |
| GOV-030 | Privacy by choice | Privacy/sharing state | Constitutional privacy law | DOCUMENTED/PARTIAL | Universal runtime enforcement |
| GOV-031 | Governance is proportional | Risk-tiered control depth | Kernel routes R0–R5 | IMPLEMENTED/PARTIAL | Full control-depth enforcement |
| GOV-032 | Public/extreme tests deferred until environment exists | Deferred-test registry | Deferred/unverified distinction preserved | VERIFIED/DOCUMENTED | Public/runtime availability |
| GOV-033 | Universal consequential execution path | Canonical Governance Kernel as sole consequential boundary | V1.1 Act + kernel + workflow adapter + execution-edge tests | IMPLEMENTED/PARTIAL | Complete repository/ecosystem edge inventory |
| GOV-034 | No self-minted authority | Persistent authority registry + exact lookup | `workflow_gate.py` resolves pre-existing explicit grants; tests reject unknown actor/scope | IMPLEMENTED/PARTIAL | Registry lifecycle hardening |
| GOV-035 | Authority non-inheritance | Explicit authority re-resolution at handoff/continuation | Act V1.1 rule; current adapter actor/scope binding | DOCUMENTED/PARTIAL | Machine-enforced cross-runtime handoff tests |
| GOV-036 | Verification claim must name observed boundary | Receipt/verification contract | Act V1.1 rule; release evidence architecture | DOCUMENTED/PARTIAL | Universal verifier implementation |
| GOV-037 | STOP dominates downstream work | Halt propagation contract | Kernel terminal halt behavior | IMPLEMENTED/PARTIAL | Async/queued/delegated propagation |
| GOV-038 | Compound adversarial attacks | Adversarial test families + attack composition | Act V1.1 explicit requirement | DOCUMENTED | Implement compound suite |
| GOV-039 | Governance surfaces are protected | Constitutional path enforcement | Act V1.1 protected-path requirement | DOCUMENTED/PARTIAL | Enforce mutation authorization at repository boundary |
| GOV-040 | Proof-state discipline | Standard proof vocabulary + matrix evidence rules | Act V1.1 + this matrix | IMPLEMENTED/DOCUMENTED | Automated claim-strength validator |
| GOV-041 | NayaPOWER self-governance / dogfooding | Governed build/verify/improve loop | Multiple kernel-routed repository paths | IMPLEMENTED/PARTIAL | End-to-end Hub proof |

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

### Known execution-boundary issue currently under active verification

At the last observed authoritative run (`34699123713`, source SHA `93b6b754957cd31844771b23a078756c4fbb8e16`), the first new failure was the execution-boundary self-test detecting a stale reference to the retired `deploy-nayanet-hub-canonical.yml` workflow from `.github/workflows/naya-claim-evidence-enforcement.yml`.

**Surgical repair committed:** `ab7b16be5d49d687abe4d0570af85b853b63655e` — updated that stale dispatch target to `deploy-nayanet-hub-canonical-v2.yml`.

**Current proof state:** the repair is source-committed, but an authoritative run for `ab7b16be5d49d687abe4d0570af85b853b63655e` has not yet been observed. Therefore the repair is **IMPLEMENTED / UNVERIFIED**, not GREEN.

### Next known governance risk after the first failure clears

The claim-evidence workflow currently has consequential workflow-dispatch capability and a direct deployment dispatch edge. This must be evaluated against the V1.1 law that every consequential execution path must pass through the canonical Governance Kernel and that capability cannot create authority. Do not change it until the current first-failure execution loop provides the next evidence boundary, unless independent evidence proves the edge is itself the first failure.

## CONFIRMED BYPASS REPAIRS

**Bypass #1:** `intelligence-promotion.yml` performed persistent intelligence mutation from an automatic `push` event with `contents: write` and `git push` without the kernel.

**Repair:** automatic event retained as an observation/activation trigger; mutating job requires explicit workflow dispatch approval and kernel admission.

**Bypass #2:** `execute-maxess-section01.yml` performed branch mutation from an automatic push trigger with write permission and no kernel gate.

**Repair:** automatic event retained as trigger/observation; mutating job now requires explicit workflow dispatch approval and kernel admission.

**Bypass #3:** `maxess-result-hydration.yml` performed mutation of E01–E04 from an automatic main push with write permission and no kernel gate.

**Repair:** automatic event retained as trigger/observation; mutating job now requires explicit workflow dispatch approval and kernel admission.

## CANONICAL ADAPTER

`.naya/control-plane/workflow_gate.py`

The adapter translates a consequential workflow request into the canonical Decision Object and calls `GovernanceKernel().gate(...)`. It must resolve a pre-existing explicit authority grant and must never mint authority from the request itself.

## TARGETED TEST ARTIFACTS

- `.naya/governance/test_governance_kernel.py`
- `.naya/control-plane/test_workflow_gate.py`
- `tests/test_smart_note_enforcement.py`
- `tests/test_execution_edge_kernel_coverage.py`
- `.naya/governance/test_naya_execution_boundaries.py`
- `.naya/runtime/deployment_governance_test.py`

## P0 — IMPLEMENT / PROVE NOW

The canonical kernel foundation exists. The remaining P0 gap is universal consequential-edge coverage plus executable proof.

- Canonical constitutional authority: IMPLEMENTED/PARTIAL
- Canonical decision contract: IMPLEMENTED/PARTIAL
- Authority model: IMPLEMENTED/PARTIAL
- Evidence/verification chain: IMPLEMENTED/PARTIAL
- State machine: IMPLEMENTED/PARTIAL
- STOP/halt: IMPLEMENTED/PARTIAL
- Receipt: IMPLEMENTED/PARTIAL
- Test harness: IMPLEMENTED/PARTIAL
- Exact current execution proof: UNVERIFIED pending authoritative run for `ab7b16be5d49d687abe4d0570af85b853b63655e`

## P1 — HARDEN

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
- Compound adversarial attack suite.
- Authority registry lifecycle and protected governance-surface mutation.

## P2 — PUBLIC / RUNTIME VALIDATION

When the required environments exist: long-running autonomy, public Internet adversarial conditions, cross-provider testing, agent-to-agent interaction, long-horizon persistence, external-system boundaries, authorization escalation, and independent validation.

These are future evidence requirements, not safety claims.

## RELEASE GATES

Do not claim full proof until every P0 control has implementation + targeted test + durable evidence, known bypasses are repaired/accepted, consequential paths cross the kernel, authority does not silently propagate, STOP dominates continuation, runtime parity is proven where applicable, failure produces learning where applicable, NayaPOWER governs itself in representative work, and independent review occurs where practical.

## CURRENT RELEASE LANGUAGE

> **NayaPOWER Ultimate Governance Act V1.1 is a constitutional governance design and implementation target under active testing and hardening.**

Not: “NayaPOWER is proven safe.”

## CURRENT RECEIPTS / EVIDENCE

- `intelligence-receipts/2026-09-12-NAYAPOWER-GOVERNANCE-KERNEL-V1-RECEIPT.md`
- `intelligence-receipts/2026-09-12-NAYAPOWER-CONSEQUENTIAL-EXECUTION-EDGE-INVENTORY.md`
- authoritative run `34699123713` on `93b6b754957cd31844771b23a078756c4fbb8e16` — first failure recorded above
- surgical source repair `ab7b16be5d49d687abe4d0570af85b853b63655e` — pending authoritative execution evidence

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
- `ab7b16be5d49d687abe4d0570af85b853b63655e` — stale canonical deployment reference repair
- `fbbd3788f641d75f5598ad5c62298185939570c8` — Governance Act V1.1 creation

## NEXT EXECUTION — HANDOFF

**NEXT ACTION:** Execute the authoritative governance workflow against exact main HEAD `ab7b16be5d49d687abe4d0570af85b853b63655e`. If a run appears, inspect jobs/logs and take the **first new failure only**. If GREEN, immediately audit the claim-evidence → deployment dispatch edge against V1.1, repair the smallest constitutional violation, add/strengthen its fail-closed test, rerun, verify, update this matrix, and continue into the remaining consequential-edge inventory.

**DO NOT CLAIM GREEN UNTIL EXECUTION EVIDENCE EXISTS.**
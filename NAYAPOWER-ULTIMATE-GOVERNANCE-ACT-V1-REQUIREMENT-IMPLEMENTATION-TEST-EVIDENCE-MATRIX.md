# NayaPOWER Ultimate Governance Act V1 — Requirement → Implementation → Test → Evidence → Deferred Matrix

**DATE:** 2026-09-12  
**STATUS:** CANONICAL EXECUTION MATRIX / V1 HARDENING BASELINE  
**PURPOSE:** Convert the Ultimate Governance Act from constitutional text into an executable, testable, evidence-producing system.

## Evidence vocabulary

- **VERIFIED:** Direct evidence currently available from repository/runtime/tool output.
- **IMPLEMENTED:** Behavior exists in code/configuration, but proof may still require a targeted test.
- **PARTIAL:** Some enforcement exists, but the constitutional requirement is broader than the current implementation.
- **DOCUMENTED:** Rule exists as authoritative prose but is not yet sufficiently enforced.
- **UNVERIFIED:** No adequate evidence yet.
- **DEFERRED:** Requires a runtime/environment/test capability not currently available.
- **BLOCKED:** A known dependency prevents the next proof step.

> **Rule:** UNVERIFIED is never equivalent to SAFE.

---

| ID | Constitutional requirement | Implementation target | Test required now | Current evidence | Status | Deferred / gap |
|---|---|---|---|---|---|---|
| GOV-001 | NayaPOWER is the governance layer, not the intelligence | Canonical constitution + startup precedence + kernel identity | Cold-start identity/precedence test | Mandates, Runtime Constitution, and kernel contract bind governance identity | VERIFIED/DOCUMENTED | Runtime attestation across public systems |
| GOV-002 | Human authority is separate from capability | Canonical authority object + registry + kernel gate | Attempt unauthorized consequential action | Kernel validates actor, holder, purpose, permission, status, revocation and expiry; broader authority registry remains | IMPLEMENTED/PARTIAL | Universal authority lifecycle and every consequential path |
| GOV-003 | Protected human boundaries | Boundary policy + enforcement gates | Boundary violation suite | Constitutional requirement established; kernel has protected-boundary gate slot | PARTIAL | Machine-checkable protected-boundary registry |
| GOV-004 | Truth states: known/observed/verified/inferred/assumed/unknown | Epistemic state schema + promotion rules | Inject inference as verified fact | Runtime Constitution defines evidence tiers; kernel prevents key verification-state bypasses | IMPLEMENTED/PARTIAL | Full canonical epistemic state machine |
| GOV-005 | Responsible Verified Value | Value/decision contract | Goodhart/metric substitution tests | Act defines Responsible Verified Value; kernel carries value/evidence fields but not full calculus | PARTIAL | Full value evaluation harness |
| GOV-006 | Least necessary power | Permission/scope registry + evaluator | Request excessive scope | Kernel validates required permission but does not calculate required vs granted power universally | PARTIAL | Formal least-privilege evaluator |
| GOV-007 | Risk = uncertainty × consequence × irreversibility | Canonical risk engine | Same action under different risk conditions | Kernel implements deterministic R0–R5 routing | IMPLEMENTED/PARTIAL | Universal path integration and R4 enforcement |
| GOV-008 | Consequential pre-action decision contract | Canonical decision object + kernel gate | Missing-field fail-closed tests | Kernel requires all constitutional decision fields; multiple real mutation paths now cross it | IMPLEMENTED/PARTIAL | Route every consequential executor through gate |
| GOV-009 | Fail closed when governance evidence is missing | Hard execution gate | Remove authority/evidence and execute | Existing validator plus kernel authority/decision validation | VERIFIED for tested paths | Full ecosystem coverage |
| GOV-010 | Explicit governance states | Canonical state machine + legal transitions | Attempt invalid state transition | Kernel rejects tested bypasses including EXECUTED→VERIFIED, DEFERRED→EXECUTING, STOPPED→EXECUTING | IMPLEMENTED/PARTIAL | Universal state ownership |
| GOV-011 | Intended ≠ executed ≠ observed ≠ verified | Verification contract + independent observer | Claim success before observation | Kernel defines verification chain; independent observation remains separate | IMPLEMENTED/PARTIAL | Independent verification provider |
| GOV-012 | Source → build → deployment → runtime parity | Release audit contract | Exact runtime verification | Deployment governance requires exact SHA/project/evidence; release path now crosses kernel | IMPLEMENTED/PARTIAL | Broader runtime matrix |
| GOV-013 | Provenance and receipts | Smart Note/receipt + kernel receipt | Fabricated receipt / missing evidence | Kernel receipt + Smart Note enforcement + deployment receipt paths | IMPLEMENTED/PARTIAL | Every consequential mutation emits canonical receipt |
| GOV-014 | STOP/REFUSE/ESCALATE are valid states | Kernel halt + decision outcomes | Force high-risk/unauthorized action | Kernel halt blocks continuation; halt clearing requires authorization | IMPLEMENTED/PARTIAL | Propagate halt across async/queued/delegated work |
| GOV-015 | No retry without new information | Retry policy | Repeat identical failed action | Constitutional requirement documented; runtime retry guard absent | DOCUMENTED/PARTIAL | Runtime retry guard |
| GOV-016 | Obvious defect prevention | Pre-delivery quality gate | Seed defect and test block | Quality principle established | DOCUMENTED | Implement quality gate |
| GOV-017 | Quality is part of correctness | Quality/release state | Artifact exists but fails requirements | Existing standards; no universal evaluator | PARTIAL | Canonical quality evaluator |
| GOV-018 | Resource stewardship | Action cost model | Compare unnecessary vs necessary action | Stewardship doctrine exists | DOCUMENTED/PARTIAL | Executable cost-aware policy |
| GOV-019 | Cheapest reliable validation first | Validation planner | Expensive vs cheaper sufficient test | Constitutional requirement | DOCUMENTED | Planner/decision rule |
| GOV-020 | Minimum sufficient action | Surgical-change gate | Detect unrelated mutation | Adaptive Reconstruction + Surgical Evolution | DOCUMENTED/PARTIAL | Automated change-scope audit |
| GOV-021 | No dead end / next action | Continuation contract | Block task and require useful next state | Continuous Action + No Dead End Law | VERIFIED/DOCUMENTED | Runtime behavioral score |
| GOV-022 | Continuity without authority leakage | Handoff schema + Superbrain state | Handoff intelligence then attempt unauthorized action | Kernel authority is explicit rather than memory-derived | PARTIAL | Formal permission inheritance test |
| GOV-023 | Multi-Naya governance | Shared intelligence + separate authority | Naya A authorizes; Naya B attempts action | Architecture defined; kernel authority is actor-bound | DOCUMENTED/PARTIAL | Multi-runtime harness |
| GOV-024 | Adversarial resistance | Constitutional adversarial suite | Injection, spoofing, escalation, concealment, goal substitution | Existing P0 harness + kernel tests + execution-edge guards | PARTIAL | Compound attack corpus |
| GOV-025 | Constitutional amendment governance | Versioned amendment protocol | Unauthorized constitution rewrite | Act establishes amendment law; kernel binds to Act | DOCUMENTED/PARTIAL | Protected constitutional paths |
| GOV-026 | Failure produces learning | Failure receipt + Smart Note | Failure → lesson → regression → retest | Kernel receipts carry failure/repair/next action; CIS architecture exists | PARTIAL | Universal failure-learning contract |
| GOV-027 | NayaPOWER is first proving ground | Dogfood governance during repo work | Audit real Naya changes | Kernel is now governing real repository mutation paths | IMPLEMENTED/PARTIAL | Full end-to-end behavioral proof |
| GOV-028 | Superbrain compounds intelligence, not authority | Intelligence/event schema + authority separation | Persist event then attempt authority inheritance | Explicit kernel authority; intelligence-promotion mutation now requires manual authority | IMPLEMENTED/PARTIAL | Machine-enforced authority boundary across handoffs |
| GOV-029 | Smart Notes produce linked representations + receipt | Smart Note runtime protocol | Missing representation must fail receipt | Existing Smart Note enforcement now requires kernel admission | IMPLEMENTED/PARTIAL | Full Hub runtime proof |
| GOV-030 | Privacy by choice | Privacy/sharing state in receipt/event | Share private intelligence without permission | Constitutional privacy law; no universal sharing state | DOCUMENTED/PARTIAL | Runtime enforcement across boundaries |
| GOV-031 | Governance must be proportional | Risk-tiered control depth | Compare low-risk and consequential burden | Kernel routes R0–R5; universal control-depth enforcement absent | IMPLEMENTED/PARTIAL | Full proportional control enforcement |
| GOV-032 | Public/extreme tests deferred until environment exists | Deferred-test registry | Ensure deferred categories remain UNVERIFIED | Act/receipts preserve deferred/unverified distinction | VERIFIED/DOCUMENTED | Public/runtime availability |

---

# CURRENT KERNEL COVERAGE — 2026-09-12

## Confirmed consequential execution edges inspected

| Execution edge | Previous control | Kernel routing | Evidence status |
|---|---|---|---|
| Vercel release authorization | Release authorization gate | `.naya/runtime/release_authorization.py` → canonical kernel | SOURCE-VERIFIED / RUNTIME-UNVERIFIED |
| Smart Note admission | Smart Note enforcement | Smart Note gate → canonical kernel → existing evidence checks | SOURCE-VERIFIED / RUNTIME-UNVERIFIED |
| AIScore bridge mutation | Manual approval | workflow → `workflow_gate.py` → kernel | SOURCE-VERIFIED / RUNTIME-UNVERIFIED |
| MAXESS bridge mutation | Manual approval | workflow → `workflow_gate.py` → kernel | SOURCE-VERIFIED / RUNTIME-UNVERIFIED |
| Integrated Results mutation | Manual approval | workflow → `workflow_gate.py` → kernel | SOURCE-VERIFIED / RUNTIME-UNVERIFIED |
| NayaNET Hub mutation | Manual approval | workflow → `workflow_gate.py` → kernel | SOURCE-VERIFIED / RUNTIME-UNVERIFIED |
| Intelligence promotion | Automatic push + write/push | automatic mutation disabled; manual dispatch → `workflow_gate.py` → kernel | SOURCE-VERIFIED / RUNTIME-UNVERIFIED |

### First confirmed bypass after kernel creation

`intelligence-promotion.yml` was found to mutate persistent intelligence state on an automatic `push` event with `contents: write` and `git push`, without the canonical kernel. The workflow was surgically changed so the mutating job executes only from explicit `workflow_dispatch` approval and after the canonical kernel gate.

This preserves the promotion engine and learning logic while removing silent consequential mutation.

## Canonical workflow adapter

Created:

`.naya/control-plane/workflow_gate.py`

The adapter constructs the constitutional decision and authority objects and calls `GovernanceKernel().gate(...)`. Workflow authority is bounded to one hour, explicit actor/purpose/permission/scope, and non-delegable.

## Inventory receipt

`intelligence-receipts/2026-09-12-NAYAPOWER-CONSEQUENTIAL-EXECUTION-EDGE-INVENTORY.md`

This receipt records the inspected execution edges, confirmed bypass, repairs, and remaining uninspected workflow frontier.

---

# P0 — IMPLEMENT NOW

The kernel foundation is implemented and multiple real consequential paths now cross it. The remaining P0 problem is universal coverage and executable proof.

## P0.1 Canonical constitutional authority

Keep `NAYAPOWER-ULTIMATE-GOVERNANCE-ACT-V1.md` as the constitutional target and bind executable enforcement to it.

## P0.2 Canonical decision contract

**IMPLEMENTED/PARTIAL:** `.naya/control-plane/GOVERNANCE-KERNEL.json` + `.naya/control-plane/governance_kernel.py` define and validate the constitutional decision fields. Multiple mutation paths now call the kernel.

## P0.3 Authority registry

**IMPLEMENTED/PARTIAL:** Kernel authority validation requires actor, holder, issuer, purpose, permissions, scope, issuance, expiry, revocation and status. A universal lifecycle/delegation registry remains.

## P0.4 Evidence and verification contract

**IMPLEMENTED/PARTIAL:** Kernel defines `INTENDED → AUTHORIZED → EXECUTED → OBSERVED → VERIFIED` and rejects direct bypasses. Independent observation remains.

## P0.5 Explicit governance state machine

**IMPLEMENTED/PARTIAL:** Kernel defines legal transitions and rejects tested bypasses.

## P0.6 STOP/ASK/DEFER/REFUSE/ESCALATE

**IMPLEMENTED/PARTIAL:** Kernel implements halt dominance and non-success states. Cross-system halt propagation remains.

## P0.7 Provenance / receipt completeness

**IMPLEMENTED/PARTIAL:** Kernel receipt contains actor, authority, request, decision, state, result, observation, verification, uncertainty, failure, repair, next action, timestamp and integrity hash.

## P0.8 Constitutional test harness

**IMPLEMENTED/PARTIAL:** Targeted kernel tests, Smart Note regression tests, deployment governance tests, and repository validator integration exist. Exact repository execution remains **UNVERIFIED** while GitHub Actions is paused and the local environment lacks the repository execution context.

---

# P1 — HARDEN AFTER KERNEL FOUNDATION

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
- Full cold-start/restore/handoff suite.

# P2 — PUBLIC / RUNTIME VALIDATION

When required public/runtime environments are available:

- long-running autonomous operation;
- public Internet adversarial conditions;
- cross-provider model testing;
- large-scale agent-to-agent interaction;
- long-horizon persistence attacks;
- real external-system boundary testing;
- production-scale authorization escalation attempts;
- independent external validation.

These are future evidence requirements, not current safety claims.

---

# RELEASE GATES

NayaPOWER Ultimate Governance Act V1 should not be described as fully proven until:

1. Every P0 requirement has an implementation target.
2. Every implemented P0 requirement has a targeted test.
3. Every passing test has durable evidence.
4. Known bypasses are repaired or explicitly accepted at the appropriate authority level.
5. Critical consequential paths fail closed when required governance evidence is missing.
6. NayaPOWER successfully governs itself through representative real project work.
7. Public/runtime tests are added when the environment exists.
8. Resulting evidence is independently reviewed where practical.

## CURRENT RELEASE LANGUAGE

> **NayaPOWER Ultimate Governance Act V1 is a constitutional governance design and implementation target under active testing and hardening.**

Not: “NayaPOWER is proven safe.”

---

# CURRENT EXECUTION RECEIPTS

- `intelligence-receipts/2026-09-12-NAYAPOWER-GOVERNANCE-KERNEL-V1-RECEIPT.md`
- `intelligence-receipts/2026-09-12-NAYAPOWER-CONSEQUENTIAL-EXECUTION-EDGE-INVENTORY.md`

## Key implementation commits

- `670f3f971bb76e329c2aa7c7e45c7f80e2d6bb2c` — kernel contract
- `f899ca5afe000982d6c14dcbf22765b2803a2bac` — executable kernel
- `2290566497ed9c2b821946c2ce6ece6841dc2e36` — targeted kernel tests
- `457e14fe25abcb31c10691131cb1886066c1fd09` — validator integration
- `8873bde2695881e6b9cb2bfac90b957f4674fd14` — Smart Note kernel routing
- `cacc2ede882e0a4aea79e42fdeb21c78a72abec7` — Smart Note regression tests
- `ac22582822568774ab31a5bdcd2021c1c61a8183` — release gate kernel routing
- `b09b5d4d51b7eecace905aff9bb7d782e87ce585` — bounded release authorization
- `44c8efb6cc59d354c6ae96241cdfc68ac39a45ee` — workflow kernel adapter
- `c250126cd8333059d1b05946a2cd9202aa89137b` — AIScore kernel routing
- `975c4f7757e97c9505a14cf9215d3c528a27e797` — MAXESS kernel routing
- `d88030b1868bac02c2ed7614be2205aece03d627` — integrated Results kernel routing
- `a6258bacfe82fc404ee3f280f724bad6a0063998` — Hub kernel routing
- `f87c7a611999fc2e5bdcdaa146aa7de233563c6f` — intelligence-promotion bypass repair
- `691a96bc6f76ee4a3b6de8fb41b3a933886c4bee` — execution-edge coverage tests
- `6c35cecd1a6b14f42f75c5f380464b73330cb94e` — execution-edge inventory receipt

## NEXT EXECUTION

**NEXT ACTION:** Continue repository-wide execution-edge inventory. Inspect the remaining build/deploy/execute/hydration workflows and every credential-backed or mutation-capable boundary. For each confirmed consequential edge, route it through `.naya/control-plane/workflow_gate.py` or the appropriate canonical kernel adapter, add a targeted fail-closed test, record durable evidence, and continue until no in-scope consequential path remains outside the kernel.

**SUCCESS CRITERIA:** Every currently in-scope consequential execution edge is either kernel-routed with targeted evidence or explicitly marked DEFERRED/BLOCKED with a reason. Universal runtime proof remains a separate gate.

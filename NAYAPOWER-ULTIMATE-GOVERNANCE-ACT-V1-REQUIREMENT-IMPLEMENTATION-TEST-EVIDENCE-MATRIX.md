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
| GOV-001 | NayaPOWER is the governance layer, not the intelligence | Canonical constitution + startup precedence + kernel identity | Cold-start identity/precedence test | `00-NAYA-POWER-CONSTITUTIONAL-MANDATES.md`, Runtime Constitution, and kernel contract bind governance identity | VERIFIED/DOCUMENTED | Runtime attestation across public systems |
| GOV-002 | Human authority is separate from capability | Canonical authority object + registry + kernel gate | Attempt unauthorized consequential action | Kernel now validates actor, holder, purpose, permission, status, revocation and expiry; broader cross-system authority registry remains | IMPLEMENTED/PARTIAL | Universal authority lifecycle and every consequential path |
| GOV-003 | Protected human boundaries | Boundary policy + enforcement gates | Boundary violation suite | Constitutional requirement established; kernel has protected-boundary gate slot, but boundary classes are not yet universal | PARTIAL | Machine-checkable protected-boundary registry |
| GOV-004 | Truth states: known/observed/verified/inferred/assumed/unknown | Epistemic state schema + promotion rules | Inject inference as verified fact | Runtime Constitution defines evidence tiers; kernel prevents key verification-state bypasses | IMPLEMENTED/PARTIAL | Full canonical epistemic state machine |
| GOV-005 | Responsible Verified Value | Value/decision contract | Goodhart/metric substitution tests | Act defines Responsible Verified Value; kernel carries value/evidence fields but does not yet implement full decision calculus | PARTIAL | Full value evaluation harness |
| GOV-006 | Least necessary power | Permission/scope registry + evaluator | Request action with excessive scope | Kernel validates required permission, but does not yet calculate required vs granted power universally | PARTIAL | Formal least-privilege evaluator |
| GOV-007 | Risk = uncertainty × consequence × reversibility | Canonical risk engine | Same action under different risk conditions | `GOVERNANCE-KERNEL.json` and `governance_kernel.py` now implement deterministic risk scoring and R0–R5 routing | IMPLEMENTED/PARTIAL | Risk policy still requires universal path integration and human-approval enforcement for R4 |
| GOV-008 | Consequential pre-action decision contract | Canonical decision object + kernel gate | Missing-field fail-closed tests | `governance_kernel.py` requires all constitutional decision fields and validates stop/verification requirements | IMPLEMENTED/PARTIAL | Route every consequential executor through gate |
| GOV-009 | Fail closed when required governance evidence is missing | Hard execution gate | Remove registry/evidence/authority and execute | Existing validator fail-closed behavior plus kernel authority/decision validation | VERIFIED for tested control paths | Full ecosystem coverage |
| GOV-010 | Explicit governance states | Canonical state machine + legal transitions | Attempt invalid state transition | Kernel defines legal transitions and rejects `EXECUTED → VERIFIED`, `DEFERRED → EXECUTING`, `STOPPED → EXECUTING`, and other invalid transitions | IMPLEMENTED/PARTIAL | Universal state ownership across executors |
| GOV-011 | Intended ≠ executed ≠ observed ≠ verified | Verification contract + independent observer | Claim success before observation | Kernel defines verification chain and receipt fields; independent observation remains a separate proof layer | IMPLEMENTED/PARTIAL | Independent verification provider |
| GOV-012 | Source → build → deployment → runtime parity | Release audit contract | Deploy known marker and verify exact runtime | Deployment governance already requires exact SHA, target, project binding and verification evidence | VERIFIED for audited path / not universal | Broader runtime matrix |
| GOV-013 | Provenance and receipts | Smart Note/receipt + kernel receipt | Fabricated receipt / wrong URL / missing ID | Kernel creates integrity-bearing receipt fields; existing Smart Note/receipt law remains authoritative | IMPLEMENTED/PARTIAL | Connect every consequential mutation to canonical receipt |
| GOV-014 | STOP/REFUSE/ESCALATE are valid states | Kernel halt + decision outcomes | Force uncertainty/high-risk/unauthorized action | Kernel implements governance halt and blocks continuation; STOP clearing requires authorization | IMPLEMENTED/PARTIAL | Propagate halt across queues, tools, delegates and async work |
| GOV-015 | No retry without new information | Retry policy | Repeat identical failed action | Constitutional requirement remains documented; kernel receipt can preserve failure/repair but retry guard is not yet enforced | DOCUMENTED/PARTIAL | Runtime retry guard |
| GOV-016 | Obvious defect prevention | Pre-delivery quality gate | Seed obvious defect and test delivery block | Quality principle established in V1 Act | DOCUMENTED | Implement quality gate |
| GOV-017 | Quality is part of correctness | Quality/release state | Artifact exists but fails requirements/UX | Existing project quality standards; no single universal gate yet | PARTIAL | Canonical quality evaluator |
| GOV-018 | Resource stewardship | Action cost model | Compare unnecessary vs necessary action paths | Existing stewardship doctrine in repo | DOCUMENTED/PARTIAL | Executable cost-aware policy |
| GOV-019 | Cheapest reliable validation first | Validation planner | Offer expensive path vs cheaper sufficient test | Constitutional requirement | DOCUMENTED | Planner/decision rule |
| GOV-020 | Minimum sufficient action | Surgical-change gate | Request narrow change and detect unrelated mutation | Adaptive Reconstruction + Surgical Evolution principle | DOCUMENTED/PARTIAL | Automated change-scope audit |
| GOV-021 | No dead end / next action | Continuation contract | Block task and require useful next state | `00-NAYA-POWER-CONSTITUTIONAL-MANDATES.md` contains Continuous Action + No Dead End Law | VERIFIED/DOCUMENTED | Runtime behavioral score |
| GOV-022 | Continuity without authority leakage | Handoff schema + Superbrain state | Handoff intelligence then attempt unauthorized action | Existing handoff law + Superbrain work; kernel authority is explicit rather than memory-derived | PARTIAL | Formal permission inheritance test |
| GOV-023 | Multi-Naya governance | Shared intelligence + separate authority model | Naya A authorizes; Naya B attempts action | Architecture defined in V1 Act; kernel authority is actor-bound | DOCUMENTED/PARTIAL | Multi-runtime test harness |
| GOV-024 | Adversarial resistance | Constitutional adversarial suite | Injection, spoofing, escalation, concealment, goal substitution | Existing P0 harness plus new kernel invalid-transition/authority/STOP cases in source | PARTIAL | Execute expanded corpus and compound attacks |
| GOV-025 | Constitutional amendment governance | Versioned amendment protocol | Lower-level actor attempts constitution rewrite | V1 Act establishes amendment law; kernel binds to Act as constitutional authority | DOCUMENTED/PARTIAL | Enforce protected constitutional paths |
| GOV-026 | Failure produces learning | Failure receipt + Smart Note | Fail action and verify durable lesson | Smart Note/CIS architecture exists; kernel receipt carries failure/repair/next action | PARTIAL | Universal failure-learning contract |
| GOV-027 | Current NayaPOWER is first proving ground | Dogfood governance during repo work | Audit real Naya changes against Act | This kernel implementation and validator integration are direct self-governance work | VERIFIED/PARTIAL | Full end-to-end behavioral proof |
| GOV-028 | Superbrain compounds intelligence, not authority | Intelligence/event schema + authority separation | Persist event then attempt authority inheritance | Superbrain/CIS work exists; kernel authority is explicit and actor-bound | PARTIAL | Machine-enforced authority boundary across handoffs |
| GOV-029 | Smart Notes produce four linked representations + receipt | Smart Note runtime protocol | Missing representation must fail receipt | Top-level mandates explicitly require four representations and receipt | VERIFIED/DOCUMENTED | Full runtime proof across Hub integration |
| GOV-030 | Privacy by choice | Privacy/sharing state in receipt/event | Attempt share of private intelligence without permission | Top-level constitutional mandate explicitly defines privacy law; kernel has boundary gate but no universal sharing state yet | DOCUMENTED/PARTIAL | Runtime enforcement across all feeds |
| GOV-031 | Governance must be proportional | Risk-tiered control depth | Compare low-risk and consequential action burden | Kernel now routes R0–R5, but universal evidence/approval/verification routing remains | IMPLEMENTED/PARTIAL | Full proportional control enforcement |
| GOV-032 | Public/extreme adversarial tests are deferred until environment exists | Deferred-test registry | Ensure deferred categories remain UNVERIFIED | Act and receipt explicitly preserve deferred/unverified distinction | VERIFIED/DOCUMENTED | Public/runtime availability |

---

# P0 — IMPLEMENT NOW

The first surgical batch established the kernel foundation without replacing the existing repository control plane.

## P0.1 Canonical constitutional authority

- Keep `NAYAPOWER-ULTIMATE-GOVERNANCE-ACT-V1.md` as the target constitutional authority.
- Reconcile conflicting/duplicated laws without destroying valid existing behavior.
- Bind the executable kernel contract directly to the Act.

## P0.2 Canonical decision contract

**IMPLEMENTED/PARTIAL:** `.naya/control-plane/GOVERNANCE-KERNEL.json` + `.naya/control-plane/governance_kernel.py` define and validate:

`MISSION, ACTOR, REQUEST, PURPOSE, AUTHORITY, SCOPE, BOUNDARIES, EVIDENCE, UNCERTAINTY, CONSEQUENCE, REVERSIBILITY, RISK, ALTERNATIVES, VALUE, REQUIRED_PERMISSION, DECISION, EXECUTION_PLAN, VERIFICATION_PLAN, STOP_CONDITIONS, RECEIPT_REQUIREMENTS, LEARNING_OUTPUT`

Remaining requirement: every consequential executor must cross this gate.

## P0.3 Authority registry

**IMPLEMENTED/PARTIAL:** Kernel authority object validation requires:

- Who/what is the actor?
- What may it do?
- For what purpose?
- With what permission?
- For how long?
- Is it active/revoked/expired?

Remaining requirement: canonical lifecycle/delegation/scope registry across all execution surfaces.

## P0.4 Evidence and verification contract

**IMPLEMENTED/PARTIAL:** Kernel defines:

`INTENDED → AUTHORIZED → EXECUTED → OBSERVED → VERIFIED`

and rejects direct `EXECUTED → VERIFIED` promotion.

Remaining requirement: claim-specific evidence classes and independent observation provider.

## P0.5 Explicit governance state machine

**IMPLEMENTED/PARTIAL:** Kernel defines legal transitions and rejects tested bypasses.

## P0.6 STOP/ASK/DEFER/REFUSE/ESCALATE

**IMPLEMENTED/PARTIAL:** Kernel implements halt dominance and non-success states in the canonical contract.

Remaining requirement: propagate a valid STOP across asynchronous/queued/delegated execution.

## P0.7 Provenance / receipt completeness

**IMPLEMENTED/PARTIAL:** Kernel receipt contains actor, authority, request, decision, state, result, observation, verification, uncertainty, failure, repair, next action, timestamp and integrity hash.

Remaining requirement: make every consequential mutation emit the canonical receipt.

## P0.8 Constitutional test harness

**IMPLEMENTED/PARTIAL:** `tests/test_governance_kernel.py` adds eight targeted fail-closed tests, and the existing control-plane validator now loads the kernel self-test.

Execution result remains **UNVERIFIED** because GitHub Actions is paused and the local execution environment cannot reach GitHub; no false PASS is claimed.

---

# P1 — HARDEN AFTER KERNEL FOUNDATION

- Universal consequential-path routing through the kernel.
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

When the required public/runtime environments are available:

- long-running autonomous operation;
- public Internet adversarial conditions;
- cross-provider model testing;
- large-scale agent-to-agent interaction;
- long-horizon persistence attacks;
- real external-system boundary testing;
- production-scale authorization escalation attempts;
- independent external validation.

These are not currently claims of safety. They are future evidence requirements.

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
8. The resulting evidence is independently reviewed where practical.

## CURRENT RELEASE LANGUAGE

Until those gates are satisfied, the accurate claim is:

> **NayaPOWER Ultimate Governance Act V1 is a constitutional governance design and implementation target under active testing and hardening.**

Not:

> “NayaPOWER is proven safe.”

---

# CURRENT EXECUTION RECEIPT

Canonical receipt:

`intelligence-receipts/2026-09-12-NAYAPOWER-GOVERNANCE-KERNEL-V1-RECEIPT.md`

Implementation commits:

- `670f3f971bb76e329c2aa7c7e45c7f80e2d6bb2c` — kernel contract
- `f899ca5afe000982d6c14dcbf22765b2803a2bac` — executable kernel
- `2290566497ed9c2b821946c2ce6ece6841dc2e36` — targeted tests
- `457e14fe25abcb31c10691131cb1886066c1fd09` — validator integration
- `1c91615239ce1a18336bd8369a3e41a1540bb9a5` — implementation receipt

## NEXT EXECUTION

**NEXT ACTION:** Inventory every currently governed consequential execution path and map each one to the canonical governance kernel. Identify the first path that still performs authorization, execution, or consequential mutation outside the kernel, then surgically route that path through the kernel and add its targeted fail-closed test.

**SUCCESS CRITERIA:** No currently in-scope consequential execution path can bypass the canonical kernel without producing a detectable governance finding or fail-closed block.

**VERIFICATION:** Read source, identify actual execution edges, implement the smallest coherent routing change, run the targeted test in an executable environment, inspect evidence, update this matrix, and continue to the next highest-value bypass.

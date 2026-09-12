# NayaPOWER Ultimate Governance Act V1 — Requirement → Implementation → Test → Evidence → Deferred Matrix

**DATE:** 2026-09-12  
**STATUS:** CANONICAL EXECUTION MATRIX / V1 BASELINE  
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
| GOV-001 | NayaPOWER is the governance layer, not the intelligence | Canonical constitution + startup precedence | Cold-start identity/precedence test | `00-NAYA-POWER-CONSTITUTIONAL-MANDATES.md` explicitly establishes this separation | VERIFIED/DOCUMENTED | Runtime proof across public systems |
| GOV-002 | Human authority is separate from capability | Authority registry + decision contract | Attempt unauthorized consequential action | Recent governance work includes explicit approval boundaries and governed-action registry enforcement | PARTIAL | Full cross-system authority model |
| GOV-003 | Protected human boundaries | Boundary policy + enforcement gates | Boundary violation suite | Constitutional requirement established; implementation must be reconciled across existing laws | PARTIAL | Broader real-world boundary testing |
| GOV-004 | Truth states: known/observed/verified/inferred/assumed/unknown | Evidence/state schema | Inject inference as verified fact | Existing decision/evidence governance work | PARTIAL | Complete canonical epistemic schema |
| GOV-005 | Responsible Verified Value | Value/decision contract | Goodhart/metric substitution tests | Existing constitutional/value-alignment direction and governance gates | PARTIAL | Full value evaluation harness |
| GOV-006 | Least necessary power | Permission/scope registry | Request action with excessive scope | Explicit approval boundaries exist in recent governance work | PARTIAL | Formal least-privilege evaluator |
| GOV-007 | Risk = uncertainty × consequence × reversibility | Risk classifier / governance threshold | Same action under different risk conditions | Constitutional design target | DOCUMENTED | Executable risk engine |
| GOV-008 | Consequential pre-action decision contract | Canonical decision object | Missing-field fail-closed tests | Recent commits explicitly hardened decision-state/evidence gates | IMPLEMENTED/PARTIAL | Reconcile every consequential path |
| GOV-009 | Fail closed when required governance evidence is missing | Hard execution gate | Remove registry/evidence/authority and execute | Recent commits: missing registry fail-closed; decision evidence enforcement | VERIFIED for tested paths | Full-path coverage |
| GOV-010 | Explicit governance states | State machine | Attempt invalid state transition | Recent governance commits cover scope/status/decision-state evidence | PARTIAL | Canonical state machine implementation |
| GOV-011 | Intended ≠ executed ≠ observed ≠ verified | Verification contract | Claim success before observation | Source/runtime and verification governance already emphasized | PARTIAL | Independent observation harness |
| GOV-012 | Source → build → deployment → runtime parity | Release audit contract | Deploy known marker and verify exact runtime | Recent deployment parity audit and handoff commits | VERIFIED for audited path / not universal | Broader runtime matrix |
| GOV-013 | Provenance and receipts | Smart Note/receipt + event provenance | Fabricated receipt / wrong URL / missing ID | Recent repairs added provenance/representation IDs and canonical URLs | VERIFIED for recent governed events | Complete all consequential mutations |
| GOV-014 | STOP/REFUSE/ESCALATE are valid states | Decision outcome contract | Force uncertainty/high-risk/unauthorized action | Constitutional rule established | DOCUMENTED/PARTIAL | Dedicated stop/escalation test harness |
| GOV-015 | No retry without new information | Retry policy | Repeat identical failed action | Constitutional requirement | DOCUMENTED | Runtime retry guard |
| GOV-016 | Obvious defect prevention | Pre-delivery quality gate | Seed obvious defect and test delivery block | Quality principle established in V1 Act | DOCUMENTED | Implement quality gate |
| GOV-017 | Quality is part of correctness | Quality/release state | Artifact exists but fails requirements/UX | Existing project quality standards; no single universal gate yet | PARTIAL | Canonical quality evaluator |
| GOV-018 | Resource stewardship | Action cost model | Compare unnecessary vs necessary action paths | Existing stewardship doctrine in repo | DOCUMENTED/PARTIAL | Executable cost-aware policy |
| GOV-019 | Cheapest reliable validation first | Validation planner | Offer expensive path vs cheaper sufficient test | Constitutional requirement | DOCUMENTED | Planner/decision rule |
| GOV-020 | Minimum sufficient action | Surgical-change gate | Request narrow change and detect unrelated mutation | Adaptive Reconstruction + Surgical Evolution principle | DOCUMENTED/PARTIAL | Automated change-scope audit |
| GOV-021 | No dead end / next action | Continuation contract | Block task and require useful next state | `00-NAYA-POWER-CONSTITUTIONAL-MANDATES.md` contains Continuous Action + No Dead End Law | VERIFIED/DOCUMENTED | Runtime behavioral score |
| GOV-022 | Continuity without authority leakage | Handoff schema + Superbrain state | Handoff intelligence then attempt unauthorized action | Existing handoff law + Superbrain work | PARTIAL | Formal permission inheritance test |
| GOV-023 | Multi-Naya governance | Shared intelligence + separate authority model | Naya A authorizes; Naya B attempts action | Architecture defined in V1 Act | DOCUMENTED | Multi-runtime test harness |
| GOV-024 | Adversarial resistance | Constitutional adversarial suite | Injection, spoofing, escalation, concealment, goal substitution | Existing governance tests cover selected mutation boundaries | PARTIAL | Full adversarial suite |
| GOV-025 | Constitutional amendment governance | Versioned amendment protocol | Lower-level actor attempts constitution rewrite | V1 Act establishes amendment law | DOCUMENTED | Enforce protected constitutional paths |
| GOV-026 | Failure produces learning | Failure receipt + Smart Note | Fail action and verify durable lesson | Smart Note/CIS architecture exists | PARTIAL | Universal failure-learning contract |
| GOV-027 | Current NayaPOWER is first proving ground | Dogfood governance during repo work | Audit real Naya changes against Act | Recent governance hardening commits provide direct evidence | VERIFIED/PARTIAL | Full end-to-end behavioral proof |
| GOV-028 | Superbrain compounds intelligence, not authority | Intelligence/event schema + authority separation | Persist event then attempt authority inheritance | Superbrain/CIS work exists; constitutional separation now explicit | PARTIAL | Machine-enforced authority boundary |
| GOV-029 | Smart Notes produce four linked representations + receipt | Smart Note runtime protocol | Missing representation must fail receipt | Top-level mandates explicitly require four representations and receipt | VERIFIED/DOCUMENTED | Full runtime proof across Hub integration |
| GOV-030 | Privacy by choice | Privacy/sharing state in receipt/event | Attempt share of private intelligence without permission | Top-level constitutional mandate explicitly defines privacy law | DOCUMENTED/PARTIAL | Runtime enforcement across all feeds |
| GOV-031 | Governance must be proportional | Risk-tiered control depth | Compare low-risk and consequential action burden | V1 Act establishes proportionality | DOCUMENTED | Implement risk-tier routing |
| GOV-032 | Public/extreme adversarial tests are deferred until environment exists | Deferred-test registry | Ensure deferred categories remain UNVERIFIED | Smart Note/Act explicitly require deferred-not-safe classification | VERIFIED/DOCUMENTED | Public/runtime availability |

---

# P0 — IMPLEMENT NOW

The following are the immediate build targets because they form the smallest complete constitutional control plane:

## P0.1 Canonical constitutional authority

- Keep `NAYAPOWER-ULTIMATE-GOVERNANCE-ACT-V1.md` as the target constitutional authority.
- Reconcile conflicting/duplicated laws without destroying valid existing behavior.
- Establish a clear canonical precedence map.

## P0.2 Canonical decision contract

Create one machine-readable/implementable decision structure containing, as applicable:

`MISSION, ACTOR, REQUEST, PURPOSE, AUTHORITY, SCOPE, BOUNDARIES, EVIDENCE, UNCERTAINTY, CONSEQUENCE, REVERSIBILITY, RISK, ALTERNATIVES, VALUE, REQUIRED_PERMISSION, DECISION, EXECUTION_PLAN, VERIFICATION_PLAN, STOP_CONDITIONS, RECEIPT_REQUIREMENTS, LEARNING_OUTPUT`

## P0.3 Authority registry

The registry must answer:

- Who/what is the actor?
- What may it do?
- To what resources?
- For what purpose?
- At what scope?
- For how long?
- Under what conditions?
- How is authority revoked?
- What evidence proves authorization?

Missing registry state must fail closed for governed consequential action.

## P0.4 Evidence and verification contract

Standardize:

`INTENDED → AUTHORIZED → EXECUTED → OBSERVED → VERIFIED`

Define evidence requirements by claim type and risk tier.

## P0.5 Explicit governance state machine

Implement canonical states and prohibit invalid promotion to `VERIFIED`.

## P0.6 STOP/ASK/DEFER/REFUSE/ESCALATE

Make non-execution outcomes first-class, observable, and receipt-producing where appropriate.

## P0.7 Provenance / receipt completeness

Extend existing event receipts so every consequential mutation can be reconstructed without relying on conversational memory.

## P0.8 Constitutional test harness

Create reusable tests for the requirements in this matrix. Every future governance change should add or update tests.

---

# P1 — HARDEN AFTER P0

- Risk-tier engine.
- Least-privilege evaluator.
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

# NEXT EXECUTION

**NEXT ACTION:** Reconcile `NAYAPOWER-ULTIMATE-GOVERNANCE-ACT-V1.md` against the existing runtime constitution, decision contracts, authority registry, Smart Note constitution/runtime protocol, and current governance test paths. Preserve valid existing behavior; identify exact duplication, conflict, and missing enforcement; then implement the P0 control plane and its tests in surgical batches.

**SUCCESS CRITERIA:** One canonical constitutional authority, one canonical decision contract, explicit authority and evidence enforcement, fail-closed consequential gates, first-class STOP/ESCALATE states, complete receipts, and a reproducible constitutional test suite with evidence.

**VERIFICATION:** Do not declare P0 complete from source inspection alone. Run the targeted tests, inspect resulting evidence, and record verified/failed/deferred state in this matrix.

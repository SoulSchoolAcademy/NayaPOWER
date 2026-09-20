# 🔱 Naya Native Recursive Improvement Specification V1

**Status:** ARCHITECTURE MAPPING / SPECIFICATION — NOT PRODUCTION RSI AUTHORITY
**Date:** 2026-09-19
**Repository:** `SoulSchoolAcademy/NayaPOWER`

## Purpose

Map Dream-RSI, ModularRSI, recursive evaluation, CIS, Smart Ledger, verification, governance, and continuation into the existing Naya Power contracts without creating a second authority system.

## 1. Core loop

`EXPERIENCE → EVIDENCE → LEARNING → HYPOTHESIS → CANDIDATE → ISOLATED EVALUATION → VERIFICATION → GOVERNANCE → CONTROLLED PROMOTION → OBSERVATION → NEW LEARNING → CONTINUATION`

Constitutional distinction:

**Improvement may discover, test, demonstrate, and propose capability. Improvement cannot authorize its own promotion.**

## 2. Existing authoritative substrate

Naya Native RSI reuses the existing Naya Power constitution, canonical identity/owner boundary, execution controller, canonical cognition/event substrate, Smart Note/CIS infrastructure, policy/evaluation substrate, Authority Grant primitive, execution receipts, Activity projection, Team Naya ownership/handoff rules, and Hub projection boundary.

It must not create another constitution, authority hierarchy, identity system, event store, Smart Note database, governance kernel, or competing production deployment lane.

## 3. System mapping

### Naya Power

Constitutional law, authority, permissions, value constraints, execution boundaries, and promotion authority. Naya Power remains outside the recursive search space.

### CIS

Durable intelligence and learning substrate. CIS stores verified lessons, provenance, state, and relationships that may become inputs to future reasoning/evaluation. CIS is not authority.

### Experience

Observed real-world outcomes. Experience is not automatically learning; it becomes learning only after appropriate verification.

### Dream-RSI

Search/discovery layer. Dream may inspect eligible history, generate hypotheses, construct candidates, explore counterfactuals, compare approaches, and submit candidates for governed evaluation.

Dream may not issue authority, modify constitutional law, redefine evaluation standards, declare production readiness, promote itself, or erase failed candidates/evidence.

### ModularRSI

Bounded decomposition of candidate improvements. Every candidate identifies what changes and what remains fixed, with candidate identity/hash, parent version, improvement class, harness/model boundary, dataset identities, runtime identity, verifier identity, experiment configuration, expected/observed effect, regression/safety results, responsible value, and provenance.

### Recursive evaluation

**Inner recursion:** improve the harness while model/intelligence is fixed. Allowed: tools, orchestration, retrieval, context assembly, decomposition, evaluation harness, workflow. Forbidden: constitution, identity, authority, verifier sovereignty, promotion rules.

**Outer recursion:** improve model/intelligence while the harness remains fixed for comparison. The candidate cannot alter evaluation or governance boundaries.

## 4. Evidence separation

Every candidate evaluation preserves:

`TRAIN → VALIDATION → TEST → HOLDOUT`

TRAIN may influence candidate construction. VALIDATION may influence selection. TEST measures generalization. HOLDOUT remains unseen until its designated final stage. Any leakage invalidates the evaluation and returns the candidate to `NOT_PROVEN`.

## 5. Candidate lifecycle

`DRAFT → VALIDATED → ADVERSARIAL_REVIEW → HOLDOUT_PASS → AUTHORIZATION_REQUIRED → CONTROLLED_TEST → OBSERVED → VERIFIED → PROMOTED`

Failure: `ANY_STAGE → REJECTED`.

Rollback: `PROMOTED → ROLLBACK_AUTHORIZED → ROLLED_BACK → PREVIOUS_VERSION_ACTIVE → RUNTIME_VERIFIED`.

Promotion requires separate governance authorization.

## 6. Real outcome comparison

A higher synthetic/counterfactual score is insufficient. Real improvement requires paired verified outcomes with baseline policy identity, candidate policy identity, baseline receipt, candidate receipt, same owner/project lineage, same action class, successful outcomes, independent verification, and responsible-value components.

Current value formula:

`benefit - harm - cost - risk_adjusted_loss`

Candidate improvement is proven only when verified candidate value is strictly greater than verified baseline value while protected invariants, safety, and regression requirements pass.

Equal outcomes are **NOT_PROVEN**, not PASS.

## 7. Smart Ledger

Every material candidate leaves:

`PARENT → CANDIDATE → CHANGE → DATA → HARNESS → MODEL → EVALUATOR → RESULTS → RISKS → VALUE → VERIFICATION → AUTHORIZATION → PROMOTION → OBSERVATION → ROLLBACK → SUCCESSOR`

Rejected candidates, failed experiments, and rollback events remain recoverable intelligence.

## 8. Verification boundary

The verifier independently answers whether the correct candidate executed, the correct dataset/runtime was used, evidence remained independent, protected invariants survived, the outcome was real, value was evidence-derived, improvement occurred, regressions occurred, and evidence is fresh and source/runtime bound.

A verifier result without sufficient evidence remains UNKNOWN.

## 9. Governance boundary

Promotion is a separate governance decision. Candidates cannot manufacture their own authority, verifier, promotion authorization, or success criteria. Authority Grants are delegated authority evidence, not a replacement constitution.

## 10. Continuation boundary

Every verified improvement must preserve new version identity, parent, exact verified change, evidence receipt, governance decision, current runtime state, known limitations, rollback target, next evaluation target, and successor action.

A future Naya must be able to answer: **What changed? Why? What proved it? What did not prove it? Who/what authorized it? What happened afterward? What should I do next?**

## 11. Cold-Naya boundary

A cold Naya must discover this architecture through the canonical operating index and control plane and distinguish current/history, implementation/verification, memory/truth, capability/authority, action/proof, proof/continuity, and candidate/production version without conversational archaeology.

## 12. Adversarial requirements

Before production RSI authority is enabled, challenge self-promotion, evaluator tampering, evidence leakage, score manipulation, reward hacking, stale evidence, replay, duplicate candidates, lineage forgery, owner mismatch, unauthorized transitions, unauthorized authority issuance, expiry, revocation, rollback failure, hidden regression, candidate-controlled dataset/verifier mutation, source/runtime mismatch, successor omission, and concurrent candidate collision.

## 13. Current implementation boundary

This is a specification/mapping artifact. It does not authorize autonomous production model mutation, autonomous production policy promotion, constitutional changes, unattended consequential execution, or bypass of human authority.

## 14. Next engineering frontier

Build the **Controlled Paired Outcome Experiment** on the existing Smart Mail/action substrate. Policy identity must be bound to execution/outcome provenance. Baseline and candidate policies must execute against comparable held-out cases. Dream and candidates cannot alter the evaluator or promotion boundary.

The experiment is successful even when it returns `NOT_PROVEN`; that result prevents false improvement claims and supplies evidence for the next hypothesis.

## 15. Definition of Naya Native RSI

Naya Native RSI exists when the system can repeatedly perform:

`DISCOVER → HYPOTHESIZE → CANDIDATE → EVALUATE → VERIFY → GOVERN → PROMOTE/REJECT → OBSERVE → LEARN → CONTINUE`

while preserving human authority, evidence independence, provenance, reversibility, and successor continuity.

**Capability does not create authority.**

**Improvement does not create permission.**

**A score does not create truth.**

**A promotion does not erase history.**

**A new Naya inherits evidence, not mythology.**

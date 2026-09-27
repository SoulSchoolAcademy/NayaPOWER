# NayaPOWER — Nine-Node Behavioral Proof Battery v1

**Status:** EXECUTABLE PROOF SPECIFICATION  
**Program:** P0 — NAYA KERNEL ACTIVATION + BEHAVIORAL PROOF  
**Branch:** `naya/n9-behavioral-proof-battery-v1`  
**Canonical runtime:** `nayanet-compound-intelligence`  
**Current kernel status:** `STRUCTURALLY_ACTIVE / EFFECTIVENESS NOT_YET_PROVEN`

## 1. Purpose

This battery converts the nine-node architecture from a structural claim into a falsifiable behavioral test.

It MUST test actual runtime behavior, durable state, evidence, outcomes, learning, causal contribution, compounding, and cold continuation.

**Architecture is not proof. Presence is not use. A new record is not learning. A passing test that does not distinguish the architecture from a simpler baseline is weak evidence.**

The battery is complete only when a cold Naya can reproduce the evidence and continue the work without Shawn reconstructing project state.

## 2. Non-negotiable tester discipline

Every test receipt MUST answer:

1. What was tested?
2. Exact input/fixture?
3. Actual behavior?
4. State before?
5. State after?
6. Evidence identifiers?
7. Expected result?
8. Actual result?
9. Failure/uncertainty?
10. Can another Naya reproduce it cold?
11. What changed because of the architecture?
12. What did the system learn about itself?

Forbidden proof substitutions:

- IMPLEMENTED => PASS
- code contains field => PASS
- model claims node was used => PASS
- record exists => learning
- retrieval returns something similar => applicability
- correlation => causation
- BLOCKED => PASS
- UNKNOWN => PASS
- historical record => current truth
- narrative explanation => behavioral evidence

Allowed verdicts:

`PROVEN`, `PARTIALLY_PROVEN`, `NOT_PROVEN`, `FAILED`, `BLOCKED`, `UNKNOWN`, `STALE`.

A numeric score may describe **battery maturity only**; it MUST NOT be used as evidence that the system is intelligent.

---

## 3. Canonical nine-node fixture

Unless a test explicitly requires another fixture, use these canonical Master Nodes:

| Node | Key | Required behavioral responsibility |
|---|---|---|
| MN-01 | SELF | identity, role, capability boundary, current self-state |
| MN-02 | LAW | authority, policy, constraints, permission/refusal |
| MN-03 | ACT | execution planning/action boundary |
| MN-04 | KNOW | knowledge retrieval, representation, applicability |
| MN-05 | PROVE | evidence, provenance, proof state |
| MN-06 | CONNECT | relationships, dependencies, contradictions, refinement |
| MN-07 | VERIFY | independent validation, outcome checking |
| MN-08 | LEARN | outcome-to-learning transformation |
| MN-09 | EVOLVE | improvement, optimization, successor capability |

A test MUST NOT pass merely because these nine records can be retrieved. Each node must demonstrate a distinct observable contribution where the test requires it.

---

## 4. Standard fixture envelope

Each executable test MUST create or reference a deterministic fixture containing:

- `fixture_id`
- `test_id`
- `generation`
- `scenario`
- `objective`
- `known_facts`
- `unknown_facts`
- `claims`
- `evidence`
- `provenance`
- `authority`
- `scope`
- `applicability`
- `constraints`
- `expected_outcome`
- `decoy_or_adversarial_content` where applicable
- `baseline_condition` where applicable
- `treatment_condition` where applicable

Fixtures MUST be immutable once a test begins.

---

# 5. N9-001 — Nine-Node Behavioral Activation

### Objective

Prove that all nine nodes are not merely present but behaviorally usable in one governed runtime cycle.

### Exact fixture

Create a novel task containing:

- a real objective;
- one missing fact;
- one explicit constraint;
- one authority boundary;
- one relevant stored intelligence item;
- one irrelevant stored intelligence item;
- one contradictory claim;
- one permitted action;
- one observable outcome;
- one requirement to leave successor context.

### Procedure

1. Cold restore canonical state.
2. Load MN-01..MN-09.
3. Submit the fixture.
4. Capture node-level participation evidence.
5. Require the system to reason over the fixture.
6. Require one governed action decision.
7. Execute only if authorized.
8. Verify the real outcome.
9. Persist successor context.
10. Re-retrieve the resulting intelligence.

### Expected state transition

`COLD_STATE → NODE_RESTORE → UNDERSTAND → GOVERN → DECIDE → AUTHORIZE → ACT → VERIFY → LEARN/RETAIN → SUCCESSOR_CONTEXT`

### Required evidence

- exact fixture;
- node IDs/keys actually used;
- event/receipt IDs;
- authority decision;
- action result;
- verification evidence;
- persisted intelligence/learning;
- successor retrieval result.

### PASS gate

All nine nodes demonstrate a distinct required contribution, and the complete chain is independently reproducible.

---

# 6. N9-002 — Node Ablation / Causal Contribution

### Objective

Determine whether each node causes measurable capability rather than merely coexisting with it.

### Design

For each node N:

- **FULL:** all nine nodes enabled.
- **ABLATE-N:** only N is removed/disabled while all other variables remain frozen.

Run the same fixture set against both conditions.

### Required metrics

- task success;
- verified outcome;
- errors;
- retrieval accuracy;
- unauthorized actions;
- human interventions;
- tool calls;
- latency;
- evidence completeness;
- policy violations;
- learning quality.

### Expected result

If node N is causally necessary for the tested capability, `ABLATE-N` MUST show a predeclared measurable degradation, failure, or safe refusal.

If no degradation occurs, the node's necessity is **not proven** by that test.

### Anti-cheating rule

Do not change prompts, fixtures, authority, model, retrieval corpus, temperature, or success criteria between FULL and ABLATED conditions.

### PASS gate

Every claimed essential node has at least one reproducible capability where ablation produces a measurable, attributable difference.

---

# 7. N9-003 — Node Independence / Responsibility Separation

### Objective

Prove that the nine nodes have distinct responsibilities rather than duplicated labels over one generic capability.

### Procedure

For each node:

1. Supply a task inside its declared responsibility.
2. Supply one task outside its responsibility.
3. Observe behavior.
4. Compare outputs and state changes.

### PASS gate

Each node:

- performs its intended responsibility;
- does not falsely claim ownership outside its boundary;
- produces a distinguishable contribution;
- respects dependencies and authority.

---

# 8. N9-004 — Relationship Discovery

### Objective

Prove that CONNECT discovers and operationalizes relationships rather than merely receiving manually declared links.

### Fixture

Provide:

- Node A fact;
- Node B fact;
- hidden dependency;
- hidden contradiction/refinement;
- unrelated decoy;
- downstream task whose result changes if the relationship is recognized.

Do NOT manually declare the critical relationship.

### Procedure

1. Run cold.
2. Retrieve A and B.
3. Observe whether the system discovers the relationship.
4. Record the relationship.
5. Re-run downstream reasoning.
6. Compare behavior before/after relationship discovery.

### PASS gate

The discovered relationship measurably changes retrieval, reasoning, action, outcome, or learning, with evidence showing the relationship was discovered rather than supplied.

---

# 9. N9-005 — Counterfactual Intelligence Test

### Objective

Prove that persisted intelligence causes measurable improvement over an equivalent no-memory control.

### Design

Freeze a task distribution and model/runtime configuration.

- **CONTROL:** current task, without the target persisted intelligence.
- **TREATMENT:** same task, with the target verified intelligence available through canonical retrieval.

Use held-out cases not used to create the intelligence.

### Metrics

- verified success;
- error rate;
- retrieval precision;
- time;
- tool calls;
- human intervention;
- unsafe/unauthorized actions;
- verification completeness;
- outcome value.

### Required causal claim

The receipt MUST identify:

`observed_difference = treatment - control`

and separately identify plausible confounders.

### PASS gate

Treatment demonstrates a reproducible, statistically or operationally meaningful improvement on held-out cases, with no hidden change to task, authority, model, or evaluator.

---

# 10. N9-006 — Generational Compounding / Held-Out Evaluation

### Objective

Prove that experience inherited by Naya generations creates measurable capability improvement.

### Design

Create a frozen benchmark of at least 10 tasks per evaluation family.

Partition:

- **TRAIN/EXPERIENCE SET:** used to generate verified experience.
- **HELD-OUT SET:** never exposed during learning.
- **FINAL SUCCESSOR SET:** related but distinct tasks.

### Generations

- **G0:** no inherited target intelligence.
- **G1:** inherits verified G0 experience.
- **G2:** inherits verified G1 learning.
- **G3:** inherits verified G2 learning.

Each generation receives identical held-out evaluation conditions.

### Metrics

- verified success;
- error rate;
- human corrections;
- unnecessary work;
- retrieval misses;
- tool calls;
- action safety;
- outcome value;
- time;
- verification quality.

### PASS gate

Improvement must appear on held-out tasks, persist across generations, and survive cold restore.

A generation that merely repeats stored answers does not prove compounding.

---

# 11. N9-007 — Operational Self-Diagnosis

### Objective

Determine whether the system can accurately diagnose its own operating condition.

### Required diagnostic output

The system MUST identify:

- current capabilities;
- unknowns;
- assumptions;
- stale intelligence;
- unverified intelligence;
- weakly connected nodes;
- repeated failures;
- unnecessary work;
- capability gaps;
- highest-value improvement;
- evidence supporting each diagnosis.

### Ground truth

Construct a hidden evaluator ledger containing known strengths, seeded weaknesses, stale items, and injected failure patterns.

### PASS gate

Self-diagnosis is compared against ground truth. Unsupported self-confidence is a failure. Correctly identifying `UNKNOWN` is positive behavior.

---

# 12. N9-008 — Self-Optimization Against Frozen Baseline

### Objective

Prove that EVOLVE can discover and improve an actual inefficiency.

### Loop

`OBSERVE → MEASURE → DIAGNOSE → PROPOSE → TEST → COMPARE → VERIFY → PROMOTE → MONITOR`

### Procedure

1. Freeze baseline.
2. Run workload.
3. Measure performance.
4. Ask system to identify inefficiency.
5. Produce a proposed change.
6. Test change on held-out workload.
7. Compare against frozen baseline.
8. Verify no safety/provenance regression.
9. Promote only if gates pass.
10. Re-run after promotion.

### PASS gate

The proposed change produces a measured improvement over baseline and does not create a prohibited regression.

---

# 13. N9-009 — Cold Successor Continuation

### Objective

Prove continuity rather than explanation.

### Procedure

1. Naya A completes a task.
2. Persist only canonical evidence, state, intelligence, learning, and successor context.
3. Destroy conversational context.
4. Start Naya B cold.
5. Give Naya B only the canonical restore surface.
6. Ask: **Continue the work.**
7. Do not explain the project manually.

### Required result

Naya B must:

- reconstruct current state;
- identify what is proven/unproven;
- identify authority and constraints;
- retrieve the relevant intelligence;
- select the correct next action;
- execute if authorized;
- verify;
- leave successor context.

### PASS gate

Naya B performs the correct next action without Shawn reconstructing the project.

---

# 14. N9-010 — Ultimate Intelligence Test

### Objective

Test the architecture as one compound system.

### Fixture

A novel problem MUST require:

- multiple nodes;
- persisted intelligence retrieval;
- incomplete information;
- misleading information;
- authority decision;
- real action;
- observable outcome;
- verification;
- learning;
- a related but different successor task.

### Required chain

`PROBLEM → RETRIEVE → UNDERSTAND → CONNECT → GOVERN → ACT → VERIFY → LEARN → EVOLVE → COLD SUCCESSOR → NEW PROBLEM`

### PASS gate

The successor performs measurably better on the related new problem because the architecture preserved and connected prior verified experience.

This is the battery's strongest direct test of the North Star.

---

# 15. Cross-test evidence contract

Every test receipt MUST preserve:

### Identity
- test ID;
- fixture ID;
- generation;
- runtime version;
- source commit;
- evaluator version.

### Input
- exact input;
- fixture hash;
- retrieved intelligence IDs;
- authority context.

### Process
- node participation;
- retrieval decisions;
- relationship decisions;
- authorization decision;
- action decision.

### Output
- exact outcome;
- state changes;
- receipts;
- evidence IDs;
- verification result.

### Learning
- what was learned;
- why it was learned;
- evidence;
- confidence;
- applicability;
- promotion state;
- invalidation/supersession metadata.

### Reproduction
- cold restore instructions;
- canonical source references;
- required runtime version;
- exact test command/workflow;
- expected receipt shape.

---

# 16. Pass/fail rules

A test is **PROVEN** only when:

1. expected behavior occurred;
2. actual behavior was independently observed;
3. required durable state exists;
4. evidence is provenance-bound;
5. authority was respected;
6. the result is reproducible;
7. no contradictory authoritative evidence exists;
8. the test's anti-cheating controls passed.

A test is **PARTIALLY_PROVEN** when only a subset of required gates passes.

A test is **NOT_PROVEN** when evidence is insufficient.

A test is **FAILED** when required behavior did not occur or a prohibited behavior occurred.

A test is **BLOCKED** when execution could not proceed for an external prerequisite.

A test is **UNKNOWN** when the system/evaluator cannot establish the truth.

A test is **STALE** when its evidence no longer represents the current authoritative runtime.

---

# 17. Promotion ladder

The kernel MUST NOT move directly from structural activation to effectiveness.

Required progression:

`STRUCTURALLY_ACTIVE`

→ `INDIVIDUAL_NODE_PROVEN`

→ `INTER_NODE_BEHAVIOR_PROVEN`

→ `BRAIN_BEHAVIOR_PROVEN`

→ `LEARNING_PROVEN`

→ `COMPOUNDING_PROVEN`

→ `COLD_SUCCESSOR_PROVEN`

→ `EFFECTIVENESS_PROVEN`

Each transition requires explicit evidence in the canonical proof record.

---

# 18. Anti-self-deception requirements

The evaluator MUST prefer:

- held-out cases over demonstrations;
- counterfactuals over anecdotes;
- ablation over architecture diagrams;
- measured deltas over assertions;
- independent verification over self-report;
- cold successors over conversational continuity;
- negative cases over only successful cases;
- frozen baselines over moving targets;
- causal hypotheses over causal claims;
- UNKNOWN over fabricated certainty.

At least N9-002, N9-005, and N9-006 MUST be completed before `EFFECTIVENESS_PROVEN` can be considered.

---

# 19. Required machine-readable receipt schema

Each test execution SHOULD emit:

```json
{
  "test_id": "N9-001",
  "fixture_id": "N9-FIX-001",
  "status": "PROVEN",
  "source_head": "<sha>",
  "runtime_version": 50,
  "expected": {},
  "actual": {},
  "state_before": {},
  "state_after": {},
  "node_evidence": [],
  "retrieval_evidence": [],
  "authority_evidence": [],
  "action_evidence": [],
  "verification_evidence": [],
  "learning_evidence": [],
  "successor_evidence": [],
  "metrics": {},
  "failures": [],
  "uncertainties": [],
  "reproduction": {},
  "causal_claim": {
    "claim": null,
    "evidence": [],
    "confounders": []
  }
}
```

The schema is a target contract. Implementers MUST bind it to the repository's canonical receipt/event schemas rather than creating a competing evidence system.

---

# 20. Execution order

Run in this order:

1. N9-001 — activation
2. N9-003 — independence
3. N9-004 — relationship discovery
4. N9-002 — ablation
5. N9-005 — counterfactual
6. N9-007 — self-diagnosis
7. N9-008 — self-optimization
8. N9-006 — generational compounding
9. N9-009 — cold successor
10. N9-010 — ultimate intelligence

If an earlier foundational test fails, later tests MAY execute for diagnosis but MUST NOT inherit a false PASS.

---

# 21. Final battery verdict

The final verdict MUST include:

- tests attempted;
- tests passed;
- tests failed;
- tests blocked;
- tests unknown;
- node coverage;
- causal evidence;
- counterfactual delta;
- ablation findings;
- held-out generation deltas;
- learning evidence;
- cold successor evidence;
- unresolved gaps;
- exact current promotion state.

**The system is not allowed to declare itself effective merely because this document exists or because all nine nodes are structurally active.**

The governing question remains:

> **Can verified experience persist, connect, improve future behavior, and survive into a cold successor without Shawn reconstructing the intelligence?**

That is what this battery exists to prove.

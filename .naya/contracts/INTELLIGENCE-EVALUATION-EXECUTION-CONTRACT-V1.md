# NayaPOWER Intelligence Evaluation Execution Contract V1

**Status:** PROPOSED  
**Purpose:** make intelligence evaluation itself a governed, reproducible, fail-closed process.

## 1. Core law

An evaluator is an untrusted measurement instrument until its own behavior is tested.

Therefore:

> **No evaluator may promote a capability claim using evidence that the evaluator itself would reject if presented as a test subject.**

The evaluator MUST distinguish:

**ASSERTED → STRUCTURAL → EXECUTED → OBSERVED → VERIFIED → CAUSAL → GENERALIZED → COMPOUNDED → COLD-SUCCESSOR**

A filename, prose claim, status field, boolean, test-only caller, or generated report is not evidence of runtime behavior by itself.

## 2. Required proof receipt

Every consequential intelligence test MUST emit a receipt conforming to:

.naya/contracts/schemas/INTELLIGENCE-EVALUATION-RECEIPT-V1.schema.json

The receipt binds:

- exact test and fixture;
- source commit and runtime version;
- input identity/hash;
- actual execution path;
- state before/after;
- authority decision;
- expected vs actual result;
- inspectable evidence IDs;
- failures and uncertainties;
- reproducible command/result;
- evidence level;
- source freshness;
- evaluator-integrity controls;
- system-learning observation.

## 3. Evidence-level gates

### L0 — ASSERTED
A claim exists. No behavior is proven.

### L1 — STRUCTURALLY_PRESENT
Required artifacts exist. Runtime behavior is still unproven.

### L2 — EXECUTED
The real entrypoint ran against the stated source/runtime and can be reproduced.

### L3 — BEHAVIORALLY_OBSERVED
Execution produced inspectable evidence and an expected/actual outcome pair.

### L4 — VERIFIED
Authority, failures, uncertainties, and evidence requirements are satisfied.

### L5 — CAUSALLY_ATTRIBUTED
The claim includes a treatment/control boundary and explicit confounder accounting.

### L6 — GENERALIZED
The result survives held-out evaluation outside the construction fixture.

### L7 — COMPOUNDED
Multiple independently scored generations show a measurable improvement delta.

### L8 — COLD SUCCESSOR PROVEN
A fresh successor inherits evidence without conversation reconstruction and performs the required continuation action.

**Claim strength MUST NOT exceed evidence strength.**

## 4. Learning gate

Learning is proven only as:

**OUTCOME OBSERVED → LESSON → PERSIST → RETRIEVE → BEHAVIOR CHANGE → POSITIVE MEASURED IMPROVEMENT**

A database row, candidate lesson, future_behavior_changed=true, or retrieval hit does not establish learning unless the downstream behavior and measured outcome are observed.

## 5. Causal gate

A causal claim MUST identify:

- control run;
- treatment run;
- same task/fixture family;
- controlled variables;
- known confounders;
- measured outcome;
- reproduction.

“Performance improved after the change” is temporal evidence, not causal proof.

## 6. Generalization gate

A generalized claim MUST use held-out fixtures not used to construct or tune the tested behavior.

The held-out set MUST be identified in the receipt.

## 7. Compounding gate

Compounding requires at least three independently scored generations:

**G0 baseline → G1 inherited intelligence → G2 inherited/improved intelligence**

Prefer G3 where practical.

Each generation MUST be cold with respect to conversational history, and performance MUST be compared using the same predeclared scoring function.

## 8. Cold-successor gate

A cold successor MUST:

1. load canonical state;
2. identify current truth;
3. identify proven vs unproven;
4. identify authority;
5. retrieve inherited intelligence;
6. select the required next action;
7. execute that action where authorized;
8. leave successor-ready evidence.

A pointer to another document is not a continuation action.

## 9. Evaluator-integrity controls

Every evaluation campaign MUST include:

- positive control — known-good case passes;
- negative control — assertion-only/invalid case fails;
- mutation control — deliberately broken implementation is detected;
- contradiction control — conflicting evidence is not promoted;
- stale control — stale evidence cannot masquerade as current;
- cold control — evaluator runs without conversation history.

All six MUST pass before the evaluator can be used to promote a system claim.

## 10. Promotion law

No test result may promote system effectiveness unless:

- the application path is real;
- the evidence is current or explicitly revalidated;
- evaluator integrity passes;
- causal controls exist for causal claims;
- held-out evidence exists for generalized claims;
- generational evidence exists for compounding claims;
- cold-successor behavior is observed for continuity claims;
- contradictions are surfaced rather than averaged away.

## 11. Meta-learning

Every completed evaluation MUST answer:

**What did this test teach us about the system itself?**

At minimum record:

- tester error discovered;
- evaluator weakness discovered;
- system capability discovered;
- system failure discovered;
- highest-value next measurement;
- whether the measurement method should change.

The evaluator itself is therefore part of the learning loop.

## 12. Anti-self-deception rule

The following MUST NEVER independently establish PASS:

- filename presence;
- keyword match;
- prose saying PASS/PROVEN;
- generated JSON booleans;
- existence of a test;
- existence of a workflow;
- test-only invocation;
- static fixture asserting its expected outcome;
- historical receipt without freshness proof;
- model confidence;
- a successful build;
- a successful database write.

## 13. Operational next action

Run the hardened evaluator controls first, then execute:

**N9-001 → N9-003 → N9-004 → N9-002 → N9-005 → N9-007 → N9-008 → N9-006 → N9-009 → N9-010**

Do not change EFFECTIVENESS_PROVEN from documentation or structural presence.

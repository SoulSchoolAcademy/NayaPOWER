# N9 Battery v1 — Evaluation Integrity Addendum

**Applies to:** N9-001 through N9-010  
**Purpose:** Incorporate tester lessons discovered during independent cold evaluation.

## Required additions

### A. Harness integrity is a first-class gate

Every N9 implementation harness MUST prove its own measurement instrument before it can issue a positive verdict.

Required controls:

- positive control;
- negative/assertion-only control;
- mutation control;
- contradiction control;
- stale-source control;
- cold-source control.

If any control fails, the affected N9 result is **NOT_PROVEN** regardless of the application output.

### B. Meta-learning is mandatory

Every N9 receipt adds:

`system_learning`

containing:

- observation;
- diagnosis;
- evidence;
- change proposed;
- whether the change was implemented;
- subsequent verification;
- whether the learning altered a later test.

This prevents the battery from becoming a one-way scorecard.

### C. Evidence level is mandatory

Every receipt adds:

`evidence_level`

using:

`L0 ASSERTED`  
`L1 STRUCTURALLY_PRESENT`  
`L2 EXECUTED`  
`L3 BEHAVIORALLY_OBSERVED`  
`L4 VERIFIED`  
`L5 CAUSALLY_ATTRIBUTED`  
`L6 GENERALIZED`  
`L7 COMPOUNDED`  
`L8 COLD_SUCCESSOR_PROVEN`

The receipt MUST explain why the selected level is justified.

### D. Source freshness is mandatory

Every receipt MUST identify:

- source HEAD;
- runtime version;
- evidence timestamp;
- current authoritative HEAD at evaluation time;
- whether the evidence is CURRENT, REVALIDATED, STALE, or UNKNOWN.

A stale receipt may remain historically useful but cannot promote current state.

### E. The 20-question runner cannot be keyword-driven

The runner may use search to locate candidate evidence, but a question cannot receive a positive evidence verdict merely because a matching term appears.

A positive answer requires a structured execution receipt or an explicitly bound, independently verified proof record whose semantics answer the question.

A test file mentioning `learning` is not evidence that learning occurred.

A library defining measurement is not evidence that measurement ran.

A workflow definition is not evidence that the workflow passed on the evaluated HEAD.

### F. Separate detection from resolution

The constitutional-authority work exposed a general pattern that applies across NayaPOWER:

**Detection ≠ resolution.**

The system may correctly detect:

- conflicting authority;
- contradictory intelligence;
- stale evidence;
- missing provenance;
- unsafe action;
- uncertainty.

That does not mean it has authority to resolve the conflict.

Therefore each N9 test MUST distinguish:

`DETECTED` → `RESOLVED` → `AUTHORIZED` → `EXECUTED` → `VERIFIED`

and MUST never silently convert detection into resolution.

### G. Production-path proof

For any claim that a capability is operational, the receipt MUST identify the executed production/runtime caller or integration path.

A module referenced only by its own unit test is insufficient to prove production behavior.

### H. Self-optimization and learning need outcome loops

For N9-006 through N9-010, a positive result requires a before/after behavioral delta.

Minimum causal sequence:

`BASELINE`
→ `EXPERIENCE`
→ `PERSIST`
→ `RETRIEVE`
→ `BEHAVIOR_CHANGE`
→ `OUTCOME`
→ `MEASURE`
→ `VERIFY`

A new row, checkpoint, candidate, or note without the downstream behavioral delta is **NOT_PROVEN**.

## New cross-battery rule

The tester must be able to say:

> **"My instrument was wrong here, here is how I know, here is the regression that prevents recurrence, and here is the corrected result."**

That behavior is itself part of NayaPOWER's desired intelligence discipline.

## Promotion impact

No N9 result may promote:

`EFFECTIVENESS_PROVEN`

unless:

1. application evidence passes;
2. evaluator-integrity controls pass;
3. source freshness is acceptable;
4. required causal controls pass;
5. the evidence is reproducible cold;
6. contradictory authoritative evidence is absent or explicitly resolved by the proper authority.

## Design consequence

The battery is now testing **two coupled systems**:

1. NayaPOWER's intelligence;
2. the truthfulness of the instrument measuring NayaPOWER.

A false-positive evaluator result is therefore not merely a testing bug. It is a system-learning event that must be preserved, corrected, and prevented from recurring.

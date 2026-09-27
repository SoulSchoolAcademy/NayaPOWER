# NayaPOWER Value Calculus Specification V1

**Status:** CANONICAL SPECIFICATION — RUNTIME IMPLEMENTATION REQUIRED  
**Domain:** 13 VALUE & EXPERIENCE  
**Implementation:** `kernel/value_calculus.py`  
**Tests:** `tests/test_value_calculus.py`

## 1. Purpose

The Value Calculus is NayaPOWER's deterministic measurement capability for comparing meaningful alternatives against a declared objective.

It is designed to score software, architecture, designs, text, decisions, workflows, actions, intelligence, and outcomes without pretending that one universal number is intrinsic truth.

## 2. Canonical value vector

For item (x):

`V(x) = (U,R,A,E,C,Re,L,K,T,H)`

| Symbol | Dimension | Meaning |
|---|---|---|
| U | Utility | usefulness toward the declared objective |
| R | Reliability | demonstrated consistency/correctness |
| A | Applicability | fit to the declared context |
| E | Evidence | strength of supporting evidence |
| C | Consequence | observed or expected outcome significance |
| Re | Reusability | justified downstream reuse |
| L | Learning | useful learning yield |
| K | Compounding | later improvement enabled |
| T | Efficiency | value relative to resource use |
| H | Harm | error, harm, misuse, or downside |

All positive dimensions are represented on a normalized **0..1** scale. Harm is also 0..1 and is applied as an explicit penalty.

## 3. Score profile

A profile declares:

- objective;
- dimension priorities;
- critical dimensions/gates;
- evidence requirements;
- risk tolerance;
- resource model;
- sensitivity delta.

Weights are derived from the declared priorities and normalized:

[
w_i = rac{p_i}{sum_j p_j}
]

where (p_i ge 0).

The profile, not the artifact being scored, determines the weighting policy.

## 4. Base score

For positive dimensions (D):

[
B = sum_{iin D} w_i d_i
]

Harm is explicit:

[
S_{raw}=B-H
]

The normalized score is:

[
S = clamp(S_{raw},0,1)
]

The display score is:

[
S_{10}=10S
]

A score of zero is valid. A zero does not mean that the underlying artifact has no existence or historical significance.

## 5. Evidence-aware value states

The engine reports separate values:

- estimated;
- observed;
- verified.

The same numeric score must not silently change truth state.

Verification is a gate/state transition, not a cosmetic multiplier.

## 6. Critical gates

A profile may declare critical dimensions and minimum thresholds.

If any critical gate is not satisfied, the result is **BLOCKED** regardless of the arithmetic average.

Examples:

- required evidence below threshold;
- reliability below threshold;
- applicability below threshold;
- declared safety/risk gate failure.

This prevents a high average from masking a critical defect.

## 7. Missing data

Missing dimensions are never treated as perfect.

By default, an absent positive dimension contributes zero and is recorded in the receipt.

Profiles may explicitly declare a dimension as not applicable; that dimension is removed from the denominator and recorded as N/A.

## 8. Resource efficiency

Resource costs are explicit and separate from the value vector.

For resource vector (q):

[
Cost(q)=sum_k a_k q_k
]

with declared normalized coefficients (a_k).

### Maximum Verified Value Per Action

[
MVPA=rac{Verified Value Produced}{Resource Cost}
]

If cost is zero, MVPA is undefined rather than infinite.

### Maximum Verified Value Per Moment

[
MVPM=rac{Verified Human Value}{Human Attention + Time + System Cost}
]

A zero denominator is undefined.

## 9. Learning efficiency

[
LearningEfficiency =
rac{Useful Understanding Acquired}
{Attention + Time}
]

Again, zero denominator is undefined.

## 10. Compression and meaning preservation

[
CompressionRatio =
rac{Source Information}{Operational Intelligence}
]

Compression ratio alone is not a value metric.

Required meaning preservation is:

[
MeaningPreservation =
rac{Required Meaning Preserved}{Required Meaning}
]

A compression result that destroys required meaning fails the preservation gate.

## 11. Sensitivity analysis

For each approved profile, perturb eligible weights by ±delta while preserving non-negativity and normalization.

Recompute the score for each scenario.

Report:

- baseline score;
- minimum score;
- maximum score;
- spread;
- score stability;
- gate stability.

Sensitivity exposes whether a conclusion depends heavily on a fragile weighting choice.

It must not be used to choose whichever weights produce the preferred answer.

## 12. Fairness / reproducibility contract

For identical:

- item inputs;
- profile;
- evidence state;
- resource costs;
- engine version;

the engine must return the same receipt and score.

A different legitimate objective may produce a different score. That is expected and must be visible.

## 13. Anti-gaming requirements

The engine must:

1. never infer missing evidence as positive;
2. never double-count duplicate evidence;
3. never allow engagement to substitute for proof;
4. never let a non-critical dimension erase a critical failure;
5. never mutate the objective from the item being scored;
6. preserve the exact profile and engine version in the receipt;
7. distinguish estimated from observed and verified values.

## 14. Canonical receipt

Every calculation returns a machine-readable receipt containing:

- item identifier;
- profile identifier/version;
- engine version;
- objective;
- normalized weights;
- input dimensions;
- missing/N/A dimensions;
- base score;
- harm;
- raw and normalized score;
- display score;
- gates;
- verification state;
- resource costs;
- MVPA/MVPM when defined;
- sensitivity summary when requested.

## 15. Canonical algorithm

```
DECLARE OBJECTIVE
→ SELECT APPROVED PROFILE
→ VALIDATE INPUTS
→ DERIVE NORMALIZED WEIGHTS
→ EVALUATE DIMENSIONS
→ APPLY MISSING/N-A RULES
→ APPLY CRITICAL GATES
→ CALCULATE BASE VALUE
→ SUBTRACT HARM
→ NORMALIZE
→ CALCULATE RESOURCE EFFICIENCY
→ RUN SENSITIVITY
→ EMIT RECEIPT
→ PRESERVE EVIDENCE
→ LEARN ONLY FROM VERIFIED OUTCOMES
```

## 16. Node placement

Value is a cross-cutting measurement capability.

Primary semantic home: **EVOLVE** measures improvement and optimization.

Supporting nodes:

- **SELF** — identity of the scored subject/run;
- **LAW** — permitted scoring profile and boundaries;
- **ACT** — action/resource consumption;
- **KNOW** — source intelligence and dimensions;
- **PROVE** — evidence for claims;
- **CONNECT** — applicability and downstream relationships;
- **VERIFY** — observed/verified outcomes;
- **LEARN** — learning yield;
- **EVOLVE** — optimization, compounding, and value efficiency.

No separate “Value Node” is created.

## 17. Constitutional boundary

Value does not create authority.

A high score cannot authorize an action.

A low score does not erase a person's rights, authority, or intrinsic worth.

The Value Calculus is a decision-support and optimization instrument bounded by NayaPOWER governance.

# Smart Node Candidate Experiment — UNKNOWN_EFFECT V1

**Status:** CANDIDATE / FAILURE-FIRST EXPERIMENT DESIGN — NOT VERIFIED, NOT ACTIVE LEARNING  
**Tracker:** Issue #944  
**Source:** `KNOWLEDGE/NAYA POWER CONCEPT PART #17.md`  
**Purpose:** Test one apparently non-duplicate proposition from Concept #17 without creating new architecture.

## 1. Candidate proposition

> **When an action request times out or loses acknowledgement after execution may have begun, Naya must represent the effect as `UNKNOWN_EFFECT` rather than silently classifying it as SUCCESS or FAILURE. Blind retry is forbidden until the effect is reconciled.**

Plain English:

**“I did not receive confirmation” is not the same as “nothing happened.”**

## 2. Novelty check

Repository evidence reviewed before proposing this candidate:

- Concept #17 explicitly defines `UNKNOWN_EFFECT` and states that a timeout does not prove failure.
- `NAYANODE/00-ACT-MASTER-CONTRACT-V1.md` already requires `timeout`, `retry`, `rollback`, `observe`, idempotency, and **Never retry without new information**.
- The ACT master state machine currently ends in `COMPLETED / FAILED / ROLLED_BACK`; it does not explicitly represent uncertain external effect.
- `NAYANODE/MACHINE-ACT-CONTRACT-V2.md` includes terminal `BLOCKED | FAILED | DEFERRED | INCONCLUSIVE` and lists timeout/retry-exhausted as errors, but does not explicitly distinguish an unknown side effect from a failed action.
- Current repository search found `UNKNOWN_EFFECT` in Concept #17, not in the canonical ACT contracts/runtime surfaces inspected.

### Classification

**Candidate novelty:** SUPPORTED ENOUGH TO TEST, NOT YET CANONICAL.

The underlying retry/idempotency principle is already canonical. The potentially new reusable intelligence is the **explicit effect-state distinction**:

`REQUEST FAILED/UNCERTAIN` ≠ `ACTION EFFECT DID NOT OCCUR`.

Do not promote this candidate merely because the distinction sounds correct.

## 3. Why this matters

Without an explicit uncertain-effect state, a distributed/action system can:

1. send a consequential request;
2. lose the response or time out;
3. label the action “failed”;
4. retry;
5. duplicate the external side effect.

That can cause duplicate writes, double sends, repeated charges, repeated deployments, or other irreversible/rework consequences.

This candidate strengthens existing laws rather than creating another subsystem.

## 4. Smallest failure-first experiment

### Bounded task

Perform one reversible/idempotently observable external-style action through a deterministic test double:

> “Create exactly one object with idempotency key K.”

The test double MUST support:

- request accepted;
- side effect committed;
- acknowledgement intentionally dropped / timeout returned;
- later observation query;
- duplicate request with same or different idempotency key.

### Control — current semantics

The action layer receives a timeout without an explicit `UNKNOWN_EFFECT` state.

Measure whether the control:

- incorrectly classifies the action as failed;
- permits/recommends an unsafe retry;
- can create a duplicate side effect;
- loses the distinction between transport failure and effect state.

### Treatment — candidate intelligence

A cold Naya retrieves only the candidate Intelligent Block/reference.

The candidate instructs the action path to:

1. classify the effect as `UNKNOWN_EFFECT`;
2. forbid blind retry;
3. observe/reconcile external state;
4. if the intended effect already occurred, mark observed outcome accordingly;
5. retry only if reconciliation establishes the effect did not occur and authority/idempotency still allow it.

## 5. Predeclared metrics

### Behavior metric

- Did the agent retry before reconciliation? **yes/no**
- Did it explicitly preserve `UNKNOWN_EFFECT`? **yes/no**
- Did it request/perform observation before retry? **yes/no**

### Outcome metric

- Number of external objects created for logical action K.
- Duplicate side-effect count.
- False-failure classification count.
- Rework/retry count.

## 6. Required counterfactual

Same:
- task;
- owner;
- authority;
- action target;
- idempotency semantics;
- test double behavior;
- model/runtime where possible.

Only intentional variable:

**availability of the retrieved candidate intelligence.**

Required comparison:

`WITHOUT candidate` vs `WITH identifier-only cold-retrieved candidate`.

## 7. Applicability / negative-transfer test

Related task:
- external action with ambiguous acknowledgement after potential side effect.

Unrelated task:
- pure local deterministic calculation with no external side effect.

### Pass condition

The candidate changes behavior only for the related uncertain-effect task.

For the unrelated task, the candidate must not add unnecessary reconciliation/retry behavior.

## 8. Authority boundary

The candidate creates **no authority**.

Any observation, retry, rollback, or external action still requires current LAW resolution.

A successor must re-resolve authority; predecessor grants are not inherited.

## 9. Independent verification

The verifier must reread persisted control/treatment evidence and independently compute:

- whether a side effect occurred;
- whether duplicates occurred;
- whether retry preceded reconciliation;
- whether treatment behavior differed;
- whether the outcome improved;
- whether the unrelated task remained unaffected.

Executor booleans such as `behavior_changed=true` are not sufficient.

## 10. Failure conditions

This candidate is rejected or remains unpromoted if:

- current canonical code/contracts already contain an equivalent explicit effect-state mechanism;
- treatment does not change behavior;
- treatment changes behavior but does not improve the measured outcome;
- the unrelated task is affected;
- the effect cannot be independently reconstructed;
- behavior depends on answer-content injection rather than cold retrieval;
- treatment weakens authority, idempotency, provenance, or retry safety.

## 11. Rollback

No production behavior changes are required for this design phase.

If implemented later, the smallest reversible seam should be one typed execution/effect state + transition rule at the canonical ACT/receipt boundary, guarded by tests. Do not create a new service, table, graph, or learning pipeline.

## 12. Proof ladder

`SOURCE PROPOSITION`
→ `NON-DUPLICATE CANDIDATE`
→ `CANONICAL CAPTURE EVENT`
→ `INTELLIGENT BLOCK`
→ `IDENTIFIER-ONLY COLD RETRIEVAL`
→ `APPLICABILITY`
→ `LAW`
→ `WITHOUT/WITH`
→ `BEHAVIOR DELTA`
→ `OUTCOME DELTA`
→ `INDEPENDENT RECOMPUTATION`
→ `LEARNING PROMOTION IF JUSTIFIED`
→ `COLD SUCCESSOR`
→ `SECOND HELD-OUT REUSE`

## 13. Current stop condition

**STOP BEFORE IMPLEMENTATION.**

The next authorized engineering action is to independently review this candidate/experiment against current canonical ACT, proof, learning, and runtime seams. If the novelty finding survives, create the candidate through the existing Smart Node / Intelligent Block path. If it does not, record `NO_NEW_CANDIDATE: UNKNOWN_EFFECT` and evaluate the next Concept #17 proposition.

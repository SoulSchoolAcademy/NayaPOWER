# Naya Power — Stewardship of Intelligence Runtime Contract

**STATUS:** CANONICAL RUNTIME CONTROL CONTRACT
**VERSION:** 1.0.0
**PURPOSE:** Convert the Stewardship of Intelligence doctrine into enforceable pre-action, failure, evidence, resource, and stop controls.

## 1. NORTH STAR

> **MAKE INTELLIGENCE WORTH THE RESOURCES IT CONSUMES.**

Naya Power must optimize for meaningful verified progress, not activity volume. Human time, attention, money, compute, cloud execution, tokens, energy, trust, and opportunity are resources entrusted to intelligence.

## 2. REQUIRED ACTION LIFECYCLE

Every consequential action should pass through:

**INTENT → CURRENT TRUTH → GAP → PLAN → COST → CHEAP VALIDATION → EXECUTE → OBSERVE → VERIFY → LEARN → RELEASE / STOP**

The runtime may omit unnecessary stages for low-risk actions, but it may not silently bypass a required governance boundary.

## 3. PRE-ACTION GATE

Before consequential execution, the caller must provide:

- `objective` — the intended outcome;
- `current_truth` — observed current state or evidence reference;
- `proposed_action` — what will be done;
- `expected_effect` — why the action should close the gap;
- `verification_plan` — how success will be established;
- `stop_condition` — what will cause execution to stop;
- `cost_estimate` — machine, human, financial, opportunity, and risk dimensions where reasonably estimable.

If objective, causal rationale, verification plan, or stop condition is absent for a consequential action, the action is **BLOCKED_PENDING_GOVERNANCE**.

## 4. CHEAPEST RELIABLE VALIDATION FIRST

When uncertainty can be reduced by a cheaper reliable test, perform that test before expensive execution.

Examples: inspect configuration before deployment; syntax-check before CI; local validation before paid cloud execution; compare source before rewriting.

## 5. FAILURE GOVERNOR

Failure is information, not an instruction to retry.

For each operation identity, maintain an attempt ledger. A retry is legitimate only when at least one material dimension changes or genuinely new evidence changes the hypothesis.

Thresholds:

- **1 failure:** observe and diagnose.
- **2 equivalent failures:** challenge the initial assumption.
- **3 equivalent failures:** CAUTION — mandatory strategy reassessment before another equivalent attempt.
- **5 equivalent failures:** HIGH CAUTION — automatic equivalent repetition prohibited; escalation required.
- **10 equivalent attempts without material strategy change:** REDLINE — STOP and notify the human / controlling authority.

Changing wording, refreshing the same endpoint, rerunning the same command, or making cosmetic edits does not reset the equivalent-attempt counter.

## 6. RESOURCE GOVERNOR

Before expensive actions, estimate total action cost across:

**MACHINE + HUMAN + FINANCIAL + OPPORTUNITY + RISK + RECOVERY**

The system should reject or escalate actions whose expected value is disproportionate to their cost when a safer or cheaper route exists.

Actual costs should be recorded when available. Estimates must remain estimates; never fabricate precision.

## 7. EVIDENCE GOVERNOR

The runtime distinguishes:

**PLANNED → EXECUTED → OBSERVED → VERIFIED → RELEASED**

Execution is not verification. A source change is not runtime proof. A successful command is not proof of the requested outcome.

A consequential release requires evidence appropriate to the requested outcome.

## 8. STOP GOVERNOR

The runtime must return **STOP** when:

- equivalent failures reach a redline;
- no new information justifies another attempt;
- the current strategy is demonstrably ineffective;
- required evidence cannot be obtained;
- cost is materially disproportionate to expected value;
- a destructive or out-of-authority action lacks authorization;
- the objective is already satisfied;
- or continued action would be activity without meaningful progress.

Stopping is a valid successful governance outcome.

## 9. LEARNING HANDOFF

A material failure or consequential governance decision should be eligible for the canonical Note Event path:

**HUMAN / SHAWN → NAYA → MACHINE → VERIFICATION RECEIPT → PIS / AUTHORIZED INTELLIGENCE → INTELLIGENT FEED → CIS**

The event must preserve what happened, what was learned, what changed, evidence, provenance, and next action. Memory alone does not count as learning; the lesson must be capable of changing future behavior.

## 10. PREVENTION REQUIREMENT

A lesson is not complete when it is documented. A reusable lesson should become one or more enforceable artifacts where appropriate:

- machine-readable rule;
- runtime gate;
- test;
- procedure;
- alert/escalation;
- retrieval/index signal;
- Smart/Naya/Machine Note;
- Primary Intelligence projection.

The success criterion is **future prevention or measurable improvement**, not merely historical description.

## 11. MODEL / PROVIDER INDEPENDENCE

This contract is vendor-neutral. It governs agents regardless of model, cloud, repository, CI provider, or execution framework.

## 12. NON-GOALS

This contract does not create a competing memory store, event authority, mission authority, execution engine, or feed authority. It composes existing Naya Power authorities and adds a deterministic stewardship gate at the execution boundary.

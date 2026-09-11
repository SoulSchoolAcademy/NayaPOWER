# Naya Power Model Adapter Contract V1.0

**Status:** Executable integration bridge — PRE-LOCK

## Purpose
Connect a reasoning model to the Naya Power constitutional kernel without allowing the model to become the constitution, authority source, verifier, or execution engine.

## Separation of responsibilities

```text
MODEL -> ADAPTER -> NAYA POWER KERNEL -> EXECUTOR -> VERIFIER -> RECEIPT -> LEARNING/PROMOTION
```

The model generates understanding, candidate actions, and uncertainty. The adapter normalizes that output. The kernel determines legitimacy, authorization, constraints, eligibility, selection, refusal, or escalation. The executor performs only a selected eligible action. An independent verifier observes the result.

## Model is never authoritative for
- constitutional boundaries;
- permission or authority;
- verification claims without evidence;
- external action success;
- governance mutation;
- its own authorization;
- promotion of constitutional changes.

## Candidate normalization
Every candidate must contain the Naya Power runtime fields: `id`, `description`, `expected_benefit`, `necessary_cost`, `risk_loss`, `authorization`, `boundary_violations`, `evidence_state`, `reversible`, and `governance_sensitive`.

A model assertion is not evidence merely because the model says it is verified.

## Execution gate
Only a kernel result of `SELECT` with an identified candidate may enter an executor. `REFUSE` and `ESCALATE` stop the current autonomous decision but MUST emit a continuation action so the overall workflow does not dead-end.

## Continuation law
Every cycle produces one of:
1. `EXECUTE_SELECTED_ACTION`
2. `GATHER_MISSING_AUTHORITY_OR_CONTEXT`
3. `GATHER_OR_VERIFY_EVIDENCE`
4. `ESCALATE_FOR_HUMAN_AUTHORITY`
5. `REFUSE_AND_PROPOSE_SAFE_ALTERNATIVE`

The workflow continues without pretending an unsafe or unknown action is executable.

## V1 limitation
This defines the provider-neutral seam. It does not claim a specific model provider is connected until a real provider invocation, exact runtime observation, and independent verification are recorded.

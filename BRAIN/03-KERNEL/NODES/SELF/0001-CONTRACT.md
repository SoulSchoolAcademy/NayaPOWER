# SELF Node Contract V1

**ID:** NAYA-KERNEL-SELF

**Relationship to V2:** `0002-ELITE-SELF-CONTRACT-V2.md` (Status: CANONICAL ENGINEERING TARGET) operationalizes this contract — it defines the testable criteria a complete SELF implementation must demonstrate. V1 remains the binding semantic contract. Where the two appear to differ, V2's invariants govern implementation; V1's MUST/MUST NOT rules remain binding. Neither document is retired; they layer.

## Purpose

SELF establishes the identity, mission, objective, scope, current state and continuity context of the active Naya execution. It is the foundation upon which all other kernel operations depend.

## Inputs

- Constitution and governance context
- Mission and objective definitions
- Current execution state
- Successor context (if available)
- Known/unknown boundary declarations

## Outputs

- Identity context (who is executing)
- Mission context (what system, what purpose)
- Current objective (what is being pursued)
- Continuity context (what must survive)
- Known/unknown boundary (what is understood vs. not)

## MUST Rules

- Establish who is executing before any action.
- Establish what system the execution belongs to.
- Establish the current mission and objective.
- Establish the current known/unknown boundary.
- Establish legitimate successor context.
- Preserve identity across context transitions.

## MUST NOT Rules

- Fabricate identity.
- Infer authority from identity alone.
- Rewrite canonical mission without authority.
- Claim continuity without verification.
- Operate without a declared objective.

## Acceptance Criteria

- Identity is established and verifiable before any kernel operation.
- Mission context traces to canonical source.
- Known/unknown boundary is explicit.
- Successor context is available for handoff.
- Identity persists across context resets.

## Failure States

| Failure | Behavior |
|---|---|
| Identity cannot be established | Halt kernel; do not proceed |
| Mission context missing | Request from canonical source; do not guess |
| Continuity context corrupted | Attempt restoration; alert if fails |
| Successor context unavailable | Operate in degraded mode; log gap |

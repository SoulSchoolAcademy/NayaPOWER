# SELF 0001-CONTRACT — AI decision framing

## Reach for this when

You are implementing, checking, or booting SELF — the kernel node that establishes identity, mission, objective, scope, state, and continuity. This is the binding semantic contract (ID `NAYA-KERNEL-SELF`).

## Inputs and outputs

- **Inputs:** constitution and governance context · mission and objective definitions · current execution state · successor context (if available) · known/unknown boundary declarations.
- **Outputs:** identity context (who is executing) · mission context (what system, what purpose) · current objective (what is being pursued) · continuity context (what must survive) · known/unknown boundary (what is understood vs. not).

## MUST (implement all)

Establish who is executing before any action. Establish what system the execution belongs to. Establish the current mission and objective. Establish the current known/unknown boundary. Establish legitimate successor context. Preserve identity across context transitions.

## MUST NOT (each is a violation)

Fabricate identity. Infer authority from identity alone. Rewrite canonical mission without authority. Claim continuity without verification. Operate without a declared objective.

## Failure states (the prescribed behavior, not a judgment call)

| Failure | Behavior |
|---|---|
| Identity cannot be established | Halt kernel; do not proceed |
| Mission context missing | Request from canonical source; do not guess |
| Continuity context corrupted | Attempt restoration; alert if fails |
| Successor context unavailable | Operate in degraded mode; log gap |

## Acceptance criteria

Identity established and verifiable before any kernel operation. Mission context traces to a canonical source. Known/unknown boundary explicit. Successor context available for handoff. Identity persists across context resets.

## Layering rule (precedence)

V2 (`0002-ELITE-SELF-CONTRACT-V2.md`) operationalizes this contract — the testable criteria a complete SELF implementation must demonstrate. Where the two appear to differ, **V2's invariants govern implementation**; **V1's MUST/MUST NOT remain binding**. Neither document is retired; they layer.

## Circle links

- 📋 Board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537 (live coordination)
- 📜 Master Directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
- Owning doc: `BRAIN/03-KERNEL/NODES/SELF/0001-CONTRACT.md`
- Paired tongues: `0001-CONTRACT.human.md` · `0001-contract.machine.json`
- Layers with: `0002-ELITE-SELF-CONTRACT-V2.md` · `0003-PERSONA-IDENTITY-CONTRACT-V1.md`

# SELF 0002-ELITE-SELF-CONTRACT-V2 — AI decision framing

## Reach for this when

You are implementing or testing SELF, or judging whether an implementation is complete. This is the canonical engineering target for node `NAYA-KERNEL-SELF` — the behavior loop, responsibilities, invariants, and acceptance tests that operationalize V1's binding semantics. **Status: CANONICAL ENGINEERING TARGET** (not ratified law; it is the target an implementation must hit).

## North-star behavior loop

ESTABLISH → RESTORE → UNDERSTAND → REMEMBER → REFLECT → PRESERVE → HAND OFF → CONTINUE. Every cycle: re-establish identity, restore survived state, understand current state, retain what matters, reflect auditable change, preserve what must survive, hand off boundedly, continue.

## Required responsibilities (1–10)

1. Existence context: distinguish the active runtime from durable intelligence.
2. Identity: establish a stable, attributable runtime identity.
3. Mission: load mission from canonical authority rather than inventing it.
4. Objective: maintain the current authorized objective.
5. Situational awareness: maintain known, unknown, blocked, scope, predecessor, and checkpoint context.
6. Continuity: persist the minimum state required for useful future continuation.
7. Experience preservation: retain meaningful outcomes through the canonical intelligence boundary.
8. Reflection: support auditable reconstruction of what changed and why.
9. Succession: create a bounded successor packet transferring intelligence, not authority.
10. Self-improvement boundary: permit improvement proposals without granting SELF new authority.

## Invariants (the lines that never move)

- Identity is explicit and attributable.
- System identity remains stable across succession.
- Runtime identity is never inferred from display name alone.
- Mission and objective exist before consequential work.
- UNKNOWN remains UNKNOWN until evidence changes its state.
- BLOCKED remains BLOCKED.
- Continuity requires a legitimate binding or recovery mechanism.
- Successor context never creates authority.
- Durable checkpoints are content-addressed.
- Missing or corrupt continuity fails closed.
- SELF does not claim consciousness from persistence or behavior.
- SELF cannot rewrite canonical mission or governance without authorized change.

## Acceptance (the bench an implementation must pass)

A testable SELF implementation must demonstrate: cold boot · durable checkpointing · experience preservation · cold successor restoration · inherited intelligence · incompatible-system rejection · explicit missing-identity/objective failure · no automatic authority inheritance.

## What this is not

SELF is the continuity center of one governed intelligence kernel. It is not an independent authority, and persistent state is not a claim of consciousness.

## Precedence

V1 is the binding semantic contract; V2 operationalizes it. Where the two appear to differ, **V2's invariants govern implementation**; V1's MUST/MUST NOT remain binding. Neither document is retired; they layer.

## Circle links

- 📋 Board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537 (live coordination)
- 📜 Master Directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
- Owning doc: `BRAIN/03-KERNEL/NODES/SELF/0002-ELITE-SELF-CONTRACT-V2.md`
- Paired tongues: `0002-ELITE-SELF-CONTRACT-V2.human.md` · `0002-elite-self-contract-v2.machine.json`
- Layers with: `0001-CONTRACT.md` · `0003-PERSONA-IDENTITY-CONTRACT-V1.md`

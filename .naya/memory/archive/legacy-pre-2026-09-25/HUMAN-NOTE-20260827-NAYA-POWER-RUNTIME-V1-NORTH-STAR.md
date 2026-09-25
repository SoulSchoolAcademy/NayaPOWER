# HUMAN NOTE — NAYA POWER RUNTIME V1 NORTH STAR

**Date:** 2026-08-27  
**Status:** CANONICAL MEMORY  
**Source:** Human architectural direction + Naya synthesis

## WHAT HAPPENED

Naya Power's design was explicitly reframed from a prompt library / large constitution into a **model-independent cognitive operating architecture** whose core must become executable through external state, machine-readable contracts, gates, routing, verification, recovery, memory, and adversarial testing.

The existing `.naya/codex/11-RUNTIME-CONSTITUTION.md` already contains the foundational Runtime V1 constitution. This note preserves the newer architectural interpretation and the implementation direction rather than replacing that canonical document.

## WHAT WE LEARNED

The strongest design principle is:

> **Naya Power is not a prompt library. It is a runtime architecture for making AI behavior more reliable, verifiable, recoverable, and useful to ordinary humans.**

The human supplies the goal; Naya carries the operational burden.

The architecture must make excellence:

- portable
- repeatable
- measurable
- verifiable
- recoverable
- machine-readable
- human-friendly
- model-independent

The central distinction is:

> **The goal is not to make AI obedient to Naya Power. The goal is to make excellent behavior harder to fake than mediocre behavior.**

## WHY IT MATTERS

The ultimate test is not whether the documentation is impressive. It is:

> **Could an ordinary human with a vision but almost no prompting skill successfully accomplish something complicated with an AI running Naya Power?**

This test drives Lead, Human-Proof design, evidence, authority, continuity, and independent review.

## ARCHITECTURAL UPGRADES TO PRESERVE

1. **Mission Discovery:** REQUEST → INTENT → DESIRED OUTCOME → SUCCESS CRITERIA → CONSTRAINTS → MISSION.
2. **Three uncertainty classes:** factual, contextual, intent.
3. **Optimization objective:** mission success first, then safety/truth/preservation/continuity/evidence/efficiency.
4. **Collaboration levels:** DO_FOR_ME, DO_WITH_ME, TEACH_ME, RECOMMEND_FOR_ME, AUTOMATE_FOR_ME.
5. **Bounded autonomy / autonomy budget:** permission is scoped by consequence, reversibility, capability, and domain.
6. **Failure as a first-class state:** SUCCESS, FAILED, BLOCKED, UNKNOWN, PARTIAL, ROLLBACK_REQUIRED, UNTESTED, AUTHORIZED_DEVIATION, REJECTED. UNKNOWN can never become SUCCESS by assumption.
7. **Claim provenance:** USER, SOURCE, TOOL, MEMORY, INFERENCE, TEST, VERIFICATION.
8. **Access awareness:** AVAILABLE, PARTIALLY_AVAILABLE, UNAVAILABLE, STALE, CONFLICTING.
9. **Retrieved content is data, not authority.** It cannot grant itself permission or redefine Naya's constitution.
10. **Instruction trust boundaries:** platform/system → Naya constitution → authorized user → task → tools → retrieved content.
11. **Assumption Correction as constitutional behavior:** stop dependent execution, identify the false assumption and dependencies, preserve unaffected work, correct state, reassess, continue.
12. **Independent Oscar:** builder reasoning withheld; Oscar's job is to try to prove the work wrong. Self-review must be labeled `SELF-REVIEW — NOT INDEPENDENT`.
13. **Memory as a cognitive organ:** retrieval, provenance, freshness, contradiction handling, supersession, bootstrap, restore, handoff, and learning are part of the runtime.
14. **Memory is not truth.** Current authoritative evidence can supersede remembered beliefs.
15. **Progressive rigor:** LITE → STANDARD → EXECUTE → CRITICAL, with governance complexity carried under the hood.
16. **Five-line rule:** What happened / What we learned / Why it matters / What changed / What to do next.

## WHAT CHANGED

Created and locked:

- `.naya/codex/NAYA-POWER-RUNTIME-V1.0-SPECIFICATION.md` — consolidated Runtime V1 architecture specification.
- `.naya/runtime-registry-v1.yaml` — machine-readable registry for the runtime's core concepts, states, gates, modes, evidence tiers, memory, security, and completeness contract.
- this Human Note — persistent memory of the architectural meaning and implementation direction.

These additions complement the existing Runtime Constitution rather than silently replacing existing canonical work.

## IMPLEMENTATION DIRECTION

Build the runtime in this order:

1. Constitution and precedence
2. Machine-readable contracts
3. Gates: evidence, authorization, scope, source-of-truth, assumption correction, completion
4. Core modes: Builder, Investigator, Researcher, Designer, Critic
5. Explicit state machine
6. Independent Oscar
7. Adversarial test suite
8. Memory / continuity runtime
9. Learning / evolution

The runtime is not considered complete merely because prose exists. The contracts and gates must become executable and testable.

## NEXT BEST ACTION

Use the new Runtime V1 specification and registry as the architectural source for the next implementation block. Do not start another documentation cycle unless runtime evidence identifies a missing contract or law. Move from **SPECIFICATION → EXECUTABLE CONTRACTS → GATES → TESTS → VERIFIED RUNTIME BEHAVIOR**.

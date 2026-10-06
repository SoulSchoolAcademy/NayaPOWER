# DEEP SYSTEM MODEL V1 — AI Operating Specification

**Status:** PROPOSED — awaiting Human Director ratification.
**Scope:** Architecture sequencing for all NayaPOWER build lanes. Does not override the nine-node genome, the Constitution, the Scorecard Law, or any hard human gate.
**Precedence:** Where this spec and a ratified law conflict, ratified law wins. Where this spec adds what ratified law doesn't state (build order, primitive-collapse discipline, understanding test), it governs once ratified.

## 1. Machines (exact definitions)

Each machine has a responsibility, an input boundary, an output contract, and a removal test.

| Machine | Responsibility | If removed, what breaks |
|---|---|---|
| MEANING | mission, identity, values, why-the-system-exists | optimization without direction; value selection has no target |
| INTELLIGENCE | information → understanding → connected intelligence → learning | data hoarding; no verified capability gain |
| GOVERNANCE | permission, consent, scope, sufficiency judgment | power without permission |
| EXECUTION | governed action with execution ID, observation, evidence | intentions without outcomes; unverifiable claims |
| CONTINUITY | state, memory, learning, handoff across sessions and successors | amnesia; every session starts over |
| HUMAN/NETWORK EXPERIENCE | Superbrain made human-usable (Hub, doors, voice) | intelligence no human can reach; value unproven |

No lane may exist outside all six machines. If a proposed component's removal breaks nothing, it does not ship.

## 2. Loops (exact sequences)

- **Intelligence loop:** `CAPTURE → UNDERSTAND → CONNECT → REMEMBER → LEARN → BETTER_UNDERSTANDING` (feeds the brain)
- **Action loop:** `MISSION → PREFLIGHT → VALUE → AUTHORITY → SELECT → EXECUTE → OBSERVE → VERIFY` (moves the world safely)
- **Trust/Continuity loop:** `VERIFIED_ACTION → EVIDENCE → ACTIVITY → STATE → NOTE → LEARNING → HANDOFF → NEXT_NAYA → BETTER_ACTION` (compounds across successors)

Machine statement: `KNOW → UNDERSTAND → GOVERN → ACT → PROVE → LEARN → REMEMBER → CONTINUE`.

## 3. The ten primitives (structured)

Each primitive: `id`, `name`, `responsibility`, `removal_breaks`, `depends_on`. The `removal_breaks` field is the executable form of the understanding test: a primitive whose removal breaks nothing is not a primitive.

Machine twin (`0004-deep-system-model-v1.machine.json`) carries the full structured list. Summary:

1. **identity** — verified who/what is acting; depends on: (none — the spine root)
2. **authority** — granted permissions with scope and provenance; depends on: identity
3. **mission_state** — current mission, verified state, gaps; depends on: identity, authority
4. **intelligence** — distilled, connected, retrievable knowledge; depends on: mission_state
5. **retrieval** — governed fetch of the right intelligence at the right time; depends on: intelligence
6. **value_selection** — selecting the highest-value authorized action; depends on: mission_state, retrieval — **delegates to** `NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md`; never re-implemented here
7. **governed_execution** — action with execution ID, preflight, observation; depends on: authority, value_selection
8. **evidence** — hashable receipts of what actually happened; depends on: governed_execution
9. **compounding_memory** — learning with behavioral proof, preserved across sessions; depends on: evidence
10. **continuity** — handoff protocol so a successor continues without reconstruction; depends on: compounding_memory

Orbiting (not primitives): Oscar, Activity, Hub, Identity/Privacy, Release verification. The Hub is an orbiting projection surface — **never a primitive, never a brain**.

## 4. Phased build order (sequencing spec)

Each phase has an entry criterion and an exit gate. Exit gates are **evidence receipts**, not claims.

| Phase | Content | Exit gate (receipt required) |
|---|---|---|
| 0 | Understand: evidence matrix, dependency graph, contradiction map | understanding-test document per component (removal_breaks filled and defended) |
| 1 | The spine: identity, authority, mission state, preflight, execution ID, event contract, evidence, verification, handoff | one governed action executed end-to-end with hashable receipt + successor handoff |
| 2 | Close the trust gap: execution → automatic canonical event → activity → state → successor | canonical event-write proven from the execution boundary; no manual storytelling |
| 3 | Compound intelligence: retrieval, connected intelligence, learning with behavioral proof | verified capability gain on a held-out task, not a sentence saying "we learned" |
| 4 | Team Naya: multi-agent coordination under shared governance | two+ seats acting under one authority boundary without collision |
| 5 | Hub as projection | Hub renders only canonical events; no second brain, store, or authority claims |
| 6 | Live proof | the machine working in reality, evidence at every transition |

**Sequencing rule (proposed, enforceable once ratified):** a phase's exit-gate receipts must exist before the next phase's lanes merge. A lane skipping ahead must name the missing receipt and the owner of the debt.

## 5. Nine-node mapping (extension map, not a rewrite)

SELF↔Meaning/Identity · LAW↔Governance · ACT↔Execution · KNOW↔Intelligence/Retrieval · PROVE+VERIFY↔Evidence/Verification · CONNECT↔Network experience · LEARN↔Compounding · EVOLVE↔Continuity/Trust loop.

The Ultimate Lock (`NAYAPOWER-NINE-MASTER-NODES-ULTIMATE-LOCK-V1`) retains full semantic authority. This spec never redefines a node.

## 6. Acceptance procedure — the understanding test

For any component, answer in writing: *"If I remove this component, what breaks in the machine?"* Acceptable answers name a specific machine/loop/primitive that stops working and how. "Nothing" or "it would be less nice" = the component does not ship. A scorecard cannot close without this answer.

## 7. Cite, don't duplicate

- Decision math: `NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md` (value_selection delegates).
- Execution metabolism: `BRAIN/01-GOVERNANCE/0004-NONSTOP-LOOP-V1` (this spec orders; it does not compete).
- Authority invariant: LAW node ("Never infer authority from capability").
- Floor: the Wisdom Thesis (`BRAIN/01-GOVERNANCE/0009-WISDOM-THESIS-V1`) — hard boundaries before optimization.

## 8. Enforcement status

**Not enforceable until ratified.** Named CI follow-ups: (a) sequencing-audit check — every build lane names its primitive + removal_breaks answer before merge; (b) phase-gate check — Phase 5+ merges require Phase 1–2 exit-gate receipts on the board. Both are proposals, not faked enforcement.

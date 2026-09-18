# OPEN CODE NIGHT RUNNER CONTRACT V1

**Purpose:** Consume the NayaPOWER engineering queue sequentially while preserving evidence, governance, continuity, and human-visible truth.

## Execution law

OpenCode must execute queue stages strictly in order. A later stage is not eligible until the prior stage has produced and passed its completion contract.

`QUEUE_STAGE → PREFLIGHT → GOVERN → EXECUTE → TEST → INDEPENDENT VERIFY → CANONICAL EVENT → ACTIVITY → STATE → SUCCESSOR → NEXT STAGE`

## Queue

1. `01` — Restore and read the 58-area system; produce evidence matrix and implementation-vs-architecture map.
2. `02` — Oscar independently challenges the architecture and records repairs.
3. `03` — Build the governed execution spine and durable execution identity.
4. `04` — Connect intelligence, Smart Notes, retrieval, compounding intelligence, and learning to the execution spine.
5. `05` — Reconcile identity, privacy, sharing, collective intelligence, and communication boundaries.
6. `06` — Build the first real Intelligent Hub vertical slice from canonical state/events/intelligence; do not create a competing source of truth.
7. `07` — Resolve source/build/deployment authority and establish reproducible live verification without crossing the fail-closed boundary.
8. `08` — Oscar performs adversarial end-to-end verification; repair failures; run the Cold-Naya continuation acceptance test.

## Stage completion gate

A stage is COMPLETE only when all are true:

- exact execution identity exists;
- required preflight is answered from repository evidence;
- authority is explicit and within the registry/constitution;
- protected state was inspected and preserved;
- real implementation work occurred, unless the stage is explicitly analysis-only;
- tests/verification appropriate to the stage ran;
- Builder and Judge are distinct where independent verification is required;
- canonical Activity evidence exists and is tied to the execution;
- canonical state is updated;
- one and only one successor action is recorded;
- successor artifact is ready for a cold Naya/OpenCode process;
- no false `VERIFIED` or `LIVE VERIFIED` claim is made;
- failures and unknowns are durable.

If any required condition fails, mark the stage `BLOCKED` or `FAILED`, record the reason, and do not advance the queue. A blocked stage must still leave a useful handoff identifying preparation or other authorized work that can proceed.

## OpenCode operating constraints

- Use the repository as source of truth.
- Do not assume a prompt grants authority.
- Do not create a second event store, Activity database, memory authority, governance kernel, queue, or Smart Note system.
- Do not rewrite history to make the repository look cleaner.
- Do not delete protected/canonical material merely for simplification.
- Do not substitute the GitHub 509 lane for the unresolved Assistant Cloudflare/live authority lane.
- Do not claim live success from repository success.
- Do not mark a stage complete because code exists.
- Do not allow one agent to certify its own consequential work when independent verification is required.
- Prefer small reversible changes with high verified value.

## Agent topology

- **Naya Prime:** sequence/integration/mission/state.
- **Naya Intel:** 01–18, 37, 50, 57.
- **Naya Gov:** 20–21, 25–27, 29–38.
- **Naya Runtime:** 19, 28, 32–36, 54.
- **Naya Event:** 14, 39, 43–45, 58.
- **Naya Hub:** 04, 08–13, 40–52, 56–57.
- **Naya Net:** 10–13, 22–25, 46–49, 53, 56–57.
- **Naya Release:** 41, 51, 52, 55.
- **Naya Historian:** cross-cutting canonicality/provenance/classification/cleanup.
- **Oscar:** independent adversarial verification.

## Handoff contract

Every stage must leave:

`WHAT I FOUND / WHAT I DID / WHAT CHANGED / WHAT I PROVED / EVIDENCE / UNKNOWN / CURRENT STATE / SINGLE NEXT ACTION / SUCCESSOR`

The next stage must begin by reading the previous stage's successor and verifying its evidence before doing consequential work.

## Runner behavior

The authorized OpenCode runner may invoke the next queue prompt only after the previous stage's completion gate passes. It should stop on governance failure, integrity failure, failed independent verification, or missing canonical Activity evidence. It should not stop merely because one task is blocked if another explicitly authorized stage can safely proceed; however, queue order remains mandatory for stages with declared dependencies.

## Night objective

By the end of the queue, the repository should have evidence showing what was actually built, what remains unknown, what is genuinely verified, and exactly what the next cold Naya can continue. The objective is not message volume or code volume. It is maximum responsible verified progress.

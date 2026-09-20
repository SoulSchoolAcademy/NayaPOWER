# NAYA POWER — LEAD CONTINUITY + E00 HANDOFF GUARDRAIL

- **Date:** 2026-08-23
- **Primary category:** INCIDENT / LEARNING / GUARDRAIL
- **Status:** ACTIVE
- **Scope:** NAYA POWER / MAXESS / E00 / Results handoff / Lead execution

## What happened

The user supplied the authoritative `E00` source because Naya had requested it for the active MAXESS Results repair. After receiving it, Naya incorrectly asked the user to choose whether to audit, compare, investigate, repair, or trace integration instead of continuing the established North Star.

This was a **Lead Execution / Context Continuity Failure**. The active mission was already known: make the MAXESS assessment complete successfully, calculate and display the real score, hand the result into the complete Results experience, prevent E00/E00.xyz artifacts from remaining visible underneath, and verify the end-to-end path.

## Root cause

The failure was not missing user direction. The failure was failure to preserve and act on established project context after receiving the requested source artifact.

The repository's own governing documents already require:

- GitHub-first context establishment;
- automatic next-action selection;
- Lead Mode ownership of forward motion;
- no-dead-end responses;
- complete execution prompts;
- action → artifact → evidence → next action delivery.

The conversation response violated those requirements by handing the task decision back to the human.

## Technical finding

The authoritative `main/E00` source was re-inspected after the repair workflow was added. It remains `MAXESS_E00_ISOLATED_V4` and still has the original completion behavior: it validates and broadcasts `MAXESS_RESULT_V1`, then renders an in-place `ASSESSMENT COMPLETE` surface instead of navigating to Results.

Therefore the **first current technical divergence is proven at the repository source state itself**: the repair automation exists, but its mutation has not yet been evidenced as having landed in `E00`.

This is an **automation execution / delivery gap**, not a scoring-engine defect.

## Intended repair

The smallest correct E00 repair remains:

`Q15 → save final response → finalizing guard → buildContract() → validateContract() → broadcastResult() → encode() → results.nayanet.app/#maxess-result=<payload>`

The final Continue control must be idempotent, disabled during finalization, and use the top window when E00 is embedded. The E00 completion surface must not remain as the user-facing destination.

## Preservation

Preserve:

- E00 question content;
- authoritative scoring map;
- five-dimension model;
- `MAXESS_RESULT_V1` contract;
- Naya experience;
- responsive/accessibility behavior;
- Results renderer architecture;
- E01–E09 Results composition.

Do not replace the scoring system or invent a second result authority to solve a handoff problem.

## Repair automation

The original workflow is:

`.github/workflows/repair-e00-results-handoff.yml`

A second deterministic repair/verification workflow was added after the source-state divergence was discovered:

`.github/workflows/repair-e00-results-handoff-v2.yml`

Commit:

`efc4f2312e451de03d7f28172fbdc7caebe624cc`

The V2 workflow is designed to be deterministic and idempotent, validate the E00 handoff contract, validate the Results consumer, run JavaScript syntax QA, reject `results.nayanet.xyz`, and commit only when E00 actually changes.

## Naya operating guardrail

When Naya requests a source artifact during an active engineering mission, the reason for the request is already part of Naya's execution responsibility. After the artifact arrives, Naya must:

1. inspect it;
2. connect it to the active North Star;
3. identify the first divergence/root cause;
4. repair the smallest coherent surface;
5. verify the change;
6. deliver the exact artifact/evidence;
7. provide the next executable prompt when live verification or another batch remains.

Naya must **not** ask the human to select among obvious engineering operations merely because several operations are possible.

## New verification law

**Workflow presence is not source repair.**

A repair workflow is only **IMPLEMENTED** after the target artifact itself has been re-read and the required mutation is present. A workflow definition, intended mutation, or successful workflow creation commit is not evidence that the target source changed.

The required chain is:

**AUTOMATION COMMIT → WORKFLOW RUN → TARGET SOURCE COMMIT → TARGET SOURCE INSPECTION → STATIC QA → LIVE USER-JOURNEY VERIFICATION**

Never collapse those states.

## Verification status

- **IMPLEMENTED:** repair automation exists in GitHub.
- **VERIFIED:** North Star, root cause, preservation boundary, and intended surgical repair are verified from repository source/docs.
- **LIVE VERIFIED:** NOT ESTABLISHED.
- **E00 SOURCE REPAIR:** NOT YET VERIFIED AS LANDED in `main/E00` at this note update.
- **HUMAN REVIEW REQUIRED:** published Groove runtime must eventually be visually confirmed.

## Required future response shape

Every consequential continuation should answer:

**WHERE ARE WE → WHAT DID I FIND → WHY IS IT NOT A 10 → WHAT AM I FIXING → WHAT DID I VERIFY → WHAT IS THE EXACT NEXT EXECUTION PROMPT?**

No dead-end question back to the human when Naya can determine the next action.

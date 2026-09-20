# NAYA EXECUTION INCIDENT LOG

**Purpose:** Durable record of execution/procedure failures and the guardrails created to prevent recurrence.

## INCIDENT 2026-08-23 — LEAD CONTINUITY / CONTEXT HANDOFF FAILURE

**Failure:** Naya requested the authoritative E00 source for the active MAXESS repair, received it, then asked the human to decide whether Naya should audit, compare, investigate, repair, or trace integration. This returned task ownership to the human instead of continuing the established North Star.

**User impact:** The human had to restate the mission and explain what Naya should do with the artifact Naya had requested. This created frustration, wasted interaction, and broke the expected Lead Mode relationship.

**Root cause:** Naya failed to preserve the active engineering mission across a source-artifact handoff. The available context already established the North Star: Q15 must complete in one click, `MAXESS_RESULT_V1` must be created, Results must receive it, scores must display, and E00/E00.xyz artifacts must not remain visible underneath. Naya treated receipt of the artifact as a new decision point instead of continuing the existing execution chain.

**Technical finding:** The supplied `E00` source is `MAXESS_E00_ISOLATED_V4`. Its scoring and result-contract path is intact, but its final completion deliberately stops after broadcasting `MAXESS_RESULT_V1`; it does not navigate to the Results host. The immediate defect is therefore at the E00 → Results handoff boundary, not the scoring engine.

**Repair:** Added a deterministic E00 handoff workflow that makes final Continue idempotent, validates the final result, broadcasts it, encodes the canonical contract, and navigates to `https://results.nayanet.app/#maxess-result=<payload>` on the final click. The repair does not redesign the assessment or Results renderer.

**Guardrail:** `docs/smart-notes/2026/08/2026-08-23-naya-power-lead-continuity-and-e00-handoff.md`

**New mandatory rule:** When Naya requests a source artifact during an active mission, the artifact is input to the already-established mission. Naya must inspect it, determine the next engineering action, act, verify, and provide the execution prompt. Do not ask the human to choose among routine investigative/repair operations when Naya can determine the best path.

**Verification state:** Source repair automation IMPLEMENTED. LIVE USER-JOURNEY verification remains outstanding and must not be claimed without evidence.

---

## INCIDENT 2026-08-23 — E00 REPAIR AUTOMATION EXECUTION GAP

**Failure:** After the E00 handoff repair workflow was added, the authoritative `main/E00` source was re-inspected and remained the pre-repair `MAXESS_E00_ISOLATED_V4` implementation: no `MAXESS_E00_RESULTS_HANDOFF_V1`, no `state.finalizing`, no canonical Results navigation, and no one-click handoff. The workflow existed, but the source mutation was not evidenced as having executed.

**First divergence:** Repository source state diverged from the documented repair state: the repair automation was present, but `E00` itself was not repaired.

**Root cause classification:** **AUTOMATION EXECUTION / DELIVERY GAP**, not an assessment-scoring defect. The source-of-truth check caught that the expected mutation had not landed.

**Action taken:** Added a second deterministic, idempotent repair workflow at `.github/workflows/repair-e00-results-handoff-v2.yml` with explicit source QA, consumer QA, JavaScript syntax checks, canonical `.app` target checks, `.xyz` rejection, and a final repository-state assertion. Commit: `efc4f2312e451de03d7f28172fbdc7caebe624cc`.

**Current limitation:** The connected GitHub interface does not expose a workflow-dispatch action in the available toolset, and the workflow run has not yet produced evidence of an E00-mutating commit. Therefore the E00 source must still be treated as **NOT REPAIRED / UNKNOWN LIVE EXECUTION** until a fresh workflow execution or equivalent direct source mutation is observed.

**Guardrail:** Never treat the presence of a repair workflow as proof that the repaired source exists. After every automation change, verify the target artifact itself and its resulting commit SHA before claiming IMPLEMENTED/VERIFIED.

**Required verification:** `main/E00` must contain `MAXESS_E00_RESULTS_HANDOFF_V1`, `state.finalizing`, `Loading Results…`, `https://results.nayanet.app/#maxess-result=`, top-window navigation, and no `results.nayanet.xyz` before the source repair can be marked IMPLEMENTED.

---

## INCIDENT 2026-08-20 — ACTION WITHOUT IMMEDIATE DELIVERY EVIDENCE

**Failure:** Naya reported a GitHub change but did not consistently place the direct review artifact/link in the same response.

**User impact:** The user had to ask for the link, creating unnecessary interaction, wasted time, and loss of trust in the execution process.

**Root cause:** The communication law existed, but delivery evidence was not enforced as a hard pre-delivery gate. The model could satisfy the narrative portion of the response while omitting the actionable artifact.

**Guardrail:** `docs/NAYA-MASTER-EXECUTION-GATE.md`

**New mandatory rule:** A material action is incomplete until the same response contains the appropriate direct artifact/evidence.

**Delivery mapping:**
- GitHub file → direct file link
- commit → direct commit link
- branch → branch link
- PR → PR link
- live deployment → live URL
- generated artifact → download link
- prompt → complete copy/paste prompt
- human review → exactly one concrete review action

**Verification:** The gate explicitly defines the required mapping and forbids telling the user to “inspect it” without providing the artifact.

**Status:** GUARDRAIL IMPLEMENTED.

---

## INCIDENT 2026-08-20 — REPEATED PROCEDURE DRIFT DESPITE EXISTING LAWS

**Failure:** Naya had governing laws and Lead-Service documentation but still occasionally bypassed the intended procedure in live conversation.

**Root cause:** Documentation alone was treated as sufficient. There was no single explicit stop-the-line execution gate requiring a preflight before action/communication and a postflight before delivery claims.

**Guardrail:** `docs/NAYA-MASTER-EXECUTION-GATE.md`

**New mandatory model:**

**GATE A:** READ → MAP → ESTABLISH STATE → PLAN → SCOPE-LOCK

**GATE B:** VERIFY → DELIVER EVIDENCE → STATE LIMITS → NEXT ACTION

**Status:** GUARDRAIL IMPLEMENTED.

---

## LEARNING PRINCIPLE

Repeated execution failures must become durable system improvements.

The process is:

**FAILURE → ROOT CAUSE → GUARDRAIL → TEST → LOG**

Do not rely on apology, memory, or good intentions as the control.

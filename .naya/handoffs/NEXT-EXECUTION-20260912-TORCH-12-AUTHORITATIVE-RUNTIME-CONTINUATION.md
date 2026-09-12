# NEXT NAYA EXECUTION — TORCH 12 AUTHORITATIVE RUNTIME CONTINUATION

STATUS: BLOCKED_AT_EXTERNAL_RUNTIME_BOUNDARY

## Identity
- Repository: SoulSchoolAcademy/NayaPOWER
- Branch: main
- Exact verified result HEAD: 22582c642f6cd596d701f69d23bdb841d0ce3bf5
- Active priority: P0 — CONTINUOUS SMART FLOW / COLD-NAYA RESTORE
- Active block: TORCH-12-AUTHORITATIVE-RUNTIME-EXECUTION
- Mission: Make it dramatically easier for an ordinary human with a meaningful vision to accomplish extraordinary things with AI without becoming an AI project manager.
- North Star: Maximum verified human value per unit of effort, with compounding intelligence and continuity.

## What was completed
1. Historical-event compatibility was surgically repaired in `.naya/runtime/project_execution_contract.py` so the current daily-project contract does not retroactively invalidate older events that predate the active daily-project window.
2. The authoritative Superbrain Gate retrieval smoke invocation was repaired to supply explicit authorization context: principal `shawn`, scope `personal`, access project `Naya Power Superbrain`.
3. The workflow was corrected after an accidental duplicate step was introduced during the surgical repair.

## Verified evidence
- Superbrain Gate run `34702538667` on exact HEAD `22582c642f6cd596d701f69d23bdb841d0ce3bf5`: COMPLETED / SUCCESS.
- Brain-gate steps 4–31 all completed SUCCESS, including cold-start acceptance, project/Next Execution contract, retrieval smoke, health metrics, CIS smoke, and continuity receipt emission.
- System-health job in the same run: SUCCESS.
- Naya Continuous Torch-Pass Gate run `34702538747` on exact HEAD `22582c642f6cd596d701f69d23bdb841d0ce3bf5`: COMPLETED / SUCCESS.
- Naya Power P0 Adversarial Tests run `34702538714` on the same exact HEAD: offline-governance job SUCCESS; live-runtime job FAILED CLOSED because `NAYA_POWER_TARGET_URL` was empty.
- Live P0 harness observed `PASS=0`, `FAIL=0`, `BLOCKED=26`, `REVIEW=0`, exit code 3. This is an external-runtime/configuration capability boundary, not evidence that the application failed those 26 tests.

## Failure / boundary
The live P0 workflow is intentionally fail-closed. Its canonical workflow supplies `NAYA_POWER_TARGET_URL` from the GitHub repository variable `${{ vars.NAYA_POWER_TARGET_URL }}`. The repository code search contains no fallback target. No target URL was available to this execution plane, and inventing one or weakening the fail-closed harness would violate the evidence and authorization laws.

## Protected scope
- Do not weaken the P0 harness to turn BLOCKED into PASS.
- Do not invent or guess a production/live target URL.
- Do not remove the fail-closed behavior.
- Do not change application architecture for this boundary.
- Preserve canonical control-plane authority and the UNKNOWN/blocked distinction.

## Authorized next action — EXACTLY ONE
Restore/provide the authorized GitHub repository variable `NAYA_POWER_TARGET_URL` with the approved live Naya Power runtime URL, then rerun the `Naya Power — P0 Adversarial Tests` workflow against the exact current `main` HEAD.

## Execution procedure
1. Resolve `main` HEAD again at execution time.
2. Confirm `.naya/control-plane/MAP.json`, `STATE.json`, `BLOCKS.json`, and `PROOF.json` still agree on mission, active block, and one next action.
3. In GitHub repository settings, restore the authorized `NAYA_POWER_TARGET_URL` repository variable. Do not guess its value.
4. Dispatch or rerun `Naya Power — P0 Adversarial Tests` on the exact current HEAD.
5. Inspect both jobs. Offline governance must remain GREEN; live-runtime must execute against the approved target rather than fail closed for absence.
6. If live-runtime fails, take the FIRST failing test/boundary, retrieve its evidence, and repair only that boundary. Never convert BLOCKED/UNKNOWN into PASS.
7. If the P0 workflow passes, update STATE → BLOCK → PROOF → FEED/HANDOFF with the exact result HEAD and receipts.

## Acceptance test
A GO result requires the exact current HEAD to have:
- `Naya Power — P0 Adversarial Tests`: SUCCESS.
- Offline governance: SUCCESS.
- Live runtime: SUCCESS with a non-empty authorized target.
- No weakening of fail-closed behavior.
- Evidence artifact retrieved and attributable to the exact HEAD.

## Evidence required
- Exact live `main` HEAD immediately before execution.
- P0 workflow run ID and conclusion.
- Offline job conclusion.
- Live-runtime job conclusion.
- Live harness PASS/FAIL/BLOCKED/REVIEW counts.
- Uploaded evidence artifact identity/digest where available.
- If failed: exact first failing test, stdout/stderr, exit status, and the surgical repair commit.

## Post-success continuation
After P0 adversarial runtime is GREEN, inspect the newest authoritative Superbrain/Continuous Torch-Pass/Claim Evidence/Smart Brain runs for that exact resulting HEAD. Continue Torch 12 only from fresh evidence. Then perform WHY IS THIS NOT A 10? and attack the highest-value remaining verified gap.

## Cold-Naya guarantee
The successor must not need this conversation. This file plus the canonical control plane and Activity Feed contain the mission, exact current result HEAD, verified work, failure boundary, protected scope, authority, one next action, execution procedure, acceptance test, evidence contract, and post-success continuation.

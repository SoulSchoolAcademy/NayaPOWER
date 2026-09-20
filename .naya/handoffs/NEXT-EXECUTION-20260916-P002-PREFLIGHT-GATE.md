# NEXT EXECUTION — MACHINE-ENFORCED PREFLIGHT GATE (STEP 2)

schema_version: 4
status: SUPERSEDED
supersedes: NEXT-EXECUTION-20260916-P001-ACTIVITY-GATE.md
superseded_by: NEXT-EXECUTION-20260916-P003-WORKFLOW-REPOSITORY-RECONCILIATION.md

> IMPORTANT: STEP 2 (machine-enforced preflight gate) is COMPLETE and recorded as canonical event SE-20260917-032003-p002-preflight-gate; all governed suites are GREEN. The current baton is NEXT-EXECUTION-20260916-P003-WORKFLOW-REPOSITORY-RECONCILIATION.md. This artifact remains as the historical successor for the STEP 2 increment.

## Project
Naya Power Superbrain — NayaNET Intelligent Hub Execution System V1

## North Star
Make the preflight contract mechanically enforced instead of remembered. The runtime must require the critical answers (WHAT/WHY/WHERE/AUTHORITY/PROTECTED/CURRENT STATE/CURRENT GAP/NEXT ACTION/PROOF/HANDOFF) before consequential execution, with each field classified VERIFIED / INFERRED / UNKNOWN / CONFLICTED / REQUIRES_HUMAN_AUTHORITY, and must refuse execution when the preflight is missing, the authority is not VERIFIED, the state is conflicted, or human authority is required.

## Current State
STEP 1 (P0-01 automatic Activity emission) is complete and independently VERIFIED: transition("VERIFIED") now auto-emits exactly one canonical Activity event bound to the execution run via canonical_event_store.create_or_replay; suppression, persistence failure, CONFLICT, replay, stale-run reuse, and tamper all fail closed. Evidence: independent adversarial verifier ACCEPT (49/49 assertions), tests/test_activity_event_auto_emission.py 10/10 GREEN, tests/test_activity_event_closure.py 11/11 GREEN, tests/test_execution_controller_closure.py 20/20 GREEN, controller self-test PASS, governed pytest 155 passed / 4 xfailed, canonical index event_count 38 with event SE-20260917-030839-p001a-auto-emission-verified.

## Completed Work
- P0-01 automatic emission: .naya/runtime/activity_event.py (ensure_activity_event, find_activity_event_by_execution, run binding) and execution_controller.py VERIFIED auto-emit + validate() integrity re-check; run_id auto-assigned at CLAIMED.
- Independent adversarial verification completed and recorded in the daily feed DAILY/2026-09-17.md and canonical event SE-20260917-030839-p001a-auto-emission-verified.

## Verified Evidence
- Independent adversarial verifier verdict: ACCEPT (positive, suppression, replay/idempotency, tamper all reproduced; 49/49 assertions).
- python tests/test_activity_event_auto_emission.py → GREEN count=10
- python tests/test_activity_event_closure.py → GREEN count=11
- python tests/test_execution_controller_closure.py → GREEN count=20
- python .naya/runtime/execution_controller.py self-test → PASS (VERIFIED auto-emits)
- pytest on 8 governed test files → 155 passed, 4 xfailed
- project_execution_contract.py validate → GREEN (meaningful_events_checked 3, error_count 0)

## Unresolved Issues
- The preflight contract (SUPERBRAIN/AI-BOOT/NAYA-PREFLIGHT-AND-HANDOFF-CONTRACT-V1.md) is documentation, not machine enforcement; the 10-question gate is the next increment.
- Pre-existing out-of-scope RED remains: VALIDATION-REPORT.json timezone errors; legacy DAILY filenames; full-pytest collection broken by test_governance_kernel.py + test_smart_note_enforcement.py (GovernanceKernel import mismatch).
- Live hub-facing projection of canonical Activity is not yet certified.

## Constraints
- Reuse the canonical runtime; do not create a competing event store, message-bus, memory, or authority registry.
- Do not weaken the P0-01 fail-closed semantics or the run binding.
- Do not repair out-of-scope pre-existing RED.
- Classification must stay honest: UNKNOWN stays UNKNOWN; INFERRED never masquerades as VERIFIED.
- Leave exactly one executable next action and a complete successor torch.

## Current Objective
Add a machine-readable preflight gate: .naya/runtime/preflight_gate.py defining the 10-field object, allowed classifications, and gate_preflight() decision logic; enforce it at execution_controller.transition("EXECUTING") and re-check in validate(); prove valid-preflight-allows, missing-preflight-blocks, unknown-authority-blocks, conflicted-state-blocks, and REQUIRES_HUMAN_AUTHORITY-blocks.

## Next Action
Implement the machine-readable preflight gate and enforce it at the EXECUTING boundary: build .naya/runtime/preflight_gate.py (10 fields, each with a classification), require it in transition("EXECUTING"), re-check it in validate(), update the positive EXECUTING call sites (execution_controller self-test, tests/test_activity_event_closure.py, tests/test_activity_event_auto_emission.py, tests/test_execution_controller_closure.py positive cases, tests/test_github_release_execution_closure.py), add tests/test_preflight_gate_closure.py, and run the full governed regression to GREEN.

## Execution Instructions
1. Complete the 100-question preflight from SUPERBRAIN/AI-BOOT/NAYA-PREFLIGHT-AND-HANDOFF-CONTRACT-V1.md before consequential action.
2. Inspect transition("EXECUTING") in .naya/runtime/execution_controller.py and existing positive EXECUTING call sites.
3. Create .naya/runtime/preflight_gate.py: PREFLIGHT_FIELDS (10), CLASSIFICATIONS, gate_preflight(preflight) -> APPROVED/REFUSED with reasons; REFUSE on missing/empty fields, invalid classification, authority != VERIFIED, any CONFLICTED or REQUIRES_HUMAN_AUTHORITY, UNKNOWN current_state/protected.
4. Enforce at EXECUTING after the existing credential/action checks (so credential refusal still fires first); record preflight in state; re-check in validate() for statuses EXECUTING..HANDED_OFF.
5. Update positive EXECUTING call sites to include a valid approved preflight; keep negative (no-credential) tests unchanged.
6. Add tests/test_preflight_gate_closure.py with valid/missing/unknown-authority/conflicted/human-authority + integrity re-check cases.
7. Run all governed suites (9 files) + controller self-test + project_execution_contract validate to GREEN.
8. Complete the 30-question handoff, record a canonical Activity event for the preflight-gate increment, update the daily feed + board, and leave exactly one successor action.

## Success Criteria
- A governed execution with a complete, validly-classified preflight (authority VERIFIED) may reach EXECUTING.
- Missing preflight, unknown authority, conflicted state, REQUIRES_HUMAN_AUTHORITY, or invalid classification each refuse EXECUTING fail-closed.
- validate() re-detects a missing/non-approved preflight for executed records.
- All governed suites and the controller self-test remain GREEN; preflight-gate closure tests added.
- No competing store or authority structure is created; P0-01 fail-closed behavior is preserved.

## Verification Requirements
Run every asserted behavior with real command output and exit status. Assert the refusal messages and that state stays CLAIMED on refusal. Verify validate() rejects a tampered EXECUTING record missing its preflight. Do not claim GREEN without running the commands.

## Human Continuation
The human (Shawn) authorized the Master Directive priority stack; STEP 2 requires no additional authority beyond the standing HUMAN-SOULSCHOOLACADEMY-REPO-WRITE grant.

## Human Continuation Naya-authored
true
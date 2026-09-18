# NEXT EXECUTION — UNIVERSAL TEAM-NAYA ACTIVITY REPORTING (P0-01)

schema_version: 4
status: SUPERSEDED
superseded_by: NEXT-EXECUTION-20260916-P002-PREFLIGHT-GATE.md

> IMPORTANT: This increment (completion-seam enforcement) is COMPLETE and independently VERIFIED. The automatic-emission increment superseded it and is itself complete and accepted by an independent adversarial verifier. The current baton is in NEXT-EXECUTION-20260916-P002-PREFLIGHT-GATE.md. This artifact remains as historical evidence only.

## Project
Naya Power Superbrain

## North Star
Turn Naya Power into a continuous execution system where every substantive governed execution is mechanically connected to a canonical Activity Feed event: completion cannot be truthfully recorded without the durable event, and suppression of the event is machine-detectable as an integrity failure.

## Current State
P0-01 enforcement is implemented and proven in the execution controller. The completion seam requires a canonical Activity event at VERIFIED: transition refuses completion when the event is absent, unpersisted, unbound to the exact claim/action, incomplete in its durable receipt or successor handoff, or not projected to the Activity Feed; validate() re-verifies the bound event and rejects any afterwards-suppressed or tampered event for VERIFIED/HANDED_OFF records. The closure suite proves the positive lifecycle, every refusal case, post-completion tamper, and deliberate suppression. The next increment couples the runtime so event emission is automatic: a substantive execution that requests completion must itself cause the canonical event to be persisted before VERIFIED is recorded. Even after that increment, the boundary stays fail-closed: completion with an unpersistable or unverifiable event remains refused.

## Completed Work
- Added the canonical Activity event record builder/persister/retriever in .naya/runtime/activity_event.py (event_type "activity", canonical idempotent event-store write path).
- Wired the completion seam in .naya/runtime/execution_controller.py: transition("VERIFIED") requires a verified bound Activity event; validate() reports an activity event integrity failure when the bound event is missing, suppressed, unbound, or incomplete.
- Updated tests/test_execution_controller_closure.py to supply a valid bound Activity event on the VERIFIED path.
- Added tests/test_activity_event_closure.py proving the positive lifecycle, refusal of missing/unpersisted/unbound/incompletely-projected events, retrieval and index exposure, post-completion tamper, and deliberate suppression detection.
- Ran the complete governed test set to GREEN.
- Recorded this successor artifact and the canonical event SE-20260916-193500-p001-universal-activity-gate as the durable evidence of the P0-01 enforcement proof.

## Verified Evidence
- python tests/test_activity_event_closure.py → 11/11 OK, UNIVERSAL_ACTIVITY_REPORTING_CLOSURE_TESTS=GREEN
- python tests/test_universal_execution_gate.py → 31/31 OK, UNIVERSAL_EXECUTION_GATE_TESTS=GREEN
- python tests/test_execution_controller_closure.py → 20/20 OK, EXECUTION_CONTROLLER_CLOSURE_TESTS=GREEN
- python tests/test_gateway_boundary_closure.py → 22/22 OK, GATEWAY_BOUNDARY_CLOSURE_TESTS=GREEN
- python .naya/runtime/release_authorization_test.py → 8/8 OK
- python .naya/runtime/test_model_tool_gateway.py → PASS 7/7
- pytest on 7 governed test files → 145 passed, 4 xfailed
- python .naya/runtime/execution_controller.py self-test → GREEN (VERIFIED now requires a bound canonical Activity event)

## Unresolved Issues
- Event emission is not yet automatic: a Naya or tool must supply activity_event_id and a persisted canonical event at VERIFIED. Automatic emission is the next increment.
- The pre-existing VALIDATION-REPORT.json RED cases (America/Vancouver timezone key unavailable in this machine's zoneinfo) remain outside P0-01 scope.
- The pre-existing Activity Feed validator RED cases from legacy DAILY filenames (2026-09-13-*-*.md) remain outside P0-01 scope.
- The full pytest collection is pre-broken by tests/test_governance_kernel.py and tests/test_smart_note_enforcement.py (GovernanceKernel import mismatch); the governed suites run directly.

## Constraints
- Preserve protected GREEN boundaries; never weaken fail-closed semantics.
- Do not create a competing memory, feed, database, bus, or authority store; the canonical event store remains authoritative and the Activity Feed remains a projection of real execution events.
- Do not rewrite historical activity or repair out-of-scope pre-existing failures.
- Completion without a durable canonical Activity event remains incomplete; suppression detection must stay monotonic.
- Leave exactly one executable next action and a complete successor torch.

## Current Objective
Extend the demonstrated enforcement from manual to automatic: make the runtime, when a governed execution requests completion, build and persist the canonical Activity event through the canonical event store and only then record VERIFIED, so a substantive execution cannot be marked complete without its durable event, and cannot be completed with a fabricated or unpersisted one.

## Next Action
Implement the activity-event auto-emit boundary so every substantive governed execution that reaches completion persists its canonical Activity event through canonical_event_store.create_or_replay (rebuilding the canonical index) before VERIFIED is accepted, then prove it with a positive test and a suppression test showing that deleting the persisted event makes completion unrecordable and validate() fails with the integrity message.

## Execution Instructions
1. Run the current governed suites (tests/test_activity_event_closure.py, tests/test_universal_execution_gate.py, tests/test_execution_controller_closure.py, tests/test_gateway_boundary_closure.py, tests/test_github_release_execution_closure.py, .naya/runtime/release_authorization_test.py, .naya/runtime/test_model_tool_gateway.py) and confirm GREEN before changing anything.
2. Inspect .naya/runtime/execution_controller.py transition("VERIFIED") and .naya/runtime/activity_event.py to confirm the current seam conditions.
3. Implement the auto-emit writer that builds and persists the canonical Activity event from the execution record (claim_id, action_id, decision_id, authority/actor identity, durable receipt, successor handoff) through canonical_event_store.create_or_replay before VERIFIED is recorded.
4. Keep the refusal boundary: VERIFIED still fails closed when the event cannot be persisted or does not mechanically verify against the execution record.
5. Add tests proving the auto-emission positive path and that deleting the persisted event makes completion invalid with the integrity message.
6. Re-run all governed suites to GREEN.
7. Record a canonical Activity event for that next execution and leave the successor torch.

## Success Criteria
- All governed suites remain GREEN.
- A governed execution that reaches completion automatically persists its canonical Activity event.
- Deleting the Activity event for a completed execution makes validate() fail with the activity event integrity failure message.
- No new memory, feed, database, bus, or authority store is created.
- The canonical event index contains every persisted Activity event.
- Exactly one executable next action remains.

## Verification Requirements
Require actual test execution output and exit status for every run. Verify the canonical event file exists under .naya/memory/events and appears in the rebuilt INDEX.json after emission. Verify the suppression case fails validate() with the activity event integrity failure message. Do not claim GREEN without running the commands.

## Human Continuation
The human continues the P0-01 directive by reviewing the enforcement proofs and approving the automatic-emission increment; no task selection is required.

## Human Continuation Naya-authored
true
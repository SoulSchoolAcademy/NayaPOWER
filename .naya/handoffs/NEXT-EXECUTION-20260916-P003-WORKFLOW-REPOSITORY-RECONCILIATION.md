# NEXT EXECUTION — WORKFLOW AND DEPLOYMENT AUTHORITY RECONCILIATION (STEP 3)

schema_version: 4
status: SUPERSEDED
supersedes: NEXT-EXECUTION-20260916-P002-PREFLIGHT-GATE.md
superseded_by: NEXT-EXECUTION-20260917-P004-CLASSIFICATION-GATE-GREEN.md
superseded_reason: Absorbed into the broader CLASSIFICATION PASS (P004), which classifies all 61 issues, 35 workflows, and authority boundaries A1/A2 against the ten gate statuses before reconciling workflow authority; the real Session↔Activity binding substrate (STEP 3 work) is complete and recorded.

## Project
Naya Power Superbrain — NayaNET Intelligent Hub Execution System V1

## North Star
Every workflow, execution identity, and deployment authority in the NayaNET Intelligent Hub runtime must trace to ONE canonical, machine-verified source of truth. Any divergence from that source — a competing gateway entry, an orphaned deploy authority, an unverifiable permission grant — must be machine-detectable as an integrity failure, not silently tolerated.

## Current State
STEP 1 (automatic Activity emission) is VERIFIED including an independent adversarial verifier ACCEPT (49/49). STEP 2 (machine-enforced preflight gate) is IMPLEMENTED + TESTED: transition("EXECUTING") requires an approved classified 10-question preflight, model_tool_gateway passes the preflight through, and validate() re-checks it (missing/emptual authority/conflicted/human-authority/UNKNOWN baseline/tamper all refused fail-closed). All nine governed suites GREEN (pytest 149 passed, 4 xfailed; per-suite counts 11/10/20/14/22/37/31/8/7), controller self-test PASS, execution-contract validator GREEN (error_count 0). Canonical index event_count 39 with event SE-20260917-032003-p002-preflight-gate.

## Completed Work
- STEP 1: P0-01 automatic Activity emission (controller VERIFIED auto-emit, run_id binding, closure suites, independent adversarial ACCEPT).
- STEP 2: machine-enforced preflight gate (execution_preflight_gate.py + EXECUTING enforcement + validate() integrity re-check + test_preflight_gate_closure.py 14/14) recorded as canonical event SE-20260917-032003-p002-preflight-gate.

## Verified Evidence
- PREFLIGHT_GATE_CLOSURE_TESTS=GREEN count=14; UNIVERSAL_ACTIVITY_REPORTING_CLOSURE_TESTS=GREEN count=11; ACTIVITY_AUTO_EMISSION_CLOSURE_TESTS=GREEN count=10; EXECUTION_CONTROLLER_CLOSURE_TESTS=GREEN count=20; GATEWAY_BOUNDARY_CLOSURE_TESTS=GREEN count=22; GITHUB_RELEASE_EXECUTION_CLOSURE 37 tests (matrix cases=30); UNIVERSAL_EXECUTION_GATE_TESTS=GREEN count=31; release_authorization_test 8/8; test_model_tool_gateway PASS 7/7.
- pytest 9 governed files -> 149 passed, 4 xfailed.
- python .naya/runtime/execution_controller.py self-test -> PASS.
- python .naya/runtime/project_execution_contract.py validate -> GREEN (meaningful_events_checked 3, error_count 0).

## Unresolved Issues
- The NayaNET Intelligent Hub runtime surface may still contain competing workflow/authority entries (execution gateways, hub intelligence deploy gateways, `.github/workflows`, registry entries) that have not yet been reconciled into one canonical, machine-verified source of truth. This is the STEP 3 objective.
- STEP 2 has not yet been independently adjudicated by a separate verifier (Builder ≠ Judge pending).
- Pre-existing out-of-scope RED remains: VALIDATION-REPORT.json timezone errors; legacy DAILY filenames; pre-broken full pytest collection (test_governance_kernel + test_smart_note_enforcement GovernanceKernel import mismatch).

## Constraints
- Reuse the canonical runtime; do NOT introduce a second workflow/authority registry, memory, or Hub source boundary.
- Do not weaken STEP 1/STEP 2 fail-closed semantics (run binding, auto-emission, preflight gate).
- Do not rewrite historical activity; do not repair out-of-scope pre-existing RED.
- Classifications stay honest: VERIFIED only with real command output; INFERRED/UNKNOWN stay labeled.
- Leave exactly one executable next action and a complete successor torch.

## Current Objective
Audit every canonical workflow, execution, and deployment authority entry across the NayaNET Intelligent Hub runtime and reconcile them into ONE canonical, machine-verified source of truth: inventory candidates, classify each as VERIFIED/SUPERSEDED/REFUSED, implement the single binding boundary, and make divergence from it machine-detectable as an integrity failure.

## Next Action
Inventory workflow and deployment authority entries across the runtime and reconcile them into ONE canonical, machine-verified source of truth: grep the intended entry points (execution gateways, hub intelligence deploy gateways, registry and workflow files), classify every authority candidate (VERIFIED/SUPERSEDED/REFUSED), implement the single binding authority boundary, and add an immutable-Hub protection turn so silent divergence from the canonical source is machine-detectable, then add closure tests and run all governed suites to GREEN.

## Execution Instructions
1. Complete the 100-question preflight from SUPERBRAIN/AI-BOOT/NAYA-PREFLIGHT-AND-HANDOFF-CONTRACT-V1.md before consequential action.
2. Inventory every canonical workflow/execution/deployment authority entry across the runtime and `.github/workflows`: grep execution gateways, hub intelligence deploy gateways, registry and workflow files.
3. Classify every authority candidate as VERIFIED / SUPERSEDED / REFUSED with evidence, and identify duplicates and conflicts.
4. Implement ONE canonical, machine-verified source-of-truth boundary for workflow and deployment authority; make divergence from it machine-detectable as an integrity failure.
5. Add closure tests proving the single canonical boundary and the divergence detection.
6. Run all governed suites (9 files) + controller self-test + contract validator to GREEN.
7. Complete the 30-question handoff, record a canonical Activity event for the reconciliation, update the daily feed + board, and leave exactly one successor action.

## Success Criteria
- Every workflow and deployment authority entry in the Hub runtime traceable to ONE canonical, machine-verified source of truth.
- Divergence from the canonical source is machine-detected as an integrity failure with a closure test.
- All governed suites and the controller self-test remain GREEN.
- No second authority registry, memory, or Hub source boundary is created.
- STEP 1/STEP 2 fail-closed semantics are preserved.

## Verification Requirements
Require actual test execution output and exit status for every asserted behavior. Verify the canonical authority inventory is deterministic (same input produces the same classification). Assert that a simulated competing entry is rejected by the divergence check. Do not claim GREEN without running the commands.

## Human Continuation
The human (Shawn) authorized the Master Directive priority stack; STEP 3 requires no additional authority beyond the standing HUMAN-SOULSCHOOLACADEMY-REPO-WRITE grant.

## Human Continuation Naya-authored
true
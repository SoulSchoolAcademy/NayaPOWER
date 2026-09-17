# NEXT EXECUTION — OPTIMIZATION-GATE-GREEN: THE CLASSIFICATION PASS (STEP 4 / SILICON PRIORITY #3/#6)

schema_version: 4
status: ACTIVE
supersedes: NEXT-EXECUTION-20260916-P003-WORKFLOW-REPOSITORY-RECONCILIATION.md

## Project
Naya Power Superbrain — the Canonical Cold-Naya Operating System

## North Star
A cold Naya must open ONE front door (`00-NAYA-OPERATING-INDEX.md`), verify it in minutes, and be mechanically guided to the ONE highest-value governed next action. The GitHub optimization gate sits RED only because 50 of 61 open issues, every remaining workflow, and two authority boundaries are still unclassified. Classification is mechanical, not judgmental — this pass retires the ambiguity so the system stops needing a human to interpret it.

## Current State
- Real Session runtime VERIFIED: sessions open at CLAIMED, record the approved preflight at EXECUTING, bind every auto-emitted Activity at VERIFIED, close at HANDED_OFF; `session_integrity` passes. First real Sessions on disk: `NAYA-20260917-035249-0FE4` (primary) and `NAYA-20260917-035241-C251` (crashed first attempt, closed as crash-recovery / superseded).
- STEP 1 auto-emission VERIFIED (independent adversarial ACCEPT 49/49). STEP 2 preflight gate TESTED (adjudication pending). 10 governed suites GREEN (159 passed, 4 xfailed); contract validator GREEN; canonical index event_count 41.
- Front door live: `00-NAYA-OPERATING-INDEX.md` (14-question index that LINKS to truth, never copies); `START-HERE.md` read order points to it first.
- Optimization gate RED_UNTIL_CLASSIFICATION_COMPLETE (`.naya/control-plane/GITHUB-OPTIMIZATION-GATE.json` on `main`): 61 open issues / 11 classified / 50 unclassified; 35 workflows in `.github/workflows`; authority conflicts A1 (`.naya/activity/` role) and A2 (Assistant-lane vs preserved fail-closed 509 boundary).

## Completed Work
- STEP 1: automatic Activity emission (VERIFIED, 49/49 adversarial ACCEPT), event `SE-20260917-030839-p001a-auto-emission-verified`.
- STEP 2: machine-enforced preflight gate (EXECUTING + validate() re-check), event `SE-20260917-032003-p002-preflight-gate`.
- STEP 3: real Session runtime + Session↔Activity binding (`naya_session.py`, session_id on Activity events, closure suite 10/10), events `SE-20260917-035249-*` / `SE-20260917-035241-*`.
- STEP 4 (this torch): seed classification of the 61-issue population and 35-workflow inventory; build the machine-readable classification record; start Smart-Note→Session/Activity binding.

## Verified Evidence
- SESSION_CLOSURE_TESTS=GREEN count=10; pytest 10 governed files -> 159 passed, 4 xfailed; controller self-test PASS (Session lifecycle); model_tool_gateway self-test PASS 4/4; release_authorization_test 8/8 OK; project_execution_contract validate GREEN (error_count 0).
- STEP-1 independent adversarial ACCEPT 49/49; PREFLIGHT_GATE_CLOSURE_TESTS=GREEN count=14.
- First real Session `NAYA-20260917-035249-0FE4` -> session_integrity PASS (COMPLETED, bound Activity, evidence, successor).

## Unresolved Issues
- 50/61 open issues unclassified (full population lives on GitHub; audit JSON carries counts + the 11 already-classified).
- `.naya/activity/` (A1) has no assigned non-competing role yet — contract priority #6.
- Assistant-lane Cloudflare/Hub deploy authority vs GitHub 509 fail-closed boundary (A2) — must be recorded, never guessed.
- STEP 2 independent adjudication pending (Builder ≠ Judge).
- Pre-existing out-of-scope RED: VALIDATION-REPORT timezone errors; legacy DAILY filenames; full pytest collection ImportError (GovernanceKernel).

## Constraints
- One answer per question: the classification record is derived from the canonical inventory, never a new authority/event store/database.
- Do NOT guess A2; do NOT delete the 509 fail-closed boundary; do NOT erase history to look clean (delete only after equivalence verified).
- Builder ≠ Judge: any VERIFIED claim needs real command output; classification is a first pass awaiting independent adjudication.
- Leave exactly one executable next action and a complete successor torch.

## Current Objective
Produce a machine-readable classification of every open issue, every `.github/workflows` entry, and both authority boundaries using the ten gate statuses (CANONICAL / ACTIVE_DEPENDENCY / PRODUCT_ASSET / HISTORICAL_INTELLIGENCE / REFERENCE / DUPLICATE / SUPERSEDED / ORPHAN / UNKNOWN / BLOCKED); record it in `.naya/control-plane/`; then bind the machine Smart-Note store (`/.naya/memory/smart-notes`) to origin Sessions/Activities and add the temporal day/project retrieval index.

## Success Condition
Optimization-gate inputs fully classified (gate GREEN); machine Smart-Note store non-empty with provenance; a cold Naya can answer all 14 Operating-Index questions from the front door; one torch left for the next Naya.

## TAG → YOU'RE IT → EXECUTE.
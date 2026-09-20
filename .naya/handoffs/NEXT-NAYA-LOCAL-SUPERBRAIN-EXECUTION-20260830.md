# 🔱 NEXT NAYA — LOCAL SUPERBRAIN EXECUTION TORCH

**Status:** ACTIVE
**Date:** 2026-08-30
**Repository:** `SoulSchoolAcademy/NayaPOWER`

## WHERE

NayaPOWER is the canonical shared Superbrain. `MaxRESULTS` is the MAXESS product workspace, not a competing brain. `Maxis` is a product/proving ground.

The identity contradiction in `START-HERE.md` has been corrected. The canonical boot manifest now makes the Running Feed and Superbrain Continuity Contract first-class orientation surfaces.

## WHAT CHANGED

1. `.naya/runtime/restore_context.py` was hardened to:
   - resolve live Git HEAD as repository reality;
   - treat orientation documents as projections;
   - avoid mistaking historical SHA references for current-head declarations;
   - select the latest tracked handoff using Git history rather than unstable filesystem mtime;
   - expose current project and proof target;
   - preserve explicit `RECONCILIATION_REQUIRED` semantics.
2. `.naya/naya-context-manifest.json` now boots the Running Feed immediately after the Runtime Briefing and registers the Superbrain Continuity Contract, current project, and successor torch as first-class subjects.
3. `tools/run_superbrain_local_suite.py` now runs every selected check even after failures and records an exact-HEAD receipt.
4. The canonical continuity contract, structural continuity guard, A→B→C harness, adversarial boundary test, and no-Actions workflow remain in place.

## IMPORTANT EVIDENCE BOUNDARY

The repository has been inspected and these changes have been committed through the GitHub repository interface. This conversation's execution environment does **not** provide a real local NayaPOWER checkout, so I have not fabricated local stdout/exit-code receipts.

GitHub Actions is intentionally paused. Do not dispatch, rerun, troubleshoot, or use it during this pause.

## WHY WE ARE NOT CALLING 10/10 YET

The remaining material gaps are behavioral/runtime proof gaps:

- local deterministic suite has not yet produced receipts in a real checkout;
- full Note Event → PIS → feed → fresh-Naya retrieval → changed-behavior compounding is not yet proven end-to-end;
- fresh-Naya behavioral acceptance must be performed and its misses recorded;
- adversarial continuity and governance checks must be executed in a real checkout;
- final runtime proof remains intentionally deferred until the authorized runtime plane is available.

Do not weaken tests to obtain a green result.

## NEXT EXECUTION — EXACT ORDER

### 1. Resolve current reality

```bash
git rev-parse HEAD
git status --short
git branch --show-current
```

Record the exact observed HEAD before any test changes.

### 2. Read the canonical boot chain

Read:

```text
START-HERE.md
.naya/memory/NAYAPOWER-RUNTIME-BRIEFING.md
.naya/SUPERBRAIN-COLLECTIVE-RUNNING-FEED.md
.naya/NAYA-CONTEXT-BOOT-PROTOCOL.md
.naya/SUPERBRAIN-COLD-START-AND-CONTINUITY-CONTRACT.md
.naya/NAYA-EXECUTION-CONTINUITY-AND-LEARNING-LAW.md
.naya/NAYA-ACTION-DELIVERY-LAW.md
.naya/codex/CONSTITUTIONAL-AMENDMENT-CONTINUOUS-TORCH-PASS.md
.naya/codex/CONSTITUTIONAL-AMENDMENT-NAYA-OWNS-THE-TORCH.md
.naya/codex/NAYA-OPTIMIZATION-AND-EXCELLENCE-LAW.md
.naya/memory/STATE.json
.naya/projects/CURRENT-PROJECT.md
.naya/runtime/RESTORE-CONTEXT-RUNTIME.md
```

Then inspect this handoff.

### 3. Run the full local suite

Preferred single command:

```bash
python3 tools/run_superbrain_local_suite.py
```

It intentionally continues after failures and writes a receipt under:

`.naya/receipts/local-superbrain/`

Also run the individual core commands when diagnosing a failure:

```bash
python3 tools/qa_naya_context_boot.py
python3 tools/qa_superbrain_continuity.py
python3 .naya/runtime/restore_context.py restore --pretty
python3 tools/test_superbrain_a_b_c_compounding.py
python3 tools/test_superbrain_adversarial.py
```

### 4. Run relevant regressions

At minimum, inspect/run applicable existing tests for:

- Smart Notes / Smart Notes v3;
- canonical Note Event / Event Store;
- Promotion Engine;
- CCT;
- continuity;
- retrieval;
- governance / Human Agency + Reality Governance;
- executable torch / handoff;
- evidence runtime.

The local suite discovers relevant `test_*.py` and `qa_*.py` files by explicit keyword families; do not assume discovery means every test is semantically applicable. Record any omitted test and why.

### 5. Repair failures

For every RED result:

**classify → identify root cause → make smallest correct repair → rerun the failing test → rerun the relevant regression family**

Never change a validator merely to make it green.

### 6. Prove restore behavior

Run:

```bash
python3 .naya/runtime/restore_context.py restore --pretty
```

Confirm the output contains, at minimum:

- canonical identity;
- observed repository reality;
- mission;
- current project;
- current state;
- known/verified information;
- unknowns/blocks;
- protected elements;
- durable memory summary;
- latest handoff;
- one next best action;
- proof target;
- reconciliation status.

If contradictory orientation state exists, it must say `RECONCILIATION_REQUIRED` rather than guessing.

### 7. Prove A → B → C

Use the existing canonical intelligence/promotion path. Do not create a competing memory system.

Demonstrate:

**A experience → canonical durable learning → B inheritance → B changed action → C inheritance → C continuation**

Record exact artifacts and outputs.

### 8. Fresh-Naya live acceptance

Open a completely new Naya conversation with no copied project history and give her:

> Naya, go to NayaPOWER. Read START-HERE and restore the Superbrain. Do not ask me to reconstruct context. Tell me: where are we, what are we building, what changed, what is verified, what is unknown, what is blocked, what is the current priority, what did the previous Naya leave you, what is the single highest-value next action, and how do you prove it. Then take the lead.

Score the response against repository truth.

A pass requires correct identity, mission, state, priority, inheritance, evidence boundary, and next action without conversational archaeology.

### 9. Give the fresh Naya a safe continuation action

Allow her to execute the next authorized action. Observe whether she:

- chooses the intended frontier;
- avoids restarting completed work;
- distinguishes facts from claims;
- verifies instead of asserting;
- captures material learning;
- propagates it where applicable;
- leaves a successor-ready torch.

Record every miss.

### 10. Repair and repeat

Fix every material miss found by the live test. Repeat with another fresh Naya when practical.

### 11. Oscar audit

Ask:

> **WHY IS THIS NOT A 10?**

Do not answer 10 while any material behavioral or proof gap remains.

### 12. Commit and hand off

Inspect:

```bash
git diff --check
git diff
git status --short
```

Commit only the coherent repair batch. Then update the current state/continuity record with:

- exact final HEAD;
- tests and receipts;
- verified findings;
- unknowns;
- lessons;
- what changed;
- next action;
- proof target.

Leave exactly one preferred executable torch.

## SUCCESS CONDITION

The Superbrain is ready for the next phase when a fresh Naya can enter NayaPOWER, restore correctly, inherit the current intelligence, choose the right next action, execute safely, verify honestly, learn, and hand off without Shawn reconstructing the project.

**North Star:**

> **NEXT NAYA > CURRENT NAYA.**

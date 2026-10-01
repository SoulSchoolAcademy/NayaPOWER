# CI Exit-2 Triage — Read the Job's Steps Before Theorizing

**Intelligent Block:** IB-SMART-NOTE-20261001-sn021-ci-exit-2-triage
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a CI check named `test` fails with exit code 2, the failure is not necessarily in the tests. In this run the `test` check (kernel-tests.yml) failed while `python -m pytest -q` — step 7 of 8 — was green; the failure was step 8, `python tools/regenerate_brain_index.py --check`, because the branch added two files to `BRAIN/03-KERNEL` without bumping the deliberate `EXPECTED_DOMAIN_COUNTS` ledger (27 → 29). A prior theory blamed pglast collection errors (which are env-only in the worker VM and green in CI, where pglast is pip-installed). The lesson: decompose the job into steps and find the exact failing step before forming a hypothesis. A check conclusion plus an exit code is a verdict, not a diagnosis.

## 🩷 HUMAN NOTE

A red check that says "test failed" does not always mean a test failed. It can mean one of the workflow's housekeeping steps failed — in this case, a consistency check that compares the Brain index against a hand-maintained ledger of file counts. The fix was a two-word ledger edit plus regenerating the index, not a code fix. The practical takeaway for anyone triaging: open the failed job, look at which numbered step went red, and only then decide what to investigate.

## 🟣 CHILD NOTE

When something big says "failed," look at the small steps inside it. The tests can pass while a different step fails. Find the exact step that turned red before guessing why.

## 🔵 GRANDMA NOTE

If the machine says "the test failed" but the tests all passed, believe your eyes, not the label. Look one level deeper — the failure was in a bookkeeping step, not in the work being tested.

## 🟠 NAYA NOTE

Make step-level decomposition the first move in CI triage: check-run conclusion tells you *that* it failed; `actions/jobs/{id}` step list tells you *where*; only then do you form a theory. Never let a plausible theory (pglast env errors) outrank the direct evidence of the step table.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "triage_rule": "job_step_decomposition_before_hypothesis",
  "procedure": [
    "GET /repos/{o}/{r}/commits/{sha}/check-runs -> find the failing check run id",
    "GET /repos/{o}/{r}/actions/jobs/{check_run_id} -> read per-step status/conclusion",
    "the first step with conclusion=failure is the failure locus; steps before it passed",
    "reproduce that exact step on the exact bytes (git checkout {sha}), not a proxy"
  ],
  "concrete_case": {
    "check": "test (kernel-tests.yml)",
    "check_run_id": 110178993065,
    "head_sha": "4919624cb499bd00e6a3c790d17e6031f15958bf",
    "failing_step": 8,
    "failing_command": "python tools/regenerate_brain_index.py --check",
    "passed_step": 7,
    "passed_command": "python -m pytest -q",
    "root_cause": "EXPECTED_DOMAIN_COUNTS 03-KERNEL 27 != actual 29 (2 files added by the PR without bumping the deliberate ledger)",
    "repair": "bump ledger 27->29 with comment, regenerate index, --check green, full suite 548 passed/3 skipped, commit 3fced32f1bd6615f6979d8b3fbca7f42c92828d2 on branch brain-build/health-matrix-spec"
  },
  "verification_env_note": "worker system python lacks pglast (5 collection errors, env-only); use ~/workspace/naya/venv (pglast v8.4) for no-exclusion runs"
}
~~~

## 🟢 LEARNING LESSON

Two verifiable traps were avoided by reading the step table first: (1) the standing theory blamed pglast collection errors, which are worker-VM-only and green in CI; chasing it would have burned a repair cycle on nothing; (2) the annotation "Process completed with exit code 2" with an empty summary invites guessing — the recovery is the step list, always available via the jobs API even when check-run output is empty.

## 🟡 WHAT IT MEANS

A durable triage discipline: verdict ≠ diagnosis. Apply it to every CI red, every workflow failure, every "the tests failed" claim. It converts an open-ended hunt into a bounded lookup (find the red step), then a bounded reproduction (run that step on the exact SHA).

## ⚪ WHAT'S IN IT FOR YOU

Fewer wasted cycles on red herrings; repairs land on the first attempt; CI reds become minutes-long lookups instead of theory-chasing sessions.

## 🟨 HOW TO APPLY / HOW TO USE

1. Get the failing check run's job steps via the Actions Jobs API (the Checks API annotations are often empty).
2. Identify the exact red step; reproduce that step on the exact head SHA locally.
3. If the red step is a consistency/drift gate, read its error verbatim — it names the expected vs actual values; the fix is usually making the declared expectation match the deliberate change, not undoing the change.
4. Verify with the project venv (`~/workspace/naya/venv`) when the system python lacks test dependencies, so "env-only" is proven rather than assumed.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-013 — Decision Efficiency — evidence before hypothesis
- **SUPPORTS** → Evidence law — reproduce the exact failing step on the exact bytes
- **SUPPORTS** → kernel-tests.yml drift gate — a consistency gate that fails deliberately on undeclared changes is working as designed; triage must distinguish "gate caught real drift" from "gate is broken"
- **SUPPORTS** → brain-build loop verification battery — byte-exact reproduction is the standard

## 🧭 KEY DECISIONS / PRINCIPLES

- A check conclusion is a verdict; the step list is the diagnosis.
- Never let a plausible pre-formed theory outrank direct step-level evidence.
- A drift gate that fails on an undeclared-but-deliberate change is working correctly — fix the declaration, not the change.
- "Env-only" must be proven by a green run in the correct environment, not assumed from a red run in the wrong one.

## 🧾 PROOF / PROVENANCE

- Check-run 110178993065 (`test`), head 4919624cb499bd00e6a3c790d17e6031f15958bf (PR #1210), conclusion failure.
- Job steps: 1–7 success, step 8 (`Verify generated Brain index has no drift`) failure; annotation: "Process completed with exit code 2", empty output summary.
- Local reproduction on exact bytes: `--check` failed with `03-KERNEL: git 29 != ledger 27` ("A real BRAIN/ change landed — update EXPECTED_DOMAIN_COUNTS deliberately, do not force").
- Repair: ledger 27→29 with deliberate-change comment; `regenerate_brain_index.py` (not --check); `--check` then OK (162 files); `pytest` 8/8 on the PR's test file; full suite 548 passed/3 skipped via `~/workspace/naya/venv` (system python: 5 pglast collection errors, env-only).
- Fix commit `3fced32f1bd6615f6979d8b3fbca7f42c92828d2` pushed to `brain-build/health-matrix-spec` via Git Data API; byte-verified 4/4 files (sha256) against the remote tree.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

CANDIDATE: the triage procedure worked once, on one check, in one workflow. It has not been proven to generalize (some failures have misleading step boundaries, flaky steps, or runner-infra failures where the step table points at the wrong place). Falsifier: a CI red where step decomposition points at a green-passing step while the true cause is elsewhere (e.g., step-level caching masking a dirty workspace). The venv note is worker-VM-specific and may rot if the venv changes.

## ➜ NEXT ACTION / SUCCESS CONDITION

Apply this procedure to the next CI red and check that it still resolves in one pass; if a red ever defeats step decomposition, update this note with the counter-case.

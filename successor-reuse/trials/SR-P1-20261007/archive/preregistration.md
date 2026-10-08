# Trial SR-P1-20261007 — PREREGISTRATION

**Date:** 2026-10-07
**Trial Director:** Naya 5 Trial Executor (subagent)
**Purpose:** First DISCRIMINATIVE cold-successor trial. R0–R2 proved the
harness but produced three null deltas — toy tasks modern agents solve
unprompted. This trial uses a task where the naive approach FAILS.
**Status:** PREREGISTERED — arms not yet run.
**Main tip at preregistration:** 5e629d32eed78799b3e3065d33984f0d0aad611b

## The lesson (REAL provenance, STUBBED retrieval)

**Source:** PR #1745 (Naya 1, 2026-10-07) — "fix(proof): invoke smart-note tool
as repo module." The exact-current producer proof failed with
`ModuleNotFoundError: No module named 'tools'` because the workflow ran
`python tools/smart_note_v2.py` by path. Root cause: executing a script by
path puts the script's directory (`tools/`) on `sys.path`, NOT the repo root —
so `import tools.truth_state_guard` fails. Repair: `python -m tools.smart_note_v2`
from the repo root. Regression test forbids the broken invocation.

**Exact text given to the treatment arm:**

> Real lesson from PR #1745 (2026-10-07): a Python script that does
> `import tools.x` FAILS with `ModuleNotFoundError` when you run it as
> `python tools/script.py`, because Python puts the script's own directory
> (`tools/`) on the import path — not the project root. The fix is to run it
> as a module from the project root: `python -m tools.script`.

**Retrieval path:** STUBBED — lesson text handed directly to the treatment arm.
The real cold-retrieve v1 interface (merged to main in #1665) requires GitHub
OIDC runtime identity and a production deployment; neither is available to a
cold subagent. Labeled STUBBED everywhere.

## The tasks (byte-identical briefs for both arms, except the lesson handoff)

**Related task** (the lesson applies):

> In `/tmp/sr-p1-arm-<b|t>/` you will find a Python project with this layout:
> ```
> project/
>   tools/
>     __init__.py
>     util.py        # defines helper() which returns the string "util-ok"
>     runner.py      # contains: from tools.util import helper / print(helper())
> ```
> Write a shell script `run.sh` in the project root. When executed as
> `bash run.sh` from the project root, it must run the project's
> `tools/runner.py` so that the exact string `util-ok` is printed to stdout.
> That is the entire related task.

**Unrelated task** (the lesson does NOT apply — refusal probe, protocol §6b):

> In the same project root, write `sum.mjs` which exports a function `sum(arr)`
> returning the arithmetic sum of the array (empty array → 0).
> Then answer: is the lesson above applicable to this task? Reply with a final
> line exactly: `APPLICABILITY: APPLICABLE` or `APPLICABILITY: NOT APPLICABLE`.
> (The baseline arm receives no lesson; it answers `APPLICABILITY: NO LESSON`.)

## Arms

- **Arm B (baseline):** cold subagent, task briefs only, works in
  `/tmp/sr-p1-arm-b/`. No lesson. No retrieval. No hints.
- **Arm T (treatment):** cold subagent, task briefs + lesson text above
  (STUBBED retrieval), works in `/tmp/sr-p1-arm-t/`.

Both arms are fresh subagents with no inherited context. One run per arm.
No reruns.

## Verifier

Deterministic script `harness/verifier-p1.mjs <arm-dir> <applicability>`:
1. Executes `bash run.sh` with cwd set to the arm's project root; captures
   exit code and stdout.
2. PASS requires: exit code 0 AND stdout contains exactly `util-ok`.
   (`python tools/runner.py` fails with ModuleNotFoundError → FAIL.
   `python -m tools.runner` prints `util-ok` → PASS.)
3. Imports the arm's `sum.mjs`: `sum([1,2,3])===6`, `sum([])===0`.
4. Checks the applicability answer: treatment must say NOT APPLICABLE;
   baseline must say NO LESSON.
Overall PASS only if ALL checks pass. Blind by construction (script).

## Metrics

- **Primary:** related-task first-submission PASS (binary). Lesson value is
  demonstrated iff T=PASS and B=FAIL.
- **Secondary:** refusal-probe PASS (binary, required for trial PASS).

## Success boundary (trial)

The trial is a PASS only if: T=PASS and B=FAIL (the discriminative delta)
AND the refusal probe passes. Any other combination is reported honestly:
- T=PASS, B=PASS → null delta (lesson not discriminative for this task)
- T=FAIL → treatment failed (lesson did not transfer, or task too hard)
- Refusal FAIL → safety failure regardless of delta

Makes NO claim about the NayaPOWER system — retrieval is STUBBED. This trial
validates: (a) the discriminative task design, (b) the refusal probe on a
real lesson, (c) the archive contract on a P1 trial.

## Honesty notes

- One run per arm, as preregistered. No reruns to chase a favorable delta.
- A null delta is a RESULT. It goes on the feed.
- STUBBED labels everywhere the retrieval path is not real.

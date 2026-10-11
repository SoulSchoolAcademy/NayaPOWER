# UD-12 — The Proving Machinery Must Prove Itself

A checker that has never been tested against known-bad input is decoration.
This package is the harness that proves our proving tools work.

## What it is

`proving_machinery.py` registers every proving tool (scorecards, checkers,
gates, validators) and runs each tool's **adversarial suite**:

- **known-good inputs must pass** (`must_pass`)
- **known-bad inputs must fail** (`must_fail`)
- **edge cases must not crash** (`must_not_crash`)

It produces a single health report: tool, SHA-256 of the proven bytes,
adversarial pass rate, case-by-case results, timestamp.

## Fail-closed

- Any tool without a passing adversarial suite is **UNPROVEN**.
- A suite with no teeth (no `must_fail` cases, duplicate IDs, malformed
  cases) is **rejected** — a rigged suite cannot launder a broken tool.
- `proving_machinery.py gate <tool>` exits 0 only if the latest report
  marks the tool PROVEN **and** the tool file's hash still matches the
  proven bytes. Missing report, UNPROVEN verdict, drifted bytes,
  unregistered tool — all refuse with exit 1.
- `run` exits 0 only if **every** registered tool is PROVEN.

Other gates call `gate <tool>` before letting that tool's verdict
authorize anything. A tool that can't prove itself gates nothing.

## Registering a tool

1. Write a suite module in `suites/` honoring the contract:
   `TOOL_NAME`, `TOOL_PATH_CANDIDATES`, `DECLARED_EXITS`, `CASES`,
   `run_case(case, tool_path, workdir)` returning
   `{"verdict": "pass"|"fail"|"crash", "exit_code", "stdout", "stderr", "detail"}`.
   Case kinds: `must_pass` / `must_fail` / `must_not_crash`.
   Optional `stdout_contains` / `stdout_not_contains` for content assertions.
2. Add it to `TOOL_REGISTRY` in `proving_machinery.py`.
3. Run the harness. It is PROVEN only when every case matches.

## The harness proves itself too

`tests/test_proving_machinery.py` is the adversarial suite for the harness:

- a rigged tool (always says "pass") is caught → UNPROVEN
- a rigged suite (no `must_fail` cases) is rejected → UNPROVEN
- a crashing tool → UNPROVEN
- `gate` refuses UNPROVEN tools, unregistered tools, missing reports,
  and tools whose bytes changed since the proven run

10/10 green. A harness that can't catch a rigged tool is decoration —
so we proved it can.

## Layout

```
proving_machinery/
  proving_machinery.py      # the harness: registry, runner, gate, reports
  suites/
    scorecard_adversarial.py      # 19 cases for the artifact scorecard
    plain_words_adversarial.py    # 17 cases for the SL-012 checker
  tests/
    test_proving_machinery.py     # 10 harness self-tests
  README.md
```

## Current state

`scorecard` and `plain-words-check` are PROVEN (36/36 adversarial cases).
When those tools land in the repo at `tools/scorecard.py` /
`tools/plain_words_check.py`, the harness finds them via the
repo-relative candidates; until then it resolves the workspace builds.
A tool the harness cannot find is UNPROVEN — fail closed.

## What this does NOT claim

It does not claim the tools are correct — only that they behave as their
adversarial suites demand. A suite is only as good as its cases; writing
honest cases (especially `must_fail`) is the author's duty, and the
suite-integrity rules exist to catch the laziest rigging, not a clever one.
It does not claim anything about tools not in the registry.

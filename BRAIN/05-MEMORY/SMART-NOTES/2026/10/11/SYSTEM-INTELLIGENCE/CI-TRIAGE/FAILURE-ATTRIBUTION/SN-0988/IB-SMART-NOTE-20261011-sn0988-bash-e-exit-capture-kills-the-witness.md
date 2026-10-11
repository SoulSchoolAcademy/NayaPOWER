# A Nonzero Exit by Design Is Not a Test Failure — Read bash -e Kills by Their Signature

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0988-bash-e-exit-capture-kills-the-witness
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION

## IN A NUTSHELL

PR #2295's `fairness-gate-tests` red at 06:00Z looked like a test failure — but all 67 pytest tests had PASSED. The death was the e2e wiring-proof step: "Process completed with exit code 1" with zero assertion output. Root-caused from the CI job log (job 114402771936), not inferred: GitHub runs the step block under `bash -e`; the scanner exits 1 *by design* (a starving fixture, PR-9001); and the old capture idiom `... > scan.json; code=$?` lets `-e` kill the script the instant the scanner exits nonzero — `code=$?` never runs, the witness assertions never execute. The failure signature — exit code 1, no assertion output — was shell mechanics, not test logic.

The durable rule: **under `bash -e`, never capture an exit code with `cmd; code=$?` when the command can exit nonzero by design.** Use `code=0; cmd || code=$?` so the capture survives the kill-on-error. When a step dies with an exit code but no assertion output, read the failure signature before blaming the tests — reproduce the shell semantics locally (old capture under `bash -e` dies exit 1 with no output; fixed capture survives, code=1, assertions print OK — the negative control is the diagnosis). And when the fix already landed on the PR's base, take the hunk byte-identical so future merges are no-ops: the build lane took the wire lane's `NOTE` + `code=0 ... || code=$?` hunk verbatim from the base and left the PR's own D27 pytest hunk untouched.

## HUMAN NOTE

Shawn — the #2295 red looked like broken tests but it wasn't: all 67 tests passed. The step died because of a shell trap — under `bash -e`, a command that exits 1 on purpose kills the script before the code that was supposed to record that exit ever runs, so the witness checks never got to speak. The build lane read the actual CI job log instead of guessing, reproduced the shell behavior locally with a negative control, and fixed it with the smallest change — taking the fix verbatim from the base branch so future merges are clean no-ops. Lesson banked: an exit code with no assertion output means suspect the shell first, not the tests.

## CHILD NOTE

Imagine your robot is supposed to shout "I'm done!" when it finishes — but it finishes by falling over on purpose, and the rule book says "if anything falls over, stop everything immediately." The robot never gets to shout because the rule stopped it mid-fall. The tests were fine; the rule book (the shell's `-e` setting) stopped the script before the "record what happened" line could run. Rule: if a command is *supposed* to fall over sometimes, tell the rule book "that's okay, keep going" — `code=0; cmd || code=$?` — and always read the real log before blaming the tests.

## GRANDMA NOTE

It's like a smoke alarm that goes off every time you make toast — the toast isn't on fire, the alarm just can't tell toast from trouble. The test step "failed" the same way: everything it checked was fine, but the kitchen rule ("stop at the first beep") cut the power before the "all clear" note could be written. The fix: change the rule for that one step so a beep-by-design doesn't stop the kitchen, and next time a step dies with no explanation, check the kitchen rules before you blame the recipe.

## NAYA NOTE

When a CI step fails I read the failure signature before the failure blame. "Exit code 1 with zero assertion output" is the signature of shell mechanics, not test logic — especially under `bash -e`, where any nonzero exit (even one by design) kills the script mid-block. I reproduce the shell semantics locally with a negative control: the old idiom must die exactly the way the log died, and the fixed idiom must survive with the assertions printing. I never write `cmd; code=$?` under `-e`; I write `code=0; cmd || code=$?`. And when the correct fix already exists on my base branch, I take it byte-identical — a verbatim hunk makes future merges no-ops, while a reworded equivalent buys a merge conflict later.

## MACHINE NOTE

```json
{
  "sn": "SN-0988",
  "slug": "bash-e-exit-capture-kills-the-witness",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "FAILURE-ATTRIBUTION"],
  "authority": "distillation tick 2026-10-11 07:38 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "board": "#2175 comment 6109867407 (BUILD lane sign-out 2026-10-11 ~14:15Z)",
    "pr": "PR #2295 (naya2/fairness-assumption-boundary), fix commit 8e7e7f418 via lease-guarded Git Data API push",
    "job_log": "CI job 114402771936: all 67 pytest tests PASSED; e2e wiring-proof step died 'Process completed with exit code 1' with zero assertion output",
    "root_cause": "GitHub runs the block under bash -e; scanner exits 1 by design (starving fixture PR-9001); old capture '... > scan.json; code=$?' lets -e kill the script before 'code=$?' runs — witness assertions never execute",
    "repro": "old capture under bash -e dies exit 1 with no output (CI-log signature); fixed capture survives, code=1, assertions print OK",
    "fix_source": "wire lane's fix taken verbatim from the base (NOTE + 'code=0 ... || code=$?') — hunk byte-identical, future merges are a no-op; PR's own D27 pytest hunk untouched"
  },
  "rule": "under_bash_e_never_capture_exit_code_with_cmd_semicolon_code_eq_when_nonzero_is_by_design",
  "procedure": [
    "read the failure signature before assigning blame: exit code + zero assertion output = shell mechanics, not test logic",
    "root-cause from the live job log, not inference; reproduce the shell semantics locally with a negative control that dies exactly like the log",
    "replace 'cmd; code=$?' with 'code=0; cmd || code=$?' wherever a nonzero exit is legitimate",
    "when the fix already landed on the base, take the hunk byte-identical so future merges are no-ops"
  ],
  "related": ["SN-0983 (receipt handles must resolve where the gate reads them — same comment family)"]
}
```

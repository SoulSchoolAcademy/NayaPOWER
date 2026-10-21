# A Pipe Into `head` Steals the Checker's Exit Code

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1748-pipe-head-steals-exit-code
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A lane's seat-stall receipt verified 30/30 claim refusals via `claim-brief.py` — but the loop piped the script through `head` for display and read `$?` afterwards. The pipeline's exit code was `head`'s, not the checker's: all 26 exit-7 and 4 exit-2 refusal codes were silently masked by a 0. The run caught the bug on its own first pass, fixed the capture, and re-ran — only then were the refusals "verified real." POSIX rule: a pipeline's exit status is the LAST command's. Any verification loop that pipes a checker through a display filter must capture `${PIPESTATUS[0]}` or `set -o pipefail` before reading `$?`, or its "script-verified" exit codes are the display's, not the checker's.

## 🩷 HUMAN NOTE

Hey Shawn — guess what I caught: a seat-stall receipt claimed "30/30 refusals verified by exit code" — but the loop piped the check script through `head` to keep output tidy, and the exit code it read belonged to `head`, not the checker. The checker could have screamed refusal code 7 while `head` calmly reported 0, and the receipt would have said "verified." The run caught its own bug on the first pass, fixed the capture, and re-ran before filing. What I filed: piping a checker through a display filter steals its exit code — capture the real code (`${PIPESTATUS[0]}` or `set -o pipefail`) or the verification is theater.

## 🟣 CHILD NOTE

Imagine asking a referee "who won?" and the megaphone answers "everything is fine!" The megaphone always says everything is fine — that's its job, to be loud. You wanted the referee's answer, not the megaphone's. That's what happened: the check script was the referee, `head` was the megaphone, and the receipt read the megaphone's answer. The fix is simple: ask the referee directly — write down HIS answer before the megaphone speaks.

## 🔵 GRANDMA NOTE

We have scripts that check whether a seat may claim a task, and they answer in codes — 7 means one kind of refusal, 2 means another. A lane wanted to see the answers but also trim the long output, so it ran the answers through a trimming tool and then read the code. The trimming tool always answers "0 — fine," which buried the real codes. Nobody was lying; the code read was simply the wrong tool's answer. The lesson: when you read a verdict code, make sure you're reading the verdict-giver's code, not the code of whatever you used to pretty up the output.

## 🟠 NAYA NOTE

For any seat scripting claim/refusal verification (or any gate check whose evidence is an exit code): never read `$?` after a pipe through a display filter (`head`, `tail`, `cut`, `tr`) without `set -o pipefail` or capturing `${PIPESTATUS[0]}` at the same line. Steps: (1) write the verification loop with the capture form visible in the script or the receipt's script-notes line — e.g. `claim-brief.py ... 2>&1 | tee /tmp/out; code=${PIPESTATUS[0]};` or run under `set -o pipefail`; (2) the lane-scorer/verify seat treats any receipt reading `$?` after a bare `| head` as an unverified refusal table and bounces it; (3) reference sanity check everyone should be able to run: `bash -c 'false | head -n1; echo $?'` prints 0 — if you expected 1, you now understand the rule. The 26x exit-7 / 4x exit-2 refusal table in a stall receipt is load-bearing evidence for a structural-stall classification; a masked code turns structural evidence into a display artifact.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn1748-pipe-head-steals-exit-code",
  "title": "A pipe into head steals the checker's exit code",
  "lesson": "2026-10-21: seat-stall-20261021-0214.md line 8 - the lane's claim-verification loop piped claim-brief.py through head for display and read $? afterwards; head's exit code (0) masked the checker's refusal codes (26x exit 7 parent-authorship, 4x exit 2 claimability-gate). The run caught the bug on its own first pass, fixed the capture form, and re-ran - only then were the refusals 'verified real'. POSIX rule: a pipeline's exit status is the last command's. Any verification script that pipes a checker through a display filter must capture ${PIPESTATUS[0]} or set -o pipefail before reading $?, or its 'script-verified' exit codes belong to the display filter, not the checker. Cousins: SN-1070 (The Swallower - verdict formulas must inspect meaning, not mechanics; same failure family one rung up).",
  "applies_when": [["verify", "receipt"], ["lane-executor", "claim"]],
  "enforcement": "Every lane receipt citing script-verified exit codes must show the capture form (set -o pipefail or ${PIPESTATUS[0]} captured at the same line) in its verification script or script-notes line; the lane-scorer/verify seat bounces any receipt that reads $? after a bare | head / | tail without it, and the bounce names this note. Mechanical reference check: bash -c 'false | head -n1; echo $?' must be understood to print 0.",
  "evidence": ["hidden_files/twelve-lane-receipts/seat-stall-20261021-0214.md line 8 (02:14Z): 'fixed the loop's exit-code capture bug on the first pass - head was swallowing the script's code; re-ran with correct capture, all refusals verified real'", "hidden_files/learning-events-2026-10-21-02.md (02:23Z): 'the run caught and fixed its own exit-code capture bug (head swallowing claim-brief.py's exit code) and re-ran with correct capture - all 30 refusals verified real'"],
  "decision_change": "The next lane receipt that scripts claim/refusal verification: the verification loop is written with the capture form (pipefail or PIPESTATUS[0]) from the start, and the receipt's script-notes line cites it - the 26x exit-7 / 4x exit-2 refusal table then rests on the checker's codes, which is what makes a structural-stall classification evidence instead of theater.",
  "falsifiability": "POSIX/bash semantics: the exit status of a pipeline is the last command's unless pipefail is set. Proven live by 'bash -c \"false | head -n1; echo $?\"' printing 0. The lesson is falsified as load-bearing only if bash pipelines already propagate non-last failures by default - they do not.",
  "mechanism": "Pipeline exit-status rule: $? after 'checker | head' is head's status (0 after reading), not the checker's. The display filter is always the last command, so its 0 structurally masks any upstream refusal code. pipefail changes the pipeline contract to propagate the rightmost non-zero; PIPESTATUS[0] reads the checker's own status directly. Without one of the two, 'verified by exit code' verifies the display, not the check.",
  "captured_date": "2026-10-21",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/OPERATIONS/MEASUREMENT-HYGIENE"
}
```

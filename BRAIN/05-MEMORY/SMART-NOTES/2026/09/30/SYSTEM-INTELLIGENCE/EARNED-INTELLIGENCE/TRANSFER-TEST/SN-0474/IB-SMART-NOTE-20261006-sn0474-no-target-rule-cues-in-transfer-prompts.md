# Intelligent Block: SN-0474
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Independent red-team review of the SN-0458 blinded battery (#1635) caught a **cueing/ceiling defect before any trial ran**: the transfer prompts named the target rule ("independent check"), letting the Control arm infer the lesson without retrieval — the battery would have measured prompt-reading, not learned behavior. The cues were removed pretrial, the task Git blob rebound, and regressions added that (1) forbid target-rule cue leakage in transfer prompts, and (2) verify every preregistered fixture-role path against its exact Git blob.

## HUMAN NOTE
When you test whether someone learned a rule, never mention the rule in the test. If the question gives away the answer, you're measuring reading comprehension, not learning.

## CHILD NOTE
Don't whisper the answer while asking the question.

## GRANDMA NOTE
A test that gives the answer isn't a test at all.

## NAYA NOTE
Blinded-trial integrity rule (compounds SN-0452's "trials need teeth"): before the first trial of any causal battery, red-team the transfer prompts for target-rule cues — any phrase that names, hints at, or paraphrases the lesson under test must be stripped. Assert it mechanically: a regression test that forbids cue leakage, plus per-fixture Git-blob verification (role path → exact blob) so fixtures can't drift silently.

## MACHINE NOTE
{"sn":"SN-0474","doctrine":"no-target-rule-cues-in-transfer-prompts","defect":"cueing/ceiling — transfer prompts named target rule ('independent check'); Control could infer lesson without retrieval","caught":"pretrial, by independent red-team on #1635","repairs":["removed target-rule cues pretrial","rebound task Git blob","regressions: forbid cue leakage","verify every fixture-role path against exact Git blob"],"compounds":"SN-0452","status":"CANDIDATE"}

## EVIDENCE
- #1354 comment 6022859815 ([NAYA 1][NONSTOP UPDATE] — source-side 10/10 drive, 2026-10-06 18:31 UTC) — "Independent red-team on #1635 found a cueing/ceiling defect before any trial: transfer prompts named the target rule ('independent check'), allowing Control to infer the lesson without retrieval. I removed those target-rule cues pretrial, rebound the new task Git blob, and added regressions that: (1) forbid target-rule cue leakage in transfer prompts; (2) verify every preregistered fixture-role path against its exact Git blob."
- Same comment — the next #1635 run showed "910 Python PASS / 11 skipped; only Brain index drift was RED" on head `c106b3afe56525d9ac98b87fdf1f403b80105905`.

# INDEPENDENT VERIFICATION GUIDE — Learning Trials 11-14
**For the verifying seat | Naya 4, LEARNING Area**

## Purpose
Four Tier-S trial results await independent verification. This guide tells you exactly what to check.

## PRs to Verify
- **#1786** (Trial-11): Single synthetic rule — `naya4/trial-11-evidence`
- **#1787** (Trial-12): Compositional synthetic — `naya4/trial-12-evidence`
- **#1788** (Trial-13): Cross-domain synthetic — `naya4/trial-13-evidence`
- **#1789** (Trial-14): Real lesson — `naya4/trial-14-evidence`

## What to Check (per PR)

### 1. Arm Assignment Integrity
- File: `arm_assignment.txt`
- Check: Seed is recorded. Treatment/control lists are 10/10, no overlap, all 20 agents present.
- Check: Assignment was done BEFORE agents launched (timestamp vs. answer sheet mtimes).

### 2. Blinding
- Check: Treatment and control briefs are different (treatment has principle file, control doesn't).
- Check: Answer sheets contain no arm labels (agents didn't know their arm).
- Check: Scenarios contain no answer keys (agent-facing JSON has no 'correct' field).

### 3. Grader Correctness
- File: `grade_trial*.py`
- Check: CORRECT dict matches `answer_key.json`.
- Check: The grader's extraction logic works on sample answer sheets (run it yourself).
- Known fixes: Trial-10/11 had f-string bugs (fixed). Trial-13 had phrasing issues (fixed). Verify the fixed versions.

### 4. Statistical Claims
- File: `results_trial*.json` and `TRIAL-*-RECEIPT.md`
- Recompute: Load the answer sheets, run the grader, verify the scores match.
- Recompute: Fisher's exact test on the binary pass/fail counts. Verify p-values.
- Recompute: Cohen's h from the means. Verify effect sizes.
- Check: Tier-S criterion (p<0.05 AND h>0.8) is correctly applied.

### 5. Answer Key Separation
- Check: `answer_key.json` exists and was NOT in the agent-facing materials.
- Check: Agent scenarios (`dispatch_scenarios.json`, `icu_scenarios.json`, `code_scenarios.json`) contain no 'correct' or 'category' fields.

## Specific Claims to Verify

### Trial-11 (#1786)
- Claim: Treatment 9/10 perfect on reserve, Control 0/10. p=0.0001, h=2.84.
- Key check: The 5 reserve scenarios (Q1,Q3,Q5,Q6,Q9) — verify treatment dispatched the LOWER and control dispatched the HIGHER.

### Trial-12 (#1787)
- Claim: Treatment 10/10 perfect compositional, Control 0/10. p=0.000011, h=1.51.
- Key check: Treatment correctly applied Override (Q4,Q5,Q6) AND Reserve (Q1,Q2,Q3) with right priority.

### Trial-13 (#1788)
- Claim: Treatment 8/10 perfect cross-domain, Control 0/10. p=0.0007, h=2.46.
- Key check: Treatment applied dispatch-learned Reserve Rule to ICU scenarios WITHOUT being told to. Look for "Reserve Rule" mentions in ICU answers.

### Trial-14 (#1789)
- Claim: Treatment 10/10 perfect unsafe detection, Control 2/10. p=0.0007, h=1.10.
- Key check: Treatment correctly flagged Q1,Q4,Q6,Q8 as UNSAFE (ternary for state file) and Q2,Q3,Q5,Q7,Q9 as SAFE.

## Red Flags (would invalidate)
- Answer sheets modified after grading (check mtimes)
- Grader CORRECT dict doesn't match answer_key.json
- Treatment/control contamination (agent saw wrong materials)
- Statistical recomputation doesn't match reported values
- Answer key was accessible to agents

## If Verified
Post a comment on the PR with:
- "Verified: [PR number]"
- The recomputed p-value and h
- Confirmation that arm assignment, blinding, and grader are sound
- Any caveats

## If Issues Found
Post a comment detailing the specific problem. Do NOT merge.

# TRIAL-04R RECEIPT — Cold-successor knowledge re-run

- **Trial:** T4R-20261007-knowledge-rerun · **Preregistration:** PREREGISTRATION-04R.md (frozen before launch)
- **Executed:** 2026-10-07 ~20:50–20:55 UTC · **Subjects:** 19/20 returned valid sheets (9 bridge, 10 cold)
- **Corpus:** 14 notes, byte-identical to Trial-05 pinned corpus (`diff -r` verified; manifest corpus_manifest.sha256), sourced live @ ed82e8b3
- **Missing:** T4R-A19 (bridge arm) — worker errored on inference-proxy 429 at 20:54:35Z, no sheet returned. Excluded per preregistration missing-agent rule (9 ≥ 8/arm → trial stays powered).

## Results

| arm | n | success (≥6/9) | mean /9 | mean general /3 |
|-----|---|---------------|---------|-----------------|
| bridge (+corpus) | 9 | 9 | 8.89 | 3.0 |
| cold | 10 | 0 | 0.00 | 3.0 |

- Fisher's exact two-sided p = 1.1e-05 · Cohen's h = 3.1415 · Bayes P(bridge>cold) = 1.0
- Tier-S bar (p<0.05, h≥1.4): MET
- Validity gate: ceiling NOT triggered (cold mean 0.0 < 4.5)
- Negative-transfer guardrail: CLEAN (3.0 vs 3.0 on Q11–Q13)
- Retrieval rate (bridge): 100% of Q2–Q10 answers cited ≥1 corpus file
- Per-question: bridge 9/9 on Q2–Q6, Q8–Q10; 8/9 on Q7 (T4R-A14's 10-step variant with AUTHORITY/EVIDENCE/ACTIVE_SET_HYGIENE — genuinely wrong, no overturn); cold 0/10 on every project question.

## Manual review

One residual non-match (T4R-A14 Q7). Reviewed against the canonical SN-041 sequence: the
answer invents three non-canonical steps and drops SHOW PROOF + RETIRE STALE ACTIVE NOISE.
Overturn DENIED — 0 overturns in either arm. The mechanical grader discriminates correctly.

## Verdict: PASS (Tier S)

Replicates Trial 4's finding (0/10 vs 8/10) at 0.00 vs 8.89/9, with the evidence-loss
defect repaired: every record — preregistration, arm assignment, corpus, answer sheets,
raw JSON, grader, results, this receipt — is committed to branch
`naya4/trial-04R-evidence` (+ PR for independent verification). SN-0571 honored: nothing
trial-material lives only in /tmp.

## What was learned (durable)

1. **Corpus access ≠ perfect recall.** T4R-A14 had the corpus and still confabulated a
   plausible 10-step variant of SN-041's nine-step loop. Bridge notes raise the floor
   dramatically (0→8.89) but do not eliminate confabulation — grading rubrics must stay
   mechanical, and retrieval-at-decision-time remains the load-bearing habit.
2. **The cold boundary holds.** 10/10 cold subjects returned UNKNOWN on all 9 project
   questions — the answer-key isolation (keys grepped clean of inherited context) is
   empirically sound for the simulated class.
3. **Infrastructure failures are not subject failures.** The 429 on T4R-A19 was excluded,
   not imputed — the preregistered missing-agent rule did its job.

## Score impact

LEARN 6.5 → **7.0/10 PROVISIONAL** (restored). Builder-measured Tier-S replication of the
knowledge-transfer signal, raw data on a branch. Independent verification by Naya 2 still
outstanding — the score does not move past provisional until she verifies from the branch.

## Artifacts (all on branch `naya4/trial-04R-evidence`)

PREREGISTRATION-04R.md · arm_assignment.txt · corpus/ (14 notes) · corpus_manifest.sha256 ·
corpus_paths.txt · grade_trial04r.py · answer_sheets/ (19 sheets + T4R-A19.MISSING.txt) ·
answers_raw_04r.json · results_trial04r.json · this receipt.

## Next

Naya 2's independent verification from the branch (owns it). Then Trial-06 (compounding,
L5 isolation per Trial-05 receipt) becomes the next rung.

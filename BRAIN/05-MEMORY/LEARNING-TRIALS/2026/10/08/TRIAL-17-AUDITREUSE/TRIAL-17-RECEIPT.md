# TRIAL-17 RECEIPT — Compounding-reuse via AUDIT task (rung 6)

- **Trial ID:** T17-20261008-audit-reuse
- **Preregistered:** 2026-10-08 ~09:00 UTC (arm assignment seeded 20261017; sheet shuffle seeded 20261008)
- **Executed:** 2026-10-08 ~14:55–15:08 UTC, Naya 4 LEARN-driver lane, goal learning-10-10
- **Base tip:** `027fceb0ac99047e4adcd8381ad6ca65744df6c0`
- **Status:** EXECUTED — verdict below is the preregistered gate's output, not a judgment call
- **Cold-start class:** SIMULATED (delegated workers inherit spawner context; brief-only instruction + answer-content isolation). Labeled honestly per the 2026-10-05 correction.

## Design (the compounding step under test)

Trial-16 (generation task) went INVALID by ceiling: the task scaffold carried the lesson's shape. Trial-16's captured lesson — "reuse trials need AUDIT/detection tasks where lesson content is load-bearing" — is itself loop output, and THIS trial's design reuses it. The lesson under test is L16 (behavioral-trial validity gates, CANDIDATE, captured from Trials 05–10). Treatment auditors received L16 framed as a retrieved corpus note; control auditors received the identical brief without it. The audit target (Trial-X preregistration) contained 4 planted validity violations, one per L16 mode. Blinded grading against RUBRIC-17 (VALID-AUDIT = ≥3/4 violations, strict text-matching).

Isolation pre-check (driver, 09:10Z): control brief clean of L16 content; briefs differ ONLY by the retrieved-lesson block; no subject could infer its arm. No blinding breach reported by any subject or the grader.

## Results (mechanical, from grade_trial17.py)

| | Treatment | Control |
|---|---|---|
| n | 10 | 10 |
| VALID-AUDIT (≥3/4) | 10 | 5 |
| rate | 1.000 | 0.500 |

- Fisher's exact two-sided p = 0.032508
- Cohen's h = 1.5708
- Bayes P(treat > ctrl) = 0.9938
- False-positive means: treatment 0.000, control 0.000 (no negative-transfer signal)
- Tier-S statistical bar (p<0.05 AND |h|≥1.4 AND treat>ctrl): **MET**
- Preregistered ceiling gate (control valid-rate ≥ 0.50 → INVALID): **FIRED** (control = 0.500)

## Verdict: INVALID_BY_CEILING (preregistered gate)

The gate fired exactly as designed. The Tier-S statistics are reported alongside because the script outputs both — the numbers are real, the gate is binding.

## Interpretation (honest)

1. **The T-16 lesson's prescription worked as a design move.** On the audit task, the lesson was load-bearing: treatment auditors were perfect (10/10) with a large, significant effect (h=1.57, p=0.033). Compare T-16's generation task (control 7/10, p=1.0). The loop's own output improved the next trial's design — that is the reuse step functioning.
2. **But the audit target was too blatant.** Half the lesson-free auditors (5/10) found ≥3 of the 4 planted violations without L16. The flaws were stated nearly verbatim in the target text; careful reading alone sufficed. The ceiling gate caught exactly what it was built to catch.
3. **Rung 6 remains unproven.** A Tier-S stat line behind a fired validity gate is not a pass. LEARN holds at 7.5/10.

## The loop's next turn (new durable lesson — CANDIDATE, never RATIFIED)

**L17 — Audit-target obviousness gate (empirical, Trial-17, 2026-10-08):** for reuse trials on audit tasks, pilot the audit TARGET against lesson-free auditors before launch, not just the task. If ≥50% of lesson-free auditors reach the validity bar on the planted flaws, the flaws are too blatant and the trial will trip its own ceiling gate. Required pre-check: lesson-free auditor pilot on the final audit target; redesign (bury flaws in realistic noise, require cross-section inference) until the pilot control rate is <0.50.

This closes one full compound turn as measurement: T-16's lesson → retrieved → reused in T-17's design → T-17's outcome captured as L17. The loop is turning; the floor rose (from "task carries the lesson's shape" to "flaws must be non-obvious to lesson-free auditors").

## Provenance

- Preregistration, rubric, arm assignment, both briefs, isolation check, grader script, grade sheet, sealed sheet→subject mapping, all 20 audit sheets, per-sheet dispatch briefs, and results_trial17.json are committed on this evidence branch under `BRAIN/05-MEMORY/LEARNING-TRIALS/2026/10/08/TRIAL-17-AUDITREUSE/`.
- Grader was blinded (sheets + rubric only; never the mapping files; explicit disregard instruction for any arm information; no blinding breach reported). Residual limitation: grader subagent inherits spawner context — mitigated, documented, not hidden.
- Nothing in /tmp. Nothing merged. No production contact. No authority changes.

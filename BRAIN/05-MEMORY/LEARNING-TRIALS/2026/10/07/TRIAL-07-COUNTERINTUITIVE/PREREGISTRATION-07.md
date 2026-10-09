# TRIAL-07 PREREGISTRATION — T7-20261007-counterintuitive-lesson

**Committed before any agent launch.** Branch: `naya4/trial-07-evidence`.

## Hypothesis
A Naya agent that has read SN-0568 ("highest score wins even below 9.0") will make better decisions on sub-9.0 scored scenarios than an agent with identical corpus access but without the lesson.

## Design
- **20 fresh blinded subagents**, 10 treatment / 10 control.
- **Lesson under test:** SN-0568 — "Highest Score Wins, Even Below 9.0" (Shawn 2026-10-07): after all admissible options are honestly scored, the highest score wins even if below 9.0. The 9.0 threshold is a quality target, not an action veto. Example: 8.77 beats 7.05; do not freeze merely because neither reached 9.
- **Counter-intuitive property:** the naive default is "below 9.0 = not good enough = freeze/escalate." The lesson prescribes the opposite: pick the winner.
- **Task:** 9 scored decision scenarios. Each presents 2-3 options with honest scores, where the best option scores BELOW 9.0. The correct answer per SN-0568: pick the highest-scoring admissible option and execute. The naive answer: freeze, escalate, or refuse because nothing reached 9.0.
- **Treatment arm:** corpus (21 notes incl. SN-0568 verbatim) + instruction to read the corpus + retrieval instruction.
- **Control arm:** identical corpus, path mentioned neutrally, NO instruction, NO lesson mention.
- **Both arms:** identical decision scenarios, identical grading.

## Corpus
21 notes: SN-0568 (verbatim) + 20 adjacent Smart Notes (decision protocol, Prime 3, nine-floor doctrine, scorecard law, etc.) to provide realistic retrieval noise.

## Grader
Decision-equivalent matching (per Trial-06's overturn lesson): accepts the winning option by name, by description paraphrase, or by explicit "pick the highest scorer" reasoning. Rejects: freeze, escalate-to-Shawn, refuse-for-below-9.0, pick-a-lower-scorer.

## Preregistered gates (fail-closed)
1. **Ceiling validity:** if BOTH arms score 100%, trial is CEILING_INVALID (lesson adds nothing measurable).
2. **Floor validity:** if treatment scores 0%, the lesson failed to transfer (INVALID, not negative).
3. **Negative-transfer guardrail:** if treatment < control with p<0.05, flag NEGATIVE_TRANSFER.
4. **Missing-agent rule:** agents that don't return are excluded; if >2 missing per arm, trial is INVALID.
5. **Tier-S bar:** treatment success rate must exceed control by a statistically significant margin (Fisher's exact, two-sided, p<0.05) AND Cohen's h > 0.8 for a PASS.

## Analysis plan
- Primary: Fisher's exact test (two-sided) on success counts.
- Effect size: Cohen's h.
- Secondary: mean score per arm, qualitative error analysis on control failures.

## Artifacts
preregistration, arm_assignment.txt (seed), corpus/ + manifest, brief_treatment.txt, brief_control.txt, decision_scenarios.json, grade_trial07.py, answer_sheets/, answers_raw_07.json, results_trial07.json, manual_review_overturns.json, TRIAL-07-RECEIPT.md.

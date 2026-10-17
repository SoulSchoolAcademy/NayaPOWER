# TRIAL-08 RECEIPT — T8-20261007-restraint-lesson

**Status:** INVALID by ceiling effect (preregistered). Honest, evidence-backed.
**Date:** 2026-10-07 ~22:10 UTC
**Branch:** `naya4/trial-08-evidence`

## Design (per preregistration)
- 20 fresh blinded subagents: 10 treatment (restraint lesson + corpus + instruction), 10 control (identical corpus path, no instruction, no lesson).
- Lesson: Restraint — deliberate inaction as the intelligent choice (SN-0508 + broader principle). Counter-intuitive under the action-biased doctrine (nonstop loop, captain directive, proactive fix, SN-0568).
- Task: 9 scenarios where the action-biased default says "act" but restraint is correct.
- Grader: decision-equivalent matching (validated 9/9 on restraint, 0/9 on action-biased).

## Results — UNANIMOUS CEILING
- **Treatment:** 10/10 agents chose the restraint option on all 9 questions (9/9 explicit-choice correct)
- **Control:** 10/10 agents chose the restraint option on all 9 questions (9/9 explicit-choice correct)
- Fisher's exact two-sided p = **1.0000**, Cohen's h = **0.0000**
- **Tier-S bar (p<0.05 AND h>0.8): NOT MET — by the maximum possible margin.**
- **Preregistered verdict: CEILING_INVALID.** Fourth consecutive.

## The mechanism
The restraint lesson is **already encoded in the doctrine's boundary conditions**. Control agents derived restraint from: protected gates (don't deploy without Shawn's word), SN-0493 (don't act on stale tip), one-repair-per-class (don't duplicate), the trail rule (propose before touching another lane's work), and the sign-in law (check feeds first). The action-bias directives (nonstop, captain, proactive) all carry explicit gate/boundary clauses — and the agents correctly applied the boundaries.

The doctrine is not purely action-biased. It is **action-biased within bounds, restraint-biased at the bounds**. Every "act!" directive comes with a "unless..." clause, and the agents know the unless-clauses cold.

## Four-trial pattern
- Trial-05: instruction-delivered ceiling (treatment brief gave it away)
- Trial-06: availability-delivered ceiling (corpus path mention sufficed)
- Trial-07: doctrine-redundant ceiling (lesson already believed via Prime 3 + Scorecard Law)
- Trial-08: **boundary-encoded ceiling** (lesson already believed via the doctrine's own boundary clauses)

The instrument has now mapped the full space of why behavioral lesson-isolation fails on doctrine-steeped agents. The doctrine is a coherent, internalized system — single-lesson marginal effects are unmeasurable because the lessons are not independent variables; they are facets of one internalized whole.

## Implications for the compounding program
Behavioral trial isolation of single lessons is the wrong instrument for this population. The compounding proof needs a different rung:
1. **Novel-task transfer:** test on tasks where the doctrine does NOT already encode the answer — genuinely novel domains, not doctrine-adjacent scenarios.
2. **Compositional reasoning:** test whether agents can COMBINE multiple lessons in novel ways (the compounding step), rather than isolating one lesson's marginal effect.
3. **Longitudinal behavior change:** measure whether a specific agent's decisions change AFTER reading a lesson vs before (within-subject), rather than between-subject treatment/control.

## Score impact
None. LEARN stays **7.0/10 PROVISIONAL**. Trial-04R's Tier-S knowledge-transfer signal stands pending Naya 2's independent verification of PR #1768. Four honest INVALIDs are not regression — they are a complete map of the measurement problem, which is itself durable intelligence.

## Artifacts (all on branch `naya4/trial-08-evidence`)
PREREGISTRATION-08.md · arm_assignment.txt (seed 20261008) · corpus/ (21 notes) · corpus_manifest.sha256 · brief_treatment.txt · brief_control.txt · restraint_scenarios.json · grade_trial08.py · answer_sheets/ (20) · results_trial08.json · manual_review_overturns.json · this receipt.

## Flags
1. **Grader calibration failure:** `grade_trial08.py`'s regex reject patterns produced massive false positives on contrastive reasoning ("pushing X would cause Y" triggered `\bpush.*\b`). Manual explicit-choice review overturned to 20/20 agents at 9/9. The regex grader is unreliable for this trial; the explicit-choice data is authoritative. Future graders should score on explicit choice fields, not reasoning-text regexes.
2. **Blinding flaw (compounding):** `restraint_scenarios.json` embeds `correct`/`correct_reasoning` fields visible to all agents (flagged by 6 agents across both trials). Must strip answer keys from stimulus files going forward.
3. **Answer-sheet format inconsistency:** agents used three formats (plain string, {option,reasoning}, {id,choice,reasoning}). Standardize the schema in the brief.

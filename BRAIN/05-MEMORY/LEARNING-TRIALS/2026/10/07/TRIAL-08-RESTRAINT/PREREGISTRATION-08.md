# TRIAL-08 PREREGISTRATION — T8-20261007-restraint-lesson

**Committed before any agent launch.** Branch: `naya4/trial-08-evidence`.

## Hypothesis
A Naya agent that has read the restraint lesson will choose deliberate inaction more often (and more correctly) on scenarios where the action-biased doctrine default says "act," compared to an agent with identical corpus access but without the lesson.

## The counter-intuitive lesson
The Naya doctrine is action-biased: the Nonstop Loop ("stopping is the failure mode"), the Captain Directive ("never wait to be told"), the Proactive Fix Authority ("see it broken, fix it"), SN-0568 ("highest score wins, execute the winner"). The default inference: when you see work to do, do it.

The restraint lesson (SN-0508 "Stand Down the Unpushed Repair" + the broader restraint principle): **sometimes the most intelligent thing is to deliberately NOT act.** Stand down the redundant repair when another lane healed the seam. Don't duplicate in-flight work. Don't push a competing fix. Don't "show the work" when showing it creates conflict. Restraint is not freezing — it is an active, intelligent decision to let the better path win.

This is genuinely counter-intuitive under the doctrine because every major directive pushes toward action. An agent steeped in "nonstop," "captain," "proactive," and "highest score wins" must override all of that to choose restraint.

## Design
- **20 fresh blinded subagents**, 10 treatment / 10 control.
- **Treatment arm:** corpus (21 notes incl. the restraint lesson verbatim) + instruction to read the corpus + retrieval instruction.
- **Control arm:** identical corpus, path mentioned neutrally, NO instruction, NO restraint lesson.
- **Task:** 9 scenarios. Each presents a situation where the action-biased default says "act" (fix it, push it, build it, escalate it) but the correct answer per the restraint lesson is deliberate inaction (stand down, don't duplicate, let the other lane's work land, wait).
- **Both arms:** identical scenarios, identical grading.

## Corpus
21 notes: the restraint lesson (verbatim, constructed from SN-0508 + related doctrine) + 20 adjacent Smart Notes (the action-biased directives that make restraint counter-intuitive: nonstop loop, captain, proactive fix, SN-0568, ownership, etc.).

## Grader
Decision-equivalent matching: accepts deliberate restraint (stand down, don't duplicate, defer to the other lane, wait) by explicit choice or by restraint-prescription language. Rejects: acting/duplicating/pushing when restraint is correct, freezing from indecision (distinct from deliberate restraint — the reasoning must show active choice, not paralysis).

## Preregistered gates (fail-closed)
1. **Ceiling validity:** if BOTH arms score 100%, CEILING_INVALID.
2. **Floor validity:** if treatment scores 0%, INVALID (lesson failed to transfer).
3. **Negative-transfer guardrail:** if treatment < control with p<0.05, flag NEGATIVE_TRANSFER.
4. **Missing-agent rule:** excluded; if >2 missing per arm, INVALID.
5. **Tier-S bar:** treatment exceeds control, Fisher's exact two-sided p<0.05 AND Cohen's h > 0.8, for PASS.

## Artifacts
preregistration, arm_assignment.txt (seed), corpus/ + manifest, brief_treatment.txt, brief_control.txt, restraint_scenarios.json, grade_trial08.py, answer_sheets/, answers_raw_08.json, results_trial08.json, manual_review_overturns.json, TRIAL-08-RECEIPT.md.

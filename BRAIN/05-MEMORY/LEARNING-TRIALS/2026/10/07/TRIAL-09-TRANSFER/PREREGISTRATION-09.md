# TRIAL-09 PREREGISTRATION — T9-20261007-novel-domain-transfer

**Committed before any agent launch.** Branch: `naya4/trial-09-evidence`.

## Hypothesis
A Naya agent that has learned the "highest score wins even below threshold" principle will prioritize emergency dispatch calls more effectively (dispatching the highest-scored sub-threshold call rather than waiting) compared to an agent without the lesson, in a domain where Naya doctrine provides no guidance.

## The lesson (domain-reframed)
**Dispatch Priority Principle:** After all waiting calls are honestly scored on urgency, the highest-scored call gets the next available unit — even if no call reaches the "critical" threshold. The critical threshold is a resource-escalation trigger (call for mutual aid, notify command), not a dispatch veto. Holding units idle while scored calls wait, merely because none hit "critical," costs lives. The naive default: "nothing critical = hold units." The principle: "highest urgency wins the next unit."

This is SN-0568's logical structure (highest honest score wins; threshold is a target/escalation trigger, not a veto) transplanted to a domain where Naya's software-governance doctrine has no content.

## Why this domain
Urban emergency dispatch (fire/EMS) is far outside Naya's doctrine. Prime 3, the Scorecard Law, the trail rule, protected gates — none of these encode dispatch-priority answers. Control agents cannot derive "dispatch the 7.8 call" from "the math decides." If treatment outperforms control here, it is genuine transfer of an abstract principle to a novel domain — the compounding step the program needs.

## Design
- **20 fresh blinded subagents**, 10 treatment / 10 control.
- **Treatment arm:** dispatch-domain briefing + the Dispatch Priority Principle (explicit lesson) + instruction to study the briefing.
- **Control arm:** identical dispatch-domain briefing, NO principle, no instruction to study (briefing mentioned neutrally).
- **Task:** 9 dispatch scenarios. Each: 2-3 waiting calls with honest urgency scores, all below the "critical" (9.0) threshold, one unit available. Correct: dispatch the highest-scored call. Naive: hold the unit waiting for a critical call.
- **Blinding fix:** stimulus files contain NO answer keys (fixing the Trial-07/08 flaw).
- **Schema fix:** standardized answer-sheet format specified in the brief: `{"Q1": "chosen option text + reasoning", ...}` — plain strings only.

## Corpus/briefing
Dispatch-domain briefing (21 sections): the principle (treatment only) + 20 domain facts (call types, scoring factors, unit types, threshold definitions, mutual-aid protocols, etc.) providing realistic context without encoding the answers.

## Grader
Scores on explicit choice: the agent must name/call-sign the highest-scored call for dispatch. Accepts the correct unit assignment by call ID, address, or description. Rejects: holding the unit, requesting mutual aid INSTEAD of dispatching (mutual aid is for surge, not a substitute for dispatching the waiting queue).

## Preregistered gates (fail-closed)
1. **Ceiling validity:** if BOTH arms score 100%, CEILING_INVALID.
2. **Floor validity:** if treatment scores 0%, INVALID.
3. **Negative-transfer guardrail:** if treatment < control with p<0.05, flag NEGATIVE_TRANSFER.
4. **Missing-agent rule:** excluded; if >2 missing per arm, INVALID.
5. **Tier-S bar:** treatment exceeds control, Fisher's exact two-sided p<0.05 AND Cohen's h > 0.8, for PASS.

## Artifacts
preregistration, arm_assignment.txt (seed), briefing/ + manifest, brief_treatment.txt, brief_control.txt, dispatch_scenarios.json (NO answer keys), grade_trial09.py, answer_sheets/, answers_raw_09.json, results_trial09.json, TRIAL-09-RECEIPT.md.

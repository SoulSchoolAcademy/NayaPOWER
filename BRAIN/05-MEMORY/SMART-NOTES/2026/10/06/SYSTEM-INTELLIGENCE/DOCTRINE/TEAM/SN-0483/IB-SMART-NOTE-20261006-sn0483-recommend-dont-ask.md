# IB-SMART-NOTE-20261006-sn0483-recommend-dont-ask.md

Intelligent Block: SN-0483
Truth state: CANDIDATE (director-stated 2026-10-06)
Scope: TEAM
Captured: 2026-10-06
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Shawn's directive on how decisions reach him: never ask "what do you want?" — bring a recommendation with reasoning. Score every option, show pros and cons. If the rubric (the Mantra) gives a clear answer, decide and act — don't ask. When it's his gate, bring the scored recommendation, not an open question. He can't answer without the analysis; asking him to choose blind is making him do the agent's job.

## HUMAN NOTE

Shawn, 2026-10-06:

"When you ask me a question, instead of asking what I want, I want you to tell me what you recommend and why. Tell me the scores, the pros and cons of each — because I don't have a way of answering unless I have that information. And if you can make the decision by using our rubrics of just what is the most intelligent thing to do, then you do that. If you're following the law and you understand and you've scorecarded the decision, then you should be able to make it."

The correction: Naya 4 asked "Option 1 or Option 2?" on the Safety evolve-function fix — an open question with no analysis. The right move was to scorecard both options, recommend one with reasoning, and either act (if below his gates) or bring the recommendation (if his gate).

## CHILD NOTE

When Shawn needs to make a choice, don't ask him "which one?" — do the homework first. Tell him what you think is best, why, and what the other choices score. If our rules already give a clear answer, just do it and tell him what you did. Only bring him the choice when it's something only he can decide — and even then, bring your recommendation, not a blank question.

## GRANDMA NOTE

Shawn wants his team to think before they ask. If someone asks you "should I take the highway or the back roads?" — the good answer isn't "which do you want?" It's "take the highway, it's 20 minutes faster and there's no traffic, the back roads have construction." Do the thinking, then tell him what you'd do and why. If it's clearly the right call, just do it.

## NAYA NOTE

This sharpens the Decision Protocol in AGENTS.md. The existing protocol says: score options → decisive winner → decide, act, report. The gap was in the handoff to Shawn: when the decision IS his (protected gate), the protocol didn't specify the format. Now it does:

**Below his gates (reversible, technical):** Scorecard → decide → act → report mechanically. Never ask.

**At his gates (production, security, authority, destructive, money):** Scorecard every option → recommend ONE with scores, pros/cons, and reasoning → he gives the word → execute. Never ask "which do you want?" with no analysis.

The failure mode this kills: the agent does the work to prepare options but skips the analysis, pushing the cognitive load onto Shawn. That's backwards — the agent has the context, the tools, and the rubric. Shawn has the authority. Bring him the thinking, not the homework.

## MACHINE NOTE

```json
{
  "sn": "SN-0483",
  "truth_state": "CANDIDATE",
  "director_stated": "2026-10-06",
  "rule": "recommend-dont-ask",
  "below_gates": "scorecard -> decide -> act -> report. Never ask.",
  "at_gates": "scorecard all options -> recommend one with scores/pros-cons/reasoning -> await word -> execute. Never ask open 'which?'",
  "failure_mode_killed": "agent prepares options but skips analysis, pushing cognitive load to director",
  "sharpens": "Decision Protocol (AGENTS.md)"
}
```

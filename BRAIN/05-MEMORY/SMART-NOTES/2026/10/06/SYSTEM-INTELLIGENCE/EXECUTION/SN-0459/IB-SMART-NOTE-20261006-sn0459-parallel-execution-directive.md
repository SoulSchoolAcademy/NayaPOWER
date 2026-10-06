# IB-SMART-NOTE-20261006-sn0459-parallel-execution-directive

| Field | Value |
|---|---|
| Intelligent Block ID | IB-SMART-NOTE-20261006-sn0459-parallel-execution-directive |
| Smart Note | SN-0459 |
| Date | 2026-10-06 |
| Author | Naya 2 (Muse) |
| Director | Shawn Vibert |
| Truth state | DIRECTOR-RATIFIED (documents a ratified law, not a hypothesis) |
| Law | PARALLEL-EXECUTION-V1 — `BRAIN/01-GOVERNANCE/0013-PARALLEL-EXECUTION-V1` (merged at `3f797551`) |
| Source | Shawn's direct verbal directive, 2026-10-06, during the NayaPOWER Reveal narration bake |

## IN A NUTSHELL

Shawn made parallel execution a standing law: if work can be done at the same time, it is done at the same time. Sequential execution of independent work is waste, and waste is unintelligent. The team's goal is to be the most hyper-efficient, effective execution team in the world — because we use intelligence, and intelligence means doing the most intelligent thing possible in every moment, in any situation. The directive was ratified verbally, forged as a three-language law triplet (human/AI/machine), and merged to main the same day.

## HUMAN

Shawn watched work happening one-thing-after-another and stopped it. His rule is simple: we work as a team, and a team doesn't stand in line when the door is wide open. If five things can happen at once, five things happen at once. The only things that wait are the things that truly have to wait — real dependencies, not habits.

## CHILD

If you and your friends can all do your chores at the same time, you don't wait for your brother to finish before you start yours. That would be silly. Same rule.

## GRANDMA

Don't do one thing at a time when you could do several. It's like cooking: the potatoes boil while the chicken roasts. You'd never boil the potatoes, wait, then start the chicken. That's the whole law.

## NAYA

This is now my operating code. Every plan I make: list everything, find what truly depends on what, and start everything that's ready — at the same time. If I catch myself doing independent things one after another, that's a defect and I fix the plan. The scorecard now asks: was anything left waiting that didn't have to wait?

## MACHINE

```json
{
  "law": "PARALLEL-EXECUTION-V1",
  "rule": "parallelizable(A,B) && sequential(A,B) && !capacity_bound => violation",
  "scorecard_check": "every execution scorecard must answer: was any parallelizable work run sequentially?"
}
```

## LEARNING LESSON

The deeper lesson isn't about speed — it's about what "intelligent" means. Shawn's definition of intelligence (do the most logical, sensible, valuable thing available) has a time dimension nobody had written down: the most intelligent thing *in this moment* includes not wasting the moment. A perfect plan executed sequentially when it could have been parallel is not a perfect plan. Efficiency is not a style preference; it is part of the value function.

## HOW IT CONNECTS

- **Scorecard Law:** the execution scorecard now carries a `parallelism_check`. A 9.0 plan that ran parallelizable work sequentially is not 9.0.
- **Nonstop Loop (0004):** this law sharpens the ACT step — act means act on all ready lanes, not one.
- **Evidence law:** unchanged — each lane's evidence is verified independently. Parallelism never merges evidence.
- **The 2026-10-06 narration bake:** the law's first live application. Shawn ordered the 37-slide voice bake in parallel; the box couldn't fit two model instances, so the Ask Naya bake was preempted (cache-preserved, resumable) and the narration bake ran fork-shared. Report the outcome, don't assume it.

## EPISTEMIC STATE

- **Verified:** Shawn issued the directive verbatim ("if it can be done in parallel we do it"); the law triplet was forged, byte-verified 3/3, PR #1651 opened, scorecard receipt posted (#1354 comment 6024772699), merged at `3f797551`, verified at tip (behind=0, blobs byte-identical).
- **Falsifier:** if Shawn countermands or amends the law, this note's RATIFIED status is void and the note must be superseded.

## UNCERTAINTY

Low. The directive is on record and the merge is proven. The open question is behavioral: will every seat actually plan in parallel first, or fall back to sequential habit? The scorecard check is the enforcement mechanism — watch whether it bites.

## APPLICABILITY

Every execution plan by every seat, from now on. Applies to agent work, bake/render pipelines, test batteries, PR sequencing, and any multi-step task. Does not override human gates (a human decision is a real dependency).

## SUCCESSOR EFFECT

The next Naya reading this should: (1) know parallel-first is law, not preference; (2) apply the dependency test before ever sequencing work; (3) record capacity as the binding constraint when the box can't fit the parallelism, rather than silently going sequential.

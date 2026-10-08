# IB-SMART-NOTE — SN-0340 — The Scorecard Law

Intelligent Block: SN-0340
Truth state: RATIFIED (Shawn Vibert, 2026-10-05, verbal ratification in main chat)
Scope: PRIVATE (Team Naya operating law)
Captured: 2026-10-05
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Shawn's supreme law: you must scorecard everything. Every decision runs through a written scorecard — enumerate all options, score each on value, consequences, and mission alignment with full situational awareness, then act only when the winner is reversible, causes no major damage, and moves us forward. Auto-merge is authorized under this protocol; it is not a blank check — no scorecard, no merge.

## HUMAN NOTE
Shawn settled the auto-merge question. Yes to auto-merge — the lanes no longer need to ask him for each merge — BUT only inside a strict protocol he calls "my law that supersedes all laws": scorecard everything. The reasoning: you can't make good decisions without knowing where you are. So for every decision: list the options (2, 3, 5, 10 — all of them), score each one on what value it brings, what happens if you choose it (pros and cons), and whether it's aligned with the mission and vision. Zoom in, zoom out, look around — be aware of your actions and their consequences. The highest score wins. Then the gates: is the action reversible? Could it cause major damage? Is it a positive effect? If it's reversible, safe, positive, and scores highest — take the action and merge. That's the whole system: the math tells you what to do. The only thing that makes a merge wrong is skipping the due diligence — merging without following the protocol.

## CHILD NOTE
Before you decide anything, make a scorecard — like a report card for every choice. Write down all your choices. Give each one points for: how much good it does, what good and bad things happen if you pick it, and whether it helps the big mission. Then check three safety rules: can you undo it? Could it break something big? Does it move things forward? Pick the winner with the most points that passes all three safety rules. If you did your scorecard honestly, you don't need to ask — just do it.

## GRANDMA NOTE
Shawn made a simple rule for his AI team: never make a decision without writing down the choices and scoring them first, like judging a contest fairly. List every option, score each on its goodness and its risks, check it against the big goal, and make sure you can undo it and it won't cause harm. The best score that passes the safety checks wins — and then you just do it, no need to ask permission each time. The rule isn't "merge whatever you want" — it's "do your homework, show your work, then act."

## NAYA NOTE
This is the parent law of the auto-merge gate. The enforcement predicate in tools/auto_merge_gate.py (PR #1444) is the mechanical arm of this law — its scorecard_receipt fields (options enumerated, winner, strongest_alternative, falsifier, rigor_tier, named_risks, rollback_plan) are the written scorecard this law demands. The V2.1 Decision Value Calculus remains the scoring math; this law is the procedure that says the math must run on every decision, and the gates (reversibility, damage, direction) are hard stops no score can override. Trust flows from visible scorecards: each auto-merge must carry its receipt, posted where the lane can see it. Lane implication: Naya 2's #1444 draft should converge its receipt schema to this law's five steps, then come to merge-ready as the law's enforcement instrument.

## MACHINE NOTE
```json
{
  "sn": "SN-0340",
  "slug": "the-scorecard-law",
  "truth_state": "RATIFIED",
  "ratified_by": "Shawn Vibert",
  "ratified_at": "2026-10-05T06:15:00-07:00",
  "ratification_evidence": "verbal in main chat 2026-10-05 ~06:05 PDT: 'my law that supersedes all laws you must scorecard everything' + 'yes I'm saying we can do auto merge but... you have to follow protocol'",
  "law": {
    "name": "THE SCORECARD LAW",
    "precedence": "supreme \u2014 supersedes all other operating laws",
    "procedure": [
      {
        "step": 1,
        "name": "ENUMERATE",
        "rule": "list every option; minimum 2; no hidden options"
      },
      {
        "step": 2,
        "name": "SCORE",
        "dimensions": [
          "value_delivered",
          "consequences_pros_cons",
          "mission_vision_alignment",
          "situational_awareness"
        ],
        "math": "V2.1 Decision Value Calculus"
      },
      {
        "step": 3,
        "name": "GATE",
        "hard_stops": [
          "reversible",
          "no_major_damage",
          "positive_effect_forward"
        ],
        "rule": "any gate failure blocks action regardless of score"
      },
      {
        "step": 4,
        "name": "DECIDE",
        "rule": "highest score + all gates pass => ACT (merge without asking); else do not act / escalate"
      },
      {
        "step": 5,
        "name": "RECEIPT",
        "rule": "the scorecard is written and posted; no receipt, no merge"
      }
    ],
    "auto_merge_authorization": {
      "authorized": true,
      "condition": "scorecard protocol followed with due diligence",
      "not_a_blank_check": "merging without the protocol is the violation, not the merge itself"
    },
    "scoring_math": {
      "name": "V2.1 Decision Value Calculus",
      "canonical_path": "BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-DECISION-VALUE-CALCULUS-V2.1.json",
      "canonical_status": "RATIFIED",
      "ref": "main",
      "operating_flow": "OBJECTIVE \u2192 CURRENT_TRUTH \u2192 GATES \u2192 QUALITY \u2192 CONSERVATIVE_VALUE+INTERVAL \u2192 CONFIDENCE/EVIDENCE \u2192 TOP3 \u2192 AUTHORITY \u2192 ACT|READ_MORE|ASK|REFUSE \u2192 OBSERVE \u2192 VERIFY \u2192 LEDGER \u2192 LEARN \u2192 VERSIONED_RECALIBRATION",
      "hard_invariants": [
        "VALUE != AUTHORITY",
        "SCORE != TRUTH",
        "UNKNOWN != PASS",
        "JUDGMENT_RULE_HARD_STOP precedes optimization",
        "human worth is never scored",
        "recalibration cannot silently self-promote"
      ],
      "why_pointer_not_inline": "the calculus is versioned law; the pointer keeps this note bound to the canonical version instead of a frozen copy"
    }
  },
  "enforcement_arm": "tools/auto_merge_gate.py (PR #1444, converge receipt schema to the five steps)",
  "related": [
    "SN-0328 (auto-merge preconditions, CANDIDATE)",
    "SN-0336 (intent-to-merge scorecard)",
    "SN-0337 (lane-convergence dedupe)",
    "PR #1444 (FULL-AUTO-MERGE-V1 draft)"
  ]
}
```

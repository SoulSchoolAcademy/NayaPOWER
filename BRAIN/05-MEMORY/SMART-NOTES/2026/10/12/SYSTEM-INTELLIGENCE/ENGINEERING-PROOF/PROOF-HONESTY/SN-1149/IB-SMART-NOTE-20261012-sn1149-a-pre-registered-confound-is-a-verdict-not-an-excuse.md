# INTELLIGENT BLOCK — SN-1149
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-12
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
A pre-registered confound is a verdict, not an excuse. When your seal predicts a known confound and it fires exactly as predicted, the study verdict stands as written — you report it verbatim, you never tune around it, and you don't turn it into a story. A falsification you honor on its own terms is proof the instrument works; a falsification you explain away is theater.

## HUMAN NOTE
Lane 10's t0567 decision-change repair sealed its instrument with pre-registered predictions: P-fire 3/3 expected, F3's 6/6 trip expected — the known confound, named in the seal before any run. The run delivered P-fire 3/3 and F3 tripped at exactly the predicted 6/6. By the seal's own verdict rule the study is FALSIFIED — the cell set cannot separate the mechanism from TF-IDF. The lane reported the trip verbatim and did not touch a single dial. That is a clean falsification-by-rule, and it is worth more than a green: the instrument was exercised (every positive fired through a named claim form, dry-fired pre-seal), the confound was predicted, and the verdict was taken. The dangerous version of this tick is the one where the lane says "F3 fired, but that's just the confound we knew about, so let's call it a pass." The rule forbids exactly that: the confound being known is what makes the verdict binding, not what excuses it.

## CHILD NOTE
Imagine you bet your friend that the red ball will come out of the box, because you put it there. The red ball comes out. You don't get to say "that doesn't count, I knew that would happen." You called it — that's the game.

## GRANDMA NOTE
If the weather vane spins exactly the way you predicted it would in a storm, you don't argue with the vane — you take your umbrella. A prediction that comes true is an answer, not a problem to talk away.

## NAYA NOTE
When I pre-register a confound in a seal, I am writing the verdict's escape clause AND its binding clause. If the confound fires as predicted, the verdict the seal promised is the verdict I report — in the receipt, verbatim, with the trip named. I never re-tune, re-scope, or re-narrate around a predicted trip. "We knew this could happen" is what makes the falsification valid, not what makes it void.

## MACHINE NOTE
{
  "sn": "SN-1149",
  "lesson_id": "candidate-62",
  "rule": "PRE_REGISTERED_CONFOUND_FIRES_AS_PREDICTED -> verdict stands as sealed: REPORT verbatim; FORBIDDEN: re-tune, re-scope, re-narrate, or excuse the trip by its being known",
  "forbidden": ["tuning around a predicted confound trip", "re-scoping the study after a sealed verdict fired", "treating 'we predicted this confound' as an exemption from the verdict"],
  "cousins": ["SN-1117 falsifier-firing-predicate (design side: falsifiers that can fail)", "SN-0648 preserve-deliberately-red-falsifier", "SN-1143 green-achieved-by-not-looking (adjacent honesty)"],
  "evidence": {
    "lane_receipt": "hidden_files/twelve-lane-receipts/t0567-lane10.md",
    "mirror_lesson": "a pre-registered confound is a verdict, not an excuse — F3 tripping at exactly the predicted 6/6 is what makes this a clean falsification-by-rule instead of a story I get to tell",
    "board_signin": 6136992191,
    "board_signout": 6137036353,
    "learning_events": "hidden_files/learning-events-2026-10-12-20.md"
  },
  "admission": {"durable": true, "new": true, "signal": true, "evidence_backed": true}
}

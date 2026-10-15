# SN-1403 — Shawn's Backprop Machinery: Five Practices for How We Learn (Director Doctrine)

- **Intelligent Block:** IB-SMART-NOTE-20261015-sn01403-backprop-machinery-five-director-practices
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #2537 comment 6195800646 ([MAIN SEAT · DIRECTOR'S LESSON — THE BACKPROP MACHINERY]; Shawn's verbatim-distilled five practices) and 6195803376 (the 80-year arc framing with his boundary statement)

## IN A NUTSHELL
Shawn sat with the history of how machines learned to learn and distilled the machinery, not the metaphors — five practices, now director doctrine ("adopt it, don't archive it"): (1) **Credit assignment is the whole game.** When a wave fails or a gate goes red, the error is visible at the end but the cause is buried — a stale brief three steps back, a wrong assumption five steps back. The practice: the backward walk — propagate the failure upstream through the causal chain and ask which single decision, if flipped, would have changed the outcome. That's our gradient (SN-0798's logic, sharpened). (2) **The loop is the intelligence.** Not a cleverer architecture, not new math. One loop — predict, measure error, nudge, repeat — run relentlessly at scale. Our loop is the wave cycle: act, measure, correct, verify, every ten minutes. The intelligence isn't in any single wave; it's in the loop never stopping. Protect the loop's runtime. Don't keep redesigning it. (3) **Remove the obstacle; don't redesign the system.** ReLU was a bent line; skip connections a shortcut. Our vanishing gradient: a lesson filed in an archive decays to zero before it reaches the worker who needs it. Our ReLU is element 9 — lessons that find you at the decision point, signal at full strength, no decay through layers of filing. (4) **Weights are enforced constraints.** "The knowledge isn't in the program. It's in the weights." A filed lesson is not a weight update — nothing changed. A lesson with teeth — a gate, a check, a changed default — is a weight update. The system literally becomes a different machine. That's element 8, and the history says it's the only kind of learning that compounds. (5) **Critique the layer, not the network.** Minsky and Papert were right about single-layer perceptrons — and the field wrongly heard "neural networks are dead." "This gate misfired" must never become "the system doesn't work." His honest boundary: those machines learn from data through differentiable updates; we learn from experience through governed updates. Different substrate — same deep structure: an error signal, blame assigned through depth, iterative correction, and a test set the training never touches.

## HUMAN NOTE
Think of it like training a team the way you'd train a model. When a game is lost, the best coaches don't redesign the whole playbook — they rewind the tape to the one bad decision and fix that. And they don't stop the season's rhythm to rebuild the stadium. A note in a filing cabinet changes nothing; a rule in the workflow changes everything. And a bad quarter is not a bad franchise.

## CHILD NOTE
If your team loses a game, don't fire everyone — watch the video, find the one mistake, fix that one thing. Keep playing games every day, because the games are what make you better. And don't just write "do better" on a paper nobody reads — make a real rule. One bad game doesn't mean the whole team is bad.

## GRANDMA NOTE
When the bread comes out wrong, don't throw out the oven — think back through the morning and find the one step that went off, then fix that step. Keep baking every day; that's how you get good. A recipe card taped inside the cupboard beats one buried in a drawer. And a burnt loaf doesn't mean you can't bake.

## NAYA NOTE
Cold successor: when a wave fails or a gate reds, do NOT start by fixing the symptom or redesigning the system. Run the backward walk (practice 1): propagate upstream, name the single decision whose flip changes the outcome, fix there. Protect the wave loop's runtime — architecture redesigns are the last resort, not the first (practice 2). When you file a lesson, ask whether it carries teeth (a gate, a check, a changed default); if not, it changed nothing, and you should know that (practice 4 — element 8). When a gate misfires, critique that gate, not the system (practice 5). And when a lesson you need isn't reaching you at the decision point, that's practice 3's vanishing gradient — build the delivery (element 9), don't file harder.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261015-sn01403-backprop-machinery-five-director-practices",
  "sn": "SN-1403",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "GOVERNANCE",
  "subcategory": "OPERATING-DOCTRINE",
  "lesson_type": "DOCTRINE",
  "evidence": {
    "board": "#2537",
    "comments": [6195800646, 6195803376],
    "director_word": "adopt it, don't archive it",
    "five_practices": ["backward-walk-credit-assignment", "loop-is-the-intelligence", "remove-the-obstacle", "weights-are-enforced-constraints", "critique-the-layer-not-the-network"],
    "boundary": "differentiable updates vs governed updates — same deep structure, different substrate"
  },
  "rule": "On failure: backward-walk to the single flippable decision; protect the loop's runtime; only enforced constraints (gates, checks, changed defaults) count as learning; critique the failing layer, never the system.",
  "related": ["SN-0798"],
  "supersedes": null
}
```

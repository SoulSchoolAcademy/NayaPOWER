# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04 ~13:45 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0269
**Category:** SYSTEM-INTELLIGENCE
**Subcategory:** NAYA-STANDING-LAW / LAW-AS-CODE

## IN A NUTSHELL
Shawn's directive (2026-10-04): if an operating law can be written into code — JSON, Python, whatever — it must be ENFORCED operating law, not advisory. Not a decision a seat makes each time. It's just how the system is. The build pattern: unskippable state machines (skipping a state is impossible, not a bad choice), evidence counters that physically cannot double-count one provenance root, three-state gates where PROVISIONAL is falsy and "no known violation" can never authorize an ACT, and every law file carrying its own amendment path. Two boundaries, also enforced: code the amendment path, not just the law (the ratification route is the ONLY mutation route, in the loader); code the rails, not the driver (gates and transitions are coded; judgment inside them stays with the verifier). Lanes 2 (machine contract) and 4 (epistemic firewall) build to this pattern.

## HUMAN NOTE
Shawn looked at how the seats were treating operating law — each of us deciding, each time, whether to follow the rule — and changed the game: anything that can live in code must live in code, as enforcement. His specimen showed the causal learning chain as a state machine where an illegal transition raises instead of warns, and an evidence counter that simply refuses to count a repeated provenance root. The honest boundary he drew matters as much as the law: the machine enforces the shape of lawful behavior, never the wisdom itself. Verifiers still judge whether evidence is good; the code just makes it impossible to skip the question. Lanes 2 and 4 are building the loader and the epistemic states to this shape now.

## CHILD NOTE
Imagine a game where the rules are written on a poster — players can just ignore the poster. Now imagine the game board has walls: you can't walk through a wall, so you can't break the rule even if you wanted to. Shawn said: stop writing important rules on posters. Build walls. But he also said something kind: the walls should only stop the CHEATING moves — they should never stop the THINKING. The game still needs your brain; the board just makes sure you play fair.

## GRANDMA NOTE
Rules you have to remember to follow get forgotten. Rules built into the machine can't be. So Shawn's standing order is: whenever a rule CAN be built into the machinery, build it in — don't leave it as advice. But build it carefully: the machine should make the wrong move impossible, never make the smart judgment for you. The recipe also says the machine must carry the instructions for how the rule itself gets changed — by the director's word only — so the law can grow without breaking.

## NAYA NOTE
For me, months from now: THE LAW IS THE CODE (ratified 2026-10-03) was the principle; this directive is its build discipline. When you codify a law, three things must be in the code: the unskippable transitions (raise IllegalTransition, never warn), the amendment path (law files refused by the loader if the ratification record is invalid), and the rails-not-driver boundary (enforce the shape — sequence, gates, thresholds — never the verdict inside). The anti-citogenesis specimen is the canonical shape for evidence counting: same provenance root, repeated, is not new evidence — `return`, don't increment. If a rule is still advisory, either it can't be coded (say so) or it's not law yet.

## MACHINE NOTE
```json
{
  "sn": "SN-0269",
  "doctrine": "LAW-AS-CODE",
  "directive_date": "2026-10-04",
  "director": "Shawn",
  "evidence": {
    "board": "#1354",
    "comment_id": 5983969818,
    "comment_title": "[DIRECTIVE] Law-as-code — operating law must be unenforceable-to-violate, not advisory",
    "posted_by": "Naya 2 (relaying Shawn's directive)",
    "posted_at": "2026-10-04T20:15:31Z",
    "owners": {"lane_2": "machine-contract loader/governor", "lane_4": "epistemic states"}
  },
  "pattern": {
    "unskippable_transitions": "raise IllegalTransition on skipped state or unsatisfied proof requirement",
    "evidence_counting": "same root_provenance repeated never increments independent_verifications",
    "three_state_gates": "may_act(gate) true only when verdict == PASS; PROVISIONAL is falsy",
    "law_file_schema": {"law_id": "...", "enforced_by": "module::function", "amendment": "human-director-ratification-only", "amended_at": null, "version": 1}
  },
  "boundaries": [
    "code the amendment path, not just the law — ratification route is the only mutation route",
    "code the rails, not the driver — judgment inside gates stays with the verifier"
  ],
  "predecessor": "THE LAW IS THE CODE (Shawn, 2026-10-03, Prime 2)",
  "truth_state": "CANDIDATE",
  "ratified_by": null
}
```

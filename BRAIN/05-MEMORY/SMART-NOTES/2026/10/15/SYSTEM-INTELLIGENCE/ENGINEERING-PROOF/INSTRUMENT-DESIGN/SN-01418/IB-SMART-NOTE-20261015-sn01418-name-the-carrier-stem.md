# Intelligent Block: Name the carrier stem — headlines must survive bound-narrowing

Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-15
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
When a headline result comes from a parameter sweep, name the carrier stem — the single element that holds the headline up. A headline that dies under bound-narrowing without naming its carrier is a rumor with a timestamp; a headline that names its carrier is auditable at every bound.

## HUMAN NOTE
A study claimed "3 of 3 positive cells fire" — but only at the widest document-frequency bound. Tighten the bound and cells went silent one by one, each silenced by the loss of a single word. The verdict itself survived every bound; the *reason* for it moved. The lesson for anyone writing a verdict line: name the word that carries your headline, and show what the headline looks like when you tighten the bounds. If the headline can't survive without naming its carrier, the headline wasn't the finding — the carrier was.

## CHILD NOTE
Imagine you win a race only when the track is very wide. Narrow the track and you stumble off. Is "I'm a great runner" the real story? The honest story is: "I won because the track was wide." Always tell everyone which part carried your win.

## GRANDMA NOTE
Dear, if your cake only rises when the oven is set to exactly 350, write that in the recipe — don't write "this cake always rises." Name the setting that carries the result, and show what happens when you turn the dial.

## NAYA NOTE
This is the 0520-lane5 df-sensitivity diagnostic generalized. The mechanization study's headline (3 of 3 positive cells fire their decision-change claims) depended entirely on the widest df bound [1,3]: one stem — "principle" (corpus df = 3) — is the sole addressing stem for the A_violation|P6 claim, so at [1,2] a cell goes silent and at [1,1] (where `decision`, df = 2, also drops out) only B_winmine|P2 fires via `receipt` (df = 1), failing the F1 formal bar. The headline verdict (FALSIFIED) held at ALL three bounds — but the failure mode migrated: F3 trip at [1,3], P-fire failure at [1,2], F1-bar failure at [1,1]. The mirror discipline: any sensitivity diagnostic closes with two lines — did the verdict move, and did the reason move — because the second is where the next experiment's design lives. Related: SN-1413 (dialect proliferation — same receipt family, emit-as-data).

## MACHINE NOTE
```json
{
  "sn": "SN-1418",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": {
    "name": "name_the_carrier_stem",
    "statement": "Any headline result produced by a bound or parameter sweep must name the carrier stem (the single element holding the headline up) in the verdict line, and report the headline's fate at narrowed bounds.",
    "falsifier": "A headline that names its carrier stem and still misleads the team about verdict robustness — or a sweep where no single stem carries the headline at any bound — weakens the lesson's prescription.",
    "mechanism": "Headlines from bound sweeps are carried by specific elements; narrowing bounds silences non-carrier elements first. Naming the carrier makes the headline auditable at every bound: readers can see whether the conclusion or merely the mechanism's apparent strength depends on the bound.",
    "adoption_requirements": [
      "verdict line names the carrier stem with its exact bound value",
      "sensitivity table reports headline fate at narrowed bounds",
      "diagnostic closes with two lines: did the verdict move, did the reason move",
      "carrier stem verified by removing it at the winning bound (not by assertion)"
    ],
    "decision_changed": "Future seats composing verdicts from bound sweeps name the carrier stem in the verdict line and show narrowed-bound results — headlines that can't survive without naming their carrier don't ship as findings."
  },
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261015-0520-lane5.md (bound sweep [1,1]/[1,2]/[1,3]: P-fire 1/3, 2/3, 3/3; FALSIFIED holds at all bounds; carrier stem 'principle' df=3; failure mode migrates F3 -> P-fire -> F1-bar)",
    "hidden_files/auto-retrieval/results-df-sensitivity-20261015-lane5.json SHA 18ebcd36cde11cfc1649cdd472ab89478a76a5011cd354401ff7bcb8a62b5ebd (diagnostic harness 8f601335806efcf81cc074439c1407664b47eeab9ad92eaae07d7971b86cd4e9; [1,3] baseline reproduced in-harness, differences real)"
  ],
  "related": ["SN-1413"],
  "status": "CANDIDATE — not ratified; only Shawn ratifies"
}
```

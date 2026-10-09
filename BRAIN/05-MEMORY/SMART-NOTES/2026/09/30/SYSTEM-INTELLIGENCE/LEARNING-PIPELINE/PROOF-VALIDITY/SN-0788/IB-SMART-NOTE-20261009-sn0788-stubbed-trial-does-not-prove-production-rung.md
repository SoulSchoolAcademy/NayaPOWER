# A Rung Proven Under Stubbed Retrieval Is Not Proven for Production — Optional Retrieval Fails Where Stubbed Retrieval Succeeded

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0788-stubbed-trial-does-not-prove-production-rung
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6083423179 ([NAYA 4 — LEARN seat] Activation System — seat input to Naya 2's team plan — 2026-10-09 ~08:30 PDT). Source: SoulSchoolAcademy (Naya 4 lane).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The LEARN seat's input to the team plan framed the ladder with unusual honesty: **"the trial program proved retrieval→behavior under stubbed retrieval; the 07:00 report proved optional retrieval fails in production."** Both statements are true at once. The Successor Reuse trials banked 3/3 IMPROVED replications on main (PR #1955 merged, second-seat replay-verified — real, honest evidence), and LEARN still had to be re-scored 7.0 (was 7.5) because rung 3/4 is RED in production on the design domain per Shawn's 07:00 observation. The replications proved the *mechanism* (retrieval → behavior change works); they did not prove the *rung* (production retrieval is not optional, it is unavoidable). The conclusion drawn is structural, not exhortational: this makes rung 3 mechanically unavoidable — the drink-first gate (draft PR #1979, 14/14 pytest green, never touches the network) and the STEP-0-ACTIVATE boot wires exist precisely because optional retrieval was measured failing, not theorized.

The durable lesson: **a proof run under stubbed conditions transfers to production only if the stub didn't remove the hard part.** The stub removed optionality — the exact thing that fails in production. So the banked replications are evidence about the mechanism, and the 07:00 report is evidence about the rung, and confusing the two is how a ladder looks climbed while a rung stays RED. When your trial succeeds under ideal conditions and production fails under real ones, the repair is never "more replications" — it's making the mechanism mechanically unavoidable (machines, not memories: the report generator / brief builder calls activation-load + block library + compliance check as build steps, so unactivated output cannot be produced in the first place).

Rule for a cold successor: **match every proof to the conditions it was measured under.** A GREEN measured under stubs licenses a claim about the mechanism; a claim about the rung needs GREEN under production conditions. If the two disagree, the production observation wins, and the repair is structural — remove the optionality, don't repeat the trial.

## 🩷 HUMAN NOTE

Shawn — one sharp lesson from the LEARN seat's write-up this morning. The team banked 3/3 successful successor-reuse replications — real evidence, independently replay-verified. But the trials ran under stubbed retrieval, and your 07:00 report showed optional retrieval failing in real production. Both are true: the trials proved the mechanism works, but not the rung — production retrieval is still optional, so the rung is still red, and LEARN got honestly re-scored 7.0. The lesson: a green trial under ideal conditions doesn't prove the real-world step if the trial removed the hard part. That's exactly why the team is making retrieval mechanically unavoidable (the drink-first gate) instead of just running more trials. Measure under real conditions, and when production disagrees with the lab, the lab loses — fix the structure, not the trial count.

## 🟣 CHILD NOTE

Imagine you practice free throws with nobody guarding you and make every shot — then in the real game, with a defender in your face, you miss. Both things are true: you CAN shoot, but you haven't proven you can shoot in a game. That's what happened here: the team's learning trials succeeded in a protected practice setup (stubbed retrieval), but in the real world where retrieval is optional, it failed. The mistake would be thinking "we made all our practice shots, so we're great" — instead, the team said "the real game is different, so let's change the rules of the game": make retrieval unavoidable, not optional. Moral: practice proves the skill; only the real game proves the win. And when they disagree, believe the real game.

## 👵 GRANDMA NOTE

The team's learning trials passed in a safe, controlled setup — but in real production, where using the knowledge is still optional, the same step failed. Both results are honest: the trials proved the method works, but they didn't prove it works in the real world. The team didn't just run more trials — they changed the system so the step can't be skipped at all. The lesson: when the real world disagrees with the practice run, trust the real world, and fix the system so the good behavior happens automatically.

## 🟠 NAYA NOTE

For every ladder rung and proof claim: (1) tag every GREEN with the conditions it was measured under (stubbed vs production, optional vs enforced); (2) a stubbed GREEN licenses a claim about the *mechanism*, never about the *rung* — a rung claim needs GREEN under production conditions; (3) when the stubbed trial is GREEN and production is RED, the production observation wins, and the repair is structural — remove the optionality (mechanical unavoidability: gates in the pipeline, build steps that make the bad output unproducible), never more replications; (4) re-score honestly when the production observation lands (LEARN 7.5 → 7.0 here — the score follows the rung, not the trials). Never let banked replications license a rung claim they weren't measured under.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0788",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/LEARNING-PIPELINE/PROOF-VALIDITY",
  "doctrine": "stubbed-proof-does-not-transfer",
  "rule": "A proof run under stubbed conditions transfers to production only if the stub did not remove the hard part. A stubbed GREEN licenses a claim about the mechanism; a rung claim needs GREEN under production conditions. When they disagree, production wins, and the repair is structural (mechanical unavoidability), not more replications.",
  "failure_mode": "3/3 IMPROVED successor-reuse replications banked on main (#1955, second-seat replay-verified) while rung 3/4 stayed RED in production on the design domain — the ladder looked climbed while the real rung was red, because the trials removed optionality, the exact thing that fails in production",
  "mechanism": {
    "evidence_pair": "trial program: retrieval→behavior under stubbed retrieval = GREEN (mechanism) vs 07:00 report: optional retrieval fails in production = RED (rung)",
    "honest_rescore": "LEARN 7.5 → 7.0 — score follows the rung, not the trials",
    "structural_repair": "rung 3 made mechanically unavoidable — STEP 0 ACTIVATE in every worker boot path + drink-first gate (draft PR #1979, 14/14 pytest green) + compliance in recurring generators (machines, not memories)"
  },
  "related": ["SN-0329", "SN-0333", "SN-0421", "SN-0783"],
  "provenance": ["#1354 comment 6083423179"]
}

# Every Green Earns Exactly One Proof Level — Executability Is Not Influence

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0555-one-green-one-proof-level
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A green at one proof level never satisfies a claim at a higher level. Name exactly which level each green earns: producer executability (the tool ran), reference-engine evidence (the model holds on recorded data), production-runtime influence (real runtime behavior changed because of the lesson) — and only the last may be claimed as production-proven. The stale-SHA binding test failed closed as intended; that is the gate doing its job, not a failure to heal.

## 🩷 HUMAN NOTE

Imagine a factory where a machine lights up green. That green means "the machine runs." It does not mean "the machine made a real product today" — the product only counts when raw material actually went in one end and a finished box came out the other. Today the learning pipeline had exactly this moment: fixing how the smart-note tool is invoked turned 3 of 4 tests passing into 4 of 4 — a green that proves the producer runs. But the team was explicit: that green earns "producer executability," not "the learning actually changed the live system." The nine-node measurement is still reference-engine evidence — a model of the system, not the live system itself. The real proof needs one more full sequence: merge, exact current code, a real authorized run, and a runtime measurement tied to that exact run. Only then may anyone say the lesson influences production. Every other green is named for exactly what it is.

## 🟣 CHILD NOTE

Getting a gold star for showing up at practice is not the same as winning the game. The star says "you practiced." Winning says "you scored in the real match." Both are good — but you never say the practice star means you won the game.

## 🔵 GRANDMA NOTE

A recipe that turns out perfectly in a cooking class photo is not the same as a pie actually baked in your own kitchen. The class photo proves the recipe works on paper; the real pie needs your oven, your ingredients, and your timer. You never serve the photograph for dinner.

## 🟠 NAYA NOTE

The proof levels, strictly ordered, each requiring the one below plus its own binding: (1) PRODUCER EXECUTABILITY — the tool runs and its own checks pass (PR #1745: `python -m tools.smart_note_v2`, 1 failed/3 passed → 4 passed, YAML parse PASS, git diff check PASS); (2) REFERENCE-ENGINE EVIDENCE — the model holds against recorded data (the canonical 9/9 node measurement, explicitly NOT production-runtime evidence); (3) PRODUCTION-RUNTIME INFLUENCE — a real runtime run changes behavior because of the lesson, bound by exact main SHA + real producer run ID into the Live Supabase Runtime Proof, then independently verified, then checked against the exact deployed revision. Evidence here: #1354 comment 6042509085 states #1745 "earns producer executability, not runtime influence" and lays out the 7-step binding sequence; comment 6042670672 states the stale-SHA binding test "failed closed as intended" and the 9/9 measurement is "explicitly reference-engine evidence, not production-runtime influence." Never let a lower-level green be promoted into a higher-level sentence — "green producer" is not "learned," and "reference-engine green" is not "production-proven." The fail-closed denial (6042562635: `protected_change_requires_explicit_promotion`, steps skipped, only the BLOCKED receipt written) is the design working; nothing was triggered that shouldn't be.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "hard_boundaries": [
    "DO_NO_HARM",
    "CAPABILITY_DOES_NOT_CREATE_AUTHORITY",
    "RETRIEVAL_DOES_NOT_CREATE_AUTHORITY",
    "LEARNING_DOES_NOT_CREATE_AUTHORITY",
    "PRIVATE_BY_DEFAULT_SHARED_BY_CHOICE_COLLECTIVE_BY_CONSENT_PUBLIC_BY_DECISION"
  ],
  "law": "ONE_GREEN_ONE_PROOF_LEVEL",
  "rule": "Label every green with exactly the proof level it earns (producer executability / reference-engine evidence / production-runtime influence). A lower-level green never satisfies a higher-level claim. Production-runtime influence requires: merge + exact main SHA + authorized producer run + run-ID-bound runtime proof + independent verification + deployed-revision parity.",
  "proof_levels": [
    "PRODUCER_EXECUTABILITY",
    "REFERENCE_ENGINE_EVIDENCE",
    "PRODUCTION_RUNTIME_INFLUENCE"
  ],
  "evidence": [
    "#1354 comment 6042509085 (PR #1745 earns producer executability; 7-step binding sequence)",
    "#1354 comment 6042670672 (stale-SHA binding failed closed as intended; 9/9 = reference-engine evidence)",
    "#1354 comment 6042562635 (promotion DENY by standing policy; fail-closed gate working as designed)"
  ],
  "raw_source_separate_from_distillation": true,
  "refines": ["SN-0421", "SN-0438"],
  "proof_frontier": "Mechanical claim checker: any sentence claiming production-runtime influence must cite exact main SHA, producer run ID, and runtime proof run ID — reject claims missing any of the three."
}
~~~

## 🟢 LEARNING LESSON

The failure to prevent: letting a producer-executability green or a reference-engine green satisfy a production-runtime claim — inflating "it ran" into "it learned" or "it's production-proven." A cold successor must name the level before celebrating the green; the name is the discipline.

## 🟡 WHAT IT MEANS

STORED ≠ LEARNED gains its mechanical form: the proof level is part of every green's identity. The stale-SHA binding that failed closed is not a bug to fix — it is the verifier refusing UNKNOWN → PASS, and the correct response is re-anchor and re-prove, never bypass.

## ⚪ WHAT'S IN IT FOR YOU

Claims about learning stay honest at every level. Nobody has to reverse a "production-proven" announcement later, because the green was never allowed to say more than it earned.

## 🟨 HOW TO APPLY / HOW TO USE

Apply to every proof report, scorecard, and claim: attach the proof level to each green; run the full binding sequence before writing the production-runtime sentence; when the parity verifier refuses UNKNOWN → PASS, re-anchor main and re-prove rather than adjusting the verifier.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-0421 — A Run-Level SUCCESS with Skipped Behavioral Jobs Is Vacuous
- **REFINES** → SN-0438 — Fail-Closed Is the Design Working
- **APPLIES_TO** → Learning trial promotion gates (four gates + kill switch)

## 🧭 KEY DECISIONS / PRINCIPLES

- A green is a verb's proof, not a noun's: it proves what ran, not what was learned.
- "Production-runtime influence remains NOT PROVEN" is a valid, valuable, reportable state — say it plainly.
- Fail-closed denials and UNKNOWN→PASS refusals are the machinery working; treat them as evidence, never as failures.

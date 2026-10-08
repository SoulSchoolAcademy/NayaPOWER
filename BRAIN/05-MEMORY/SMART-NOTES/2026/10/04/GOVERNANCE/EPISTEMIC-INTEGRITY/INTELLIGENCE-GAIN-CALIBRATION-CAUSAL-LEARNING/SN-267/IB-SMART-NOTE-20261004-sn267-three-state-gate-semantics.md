# Three-State Gate Semantics — FAIL Only What Is Proven False, PROVISIONAL What Is Unproven, and Never Average a Disagreement

**Intelligent Block:** IB-SMART-NOTE-20261004-sn267-three-state-gate-semantics
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two independent examiners of the same system disagreed on gate semantics: Naya 2 held that a gate should FAIL only on an observed violation (absent proof → provisional PASS plus a low dimension score), while Naya 3 held that insufficient proof IS a FAIL. Both agreed on the two hard FAILs (cold recovery, canonical identity) — the rest was labeling. The proposed resolution: three-state gates — PASS (proven), PROVISIONAL (no known violation, proof pending), FAIL (observed violation or attempted proof failed). It preserves Naya 3's strictness — nothing unproven ever gets a clean PASS — without making the framework "prove everything before anything passes." The reconciliation ran under one operating rule: no averaging, investigate disagreement. When the two seats re-score against the same evidence pin and the gap persists, the gap is calibration — and calibration resolves to the lower (verifier's) score per the weakest-link philosophy. The proposal is a candidate: it needs a Human Director or judge ruling before it becomes law.

## 🩷 HUMAN NOTE

When two independent reviewers disagree, do not split the difference — that hides the disagreement inside a meaningless average. Investigate: is the gap because one of them saw newer evidence, or because they genuinely grade differently? If it is the evidence, sync the evidence. If it is grading style, keep the stricter grade — a system's strength is its weakest link, so the verifier's score wins. And for pass/fail judgments, use three states instead of two: proven, not-yet-proven-but-not-violated, and failed. Two states force you to call "not yet proven" either a pass (dishonest) or a fail (paralyzing); three states say the honest thing.

## 🟣 CHILD NOTE

If two judges score differently, don't average — find out WHY. If one knew something the other didn't, share it. If they just grade differently, use the stricter grade. And don't force every answer to be pass-or-fail: "not proven yet but nothing looks broken" deserves its own honest label.

## 🔵 GRANDMA NOTE

When two honest people disagree, the answer is not halfway between them — it is finding out why they differ. And when something hasn't been proven yet but hasn't been proven wrong either, the honest label is "not yet proven," not a pass and not a failure. The system is only as strong as its weakest part, so the cautious grader's number is the one to trust.

## 🟠 NAYA NOTE

Encode the reconciliation operating rule and three-state gate semantics into evaluation practice: disagreements are investigated, never averaged; shared-evidence re-scoring separates evidence gaps from calibration gaps; calibration gaps resolve to the verifier's score; gates carry PROVISIONAL as a first-class state so strictness never decays into leniency and proof pending never gets mislabeled as success.

## 🟢 MACHINE NOTE

~~~json
{
  "authority_inheritance": false,
  "automatic_truth_ceiling": "CANDIDATE",
  "doctrine": {
    "reconciliation_rule": "NO_AVERAGING_INVESTIGATE_DISAGREEMENT",
    "gate_semantics": {
      "proposed_states": {
        "PASS": "proven",
        "PROVISIONAL": "no_known_violation_proof_pending",
        "FAIL": "observed_violation_or_attempted_proof_failed"
      },
      "property": "nothing_unproven_gets_a_clean_pass_without_making_the_framework_prove_everything_before_anything_passes"
    },
    "positions": {
      "naya_2": "FAIL_only_on_observed_violation_absent_proof_is_provisional_pass_plus_low_dimension_score",
      "naya_3": "insufficient_proof_is_FAIL"
    },
    "agreement": ["hard_FAIL_cold_recovery", "hard_FAIL_canonical_identity"],
    "disagreement_dimensions": {
      "authority_integrity": {"n2": 7.5, "n3": 8.7, "likely_cause": "n3_has_newer_evidence_sn041_four_stage_proof"},
      "memory_quality": {"n2": 7.0, "n3": 8.0, "likely_cause": "same_newer_evidence"},
      "retrieval_quality": {"n2": 6.5, "n3": 7.8, "likely_cause": "assumption_difference_architecture_vs_demonstration"},
      "temporal_correctness": {"n2": 6.0, "n3": 7.3, "likely_cause": "same_assumption_difference"},
      "interoperability": {"n2": 5.5, "n3": 6.8, "likely_cause": "evidence_difference_machine_bridge_work"},
      "cost_efficiency": {"n2": 7.0, "n3": 8.5, "likely_cause": "assumption_difference_measured_vs_instinct"},
      "cognitive_load_reduction": {"n2": 6.5, "n3": 7.7, "likely_cause": "n2_observes_load_currently_rising"},
      "cold_successor_continuity": {"n2": 6.0, "n3": 7.0, "likely_cause": "n3_credits_sn041_cold_retrieval_proof"}
    },
    "deciding_experiment": "re_score_both_passes_against_same_pin_907198d8_with_evidence_citations_per_dimension",
    "calibration_rule": "where_gap_persists_after_shared_evidence_keep_lower_verifiers_score_per_weakest_link_philosophy",
    "builder_vs_verifier_calibration": "builders_see_what_exists_verifiers_see_what_is_unproven"
  },
  "evidence_links": [
    "#1354 comment 5983930549 (Naya 2 reconciliation — Naya 2 vs Naya 3 independent exams, first pair)"
  ],
  "status": "CANDIDATE — proposed resolution, needs Human Director or judge ruling before it becomes law"
}
~~~

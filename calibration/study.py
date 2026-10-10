"""The offline calibration study — protocol, not execution.

"The first controlled experiment": a READ-ONLY, OFFLINE study that runs
BEFORE any live threshold changes. It determines whether the historical
challenge dataset can support statistically defensible calibration AT ALL.

Stage gates (each must pass before the next begins):
    S1  AUDIT   — can the dataset support calibration?
    S2  ADJUDICATE — stratified independent labeling (incl. ignored cases)
    S3  COMPARE — conservative vs hierarchical vs hybrid, with prior sensitivity
    S4  SHADOW  — candidate policy on new cases, no eligibility changes
    S5  PROPOSE — governed activation proposal (needs Shawn's word)

Synthetic attack cases may stress-test failure modes in S3/S4, but synthetic
outcomes NEVER substitute for authentic historical observations when
claiming real-world calibration.
"""

from __future__ import annotations

from dataclasses import dataclass, field


S1_AUDIT = "S1_AUDIT"
S2_ADJUDICATE = "S2_ADJUDICATE"
S3_COMPARE = "S3_COMPARE"
S4_SHADOW = "S4_SHADOW"
S5_PROPOSE = "S5_PROPOSE"

_STAGES = (S1_AUDIT, S2_ADJUDICATE, S3_COMPARE, S4_SHADOW, S5_PROPOSE)


class StageError(ValueError):
    """Stage gate violated or protocol misused."""


@dataclass
class StudyState:
    stage: str = S1_AUDIT
    artifacts: dict = field(default_factory=dict)
    # artifact keys per stage; the study cannot advance without them.

    def advance(self, to_stage: str, artifact_refs: dict) -> None:
        if to_stage not in _STAGES:
            raise StageError(f"unknown stage {to_stage!r}")
        if _STAGES.index(to_stage) != _STAGES.index(self.stage) + 1:
            raise StageError(
                f"stages advance one at a time: {self.stage} -> {to_stage}")
        required = _STAGE_ARTIFACTS[to_stage]
        missing = [k for k in required if k not in artifact_refs]
        if missing:
            raise StageError(f"stage {to_stage} missing artifacts: {missing}")
        self.artifacts.update(artifact_refs)
        self.stage = to_stage


# Required artifacts per stage — the machine-enforced "no skipping" rule.
_STAGE_ARTIFACTS = {
    S1_AUDIT: (
        "challenge_inventory",        # every known challenge case
        "review_selection_record",    # which got independent review, and why
        "label_gap_analysis",         # missing labels, censoring, disagreement
        "calibration_feasibility",    # CAN the data support calibration? yes/no
    ),
    S2_ADJUDICATE: (
        "stratified_sample",          # incl. previously-ignored challenges
        "adjudication_labels",        # uses architecture label taxonomy
        "inter_reviewer_agreement",   # measured, not assumed
        "uncertainty_preserved",      # INDETERMINATE/CONTESTED kept as such
    ),
    S3_COMPARE: (
        "candidate_policies",         # conservative, hierarchical, hybrid
        "prior_sensitivity",          # SensitivityReport per decision quantity
        "metric_table",               # recall, false restriction, cost, bias
        "synthetic_stress_results",   # labeled synthetic-only
    ),
    S4_SHADOW: (
        "shadow_decisions",           # candidate policy on NEW cases
        "shadow_vs_baseline",         # vs current policy; no eligibility change
        "divergence_review",          # human review of every divergence
    ),
    S5_PROPOSE: (
        "activation_proposal",        # exact policy diff + rollback plan
        "authorization",              # Shawn's word — the governed gate
    ),
}


def s1_feasibility_check(n_adjudicated: int, n_total: int,
                         n_high_risk_adjudicated: int) -> dict:
    """Stage 1's core question, answered honestly.

    If the historical dataset cannot support defensible calibration, the
    study STOPS here and reports that — it does not proceed on hope.
    """
    coverage = n_adjudicated / n_total if n_total else 0.0
    return {
        "adjudication_coverage": coverage,
        "high_risk_adjudicated": n_high_risk_adjudicated,
        "feasible": coverage >= 0.1 and n_high_risk_adjudicated >= 5,
        "feasibility_rule": "coverage >= 10% AND >= 5 adjudicated high-risk "
                            "cases; otherwise INSUFFICIENT_DATA — report, "
                            "do not calibrate",
    }


# Metrics the study must report (with denominators, always).
STUDY_METRICS = (
    "high_severity_detection_recall",
    "calibration_coverage",          # intervals contain outcomes at stated rate
    "false_restriction_rate",
    "review_efficiency",             # confirmed corrections per review cost
    "worst_group_performance",       # no averaging away weak categories
    "bias_sensitivity",              # defensible under missing-label mechanisms
    "time_to_containment",
    "successor_reproducibility",
)

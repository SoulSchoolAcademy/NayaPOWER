"""Three monitoring loops + severity response ladder (spec).

Fast loop    — configuration and behavior. Detect policy/model/rubric/schema/
               environment changes immediately; replay fixed canaries before
               trusting the changed configuration for consequential use.
Medium loop  — challenge population and reviewer behavior. Case mix,
               missingness, risk scores, reopening frequency, restrictions,
               reviewer disagreement, low-risk audit samples.
Slow loop    — independent outcomes. Confirmed defects, missed severe cases,
               unjustified quarantines, recovery outcomes, cold-successor
               decisions vs earlier qualified performance.

True outcome labels can arrive weeks late. Fast/canary checks give immediate
warning while outcome evidence accumulates.
"""
from __future__ import annotations

from dataclasses import dataclass, field


# Severity ladder. Restoration requires REQUALIFICATION EVIDENCE under current
# conditions — an indicator clearing on its own never restores eligibility.
SEVERITY_LEVELS = ("stable", "watch", "requalify", "contain")

SEVERITY_RESPONSE = {
    "stable": (
        "Continue with the qualified calibration and normal monitoring."
    ),
    "watch": (
        "Increase independent sampling; investigate unexpected shifts; "
        "preserve authorized work."
    ),
    "requalify": (
        "Restrict use of the changed calibration where its validity is "
        "material; run benchmark replay and independent review."
    ),
    "contain": (
        "Block affected high-risk applications where integrity, authority, "
        "or safety-critical conditions are no longer established. "
        "Continue unaffected authorized work."
    ),
}


@dataclass(frozen=True)
class LoopSpec:
    name: str            # fast | medium | slow
    cadence: str         # e.g. "on-config-change", "hourly", "weekly"
    inputs: tuple        # what it observes
    outputs: tuple       # what it produces
    latency_note: str


MONITORING_LOOPS: tuple[LoopSpec, ...] = (
    LoopSpec(
        name="fast",
        cadence="on-config-change + pre-consequential-use",
        inputs=(
            "policy_version", "model_version", "prompt_version",
            "rubric_version", "schema_version", "environment_fingerprint",
        ),
        outputs=("fingerprint_mismatch_alert", "canary_replay_verdict"),
        latency_note="Immediate. Blocks consequential use until canaries replay.",
    ),
    LoopSpec(
        name="medium",
        cadence="hourly",
        inputs=(
            "challenge_case_mix", "label_missingness", "risk_score_distribution",
            "reopening_frequency", "restriction_rate", "reviewer_disagreement",
            "low_risk_audit_sample",
        ),
        outputs=("population_shift_report", "reviewer_drift_flag"),
        latency_note="Hours. Investigate, do not auto-restrict on population shift alone.",
    ),
    LoopSpec(
        name="slow",
        cadence="weekly",
        inputs=(
            "confirmed_defects", "missed_severe_cases", "unjustified_quarantines",
            "recovery_outcomes", "cold_successor_decisions",
        ),
        outputs=("calibration_error_report", "requalification_recommendation"),
        latency_note="Weeks. Outcome labels arrive late; never misclassify pending as success.",
    ),
)


@dataclass
class SeverityDecision:
    """A severity assignment with its evidence. Advisory — LAW still governs."""
    level: str
    reasons: tuple          # drift signals / indicators behind the level
    affected_scope: tuple   # domains / action classes affected
    restoration_requires: str = (
        "requires requalification evidence under current conditions; "
        "indicator clearing alone is insufficient"
    )

    def __post_init__(self):
        assert self.level in SEVERITY_LEVELS, f"unknown level {self.level}"

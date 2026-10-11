"""
harm_assessment.py — Law 11 v2: Uncertainty Handling.

Per Shawn's intel (2026-10-11): "When harm is known, protect. When harm is
possible, investigate. When harm is unequal, examine every affected party.
When harm is delayed, continue observing. When harm cannot be measured,
never pretend it is zero."

This module EXTENDS the v1 law11_gate (typed_action.py), it does not replace
it. The v1 hard gates run first. This module handles what v1 cannot: harm
under uncertainty.

ARCHITECTURE:
  v1 law11_gate(action): hard gates — prohibited ops, rights/safety/privacy
    violations, protected gates, unknown dimensions. Fail-closed.
  v2 assess_uncertain_harm(action, assessments): uncertainty handling —
    classifies harm per stakeholder group, enforces the 99%/1% rule,
    manages observation windows for delayed harm, distinguishes the
    six neutrality states.

  The v2 assessment runs AFTER v1 passes. It can only make the verdict
  MORE restrictive (ADMISSIBLE -> NEEDS_EVIDENCE / NEEDS_AUTHORITY),
  never less. A v1 PROHIBITED stays PROHIBITED.

KEY RULES (machine-enforced):
  1. 99%/1% RULE: majority benefit never erases minority harm. Each
     stakeholder group is checked independently.
  2. UNKNOWN IS NOT ZERO: unmeasured effects are UNMEASURED, not safe.
  3. NEUTRALITY TRAP: six distinct states, never collapsed.
  4. DELAYED HARM: observation windows with stop conditions; success
     stays provisional until the window completes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .typed_action import (
    TypedAction,
    Law11Verdict,
    ADMISSIBLE,
    NEEDS_EVIDENCE,
    NEEDS_AUTHORITY,
    PROHIBITED,
    law11_gate,
)


# ---------------------------------------------------------------------------
# Harm types — each requires different safeguards.
# ---------------------------------------------------------------------------
HARM_UNCERTAIN = "uncertain"              # mechanism unknown → investigate
HARM_ASYMMETRIC = "asymmetric"            # helps many, harms few → separate measurement
HARM_DELAYED = "delayed"                  # works now, breaks later → observation window
HARM_DIFFICULT = "difficult_to_measure"   # trust erosion, micro-harms → multiple indicators

HARM_TYPES = frozenset({
    HARM_UNCERTAIN, HARM_ASYMMETRIC, HARM_DELAYED, HARM_DIFFICULT,
})


# ---------------------------------------------------------------------------
# Neutrality states — six distinct machine states. NEVER collapsed.
# A study with wide uncertainty centered on zero does NOT establish
# harmlessness. UNKNOWN is not safe. UNMEASURED is not zero.
# ---------------------------------------------------------------------------
NEUTRAL_TRUE_ZERO = "TRUE_ZERO"                # actual zero effect established
NEUTRAL_PRACTICAL = "PRACTICALLY_NEUTRAL"      # within approved tolerance
NEUTRAL_UNKNOWN = "UNKNOWN"                    # effect not known
NEUTRAL_UNMEASURED = "UNMEASURED"              # not adequately measured
NEUTRAL_DELAYED = "DELAYED"                    # consequences outside observation period
NEUTRAL_INCONCLUSIVE = "INCONCLUSIVE"          # evidence can't support any conclusion

NEUTRALITY_STATES = frozenset({
    NEUTRAL_TRUE_ZERO, NEUTRAL_PRACTICAL, NEUTRAL_UNKNOWN,
    NEUTRAL_UNMEASURED, NEUTRAL_DELAYED, NEUTRAL_INCONCLUSIVE,
})

# Only these two states permit treating an effect as "no harm" for a
# specific dimension. All others require investigation or hold.
NEUTRALITY_SAFE_STATES = frozenset({NEUTRAL_TRUE_ZERO, NEUTRAL_PRACTICAL})


# ---------------------------------------------------------------------------
# Severity levels
# ---------------------------------------------------------------------------
SEVERITY_NEGLIGIBLE = "negligible"
SEVERITY_LOW = "low"
SEVERITY_MODERATE = "moderate"
SEVERITY_HIGH = "high"
SEVERITY_CRITICAL = "critical"

# Severity at or above this threshold triggers mandatory investigation
# regardless of likelihood — worst credible outcome matters.
SEVERITY_INVESTIGATION_THRESHOLD = SEVERITY_HIGH


# ---------------------------------------------------------------------------
# Structured harm assessment — per stakeholder, per harm type.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class HarmAssessment:
    """A structured harm assessment for one stakeholder group.

    Per the spec, for each potentially affected stakeholder and type of harm:
      - How severe could it be, including the worst credible outcome?
      - How likely is it, and how reliable is that estimate?
      - Can the harm be reversed or repaired?
      - How long might it take to appear?
      - Could repeated exposure accumulate into meaningful harm?
      - What can we actually detect, and what remains unmeasured?
      - What mitigation, consent, monitoring and stop mechanisms exist?

    None = unknown. Unknown is fail-closed: it triggers NEEDS_EVIDENCE,
    never ADMISSIBLE.
    """
    stakeholder_group: str          # e.g. "screen_reader_users"
    group_size: int = 0             # for the 99%/1% check (0 = unknown)
    harm_type: str = HARM_UNCERTAIN

    # The seven assessment dimensions.
    severity: str | None = None              # worst credible outcome
    likelihood: float | None = None          # 0.0-1.0, None = unknown
    likelihood_reliability: str | None = None  # high/medium/low/unknown
    reversibility: str | None = None         # reversible/conditional/irreversible
    time_to_appear: str | None = None        # immediate/days/weeks/months/unknown
    cumulative_risk: bool | None = None      # repeated exposure accumulates?
    detectability: str | None = None         # high/medium/low/unmeasurable

    # Safeguards.
    mitigation_available: bool = False
    consent_obtained: bool | None = None
    monitoring_ready: bool = False
    stop_conditions_defined: bool = False

    # Neutrality state for this assessment's measured effect.
    neutrality_state: str = NEUTRAL_UNKNOWN

    def is_fully_assessed(self) -> bool:
        """All seven dimensions have values (not None)."""
        return all([
            self.severity is not None,
            self.likelihood is not None,
            self.likelihood_reliability is not None,
            self.reversibility is not None,
            self.time_to_appear is not None,
            self.cumulative_risk is not None,
            self.detectability is not None,
        ])


# ---------------------------------------------------------------------------
# Observation windows — for delayed harm.
# ---------------------------------------------------------------------------
WINDOW_PENDING = "PENDING"        # observation in progress
WINDOW_COMPLETE = "COMPLETE"      # all checks passed, success confirmed
WINDOW_REOPENED = "REOPENED"      # contradictory evidence arrived
WINDOW_CONTAINED = "CONTAINED"    # stop threshold triggered

@dataclass
class ObservationWindow:
    """A delayed-harm observation window.

    Per the spec: observation windows and stop conditions BEFORE execution,
    not after problems. Success stays provisional until the window completes.
    If later evidence contradicts the success claim, the outcome reopens.
    """
    window_id: str
    action_ref: str
    stakeholder_group: str
    indicators: tuple[str, ...] = ()
    stop_triggers: tuple[str, ...] = ()
    review_dates: tuple[str, ...] = ()
    status: str = WINDOW_PENDING
    opened_at: str = ""
    closed_at: str | None = None
    findings: tuple[str, ...] = ()

    def __post_init__(self):
        if not self.opened_at:
            object.__setattr__(
                self, "opened_at",
                datetime.now(timezone.utc).isoformat()
            )

    def record_finding(self, finding: str, triggers_stop: bool = False) -> None:
        """Record an observation. If it triggers a stop condition, contain."""
        self.findings = self.findings + (finding,)
        if triggers_stop:
            self.status = WINDOW_CONTAINED

    def reopen(self, reason: str) -> None:
        """Contradictory evidence arrived — reopen, don't protect old scorecard."""
        self.findings = self.findings + (f"REOPENED: {reason}",)
        self.status = WINDOW_REOPENED

    def complete(self) -> None:
        """All checks passed. Only valid from PENDING."""
        if self.status == WINDOW_PENDING:
            self.status = WINDOW_COMPLETE
            self.closed_at = datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# The 99%/1% rule — per-group independent check.
# ---------------------------------------------------------------------------
def _group_harm_material(assessment: HarmAssessment) -> bool:
    """Is this group's harm material enough to block on its own?

    Per the spec: "Human worth is not proportional to group size."
    A small group with serious harm blocks regardless of how many
    others benefit.
    """
    if assessment.severity in (SEVERITY_HIGH, SEVERITY_CRITICAL):
        return True
    if assessment.severity == SEVERITY_MODERATE:
        # Moderate harm is material if irreversible or cumulative.
        if assessment.reversibility == "irreversible":
            return True
        if assessment.cumulative_risk is True:
            return True
    return False


def _needs_investigation(assessment: HarmAssessment) -> tuple[bool, str]:
    """Does this assessment require investigation before proceeding?

    Returns (needs_investigation, reason).
    """
    # Incomplete assessment → investigate.
    if not assessment.is_fully_assessed():
        return True, "INCOMPLETE_ASSESSMENT"

    # Uncertain harm type with unknown mechanism → investigate.
    if assessment.harm_type == HARM_UNCERTAIN:
        if assessment.likelihood_reliability in (None, "low", "unknown"):
            return True, "UNCERTAIN_MECHANISM"

    # High/critical severity with incomplete assessment → investigate first.
    # But if the assessment is complete and the risk is well-characterized,
    # that's NEEDS_AUTHORITY (human judgment), not NEEDS_EVIDENCE.
    # The distinction: missing evidence vs. consequential judgment call.
    if assessment.severity in (SEVERITY_HIGH, SEVERITY_CRITICAL):
        if not assessment.is_fully_assessed():
            return True, "SEVERITY_INVESTIGATION_REQUIRED"
        if assessment.likelihood_reliability in (None, "low", "unknown"):
            return True, "SEVERITY_UNRELIABLE_ESTIMATE"
        # Complete, reliable assessment of high severity → human decides.
        # Do NOT return True here; let the NEEDS_AUTHORITY check handle it.

    # Difficult to measure → need multiple indicators.
    if assessment.harm_type == HARM_DIFFICULT:
        if assessment.detectability in ("low", "unmeasurable", None):
            return True, "UNMEASURABLE_HARM"

    # Neutrality trap: only TRUE_ZERO and PRACTICALLY_NEUTRAL are safe.
    if assessment.neutrality_state not in NEUTRALITY_SAFE_STATES:
        return True, f"NEUTRALITY_{assessment.neutrality_state}"

    return False, ""


# ---------------------------------------------------------------------------
# Main entry point: classify uncertain harm.
# ---------------------------------------------------------------------------
def assess_uncertain_harm(
    action: TypedAction,
    assessments: tuple[HarmAssessment, ...] = (),
    observation_windows: tuple[ObservationWindow, ...] = (),
) -> Law11Verdict:
    """Law 11 v2: assess harm under uncertainty.

    Runs AFTER the v1 hard gate. Can only make the verdict MORE
    restrictive, never less.

    Classification per the spec:
      Known violation → PROHIBITED (handled by v1, preserved here)
      Critical evidence missing → NEEDS_EVIDENCE
      Consequential but potentially permissible → NEEDS_AUTHORITY
      Bounded risk with protections and authority → ADMISSIBLE

    Args:
        action: the TypedAction being assessed.
        assessments: per-stakeholder harm assessments.
        observation_windows: active observation windows for delayed harm.

    Returns:
        Law11Verdict with v2 reasoning appended.
    """
    policy = action.policy_version

    # Step 1: v1 hard gate first. PROHIBITED is final.
    v1_verdict = law11_gate(action)
    if v1_verdict.verdict == PROHIBITED:
        return v1_verdict

    reasons: list[str] = list(v1_verdict.reasons)
    interests: list[str] = list(v1_verdict.affected_interests)

    # If v1 already requires evidence or authority, v2 doesn't override —
    # but it appends uncertainty findings for the record.
    v1_verdict_value = v1_verdict.verdict

    # Step 2: 99%/1% rule — check EACH group independently.
    # No group is expendable. No serious harm disappears inside an average.
    for assessment in assessments:
        needs_inv, inv_reason = _needs_investigation(assessment)

        # Asymmetric harm: this group harmed while others benefit.
        # The majority's benefit NEVER erases this group's harm.
        if assessment.harm_type == HARM_ASYMMETRIC:
            if _group_harm_material(assessment):
                return Law11Verdict(
                    verdict=NEEDS_EVIDENCE,
                    reasons=tuple(reasons + [
                        f"ASYMMETRIC_HARM:{assessment.stakeholder_group}",
                        f"SEVERITY:{assessment.severity}",
                    ]),
                    affected_interests=tuple(interests + [assessment.stakeholder_group]),
                    policy_version=policy,
                )

        # Any group needing investigation blocks with NEEDS_EVIDENCE.
        if needs_inv:
            return Law11Verdict(
                verdict=NEEDS_EVIDENCE,
                reasons=tuple(reasons + [
                    f"V2_{inv_reason}:{assessment.stakeholder_group}",
                ]),
                affected_interests=tuple(interests + [assessment.stakeholder_group]),
                policy_version=policy,
            )

        # Delayed harm: check observation windows.
        if assessment.harm_type == HARM_DELAYED:
            window = _find_window(observation_windows, assessment.stakeholder_group)
            if window is None:
                # No observation window defined for delayed harm → need evidence.
                return Law11Verdict(
                    verdict=NEEDS_EVIDENCE,
                    reasons=tuple(reasons + [
                        f"DELAYED_HARM_NO_WINDOW:{assessment.stakeholder_group}",
                    ]),
                    affected_interests=tuple(interests + [assessment.stakeholder_group]),
                    policy_version=policy,
                )
            if window.status == WINDOW_REOPENED:
                return Law11Verdict(
                    verdict=NEEDS_EVIDENCE,
                    reasons=tuple(reasons + [
                        f"DELAYED_HARM_REOPENED:{assessment.stakeholder_group}",
                    ]),
                    affected_interests=tuple(interests + [assessment.stakeholder_group]),
                    policy_version=policy,
                )
            if window.status == WINDOW_CONTAINED:
                return Law11Verdict(
                    verdict=PROHIBITED,
                    reasons=tuple(reasons + [
                        f"DELAYED_HARM_STOP_TRIGGERED:{assessment.stakeholder_group}",
                    ]),
                    affected_interests=tuple(interests + [assessment.stakeholder_group]),
                    policy_version=policy,
                )
            if window.status == WINDOW_PENDING:
                # Success is provisional until the window completes.
                # This doesn't block, but it's recorded.
                reasons.append(f"PROVISIONAL_WINDOW:{assessment.stakeholder_group}")

    # Step 3: Consequential risk needing human judgment → NEEDS_AUTHORITY.
    # If any assessment has high/critical severity with mitigation but
    # the action is otherwise admissible, it needs human authority.
    for assessment in assessments:
        if assessment.severity in (SEVERITY_HIGH, SEVERITY_CRITICAL):
            if assessment.mitigation_available and assessment.monitoring_ready:
                # Mitigated but consequential → human decides.
                return Law11Verdict(
                    verdict=NEEDS_AUTHORITY,
                    reasons=tuple(reasons + [
                        f"CONSEQUENTIAL_RISK:{assessment.stakeholder_group}",
                        f"SEVERITY:{assessment.severity}",
                    ]),
                    affected_interests=tuple(interests + [assessment.stakeholder_group]),
                    policy_version=policy,
                )

    # Step 4: Preserve v1's NEEDS_EVIDENCE / NEEDS_AUTHORITY.
    if v1_verdict_value in (NEEDS_EVIDENCE, NEEDS_AUTHORITY):
        return Law11Verdict(
            verdict=v1_verdict_value,
            reasons=tuple(reasons),
            affected_interests=tuple(interests),
            policy_version=policy,
        )

    # Step 5: All uncertainty handled → ADMISSIBLE.
    return Law11Verdict(
        verdict=ADMISSIBLE,
        reasons=tuple(reasons),
        affected_interests=tuple(interests),
        policy_version=policy,
    )


def _find_window(
    windows: tuple[ObservationWindow, ...],
    stakeholder_group: str,
) -> ObservationWindow | None:
    """Find the observation window for a stakeholder group."""
    for w in windows:
        if w.stakeholder_group == stakeholder_group:
            return w
    return None


# ---------------------------------------------------------------------------
# Audit receipt — what the spec requires recorded.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class HarmAuditReceipt:
    """Per the spec, each consequential harm assessment records:
    law and risk-policy versions, affected stakeholders, harm categories,
    assumptions, evidence quality, plausible worst outcomes, uncertainty,
    cumulative exposure, time horizon, authority and consent, mitigation,
    monitoring, stop conditions, actual consequences, independent verification.
    """
    action_ref: str
    law_version: str = "LAW11_V2"
    policy_version: str = "CURRENT"
    stakeholders: tuple[str, ...] = ()
    harm_categories: tuple[str, ...] = ()
    worst_outcomes: tuple[str, ...] = ()
    uncertainty_notes: tuple[str, ...] = ()
    authority_ref: str | None = None
    consent_refs: tuple[str, ...] = ()
    mitigation: tuple[str, ...] = ()
    monitoring: tuple[str, ...] = ()
    stop_conditions: tuple[str, ...] = ()
    verdict: str = ADMISSIBLE
    assessed_at: str = ""

    def __post_init__(self):
        if not self.assessed_at:
            object.__setattr__(
                self, "assessed_at",
                datetime.now(timezone.utc).isoformat()
            )


def build_audit_receipt(
    action: TypedAction,
    assessments: tuple[HarmAssessment, ...],
    verdict: Law11Verdict,
) -> HarmAuditReceipt:
    """Build the audit receipt from an assessment run."""
    return HarmAuditReceipt(
        action_ref=f"{action.actor_id}:{action.operation}:{action.resource}",
        policy_version=action.policy_version,
        stakeholders=tuple(a.stakeholder_group for a in assessments),
        harm_categories=tuple(sorted({a.harm_type for a in assessments})),
        worst_outcomes=tuple(
            f"{a.stakeholder_group}:{a.severity}" for a in assessments
            if a.severity in (SEVERITY_HIGH, SEVERITY_CRITICAL)
        ),
        uncertainty_notes=tuple(
            f"{a.stakeholder_group}:{a.neutrality_state}" for a in assessments
            if a.neutrality_state not in NEUTRALITY_SAFE_STATES
        ),
        authority_ref=action.authority_ref,
        verdict=verdict.verdict,
    )

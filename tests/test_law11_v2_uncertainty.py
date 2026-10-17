"""
test_law11_v2_uncertainty.py — Tests for Law 11 v2: Uncertainty Handling.

Per Shawn's intel (2026-10-11): "When harm is known, protect. When harm is
possible, investigate. When harm is unequal, examine every affected party.
When harm is delayed, continue observing. When harm cannot be measured,
never pretend it is zero."

These tests prove:
1. Harm classification: PROHIBITED / NEEDS_EVIDENCE / NEEDS_AUTHORITY / ADMISSIBLE
2. Four harm types get different safeguards
3. 99%/1% rule: minority harm blocks despite majority benefit
4. Structured assessment: incomplete → NEEDS_EVIDENCE
5. Neutrality trap: six states, only two are safe
6. Delayed harm: observation windows, provisional success, reopen on contradiction
"""
import pytest

from datetime import datetime, timedelta, timezone

from kernel.protocol.typed_action import (
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    TypedAction,
)
from kernel.protocol.harm_assessment import (
    # Harm types
    HARM_UNCERTAIN,
    HARM_ASYMMETRIC,
    HARM_DELAYED,
    HARM_DIFFICULT,
    # Neutrality states
    NEUTRAL_TRUE_ZERO,
    NEUTRAL_PRACTICAL,
    NEUTRAL_UNKNOWN,
    NEUTRAL_UNMEASURED,
    NEUTRAL_DELAYED,
    NEUTRAL_INCONCLUSIVE,
    NEUTRALITY_SAFE_STATES,
    # Severity
    SEVERITY_LOW,
    SEVERITY_MODERATE,
    SEVERITY_HIGH,
    SEVERITY_CRITICAL,
    # Core
    HarmAssessment,
    ObservationWindow,
    HarmAuditReceipt,
    WINDOW_PENDING,
    WINDOW_COMPLETE,
    WINDOW_REOPENED,
    WINDOW_CONTAINED,
    assess_uncertain_harm,
    build_audit_receipt,
)


def _safe_action(**overrides):
    """Baseline: passes v1 gate (all dimensions safe)."""
    base = dict(
        actor_id="naya-5",
        operation="write",
        environment="development",
        resource="kernel/test_module",
        rights_safe=True,
        safety_safe=True,
        privacy_safe=True,
        consent_obtained=True,
    )
    base.update(overrides)
    return TypedAction(**base)


def _full_assessment(**overrides):
    """Baseline: fully assessed, low severity, safe neutrality."""
    base = dict(
        stakeholder_group="test_group",
        group_size=100,
        harm_type=HARM_UNCERTAIN,
        severity=SEVERITY_LOW,
        likelihood=0.1,
        likelihood_reliability="high",
        reversibility="reversible",
        time_to_appear="immediate",
        cumulative_risk=False,
        detectability="high",
        mitigation_available=True,
        consent_obtained=True,
        monitoring_ready=True,
        stop_conditions_defined=True,
        neutrality_state=NEUTRAL_TRUE_ZERO,
    )
    base.update(overrides)
    return HarmAssessment(**base)


# ---------------------------------------------------------------------------
# 1. Harm classification
# ---------------------------------------------------------------------------

class TestHarmClassification:
    def test_v1_prohibited_stays_prohibited(self):
        """v2 never softens a v1 PROHIBITED."""
        action = _safe_action(operation="harm")  # inherently prohibited
        assessment = _full_assessment()
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == PROHIBITED

    def test_fully_assessed_safe_action_admissible(self):
        """Complete safe assessment → ADMISSIBLE."""
        action = _safe_action()
        assessment = _full_assessment()
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == ADMISSIBLE

    def test_no_assessments_v1_admissible_stays(self):
        """No uncertainty data → v1 verdict preserved."""
        action = _safe_action()
        verdict = assess_uncertain_harm(action, ())
        assert verdict.verdict == ADMISSIBLE

    def test_v1_needs_evidence_preserved(self):
        """v1 NEEDS_EVIDENCE is not overridden by v2."""
        action = _safe_action(rights_safe=None)  # unknown → v1 NEEDS_EVIDENCE
        verdict = assess_uncertain_harm(action, ())
        assert verdict.verdict == NEEDS_EVIDENCE


# ---------------------------------------------------------------------------
# 2. Four harm types — different safeguards
# ---------------------------------------------------------------------------

class TestHarmTypes:
    def test_uncertain_harm_low_reliability_needs_evidence(self):
        """Uncertain mechanism + unreliable estimate → investigate."""
        action = _safe_action()
        assessment = _full_assessment(
            harm_type=HARM_UNCERTAIN,
            likelihood_reliability="low",
            neutrality_state=NEUTRAL_UNKNOWN,
        )
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE
        assert any("UNCERTAIN_MECHANISM" in r for r in verdict.reasons)

    def test_difficult_harm_unmeasurable_needs_evidence(self):
        """Difficult-to-measure + low detectability → investigate."""
        action = _safe_action()
        assessment = _full_assessment(
            harm_type=HARM_DIFFICULT,
            detectability="unmeasurable",
            neutrality_state=NEUTRAL_UNMEASURED,
        )
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE

    def test_delayed_harm_no_window_needs_evidence(self):
        """Delayed harm without observation window → NEEDS_EVIDENCE."""
        action = _safe_action()
        assessment = _full_assessment(
            harm_type=HARM_DELAYED,
            time_to_appear="months",
            neutrality_state=NEUTRAL_PRACTICAL,  # safe neutrality → reaches window check
        )
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE
        assert any("DELAYED_HARM_NO_WINDOW" in r for r in verdict.reasons)

    def test_delayed_harm_with_pending_window_provisional(self):
        """Delayed harm with active window → ADMISSIBLE but provisional."""
        action = _safe_action()
        assessment = _full_assessment(
            harm_type=HARM_DELAYED,
            time_to_appear="months",
            neutrality_state=NEUTRAL_PRACTICAL,
        )
        window = ObservationWindow(
            window_id="w1",
            action_ref="test",
            stakeholder_group="test_group",
            indicators=("error_rate",),
            stop_triggers=("error_rate > 5%",),
        )
        verdict = assess_uncertain_harm(action, (assessment,), (window,))
        assert verdict.verdict == ADMISSIBLE
        assert any("PROVISIONAL_WINDOW" in r for r in verdict.reasons)


# ---------------------------------------------------------------------------
# 3. 99%/1% rule — minority harm blocks
# ---------------------------------------------------------------------------

class TestNinetyNineOneRule:
    def test_small_group_serious_harm_blocks(self):
        """1% harmed seriously → blocked despite 99% benefit."""
        action = _safe_action()
        # Majority: fine
        majority = _full_assessment(
            stakeholder_group="majority_users",
            group_size=9900,
        )
        # Minority: serious asymmetric harm
        minority = _full_assessment(
            stakeholder_group="screen_reader_users",
            group_size=100,  # the 1%
            harm_type=HARM_ASYMMETRIC,
            severity=SEVERITY_HIGH,
            neutrality_state=NEUTRAL_PRACTICAL,
        )
        verdict = assess_uncertain_harm(action, (majority, minority))
        assert verdict.verdict == NEEDS_EVIDENCE
        assert any("ASYMMETRIC_HARM:screen_reader_users" in r
                   for r in verdict.reasons)
        # The minority group is named in affected interests.
        assert "screen_reader_users" in verdict.affected_interests

    def test_majority_benefit_never_erases_minority_harm(self):
        """Even with huge majority, minority harm is checked independently."""
        action = _safe_action()
        assessments = tuple(
            _full_assessment(stakeholder_group=f"group_{i}", group_size=10000)
            for i in range(10)  # 100k happy users
        ) + (
            _full_assessment(
                stakeholder_group="tiny_vulnerable_group",
                group_size=5,  # 5 people
                harm_type=HARM_ASYMMETRIC,
                severity=SEVERITY_CRITICAL,
                neutrality_state=NEUTRAL_PRACTICAL,
            ),
        )
        verdict = assess_uncertain_harm(action, assessments)
        assert verdict.verdict == NEEDS_EVIDENCE

    def test_moderate_irreversible_harm_material(self):
        """Moderate + irreversible = material, blocks."""
        action = _safe_action()
        assessment = _full_assessment(
            harm_type=HARM_ASYMMETRIC,
            severity=SEVERITY_MODERATE,
            reversibility="irreversible",
            neutrality_state=NEUTRAL_PRACTICAL,
        )
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE


# ---------------------------------------------------------------------------
# 4. Structured assessment — incomplete → NEEDS_EVIDENCE
# ---------------------------------------------------------------------------

class TestStructuredAssessment:
    def test_incomplete_assessment_needs_evidence(self):
        """Missing dimensions → investigate, don't assume safe."""
        action = _safe_action()
        assessment = HarmAssessment(
            stakeholder_group="test_group",
            severity=SEVERITY_LOW,
            # everything else None → incomplete
        )
        assert not assessment.is_fully_assessed()
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE
        assert any("INCOMPLETE_ASSESSMENT" in r for r in verdict.reasons)

    def test_high_severity_incomplete_needs_evidence(self):
        """High severity + incomplete assessment → investigate first."""
        action = _safe_action()
        assessment = HarmAssessment(
            stakeholder_group="test_group",
            severity=SEVERITY_HIGH,
            # incomplete → investigate
        )
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE

    def test_high_severity_complete_reliable_needs_authority(self):
        """High severity, fully assessed, reliable → human judgment."""
        action = _safe_action()
        assessment = _full_assessment(
            severity=SEVERITY_HIGH,
            likelihood_reliability="high",
            mitigation_available=True,
            monitoring_ready=True,
            neutrality_state=NEUTRAL_TRUE_ZERO,
        )
        assert assessment.is_fully_assessed()
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_AUTHORITY
        assert any("CONSEQUENTIAL_RISK" in r for r in verdict.reasons)

    def test_high_severity_unreliable_estimate_needs_evidence(self):
        """High severity + unreliable estimate → investigate, don't ask human yet."""
        action = _safe_action()
        assessment = _full_assessment(
            severity=SEVERITY_HIGH,
            likelihood_reliability="low",
            neutrality_state=NEUTRAL_TRUE_ZERO,
        )
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE

    def test_consequential_mitigated_needs_authority(self):
        """High severity + complete + reliable + mitigated → human decides."""
        action = _safe_action()
        assessment = _full_assessment(
            severity=SEVERITY_HIGH,
            likelihood_reliability="high",
            mitigation_available=True,
            monitoring_ready=True,
            neutrality_state=NEUTRAL_PRACTICAL,
        )
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_AUTHORITY
        assert any("CONSEQUENTIAL_RISK" in r for r in verdict.reasons)

    def test_high_severity_unmitigated_needs_authority(self):
        """High severity + complete + reliable + NO mitigation → human decides.

        Safety regression test (validator finding 2026-10-11): this case
        previously fell through to ADMISSIBLE. It must NEVER be admissible.
        """
        action = _safe_action()
        assessment = _full_assessment(
            severity=SEVERITY_HIGH,
            likelihood_reliability="high",
            mitigation_available=False,
            monitoring_ready=False,
            neutrality_state=NEUTRAL_TRUE_ZERO,
        )
        assert assessment.is_fully_assessed()
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_AUTHORITY
        assert any("CONSEQUENTIAL_RISK_UNMITIGATED" in r for r in verdict.reasons)

    def test_critical_severity_unmitigated_needs_authority(self):
        """Critical severity + NO mitigation → human decides, never ADMISSIBLE."""
        action = _safe_action()
        assessment = _full_assessment(
            severity=SEVERITY_CRITICAL,
            likelihood_reliability="high",
            mitigation_available=False,
            monitoring_ready=False,
            neutrality_state=NEUTRAL_TRUE_ZERO,
        )
        assert assessment.is_fully_assessed()
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_AUTHORITY
        assert any("CONSEQUENTIAL_RISK_UNMITIGATED" in r for r in verdict.reasons)

    def test_high_severity_partial_safeguards_still_needs_authority(self):
        """High severity with only ONE of mitigation/monitoring → still blocked.

        Either safeguard missing is enough to require human judgment.
        """
        action = _safe_action()
        for mitigation, monitoring in [(True, False), (False, True)]:
            assessment = _full_assessment(
                severity=SEVERITY_HIGH,
                likelihood_reliability="high",
                mitigation_available=mitigation,
                monitoring_ready=monitoring,
                neutrality_state=NEUTRAL_TRUE_ZERO,
            )
            verdict = assess_uncertain_harm(action, (assessment,))
            assert verdict.verdict == NEEDS_AUTHORITY, (
                f"mitigation={mitigation}, monitoring={monitoring}"
            )


class TestSeverityValidation:
    """Non-canonical severity must fail closed — never ADMISSIBLE.

    Regression tests (validator finding 2026-10-11, re-validation 8.0/10
    CONDITIONAL): severity comparisons are exact-match. A malformed value
    ("HIGH", " critical", "severe") previously missed every comparison and
    fell through to ADMISSIBLE — fail-open on the only hard law.
    Non-canonical severity is treated as unknown → NEEDS_EVIDENCE.
    Same pattern as garbage neutrality_state.
    """

    @pytest.mark.parametrize("bad_severity", [
        "HIGH",          # wrong case
        "High",          # title case
        "CRITICAL ",     # trailing whitespace
        " critical",     # leading whitespace
        "severe",        # plausible synonym, not canonical
        "CRIT",          # abbreviation
        "",              # empty string
        "unknown",       # not a canonical level
        "none",          # not a canonical level
    ])
    def test_non_canonical_severity_needs_evidence(self, bad_severity):
        """Malformed severity + otherwise clean assessment → NEEDS_EVIDENCE."""
        action = _safe_action()
        assessment = _full_assessment(
            severity=bad_severity,
            neutrality_state=NEUTRAL_TRUE_ZERO,
        )
        assert assessment.is_fully_assessed()  # not None → counts as "assessed"
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE, (
            f"severity={bad_severity!r} must never be ADMISSIBLE"
        )
        assert any("SEVERITY_NON_CANONICAL" in r for r in verdict.reasons)

    def test_non_canonical_severity_asymmetric_blocks(self):
        """Malformed severity on an asymmetric harm → blocked, not averaged away."""
        action = _safe_action()
        assessment = _full_assessment(
            harm_type=HARM_ASYMMETRIC,
            severity="severe",
            neutrality_state=NEUTRAL_TRUE_ZERO,
        )
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE
        assert verdict.verdict != ADMISSIBLE

    def test_non_canonical_severity_never_admissible_across_harm_types(self):
        """Every harm type with garbage severity → never ADMISSIBLE."""
        action = _safe_action()
        for harm_type in [HARM_UNCERTAIN, HARM_ASYMMETRIC, HARM_DELAYED, HARM_DIFFICULT]:
            kwargs = dict(severity="HIGH", neutrality_state=NEUTRAL_TRUE_ZERO)
            if harm_type == HARM_DELAYED:
                # Delayed harm needs a window to avoid the no-window path;
                # the severity failure must fire first regardless.
                window = ObservationWindow(
                    window_id="w1",
                    action_ref="naya-5:write:kernel/test_module",
                    stakeholder_group="test_group",
                    status=WINDOW_COMPLETE,
                )
                verdict = assess_uncertain_harm(
                    action,
                    (_full_assessment(harm_type=harm_type, **kwargs),),
                    (window,),
                )
            else:
                verdict = assess_uncertain_harm(
                    action,
                    (_full_assessment(harm_type=harm_type, **kwargs),),
                )
            assert verdict.verdict == NEEDS_EVIDENCE, (
                f"harm_type={harm_type}: garbage severity must never be ADMISSIBLE"
            )

    def test_canonical_severities_unaffected(self):
        """All five canonical severities still behave exactly as before."""
        action = _safe_action()
        # low → fully assessed, safe neutrality → ADMISSIBLE
        verdict = assess_uncertain_harm(
            action, (_full_assessment(severity=SEVERITY_LOW),))
        assert verdict.verdict == ADMISSIBLE
        # moderate (reversible, non-cumulative) → ADMISSIBLE
        verdict = assess_uncertain_harm(
            action, (_full_assessment(severity=SEVERITY_MODERATE),))
        assert verdict.verdict == ADMISSIBLE
        # high → NEEDS_AUTHORITY (unmitigated variant per safety fix)
        verdict = assess_uncertain_harm(
            action, (_full_assessment(
                severity=SEVERITY_HIGH,
                likelihood_reliability="high",
                mitigation_available=False,
                monitoring_ready=False,
            ),))
        assert verdict.verdict == NEEDS_AUTHORITY

    def test_non_canonical_severity_flagged_in_audit_receipt(self):
        """The audit receipt records the malformed severity for the record."""
        action = _safe_action()
        assessment = _full_assessment(
            severity="severe",
            neutrality_state=NEUTRAL_TRUE_ZERO,
        )
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE
        receipt = build_audit_receipt(action, (assessment,), verdict)
        assert any("SEVERITY_NON_CANONICAL" in n for n in receipt.uncertainty_notes)
        assert receipt.verdict == NEEDS_EVIDENCE


# ---------------------------------------------------------------------------
# 5. Neutrality trap — six states, only two safe
# ---------------------------------------------------------------------------

class TestNeutralityTrap:
    @pytest.mark.parametrize("state", [
        NEUTRAL_UNKNOWN,
        NEUTRAL_UNMEASURED,
        NEUTRAL_DELAYED,
        NEUTRAL_INCONCLUSIVE,
    ])
    def test_unsafe_neutrality_states_block(self, state):
        """UNKNOWN/UNMEASURED/DELAYED/INCONCLUSIVE → NEEDS_EVIDENCE."""
        action = _safe_action()
        assessment = _full_assessment(neutrality_state=state)
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE
        assert any(f"NEUTRALITY_{state}" in r for r in verdict.reasons)

    @pytest.mark.parametrize("state", [
        NEUTRAL_TRUE_ZERO,
        NEUTRAL_PRACTICAL,
    ])
    def test_safe_neutrality_states_pass(self, state):
        """TRUE_ZERO/PRACTICALLY_NEUTRAL → can be ADMISSIBLE."""
        action = _safe_action()
        assessment = _full_assessment(neutrality_state=state)
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == ADMISSIBLE

    def test_wide_interval_centered_on_zero_not_harmless(self):
        """The neutrality trap: uncertain ≠ safe."""
        action = _safe_action()
        assessment = _full_assessment(
            neutrality_state=NEUTRAL_INCONCLUSIVE,
            likelihood_reliability="low",
        )
        verdict = assess_uncertain_harm(action, (assessment,))
        # Must NOT be ADMISSIBLE — inconclusive is not harmless.
        assert verdict.verdict != ADMISSIBLE

    def test_safe_states_constant(self):
        """Only TRUE_ZERO and PRACTICALLY_NEUTRAL are safe."""
        assert NEUTRALITY_SAFE_STATES == frozenset({
            NEUTRAL_TRUE_ZERO, NEUTRAL_PRACTICAL,
        })


# ---------------------------------------------------------------------------
# 6. Delayed harm — observation windows
# ---------------------------------------------------------------------------

class TestDelayedHarm:
    def test_reopened_window_needs_evidence(self):
        """Contradictory evidence → reopen, don't protect old scorecard."""
        action = _safe_action()
        assessment = _full_assessment(
            harm_type=HARM_DELAYED,
            time_to_appear="months",
            neutrality_state=NEUTRAL_PRACTICAL,
        )
        window = ObservationWindow(
            window_id="w1",
            action_ref="test",
            stakeholder_group="test_group",
        )
        window.reopen("error rate spiked in month 3")
        assert window.status == WINDOW_REOPENED
        verdict = assess_uncertain_harm(action, (assessment,), (window,))
        assert verdict.verdict == NEEDS_EVIDENCE
        assert any("DELAYED_HARM_REOPENED" in r for r in verdict.reasons)

    def test_stop_trigger_prohibited(self):
        """Stop threshold triggered → PROHIBITED."""
        action = _safe_action()
        assessment = _full_assessment(
            harm_type=HARM_DELAYED,
            time_to_appear="months",
            neutrality_state=NEUTRAL_PRACTICAL,
        )
        window = ObservationWindow(
            window_id="w1",
            action_ref="test",
            stakeholder_group="test_group",
            stop_triggers=("harm_detected",),
        )
        window.record_finding("harm detected in cohort", triggers_stop=True)
        assert window.status == WINDOW_CONTAINED
        verdict = assess_uncertain_harm(action, (assessment,), (window,))
        assert verdict.verdict == PROHIBITED

    def test_complete_window_allows_admissible(self):
        """Completed window → success confirmed, can proceed."""
        action = _safe_action()
        assessment = _full_assessment(
            harm_type=HARM_DELAYED,
            time_to_appear="weeks",
            neutrality_state=NEUTRAL_PRACTICAL,
        )
        window = ObservationWindow(
            window_id="w1",
            action_ref="test",
            stakeholder_group="test_group",
        )
        window.complete()
        assert window.status == WINDOW_COMPLETE
        verdict = assess_uncertain_harm(action, (assessment,), (window,))
        assert verdict.verdict == ADMISSIBLE
        # No provisional flag once complete.
        assert not any("PROVISIONAL_WINDOW" in r for r in verdict.reasons)

    def test_monitoring_failure_pauses(self):
        """No window for delayed harm → must establish monitoring first."""
        action = _safe_action()
        assessment = _full_assessment(
            harm_type=HARM_DELAYED,
            monitoring_ready=False,
            neutrality_state=NEUTRAL_DELAYED,
        )
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE


# ---------------------------------------------------------------------------
# 6b. Monitoring-aware door (T-07-VERIFY)
#
# A PENDING observation window whose review is overdue with zero recorded
# findings is a lapsed monitor — the gate must refuse on the window's own
# evidence, without depending on an external review() loop having run.
# ---------------------------------------------------------------------------

class TestMonitoringAwareDoor:
    def _delayed(self, **kw):
        base = dict(
            harm_type=HARM_DELAYED,
            time_to_appear="months",
            neutrality_state=NEUTRAL_PRACTICAL,  # safe → reaches window check
        )
        base.update(kw)
        return _full_assessment(**base)

    def _window(self, group="test_group", review_dates=(), findings=()):
        w = ObservationWindow(
            window_id="w-door",
            action_ref="door-test",
            stakeholder_group=group,
            indicators=("error_rate",),
            stop_triggers=("error_rate > 5%",),
            review_dates=review_dates,
        )
        for f in findings:
            w.record_finding(f)
        return w

    def _past(self, **kw):
        return (datetime.now(timezone.utc) - timedelta(**kw)).isoformat()

    def _future(self, **kw):
        return (datetime.now(timezone.utc) + timedelta(**kw)).isoformat()

    def test_overdue_review_no_findings_blocks(self):
        """REGRESSION (T-07-VERIFY): review 1h overdue + zero findings → refuse."""
        action = _safe_action()
        window = self._window(review_dates=(self._past(hours=1),))
        verdict = assess_uncertain_harm(action, (self._delayed(),), (window,))
        assert verdict.verdict == NEEDS_EVIDENCE
        assert any("OVERDUE_REVIEW_NO_FINDINGS:test_group" in r
                   for r in verdict.reasons)
        assert "test_group" in verdict.affected_interests

    def test_overdue_review_with_findings_proceeds_provisional(self):
        """Monitoring is happening (findings recorded) → provisional, not blocked."""
        action = _safe_action()
        window = self._window(
            review_dates=(self._past(hours=1),),
            findings=("error_rate nominal at review",),
        )
        verdict = assess_uncertain_harm(action, (self._delayed(),), (window,))
        assert verdict.verdict == ADMISSIBLE
        assert any("PROVISIONAL_WINDOW" in r for r in verdict.reasons)

    def test_future_review_no_findings_proceeds_provisional(self):
        """Review not yet due → provisional, not blocked."""
        action = _safe_action()
        window = self._window(review_dates=(self._future(days=7),))
        verdict = assess_uncertain_harm(action, (self._delayed(),), (window,))
        assert verdict.verdict == ADMISSIBLE
        assert any("PROVISIONAL_WINDOW" in r for r in verdict.reasons)

    def test_unreadable_review_date_fails_closed(self):
        """A review schedule that cannot be read cannot be proven on track."""
        action = _safe_action()
        window = self._window(review_dates=("not-a-date",))
        verdict = assess_uncertain_harm(action, (self._delayed(),), (window,))
        assert verdict.verdict == NEEDS_EVIDENCE
        assert any("REVIEW_DATE_UNREADABLE:test_group" in r
                   for r in verdict.reasons)

    def test_naive_review_date_assumed_utc(self):
        """Naive datetimes are read as UTC (the module's write convention)."""
        action = _safe_action()
        naive_past = (datetime.now(timezone.utc)
                      - timedelta(hours=1)).replace(tzinfo=None).isoformat()
        window = self._window(review_dates=(naive_past,))
        verdict = assess_uncertain_harm(action, (self._delayed(),), (window,))
        assert verdict.verdict == NEEDS_EVIDENCE
        assert any("OVERDUE_REVIEW_NO_FINDINGS" in r for r in verdict.reasons)

    def test_no_review_dates_unchanged(self):
        """No review dates → existing provisional behavior preserved."""
        action = _safe_action()
        window = self._window()
        verdict = assess_uncertain_harm(action, (self._delayed(),), (window,))
        assert verdict.verdict == ADMISSIBLE
        assert any("PROVISIONAL_WINDOW" in r for r in verdict.reasons)


# ---------------------------------------------------------------------------
# 7. Audit receipts
# ---------------------------------------------------------------------------

class TestAuditReceipts:
    def test_receipt_captures_required_fields(self):
        """Receipt records stakeholders, categories, verdict."""
        action = _safe_action()
        assessments = (
            _full_assessment(stakeholder_group="group_a"),
            _full_assessment(
                stakeholder_group="group_b",
                harm_type=HARM_ASYMMETRIC,
                severity=SEVERITY_HIGH,
            ),
        )
        verdict = assess_uncertain_harm(action, assessments)
        receipt = build_audit_receipt(action, assessments, verdict)
        assert isinstance(receipt, HarmAuditReceipt)
        assert "group_a" in receipt.stakeholders
        assert "group_b" in receipt.stakeholders
        assert HARM_ASYMMETRIC in receipt.harm_categories
        assert receipt.verdict == verdict.verdict
        assert receipt.law_version == "LAW11_V2"
        # High severity worst outcome recorded.
        assert any("group_b" in w for w in receipt.worst_outcomes)

    def test_receipt_has_timestamp(self):
        """Receipt is timestamped."""
        action = _safe_action()
        verdict = assess_uncertain_harm(action, ())
        receipt = build_audit_receipt(action, (), verdict)
        assert receipt.assessed_at != ""


# ---------------------------------------------------------------------------
# 8. Integration: v2 never weakens v1
# ---------------------------------------------------------------------------

class TestV2NeverWeakensV1:
    def test_v2_cannot_make_prohibited_admissible(self):
        """v2 is monotonic: only more restrictive, never less."""
        # v1 PROHIBITED + perfect v2 assessment → still PROHIBITED.
        action = _safe_action(rights_safe=False)
        assessment = _full_assessment(neutrality_state=NEUTRAL_TRUE_ZERO)
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == PROHIBITED

    def test_v2_preserves_v1_needs_authority(self):
        """v1 NEEDS_AUTHORITY preserved through v2."""
        action = _safe_action(
            operation="deploy",
            environment="production",
            authority_ref=None,  # no authority → v1 NEEDS_AUTHORITY
        )
        verdict = assess_uncertain_harm(action, ())
        assert verdict.verdict == NEEDS_AUTHORITY

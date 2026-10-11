"""test_neutrality_trap.py — T-06: six-state finding classification tests.

The trap: systems claim "neutral" when they mean "unknown". These tests
prove the machine vocabulary kills it: every "no material harm" claim on a
harm-profile dimension needs a machine-validated finding state, and the
gate fails closed on anything that is not validated neutrality.

Negative controls throughout: each test names the exact seam that must
fail it, so a green run proves the seam works, not the data.
"""
import pytest

from kernel.protocol import harm_profile as hp
from kernel.protocol import neutrality_finding as nf
from kernel.protocol.typed_action import (
    ADMISSIBLE,
    NEEDS_EVIDENCE,
    TypedAction,
    law11_gate,
)

# ---------------------------------------------------------------------------
# Fixtures: profiles that say "no material harm".
# ---------------------------------------------------------------------------

BENIGN_DIMS = dict(
    severity=hp.SEVERITY_NEGLIGIBLE,
    reversibility=hp.REV_FULLY,
    timing=hp.TIME_IMMEDIATE,
    measurability=hp.MEAS_MEASURED,
    distribution=hp.DIST_SMALL_GROUP,
)


def negligible_profile(*group_ids):
    return hp.HarmProfile(
        groups=tuple(hp.GroupHarm(group_id=g, **BENIGN_DIMS) for g in group_ids),
        assessed_by="test",
        assessed_at="2026-10-11",
    )


def clean_action(profile, *assessments):
    """A typed action that is admissible on every OTHER Law 11 axis, so the
    only thing standing between it and ADMISSIBLE is the neutrality consult."""
    return TypedAction(
        actor_id="test",
        operation="read",
        environment="development",
        resource="test",
        rights_safe=True,
        safety_safe=True,
        privacy_safe=True,
        consent_obtained=True,
        reversibility="reversible",
        harm_profile=profile,
        neutrality_assessments=tuple(assessments),
    )


def severity_assessment(group, **kw):
    base = dict(dimension="severity", group=group, finding=nf.UNKNOWN)
    base.update(kw)
    return nf.NeutralityAssessment(**base)


# ---------------------------------------------------------------------------
# The six design tests.
# ---------------------------------------------------------------------------

def test_true_zero_requires_exact_zero_evidence():
    """R1: a bare 'no effect observed' must NOT classify TRUE_ZERO."""
    a = severity_assessment(
        "g1",
        finding=nf.TRUE_ZERO,
        effect_estimate=0.0,  # observed zero, but NOT by mechanism
    )
    v = nf.classify_finding(a)
    assert v.accepted_finding == nf.UNKNOWN, v
    assert not v.clears
    assert v.reason_ids[0].startswith("NEUTRALITY_TRUE_ZERO_UNEVIDENCED")

    # At the gate: the dimension does not clear -> NEEDS_EVIDENCE.
    verdict = law11_gate(clean_action(negligible_profile("g1"), a))
    assert verdict.verdict == NEEDS_EVIDENCE
    assert any("TRUE_ZERO_UNEVIDENCED" in r for r in verdict.reasons)


def test_true_zero_accepted_with_mechanism_evidence():
    """TRUE_ZERO with exact-zero evidence by mechanism clears."""
    a = severity_assessment(
        "g1",
        finding=nf.TRUE_ZERO,
        zero_by_mechanism=True,
        zero_by_mechanism_ref="code-path analysis: read path never touches PII store",
    )
    v = nf.classify_finding(a)
    assert v.accepted_finding == nf.TRUE_ZERO
    assert v.clears
    verdict = law11_gate(clean_action(negligible_profile("g1"), a))
    assert verdict.verdict == ADMISSIBLE, verdict.reasons


def test_wide_interval_centered_on_zero_is_inconclusive():
    """R2 — the core trap test: CI [-5, +5] centered on 0 is INCONCLUSIVE,
    and the gate must NOT admit on that dimension alone."""
    a = severity_assessment(
        "g1",
        finding=nf.PRACTICALLY_NEUTRAL,
        effect_estimate=0.1,
        uncertainty_interval=(-5.0, 5.0),  # wide, centered on zero
        tolerance=1.0,
        tolerance_approval_ref="domain-tolerances/v3#severity-eps",
        tolerance_preapproved=True,
    )
    v = nf.classify_finding(a)
    assert v.accepted_finding == nf.INCONCLUSIVE, v
    assert not v.clears
    assert v.reason_ids[0].startswith("NEUTRALITY_WIDE_INTERVAL")

    verdict = law11_gate(clean_action(negligible_profile("g1"), a))
    assert verdict.verdict == NEEDS_EVIDENCE
    assert any("WIDE_INTERVAL" in r for r in verdict.reasons)


def test_practically_neutral_rejects_posthoc_tolerance():
    """R3: a tolerance chosen AFTER the measurement is a defect — rejected
    even when |effect| <= epsilon."""
    a = severity_assessment(
        "g1",
        finding=nf.PRACTICALLY_NEUTRAL,
        effect_estimate=0.3,
        uncertainty_interval=(-0.6, 0.6),
        tolerance=1.0,
        tolerance_approval_ref="chosen after seeing the numbers",
        tolerance_preapproved=False,  # post-hoc
    )
    v = nf.classify_finding(a)
    assert v.accepted_finding == nf.INCONCLUSIVE, v
    assert not v.clears
    assert v.reason_ids[0].startswith("NEUTRALITY_TOLERANCE_POSTHOC")

    verdict = law11_gate(clean_action(negligible_profile("g1"), a))
    assert verdict.verdict == NEEDS_EVIDENCE


def test_practically_neutral_accepts_preapproved_tolerance():
    """PRACTICALLY_NEUTRAL with a preapproved epsilon, |effect| <= epsilon,
    and justified bounds fully inside epsilon clears."""
    a = severity_assessment(
        "g1",
        finding=nf.PRACTICALLY_NEUTRAL,
        effect_estimate=0.3,
        uncertainty_interval=(-0.6, 0.6),
        tolerance=1.0,
        tolerance_approval_ref="domain-tolerances/v3#severity-eps",
        tolerance_preapproved=True,
    )
    v = nf.classify_finding(a)
    assert v.accepted_finding == nf.PRACTICALLY_NEUTRAL
    assert v.clears
    verdict = law11_gate(clean_action(negligible_profile("g1"), a))
    assert verdict.verdict == ADMISSIBLE, verdict.reasons


def test_practically_neutral_rejects_missing_bounds():
    """R2's second half: no justified uncertainty bounds -> UNKNOWN, never
    PRACTICALLY_NEUTRAL."""
    a = severity_assessment(
        "g1",
        finding=nf.PRACTICALLY_NEUTRAL,
        effect_estimate=0.1,
        tolerance=1.0,
        tolerance_approval_ref="domain-tolerances/v3#severity-eps",
        tolerance_preapproved=True,
        # uncertainty_interval omitted
    )
    v = nf.classify_finding(a)
    assert v.accepted_finding == nf.UNKNOWN, v
    assert not v.clears
    verdict = law11_gate(clean_action(negligible_profile("g1"), a))
    assert verdict.verdict == NEEDS_EVIDENCE


def test_missing_finding_state_fails_closed():
    """R1 -> R4: a negligible-severity claim with NO assessment is treated
    as UNKNOWN and fails closed."""
    verdict = law11_gate(clean_action(negligible_profile("g1")))
    assert verdict.verdict == NEEDS_EVIDENCE
    assert any("MISSING_ASSESSMENT" in r for r in verdict.reasons)
    # The auditor can see which group and dimension blocked.
    assert any("group=g1" in r and "dimension=severity" in r for r in verdict.reasons)


def test_delayed_without_window_blocks():
    """R5: DELAYED with no named observation window -> NEEDS_EVIDENCE."""
    a = severity_assessment("g1", finding=nf.DELAYED)
    verdict = law11_gate(clean_action(negligible_profile("g1"), a))
    assert verdict.verdict == NEEDS_EVIDENCE
    assert any("DELAYED_NO_WINDOW" in r for r in verdict.reasons)


def test_delayed_with_window_is_admissible_with_advisory():
    """R5: DELAYED with a named T-07 window -> admissible-with-window; the
    window rides the verdict as advisory, never as a block."""
    a = severity_assessment(
        "g1",
        finding=nf.DELAYED,
        observation_window_ref="obs-window/2026-11-30:latency-regression",
    )
    verdict = law11_gate(clean_action(negligible_profile("g1"), a))
    assert verdict.verdict == ADMISSIBLE, verdict.reasons
    assert any("NEUTRALITY_DELAYED_WINDOW" in r for r in verdict.reasons)
    assert any("obs-window/2026-11-30" in r for r in verdict.reasons)


def test_unknown_unmeasured_inconclusive_fail_closed():
    """R4: the honest non-neutral states map to NEEDS_EVIDENCE."""
    for state in (nf.UNKNOWN, nf.UNMEASURED, nf.INCONCLUSIVE):
        a = severity_assessment("g1", finding=state)
        v = nf.classify_finding(a)
        assert v.accepted_finding == state
        assert not v.clears
        verdict = law11_gate(clean_action(negligible_profile("g1"), a))
        assert verdict.verdict == NEEDS_EVIDENCE, state
        assert any(f"NEUTRALITY_{state}" in r for r in verdict.reasons), state


# ---------------------------------------------------------------------------
# Integration: the consult layers ON the profile, never under it.
# ---------------------------------------------------------------------------

def test_no_profile_means_no_neutrality_consult():
    """Backward compat: without a harm profile the neutrality layer does
    not engage — the scalar Law 11 dimensions decide alone."""
    action = clean_action(None)
    verdict = law11_gate(action)
    assert verdict.verdict == ADMISSIBLE, verdict.reasons


def test_non_negligible_groups_need_no_assessment():
    """Only the neutrality claim (negligible severity) requires a finding
    state. A moderate-severity profile passes the consult with no
    assessments — T-05's own rules still govern it."""
    profile = hp.HarmProfile(
        groups=(
            hp.GroupHarm(
                group_id="g1",
                severity=hp.SEVERITY_MODERATE,
                reversibility=hp.REV_FULLY,
                timing=hp.TIME_IMMEDIATE,
                measurability=hp.MEAS_MEASURED,
                distribution=hp.DIST_SMALL_GROUP,
            ),
        ),
        assessed_by="test",
        assessed_at="2026-10-11",
    )
    consult = nf.consult_neutrality(profile, ())
    assert not consult.blocks_admission
    assert consult.verdicts == ()


def test_required_keys_are_per_group_never_averaged():
    """Two negligible groups -> two required keys; one good assessment does
    not cover the other."""
    a = severity_assessment(
        "g1",
        finding=nf.TRUE_ZERO,
        zero_by_mechanism=True,
        zero_by_mechanism_ref="path cannot execute",
    )
    consult = nf.consult_neutrality(negligible_profile("g1", "g2"), (a,))
    assert consult.blocks_admission
    assert any("MISSING_ASSESSMENT" in r and "group=g2" in r
               for r in consult.needs_evidence_reasons)


def test_voluntary_assessment_validated_not_ignored():
    """An assessment supplied for a non-claimed dimension is validated, not
    silently ignored — a voluntary UNKNOWN still fails closed."""
    profile = hp.HarmProfile(
        groups=(
            hp.GroupHarm(
                group_id="g1",
                severity=hp.SEVERITY_MODERATE,
                reversibility=hp.REV_FULLY,
                timing=hp.TIME_IMMEDIATE,
                measurability=hp.MEAS_MEASURED,
                distribution=hp.DIST_SMALL_GROUP,
            ),
        ),
        assessed_by="test",
        assessed_at="2026-10-11",
    )
    a = nf.NeutralityAssessment(dimension="reversibility", group="g1",
                               finding=nf.UNKNOWN)
    consult = nf.consult_neutrality(profile, (a,))
    assert consult.blocks_admission
    assert any("NEUTRALITY_UNKNOWN:group=g1:dimension=reversibility" in r
               for r in consult.needs_evidence_reasons)


def test_duplicate_assessment_rejected():
    """Two assessments for the same (group, dimension) is a defect, not a
    vote."""
    a1 = severity_assessment("g1", finding=nf.UNKNOWN)
    a2 = severity_assessment("g1", finding=nf.DELAYED)
    with pytest.raises(ValueError):
        nf.consult_neutrality(negligible_profile("g1"), (a1, a2))


def test_noncanonical_finding_rejected_at_construction():
    with pytest.raises(ValueError):
        nf.NeutralityAssessment(dimension="severity", group="g1",
                               finding="HARMLESS")


def test_inverted_interval_rejected_at_construction():
    with pytest.raises(ValueError):
        severity_assessment(
            "g1",
            finding=nf.PRACTICALLY_NEUTRAL,
            effect_estimate=0.1,
            uncertainty_interval=(1.0, -1.0),
            tolerance=2.0,
            tolerance_approval_ref="x",
            tolerance_preapproved=True,
        )


def test_neutrality_reasons_carry_group_and_dimension():
    """Receipts: an auditor sees WHY a dimension was called neutral — every
    reason id names its group and dimension."""
    consult = nf.consult_neutrality(negligible_profile("g1"), ())
    for r in consult.needs_evidence_reasons:
        assert r.startswith("NEUTRALITY_"), r
        assert "group=g1" in r, r
        assert "dimension=severity" in r, r

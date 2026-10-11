"""T-05: Law 11 structured harm profiles — H_g(a) per group, never collapsed.

Tests the seam: kernel/protocol/harm_profile.py + the step-2b consult in
kernel/protocol/typed_action.py::law11_gate.

Falsifier pattern (per the anti-theater standard): the anti-collapse,
unknown-fails-closed, and severity/reversibility-independence tests would
FAIL if the step-2b consult were removed from law11_gate — i.e. if the
profile existed as data but the gate never read it. The sabotage script
hidden_files/batt-t05/sabotage_remove_consult.py proves this by removing
exactly that block and re-running these tests.
"""
import pytest

from kernel.protocol import harm_profile as hp
from kernel.protocol.typed_action import (
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    TypedAction,
    law11_gate,
)


def _group(gid, severity=hp.SEVERITY_NEGLIGIBLE,
           reversibility=hp.REV_FULLY, timing=hp.TIME_IMMEDIATE,
           measurability=hp.MEAS_MEASURED, distribution=hp.DIST_SINGLE,
           **kw):
    return hp.GroupHarm(
        group_id=gid, severity=severity, reversibility=reversibility,
        timing=timing, measurability=measurability,
        distribution=distribution, **kw,
    )


def _profile(*groups, **kw):
    return hp.HarmProfile(groups=tuple(groups), assessed_by="t05-test",
                          assessed_at="2026-10-11T16:55:00Z", **kw)


def _action(profile=None, **kw):
    base = dict(
        actor_id="naya-2", operation="write", environment="development",
        resource="smart_note_events", authority_ref="grant-test-1",
        rights_safe=True, safety_safe=True, privacy_safe=True,
        consent_obtained=True, harm_profile=profile,
    )
    base.update(kw)
    return TypedAction(**base)


# ---------------------------------------------------------------------------
# 1. No collapse: one catastrophic group blocks, however many are unharmed.
# ---------------------------------------------------------------------------

def test_no_collapse_nine_unharmed_one_catastrophic():
    groups = [_group(f"person-{i}") for i in range(9)]
    groups.append(_group(
        "person-9", severity=hp.SEVERITY_CATASTROPHIC,
        reversibility=hp.REV_FULLY, timing=hp.TIME_IMMEDIATE,
        measurability=hp.MEAS_MEASURED, distribution=hp.DIST_SINGLE))
    verdict = law11_gate(_action(_profile(*groups)))
    assert verdict.verdict == PROHIBITED
    assert any("person-9" in r and "catastrophic" in r for r in verdict.reasons)
    assert "person-9" in verdict.affected_interests


def test_adversarial_average_would_admit_but_gate_blocks():
    """Documents WHY averaging is banned: a naive mean-severity decision
    function would admit this profile ('mostly negligible'), while the
    real gate blocks. If anyone ever replaces worst-of with a mean, this
    test names the exact failure."""
    groups = [_group(f"person-{i}") for i in range(9)]
    groups.append(_group("person-9", severity=hp.SEVERITY_CATASTROPHIC))
    profile = _profile(*groups)

    rank = {"negligible": 0, "minor": 1, "moderate": 2, "major": 3,
            "catastrophic": 4}
    mean_sev = sum(rank[g.severity] for g in profile.groups) / len(profile.groups)
    naive_would_admit = mean_sev < rank["moderate"]  # "on average it's minor"
    assert naive_would_admit, "test setup: the naive average must look safe"
    assert law11_gate(_action(profile)).verdict == PROHIBITED


# ---------------------------------------------------------------------------
# 2. Severity and reversibility are independent qualifiers.
# ---------------------------------------------------------------------------

def test_major_reversible_not_blocked_but_major_irreversible_blocked():
    reversible = _profile(_group("g1", severity=hp.SEVERITY_MAJOR,
                                 reversibility=hp.REV_FULLY))
    v = law11_gate(_action(reversible))
    assert v.verdict == ADMISSIBLE, v.reasons  # not blocked by the profile

    irreversible = _profile(_group("g1", severity=hp.SEVERITY_MAJOR,
                                   reversibility=hp.REV_IRREVERSIBLE))
    v = law11_gate(_action(irreversible))
    assert v.verdict == PROHIBITED
    assert any("major" in r and "irreversible" in r for r in v.reasons)


def test_negligible_irreversible_not_blocked():
    # Irreversibility alone is not harm: negligible severity stays admissible.
    # Severity and reversibility are independent — one never implies the other.
    # T-06 update: the negligible ("no material harm") claim now carries its
    # finding state (TRUE_ZERO by mechanism); without one the gate fails
    # closed on the neutrality trap (see tests/test_neutrality_trap.py).
    from kernel.protocol import neutrality_finding as nf
    profile = _profile(_group("g1", severity=hp.SEVERITY_NEGLIGIBLE,
                              reversibility=hp.REV_IRREVERSIBLE))
    assessment = nf.NeutralityAssessment(
        dimension="severity", group="g1", finding=nf.TRUE_ZERO,
        zero_by_mechanism=True,
        zero_by_mechanism_ref="no write path reaches external systems",
    )
    v = law11_gate(_action(profile, neutrality_assessments=(assessment,)))
    assert v.verdict == ADMISSIBLE
    assert not any(r.startswith("BLOCK:") for r in v.reasons)


def test_catastrophic_not_redeemed_by_reversibility():
    profile = _profile(_group("g1", severity=hp.SEVERITY_CATASTROPHIC,
                              reversibility=hp.REV_FULLY))
    v = law11_gate(_action(profile))
    assert v.verdict == PROHIBITED


# ---------------------------------------------------------------------------
# 3. Unknown is not safe: any unqualified dimension fails closed.
# ---------------------------------------------------------------------------

def test_unknown_dimension_fails_closed():
    profile = _profile(_group("g1", severity=hp.SEVERITY_MINOR,
                              reversibility=hp.REV_UNKNOWN,
                              timing=hp.TIME_UNKNOWN,
                              measurability=hp.MEAS_UNKNOWN,
                              distribution=hp.DIST_UNKNOWN))
    v = law11_gate(_action(profile))
    assert v.verdict == NEEDS_EVIDENCE
    assert any(r.startswith("UNKNOWN:group=g1:dimension=reversibility")
               for r in v.reasons)
    assert any(r.startswith("UNKNOWN:group=g1:dimension=timing")
               for r in v.reasons)


def test_fully_unknown_profile_never_admissible():
    v = law11_gate(_action(_profile(hp.GroupHarm(group_id="g1"))))
    assert v.verdict == NEEDS_EVIDENCE


# ---------------------------------------------------------------------------
# 4. Malformed input fails closed at construction.
# ---------------------------------------------------------------------------

def test_invalid_dimension_literal_raises():
    with pytest.raises(ValueError):
        hp.GroupHarm(group_id="g1", severity="extreme")


def test_empty_group_id_raises():
    with pytest.raises(ValueError):
        hp.GroupHarm(group_id="  ")


def test_empty_profile_raises():
    with pytest.raises(ValueError):
        hp.HarmProfile(groups=())


def test_duplicate_group_id_raises():
    with pytest.raises(ValueError):
        _profile(_group("g1"), _group("g1"))


# ---------------------------------------------------------------------------
# 5. The judgment preserves every group's full assessment (auditability).
# ---------------------------------------------------------------------------

def test_judgment_preserves_all_groups():
    profile = _profile(
        _group("elders", severity=hp.SEVERITY_MODERATE,
               reversibility=hp.REV_CONDITIONAL, timing=hp.TIME_DELAYED,
               measurability=hp.MEAS_ESTIMATED, distribution=hp.DIST_SMALL_GROUP,
               note="cultural impact"),
        _group("operators", severity=hp.SEVERITY_MINOR),
    )
    j = hp.judge(profile)
    assert {g.group_id for g in j.groups} == {"elders", "operators"}
    elders = next(g for g in j.groups if g.group_id == "elders")
    assert elders.note == "cultural impact"
    assert elders.timing == hp.TIME_DELAYED
    assert j.delayed_observation is True
    assert j.worst_severity == hp.SEVERITY_MODERATE  # worst-of, not a mean


# ---------------------------------------------------------------------------
# 6. Delayed timing is advisory: surfaced, not verdict-forcing.
# ---------------------------------------------------------------------------

def test_delayed_harm_surfaced_on_admissible_verdict():
    profile = _profile(_group("g1", severity=hp.SEVERITY_MINOR,
                              timing=hp.TIME_DELAYED))
    v = law11_gate(_action(profile))
    assert v.verdict == ADMISSIBLE
    assert any(r == "HARM_PROFILE_DELAYED_OBSERVATION_REQUIRED:g1"
               for r in v.reasons)


# ---------------------------------------------------------------------------
# 7. Backward compatibility: no profile -> existing behavior unchanged.
# ---------------------------------------------------------------------------

def test_backward_compat_scalar_violation_unchanged():
    v = law11_gate(_action(rights_safe=False))
    assert v.verdict == PROHIBITED
    assert "RIGHTS_VIOLATION" in v.reasons


def test_backward_compat_clean_action_admissible_with_empty_reasons():
    v = law11_gate(_action())
    assert v.verdict == ADMISSIBLE
    assert v.reasons == ()


def test_backward_compat_profile_defers_to_scalar_authority_rule():
    # A clean profile does not waive the protected-gate authority rule.
    profile = _profile(_group("g1", severity=hp.SEVERITY_MINOR))
    v = law11_gate(_action(profile, operation="deploy",
                           environment="production", authority_ref=None))
    assert v.verdict == NEEDS_AUTHORITY


# ---------------------------------------------------------------------------
# 8. Digest: deterministic, order-independent, Law-12-bindable.
# ---------------------------------------------------------------------------

def test_digest_deterministic_and_order_independent():
    p1 = _profile(_group("a", severity=hp.SEVERITY_MINOR), _group("b"))
    p2 = _profile(_group("b"), _group("a", severity=hp.SEVERITY_MINOR))
    assert hp.profile_digest(p1) == hp.profile_digest(p2)
    assert len(hp.profile_digest(p1)) == 64
    p3 = _profile(_group("a", severity=hp.SEVERITY_MAJOR), _group("b"))
    assert hp.profile_digest(p3) != hp.profile_digest(p1)

"""Adversarial suite for the Human Invaluable Gate — G(a).

Every case attacks the principle: no one gets priced, and no score can buy
a violation. All must be green.
"""

import inspect
import sys

import pytest

sys.path.insert(0, "/tmp/hig/tools")
import human_invaluable_gate as hig  # noqa: E402


def rights_action(benefit, action_id="a-rights"):
    return hig.ActionAssessment(
        action_id=action_id,
        description="Publish a user's private messages to boost engagement.",
        violates_rights=("PRIVACY", "CONSENT", "DIGNITY"),
        projected_benefit=benefit,
    )


def test_rights_violation_with_plus9_is_prohibited():
    v = hig.evaluate(rights_action(9.0))
    assert v.verdict == hig.PROHIBITED
    assert v.eligible_for_optimization is False
    assert any("PRIVACY" in r for r in v.reasons)


def test_anti_purchase_absurd_benefit_still_prohibited():
    # No benefit magnitude, however large, flips PROHIBITED to ADMISSIBLE.
    v = hig.evaluate(rights_action(1000.0))
    assert v.verdict == hig.PROHIBITED
    assert v.eligible_for_optimization is False


def test_benefit_magnitude_never_consulted():
    # Two actions differing ONLY in projected benefit get identical verdicts.
    low = hig.evaluate(rights_action(0.5, "a-low"))
    high = hig.evaluate(rights_action(1e9, "a-high"))
    assert (low.verdict, low.reasons) == (high.verdict, high.reasons)


def test_prohibited_action_absent_from_ranking():
    actions = [
        rights_action(9.0, "bad"),
        hig.ActionAssessment(action_id="good", description="Fix the broken link.",
                             projected_benefit=3.0),
    ]
    admissible, verdicts = hig.filter_candidates(actions)
    assert [a.action_id for a in admissible] == ["good"]
    refused = [v for v in verdicts if v.verdict == hig.PROHIBITED]
    assert len(refused) == 1 and refused[0].action_id == "bad"
    # The prohibited action is a refusal record only — no ranker input exists.
    assert refused[0].eligible_for_optimization is False


def test_medical_like_with_consent_safeguards_proportionality_admissible():
    a = hig.ActionAssessment(
        action_id="treatment",
        description="Treatment with unavoidable side effects, genuine benefit.",
        has_unavoidable_risk=True,
        genuine_benefit=True,
        consent_obtained=True,
        consent_detail="Informed consent signed, scope documented.",
        safeguards=("monitoring", "dose-limits", "stop-criteria"),
        proportionality_recorded=True,
        proportionality_detail="Expected benefit outweighs burden 10:1; least-harmful option.",
        projected_benefit=8.0,
    )
    v = hig.evaluate(a)
    assert v.verdict == hig.ADMISSIBLE
    assert v.eligible_for_optimization is True


def test_medical_like_without_consent_prohibited():
    a = hig.ActionAssessment(
        action_id="treatment-no-consent",
        has_unavoidable_risk=True,
        genuine_benefit=True,
        consent_obtained=False,
        safeguards=("monitoring",),
        proportionality_recorded=True,
        projected_benefit=8.0,
    )
    v = hig.evaluate(a)
    assert v.verdict == hig.PROHIBITED
    assert any("CONSENT_MISSING" in r for r in v.reasons)


def test_medical_like_without_safeguards_prohibited():
    a = hig.ActionAssessment(
        action_id="treatment-no-safeguards",
        has_unavoidable_risk=True,
        genuine_benefit=True,
        consent_obtained=True,
        safeguards=(),
        proportionality_recorded=True,
        projected_benefit=8.0,
    )
    v = hig.evaluate(a)
    assert v.verdict == hig.PROHIBITED
    assert any("SAFEGUARDS_MISSING" in r for r in v.reasons)


def test_medical_like_without_proportionality_prohibited():
    a = hig.ActionAssessment(
        action_id="treatment-no-prop",
        has_unavoidable_risk=True,
        genuine_benefit=True,
        consent_obtained=True,
        safeguards=("monitoring",),
        proportionality_recorded=False,
        projected_benefit=8.0,
    )
    v = hig.evaluate(a)
    assert v.verdict == hig.PROHIBITED
    assert any("PROPORTIONALITY_MISSING" in r for r in v.reasons)


def test_anti_averaging_collective_gain_cannot_buy_individual_harm():
    # A million units of collective benefit cannot offset one dignity violation
    # at the gate. The gate evaluates boundary compliance, never a net score.
    a = hig.ActionAssessment(
        action_id="sacrifice-one",
        description="Harm one person's dignity to benefit a million others.",
        violates_rights=("DIGNITY",),
        projected_benefit=1_000_000.0,
    )
    v = hig.evaluate(a)
    assert v.verdict == hig.PROHIBITED
    assert v.eligible_for_optimization is False


def test_prohibited_harm_without_rights_label_still_prohibited():
    a = hig.ActionAssessment(
        action_id="harm",
        causes_prohibited_harm=True,
        prohibited_harm_detail="Irreversible physical injury.",
        projected_benefit=500.0,
    )
    v = hig.evaluate(a)
    assert v.verdict == hig.PROHIBITED
    assert any("PROHIBITED_HARM" in r for r in v.reasons)


def test_clean_action_admissible():
    v = hig.evaluate(hig.ActionAssessment(action_id="clean", projected_benefit=2.0))
    assert v.verdict == hig.ADMISSIBLE
    assert v.eligible_for_optimization is True


def test_no_human_worth_scoring_structural():
    # The module must contain NO human-worth scoring — test-asserted.
    assert hig.no_human_worth_scoring() is True
    # Belt and braces: no function signature or name in this module may
    # accept a person as a scored entity.
    module = sys.modules[hig.__name__]
    for name, obj in vars(module).items():
        if name == "no_human_worth_scoring":
            continue  # the guard itself names what it guards against
        if inspect.isfunction(obj) and obj.__module__ == hig.__name__:
            blob = (name + " " + str(inspect.signature(obj))).lower()
            assert "person" not in blob, f"human entity in scored signature: {name}"
            assert "human_worth" not in blob
            assert "worth_of" not in blob


def test_action_assessment_carries_no_person_worth_field():
    fields = set(hig.ActionAssessment.__dataclass_fields__)
    joined = " ".join(fields).lower()
    assert "person" not in joined
    assert "worth" not in joined


def test_seam_into_value_calculus_hard_violation():
    v_bad = hig.evaluate(rights_action(9.0))
    v_good = hig.evaluate(hig.ActionAssessment(action_id="ok"))
    assert hig.hard_violation_flag(v_bad) is True
    assert hig.hard_violation_flag(v_good) is False


def test_unknown_right_rejected_at_construction():
    with pytest.raises(ValueError):
        hig.ActionAssessment(action_id="x", violates_rights=("MADE_UP_RIGHT",))


def test_zero_eligibility_means_never_ranked():
    # PROHIBITED => not eligible for optimization: simulate a downstream
    # ranker that only ever sees the admissible set.
    actions = [rights_action(1e6, f"bad-{i}") for i in range(5)]
    actions.append(hig.ActionAssessment(action_id="only-good", projected_benefit=0.1))
    admissible, verdicts = hig.filter_candidates(actions)
    ranked = sorted(admissible, key=lambda a: a.projected_benefit, reverse=True)
    assert [a.action_id for a in ranked] == ["only-good"]
    assert all(v.verdict == hig.PROHIBITED for v in verdicts if v.action_id != "only-good")

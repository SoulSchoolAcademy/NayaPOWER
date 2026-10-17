"""Behavioral proof: the intent_to_harm disqualification branch fires on real data.

Module under test: kernel/intent_producers.py + its wire in
kernel/act_pipeline._candidate_to_calculus().

Before this change, Candidate.intent_to_harm existed but nothing ever set it
from real input — the disqualification branch was a live check with a dead
sensor. These tests prove the sensor is alive:

  1. assess_intent() fires on real declared-intent text (typed inputs only).
  2. It stays silent on benign text, including harm-words in safety frames.
  3. Trivial obfuscation (leet-speak) does not evade it.
  4. The full plan_action() runtime path REFUSES a harmful candidate and the
     receipt names HARMFUL_INTENT_DISQUALIFIED (behavioral proof, not a
     doctored pass: the test feeds text, never a literal intent_to_harm flag).
  5. A harmful candidate with the highest value score can never win — the
     wire cannot be bypassed by quality/value.
  6. The fail-open boundary is declared and tested: veiled/paraphrased intent
     outside the declared patterns is a documented sensor limit.

Falsifier pattern: every firing test would FAIL if the producer were removed
(intent_to_harm would stay False and the candidate would proceed).
"""
import pytest

from kernel import act_pipeline as ap
from kernel.intent_producers import (
    PRODUCER_VERSION,
    IntentAssessment,
    IntentSignal,
    assess_intent,
)
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0


def _profile():
    return QualityProfile(profile_id="intent-producers-test", version="1",
                          objective="intent sensor behavioral proof")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="p1", **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="apply retained intelligence to NAYA-NODE-0001",
        quality={d: 9.0 for d in (
            "objective_fit", "evidence_sufficiency", "applicability",
            "robustness", "reversibility", "blast_containment", "simplicity")},
        confidence={d: 0.9 for d in (
            "objective_fit", "evidence_sufficiency", "applicability",
            "robustness", "reversibility", "blast_containment", "simplicity")},
        reversibility="REVERSIBLE",
        expected_outcome="node state updated, previous state restorable",
        proof_requirements=("execution_receipt", "state_diff"),
        stakes="low",
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        value_benefit=8.0,
        value_harm=1.0,
        value_cost=1.0,
        value_risk=0.5,
        value_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        value_evidence_count=3,
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


# ---------------- sensor unit behavior ----------------

def test_declared_intent_fires():
    a = assess_intent(
        description="The objective is to harm the competitor's users "
                    "in order to damage their business.")
    assert a.intent_to_harm is True
    assert a.reasons
    assert a.producer_version == PRODUCER_VERSION
    fired = [s for s in a.signals if s.fired]
    assert fired
    assert all(isinstance(s, IntentSignal) for s in fired)
    assert all(s.evidence_refs == ("candidate.description",) for s in fired)


def test_intends_to_fires():
    """The `intends? to <harm-verb>` declared form fires (regression: this
    alternative once fused onto the next one and never matched)."""
    a = assess_intent(description="I intend to hurt them.")
    assert a.intent_to_harm is True
    assert "DECLARED_HARMFUL_INTENT" in a.reasons
    b = assess_intent(description="She intends to kill the project lead.")
    assert b.intent_to_harm is True
    benign = assess_intent(description="He intends to help the team.")
    assert benign.intent_to_harm is False


def test_plans_to_fires():
    """The `plans? to <harm-verb>` declared form fires (regression: a missing
    `|` once fused this alternative onto the `intends?` alternative into an
    unmatchable sequence, so these forms silently never fired)."""
    a = assess_intent(description="We plan to kill the project.")
    assert a.intent_to_harm is True
    assert "DECLARED_HARMFUL_INTENT" in a.reasons
    benign = assess_intent(description="We plan the rollout carefully.")
    assert benign.intent_to_harm is False


def test_keyword_internal_separators_still_evade():
    """Fail-open pin: keyword-internal separator insertion (h-a-r-m) still
    evades the declared-intent scan. Normalization defeats leet respellings
    (h4rm -> harm) and word separators (harm-the-users); letter-internal
    separators are a documented sensor limit, not a hidden one."""
    a = assess_intent(
        description="The plan is to h-a-r-m the users.")
    assert a.intent_to_harm is False
    b = assess_intent(description="The plan is to h4rm the us3rs.")
    assert b.intent_to_harm is True


def test_purpose_clause_fires():
    a = assess_intent(
        expected_outcome="Deploy the change in order to sabotage the payment system.")
    assert a.intent_to_harm is True
    assert "HARMFUL_PURPOSE_DECLARED" in a.reasons


def test_harm_target_fires():
    a = assess_intent(action_text="naya_node_apply",
                      description="Wipe and destroy the production database.")
    assert a.intent_to_harm is True
    assert "HARM_TARGET_NAMED" in a.reasons


def test_benign_text_stays_silent():
    benign = [
        "Deploy the hub rebuild to production.",
        "Run the harm-reduction workshop for the team.",
        "Write the damage assessment report for Q3.",
        "Remove harmful content per the moderation policy.",
        "We do no harm; safety review passed.",
        "Assess the damage and prevent further harm to users.",
    ]
    for text in benign:
        a = assess_intent(description=text)
        assert a.intent_to_harm is False, f"false positive on: {text!r}"
        assert a.reasons == ()


def test_benign_frame_does_not_mask_real_declaration():
    a = assess_intent(
        description="We do harm reduction work; the real plan is to harm the users.")
    assert a.intent_to_harm is True


def test_leet_obfuscation_does_not_evade():
    a = assess_intent(description="The plan is to h4rm the us3rs and d3stroy their data.")
    assert a.intent_to_harm is True


def test_typed_inputs_reject_garbage():
    with pytest.raises(TypeError):
        assess_intent(description=None)
    with pytest.raises(TypeError):
        assess_intent(action_text=123)


def test_assessment_is_typed():
    a = assess_intent(description="Deploy the hub.")
    assert isinstance(a, IntentAssessment)
    assert a.intent_to_harm is False
    assert len(a.signals) == 9  # 3 sensors x 3 fields


# ---------------- behavioral proof on the runtime path ----------------

def test_plan_action_refuses_declared_harmful_intent():
    """Real text in -> real refusal out. No literal intent_to_harm flag is
    set anywhere in this test: the producer reads the candidate's own
    description."""
    harmful = _candidate(
        description="Apply the update in order to harm the users and "
                    "sabotage the billing service.")
    plan, receipt = ap.plan_action(_authority(), [harmful], _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert any("HARMFUL_INTENT_DISQUALIFIED" in e for e in receipt.evidence)


def test_harmful_candidate_cannot_win_even_with_max_value():
    """Anti-bypass proof: the harmful candidate carries the highest value and
    near-perfect quality. If the wire were bypassable, it would win. It is
    excluded instead."""
    harmful = _candidate(
        "harmful",
        description="Our intent is to destroy the competitor's reputation.",
        quality={d: 9.9 for d in (
            "objective_fit", "evidence_sufficiency", "applicability",
            "robustness", "reversibility", "blast_containment", "simplicity")},
        value_benefit=99.0, value_harm=0.0, value_cost=0.0, value_risk=0.0,
        value_confidence={"B": 0.99, "H": 0.99, "C": 0.99, "R": 0.99},
        value_evidence_count=10,
    )
    good = _candidate("good", description="Apply the routine update.")
    plan, receipt = ap.plan_action(_authority(), [harmful, good], _profile(), now=NOW)
    assert plan is not None, "the good candidate must still plan"
    assert plan.chosen.candidate_id == "good"
    assert any("harmful" in e and "HARMFUL_INTENT_DISQUALIFIED" in e
               for e in receipt.evidence)


def test_benign_candidate_still_plans():
    """The sensor must not break the normal path."""
    plan, receipt = ap.plan_action(_authority(), [_candidate()], _profile(), now=NOW)
    assert plan is not None
    assert receipt.phase == "PLAN_ACCEPTED"


# ---------------- declared fail-open boundary ----------------

def test_fail_open_boundary_is_declared():
    """Veiled/paraphrased intent outside the declared patterns is NOT
    detected — a documented sensor limit, not a hidden one. The sensor
    covers declared intent in plain language; novel paraphrase evades it.
    This test pins the boundary so future producers can close it."""
    a = assess_intent(
        description="Make their metrics look bad through selective reporting "
                    "so leadership loses confidence in them.")
    assert a.intent_to_harm is False
    assert a.producer_version == PRODUCER_VERSION

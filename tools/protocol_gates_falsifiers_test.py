"""Review-only falsifier suite for the machine gates merged via PR #1809.

This suite is INTENTIONALLY RED on the current candidate behavior. It adds no
authorization implementation or second LAW path; downstream source owners must
fix the canonical gates before these tests can be merged. Tests examine direct
adapter responses (NOT the wider LAW/ACT execution boundary).

Run: python -m pytest tools/protocol_gates_falsifiers_test.py -q
"""
import copy

import pytest

from protocol_gates import check_protected_gates, check_scorecard


def sample():
    return {
        "decision": "choose the safer protocol implementation",
        "options": ["safe", "unsafe"],
        "scores": {
            "safe": {"value": 9.5, "consequences": 9, "mission_alignment": 9,
                     "risk": 9, "reversibility": 9, "evidence_strength": 9, "total": 9.2},
            "unsafe": {"value": 5, "consequences": 3, "mission_alignment": 4,
                       "risk": 2, "reversibility": 3, "evidence_strength": 3, "total": 3.4},
        },
        "gates_checked": {
            "reversible_or_safe": True,
            "no_major_damage": True,
            "positive_forward_effect": True,
            "authority_clear": True,
        },
        "winner": "safe",
        "receipt_posted": True,
    }


def test_positive_control_admissible_read_only_work():
    r = check_protected_gates("Write a unit test in the isolated feature branch")
    assert r.passed


@pytest.mark.parametrize("action", [
    "Read the live database table containing private member profiles.",
    "Export all customer email addresses from the live service.",
    "Release the application update to paying users.",
])
def test_protected_actions_not_automatically_allowed_by_different_wording(action):
    r = check_protected_gates(action)
    assert not r.passed, "Ambiguous/protected action was ALLOW-by-default: " + action


def test_blank_action_never_grants_authorization():
    r = check_protected_gates("")
    assert not r.passed, "An empty action cannot establish valid authority."


def test_decision_gate_false_authority_is_not_a_pass():
    s = sample()
    s["gates_checked"]["authority_clear"] = False
    assert not check_scorecard(s).passed, "Denied authority must block a decision."


def test_decision_gate_false_damage_is_not_a_pass():
    s = sample()
    s["gates_checked"]["no_major_damage"] = False
    assert not check_scorecard(s).passed, "Unsafe consequence must block a decision."


def test_decision_winner_must_not_be_lower_scored_without_override():
    s = sample()
    s["winner"] = "unsafe"
    assert not check_scorecard(s).passed, "Lowest-value winner passed with no override."


def test_decision_receipt_boolean_is_only_attestation():
    s = sample()
    s["receipt_posted"] = True  # not an independently checked URL/receipt
    result = check_scorecard(s)
    assert result.passed  # format check currently; integration must not claim post verified

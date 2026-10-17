"""Tests for tools/scorecard.py — the automatic scorecard calculator.

Every test names a concrete work description and pins the score the
rubric must return. A test that cannot fail is theater; these can.
"""

import json
import subprocess
import sys

import pytest

sys.path.insert(0, "tools")
from scorecard import score_work  # noqa: E402


def good_work(**over):
    work = {
        "title": "Example good work",
        "evidence": [
            {"claim": "tests green", "ref": "tests/test_scorecard.py 12/12"},
            {"claim": "server tree matches", "ref": "tree 9d6af390"},
        ],
        "tests": {"ran": True, "passed": 12, "failed": 0, "can_fail": True},
        "verification": {"seat": "Naya Epsilon", "independent": True, "score": 9.5},
        "value": {"human_benefit": "a human gets a working checker",
                  "unblocks": "board-post rule becomes executable"},
        "prevention": {"gate": "receipt gate refuses field-missing posts", "wired": True},
        "honesty": {"why_not_10": "not yet run on a live PR",
                    "limits": ["one repo only"]},
    }
    work.update(over)
    return work


def test_caller_supplied_evidence_cannot_ship():
    report = score_work(good_work())
    assert report["criteria"]["evidence"]["score"] == 8.0
    assert "not authenticated" in report["criteria"]["evidence"]["reasons"][0]
    assert report["overall"] == 8.0
    assert report["verdict"] == "FIX"


def test_caller_cannot_inject_a_trusted_verifier():
    # A caller-controlled lambda must not be accepted as authenticated proof.
    with pytest.raises(TypeError):
        score_work(good_work(), evidence_verifier=lambda _item: True)


def test_forged_verified_flag_does_not_bypass_trust_boundary():
    forged = good_work(evidence=[
        {"claim": "tests green", "ref": "made-up://perfect", "verified": True},
        {"claim": "everything proven", "ref": "made-up://also-perfect", "verified": True},
    ])
    report = score_work(forged)
    assert report["criteria"]["evidence"]["score"] == 8.0
    assert report["verdict"] == "FIX"


def test_self_verification_capped_by_inviolable():
    report = score_work(good_work(
        verification={"seat": "Naya Verity", "independent": False, "score": 10.0}))
    assert report["criteria"]["verification"]["score"] == 3.0
    assert report["overall"] == 3.0
    assert report["verdict"] == "HOLD"


def test_no_evidence_means_no_bytes():
    report = score_work(good_work(evidence=[]))
    assert report["criteria"]["evidence"]["score"] == 2.0
    assert report["overall"] == 2.0


def test_evidence_without_refs_is_vague():
    report = score_work(good_work(evidence=[{"claim": "trust me"}]))
    assert report["criteria"]["evidence"]["score"] == 5.0


def test_activity_without_value_scores_3():
    report = score_work(good_work(value={}))
    assert report["criteria"]["value"]["score"] == 3.0
    assert report["overall"] == 3.0


def test_unblocks_without_human_benefit_scores_7():
    report = score_work(good_work(value={"unblocks": "the dock"}))
    assert report["criteria"]["value"]["score"] == 7.0


def test_red_tests_fail():
    report = score_work(good_work(
        tests={"ran": True, "passed": 10, "failed": 2, "can_fail": True}))
    assert report["criteria"]["tests"]["score"] == 5.0


def test_tests_that_cannot_fail_are_theater():
    report = score_work(good_work(
        tests={"ran": True, "passed": 12, "failed": 0, "can_fail": False}))
    assert report["criteria"]["tests"]["score"] == 5.0


def test_no_prevention_gate_means_class_can_recur():
    report = score_work(good_work(prevention={}))
    assert report["criteria"]["prevention"]["score"] == 4.0


def test_named_but_unwired_gate_scores_6():
    report = score_work(good_work(
        prevention={"gate": "a gate", "wired": False}))
    assert report["criteria"]["prevention"]["score"] == 6.0


def test_missing_honesty_scores_3():
    report = score_work(good_work(honesty={}))
    assert report["criteria"]["honesty"]["score"] == 3.0


def test_half_honest_scores_6():
    report = score_work(good_work(
        honesty={"why_not_10": "not yet live", "limits": []}))
    assert report["criteria"]["honesty"]["score"] == 6.0


def test_overall_is_minimum_not_average():
    # Five criteria at 10, one at 4 → overall 4, not ~9.
    report = score_work(good_work(prevention={}))
    assert report["overall"] == 4.0
    assert report["blocking"] == ["prevention"]


def test_unreadable_input_fail_closed():
    report = score_work(None)
    assert report["overall"] == 0.0
    assert report["verdict"] == "HOLD"


def test_cli_cannot_ship_without_trusted_evidence_verifier():
    payload = json.dumps(good_work())
    out = subprocess.run(
        [sys.executable, "tools/scorecard.py", "--json"],
        input=payload, capture_output=True, text=True)
    assert out.returncode == 1
    report = json.loads(out.stdout)
    assert report["verdict"] == "FIX"
    assert report["overall"] == 8.0
    assert "not authenticated" in report["criteria"]["evidence"]["reasons"][0]


def test_cli_hold_exit_1():
    payload = json.dumps(good_work(value={}))
    out = subprocess.run(
        [sys.executable, "tools/scorecard.py"],
        input=payload, capture_output=True, text=True)
    assert out.returncode == 1
    assert "HOLD" in out.stdout


def test_cli_unreadable_exit_2():
    out = subprocess.run(
        [sys.executable, "tools/scorecard.py"],
        input="not json", capture_output=True, text=True)
    assert out.returncode == 2


def test_to_10_lists_solutions_for_gaps():
    report = score_work(good_work(value={}))
    assert report["to_10"]
    assert any("human benefit" in fix for fix in report["to_10"])


def test_unverified_refs_generate_trusted_verifier_remediation():
    report = score_work(good_work())
    assert any("canonical authenticated evidence resolver" in fix for fix in report["to_10"])


def test_to_10_capped_at_10():
    worst = good_work(evidence=[], tests={"ran": False, "passed": 0,
                                           "failed": 0, "can_fail": False},
                      verification={}, value={}, prevention={}, honesty={})
    assert len(score_work(worst)["to_10"]) <= 10


def test_pass_3_hold_announces_and_passes_off():
    report = score_work(good_work(value={}, **{"pass": 3}))
    assert report["verdict"] == "HOLD"
    assert "Announce" in report["next"]
    assert "Pass off" in report["next"]


def test_pass_3_fix_announces():
    report = score_work(good_work(value={"human_benefit": "x"}, **{"pass": 3}))
    assert report["overall"] == 8.0
    assert report["verdict"] == "FIX"
    assert "Announce" in report["next"]



def test_malformed_evidence_item_prevents_perfect_evidence_score():
    work = good_work(evidence=[
        {"claim": "tests green", "ref": "tests/test_scorecard.py 12/12"},
        {"claim": "missing ref"},
    ])
    report = score_work(work)
    assert report["criteria"]["evidence"]["score"] == 5.0
    assert report["verdict"] == "HOLD"


def test_single_reference_cannot_score_10_without_internal_resolver():
    report = score_work(
        good_work(evidence=[{"claim": "tests green", "ref": "tests/test_scorecard.py 12/12"}]))
    assert report["criteria"]["evidence"]["score"] == 8.0
    assert report["verdict"] == "FIX"

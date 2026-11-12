"""Adversarial, pure checks against same-login false approvals.

Dependent on PR #2808. These tests are red on a5fa991 (baseline) and
must pass after the identity-separation repair; they do not prove the
supplied PR snapshot was fetched/authenticated from GitHub.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "protocol"))
from checks.identity_separation import check


def record(reviews, **overrides):
    base = {
        "number": 2808,
        "author_login": "nayapower-lane-agent[bot]",
        "merger_login": "nayapower-lane-agent[bot]",
        "merged": True,
        "claims_validated": True,
        "reviews": reviews,
    }
    base.update(overrides)
    return base


@pytest.mark.parametrize("reviews", [
    [{"login": "NAYAPOWER-LANE-AGENT[BOT]", "state": "APPROVED"}],
    [{"login": "other-seat", "state": "CHANGES_REQUESTED"}],
    [{"login": "other-seat", "state": "DISMISSED"}],
    [{"login": "other-seat", "state": "COMMENTED"}],
    [{"login": "other-seat", "state": "APPROVED"},
     {"login": "OTHER-SEAT", "state": "DISMISSED"}],
])
def test_merger_cannot_claim_independence_without_effective_approval(reviews):
    outcome = check(record(reviews))
    assert outcome["pass"] is False, outcome


def test_missing_merger_login_fails_closed_on_merged_pr():
    assert check(record([{"login": "other-seat", "state": "APPROVED"}],
                        merger_login=""))["pass"] is False


def test_unmerged_without_validation_can_wait_for_review():
    assert check(record([], merged=False, claims_validated=False,
                        merger_login=""))["pass"] is True


def test_valid_different_login_approved_eligible_for_other_gates():
    outcome = check(record([{"login": "other-seat", "state": "APPROVED"}]))
    assert outcome["pass"] is True, outcome


def test_case_only_author_alias_refused_when_merger_is_other_login():
    outcome = check(record([{"login": "NAYAPOWER-LANE-AGENT[BOT]",
                             "state": "APPROVED"}],
                           merger_login="merger-separate"))
    assert outcome["pass"] is False, outcome

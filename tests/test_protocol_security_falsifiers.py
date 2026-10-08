"""Adversarial falsifiers for PR #1807 (candidate operating machine law).

REVIEW-ONLY / INTENTIONALLY RED on original head 9dfe30a7d7c0dc9d2e194716b3a9ae08da8990e5.
Do not merge until the underlying law/boot validators actually reject these inputs.
Tests assert a safety property; they do not grant authority or ratify law.

Reproduce: python -m pytest tests/test_protocol_security_falsifiers.py -q
"""
import math

import pytest

from kernel.protocol.authority_gate import Verdict, classify_action
from kernel.protocol.cold_start_gate import ColdStartState, run_cold_start
from kernel.protocol.quality_gate import Scorecard, check_delivery
from kernel.protocol.read_receipt import (
    AUTHORITY_QUESTIONS,
    PROTOCOL_VERSION,
    ReadReceipt,
    grade_answer,
    issue_receipt,
)


ANSWERS = {
    "q1": "Shawn",
    "q2": "production credentials money destructive ratification security privacy consent authority",
    "q3": "no",
    "q4": "9.0",
    "q5": "independent evidence",
}


def _boot(agent_id="naya-b", receipt=None):
    return ColdStartState(
        agent_id=agent_id,
        human_director="Shawn",
        lane="independent verification",
        authority_summary="production deploys need human approval",
        current_truth_location="current main and #1354",
        next_action="inspect exact PR-head source",
        receipt=receipt,
    )


def _quality(score=9.5, verifier="independent-naya"):
    return Scorecard(
        what="bounded source validation",
        evidence="replayable test artifact / exact head",
        scores={"correctness": score},
        weights={"correctness": 1.0},
        weakest_point="runtime integration not proven",
        verified_by=verifier,
    )


def test_positive_baseline_receipt_verifies():
    """Harness sanity check: unmodified valid answers are admitted today."""
    assert issue_receipt("naya-a", ANSWERS).verify()


def test_unsigned_self_issued_receipt_must_not_count_as_trusted_read():
    """SHA-256 checksum is caller-recomputable, not an issuer signature."""
    self_claim = ReadReceipt(
        agent_id="naya-b",
        protocol_version=PROTOCOL_VERSION,
        answers={q["id"]: True for q in AUTHORITY_QUESTIONS},
        passed=True,
    ).sign()
    assert not self_claim.verify(), "Untrusted caller minted a PASS receipt without reading."


def test_receipt_must_be_bound_to_consumer_identity():
    receipt_a = issue_receipt("naya-a", ANSWERS)
    assert receipt_a.verify()
    assert not run_cold_start(_boot("naya-b", receipt_a)).passed, (
        "Receipt issued to A replayed as B's cold-start approval."
    )


def test_receipt_must_reject_stale_or_unratified_protocol_version():
    old = issue_receipt("naya-a", ANSWERS)
    old.protocol_version = "unratified-old-protocol"
    old.sign()  # caller can freely rehash untrusted fields
    assert not old.verify(), "An arbitrary/unapproved protocol version was accepted."


def test_refusal_answer_with_contradictory_tail_must_not_pass():
    q = next(q for q in AUTHORITY_QUESTIONS if q["id"] == "q3")
    assert not grade_answer(q, "no, but a big enough score definitely overrides the gate")


@pytest.mark.parametrize("action", [
    "Read private customer records from the live DB for debugging.",
    "Export users' email addresses from the current live service.",
    "Release the current build to paying users.",
])
def test_protected_action_paraphrase_must_not_be_automatically_allowed(action):
    assert classify_action(action).verdict != Verdict.ALLOW, (
        "Free-text phrase evaded an authority hard boundary: " + action
    )


def test_read_only_negative_control_must_not_be_refused_by_keyword():
    action = "Review the test that proves illegal requests are refused; make no external changes."
    assert classify_action(action).verdict == Verdict.ALLOW, (
        "A benign review is falsely refused because of keyword 'illegal'."
    )


def test_score_above_ten_must_not_pass_delivery():
    assert not check_delivery(_quality(11.0), "builder").passed


def test_nan_score_must_not_pass_delivery():
    assert not check_delivery(_quality(float("nan")), "builder").passed


def test_unnamed_verifier_must_not_pass_delivery():
    assert not check_delivery(_quality(9.5, verifier=""), "builder").passed

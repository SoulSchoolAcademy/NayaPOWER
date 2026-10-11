#!/usr/bin/env python3
"""
Tests for tools/activation_contract.py (#2244 req 1).

Negative controls: every required orientation element is removed, staled,
drifted, or conflicted in turn, and the gate must STAND_DOWN. One positive
control proves a fully-oriented worker PROCEEDs. All fixtures are hermetic:
a fake repo tree with known bytes, hashes recomputed by the fixture itself.
"""

import hashlib
import json
import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from activation_contract import (  # noqa: E402
    CANONICAL_FEEDS,
    ActivationClaim,
    verify_claim,
    VERDICT_PROCEED,
    VERDICT_STAND_DOWN,
)

LIVE_TIP = "57e935c1b44b10fcc27a80f8c99fc9ddb2e69440"
STALE_TIP = "ac95cadf0000000000000000000000000000000000"  # wrong SHA on purpose


@pytest.fixture()
def tree():
    """A fake repo tree with known mission-state + protocol bytes."""
    with tempfile.TemporaryDirectory() as d:
        ms_dir = os.path.join(d, "BRAIN")
        os.makedirs(ms_dir)
        ms_path = os.path.join(d, "BRAIN/CURRENT-MISSION-STATE.md")
        pr_path = os.path.join(d, "BRAIN/01-GOVERNANCE")
        os.makedirs(pr_path, exist_ok=True)
        pr_file = os.path.join(pr_path, "TEAM-NAYA-OPERATING-PROTOCOL-V1.md")
        with open(ms_path, "w") as f:
            f.write("# mission state @ live tip\n")
        with open(pr_file, "w") as f:
            f.write("# protocol @ live tip\n")
        yield d, ms_path, pr_file


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def make_claim(tree, ms_path, pr_file, **over):
    base = {
        "worker_id": "naya2-nightshift-build",
        "lane": "naya2/build",
        "main_sha": LIVE_TIP,
        "mission_state": {
            "path": "BRAIN/CURRENT-MISSION-STATE.md",
            "sha256": _sha(ms_path),
        },
        "protocol": {
            "path": "BRAIN/01-GOVERNANCE/TEAM-NAYA-OPERATING-PROTOCOL-V1.md",
            "sha256": _sha(pr_file),
        },
        "feeds_read": [1870, 1872],
        "sign_in_feed": 1870,
        "sign_in_evidence": "issue#1870:comment-6106864062",
        "board_ack": "live coordination board is #2175 (issue #1354 is archive-only)",
        "toc_ack": "TOC is #1599",
    }
    base.update(over)
    return ActivationClaim.from_dict(base)


def verdict_of(result):
    return result.verdict, {c.name: (c.passed, c.code) for c in result.checks}


# --- positive control --------------------------------------------------------

def test_valid_claim_proceeds(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file)
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_PROCEED, checks
    assert all(passed for passed, _ in checks.values())


def test_proceed_receipt_marks_sign_in_unverified(tree):
    """Honest boundary: even PROCEED never claims the sign-in landed."""
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file)
    result = verify_claim(claim, d, LIVE_TIP)
    assert result.verdict == VERDICT_PROCEED
    assert any("sign-in" in u for u in result.unverified), result.unverified


# --- negative controls: SHA ---------------------------------------------------

def test_stale_main_sha_stands_down(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file, main_sha=STALE_TIP)
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["main_sha_fresh"] == (False, "STALE_SHA")


def test_missing_main_sha_stands_down(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file, main_sha="")
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["main_sha_present"] == (False, "MISSING_SHA")


def test_claim_cannot_supply_its_own_tip(tree):
    """The live tip comes from the caller, never the claim: a claim whose
    SHA matches nothing independently verified must fail even if internally
    consistent."""
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file, main_sha=STALE_TIP)
    verdict, _ = verdict_of(verify_claim(claim, d, STALE_TIP + "x"))
    assert verdict == VERDICT_STAND_DOWN


# --- negative controls: artifact bytes ---------------------------------------

def test_mission_state_drift_stands_down(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file)
    with open(ms_path, "a") as f:
        f.write("tampered after the claim was written\n")
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["mission_state_intact"] == (False, "MISSION_STATE_DRIFT")


def test_protocol_drift_stands_down(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file)
    with open(pr_file, "a") as f:
        f.write("tampered after the claim was written\n")
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["protocol_intact"] == (False, "PROTOCOL_DRIFT")


def test_missing_mission_state_file_stands_down(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file)
    os.remove(ms_path)
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["mission_state_present"] == (False, "MISSION_STATE_MISSING")


# --- negative controls: feeds + sign-in ---------------------------------------

def test_unknown_feed_stands_down(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file, feeds_read=[1870, 9999])
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["feeds_known"] == (False, "UNKNOWN_FEED")


def test_sign_in_feed_not_read_stands_down(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file,
                       feeds_read=[1872], sign_in_feed=1870)
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["sign_in_feed_valid"] == (False, "SIGN_IN_FEED_INVALID")


def test_noncanonical_sign_in_feed_stands_down(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file,
                       feeds_read=[4242], sign_in_feed=4242)
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["feeds_known"] == (False, "UNKNOWN_FEED")
    assert checks["sign_in_feed_valid"] == (False, "SIGN_IN_FEED_INVALID")


def test_missing_sign_in_evidence_stands_down(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file, sign_in_evidence="  ")
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["sign_in_evidence"] == (False, "SIGN_IN_EVIDENCE_MISSING")


# --- negative controls: board / TOC reconciliation ----------------------------

def test_stale_board_1354_stands_down(tree):
    """The core #2244 reconciliation: naming #1354 as the live board fails."""
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file,
                       board_ack="live coordination board is #1354")
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["board_not_stale"] == (False, "STALE_BOARD")


def test_adversarial_board_swap_stands_down(tree):
    """'live board #1354 (archive #2175)' must not smuggle 1354 through."""
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file,
                       board_ack="live board #1354 (archive #2175)")
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["board_not_stale"] == (False, "STALE_BOARD")
    assert checks["board_ack_current"] == (False, "BOARD_ACK_MISSING")


def test_archive_qualification_in_own_clause_proceeds(tree):
    """Mentioning #1354 as archive in its own clause is fine."""
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file,
                       board_ack="live board is #2175. #1354 is archive-only.")
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_PROCEED, checks


def test_missing_board_ack_stands_down(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file, board_ack="i read the board")
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["board_ack_current"] == (False, "BOARD_ACK_MISSING")


def test_missing_toc_ack_stands_down(tree):
    d, ms_path, pr_file = tree
    claim = make_claim(tree, ms_path, pr_file, toc_ack="what toc?")
    verdict, checks = verdict_of(verify_claim(claim, d, LIVE_TIP))
    assert verdict == VERDICT_STAND_DOWN
    assert checks["toc_ack"] == (False, "TOC_ACK_MISSING")


# --- negative controls: malformed claims --------------------------------------

def test_malformed_claim_missing_field():
    with pytest.raises(ValueError, match="CLAIM_MALFORMED"):
        ActivationClaim.from_dict({"worker_id": "x"})


def test_malformed_claim_bad_artifact_pin():
    with pytest.raises(ValueError, match="CLAIM_MALFORMED"):
        ActivationClaim.from_dict({
            "worker_id": "x", "lane": "y", "main_sha": LIVE_TIP,
            "mission_state": {"path": "p"}, "protocol": {"path": "p", "sha256": "s"},
            "feeds_read": [], "sign_in_feed": 1870, "sign_in_evidence": "e",
            "board_ack": "live board #2175", "toc_ack": "#1599",
        })


# --- canonical feed registry ---------------------------------------------------

def test_canonical_feeds_are_the_nine_ratified():
    assert set(CANONICAL_FEEDS) == set(range(1865, 1874))

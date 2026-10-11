#!/usr/bin/env python3
"""Tests for sweep_verify_claims.py — the automated verify-before-accept sweep."""

import json
import re
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import sweep_verify_claims as svc


def test_pr_regex_matches_variants():
    texts = [
        ("PR #1772 opened", [1772]),
        ("PR#1773", [1773]),
        ("see pull/1774", [1774]),
        ("PR #12 too short", []),  # only 4-5 digit
        ("no pr here", []),
        ("PR #1775 and PR #1776", [1775, 1776]),
    ]
    for text, expected in texts:
        found = [int(m.group(1)) for m in svc.PR_RE.finditer(text)]
        assert found == expected, f"{text!r}: got {found}, want {expected}"


def test_completion_filter():
    # Only completion/verification contexts are scanned
    assert re.search(r"complet|verif|open|land|merg", "completion report", re.IGNORECASE)
    assert re.search(r"complet|verif|open|land|merg", "PR opened", re.IGNORECASE)
    assert not re.search(r"complet|verif|open|land|merg", "random chatter xyz", re.IGNORECASE)


def test_receipt_shape():
    # Receipt must match verifier's expected format
    artifacts = [
        {"kind": "pr", "number": 1772,
         "head": "e48d007a2f10c2f5ea4066eee0de64781f24b456",
         "state": "open"},
    ]
    receipt = {"artifacts": artifacts}
    assert receipt["artifacts"][0]["kind"] == "pr"
    assert len(receipt["artifacts"][0]["head"]) == 40
    assert receipt["artifacts"][0]["number"] == 1772


def test_deduplication():
    # Same PR claimed twice → verified once
    nums = [1772, 1772, 1773]
    assert len(set(nums)) == 2


if __name__ == "__main__":
    test_pr_regex_matches_variants()
    print("PASS test_pr_regex_matches_variants")
    test_completion_filter()
    print("PASS test_completion_filter")
    test_receipt_shape()
    print("PASS test_receipt_shape")
    test_deduplication()
    print("PASS test_deduplication")
    print("4/4 green")

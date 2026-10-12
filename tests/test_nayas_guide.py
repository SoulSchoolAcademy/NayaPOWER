#!/usr/bin/env python3
"""Tests for Naya's Guide — the decision layer.

These test the gate LOGIC with synthetic evidence (no GitHub API needed).
Live evidence mining is tested by running `guide merge --pr N --auto` directly.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
import nayas_guide as g


def make_evidence(**overrides):
    """Build a synthetic evidence dict for testing the gate."""
    base = {
        "pr": "9999",
        "details": {
            "title": "Test PR", "head_sha": "abc123", "head_branch": "test",
            "draft": False,
        },
        "ci": {
            "total": 5, "passed": ["a", "b", "c", "d", "e"],
            "own_failures": [], "pending": [],
            "has_runs": True, "all_green": True,
        },
        "receipt": {
            "present": True, "self_score": 9.5,
            "markers_found": {}, "scores_mentioned": [9.5],
        },
        "conflicts": False,
        "mergeable": True,
        "protected_changes": [],
    }
    for k, v in overrides.items():
        if isinstance(v, dict) and k in base and isinstance(base[k], dict):
            base[k] = {**base[k], **v}
        else:
            base[k] = v
    return base


def test_merge_all_green():
    ev = make_evidence()
    decision, reasons, conf = g.merge_decision(ev)
    assert decision == "MERGE", f"expected MERGE, got {decision}: {reasons}"
    assert conf == "high"
    print("PASS: all-green PR → MERGE")


def test_hold_on_ci_failure():
    ev = make_evidence(ci={"own_failures": ["test"], "all_green": False})
    decision, reasons, conf = g.merge_decision(ev)
    assert decision == "HOLD", f"expected HOLD, got {decision}"
    assert any("CI failures" in r for r in reasons)
    print("PASS: CI failure → HOLD")


def test_hold_on_ci_pending():
    ev = make_evidence(ci={"pending": ["test"], "all_green": False})
    decision, reasons, conf = g.merge_decision(ev)
    assert decision == "HOLD", f"expected HOLD, got {decision}"
    print("PASS: CI pending → HOLD")


def test_hold_on_missing_receipt():
    ev = make_evidence(receipt={"present": False, "self_score": 0.0,
                                 "markers_found": {"pass1": False}})
    decision, reasons, conf = g.merge_decision(ev)
    assert decision == "HOLD", f"expected HOLD, got {decision}"
    assert any("receipt" in r.lower() for r in reasons)
    print("PASS: missing receipt → HOLD")


def test_hold_on_low_self_score():
    ev = make_evidence(receipt={"present": True, "self_score": 8.0})
    decision, reasons, conf = g.merge_decision(ev)
    assert decision == "HOLD", f"expected HOLD, got {decision}"
    assert any("9.0" in r for r in reasons)
    print("PASS: self-score 8.0 → HOLD (below 9.0 bar)")


def test_hold_on_conflicts():
    ev = make_evidence(conflicts=True, mergeable=False)
    decision, reasons, conf = g.merge_decision(ev)
    assert decision == "HOLD", f"expected HOLD, got {decision}"
    print("PASS: conflicts → HOLD")


def test_ask_on_protected():
    ev = make_evidence(protected_changes=[".github/workflows/deploy.yml"])
    decision, reasons, conf = g.merge_decision(ev)
    assert decision == "ASK", f"expected ASK, got {decision}"
    print("PASS: protected changes → ASK (Shawn's gate)")


def test_hold_on_draft():
    ev = make_evidence(details={"draft": True})
    decision, reasons, conf = g.merge_decision(ev)
    assert decision == "HOLD", f"expected HOLD, got {decision}"
    print("PASS: draft PR → HOLD")


def test_receipt_detection():
    # A proper 3-pass receipt
    body = """
    ## 3-Pass Scorecard
    Pass 1: 7.5/10. Holes found: missing tests, unclear docs.
    Pass 2: 9.0/10. Holes filled.
    Pass 3: 9.5/10. Final pass confirmed.
    head: abc123def456
    Why not a 10: minor docs polish remaining.
    """
    has_receipt, details = g.mine_receipt(body)
    assert has_receipt, f"expected receipt detected: {details}"
    assert details["self_score"] == 9.5
    assert details["meets_bar"]
    print("PASS: 3-pass receipt detected, self-score 9.5")

    # Not a receipt — just a claim
    body2 = "This PR is done. Trust me. 3-pass receipt in body — this is it."
    has_receipt2, _ = g.mine_receipt(body2)
    assert not has_receipt2, "should NOT detect a receipt from a bare claim"
    print("PASS: bare claim without passes → no receipt (honest)")


def test_protected_patterns():
    for path in [".github/workflows/deploy-prod.yml", "src/secrets.py", "config/api_token.json"]:
        matched = any(
            __import__("re").search(p, path, __import__("re").IGNORECASE)
            for p in g.PROTECTED_PATTERNS
        )
        assert matched, f"{path} should be flagged as protected"
    print("PASS: protected patterns catch deploy/secrets/tokens")

    for path in ["src/feature.py", "tests/test_foo.py", "README.md"]:
        matched = any(
            __import__("re").search(p, path, __import__("re").IGNORECASE)
            for p in g.PROTECTED_PATTERNS
        )
        assert not matched, f"{path} should NOT be flagged"
    print("PASS: normal files not flagged as protected")


if __name__ == "__main__":
    test_merge_all_green()
    test_hold_on_ci_failure()
    test_hold_on_ci_pending()
    test_hold_on_missing_receipt()
    test_hold_on_low_self_score()
    test_hold_on_conflicts()
    test_ask_on_protected()
    test_hold_on_draft()
    test_receipt_detection()
    test_protected_patterns()
    print("\nAll 10 Naya's Guide logic tests passed.")

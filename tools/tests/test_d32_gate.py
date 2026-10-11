"""Tests for tools/d32_gate.py — D32 uncertainty-discipline document gate.

Every test asserts the EXACT verdict. If the gate logic is wrong, the test
fails. No vacuous checks: each negative case is verified to produce at
least one violation, each positive case to produce zero.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.d32_gate import check_document


# ---------------------------------------------------------------------------
# Positive cases — these documents MUST pass.
# ---------------------------------------------------------------------------

def test_pass_full_report():
    """A well-formed report: sourced numbers, does-not-claim, evidenced confidence."""
    doc = """# Wave 2 Status Report

All three directives built. D34 delivered in PR #2217
(see https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2217).
D35 delivered in PR #2215 at commit 82704029.

The gate is verified working — see the CI run
https://github.com/SoulSchoolAcademy/NayaPOWER/actions/runs/12345.

## WHAT THIS DOES NOT CLAIM

This report does not claim the directives are enforced in production.
It claims only that draft code exists on branches.
"""
    result = check_document(doc)
    assert result["verdict"] == "PASS", result["violations"]
    assert result["violations"] == []


def test_pass_numbers_with_issue_sources():
    """Numbers sourced by #issue references within 3 lines pass R1."""
    doc = """# Count

We tracked 58 directives (#2175).
Of those, 8 are built as code (#2217, #2215).

## What this does not claim

Does not claim enforcement — code only, per #2213 discussion.
"""
    result = check_document(doc)
    assert result["verdict"] == "PASS", result["violations"]


def test_pass_numbers_with_sha_sources():
    """Numbers sourced by commit SHAs pass R1."""
    doc = """# Merge record

3 merges landed at f2c614a5386b65c84156c707a93a775ec51b907a.

## WHAT THIS DOES NOT CLAIM

This does not claim the merges were protocol-clean.
"""
    result = check_document(doc)
    assert result["verdict"] == "PASS", result["violations"]


def test_pass_confidence_with_evidence():
    """'Verified' alongside a URL in the same paragraph passes R3."""
    doc = """# Gate status

The merge gate is verified working on PR #2196 —
see https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2196 for the run.

## WHAT THIS DOES NOT CLAIM

Does not claim all PRs are gated; only the merge path.
"""
    result = check_document(doc)
    assert result["verdict"] == "PASS", result["violations"]


def test_pass_dates_and_versions_not_claims():
    """Dates and version strings are not quantitative claims (no source needed)."""
    doc = """# Timeline

On 2026-10-11 we shipped v2.1 of the report.
Met at 23:44 to review.

## What this does not claim

This does not claim completeness.
"""
    result = check_document(doc)
    assert result["verdict"] == "PASS", result["violations"]


# ---------------------------------------------------------------------------
# Negative cases — these documents MUST fail, with the expected rule.
# ---------------------------------------------------------------------------

def test_fail_bare_numbers():
    """A bare number with no source within 3 lines fails R1."""
    doc = """# Report

We completed 42 tasks this week with great success.

## WHAT THIS DOES NOT CLAIM

Nothing further.
"""
    result = check_document(doc)
    assert result["verdict"] == "FAIL"
    rules = [v["rule"] for v in result["violations"]]
    assert "R1" in rules, result["violations"]
    r1 = [v for v in result["violations"] if v["rule"] == "R1"][0]
    assert r1["line"] == 3
    assert "42" in r1["text"]


def test_fail_missing_does_not_claim():
    """No DOES NOT CLAIM section fails R2, even if everything else is clean."""
    doc = """# Clean report

We fixed 3 bugs (#1234).

All good.
"""
    result = check_document(doc)
    assert result["verdict"] == "FAIL"
    rules = [v["rule"] for v in result["violations"]]
    assert "R2" in rules, result["violations"]


def test_fail_bare_proven():
    """'Proven' with no evidence in the paragraph fails R3."""
    doc = """# Claim

Our approach is proven to work at scale.

## WHAT THIS DOES NOT CLAIM

Does not claim universality.
"""
    result = check_document(doc)
    assert result["verdict"] == "FAIL"
    rules = [v["rule"] for v in result["violations"]]
    assert "R3" in rules, result["violations"]
    r3 = [v for v in result["violations"] if v["rule"] == "R3"][0]
    assert "proven" in r3["text"].lower()


def test_fail_bare_guaranteed_and_certain():
    """'Guaranteed' and 'certain' without evidence each fail R3."""
    doc = """# Promise

This is guaranteed to never fail.

We are certain it scales.

## WHAT THIS DOES NOT CLAIM

Does not claim anything else.
"""
    result = check_document(doc)
    assert result["verdict"] == "FAIL"
    r3 = [v for v in result["violations"] if v["rule"] == "R3"]
    assert len(r3) == 2, result["violations"]
    words = " ".join(v["text"] for v in r3).lower()
    assert "guaranteed" in words
    assert "certain" in words


def test_fail_all_three_rules():
    """A document violating R1, R2, and R3 fails with all three rules cited."""
    doc = """# Bad report

We shipped 99 features. It is verified awesome.
"""
    result = check_document(doc)
    assert result["verdict"] == "FAIL"
    rules = {v["rule"] for v in result["violations"]}
    assert rules == {"R1", "R2", "R3"}, result["violations"]


# ---------------------------------------------------------------------------
# Gate integrity — the tests themselves must be able to fail.
# ---------------------------------------------------------------------------

def test_gate_rejects_empty_document():
    """Empty document fails R2 (sanity: the gate is not vacuously passing)."""
    result = check_document("")
    assert result["verdict"] == "FAIL"
    assert any(v["rule"] == "R2" for v in result["violations"])


def test_violation_shape():
    """Violations carry line (int), rule (R1/R2/R3), text (str)."""
    result = check_document("We did 7 things.\n")
    assert result["verdict"] == "FAIL"
    for v in result["violations"]:
        assert isinstance(v["line"], int)
        assert v["rule"] in ("R1", "R2", "R3")
        assert isinstance(v["text"], str) and v["text"]

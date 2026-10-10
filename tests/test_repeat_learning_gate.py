"""Negative-control-first tests for the Repeat Tracker v1.1 gate."""

from kernel.protocol.repeat_learning_gate import (
    BLOCKED,
    LEARNING_HOLD,
    PASS,
    evaluate_learning_gate,
    release_learning_hold,
)


def _entry(status="WIRED"):
    return {
        "id": "R-002",
        "directive_essence": "Hourly PDF reports must match the intelligent boards brand format",
        "fix_status": status,
        "death_stage": "APPLY",
        "death_evidence": "sample was retrieved but application failed",
    }


def test_unresolved_known_repeat_cannot_complete():
    r = evaluate_learning_gate(
        topic="reports",
        action="deliver hourly PDF report",
        ledger=[_entry("WIRED")],
        evidence_refs=["receipt-before"],
        authority_ref="board-1354",
        timestamp=1000,
    )
    assert not r.passed
    assert r.decision == LEARNING_HOLD
    assert r.receipts[0].directive_id == "R-002"
    assert r.receipts[0].fix_status_before == "WIRED"
    assert r.receipts[0].decision == LEARNING_HOLD


def test_unknown_ledger_is_blocked_not_pass():
    r = evaluate_learning_gate(
        topic="reports",
        action="deliver report",
        ledger=None,
        evidence_refs=[],
        authority_ref="board-1354",
        timestamp=1000,
    )
    assert not r.passed
    assert r.decision == BLOCKED


def test_ambiguous_unresolved_match_is_blocked():
    a = _entry("WIRED")
    b = {
        **_entry("BUILT"),
        "id": "R-999",
        "directive_essence": "PDF reports must use the intelligent boards format",
    }
    r = evaluate_learning_gate(
        topic="reports",
        action="deliver PDF report",
        ledger=[a, b],
        evidence_refs=["x"],
        authority_ref="board-1354",
        timestamp=1000,
    )
    assert not r.passed
    assert r.decision == BLOCKED


def test_verified_fix_requires_behavioral_evidence():
    r = evaluate_learning_gate(
        topic="reports",
        action="deliver report",
        ledger=[_entry("VERIFIED")],
        evidence_refs=[],
        authority_ref="board-1354",
        timestamp=1000,
    )
    assert not r.passed
    assert r.decision == BLOCKED


def test_verified_fix_can_pass_with_later_behavioral_evidence():
    r = evaluate_learning_gate(
        topic="reports",
        action="deliver report",
        ledger=[_entry("VERIFIED")],
        evidence_refs=["later-behavior-receipt-001"],
        authority_ref="board-1354",
        timestamp=1000,
    )
    assert r.passed
    assert r.decision == PASS


def test_governed_exception_does_not_mutate_fix_status():
    e = _entry("WIRED")
    r = release_learning_hold(
        entry=e,
        authorized_exception={
            "authorized": True,
            "authority_ref": "shawn-2026-10-08",
            "reason": "time-bounded emergency delivery",
            "scope": "single report",
            "expiry": "2026-10-08T20:00:00Z",
        },
        timestamp=1000,
    )
    assert r.passed
    assert r.decision == PASS
    assert e["fix_status"] == "WIRED"
    assert "exception" in r.receipts[0].reason


def test_unauthorized_exception_cannot_release():
    r = release_learning_hold(
        entry=_entry("WIRED"),
        authorized_exception={
            "authorized": False,
            "authority_ref": "none",
            "reason": "because",
            "scope": "anything",
            "expiry": "later",
        },
        timestamp=1000,
    )
    assert not r.passed
    assert r.decision == BLOCKED

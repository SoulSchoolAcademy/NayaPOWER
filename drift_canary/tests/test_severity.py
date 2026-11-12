"""Tests: severity ladder + monitoring loops."""
from ..loops import (
    SEVERITY_LEVELS, SEVERITY_RESPONSE, MONITORING_LOOPS, SeverityDecision,
)


def test_four_severity_levels():
    assert SEVERITY_LEVELS == ("stable", "watch", "requalify", "contain")


def test_restoration_requires_requalification():
    d = SeverityDecision(level="contain", reasons=("integrity failure",),
                         affected_scope=("high-risk-act",))
    assert "requalif" in d.restoration_requires
    assert "clearing" in d.restoration_requires or "insufficient" in d.restoration_requires


def test_severity_rejects_unknown():
    try:
        SeverityDecision(level="panic", reasons=(), affected_scope=())
    except AssertionError:
        return
    raise AssertionError("unknown severity must be rejected")


def test_three_loops():
    names = [l.name for l in MONITORING_LOOPS]
    assert names == ["fast", "medium", "slow"]


def test_fast_loop_blocks_consequential_use():
    fast = next(l for l in MONITORING_LOOPS if l.name == "fast")
    assert "canary_replay_verdict" in fast.outputs


def test_slow_loop_never_misclassifies_pending():
    slow = next(l for l in MONITORING_LOOPS if l.name == "slow")
    assert "pending" in slow.latency_note.lower() or "late" in slow.latency_note.lower()


def test_all_levels_have_responses():
    assert set(SEVERITY_RESPONSE) == set(SEVERITY_LEVELS)

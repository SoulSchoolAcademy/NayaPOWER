"""AER-LIVE-4 tests: Uncertainty Preservation."""
import sys
sys.path.insert(0, "drift_canary")

from aer_live4_uncertainty import (
    UncertaintyVerdict,
    assess_with_uncertainty,
)


def test_missing_fact_yields_undetermined():
    r = assess_with_uncertainty(
        facts_established={"a": True, "b": True},
        facts_missing={"c"},
    )
    assert r.verdict == UncertaintyVerdict.UNDETERMINED
    assert len(r.reconstruction_obligations) == 1
    assert r.reconstruction_obligations[0].missing_fact == "c"


def test_undetermined_never_becomes_false():
    """Missing evidence is not disproof."""
    r = assess_with_uncertainty(
        facts_established={"a": True},
        facts_missing={"b"},
    )
    assert r.verdict != UncertaintyVerdict.DISPROVEN


def test_debt_is_range_not_guess():
    r = assess_with_uncertainty(
        facts_established={},
        facts_missing={"history"},
        debt_evidence={"min": 2.0, "max": 7.0},
    )
    assert r.debt_range.min_possible == 2.0
    assert r.debt_range.max_possible == 7.0
    assert not r.debt_range.is_precise()


def test_deadline_escalates_not_manufactures():
    """Deadline escalates urgency, never flips UNDETERMINED to PROVEN."""
    r = assess_with_uncertainty(
        facts_established={"a": True},
        facts_missing={"b"},
        deadline_approaching=True,
    )
    assert r.verdict == UncertaintyVerdict.UNDETERMINED
    assert r.reconstruction_obligations[0].escalated is True


def test_all_proven_yields_proven():
    r = assess_with_uncertainty(
        facts_established={"a": True, "b": True},
        facts_missing=set(),
    )
    assert r.verdict == UncertaintyVerdict.PROVEN

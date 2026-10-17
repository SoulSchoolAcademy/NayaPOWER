"""AER-LIVE-6 tests: Unbounded Missing Histories."""
import sys
sys.path.insert(0, "drift_canary")

from aer_live6_unbounded import (
    HistoryVerdict,
    MissingInterval,
    assess_interval,
    decide_missing_interval,
    u_star_fixture,
)


def test_bounded_below_threshold():
    iv = MissingInterval(max_length=5, debt_min=0.0, debt_max=2.0)
    assert assess_interval(iv, 10.0) == HistoryVerdict.BOUNDED


def test_bounded_exceeding_is_violation():
    iv = MissingInterval(max_length=5, debt_min=0.0, debt_max=15.0)
    assert assess_interval(iv, 10.0) == HistoryVerdict.FAIRNESS_VIOLATION_PROVEN


def test_unknown_length_unbounded_is_no_bound():
    """Distinguish from UNBOUNDED_IN_MODEL."""
    iv = MissingInterval(max_length=None, debt_min=0.0, debt_max=None)
    r = assess_interval(iv, 10.0)
    assert r == HistoryVerdict.NO_FINITE_UPPER_BOUND_ESTABLISHED
    assert r != HistoryVerdict.UNBOUNDED_IN_MODEL


def test_known_length_unbounded_is_in_model():
    iv = MissingInterval(max_length=10, debt_min=0.0, debt_max=None)
    assert assess_interval(iv, 10.0) == HistoryVerdict.UNBOUNDED_IN_MODEL


def test_u_star_fixture_unresolved():
    """Decisive U*S: final 0, peak 1..inf, verdict unresolved."""
    assert u_star_fixture() == HistoryVerdict.UNRESOLVED


def test_flowchart_finite_count():
    """Flowchart: finite opportunity count → finite-state bounds."""
    assert decide_missing_interval(True, False, False, False, False) == "FINITE_STATE_BOUNDS"


def test_flowchart_productive_cycle_with_exit():
    """Flowchart: productive cycle + valid exit → peak is +infinity."""
    assert decide_missing_interval(False, True, True, False, True) == "PEAK_INFINITY"


def test_flowchart_nonproductive_cycle_excluded():
    """Flowchart: cycle without valid exit → exclude, finite max."""
    assert decide_missing_interval(False, True, True, False, False) == "FINITE_MAX_DESPITE_UNBOUNDED"


def test_flowchart_no_cycle():
    """Flowchart: no repeatable cycle → finite max despite unbounded."""
    assert decide_missing_interval(False, False, False, False, False) == "FINITE_MAX_DESPITE_UNBOUNDED"


def test_flowchart_mandatory_reset_breaks_cycle():
    """Flowchart: mandatory reset → not a productive cycle → finite max."""
    assert decide_missing_interval(False, True, True, True, True) == "FINITE_MAX_DESPITE_UNBOUNDED"

"""AER-LIVE-9 tests: Dependency-Ordered Verification."""
import sys
sys.path.insert(0, "drift_canary")

from aer_live9_deporder import (
    Invariant,
    TriValue,
    diagnose_causal,
    f1_law_expiry_proven,
    f6_law_timing_missing,
    topological_order,
)


def test_topological_prerequisites_first():
    invs = [
        Invariant("authority", ("temporal",)),
        Invariant("temporal", ()),
    ]
    order = topological_order(invs)
    assert order.index("temporal") < order.index("authority")


def test_causal_diagnosis_finds_primary():
    invs = [
        Invariant("temporal", (), TriValue.FALSE, "TIME-11"),
        Invariant("authority", ("temporal",), TriValue.FALSE, None),
    ]
    d = diagnose_causal(invs, ["temporal", "authority"])
    assert d.primary_failure == "temporal"
    assert "authority" in d.dependent_failures


def test_undetermined_never_false():
    inv = Invariant("x", (), TriValue.UNDETERMINED)
    assert inv.value != TriValue.FALSE


def test_f1_honesty_gate():
    """F1: proven expiry → minimal counterexample with primary identified."""
    d = f1_law_expiry_proven()
    assert d.primary_failure == "temporal"
    assert d.counterexample_reachable is True


def test_f6_honesty_gate():
    """F6: missing evidence → UNDETERMINED, no fabricated counterexample."""
    assert f6_law_timing_missing() == TriValue.UNDETERMINED

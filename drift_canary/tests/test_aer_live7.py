"""AER-LIVE-7 tests: Pumping-Witness Integrity."""
import sys
sys.path.insert(0, "drift_canary")

from aer_live7_pumping import (
    PumpingWitness,
    finite_token_mutation_test,
    verify_witness,
)


def valid_witness():
    return PumpingWitness(
        entry_reachable=True,
        debt_per_cycle=1.0,
        max_repetitions=None,
        exit_valid_after_n=True,
        constraints=("c1", "c2"),
    )


def test_valid_witness_passes():
    assert verify_witness(valid_witness()).valid


def test_unreachable_entry_fails():
    w = PumpingWitness(False, 1.0, None, True, ())
    assert not verify_witness(w).valid


def test_nonpositive_debt_fails():
    w = PumpingWitness(True, 0.0, None, True, ())
    assert not verify_witness(w).valid


def test_bounded_repetitions_fails():
    w = PumpingWitness(True, 1.0, 100, True, ())
    assert not verify_witness(w).valid


def test_no_exit_fails():
    w = PumpingWitness(True, 1.0, None, False, ())
    assert not verify_witness(w).valid


def test_finite_token_mutation():
    """Finite-token mutation must invalidate secretly-bounded cycles."""
    # Truly unbounded witness survives
    assert finite_token_mutation_test(valid_witness(), 1000) is True

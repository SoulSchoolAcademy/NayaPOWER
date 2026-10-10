"""AER-LIVE-7 tests: Pumping-Witness Integrity."""
import sys
sys.path.insert(0, "drift_canary")

import pytest

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


def test_finite_token_mutation_negative():
    """NEGATIVE: a witness that passes verification but consumes tokens
    per cycle must FAIL the mutation test — proving the check actually
    discriminates instead of echoing verify_witness."""
    w = PumpingWitness(
        entry_reachable=True,
        debt_per_cycle=1.0,
        max_repetitions=None,
        exit_valid_after_n=True,
        constraints=("c1",),
        tokens_per_cycle=10.0,
    )
    # Passes syntactic verification...
    assert verify_witness(w).valid
    # ...but the finite-token mutation invalidates the unbounded claim.
    assert finite_token_mutation_test(w, 1000) is False


def test_finite_token_mutation_huge_bound_still_fails():
    """Arbitrary repetition means NO finite ceiling: even an enormous
    token pool invalidates a token-consuming witness."""
    w = PumpingWitness(True, 1.0, None, True, (),
                       tokens_per_cycle=1.0)
    assert verify_witness(w).valid
    assert finite_token_mutation_test(w, 10**18) is False


def test_finite_token_mutation_rejects_negative_bound():
    with pytest.raises(ValueError):
        finite_token_mutation_test(valid_witness(), -1)


def test_negative_tokens_rejected():
    with pytest.raises(ValueError):
        PumpingWitness(True, 1.0, None, True, (), tokens_per_cycle=-1.0)

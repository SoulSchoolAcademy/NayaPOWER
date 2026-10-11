"""Tests for drift_canary/pumping_witness.py (D62 / AER-LIVE-7).

Negative controls throughout: every rejection path is exercised, the
verifier is proven to be a real control by a dedicated mutation test (a
sabotaged replay MUST break verification — verified red), and the
AER-LIVE-007 fixtures behave exactly as the directive prescribes:

  - the naive checker (cycle-shape only) declares the two-token fixture
    UNBOUNDED — the bug D62 exists to catch;
  - the real verifier rejects it with the minimal counterexample at the
    third repetition;
  - mandatory-reset and unreachable-exit fixtures are rejected;
  - the valid witness keeps its unbounded peak and finite final debt,
    reproducible by a cold verifier from the certificate bytes alone;
  - the quantifiers stay separate: an accepted witness answers UNRESOLVED
    on the breach question, and any upgrade to a breach fails closed —
    a pumping witness is never a starvation accusation.
"""
import json

import pytest

from drift_canary import pumping_witness as d62
from drift_canary.pumping_witness import (
    BREACH,
    PROVEN_UNBOUNDED,
    UNRESOLVED,
    WITNESS_REJECTED,
    CertificateSerializationError,
    CertificateShapeError,
    PumpingStep,
    PumpingWitnessCertificate,
    PumpingWitnessError,
    StarvationAccusationError,
    certificate_from_json,
    certificate_to_json,
    fixtures_aer_live_007,
    independent_verify,
    is_minimal,
    minimize_certificate,
    naive_unbounded_checker,
    upgrade_to_breach,
    verify_pumping_witness,
)


@pytest.fixture()
def fixtures():
    return fixtures_aer_live_007()


def test_valid_witness_accepted(fixtures):
    v = verify_pumping_witness(fixtures["valid"])
    assert v.accepted is True
    assert v.peak_status == PROVEN_UNBOUNDED
    # Quantifier separation: peak proven, breach UNRESOLVED.
    assert v.breach_verdict == UNRESOLVED
    assert v.failure is None
    assert v.demonstrated
    for k, peak, final in v.demonstrated:
        assert peak == 3 + k  # entry_debt 2 + 1 entry U + k cycle U's
        assert final == 0  # the valid exit clears the counter
    assert v.certificate_fingerprint


def test_valid_witness_finite_final_debt(fixtures):
    v = verify_pumping_witness(fixtures["valid"])
    assert v.accepted
    finals = {final for _, _, final in v.demonstrated}
    assert all(isinstance(f, int) for f in finals)
    assert 0 in finals


def test_naive_checker_declares_two_token_unbounded(fixtures):
    # The defective baseline: sees the self-loop, declares unbounded —
    # ignoring the finite recovery-token supply. This is the bug.
    assert naive_unbounded_checker(fixtures["two_token_defect"]) == PROVEN_UNBOUNDED


def test_two_token_defect_rejected_with_minimal_counterexample(fixtures):
    v = verify_pumping_witness(fixtures["two_token_defect"])
    assert v.accepted is False
    assert v.peak_status == WITNESS_REJECTED
    assert v.breach_verdict == UNRESOLVED
    assert v.failure is not None
    # Minimal counterexample: the cycle repeats twice, the THIRD
    # traversal exhausts the last recovery token.
    assert "repetition 3" in v.failure
    assert "recovery_token" in v.failure
    assert "not arbitrarily repeatable" in v.failure


def test_two_token_supply_one_fails_at_repetition_two():
    f = fixtures_aer_live_007()
    cert = f["two_token_defect"]
    one_token = PumpingWitnessCertificate(
        obligation_id=cert.obligation_id,
        boundary_ref=cert.boundary_ref,
        entry_debt=cert.entry_debt,
        entry_path=cert.entry_path,
        cycle=cert.cycle,
        exit_path=cert.exit_path,
        initial_resources=(("recovery_token", 1),),
        model_assumptions=cert.model_assumptions,
    )
    v = verify_pumping_witness(one_token)
    assert not v.accepted
    assert "repetition 2" in v.failure


def test_mandatory_reset_defect_rejected(fixtures):
    v = verify_pumping_witness(fixtures["mandatory_reset_defect"])
    assert not v.accepted
    assert v.peak_status == WITNESS_REJECTED
    assert "mandatory reset" in v.failure


def test_unreachable_exit_defect_rejected(fixtures):
    v = verify_pumping_witness(fixtures["unreachable_exit_defect"])
    assert not v.accepted
    assert v.peak_status == WITNESS_REJECTED
    assert "exit" in v.failure


def test_short_cycle_rejected():
    # A zero-debt step minimizes away; an empty remainder is defective.
    cert = PumpingWitnessCertificate(
        obligation_id="short",
        boundary_ref="ledger@verified-rev",
        entry_debt=0,
        entry_path=(),
        cycle=(PumpingStep(name="noop", debt_delta=0),),
        exit_path=(PumpingStep(name="S", debt_delta=0, clears_debt=True),),
        initial_resources=(),
        model_assumptions=("test",),
    )
    v = verify_pumping_witness(cert)
    assert not v.accepted
    assert "not proof of unboundedness" in v.failure or "minimization" in v.failure


def test_nonminimal_certificate_refused_with_part_named(fixtures):
    cert = fixtures["valid"]
    padded = PumpingWitnessCertificate(
        obligation_id=cert.obligation_id,
        boundary_ref=cert.boundary_ref,
        entry_debt=cert.entry_debt,
        entry_path=cert.entry_path + (PumpingStep(name="identity", debt_delta=0),),
        cycle=cert.cycle,
        exit_path=cert.exit_path,
        initial_resources=cert.initial_resources,
        model_assumptions=cert.model_assumptions,
    )
    minimal, _ = is_minimal(padded)
    assert minimal is False
    v = verify_pumping_witness(padded)
    assert not v.accepted
    assert "non-minimal" in v.failure


def test_minimize_certificate_produces_fixed_point(fixtures):
    cert = fixtures["valid"]
    padded = PumpingWitnessCertificate(
        obligation_id=cert.obligation_id,
        boundary_ref=cert.boundary_ref,
        entry_debt=cert.entry_debt,
        entry_path=cert.entry_path + (PumpingStep(name="identity", debt_delta=0),),
        cycle=cert.cycle + (PumpingStep(name="zero", debt_delta=0),),
        exit_path=cert.exit_path,
        initial_resources=cert.initial_resources + (("unused_claim", 5),),
        model_assumptions=cert.model_assumptions,
    )
    minimized = minimize_certificate(padded)
    assert minimized == cert
    assert is_minimal(minimized) == (True, "minimized")


def test_entry_with_mandatory_reset_unreachable():
    cert = PumpingWitnessCertificate(
        obligation_id="entry-reset",
        boundary_ref="ledger@verified-rev",
        entry_debt=0,
        entry_path=(PumpingStep(name="R", debt_delta=0, is_mandatory_reset=True),),
        cycle=(PumpingStep(name="U", debt_delta=1),),
        exit_path=(PumpingStep(name="S", debt_delta=0, clears_debt=True),),
        initial_resources=(),
        model_assumptions=("test",),
    )
    v = verify_pumping_witness(cert)
    assert not v.accepted
    assert "entry not independently reachable" in v.failure


def test_empty_cycle_is_shape_error():
    with pytest.raises(CertificateShapeError):
        PumpingWitnessCertificate(
            obligation_id="empty",
            boundary_ref="b",
            entry_debt=0,
            entry_path=(),
            cycle=(),
            exit_path=(PumpingStep(name="S", debt_delta=0),),
            model_assumptions=("test",),
        )


def test_missing_assumptions_is_shape_error():
    with pytest.raises(CertificateShapeError):
        PumpingWitnessCertificate(
            obligation_id="no-assumptions",
            boundary_ref="b",
            entry_debt=0,
            entry_path=(),
            cycle=(PumpingStep(name="U", debt_delta=1),),
            exit_path=(PumpingStep(name="S", debt_delta=0),),
            model_assumptions=(),
        )


def test_upgrade_to_breach_always_fails_closed(fixtures):
    v = verify_pumping_witness(fixtures["valid"])
    assert v.accepted
    with pytest.raises(StarvationAccusationError):
        upgrade_to_breach(v)
    # Even a rejected verdict cannot be laundered into a breach claim.
    r = verify_pumping_witness(fixtures["two_token_defect"])
    with pytest.raises(StarvationAccusationError):
        upgrade_to_breach(r)


def test_cold_verifier_reproduces_from_certificate_bytes(fixtures):
    cert = fixtures["valid"]
    payload = certificate_to_json(cert)
    v_cold = independent_verify(payload)
    v_hot = verify_pumping_witness(cert)
    assert v_cold.accepted == v_hot.accepted
    assert v_cold.peak_status == v_hot.peak_status
    assert v_cold.breach_verdict == v_hot.breach_verdict == UNRESOLVED
    assert v_cold.demonstrated == v_hot.demonstrated
    assert v_cold.certificate_fingerprint == v_hot.certificate_fingerprint


def test_cold_verifier_rejects_two_token_from_bytes(fixtures):
    payload = certificate_to_json(fixtures["two_token_defect"])
    v = independent_verify(payload)
    assert not v.accepted
    assert "repetition 3" in v.failure


def test_cold_verifier_fails_closed_on_malformed_bytes():
    with pytest.raises(CertificateSerializationError):
        independent_verify(b"not-json-at-all{{{")
    with pytest.raises(CertificateSerializationError):
        independent_verify(json.dumps({"obligation_id": "x"}).encode())


def test_roundtrip_serialization(fixtures):
    cert = fixtures["valid"]
    back = certificate_from_json(certificate_to_json(cert))
    assert back == cert


def test_exit_reachable_at_every_sampled_count(fixtures):
    v = verify_pumping_witness(fixtures["valid"])
    assert v.accepted
    ks = [k for k, _, _ in v.demonstrated]
    assert 0 in ks and 1000 in ks
    # Peak strictly grows with repetitions; final stays finite.
    peaks = [p for _, p, _ in v.demonstrated]
    assert peaks == sorted(peaks) and len(set(peaks)) == len(peaks)


def test_mutation_control_sabotaged_replay_goes_red(monkeypatch, fixtures):
    """The verifier must be a real control: if the replay machinery is
    sabotaged so U steps stop adding debt, the valid fixture MUST fail
    verification. Verified red here proves the green above is earned."""
    # Sabotage at the cycle-gain level: flip the debt deltas.
    real_gain = d62._cycle_debt_gain
    monkeypatch.setattr(d62, "_cycle_debt_gain", lambda cycle: -real_gain(cycle))
    v = verify_pumping_witness(fixtures["valid"])
    assert not v.accepted, "sabotaged gain must break verification"


def test_verifier_recomputes_entry_never_trusts_claim():
    # A certificate whose entry_path does not reproduce its own claimed
    # entry state still verifies only on replay — the verifier recomputes.
    cert = PumpingWitnessCertificate(
        obligation_id="recompute",
        boundary_ref="ledger@verified-rev",
        entry_debt=5,
        entry_path=(PumpingStep(name="U", debt_delta=1),),
        cycle=(PumpingStep(name="U", debt_delta=1),),
        exit_path=(PumpingStep(name="S", debt_delta=0, clears_debt=True),),
        initial_resources=(),
        model_assumptions=("test",),
    )
    v = verify_pumping_witness(cert)
    assert v.accepted
    # Entry replay: 5 + 1 = 6; peaks are 6 + k, not 5 + k.
    assert v.demonstrated[0] == (0, 6, v.demonstrated[0][2])


def test_zero_supply_resource_fails_at_first_repetition():
    cert = PumpingWitnessCertificate(
        obligation_id="zero-supply",
        boundary_ref="b",
        entry_debt=0,
        entry_path=(),
        cycle=(PumpingStep(name="U", debt_delta=1,
                           resource_costs=(("fuel", 1),)),),
        exit_path=(PumpingStep(name="S", debt_delta=0, clears_debt=True),),
        initial_resources=(),
        model_assumptions=("test",),
    )
    v = verify_pumping_witness(cert)
    assert not v.accepted
    assert "repetition 1" in v.failure


def test_verdict_model_assumptions_named(fixtures):
    v = verify_pumping_witness(fixtures["valid"])
    assert v.model_assumptions
    joined = " ".join(v.model_assumptions)
    assert "AER-LIVE-007" in joined


def test_rejection_verdict_invariants(fixtures):
    for name in ("two_token_defect", "mandatory_reset_defect",
                 "unreachable_exit_defect"):
        v = verify_pumping_witness(fixtures[name])
        assert not v.accepted
        assert v.peak_status == WITNESS_REJECTED
        assert v.breach_verdict == UNRESOLVED
        assert v.failure
        assert v.demonstrated == ()


def test_minimization_preserves_resource_constrained_cycle_step():
    """Finding 1 (medium): minimize_certificate dropped zero-debt cycle
    steps even when they carried resource costs — erasing the fuel
    constraint and letting a bounded cycle verify as unbounded. The
    minimizer must keep resource-constrained steps; the verifier must
    then REJECT on fuel exhaustion, not ACCEPT."""
    fuel_step = PumpingStep(name="F", debt_delta=0,
                            resource_costs=(("fuel", 1),))
    cert = PumpingWitnessCertificate(
        obligation_id="fuel",
        boundary_ref="b",
        entry_debt=0,
        entry_path=(),
        cycle=(PumpingStep(name="U", debt_delta=1), fuel_step),
        exit_path=(PumpingStep(name="S", debt_delta=0, clears_debt=True),),
        initial_resources=(("fuel", 2),),
        model_assumptions=("test",),
    )
    minimized = minimize_certificate(cert)
    assert len(minimized.cycle) == 2  # the fuel step is load-bearing
    assert minimized.cycle[1] == fuel_step
    assert is_minimal(minimized) == (True, "minimized")
    v = verify_pumping_witness(minimized)
    assert not v.accepted
    assert v.peak_status == WITNESS_REJECTED
    # Supply 2, cost 1/traversal: traversals 1-2 complete, #3 exhausts.
    assert "repetition 3" in v.failure
    assert "fuel" in v.failure


def test_entry_consumption_shifts_minimal_counterexample():
    """Finding 2: the minimal counterexample used pre-entry supplies.
    Entry consumes 1 of 2 tokens and the cycle costs 1/traversal — the
    true first-failing repetition is 2 (post-entry supply 1), not 3."""
    cert = PumpingWitnessCertificate(
        obligation_id="entry-consumes",
        boundary_ref="b",
        entry_debt=0,
        entry_path=(PumpingStep(name="E", debt_delta=0,
                                resource_costs=(("tok", 1),)),),
        cycle=(PumpingStep(name="U", debt_delta=1,
                           resource_costs=(("tok", 1),)),),
        exit_path=(PumpingStep(name="S", debt_delta=0, clears_debt=True),),
        initial_resources=(("tok", 2),),
        model_assumptions=("test",),
    )
    assert is_minimal(cert) == (True, "minimized")
    v = verify_pumping_witness(cert)
    assert not v.accepted
    assert v.peak_status == WITNESS_REJECTED
    assert "repetition 2" in v.failure
    assert "tok" in v.failure


def test_demonstrated_peak_tracks_exit_debt():
    """Finding 4: `demonstrated` peak was debt-before-exit. An exit with
    positive-debt steps pushes the true peak above it — the reported peak
    must say so (probe: reported 0, true 5)."""
    cert = PumpingWitnessCertificate(
        obligation_id="exit-debt",
        boundary_ref="b",
        entry_debt=0,
        entry_path=(),
        cycle=(PumpingStep(name="U", debt_delta=1),),
        exit_path=(PumpingStep(name="X", debt_delta=5),),
        initial_resources=(),
        model_assumptions=("test",),
    )
    assert is_minimal(cert) == (True, "minimized")
    v = verify_pumping_witness(cert)
    assert v.accepted
    assert v.peak_status == PROVEN_UNBOUNDED
    # k=0: pre-exit debt 0, exit adds 5 → peak 5, final 5.
    assert v.demonstrated[0] == (0, 5, 5)
    # Peaks still strictly grow with the repetition count.
    peaks = [p for _, p, _ in v.demonstrated]
    assert peaks == sorted(peaks) and len(set(peaks)) == len(peaks)

"""Tests for drift_canary/full_state_repeatability.py (D63 / AER-LIVE-8).

Negative controls throughout: every rejection path is exercised, the
verifier is proven to be a real control by a dedicated mutation test (a
sabotaged certificate MUST break verification — verified red), and the
AER-LIVE-008 fixtures behave exactly as the directive prescribes:

  - the naive checker (debt-gain only) declares the authority-expiry and
    budget-drain fixtures REPEATABLE — the bug D63 exists to catch;
  - the real verifier rejects them with the minimal counterexample named
    (AUTHORITY at repetition 51; BUDGET at repetition 20);
  - zero-gain, finite-retries (CONTROL), broken-entry, and
    unaffordable-exit fixtures are rejected;
  - the valid fixture (TREATMENT: eligible waiting) ACCEPTS with
    arbitrary repeatability, reproducible by a cold verifier from the
    certificate bytes alone;
  - repeatability never answers the authorization question, and any
    upgrade to a production authorization fails closed.
"""
import pytest

from drift_canary import full_state_repeatability as d63
from drift_canary.full_state_repeatability import (
    AUTHORITY,
    BUDGET,
    EVIDENCE,
    NOT_REPEATABLE,
    REPEATABLE,
    UNDETERMINED,
    CertificateSerializationError,
    CertificateShapeError,
    FullState,
    ProductionAuthorizationError,
    RepeatabilityCertificate,
    StateTransition,
    certificate_from_json,
    certificate_to_json,
    fixtures_aer_live_008,
    independent_verify,
    is_minimal,
    minimize_certificate,
    naive_repeatability_checker,
    upgrade_to_authorization,
    verify_full_state_repeatability,
)


@pytest.fixture()
def fixtures():
    return fixtures_aer_live_008()


def test_valid_accepted(fixtures):
    v = verify_full_state_repeatability(fixtures["valid"])
    assert v.accepted is True
    assert v.repeatability == REPEATABLE
    # Arbitrary: no finite break exists.
    assert v.verified_up_to is None
    # Repeatability never answers the authorization question.
    assert v.authorization == UNDETERMINED
    assert v.failure is None
    assert v.certificate_fingerprint
    # Demonstrated triples are replayed: (repetition, debt, budget).
    assert v.demonstrated[0] == (0, 0.0, 100.0)
    assert v.demonstrated[1] == (1, 1.0, 100.0)
    assert all(d[1] == d[0] * 1.0 for d in v.demonstrated)


def test_authority_expiry_rejected(fixtures):
    v = verify_full_state_repeatability(fixtures["authority_expiry_defect"])
    assert v.accepted is False
    assert v.repeatability == NOT_REPEATABLE
    # Minimal counterexample: AUTHORITY at repetition 51.
    assert AUTHORITY in v.failure
    assert "51" in v.failure
    assert v.authorization == UNDETERMINED


def test_budget_drain_rejected(fixtures):
    v = verify_full_state_repeatability(fixtures["budget_drain_defect"])
    assert v.accepted is False
    # 100 - 20*5 = 0, not > 0: breaks exactly at repetition 20.
    assert BUDGET in v.failure
    assert "20" in v.failure


def test_zero_gain_rejected(fixtures):
    v = verify_full_state_repeatability(fixtures["zero_gain_defect"])
    assert v.accepted is False
    assert "debt gain" in v.failure


def test_finite_retries_rejected_control(fixtures):
    """CONTROL: 3 finite retries cannot support the arbitrary-repetition
    claim — retries exhaust at repetition 4."""
    v = verify_full_state_repeatability(fixtures["finite_retries_defect"])
    assert v.accepted is False
    assert "CONTROL" in v.failure
    assert "4" in v.failure


def test_broken_entry_rejected(fixtures):
    v = verify_full_state_repeatability(fixtures["broken_entry_defect"])
    assert v.accepted is False
    assert "entry" in v.failure
    assert AUTHORITY in v.failure


def test_unaffordable_exit_rejected(fixtures):
    """The invariant holds arbitrarily, but the exit costs 150 against a
    100 budget — proof obligation 4 fails independently of preservation."""
    v = verify_full_state_repeatability(fixtures["unaffordable_exit_defect"])
    assert v.accepted is False
    assert "exit" in v.failure
    assert "150" in v.failure


def test_naive_checker_declares_defects_repeatable(fixtures):
    """The bug D63 exists to catch: a debt-gain-only checker declares the
    authority-expiry and budget-drain fixtures repeatable."""
    assert naive_repeatability_checker(
        fixtures["authority_expiry_defect"]) == REPEATABLE
    assert naive_repeatability_checker(
        fixtures["budget_drain_defect"]) == REPEATABLE
    # The real verifier rejects both.
    assert verify_full_state_repeatability(
        fixtures["authority_expiry_defect"]).accepted is False
    assert verify_full_state_repeatability(
        fixtures["budget_drain_defect"]).accepted is False


def test_naive_checker_agrees_on_zero_gain(fixtures):
    assert naive_repeatability_checker(
        fixtures["zero_gain_defect"]) == NOT_REPEATABLE


def test_mutation_breaks_verification(fixtures):
    """Verified red: sabotage the valid certificate (evidence now corrupts
    on the first traversal) — the verifier MUST reject. If it still
    accepted, the green would be unearned."""
    valid = fixtures["valid"]
    sabotaged_step = StateTransition(
        name="U:unserved-round", debt_gain=1.0,
        component_ttl=((EVIDENCE, 0),))
    sabotaged = RepeatabilityCertificate(
        obligation_id=valid.obligation_id,
        boundary_ref=valid.boundary_ref,
        entry_state=valid.entry_state,
        entry_established=valid.entry_established,
        cycle=(sabotaged_step,),
        exit_requires=valid.exit_requires,
        exit_cost=valid.exit_cost,
        retry_budget=valid.retry_budget,
        model_assumptions=valid.model_assumptions,
    )
    v = verify_full_state_repeatability(sabotaged)
    assert v.accepted is False
    assert EVIDENCE in v.failure
    assert "1" in v.failure


def test_cold_verifier_reproduces_valid(fixtures):
    payload = certificate_to_json(fixtures["valid"])
    v = independent_verify(payload)
    assert v.accepted is True
    assert v.repeatability == REPEATABLE
    assert v.certificate_fingerprint == verify_full_state_repeatability(
        fixtures["valid"]).certificate_fingerprint


def test_cold_verifier_reproduces_rejection(fixtures):
    payload = certificate_to_json(fixtures["authority_expiry_defect"])
    v = independent_verify(payload)
    assert v.accepted is False
    assert AUTHORITY in v.failure


def test_malformed_bytes_fail_closed():
    with pytest.raises(CertificateSerializationError):
        independent_verify(b"this is not json")
    with pytest.raises(CertificateSerializationError):
        independent_verify(b'{"obligation_id": "x"}')
    # Valid JSON, wrong shape: not a certificate.
    with pytest.raises(CertificateSerializationError):
        certificate_from_json(b'{"cycle": [{"name": 42}]}')


def test_upgrade_to_authorization_always_refused(fixtures):
    """Repeatability is a model property, never a production grant — on
    accepted AND rejected verdicts alike."""
    for name in ("valid", "authority_expiry_defect"):
        v = verify_full_state_repeatability(fixtures[name])
        with pytest.raises(ProductionAuthorizationError):
            upgrade_to_authorization(v)


def test_nonminimal_certificate_rejected(fixtures):
    """A no-op step padding the cycle is refused with the redundancy
    named, never silently repaired."""
    valid = fixtures["valid"]
    noop = StateTransition(name="noop", debt_gain=0.0)
    padded = RepeatabilityCertificate(
        obligation_id=valid.obligation_id,
        boundary_ref=valid.boundary_ref,
        entry_state=valid.entry_state,
        entry_established=valid.entry_established,
        cycle=(valid.cycle[0], noop),
        exit_requires=valid.exit_requires,
        exit_cost=valid.exit_cost,
        retry_budget=valid.retry_budget,
        model_assumptions=valid.model_assumptions,
    )
    assert is_minimal(padded)[0] is False
    v = verify_full_state_repeatability(padded)
    assert v.accepted is False
    assert "no-op" in v.failure


def test_minimization_fixed_point(fixtures):
    valid = fixtures["valid"]
    assert is_minimal(valid) == (True, "minimized")
    assert minimize_certificate(valid) == valid


def test_entry_not_established_rejected(fixtures):
    valid = fixtures["valid"]
    cert = RepeatabilityCertificate(
        obligation_id=valid.obligation_id,
        boundary_ref=valid.boundary_ref,
        entry_state=valid.entry_state,
        entry_established=False,
        cycle=valid.cycle,
        exit_requires=valid.exit_requires,
        exit_cost=valid.exit_cost,
        retry_budget=valid.retry_budget,
        model_assumptions=valid.model_assumptions,
    )
    v = verify_full_state_repeatability(cert)
    assert v.accepted is False
    assert "entry not established" in v.failure


def test_ttl_merges_to_strictest():
    """Duplicate TTLs for one component merge to the minimum — the
    authority breaks at repetition 31, not 51."""
    step_a = StateTransition(name="a", debt_gain=0.5,
                             component_ttl=((AUTHORITY, 50),))
    step_b = StateTransition(name="b", debt_gain=0.5,
                             component_ttl=((AUTHORITY, 30),))
    cert = RepeatabilityCertificate(
        obligation_id="ttl-merge",
        boundary_ref="ledger@verified-rev",
        entry_state=FullState(True, 100.0, True, True, True, True, True),
        entry_established=True,
        cycle=(step_a, step_b),
        exit_requires=(AUTHORITY,),
        exit_cost=0.0,
        retry_budget=None,
        model_assumptions=("ttl merge case",),
    )
    v = verify_full_state_repeatability(cert)
    assert v.accepted is False
    assert AUTHORITY in v.failure
    assert "31" in v.failure


def test_verdict_invariants_all_fixtures(fixtures):
    """Accepted ⟺ failure None; rejected ⟹ failure names the
    counterexample; authorization always UNDETERMINED."""
    for name, cert in fixtures.items():
        v = verify_full_state_repeatability(cert)
        assert v.authorization == UNDETERMINED, name
        if v.accepted:
            assert v.failure is None, name
            assert v.repeatability == REPEATABLE, name
        else:
            assert v.failure, name
            assert v.repeatability == NOT_REPEATABLE, name


def test_shape_errors_fail_closed():
    good_state = FullState(True, 100.0, True, True, True, True, True)
    good_step = StateTransition(name="s", debt_gain=1.0)

    def cert(**kw):
        params = dict(
            obligation_id="shape", boundary_ref="b", entry_state=good_state,
            entry_established=True, cycle=(good_step,),
            exit_requires=(AUTHORITY,), exit_cost=0.0, retry_budget=None,
            model_assumptions=("a",))
        params.update(kw)
        return RepeatabilityCertificate(**params)

    with pytest.raises(CertificateShapeError):
        cert(cycle=())  # empty cycle
    with pytest.raises(CertificateShapeError):
        cert(exit_requires=())  # shapeless exit
    with pytest.raises(CertificateShapeError):
        cert(exit_requires=("budget_remaining",))  # budget via exit_cost
    with pytest.raises(CertificateShapeError):
        cert(retry_budget=-1)
    with pytest.raises(CertificateShapeError):
        StateTransition(name="s", debt_gain=-1.0)
    with pytest.raises(CertificateShapeError):
        StateTransition(name="s", debt_gain=True)  # bool is not a number
    with pytest.raises(CertificateShapeError):
        StateTransition(name="s", debt_gain=1.0,
                        component_ttl=(("budget_remaining", 5),))
    with pytest.raises(CertificateShapeError):
        StateTransition(name="s", debt_gain=1.0,
                        component_ttl=(("authority_valid", -1),))
    with pytest.raises(CertificateShapeError):
        FullState(True, "lots", True, True, True, True, True)
    with pytest.raises(CertificateShapeError):
        FullState("yes", 100.0, True, True, True, True, True)

"""Tests for drift_canary/dependency_ordered_verification.py — D64/AER-LIVE-9.

Rule under test: verify prerequisites in dependency order, diagnose
failures in causal execution order, preserve three-valued results
(PROVEN_TRUE / PROVEN_FALSE / UNDETERMINED), and never fabricate
evidence: a failed witness kills the certificate, never the claim.

Negative controls throughout: every rejection path is exercised, the
naive checker's three bugs are demonstrated on the fixtures it gets
wrong, and a mutation control proves the verifier goes red when a
witness is sabotaged.
"""
import pytest

from drift_canary.dependency_ordered_verification import (
    DEFERRED,
    CertificateShapeError,
    CertificateSerializationError,
    DependencyCertificate,
    DependencyOrderVerdict,
    Invariant,
    JointInvariant,
    ModelStep,
    TriValue,
    Witness,
    _MODEL_ASSUMPTIONS,
    _spec_topological_order,
    aer_live9_certificate_cyclic,
    aer_live9_certificate_f1,
    aer_live9_certificate_f6,
    aer_live9_certificate_joint,
    aer_live9_model,
    canonical_verification_order,
    find_cycle,
    independent_verify,
    is_minimal_witness,
    naive_dependency_checker,
    replay_witness,
    serialize_certificate,
    transitive_prereqs,
    verify_dependency_order,
)

T = TriValue.PROVEN_TRUE
F = TriValue.PROVEN_FALSE
U = TriValue.UNDETERMINED


def _verdicts(v):
    return {iv.name: iv for iv in v.invariant_verdicts}


# ---------------------------------------------------------------------------
# F1: LAW expiry proven — the valid certificate.
# ---------------------------------------------------------------------------
def test_f1_accepts_with_roots_and_dependents():
    v = verify_dependency_order(aer_live9_certificate_f1())
    assert v.accepted, v.failure
    assert v.failure is None
    assert v.primary_failures == ("temporal", "budget")
    assert v.dependent_failures == ("lifecycle", "authority")
    iv = _verdicts(v)
    assert iv["temporal"].verdict == F.value
    assert iv["temporal"].independently_proven is True
    assert iv["temporal"].witness_status == "valid"
    assert iv["lifecycle"].verdict == F.value
    assert iv["lifecycle"].independently_proven is False
    assert iv["preservation"].verdict == U.value
    assert iv["exit"].verdict == U.value
    assert iv["obs"].verdict == T.value


def test_f1_verification_order_is_canonical_topological():
    v = verify_dependency_order(aer_live9_certificate_f1())
    order = v.verification_order
    pos = {n: i for i, n in enumerate(order)}
    cert = aer_live9_certificate_f1()
    for inv in cert.invariants:
        for pre in inv.prerequisites:
            assert pos[pre] < pos[inv.name], \
                f"{pre} must precede {inv.name}"
    assert order == ("obs", "budget", "timing", "temporal", "lifecycle",
                     "authority", "preservation", "exit")


def test_f1_minimal_one_cycle_witness():
    cert = aer_live9_certificate_f1()
    w = next(w for w in cert.witnesses if w.invariant == "temporal")
    ok, _ = replay_witness(w, cert)
    assert ok
    minimal, _ = is_minimal_witness(w, cert)
    assert minimal
    assert w.steps == ("advance_past_expiry",)


def test_every_falsified_invariant_is_primary_or_dependent():
    v = verify_dependency_order(aer_live9_certificate_f1())
    falsified = {n for n, iv in _verdicts(v).items()
                 if iv.verdict == F.value}
    assert set(v.primary_failures) | set(v.dependent_failures) == falsified
    assert not (set(v.primary_failures) & set(v.dependent_failures))


# ---------------------------------------------------------------------------
# F6: timing evidence missing — UNDETERMINED preserved, never fabricated.
# ---------------------------------------------------------------------------
def test_f6_accepts_with_no_failures():
    v = verify_dependency_order(aer_live9_certificate_f6())
    assert v.accepted, v.failure
    assert v.primary_failures == ()
    assert v.dependent_failures == ()
    iv = _verdicts(v)
    for name in ("timing", "temporal", "lifecycle", "authority",
                 "preservation", "exit"):
        assert iv[name].verdict == U.value, name


def test_f6_triggers_evidence_reconstruction():
    v = verify_dependency_order(aer_live9_certificate_f6())
    iv = _verdicts(v)
    assert "timing" in iv["temporal"].evidence_needed


def test_f6_naive_checker_invents_a_failure():
    cert = aer_live9_certificate_f6()
    naive = naive_dependency_checker(cert)
    # The naive checker collapses UNDETERMINED -> FALSE and names a
    # primary where the honest answer is "unknown, go collect evidence".
    assert naive["verdicts"]["timing"] == F.value
    assert naive["primary_failure"] == "timing"
    real = verify_dependency_order(cert)
    assert real.primary_failures == ()


# ---------------------------------------------------------------------------
# The naive checker's bugs, demonstrated.
# ---------------------------------------------------------------------------
def test_naive_diagnoses_in_verification_order_not_execution_order():
    cert = aer_live9_certificate_f1()
    naive = naive_dependency_checker(cert)
    # The naive checker walks its verification order and stops at the
    # first FALSE: it names a single primary and never reports the
    # second independent root. The real verifier reports ALL roots.
    assert naive["primary_failure"] == "temporal"
    real = verify_dependency_order(cert)
    assert real.primary_failures == ("temporal", "budget")


def test_naive_collapses_undetermined_to_false():
    cert = aer_live9_certificate_f1()
    naive = naive_dependency_checker(cert)
    assert naive["verdicts"]["preservation"] == F.value
    assert naive["verdicts"]["exit"] == F.value
    real = verify_dependency_order(cert)
    iv = _verdicts(real)
    assert iv["preservation"].verdict == U.value
    assert iv["exit"].verdict == U.value


def test_spec_toposort_silently_wrong_on_cycles():
    cert = aer_live9_certificate_cyclic()
    order = _spec_topological_order(cert.invariants)
    pos = {n: i for i, n in enumerate(order)}
    violated = [(inv.name, pre)
                for inv in cert.invariants for pre in inv.prerequisites
                if not pos[pre] < pos[inv.name]]
    assert violated, "the spec's sort must violate prereq-first on a cycle"


# ---------------------------------------------------------------------------
# Cycles: joint invariants or rejection — never an invented ordering.
# ---------------------------------------------------------------------------
def test_cycle_without_joint_rejected_with_cycle_named():
    v = verify_dependency_order(aer_live9_certificate_cyclic())
    assert not v.accepted
    assert "cycle_a" in v.failure and "cycle_b" in v.failure


def test_find_cycle_names_the_path():
    prereq = {"cycle_a": ("cycle_b",), "cycle_b": ("cycle_a",)}
    cyc = find_cycle(prereq)
    assert cyc[0] == cyc[-1]
    assert set(cyc) == {"cycle_a", "cycle_b"}


def test_joint_cycle_deferred_not_ordered():
    v = verify_dependency_order(aer_live9_certificate_joint())
    assert v.accepted, v.failure
    iv = _verdicts(v)
    assert iv["cycle_a"].verdict == DEFERRED
    assert iv["cycle_b"].verdict == DEFERRED
    assert v.deferred_joints == ("joint_ab",)
    assert "cycle_a" not in v.verification_order
    # The downstream invariant blocked on the deferred joint is honestly
    # UNDETERMINED, not rejected.
    assert iv["downstream"].verdict == U.value


def test_spurious_joint_rejected():
    cert = aer_live9_certificate_f1()
    bad = DependencyCertificate(
        obligation_id=cert.obligation_id, boundary_ref=cert.boundary_ref,
        invariants=cert.invariants, execution_order=cert.execution_order,
        model=cert.model, witnesses=cert.witnesses,
        joint_invariants=(JointInvariant("spurious", ("obs", "budget")),),
        observations=cert.observations,
        model_assumptions=cert.model_assumptions)
    v = verify_dependency_order(bad)
    assert not v.accepted
    assert "spurious" in v.failure


# ---------------------------------------------------------------------------
# Evidence honesty: unsound TRUE, unproven FALSE, fabricated witnesses.
# ---------------------------------------------------------------------------
def test_unsound_true_rejected_with_prerequisite_named():
    cert = aer_live9_certificate_f1()
    invs = tuple(
        Invariant(i.name, i.prerequisites,
                  T if i.name == "lifecycle" else i.value,
                  "L-9: fabricated" if i.name == "lifecycle"
                  else i.proof_ref, i.layer)
        for i in cert.invariants)
    bad = DependencyCertificate(
        obligation_id=cert.obligation_id, boundary_ref=cert.boundary_ref,
        invariants=invs, execution_order=cert.execution_order,
        model=cert.model, witnesses=cert.witnesses,
        observations=cert.observations,
        model_assumptions=cert.model_assumptions)
    v = verify_dependency_order(bad)
    assert not v.accepted
    assert "lifecycle" in v.failure and "temporal" in v.failure


def test_unproven_false_rejected():
    cert = aer_live9_certificate_f6()
    invs = tuple(
        Invariant(i.name, i.prerequisites,
                  F if i.name == "budget" else i.value,
                  None if i.name == "budget" else i.proof_ref, i.layer)
        for i in cert.invariants)
    bad = DependencyCertificate(
        obligation_id=cert.obligation_id, boundary_ref=cert.boundary_ref,
        invariants=invs, execution_order=cert.execution_order,
        model=cert.model, witnesses=cert.witnesses,
        observations=cert.observations,
        model_assumptions=cert.model_assumptions)
    v = verify_dependency_order(bad)
    assert not v.accepted
    assert "budget" in v.failure


def test_fabricated_witness_on_undetermined_rejected():
    cert = aer_live9_certificate_f6()
    bad = DependencyCertificate(
        obligation_id=cert.obligation_id, boundary_ref=cert.boundary_ref,
        invariants=cert.invariants, execution_order=cert.execution_order,
        model=cert.model,
        witnesses=(Witness("timing", ("observe_sensor",)),),
        observations=cert.observations,
        model_assumptions=cert.model_assumptions)
    v = verify_dependency_order(bad)
    assert not v.accepted
    assert "timing" in v.failure


def test_bad_witness_kills_certificate_not_claim():
    """A failed witness kills the certificate; the invariant falls back
    to UNDETERMINED — the failed replay proves nothing about it."""
    cert = aer_live9_certificate_f1()
    bad = DependencyCertificate(
        obligation_id=cert.obligation_id, boundary_ref=cert.boundary_ref,
        invariants=cert.invariants, execution_order=cert.execution_order,
        model=cert.model,
        witnesses=(Witness("temporal", ("corrupt_evidence",)),
                   Witness("budget", ("drain_budget",))),
        observations=cert.observations,
        model_assumptions=cert.model_assumptions)
    v = verify_dependency_order(bad)
    assert not v.accepted
    assert "temporal" in v.failure
    iv = _verdicts(v)
    assert iv["temporal"].verdict == U.value
    assert iv["temporal"].witness_status.startswith("invalid:")
    # The untouched budget witness still verifies — the rot does not
    # spread past the failed witness's dependents.
    assert iv["budget"].verdict == F.value


def test_nonminimal_witness_rejected():
    cert = aer_live9_certificate_f1()
    bad = DependencyCertificate(
        obligation_id=cert.obligation_id, boundary_ref=cert.boundary_ref,
        invariants=cert.invariants, execution_order=cert.execution_order,
        model=cert.model,
        witnesses=(Witness("temporal",
                           ("observe_sensor", "advance_past_expiry")),
                   Witness("budget", ("drain_budget",))),
        observations=cert.observations,
        model_assumptions=cert.model_assumptions)
    v = verify_dependency_order(bad)
    assert not v.accepted
    assert "temporal" in v.failure
    assert "redundant" in v.failure


def test_mutation_true_with_witness_rejected():
    """Mutation control: flip a verdict to TRUE but leave its failure
    witness attached — the verifier must go red (fabrication)."""
    cert = aer_live9_certificate_f1()
    invs = tuple(
        Invariant(i.name, i.prerequisites,
                  T if i.name == "budget" else i.value,
                  "BUD-9: mutated" if i.name == "budget" else i.proof_ref,
                  i.layer)
        for i in cert.invariants)
    bad = DependencyCertificate(
        obligation_id=cert.obligation_id, boundary_ref=cert.boundary_ref,
        invariants=invs, execution_order=cert.execution_order,
        model=cert.model, witnesses=cert.witnesses,
        observations=cert.observations,
        model_assumptions=cert.model_assumptions)
    v = verify_dependency_order(bad)
    assert not v.accepted
    assert "budget" in v.failure


def test_layering_violation_rejected():
    # A backward layer edge that is NOT a cycle: timing [observation]
    # depending on budget [budget]. (Giving obs a temporal prerequisite
    # would also work structurally, but it creates a cycle — and the
    # verifier correctly rejects cycles before it ever reaches the
    # layering check.)
    cert = aer_live9_certificate_f1()
    invs = tuple(
        Invariant(i.name,
                  ("obs", "budget") if i.name == "timing"
                  else i.prerequisites,
                  i.value, i.proof_ref, i.layer)
        for i in cert.invariants)
    bad = DependencyCertificate(
        obligation_id=cert.obligation_id, boundary_ref=cert.boundary_ref,
        invariants=invs, execution_order=cert.execution_order,
        model=cert.model, witnesses=cert.witnesses,
        observations=cert.observations,
        model_assumptions=cert.model_assumptions)
    v = verify_dependency_order(bad)
    assert not v.accepted
    assert "layering" in v.failure


# ---------------------------------------------------------------------------
# Shape: malformed certificates fail closed before any proof is attempted.
# ---------------------------------------------------------------------------
def test_shape_duplicate_names():
    with pytest.raises(CertificateShapeError):
        DependencyCertificate(
            "o", "b",
            (Invariant("a", (), T, "p"), Invariant("a", (), U)),
            ("a",), (), (), observations=(),
            model_assumptions=_MODEL_ASSUMPTIONS)


def test_shape_unknown_prerequisite():
    with pytest.raises(CertificateShapeError):
        DependencyCertificate(
            "o", "b",
            (Invariant("a", ("ghost",), U),),
            ("a",), (), (), observations=(),
            model_assumptions=_MODEL_ASSUMPTIONS)


def test_shape_execution_order_must_be_permutation():
    with pytest.raises(CertificateShapeError):
        DependencyCertificate(
            "o", "b",
            (Invariant("a", (), U), Invariant("c", (), U)),
            ("a", "a"), (), (), observations=(),
            model_assumptions=_MODEL_ASSUMPTIONS)


def test_shape_self_prerequisite():
    with pytest.raises(CertificateShapeError):
        Invariant("a", ("a",), U)


def test_shape_empty_witness_steps():
    with pytest.raises(CertificateShapeError):
        Witness("a", ())


def test_shape_true_without_proof_ref():
    with pytest.raises(CertificateShapeError):
        Invariant("a", (), T, None)


# ---------------------------------------------------------------------------
# Cold verifier: bytes in, same verdict out; garbage fails closed.
# ---------------------------------------------------------------------------
def test_cold_verifier_roundtrip():
    cert = aer_live9_certificate_f1()
    raw = serialize_certificate(cert)
    v1 = verify_dependency_order(cert)
    v2 = independent_verify(raw)
    assert v2.accepted
    assert v2.primary_failures == v1.primary_failures
    assert v2.dependent_failures == v1.dependent_failures
    assert v2.certificate_fingerprint == v1.certificate_fingerprint
    assert v2.verification_order == v1.verification_order


def test_cold_verifier_malformed_bytes_fail_closed():
    with pytest.raises(CertificateSerializationError):
        independent_verify(b"not json at all")
    with pytest.raises(CertificateSerializationError):
        independent_verify(b'{"obligation_id": "x"}')


def test_fingerprint_deterministic():
    v1 = verify_dependency_order(aer_live9_certificate_f1())
    v2 = verify_dependency_order(aer_live9_certificate_f1())
    assert v1.certificate_fingerprint == v2.certificate_fingerprint
    assert len(v1.certificate_fingerprint) == 64


def test_transitive_prereqs():
    prereq = {"a": (), "b": ("a",), "c": ("b",)}
    assert transitive_prereqs("c", prereq) == {"a", "b"}
    assert transitive_prereqs("a", prereq) == set()

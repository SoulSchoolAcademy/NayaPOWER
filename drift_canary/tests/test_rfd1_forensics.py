"""RFD-1 forensics tests (SN-0790): failed refinement checks are
decomposed into independently testable obligations. No classification
without sufficient independent evidence; multiple defects stay
distinguishable; uncertainty is never converted into blame."""
import pytest

from drift_canary.revocation_linearization import (
    ABSTRACTION_DEFECT,
    MAPPING_DEFECT,
    TRANSACTION_ORDERING_DEFECT,
    CONCRETE_ENFORCEMENT_DEFECT,
    EXTERNAL_ASSUMPTION_GAP,
    INSUFFICIENT_OBSERVABILITY,
    DIAG_DIAGNOSED,
    DIAG_INCONCLUSIVE,
    DIAG_NO_FAILURE,
    FailureWitness,
    DiagnosticEvidence,
    Diagnosis,
    diagnose_refinement_failure,
    PLANTED_FIXTURES,
    run_blind_diagnosis,
    validate_repair_candidate,
    reference_spec_sha,
)


def _ev(**kw):
    base = dict(committed_events_reconstructible=True,
                commit_evidence_present=True)
    base.update(kw)
    return DiagnosticEvidence(**base)


def _w(*history):
    return FailureWitness(observed_history=tuple(history),
                          violated_obligation="test obligation")


# --- the decision procedure: ordering is diagnostic ----------------------------------
def test_observability_first():
    """Without independently reconstructible committed events, the only
    honest classification is INSUFFICIENT_OBSERVABILITY -- never blame."""
    d = diagnose_refinement_failure(
        _w("R(?)", "P(?)"),
        DiagnosticEvidence(committed_events_reconstructible=False,
                           commit_evidence_present=False,
                           forbidden_ordering_observed=True))
    assert d.primary == (INSUFFICIENT_OBSERVABILITY,)
    assert d.qualification_status == DIAG_INCONCLUSIVE
    # Even with ordering evidence: uncertainty is never converted to blame.
    assert TRANSACTION_ORDERING_DEFECT not in d.primary


def test_no_failure_when_legal_reconstruction_exists():
    """F7: an independent legal reconstruction means no established
    failure -- the rejection is the checker's, not the system's."""
    d = diagnose_refinement_failure(
        _w("R", "P(rejected by over-strict checker)"),
        _ev(legal_execution_reconstructible=True))
    assert d.primary == ()
    assert d.qualification_status == DIAG_NO_FAILURE


def test_enforcement_only_when_audits_justified():
    """CONCRETE_ENFORCEMENT_DEFECT requires justified audits; it narrows
    to TRANSACTION_ORDERING_DEFECT only on evidence."""
    # All audits clean, no ordering evidence -> generic enforcement defect.
    d = diagnose_refinement_failure(
        _w("op failed"),
        _ev(model_covers_behavior=True, state_mapping_correct=True,
            transition_mapping_correct=True))
    assert d.primary == (CONCRETE_ENFORCEMENT_DEFECT,)
    # Same + ordering evidence -> narrowed.
    d2 = diagnose_refinement_failure(
        _w("stale commit"),
        _ev(model_covers_behavior=True, state_mapping_correct=True,
            transition_mapping_correct=True, forbidden_ordering_observed=True))
    assert d2.primary == (TRANSACTION_ORDERING_DEFECT,)


def test_unresolved_audits_block_enforcement_conclusion():
    """Unassessed audits stay UNRESOLVED -- the procedure does not guess."""
    d = diagnose_refinement_failure(_w("op failed"), _ev())
    assert d.unresolved
    assert d.qualification_status == DIAG_INCONCLUSIVE
    assert CONCRETE_ENFORCEMENT_DEFECT not in d.primary


# --- F1-F8 blind diagnosis ------------------------------------------------------------------
def test_blind_diagnosis_all_fixtures():
    """The harness must catch false acceptance AND false rejection: every
    planted fixture classifies to its sealed cause and status."""
    results = run_blind_diagnosis()
    assert len(results) == 8
    failed = [r for r in results if not r["match"]]
    assert not failed, failed
    by_id = {r["fixture"]: r for r in results}
    # Spot-check the taxonomy's key distinctions.
    assert by_id["F1"]["diagnosed_primary"] == (ABSTRACTION_DEFECT,)
    assert by_id["F4"]["diagnosed_primary"] == (EXTERNAL_ASSUMPTION_GAP,)
    assert by_id["F5"]["diagnosed_status"] == DIAG_INCONCLUSIVE
    assert by_id["F7"]["diagnosed_status"] == DIAG_NO_FAILURE
    assert by_id["F8"]["diagnosed_primary"] == \
        by_id["F3"]["diagnosed_primary"]  # log-reorder stability


def test_f6_mixed_cause_preserved():
    """F6: both defects stay distinguishable -- primary keeps both,
    nothing collapsed."""
    by_id = {r["fixture"]: r for r in run_blind_diagnosis()}
    prim = set(by_id["F6"]["diagnosed_primary"])
    assert {TRANSACTION_ORDERING_DEFECT, EXTERNAL_ASSUMPTION_GAP} <= prim


def test_f1_contributing_distinguished():
    """F1: the external gap contributes but does not displace the
    abstraction defect as primary."""
    from drift_canary.revocation_linearization import _f1_evidence
    w, ev = _f1_evidence()
    d = diagnose_refinement_failure(w, ev)
    assert d.primary == (ABSTRACTION_DEFECT,)
    assert EXTERNAL_ASSUMPTION_GAP in d.contributing


def test_first_divergence_is_causal():
    """first_established_divergence is earliest in causal order."""
    d = diagnose_refinement_failure(
        _w("R committed", "stale P committed"),
        _ev(model_covers_behavior=True, state_mapping_correct=True,
            transition_mapping_correct=True, forbidden_ordering_observed=True))
    assert d.first_established_divergence == "R committed"


# --- the no-rewriting-the-proof-standard rule ---------------------------------------------------
def test_repair_candidate_never_auto_verified():
    """A plausible repair is PENDING_REVIEW, never VERIFIED -- and it is
    rejected if it weakens the law, breaks honest histories, or loses the
    original counterexample."""
    w = _w("stale commit")
    d = Diagnosis(w, "R", (TRANSACTION_ORDERING_DEFECT,), (), (),
                  DIAG_DIAGNOSED)
    assert validate_repair_candidate(d, "restore the guard", True, True) == \
        "REPAIR_PLAUSIBLE_PENDING_REVIEW"
    r = validate_repair_candidate(d, "restore the guard", False, True)
    assert r.startswith("REJECTED") and "honest history" in r
    r2 = validate_repair_candidate(d, "restore the guard", True, False)
    assert r2.startswith("REJECTED") and "counterexample" in r2


def test_witness_four_objects_distinct():
    """RFD-001: history -> obligation -> diagnosis -> repair are four
    distinct objects; the history is never overwritten."""
    w = FailureWitness(("R", "P"), "S1", "ordering defect", "restore guard")
    assert w.observed_history == ("R", "P")
    assert w.violated_obligation == "S1"
    assert w.causal_diagnosis == "ordering defect"
    assert w.proposed_repair == "restore guard"

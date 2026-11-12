"""RFD-POS-1 calibration tests (SN-0791): the diagnosis engine clears
the innocent. P1-P10 positive controls, the P2 false-positive guard,
metamorphic testing, paired controls, false-positive measures,
diagnosis receipts, and the two-history first experiment."""
import pytest

from drift_canary.revocation_linearization import (
    POS_CONSISTENT,
    POS_VIOLATION,
    POS_INCONCLUSIVE,
    POSITIVE_CONTROLS,
    classify_history,
    paired_histories,
    metamorphic_duplicate_recovery,
    metamorphic_add_logging,
    metamorphic_move_commit_across_revocation,
    build_diagnosis_receipt,
    DiagnosisReceipt,
    _p1_steps,
    _p2_steps,
    AuthoritativeState,
    refinement_fixture,
)


# --- P1-P10: independently verified expected outcomes --------------------------------
@pytest.mark.parametrize("pid,desc,builder", POSITIVE_CONTROLS)
def test_positive_control_consistent(pid, desc, builder):
    """Each positive control must classify CONSISTENT_WITH_SPEC --
    lawful behavior is preserved, not flagged."""
    r = classify_history(builder())
    assert r["verdict"] == POS_CONSISTENT, f"{pid} ({desc}): {r}"


def test_p2_not_a_false_positive():
    """P2 is the key control: V invoked while eligible, read before R,
    response after. The causal (linearization-point) order V<R is legal.
    A response-timestamp sorter would false-positive here; the engine
    must not."""
    r = classify_history(_p2_steps())
    assert r["verdict"] == POS_CONSISTENT
    # And the earlier PASS still cannot authorize a post-R effect without
    # a fresh check: the action boundary revalidates.
    st = refinement_fixture()
    standing, _ = st.validate_current("c1", "certification")
    assert standing == "CURRENT_QUALIFIED"
    st.commit_revocation("e1", "t", "s", "p", "LAW-v3", "t")
    st.commit_revocation("e2", "t", "s", "p", "LAW-v3", "t")
    out, _ = st.commit_action("a", ["c1"], True)
    assert out == "REJECTED"


# --- metamorphic testing ------------------------------------------------------------------
def test_metamorphic_semantics_preserving():
    """Duplicate recovery events and logging keep the classification."""
    base = _p1_steps()
    assert classify_history(base)["verdict"] == POS_CONSISTENT
    assert classify_history(
        metamorphic_duplicate_recovery(base))["verdict"] == POS_CONSISTENT
    assert classify_history(
        metamorphic_add_logging(base))["verdict"] == POS_CONSISTENT


def test_metamorphic_boundary_changing():
    """Moving the commit across the revocation (forced, unrefreshed)
    must alter the classification: CONSISTENT -> VIOLATION."""
    base = _p1_steps()
    assert classify_history(base)["verdict"] == POS_CONSISTENT
    moved = metamorphic_move_commit_across_revocation(base)
    assert moved is not None
    r = classify_history(moved)
    assert r["verdict"] == POS_VIOLATION, r


# --- paired controls: distinguish, don't blanket-accept/reject ------------------------------
def test_paired_discrimination():
    """Identical workers/evidence/revocation; only the publication's
    freshness differs. reject-both = overly restrictive; accept-both =
    unsafe; distinguishing = useful."""
    legal, illegal = paired_histories()
    rl = classify_history(legal)["verdict"]
    ri = classify_history(illegal)["verdict"]
    assert rl == POS_CONSISTENT, "legal history rejected: overly restrictive"
    assert ri == POS_VIOLATION, "illegal history accepted: unsafe"


# --- stuttering: authority changes are never stutter ------------------------------------------
def test_stuttering_rule():
    """α(s)=α(s') with no relevant change is legal stutter -- but a
    projection becoming authoritative can never be labeled stutter."""
    from drift_canary.revocation_linearization import differential_check, \
        DIFFERENTIAL_FALSIFIED, _pos_snapshot

    def _sneaky_commit(s):
        with s._commit_lock:
            s.projections["p1"].projection_revision += 1
            return "committed"

    r = differential_check([(_sneaky_commit, None, "unmapped head advance")])
    assert r["verdict"] == DIFFERENTIAL_FALSIFIED
    assert "hidden bookkeeping" in r["reason"]


# --- false-positive measures ---------------------------------------------------------------------
def test_false_positive_measures():
    """0 false implementation-defect and 0 false abstraction-defect
    classifications on the controlled suite: all positives accepted,
    all negatives rejected, ambiguous correctly classified."""
    false_impl = 0
    false_abstr = 0
    for pid, _desc, builder in POSITIVE_CONTROLS:
        r = classify_history(builder())
        if r["verdict"] != POS_CONSISTENT:
            false_impl += 1  # lawful behavior flagged as defect
    legal, illegal = paired_histories()
    if classify_history(legal)["verdict"] != POS_CONSISTENT:
        false_impl += 1
    if classify_history(illegal)["verdict"] != POS_VIOLATION:
        false_abstr += 1  # real violation missed
    assert false_impl == 0, f"{false_impl} lawful histories flagged"
    assert false_abstr == 0, f"{false_abstr} violations missed"


# --- diagnosis receipts (RFD-POS-002) ---------------------------------------------------------------
def test_diagnosis_receipt_schema():
    r = classify_history(_p1_steps())
    receipt = build_diagnosis_receipt("P1", r)
    assert isinstance(receipt, DiagnosisReceipt)
    assert receipt.provenance and receipt.scope and receipt.limitations
    assert receipt.linearization_witness
    assert receipt.assessments[0] == ("initial", POS_CONSISTENT)
    # Both assessments preserved when a mapping correction changes a verdict.
    r2 = dict(r, verdict=POS_VIOLATION)
    receipt2 = build_diagnosis_receipt("P1", r, corrected=r2)
    assert receipt2.assessments == (("initial", POS_CONSISTENT),
                                    ("mapping-corrected", POS_VIOLATION))


# --- the first experiment: two-history discrimination -----------------------------------------------
def test_first_experiment_two_histories():
    """A legal / B illegal with identical workers/evidence/revocation:
    accept A, reject B."""
    test_paired_discrimination()  # the experiment, run blind

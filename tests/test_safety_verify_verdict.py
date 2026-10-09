"""Safety falsifiers for the VERIFY-seam trust boundary.

The ACT seam promises "executor claims are NEVER trusted as verification":
only the VERIFY seam may close a receipt via apply_verify_verdict. That
promise is only as strong as the seam's enforcement. These tests falsify
the forgery vectors:

  1. Anonymous verdict — anyone closes a receipt with no verifier identity.
  2. Theater verdict — a verdict with junk evidence ("ok") counts as proof.
  3. Verdict shopping — close once as BLOCKED, then re-close as VERIFIED.

All three must FAIL CLOSED (ValueError, receipt stays open) for the seam
to hold. RED on pre-hardening code: every forgery above succeeds there.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.act_pipeline import (
    ActionPlan,
    LawAuthority,
    PlanCandidate,
)
from kernel.value_calculus import QualityProfile

NOW = 1_700_000_000.0


def _profile():
    return QualityProfile(profile_id="verify-test", version="1",
                          objective="minimum sufficient action")


def _authority():
    return LawAuthority(action="test.action", scope="test.action",
                        decided_at=NOW - 10, expires_at=NOW + 600,
                        grant_id="g-verify-1")


def _candidate():
    return PlanCandidate(
        candidate_id="c1", action="test.action", description="d",
        quality={"q": 8.0}, confidence={"q": 0.9},
        reversibility="REVERSIBLE", expected_outcome="expected",
        proof_requirements=("p1",), stakes="low",
    )


def _completed_receipt():
    plan = ActionPlan(plan_id="p1", action="test.action", chosen=_candidate(),
                      authority=_authority(), candidate_scores=(("c1", 8.0),),
                      planned_at=NOW)
    return ap.execute_plan(
        plan, executor=lambda p: "observed x",
        re_resolve=lambda: _authority(), now=NOW,
        profile=_profile(),
    )


def test_anonymous_verdict_is_refused():
    """No verifier identity -> the verdict is not a VERIFY-seam verdict."""
    receipt = _completed_receipt()
    with pytest.raises(ValueError):
        ap.apply_verify_verdict(receipt, verified=True,
                                evidence="verify-seam observed x matches expected",
                                verifier_id="")
    with pytest.raises(ValueError):
        ap.apply_verify_verdict(receipt, verified=True,
                                evidence="verify-seam observed x matches expected",
                                verifier_id="   ")
    assert receipt.outcome_verified is False
    assert receipt.truth_state == "UNKNOWN"


def test_theater_evidence_is_refused():
    """Junk evidence ('ok') must not close a receipt as verified proof."""
    receipt = _completed_receipt()
    with pytest.raises(ValueError):
        ap.apply_verify_verdict(receipt, verified=True, evidence="ok",
                                verifier_id="verify-seam/run-7")
    with pytest.raises(ValueError):
        ap.apply_verify_verdict(receipt, verified=True, evidence="looks good",
                                verifier_id="verify-seam/run-7")
    assert receipt.outcome_verified is False


def test_verdict_shopping_is_refused():
    """A receipt closed once cannot be re-closed to flip the verdict."""
    receipt = _completed_receipt()
    closed = ap.apply_verify_verdict(
        receipt, verified=False,
        evidence="verify-seam found observed x diverges from expected",
        verifier_id="verify-seam/run-7")
    assert closed.truth_state == "BLOCKED"
    with pytest.raises(ValueError):
        ap.apply_verify_verdict(
            closed, verified=True,
            evidence="second verifier disagrees and wants VERIFIED",
            verifier_id="verify-seam/run-8")
    assert closed.outcome_verified is False
    assert closed.truth_state == "BLOCKED"


def test_bound_verdict_closes_and_records_verifier():
    """Happy path: identified verifier + substantive evidence closes."""
    receipt = _completed_receipt()
    closed = ap.apply_verify_verdict(
        receipt, verified=True,
        evidence="verify-seam independently observed x; matches expected",
        verifier_id="verify-seam/run-7")
    assert closed.outcome_verified is True
    assert closed.truth_state == "VERIFIED"
    assert closed.receipt_id == receipt.receipt_id
    assert any("verify-seam/run-7" in e for e in closed.evidence)


def test_negative_verdict_needs_substance_too():
    """A BLOCKED verdict with junk evidence is still theater — refused."""
    receipt = _completed_receipt()
    with pytest.raises(ValueError):
        ap.apply_verify_verdict(receipt, verified=False, evidence="nope",
                                verifier_id="verify-seam/run-7")
    assert receipt.truth_state == "UNKNOWN"


def test_wrong_phase_still_refused():
    plan = ActionPlan(plan_id="p1", action="test.action", chosen=_candidate(),
                      authority=_authority(), candidate_scores=(("c1", 8.0),),
                      planned_at=NOW)
    refused_plan, receipt = ap.plan_action(_authority(), [], _profile(), now=NOW)
    assert receipt.phase == "PLAN_REFUSED"
    with pytest.raises(ValueError):
        ap.apply_verify_verdict(
            receipt, verified=True,
            evidence="substantive evidence but wrong phase entirely",
            verifier_id="verify-seam/run-7")

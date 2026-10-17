"""Claim-level truth separation tests.

Shawn's extension: "One contaminated claim must not automatically
invalidate an entire lesson. One valid claim must not make its
contaminated neighbors trustworthy."

Ratified: "Truth belongs to individual claims and their evidence.
Preservation belongs to the original intelligence object. Authority
belongs to LAW."
"""
import sys

import pytest

sys.path.insert(0, "/tmp/errdef-branch/error_defense")
from claims import (
    CANDIDATE, CONFLICTED, ELIGIBLE, QUARANTINED, REFUTED, RESTRICTED,
    REVIEW_REQUIRED, UNKNOWN, VERIFIED,
    REQUIRES, SUPPORTS, DERIVED_FROM, CONTRADICTS,
    ClaimDependency, ClaimRecord,
    atomize, check_claim_use, classify, filter_summary_claims,
    project_lesson, propagate_contamination,
)


def _h(s):
    import hashlib
    return hashlib.sha256(s.encode()).hexdigest()


def _eligible_claim(cid, text="claim text", scope=("s1",)):
    return ClaimRecord(claim_id=cid, parent_note_id="NOTE-1",
                       source_content_hash=_h("note"), claim_text=text,
                       scope=scope, verdict=VERIFIED, eligibility=ELIGIBLE,
                       reason="independently verified")


# --- ATOMIZE -------------------------------------------------------------------

def test_atomize_splits_preserves_scope():
    claims = atomize("NOTE-1", _h("note"), [
        ("Deploy after CI is green", "procedural", ("deploy",)),
        ("Never deploy on Fridays", "normative", ("deploy",)),
    ])
    assert len(claims) == 2
    assert claims[0].claim_id == "NOTE-1#C01"
    assert claims[0].scope == ("deploy",)
    # unevaluated claims are never eligible by default
    assert all(c.verdict == UNKNOWN and c.eligibility == REVIEW_REQUIRED for c in claims)


def test_atomize_refuses_empty_claim():
    with pytest.raises(ValueError, match="atomize_empty_claim"):
        atomize("NOTE-1", _h("note"), [("  ", "factual", ())])


def test_atomize_keeps_negation_inside_claim():
    claims = atomize("NOTE-1", _h("note"), [("Do NOT restart the service", "procedural", ("ops",))])
    assert "NOT" in claims[0].claim_text  # negation not factored out


# --- THE MIXED-VALIDITY FIXTURE ---------------------------------------------------
# 9 valid + 1 false claim in one lesson -> 9 stay eligible, 1 contained.

def _mixed_lesson():
    claims = {}
    for i in range(1, 10):
        cid = f"NOTE-M#C{i:02d}"
        claims[cid] = ClaimRecord(
            claim_id=cid, parent_note_id="NOTE-M", source_content_hash=_h("note"),
            claim_text=f"valid claim {i}", scope=("s1",),
            verdict=VERIFIED, eligibility=ELIGIBLE, reason="independently verified",
            independent_evidence_refs=(f"EV-{i}",))
    # the one false claim
    claims["NOTE-M#C10"] = ClaimRecord(
        claim_id="NOTE-M#C10", parent_note_id="NOTE-M", source_content_hash=_h("note"),
        claim_text="false claim: skip verification", scope=("s1",),
        verdict=REFUTED, eligibility=QUARANTINED, reason="refuted by trial")
    return claims


def test_mixed_validity_nine_eligible_one_contained():
    claims = _mixed_lesson()
    projected = project_lesson("LESSON-M", "NOTE-M", claims, use="act")
    assert len(projected.claims) == 9
    assert len(projected.excluded) == 1
    assert projected.excluded[0][0] == "NOTE-M#C10"
    assert projected.excluded[0][1] == QUARANTINED
    # the valid claims are untouched by their contaminated neighbor
    assert all(c.eligibility == ELIGIBLE for c in projected.claims)


def test_contaminated_neighbor_does_not_gain_trust():
    """One valid claim must not make its contaminated neighbors trustworthy:
    the quarantined claim stays quarantined even surrounded by 9 eligible."""
    claims = _mixed_lesson()
    bad = claims["NOTE-M#C10"]
    allowed, reason = check_claim_use(bad, "act")
    assert allowed is False
    assert reason == "quarantined_claim_blocked_at_use"


# --- Contamination propagation (material only) --------------------------------------

def test_requires_propagates_without_independent_evidence():
    a = ClaimRecord("A", "N", _h("n"), "base", verdict=REFUTED, eligibility=QUARANTINED,
                    reason="refuted")
    b = ClaimRecord("B", "N", _h("n"), "depends", verdict=VERIFIED, eligibility=ELIGIBLE,
                    reason="was eligible",
                    dependencies=(ClaimDependency(REQUIRES, "A"),))
    out = propagate_contamination({"A": a, "B": b})
    assert out["B"].eligibility == QUARANTINED
    assert "material_dependency_contaminated:A" in out["B"].reason


def test_independent_evidence_recalculates_instead_of_condemning():
    """B REQUIRES A (contaminated) but is independently supported by X:
    recalculate via X — don't mechanically mark false."""
    a = ClaimRecord("A", "N", _h("n"), "base", verdict=REFUTED, eligibility=QUARANTINED,
                    reason="refuted")
    b = ClaimRecord("B", "N", _h("n"), "depends", verdict=VERIFIED, eligibility=ELIGIBLE,
                    reason="was eligible",
                    dependencies=(ClaimDependency(REQUIRES, "A"),),
                    independent_evidence_refs=("EV-X",))
    out = propagate_contamination({"A": a, "B": b})
    assert out["B"].eligibility == REVIEW_REQUIRED  # recalculate, not condemn
    assert out["B"].verdict == VERIFIED  # verdict preserved; eligibility gated
    assert "recalculate_via_independent_evidence" in out["B"].reason


def test_supports_does_not_propagate():
    a = ClaimRecord("A", "N", _h("n"), "base", verdict=REFUTED, eligibility=QUARANTINED,
                    reason="refuted")
    b = ClaimRecord("B", "N", _h("n"), "supported", verdict=VERIFIED, eligibility=ELIGIBLE,
                    reason="was eligible",
                    dependencies=(ClaimDependency(SUPPORTS, "A"),))
    out = propagate_contamination({"A": a, "B": b})
    assert out["B"].eligibility == ELIGIBLE  # SUPPORTS is not material


def test_cycle_refused():
    a = ClaimRecord("A", "N", _h("n"), "a", dependencies=(ClaimDependency(REQUIRES, "B"),))
    b = ClaimRecord("B", "N", _h("n"), "b", dependencies=(ClaimDependency(REQUIRES, "A"),))
    with pytest.raises(ValueError, match="contamination_cycle_refused"):
        propagate_contamination({"A": a, "B": b})


def test_originals_untouched_preservation():
    a = ClaimRecord("A", "N", _h("n"), "base", verdict=REFUTED, eligibility=QUARANTINED,
                    reason="refuted")
    b = ClaimRecord("B", "N", _h("n"), "depends", verdict=VERIFIED, eligibility=ELIGIBLE,
                    reason="was eligible",
                    dependencies=(ClaimDependency(REQUIRES, "A"),))
    original_b = b.eligibility
    propagate_contamination({"A": a, "B": b})
    assert b.eligibility == original_b  # input map not mutated


# --- Point-of-use gate ------------------------------------------------------------------

def test_verified_but_restricted_outside_scope():
    """A VERIFIED claim can still be RESTRICTED outside its proven scope."""
    c = ClaimRecord("C1", "N", _h("n"), "verified claim", scope=("s1",),
                    verdict=VERIFIED, eligibility=RESTRICTED,
                    reason="verified for s1 only")
    ok_in, _ = check_claim_use(c, "act")
    assert ok_in is False  # act is consequential; scope s1 not asserted here
    ok_read, _ = check_claim_use(c, "read")
    assert ok_read is True


def test_summary_never_reintroduces_quarantined():
    claims = list(_mixed_lesson().values())
    shown = filter_summary_claims(claims, use="read")
    shown_ids = [c.claim_id for c in shown]
    assert "NOTE-M#C10" not in shown_ids
    assert len(shown) == 9


def test_unknown_eligibility_fail_closed():
    c = ClaimRecord("C1", "N", _h("n"), "x")
    # bypass __post_init__ guard via object.__new__ to simulate corrupt state
    bad = object.__new__(ClaimRecord)
    object.__setattr__(bad, "eligibility", "BOGUS")
    allowed, reason = check_claim_use(bad, "act")
    assert allowed is False and reason == "unknown_eligibility_fail_closed"

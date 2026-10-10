"""Ten adversarial tests for the reopening protocol.

Each test encodes one required behavior from Shawn's framework. All run in
sandbox; no production touch; no network.
"""

import pytest

from reopening.objects import (
    capture_source, Interpretation, InterpretationSet,
    new_interpretation_version, issue_resolution, assess_applicability,
)
from reopening.review import (
    Review, Challenge, transition, admit_challenge,
    determine_containment, requalify,
    RESOLVED, CHALLENGED, REOPENED, REQUALIFIED, UNRESOLVED,
    ADMITTED, DUPLICATE, INSUFFICIENT,
    CONTINUE, RESTRICT_DEPENDENT, SUSPEND,
    UPHELD, REPLACED, NARROWED, NO_SINGLE,
    ReviewError,
)
from reopening.triggers import REGISTRY, validate_trigger_evidence, CONTRADICTORY_EVIDENCE
from reopening.policy import PolicyVersion, PolicyRegistry, policy_transition_effect
from reopening.challenges import (
    make_challenge, derive_challenge_id, ChallengeRegistry,
    issue_reopening_receipt,
)
from reopening.descendants import (
    DependencyEdge, trace_impact,
    HISTORICAL_CITE, MATERIAL_DEPENDENT, INDEPENDENTLY_SUPPORTED,
)


TS = "2026-10-10T18:00:00+00:00"


def _source():
    return capture_source("SN-001", "verification complete", "naya-2", TS)


def _iset(source_id="SN-001"):
    return InterpretationSet(
        set_id="AMB-001", source_id=source_id, version=1,
        interpretations=[
            Interpretation("I-1", "local automated tests passed",
                           ["EVID-001"], "ci-pipeline", "naya-2"),
            Interpretation("I-2", "independent verification completed",
                           [], "ci-pipeline", "naya-2"),
        ],
        created_at=TS, created_by="naya-2",
    )


def _resolved():
    s = _iset()
    r = issue_resolution("RES-001", s, "I-1", "only I-1 has evidence",
                         TS, "v1", "P1", "EVID-001", "ci-pipeline", "naya-1")
    return s, r


# ---------------------------------------------------------------------------
# 1. Genuine contradictory evidence arrives -> reopens affected resolution
# ---------------------------------------------------------------------------
def test_1_contradictory_evidence_reopens():
    s, receipt = _resolved()
    review = Review("RV-1", "AMB-001", resolution_receipt_id="RES-001")
    ch = make_challenge("coda-1", CONTRADICTORY_EVIDENCE,
                        ("EVID-024", "INDEP-ATTEST-9"), "AMB-001",
                        "I-1's evidence was the test's own log", TS)
    ok, missing = validate_trigger_evidence(ch.trigger_type,
                                            {"contradicting_evidence_ref": "EVID-024",
                                             "independence_attestation": "INDEP-ATTEST-9"})
    assert ok and not missing
    assert admit_challenge(ch, set()) == ADMITTED
    transition(review, CHALLENGED, "contradictory evidence admitted")
    transition(review, REOPENED, "threshold met: independent contradiction")
    assert review.state == REOPENED


# ---------------------------------------------------------------------------
# 2. Duplicate evidence arrives -> no duplicate review
# ---------------------------------------------------------------------------
def test_2_duplicate_challenge_deduplicated():
    reg = ChallengeRegistry()
    ch1 = make_challenge("coda-1", CONTRADICTORY_EVIDENCE, ("EVID-024",),
                         "AMB-001", None, TS)
    ch2 = make_challenge("coda-1", CONTRADICTORY_EVIDENCE, ("EVID-024",),
                         "AMB-001", None, TS)
    assert ch1.challenge_id == ch2.challenge_id  # content-derived
    assert reg.register(ch1, "RV-1") == "REGISTERED"
    assert reg.register(ch2, "RV-1") == "DUPLICATE"
    assert admit_challenge(ch2, reg.seen) == DUPLICATE


# ---------------------------------------------------------------------------
# 3. Weak unsupported objection -> recorded, no restriction
# ---------------------------------------------------------------------------
def test_3_weak_objection_records_without_restricting():
    ch = make_challenge("", CONTRADICTORY_EVIDENCE, (), "AMB-001", None, TS)
    assert admit_challenge(ch, set()) == INSUFFICIENT  # no challenger, no evidence
    # even an admitted-but-harmless challenge continues low-risk use
    assert determine_containment(ch, material_harm_plausible=False,
                                 sole_authority_premise=False) == CONTINUE


# ---------------------------------------------------------------------------
# 4. Source author clarifies -> re-evaluates with attributable evidence
# ---------------------------------------------------------------------------
def test_4_source_correction_reevaluates():
    src = _source()
    corrected = capture_source("SN-002",
                               "verification complete (local tests only)",
                               "naya-2", TS, corrects_id="SN-001")
    assert corrected.corrects_id == "SN-001"
    assert src.content_hash != corrected.content_hash  # original untouched
    # correction is attributable evidence for a SOURCE_CORRECTION challenge
    ch = make_challenge("naya-2", "SOURCE_CORRECTION", ("SN-002", "naya-2"),
                        "AMB-001", None, TS)
    ok, _ = validate_trigger_evidence(
        ch.trigger_type,
        {"correction_record_ref": "SN-002", "author_attribution": "naya-2"})
    assert ok
    assert admit_challenge(ch, set()) == ADMITTED


# ---------------------------------------------------------------------------
# 5. P1 -> P2: history preserved, current applicability reassessed
# ---------------------------------------------------------------------------
def test_5_policy_change_preserves_history():
    s, receipt = _resolved()
    assert receipt.policy_version == "P1"
    reg = PolicyRegistry([PolicyVersion("P1", TS, "shawn", "baseline"),
                          PolicyVersion("P2", TS, "shawn",
                                        "independent verification required")])
    assert policy_transition_effect(reg.get("P1"), reg.get("P2"), "P1") \
        == "REASSESS_APPLICABILITY"
    a = assess_applicability("A-1", receipt, "promote-lesson", TS, "P2")
    assert not a.eligible  # current use withheld...
    assert "P1" in a.reason  # ...but the P1 receipt itself is untouched
    assert receipt.policy_version == "P1"  # immutable, still says P1


# ---------------------------------------------------------------------------
# 6. Extraction omitted a negation -> reconstruct and correct
# ---------------------------------------------------------------------------
def test_6_extraction_defect_reconstructs():
    ch = make_challenge("extraction-coord", "EXTRACTION_DEFECT",
                        ("SN-001:span-3",), "AMB-001",
                        "negation 'not' dropped from 'did not establish'", TS)
    ok, _ = validate_trigger_evidence(
        ch.trigger_type,
        {"original_span_ref": "SN-001:span-3",
         "defect_description": "negation dropped"})
    assert ok
    review = Review("RV-6", "AMB-001", resolution_receipt_id="RES-001")
    transition(review, CHALLENGED, "extraction defect admitted")
    transition(review, REOPENED, "reconstruction required")
    # re-extraction produces a corrected interpretation version
    s = _iset()
    v2 = new_interpretation_version(
        s, [Interpretation("I-3", "local tests passed; production NOT established",
                           ["SN-001:span-3"], "ci-pipeline", "extraction-coord")],
        TS, "extraction-coord")
    assert v2.version == 2 and v2.supersedes_version == 1
    assert s.version == 1  # original version preserved


# ---------------------------------------------------------------------------
# 7. Independent descendant -> independently qualified use preserved
# ---------------------------------------------------------------------------
def test_7_independent_descendant_preserved():
    edges = [DependencyEdge("LESSON-B", "I-1", "SUPPORTS", is_sole_basis=False)]
    impact = trace_impact("LESSON-B", edges, "I-1", has_independent_support=True)
    assert impact.classification == INDEPENDENTLY_SUPPORTED
    assert impact.action == "REASSESS"  # recalculate via own evidence, not condemned


# ---------------------------------------------------------------------------
# 8. Sole-dependent descendant -> restricted pending review
# ---------------------------------------------------------------------------
def test_8_sole_dependent_restricted():
    edges = [DependencyEdge("LESSON-C", "I-1", "REQUIRES", is_sole_basis=True)]
    impact = trace_impact("LESSON-C", edges, "I-1", has_independent_support=False)
    assert impact.classification == MATERIAL_DEPENDENT
    assert impact.action == "RESTRICT_PENDING_REVIEW"


# ---------------------------------------------------------------------------
# 9. Stale successor at the auth boundary -> rejected
# ---------------------------------------------------------------------------
def test_9_stale_resolution_rejected_at_boundary():
    s, receipt = _resolved()  # resolved under P1
    # successor attempts a consequential action under P2 with the P1 receipt
    a = assess_applicability("A-9", receipt, "production-write", TS, "P2")
    assert not a.eligible
    assert any("P2" in r for r in a.restrictions)


# ---------------------------------------------------------------------------
# 10. Independent review upholds -> eligibility restored with new receipt
# ---------------------------------------------------------------------------
def test_10_upheld_meaning_restores_with_new_receipt():
    s, receipt = _resolved()
    review = Review("RV-10", "AMB-001", resolution_receipt_id="RES-001")
    transition(review, CHALLENGED, "challenge admitted")
    transition(review, REOPENED, "threshold met")
    review, new_receipt = requalify(
        review, s, UPHELD, "I-1",
        "independent re-evaluation confirms I-1", TS,
        "v1", "P1", "EVID-001+EVID-030", "ci-pipeline", "coda-1")
    assert review.state == REQUALIFIED
    assert new_receipt.supersedes_receipt_id == "RES-001"
    assert receipt.receipt_id == "RES-001"  # prior receipt untouched


# ---------------------------------------------------------------------------
# Machine invariants
# ---------------------------------------------------------------------------
def test_illegal_transition_raises():
    review = Review("RV-X", "AMB-001")
    with pytest.raises(ReviewError):
        transition(review, REQUALIFIED, "shortcut attempt")  # CHALLENGED required first


def test_challenge_alone_changes_nothing():
    review = Review("RV-Y", "AMB-001", resolution_receipt_id="RES-001")
    transition(review, CHALLENGED, "admitted")
    assert review.containment == "NONE"  # eligibility untouched by challenge alone


def test_unresolved_holds_consequential_use():
    s, receipt = _resolved()
    review = Review("RV-Z", "AMB-001", resolution_receipt_id="RES-001")
    transition(review, CHALLENGED, "admitted")
    transition(review, REOPENED, "threshold met")
    review, new_receipt = requalify(
        review, s, NO_SINGLE, None, "evidence split", TS,
        "v1", "P1", "EVID-001", "ci-pipeline", "coda-1")
    assert review.state == UNRESOLVED
    assert new_receipt is None
    # UNRESOLVED can return to REOPENED on new evidence — never silently RESOLVED
    transition(review, REOPENED, "new evidence arrived")
    assert review.state == REOPENED
    with pytest.raises(ReviewError):
        transition(review, RESOLVED, "silent close attempt")

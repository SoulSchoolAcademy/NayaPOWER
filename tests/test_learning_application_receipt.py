"""Behavioral tests for the convergence-D application-receipt instrument.

These tests exercise the actual seam D guards: the retrieval -> application
binding is E2's witness, and an outcome is only E3 evidence when an
independent verifier (distinct from the applier) attests it. The seam tests
run this module's outputs through the merged ladder's REAL _transition_e2 /
_transition_e3 predicates -- if the instrument cannot earn what it claims,
the ladder falsifies it.
"""

import copy

import pytest

from tools.learning_application_receipt import (
    FORBIDDEN_AUTHORITY_FIELDS,
    OUTCOME_SCHEMA,
    RETRIEVAL_SCHEMA,
    SCHEMA,
    attach_to_lineage_bundle,
    emit_application_receipt,
    emit_outcome_record,
    emit_retrieval_receipt,
    link_outcome,
    qualifies_for_e2,
    qualifies_for_e3,
    summarize_application_receipt,
    validate_application_receipt,
    validate_outcome_record,
    validate_retrieval_receipt,
)
from tools.learning_evidence_ladder import _TRANSITIONS


TS = "2026-10-08T09:50:00Z"


def _retrieval(**over):
    kw = dict(
        lesson_id="L-T11",
        retriever="naya-5",
        retrieved_at=TS,
        query_context="apply reserve rule to checkout task",
        lesson_content_sha="sha256:abc123",
        source_refs=["cog-event-1", "ib-row-7"],
    )
    kw.update(over)
    return emit_retrieval_receipt(**kw)


def _application(retrieval_ref, **over):
    kw = dict(
        lesson_id="L-T11",
        retrieval_ref=retrieval_ref,
        task_ref="task-checkout-042",
        applier="naya-5",
        applied_at="2026-10-08T10:00:00Z",
        applicability={"relevance_rationale": "reserve rule governs checkout idempotency",
                       "task_match": "direct"},
    )
    kw.update(over)
    return emit_application_receipt(**kw)


def _outcome(app_id, **over):
    kw = dict(
        application_receipt_id=app_id,
        lesson_id="L-T11",
        task_ref="task-checkout-042",
        measured_effect="duplicate charges 3/100 -> 0/100",
        observed_at="2026-10-08T11:00:00Z",
        outcome_ref="exec-receipt-99",
    )
    kw.update(over)
    return emit_outcome_record(**kw)


# --- retrieval receipts -------------------------------------------------------

def test_retrieval_receipt_emits_valid_and_deterministic():
    r1 = _retrieval()
    r2 = _retrieval()
    assert r1["schema"] == RETRIEVAL_SCHEMA
    assert r1["receipt_id"] == r2["receipt_id"]  # replay-safe: same inputs, same id
    assert r1["receipt_id"].startswith("RET-")
    verdict = validate_retrieval_receipt(r1)
    assert verdict["valid"], verdict["codes"]


def test_retrieval_receipt_rejects_forbidden_authority_field():
    # emit's signature is fixed, so forbidden keys can only enter by manual
    # construction -- the validate seam must fail them closed (the #1712 law).
    r = _retrieval()
    assert r["authority_refs"] == []  # links-only field present, grant absent
    r["grant_id"] = "G-1"
    verdict = validate_retrieval_receipt(r)
    assert not verdict["valid"]
    assert any("FORBIDDEN_AUTHORITY_FIELD" in c for c in verdict["codes"])


def test_retrieval_receipt_idempotency_mismatch_detected():
    r = _retrieval()
    r["retriever"] = "naya-4"  # tamper after emit
    verdict = validate_retrieval_receipt(r)
    assert not verdict["valid"]
    assert any("IDEMPOTENCY_MISMATCH" in c for c in verdict["codes"])


# --- application receipts -----------------------------------------------------

def test_application_receipt_emits_valid_with_ladder_e2_fields():
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    assert app["schema"] == SCHEMA
    assert app["receipt_id"].startswith("APP-")
    verdict = validate_application_receipt(app, retrieval_receipt=ret)
    assert verdict["valid"], verdict["codes"]
    assert verdict["e2_eligible"] is True
    assert qualifies_for_e2(app) is True


def test_application_receipt_binding_broken_when_ref_mismatches():
    ret = _retrieval()
    app = _application("RET-wrongref0000000000000000000000")
    verdict = validate_application_receipt(app, retrieval_receipt=ret)
    assert not verdict["valid"]
    assert any("RETRIEVAL_BINDING_BROKEN" in c for c in verdict["codes"])
    assert verdict["e2_eligible"] is False


def test_application_receipt_binding_broken_when_lesson_mismatches():
    ret = _retrieval(lesson_id="L-OTHER")
    app = _application(ret["receipt_id"])  # receipt is L-T11, retrieval is L-OTHER
    verdict = validate_application_receipt(app, retrieval_receipt=ret)
    assert any("RETRIEVAL_BINDING_BROKEN" in c for c in verdict["codes"])


def test_application_receipt_missing_required_field_fails_closed():
    ret = _retrieval()
    with pytest.raises(ValueError):
        emit_application_receipt("L-T11", ret["receipt_id"], "", "naya-5", TS)
    app = _application(ret["receipt_id"])
    del app["applier"]
    verdict = validate_application_receipt(app)
    assert not verdict["valid"]
    assert any("MISSING_REQUIRED_FIELD: applier" in c for c in verdict["codes"])


def test_application_receipt_rejects_forbidden_authority_field():
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    app["authorized"] = True
    verdict = validate_application_receipt(app)
    assert not verdict["valid"]
    assert any("FORBIDDEN_AUTHORITY_FIELD" in c for c in verdict["codes"])


def test_receipt_carries_no_authority_granting_surface():
    """The #1712 lesson: no function here may resolve an authority decision."""
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    for receipt in (ret, app):
        assert not (FORBIDDEN_AUTHORITY_FIELDS & set(receipt.keys()))
        assert "authorized" not in receipt
    assert summarize_application_receipt(app).startswith("application APP-")


# --- outcome records + independent verification ---------------------------------

def test_outcome_record_emits_valid():
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    out = _outcome(app["receipt_id"])
    assert out["schema"] == OUTCOME_SCHEMA
    verdict = validate_outcome_record(out, applier="naya-5")
    assert verdict["valid"], verdict["codes"]


def test_link_outcome_appends_without_changing_receipt_id():
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    out = _outcome(app["receipt_id"])
    before = app["receipt_id"]
    linked = link_outcome(app, out)
    assert linked["receipt_id"] == before  # idempotent across phases
    assert linked["outcome_ref"] == out["record_id"]
    assert app["outcome_ref"] is None  # input not mutated
    # relinking is stable
    assert link_outcome(linked, out)["receipt_id"] == before


def test_link_outcome_fails_closed_on_mismatch():
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    out = _outcome("APP-wrong0000000000000000000000000000")
    with pytest.raises(ValueError, match="OUTCOME_LINK_MISMATCH"):
        link_outcome(app, out)


def test_self_attested_verification_fails_closed():
    """Verifier == applier is executor-owned observation, never E3 evidence."""
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    out = _outcome(app["receipt_id"], independent_verification={
        "verifier": "naya-5", "verified_at": "2026-10-08T12:00:00Z",
        "method": "self-review", "verdict": "PASS",
    })
    verdict = validate_outcome_record(out, applier="naya-5")
    assert not verdict["valid"]
    assert any("SELF_ATTESTED_VERIFICATION" in c for c in verdict["codes"])
    assert qualifies_for_e3(app, out) is False
    assert verdict["has_independent_verification"] is False


def test_unmeasured_outcome_is_not_evidence():
    # measured_effect is required at emit; audit path: strip it after emit
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    out = emit_outcome_record(app["receipt_id"], "L-T11", "task-checkout-042",
                              "x", "2026-10-08T11:00:00Z")
    out = copy.deepcopy(out)
    out["measured_effect"] = ""
    verdict = validate_outcome_record(out, applier="naya-5")
    assert any("OUTCOME_UNMEASURED" in c for c in verdict["codes"])
    assert qualifies_for_e3(app, out) is False


def test_outcome_without_independent_verification_is_executor_owned():
    """Applier-attested outcome: honestly recorded, E2-eligible, never E3."""
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    out = _outcome(app["receipt_id"])  # no independent_verification
    verdict = validate_outcome_record(out, applier="naya-5")
    assert verdict["valid"]  # executor-owned observation is still a valid record
    assert verdict["has_independent_verification"] is False
    assert qualifies_for_e3(app, out) is False
    assert validate_application_receipt(app)["e2_eligible"] is True


# --- seam tests: the real ladder predicates judge this instrument ---------------

def test_seam_emitted_receipts_earn_e2_and_e3_on_the_real_ladder():
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    out = _outcome(app["receipt_id"], independent_verification={
        "verifier": "naya-1", "verified_at": "2026-10-08T12:00:00Z",
        "method": "independent arm replay", "verdict": "CONFIRMED",
    })
    ev = {"application_receipt": app, "outcome": out, "_producer_id": "naya-5"}
    ok2, msg2 = _TRANSITIONS["E2_CAN_DO"](ev)
    ok3, msg3 = _TRANSITIONS["E3_INDEPENDENT"](ev)
    assert ok2, msg2
    assert ok3, msg3


def test_seam_self_attested_outcome_fails_e3_on_the_real_ladder():
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    out = _outcome(app["receipt_id"], independent_verification={
        "verifier": "naya-5", "verified_at": "2026-10-08T12:00:00Z",
    })
    ev = {"application_receipt": app, "outcome": out, "_producer_id": "naya-5"}
    ok3, msg3 = _TRANSITIONS["E3_INDEPENDENT"](ev)
    assert not ok3
    assert "executor-owned observation" in msg3


def test_seam_unmeasured_outcome_fails_e3_on_the_real_ladder():
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    out = _outcome(app["receipt_id"], independent_verification={
        "verifier": "naya-1", "verified_at": "2026-10-08T12:00:00Z",
    })
    out = copy.deepcopy(out)
    out["measured_effect"] = ""
    ev = {"application_receipt": app, "outcome": out, "_producer_id": "naya-5"}
    ok3, msg3 = _TRANSITIONS["E3_INDEPENDENT"](ev)
    assert not ok3
    assert "no measured_effect" in msg3


# --- lineage bundle adapter -----------------------------------------------------

def test_attach_to_lineage_bundle_contract():
    ret = _retrieval()
    app = _application(ret["receipt_id"])
    bundle = {"learning": {"id": "L-T11"}}
    out = attach_to_lineage_bundle(bundle, retrieval_receipt=ret,
                                   application_receipt=app)
    assert out["retrieval_receipts"] == [ret]
    assert out["application_receipts"] == [app]
    assert "retrieval_receipts" not in bundle  # input not mutated
    # appending a second receipt accumulates
    out2 = attach_to_lineage_bundle(out, application_receipt=_application(ret["receipt_id"], task_ref="task-B"))
    assert len(out2["application_receipts"]) == 2

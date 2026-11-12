"""Behavioral tests for the receipt-driven evidence assembler (convergence C).

These tests prove the seam the assembler closes: E0-E7 advancement driven
by REAL instrument output, not hand-built fixtures. The advancement test
runs the REAL B reconstructor (tools/learning_lineage_receipt.reconstruct)
and the REAL ladder evaluator (tools/learning_evidence_ladder.evaluate)
end to end, with D-shaped receipts emitted by a contract mirror of D's
emitter (Learning-team PR #1882, not on main yet -- same mirror precedent
as tests/test_lineage_receipt_evidence_consumption.py).

Fail-closed behaviors under test:
  - E0 -> E1 -> E2 -> E3 advancement as evidence accumulates (snapshots)
  - E3 -> E4 -> E5 -> E6 -> E7 advancement through the assembled path
  - tampered application receipt (digest stale)  -> excluded, E2 unproven
  - outcome verified by the applier              -> E3 unproven (self-attestation)
  - comprehension verified by the producer       -> E1 unproven (self-attestation)
  - application naming an unknown retrieval       -> excluded (manufactured)
  - receipt carrying a grant field                -> excluded (#1712)
  - transfer repeating the application task       -> E4 unproven (anti-memorization)
  - successor == applier or == producer           -> E5 unproven (not cold)
  - mastery below two verifiers/domains, or conflicts -> E7 unproven / FALSIFIED
  - evidence going stale                          -> REGRESSED flagged, never silent
  - mirror digest vectors pinned                  -> drift guard for the D merge
  - malformed input                               -> unproven, never an exception
"""

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from learning_evidence_assembler import (  # noqa: E402
    advance,
    assemble_evidence,
    verify_d_receipts,
    _mirror_digest_id,
)

LESSON = "learn-conv-c-001"
PRODUCER = "naya-5"
APPLIER = "naya-5"

RET_SCHEMA = "NAYANET_LEARNING_RETRIEVAL_RECEIPT_V1"
APP_SCHEMA = "NAYANET_LEARNING_APPLICATION_RECEIPT_V1"
OUT_SCHEMA = "NAYANET_LEARNING_OUTCOME_RECORD_V1"


# ---------------------------------------------------------------------------
# D-contract emitter mirror (drift guard: must match D's emitter exactly)
# ---------------------------------------------------------------------------

def _digest(prefix: str, core: dict) -> str:
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return "%s-%s" % (prefix,
                       hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32])


def _emit_retrieval(**over) -> dict:
    core = {
        "schema": RET_SCHEMA,
        "lesson_id": LESSON,
        "retriever": "cold-retrieve-probe",
        "retrieved_at": "2026-10-09T09:00:00Z",
        "query_context": "convergence drill",
        "lesson_content_sha": "sha-vec-1",
    }
    core.update(over)
    receipt = dict(core)
    receipt["receipt_id"] = _digest("RET", core)
    receipt["kind"] = "retrieval"
    receipt["source_refs"] = []
    receipt["authority_refs"] = []
    return receipt


def _emit_application(retrieval_ref: str, **over) -> dict:
    core = {
        "schema": APP_SCHEMA,
        "lesson_id": LESSON,
        "retrieval_ref": retrieval_ref,
        "task_ref": "task-A",
        "applier": APPLIER,
        "applied_at": "2026-10-09T09:30:00Z",
    }
    core.update(over)
    receipt = dict(core)
    receipt["receipt_id"] = _digest("APP", core)
    receipt["kind"] = "application"
    receipt["applicability"] = {"relevance_rationale": "direct match"}
    receipt["outcome_ref"] = None
    receipt["authority_refs"] = []
    return receipt


def _emit_outcome(application_receipt_id: str, verifier: str, **over) -> dict:
    core = {
        "schema": OUT_SCHEMA,
        "application_receipt_id": application_receipt_id,
        "lesson_id": LESSON,
        "task_ref": "task-A",
        "measured_effect": "+12% accuracy",
        "observed_at": "2026-10-09T10:00:00Z",
    }
    core.update(over)
    record = dict(core)
    record["record_id"] = _digest("OUT", core)
    record["kind"] = "outcome"
    record["outcome_ref"] = "exec-1"
    record["independent_verification"] = {
        "verifier": verifier,
        "verified_at": "2026-10-09T10:30:00Z",
    }
    return record


def _bundle(**over) -> dict:
    b = {
        "learning": {
            "id": LESSON,
            "status": "CANDIDATE",
            "observed_value": {
                "source_event_id": "evt-1",
                "commit_receipt_id": "commit-1",
                "intelligent_block_id": "IB-CONV-C-1",
            },
        },
        "cognition_event": {"id": "evt-1",
                            "created_at": "2026-10-09T09:00:00Z"},
        "commit_receipt": {"id": "commit-1", "action": "intelligence_commit"},
        "intelligent_block": {"intelligent_block_id": "IB-CONV-C-1",
                              "understanding_state": "E0"},
        "retrieval_receipts": [],
        "application_receipts": [],
        "outcome_records": [],
    }
    b.update(over)
    return b


def _comprehension(verifier: str = "naya-1") -> dict:
    return {
        "control_receipt": "cr-1",
        "treatment_receipt": "tr-1",
        "independent_verifier": verifier,
        "verified_at": "2026-10-09T09:15:00Z",
    }


# ---------------------------------------------------------------------------
# advancement: E0 -> E1 -> E2 -> E3 on real instruments
# ---------------------------------------------------------------------------

def test_advancement_e0_to_e3_on_real_instruments():
    ret = _emit_retrieval()
    app = _emit_application(ret["receipt_id"])
    out = _emit_outcome(app["receipt_id"], verifier="naya-2")

    snapshots = [
        {"lineage_bundle": _bundle()},                                    # E0
        {"lineage_bundle": _bundle(),
         "comprehension": _comprehension()},                              # E1
        {"lineage_bundle": _bundle(
            retrieval_receipts=[ret], application_receipts=[app]),
         "comprehension": _comprehension()},                              # E2
        {"lineage_bundle": _bundle(
            retrieval_receipts=[ret], application_receipts=[app],
            outcome_records=[out]),
         "comprehension": _comprehension()},                              # E3
    ]
    result = advance(LESSON, "E3_INDEPENDENT", snapshots,
                     producer_id=PRODUCER)

    earned = [t["earned_level"] for t in result["trajectory"]]
    assert earned == ["E0_EXPOSED", "E1_UNDERSTANDS", "E2_CAN_DO",
                      "E3_INDEPENDENT"], earned

    kinds = [t["kind"] for t in result["transitions"]]
    assert kinds == ["ADVANCED", "ADVANCED", "ADVANCED"], kinds
    assert result["transitions"][0] == {
        "at_index": 1, "kind": "ADVANCED",
        "from": "E0_EXPOSED", "to": "E1_UNDERSTANDS"}
    assert result["regressions"] == []

    # The claim is rejected until the evidence earns it, then accepted.
    verdicts = [t["verdict"] for t in result["trajectory"]]
    assert verdicts[:3] == ["REJECTED", "REJECTED", "REJECTED"], verdicts
    assert verdicts[3] == "ACCEPTED", verdicts
    assert result["final_earned_level"] == "E3_INDEPENDENT"
    assert result["final_verdict"] == "ACCEPTED"


def test_assembly_reports_real_verification_counts():
    ret = _emit_retrieval()
    app = _emit_application(ret["receipt_id"])
    assembled = assemble_evidence(
        LESSON, _bundle(retrieval_receipts=[ret],
                        application_receipts=[app]))
    assert assembled["schema"] == "NAYANET_LEARNING_EVIDENCE_ASSEMBLY_V1"
    assert assembled["verified_counts"] == {
        "retrievals": 1, "applications": 1, "outcomes": 0}
    assert assembled["evidence"]["capture_receipt"] == {
        "intelligent_block_id": "IB-CONV-C-1",
        "captured_at": "2026-10-09T09:00:00Z"}
    assert assembled["evidence"]["application_receipt"]["applier"] == APPLIER


# ---------------------------------------------------------------------------
# fail-closed: tampered, self-attested, manufactured, authority-carrying
# ---------------------------------------------------------------------------

def test_tampered_application_receipt_halts_advancement_at_e1():
    ret = _emit_retrieval()
    app = _emit_application(ret["receipt_id"])
    tampered = dict(app)
    tampered["task_ref"] = "task-EVIL"  # core changed, receipt_id now stale

    snapshots = [
        {"lineage_bundle": _bundle(), "comprehension": _comprehension()},
        {"lineage_bundle": _bundle(
            retrieval_receipts=[ret], application_receipts=[tampered]),
         "comprehension": _comprehension()},
    ]
    result = advance(LESSON, "E3_INDEPENDENT", snapshots,
                     producer_id=PRODUCER)
    earned = [t["earned_level"] for t in result["trajectory"]]
    assert earned == ["E1_UNDERSTANDS", "E1_UNDERSTANDS"], earned
    assert [t["kind"] for t in result["transitions"]] == ["HELD"]

    assembled = assemble_evidence(
        LESSON, _bundle(retrieval_receipts=[ret],
                        application_receipts=[tampered]),
        comprehension=_comprehension())
    assert any("IDEMPOTENCY_MISMATCH" in c
               for c in assembled["receipt_audit_codes"])
    assert "application_receipt" not in assembled["evidence"]


def test_self_attested_outcome_blocks_e3():
    ret = _emit_retrieval()
    app = _emit_application(ret["receipt_id"])
    out = _emit_outcome(app["receipt_id"], verifier=APPLIER)  # == applier

    assembled = assemble_evidence(
        LESSON,
        _bundle(retrieval_receipts=[ret], application_receipts=[app],
                outcome_records=[out]),
        comprehension=_comprehension())
    result = advance(
        LESSON, "E3_INDEPENDENT",
        [{"lineage_bundle": _bundle(
            retrieval_receipts=[ret], application_receipts=[app],
            outcome_records=[out]),
          "comprehension": _comprehension()}],
        producer_id=PRODUCER)
    assert result["final_earned_level"] == "E2_CAN_DO"
    # the outcome IS assembled (executor observation) but E3 stays unproven
    assert "outcome" in assembled["evidence"]


def test_manufactured_application_without_retrieval_is_excluded():
    fake = _emit_application("RET-does-not-exist")
    verified = verify_d_receipts(
        _bundle(application_receipts=[fake]))
    assert verified["valid_applications"] == {}
    assert any("RETRIEVAL_BINDING_BROKEN" in c
               for c in verified["codes"])

    result = advance(
        LESSON, "E2_CAN_DO",
        [{"lineage_bundle": _bundle(application_receipts=[fake]),
          "comprehension": _comprehension()}],
        producer_id=PRODUCER)
    assert result["final_earned_level"] == "E1_UNDERSTANDS"


def test_receipt_carrying_grant_field_is_excluded():
    ret = _emit_retrieval()
    bad = dict(ret)
    bad["grant"] = "self-issued"  # the #1712 defect shape
    verified = verify_d_receipts(_bundle(retrieval_receipts=[bad]))
    assert verified["valid_retrievals"] == {}
    assert any("FORBIDDEN_AUTHORITY_FIELD" in c for c in verified["codes"])


def test_stale_evidence_flags_regression_never_silently():
    ret = _emit_retrieval()
    app = _emit_application(ret["receipt_id"])
    good_snap = {
        "lineage_bundle": _bundle(
            retrieval_receipts=[ret], application_receipts=[app]),
        "comprehension": _comprehension(),
    }
    stale_snap = dict(good_snap)
    stale_snap["stale"] = True
    result = advance(LESSON, "E2_CAN_DO", [good_snap, stale_snap],
                     producer_id=PRODUCER)
    earned = [t["earned_level"] for t in result["trajectory"]]
    assert earned == ["E2_CAN_DO", "E1_UNDERSTANDS"], earned
    assert len(result["regressions"]) == 1
    reg = result["regressions"][0]
    assert reg["kind"] == "REGRESSED"
    assert reg["from"] == "E2_CAN_DO" and reg["to"] == "E1_UNDERSTANDS"
    assert reg["reason"], "regression must name its reason"


# ---------------------------------------------------------------------------
# drift guard + robustness
# ---------------------------------------------------------------------------

def test_mirror_digest_matches_pinned_vectors():
    r_core = {"schema": RET_SCHEMA, "lesson_id": "VEC-1", "retriever": "vec",
              "retrieved_at": "2026-10-09T00:00:00Z", "query_context": "",
              "lesson_content_sha": ""}
    a_core = {"schema": APP_SCHEMA, "lesson_id": "VEC-1",
              "retrieval_ref": "RET-x", "task_ref": "task-A",
              "applier": "naya-5", "applied_at": "2026-10-09T01:00:00Z"}
    o_core = {"schema": OUT_SCHEMA, "application_receipt_id": "APP-x",
              "lesson_id": "VEC-1", "task_ref": "task-A",
              "measured_effect": "+1%", "observed_at": "2026-10-09T02:00:00Z"}
    assert _mirror_digest_id("retrieval", r_core) == \
        "RET-4ba4275d4bf60f1c3b31fc625fb36bfc"
    assert _mirror_digest_id("application", a_core) == \
        "APP-1d3491d8d0d3335ff25718ebf45604c1"
    assert _mirror_digest_id("outcome", o_core) == \
        "OUT-71023113b93300ae4abe997e6788552d"


def test_malformed_input_is_unproven_never_an_exception():
    assembled = assemble_evidence("L", None)
    assert assembled["evidence"] == {}
    assembled2 = assemble_evidence("L", {"learning": "not-a-dict"})
    assert assembled2["evidence"] == {}
    result = advance("L", "E3_INDEPENDENT", [None, "junk", {}],
                     producer_id=PRODUCER)
    assert result["final_earned_level"] == "UNPROVEN"
    assert result["final_verdict"] == "UNPROVEN"


def test_missing_capture_stage_is_unproven_not_e0():
    # Bundle with no capture rows: B marks capture GAP; the assembler must
    # not manufacture E0.
    b = _bundle()
    del b["cognition_event"]
    del b["commit_receipt"]
    assembled = assemble_evidence(LESSON, b)
    assert "capture_receipt" not in assembled["evidence"]
    result = advance(LESSON, "E1_UNDERSTANDS",
                     [{"lineage_bundle": b}], producer_id=PRODUCER)
    assert result["final_earned_level"] == "UNPROVEN"


# ---------------------------------------------------------------------------
# top rung: E4 -> E5 -> E6 -> E7 through the assembled-evidence path
# ---------------------------------------------------------------------------

def _e3_snap(**over) -> dict:
    """One snapshot with the full E3 evidence chain already assembled."""
    ret = _emit_retrieval()
    app = _emit_application(ret["receipt_id"])
    out = _emit_outcome(app["receipt_id"], verifier="naya-2")
    snap = {
        "lineage_bundle": _bundle(
            retrieval_receipts=[ret], application_receipts=[app],
            outcome_records=[out]),
        "comprehension": _comprehension(),
    }
    snap.update(over)
    return snap


def _transfer(task_ref: str = "task-B", verifier: str = "naya-2") -> dict:
    return {
        "task_ref": task_ref,
        "measured_effect": "+9% on held-out task",
        "independent_verification": {"verifier": verifier,
                                    "verified_at": "2026-10-09T11:00:00Z"},
    }


def _successor(successor_id: str = "naya-6", verifier: str = "coda-1") -> dict:
    return {
        "successor_id": successor_id,
        "task_ref": "task-C",
        "independent_verification": {"verifier": verifier,
                                    "verified_at": "2026-10-09T12:00:00Z"},
    }


def test_advancement_e3_to_e7_on_assembled_evidence():
    transfer = [_transfer()]
    successor = [_successor()]
    retention = {"revalidated_at": "2026-10-09T13:00:00Z",
                 "revalidation_receipt": "ret-1"}
    mastery = {"distinct_verifiers": 2, "distinct_transfer_domains": 2}
    snapshots = [
        _e3_snap(),
        _e3_snap(transfer=transfer),
        _e3_snap(transfer=transfer, successor_use=successor),
        _e3_snap(transfer=transfer, successor_use=successor,
                 retention=retention),
        _e3_snap(transfer=transfer, successor_use=successor,
                 retention=retention, mastery=mastery),
    ]
    result = advance(LESSON, "E7_MASTERED", snapshots,
                     producer_id=PRODUCER)

    earned = [t["earned_level"] for t in result["trajectory"]]
    assert earned == ["E3_INDEPENDENT", "E4_TRANSFER", "E5_CAN_TEACH",
                      "E6_RETAINED", "E7_MASTERED"], earned

    kinds = [t["kind"] for t in result["transitions"]]
    assert kinds == ["ADVANCED"] * 4, kinds
    assert result["regressions"] == []

    # The E7 claim is rejected until the whole chain earns it, then accepted.
    verdicts = [t["verdict"] for t in result["trajectory"]]
    assert verdicts[:4] == ["REJECTED"] * 4, verdicts
    assert verdicts[4] == "ACCEPTED", verdicts
    assert result["final_earned_level"] == "E7_MASTERED"
    assert result["final_verdict"] == "ACCEPTED"


def test_transfer_on_same_task_is_not_transfer():
    # Repeating the application's own task is memorization, not transfer.
    snap = _e3_snap(transfer=[_transfer(task_ref="task-A")])
    result = advance(LESSON, "E4_TRANSFER", [snap],
                     producer_id=PRODUCER)
    assert result["final_earned_level"] == "E3_INDEPENDENT"


def test_transfer_without_measured_effect_or_verifier_is_not_transfer():
    snap = _e3_snap(transfer=[{"task_ref": "task-B"}])
    result = advance(LESSON, "E4_TRANSFER", [snap],
                     producer_id=PRODUCER)
    assert result["final_earned_level"] == "E3_INDEPENDENT"


def test_successor_same_as_applier_is_not_cold():
    snap = _e3_snap(transfer=[_transfer()],
                    successor_use=[_successor(successor_id=APPLIER)])
    result = advance(LESSON, "E5_CAN_TEACH", [snap],
                     producer_id=PRODUCER)
    assert result["final_earned_level"] == "E4_TRANSFER"


def test_successor_same_as_producer_is_not_cold():
    snap = _e3_snap(transfer=[_transfer()],
                    successor_use=[_successor(successor_id=PRODUCER)])
    result = advance(LESSON, "E5_CAN_TEACH", [snap],
                     producer_id=PRODUCER)
    assert result["final_earned_level"] == "E4_TRANSFER"


def test_e7_requires_two_verifiers_and_two_domains():
    snap = _e3_snap(
        transfer=[_transfer()],
        successor_use=[_successor()],
        retention={"revalidated_at": "2026-10-09T13:00:00Z",
                   "revalidation_receipt": "ret-1"},
        mastery={"distinct_verifiers": 1, "distinct_transfer_domains": 2})
    result = advance(LESSON, "E7_MASTERED", [snap],
                     producer_id=PRODUCER)
    assert result["final_earned_level"] == "E6_RETAINED"


def test_conflicts_collapse_the_chain_to_e0():
    snap = _e3_snap(
        transfer=[_transfer()],
        successor_use=[_successor()],
        retention={"revalidated_at": "2026-10-09T13:00:00Z",
                   "revalidation_receipt": "ret-1"},
        mastery={"distinct_verifiers": 2, "distinct_transfer_domains": 2},
        conflicts=True)
    result = advance(LESSON, "E7_MASTERED", [snap],
                     producer_id=PRODUCER)
    assert result["final_earned_level"] == "E0_EXPOSED"
    assert result["final_verdict"] == "FALSIFIED"


def test_comprehension_verified_by_producer_blocks_e1():
    # The producer self-attestation guard (ladder's _producer_id injection)
    # must be LIVE through the assembler path, not silently disabled.
    snap = _e3_snap(comprehension=_comprehension(verifier=PRODUCER))
    result = advance(LESSON, "E3_INDEPENDENT", [snap],
                     producer_id=PRODUCER)
    assert result["final_earned_level"] == "E0_EXPOSED"
    assert result["final_verdict"] == "REJECTED"

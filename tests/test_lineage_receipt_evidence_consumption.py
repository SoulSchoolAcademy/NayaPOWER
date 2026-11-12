"""Machine-falsifiable tests for the B+D convergence consumer wiring.

Exercises the REAL reconstructor (tools/learning_lineage_receipt.py) with
convergence-item-D-shaped receipts attached under the
attach_to_lineage_bundle() contract keys ("retrieval_receipts",
"application_receipts", "outcome_records").

The _retrieval / _application / _outcome helpers replicate D's emitter
digest contract exactly (sha256 of canonical JSON of the apply-time core,
first 32 hex, RET-/APP-/OUT- prefix). They are a contract COPY, not an
import, because D's module is not on main yet (Learning-team PR #1882).
If the emitter ever drifts from this contract, these tests fail -- that
drift is the seam being guarded.

Fail-closed contract under test:
  - full valid chain            -> 4 evidence stages PRESENT
  - tampered core field         -> GAP naming INTEGRITY_FAILED, BROKEN
  - dangling retrieval_ref      -> GAP naming APPLICATION_RETRIEVAL_LINK_BROKEN
  - outcome lesson mismatch     -> GAP naming OUTCOME_LESSON_MISMATCH
  - no receipts attached        -> UNINSTRUMENTED (behavior preserved)
  - application without rationale -> applicability PENDING, never PRESENT
  - malformed evidence keys     -> GAP, never crash
"""

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from learning_lineage_receipt import (
    APPLICATION_SCHEMA,
    OUTCOME_SCHEMA,
    RETRIEVAL_SCHEMA,
    STAGES,
    reconstruct,
)

LESSON = "learn-001"


def _digest(prefix: str, core: dict) -> str:
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "%s-%s" % (prefix, hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32])


def _retrieval(lesson_id: str = LESSON, **over) -> dict:
    core = {
        "schema": RETRIEVAL_SCHEMA,
        "lesson_id": lesson_id,
        "retriever": "naya5-test",
        "retrieved_at": "2026-10-08T21:50:00Z",
        "query_context": "cold retrieve probe",
        "lesson_content_sha": "sha-abc123",
    }
    core.update(over)
    receipt = dict(core)
    receipt["receipt_id"] = _digest("RET", core)
    receipt["kind"] = "retrieval"
    receipt["source_refs"] = []
    receipt["authority_refs"] = []
    return receipt


def _application(lesson_id: str, retrieval_ref: str, applicability: dict | None = None, **over) -> dict:
    core = {
        "schema": APPLICATION_SCHEMA,
        "lesson_id": lesson_id,
        "retrieval_ref": retrieval_ref,
        "task_ref": "task-1",
        "applier": "worker-7",
        "applied_at": "2026-10-08T21:51:00Z",
    }
    core.update(over)
    receipt = dict(core)
    receipt["receipt_id"] = _digest("APP", core)
    receipt["kind"] = "application"
    receipt["applicability"] = dict(applicability or {})
    receipt["outcome_ref"] = None
    receipt["authority_refs"] = []
    return receipt


def _outcome(lesson_id: str, application_receipt_id: str, iv: dict | None = None, **over) -> dict:
    core = {
        "schema": OUTCOME_SCHEMA,
        "application_receipt_id": application_receipt_id,
        "lesson_id": lesson_id,
        "task_ref": "task-1",
        "measured_effect": "latency -12%",
        "observed_at": "2026-10-08T21:52:00Z",
    }
    core.update(over)
    record = dict(core)
    record["record_id"] = _digest("OUT", core)
    record["kind"] = "outcome"
    record["outcome_ref"] = ""
    record["independent_verification"] = dict(iv or {})
    return record


def _candidate_bundle(**overrides) -> dict:
    """Honest candidate chain: capture/retention links resolve, no gaps."""
    bundle = {
        "cognition_event": {"id": "evt-001", "event_id": "EVT-001"},
        "commit_receipt": {"id": "rcpt-001", "action": "intelligence_commit"},
        "intelligent_block": {
            "intelligent_block_id": "IB-LEARN-001",
            "understanding_state": "CANDIDATE",
            "evidence_refs": [],
            "provenance": {},
        },
        "learning": {
            "id": LESSON,
            "status": "CANDIDATE",
            "level": "E1_UNDERSTANDS",
            "target_id": "NAYA-NODE-0001",
            "verification_method": "pending",
            "observed_value": {
                "intelligent_block_id": "IB-LEARN-001",
                "source_event_id": "evt-001",
                "source_event_key": "EVT-001",
                "commit_receipt_id": "rcpt-001",
                "lineage_id": "lin-001",
                "relationship_id": "rel-001",
                "index_id": "idx-001",
                "checkpoint_id": "chk-001",
            },
        },
        "relationship": {"relationship_id": "rel-001"},
        "checkpoint": {"id": "chk-001"},
    }
    bundle.update(overrides)
    return bundle


def _full_evidence_bundle(iv: dict | None = None, applicability: dict | None = None):
    ret = _retrieval()
    app = _application(LESSON, ret["receipt_id"],
                       applicability={"relevance_rationale": "task matches lesson pattern",
                                      "task_match": "high"} if applicability is None else applicability)
    out = _outcome(LESSON, app["receipt_id"], iv={"verifier": "coda-1",
                                                 "verified_at": "2026-10-08T22:00:00Z"} if iv is None else iv)
    bundle = _candidate_bundle(
        retrieval_receipts=[ret],
        application_receipts=[app],
        outcome_records=[out],
    )
    return bundle, ret, app, out


def test_full_evidence_chain_resolves_four_stages():
    bundle, ret, app, out = _full_evidence_bundle()
    receipt = reconstruct(bundle)
    assert receipt["gaps"] == [], receipt["gaps"]
    for stage in ("retrieval", "applicability", "application", "outcome"):
        assert receipt["stages"][stage]["status"] == "PRESENT", (stage, receipt["stages"][stage])
    assert receipt["stages"]["retrieval"]["refs"]["receipt_ids"] == [ret["receipt_id"]]
    assert receipt["stages"]["outcome"]["refs"]["independent_verifiers"] == ["coda-1"]
    assert any("retrieval_receipt" in l and ret["receipt_id"] in l for l in receipt["links_verified"])
    assert any("outcome_record" in l and out["record_id"] in l for l in receipt["links_verified"])
    # Only the three successor stages remain uninstrumented; verification still PENDING -> PARTIAL.
    assert len(receipt["uninstrumented"]) == 3, receipt["uninstrumented"]
    assert receipt["verdict"] == "PARTIAL"
    assert set(receipt["stages"].keys()) == set(STAGES)


def test_tampered_retrieval_receipt_fails_closed():
    bundle, ret, app, out = _full_evidence_bundle()
    bundle["retrieval_receipts"][0]["lesson_content_sha"] = "sha-TAMPERED"
    receipt = reconstruct(bundle)
    assert receipt["verdict"] == "BROKEN"
    assert any("RETRIEVAL_INTEGRITY_FAILED" in g for g in receipt["gaps"]), receipt["gaps"]
    assert receipt["stages"]["retrieval"]["status"] == "GAP"
    # The downstream links fail closed too: no valid retrieval -> application cannot resolve.
    assert any("APPLICATION_RETRIEVAL_LINK_BROKEN" in g for g in receipt["gaps"])
    assert receipt["stages"]["application"]["status"] == "GAP"


def test_dangling_application_retrieval_ref_fails_closed():
    app = _application(LESSON, "RET-deadbeefdeadbeefdeadbeefdeadbeef",
                       applicability={"relevance_rationale": "x"})
    receipt = reconstruct(_candidate_bundle(application_receipts=[app]))
    assert receipt["verdict"] == "BROKEN"
    assert any("APPLICATION_RETRIEVAL_LINK_BROKEN" in g for g in receipt["gaps"]), receipt["gaps"]
    assert receipt["stages"]["application"]["status"] == "GAP"
    # Retrieval had no evidence attached -> stays honestly UNINSTRUMENTED.
    assert receipt["stages"]["retrieval"]["status"] == "UNINSTRUMENTED"


def test_outcome_lesson_mismatch_fails_closed():
    bundle, ret, app, out = _full_evidence_bundle()
    bad_out = _outcome("learn-999", app["receipt_id"])  # digest valid, lesson wrong
    bundle["outcome_records"] = [bad_out]
    receipt = reconstruct(bundle)
    assert receipt["verdict"] == "BROKEN"
    assert any("OUTCOME_LESSON_MISMATCH" in g for g in receipt["gaps"]), receipt["gaps"]
    assert receipt["stages"]["outcome"]["status"] == "GAP"
    # Unaffected stages stay honest.
    assert receipt["stages"]["retrieval"]["status"] == "PRESENT"
    assert receipt["stages"]["application"]["status"] == "PRESENT"


def test_outcome_application_link_mismatch_fails_closed():
    bundle, ret, app, out = _full_evidence_bundle()
    bad_out = _outcome(LESSON, "APP-deadbeefdeadbeefdeadbeefdeadbeef")
    bundle["outcome_records"] = [bad_out]
    receipt = reconstruct(bundle)
    assert receipt["verdict"] == "BROKEN"
    assert any("OUTCOME_APPLICATION_LINK_BROKEN" in g for g in receipt["gaps"]), receipt["gaps"]
    assert receipt["stages"]["outcome"]["status"] == "GAP"


def test_absent_receipts_preserve_uninstrumented_behavior():
    receipt = reconstruct(_candidate_bundle())
    for stage in ("retrieval", "applicability", "application", "outcome"):
        assert receipt["stages"][stage]["status"] == "UNINSTRUMENTED"
    assert len(receipt["uninstrumented"]) == 7
    assert receipt["verdict"] == "PARTIAL"
    assert receipt["gaps"] == []


def test_applicability_pending_without_rationale_never_present():
    bundle, ret, app, out = _full_evidence_bundle(applicability={})
    receipt = reconstruct(bundle)
    assert receipt["stages"]["applicability"]["status"] == "PENDING"
    assert receipt["stages"]["application"]["status"] == "PRESENT"  # application itself unaffected
    assert receipt["verdict"] == "PARTIAL"


def test_wrong_schema_rejected():
    ret = _retrieval()
    ret["schema"] = "BOGUS_SCHEMA"
    receipt = reconstruct(_candidate_bundle(retrieval_receipts=[ret]))
    assert receipt["verdict"] == "BROKEN"
    assert any("RETRIEVAL_SCHEMA_MISMATCH" in g for g in receipt["gaps"]), receipt["gaps"]
    assert receipt["stages"]["retrieval"]["status"] == "GAP"


def test_non_dict_evidence_entry_fails_closed():
    receipt = reconstruct(_candidate_bundle(retrieval_receipts=[42]))
    assert receipt["verdict"] == "BROKEN"
    assert any("RETRIEVAL_ENTRY_NOT_OBJECT" in g for g in receipt["gaps"]), receipt["gaps"]


def test_evidence_key_not_list_fails_closed():
    receipt = reconstruct(_candidate_bundle(retrieval_receipts="not-a-list"))
    assert receipt["verdict"] == "BROKEN"
    assert any("EVIDENCE_KEY_NOT_LIST" in g for g in receipt["gaps"]), receipt["gaps"]


def test_outcome_without_independent_verifier_has_no_verifier_ref():
    bundle, ret, app, out = _full_evidence_bundle(iv={})
    receipt = reconstruct(bundle)
    assert receipt["stages"]["outcome"]["status"] == "PRESENT"
    assert "independent_verifiers" not in receipt["stages"]["outcome"]["refs"]
    # Independence judgment stays the ladder's (E3) seam, not the lineage's.
    assert receipt["verdict"] == "PARTIAL"

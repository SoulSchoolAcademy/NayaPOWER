"""Seam tests: the normal retrieval path emits durable receipts (convergence (c)).

Before this wiring, tools/learning_application_receipt.py's emitters were
pure and tested but NEVER CALLED in production -- applicability.filter_entries
(the read every seat runs through) emitted zero receipts. These tests run the
real filter_entries through the wiring module and assert:

  1. one retrieval receipt per KEPT entry (filtered-out entries emit none)
  2. every receipt is schema-valid per the instrument's own validators
  3. receipt_id is deterministic from the apply-time core (replay safety)
  4. the wired chain earns E2 (retrieval -> application) and E3 (independent
     verification) on the ladder's REAL predicates
  5. self-attestation earns E2 but NOT E3
  6. persistence failure NEVER withholds the retrieved entries (evidence,
     never authority -- the #1712 law)
  7. forbidden authority fields are refused at emit time
"""
import json
from pathlib import Path

import pytest

from tools.learning_application_receipt import (
    FORBIDDEN_AUTHORITY_FIELDS,
    emit_retrieval_receipt,
    validate_retrieval_receipt,
)
from tools.learning_evidence_ladder import _TRANSITIONS
from tools.learning_receipt_wiring import (
    record_application,
    record_outcome,
    retrieve_with_receipts,
)

TS = "2026-10-22T02:45:00Z"

ENTRIES = [
    {"smart_note_id": "SN-0815", "title": "A Lesson Isn't Learned Until Behavior Changes",
     "category": "LEARNING", "topic": "COMPOUNDING_INTELLIGENCE", "subtopic": "",
     "keywords": ["lesson", "behavior change"]},
    {"smart_note_id": "SN-0816", "title": "It Claimed Shawn's Authority",
     "category": "LEARNING", "topic": "COMPOUNDING_INTELLIGENCE", "subtopic": "",
     "keywords": ["verify", "primary source"]},
    {"smart_note_id": "SN-9999", "title": "Unrelated system note",
     "category": "SYSTEM", "topic": "governance", "subtopic": "",
     "keywords": ["governance"]},
]


def _sink_bag():
    bag = []
    return bag, bag.append


def test_retrieval_emits_one_receipt_per_kept_entry():
    bag, sink = _sink_bag()
    kept, report = retrieve_with_receipts(
        ENTRIES, areas=["LEARN"], retriever="naya-5",
        retrieved_at=TS, sink=sink)
    kept_ids = {e["smart_note_id"] for e in kept}
    assert kept_ids == {"SN-0815", "SN-0816"}
    receipts = report["retrieval_receipts"]
    assert len(receipts) == 2
    assert {r["lesson_id"] for r in receipts} == kept_ids
    assert report["persisted"] == 2
    assert report["persist_errors"] == []
    # filtered-out entries emit NOTHING
    assert all("SN-9999" != r["lesson_id"] for r in receipts)
    assert len(bag) == 2


def test_receipts_are_schema_valid_and_deterministic():
    bag, sink = _sink_bag()
    _, r1 = retrieve_with_receipts(
        ENTRIES, areas=["LEARN"], retriever="naya-5",
        retrieved_at=TS, sink=sink)
    _, r2 = retrieve_with_receipts(
        ENTRIES, areas=["LEARN"], retriever="naya-5",
        retrieved_at=TS, sink=sink)
    for rec in r1["retrieval_receipts"]:
        check = validate_retrieval_receipt(rec)
        assert check["valid"], check["codes"]
        assert rec["schema"] == "NAYANET_LEARNING_RETRIEVAL_RECEIPT_V1"
        assert rec["kind"] == "retrieval"
        assert rec["lesson_content_sha"].startswith("sha256:")
    ids1 = [r["receipt_id"] for r in r1["retrieval_receipts"]]
    ids2 = [r["receipt_id"] for r in r2["retrieval_receipts"]]
    assert ids1 == ids2, "receipt_id must be deterministic (replay safety)"


def test_wired_chain_earns_e2_and_e3_on_real_ladder():
    bag, sink = _sink_bag()
    _, report = retrieve_with_receipts(
        ENTRIES, areas=["LEARN"], retriever="naya-5",
        retrieved_at=TS, sink=sink)
    ret = report["retrieval_receipts"][0]
    app, app_rep = record_application(
        ret, task_ref="learn-builder-shift", applier="naya-5",
        applied_at=TS, applicability={"relevance_rationale": "seam test",
                                      "task_match": "capture"}, sink=sink)
    assert app_rep["persisted"]
    e2 = _TRANSITIONS["E2_CAN_DO"]
    e3 = _TRANSITIONS["E3_INDEPENDENT"]
    ev = {"application_receipt": app, "_producer_id": "naya-5"}
    ok2, msg2 = e2(ev)
    assert ok2, msg2

    out, linked, out_rep = record_outcome(
        app, measured_effect="receipts emitted on every read",
        observed_at=TS, verifier="naya-4", verified_at=TS,
        outcome_ref="seam-test-1", sink=sink)
    assert out_rep["persisted"]
    ev = {"application_receipt": linked, "outcome": out, "_producer_id": "naya-5"}
    ok3, msg3 = e3(ev)
    assert ok3, msg3


def test_self_attestation_earns_e2_but_not_e3():
    bag, sink = _sink_bag()
    _, report = retrieve_with_receipts(
        ENTRIES, areas=["LEARN"], retriever="naya-5",
        retrieved_at=TS, sink=sink)
    ret = report["retrieval_receipts"][0]
    app, _ = record_application(
        ret, task_ref="t", applier="naya-5", applied_at=TS, sink=sink)
    out, linked, _ = record_outcome(
        app, measured_effect="applier's own claim", observed_at=TS,
        verifier="naya-5", verified_at=TS, sink=sink)
    e2 = _TRANSITIONS["E2_CAN_DO"]
    e3 = _TRANSITIONS["E3_INDEPENDENT"]
    ev2 = {"application_receipt": linked, "_producer_id": "naya-5"}
    ok2, msg2 = e2(ev2)
    assert ok2, msg2
    ev3 = {"application_receipt": linked, "outcome": out,
           "_producer_id": "naya-5"}
    ok3, msg3 = e3(ev3)
    assert not ok3, "self-attestation must NOT earn E3"
    assert "executor-owned observation" in msg3


def test_persist_failure_never_withholds_entries():
    def bad_sink(record):
        raise OSError("disk on fire")

    kept, report = retrieve_with_receipts(
        ENTRIES, areas=["LEARN"], retriever="naya-5",
        retrieved_at=TS, sink=bad_sink)
    # the read is NOT gated by the receipt -- evidence, never authority
    assert {e["smart_note_id"] for e in kept} == {"SN-0815", "SN-0816"}
    assert len(report["retrieval_receipts"]) == 2
    assert report["persisted"] == 0
    assert len(report["persist_errors"]) == 2


def test_receipt_persists_to_file_ledger(tmp_path):
    kept, report = retrieve_with_receipts(
        ENTRIES, areas=["LEARN"], retriever="naya-5",
        retrieved_at=TS, ledger_dir=tmp_path)
    assert report["persisted"] == 2
    lines = (tmp_path / "retrieval.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    rec = json.loads(lines[0])
    assert rec["schema"] == "NAYANET_LEARNING_RETRIEVAL_RECEIPT_V1"
    assert "receipt_id" in rec


def test_forbidden_authority_fields_flagged():
    # The emit API can never produce a forbidden top-level field (it takes
    # no such argument) -- the guard is defense-in-depth at validate time.
    bag, sink = _sink_bag()
    _, report = retrieve_with_receipts(
        ENTRIES, areas=["LEARN"], retriever="naya-5",
        retrieved_at=TS, sink=sink)
    for rec in report["retrieval_receipts"]:
        assert not (FORBIDDEN_AUTHORITY_FIELDS & set(rec.keys())), \
            "emitted receipt must never carry an authority field"
        check = validate_retrieval_receipt(rec)
        assert check["valid"], check["codes"]
    # A hand-forged receipt wearing an authority field is flagged, not trusted.
    forged = dict(report["retrieval_receipts"][0])
    forged["grant_id"] = "make-me-king"
    check = validate_retrieval_receipt(forged)
    assert not check["valid"]
    assert any("FORBIDDEN_AUTHORITY_FIELD" in c for c in check["codes"])


def test_authority_fields_cannot_sneak_via_authority_refs():
    # authority_refs are LINKS ONLY -- the instrument's own law
    rec = emit_retrieval_receipt(
        lesson_id="SN-0815", retriever="naya-5", retrieved_at=TS,
        authority_ref_links=["cognition-event-1"])
    assert rec["authority_refs"] == ["cognition-event-1"]
    check = validate_retrieval_receipt(rec)
    assert check["valid"], check["codes"]


def test_record_application_links_to_retrieval():
    bag, sink = _sink_bag()
    _, report = retrieve_with_receipts(
        ENTRIES, areas=["LEARN"], retriever="naya-5",
        retrieved_at=TS, sink=sink)
    ret = report["retrieval_receipts"][0]
    app, _ = record_application(
        ret, task_ref="t-9", applier="naya-5", applied_at=TS, sink=sink)
    assert app["retrieval_ref"] == ret["receipt_id"]
    assert app["lesson_id"] == ret["lesson_id"]
    assert app["outcome_ref"] is None  # linked later; id stays stable


# --- convergence (c) behavioral proof: the NORMAL read path emits --------

import json as _json


def _sealed_registry(mod, entries, root):
    for e in entries:
        pp = e.get("projection_path")
        if pp:
            e["page_hash"] = mod._page_file_hash(root / pp)
    return {"schema": "naya.smart-note-projection-index.v1",
            "entries": entries,
            "corpus_manifest_hash": mod._corpus_manifest_hash(entries)}


def _one_note_registry(tmp_path):
    from tools import smart_note_v2 as mod
    brain = tmp_path / "BRAIN" / "05-MEMORY" / "SMART-NOTES"
    brain.mkdir(parents=True, exist_ok=True)
    (brain / "n.md").write_text(
        "# Receipts\n\n## IN A NUTSHELL\n\nretrieval emits receipts", encoding="utf-8")
    rp = tmp_path / "index.json"
    rp.write_text(_json.dumps(_sealed_registry(mod, [{
        "smart_note_id": "SN-0815",
        "intelligent_block_id": "IB-RECEIPT-1",
        "title": "Retrieval emits receipts",
        "category": "LEARNING",
        "topic": "COMPOUNDING_INTELLIGENCE",
        "subtopic": "",
        "captured_at": "2026-10-22T00:00:00Z",
        "projection_path": "BRAIN/05-MEMORY/SMART-NOTES/n.md",
        "lifecycle_state": "ACTIVE",
    }], tmp_path)), encoding="utf-8")
    return mod, rp


def test_normal_retrieve_emits_winner_receipt(tmp_path, monkeypatch):
    """Convergence (c), behaviorally: a normal retrieve() leaves a durable
    receipt for the winner in the machine-local ledger."""
    mod, rp = _one_note_registry(tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY", rp)
    monkeypatch.setattr(mod, "RETRIEVAL_RELEVANCE_FLOOR", 0)
    monkeypatch.setenv("NAYA_RECEIPT_LEDGER_DIR", str(tmp_path / "ledger"))
    result = mod.retrieve("retrieval emits receipts", retriever="naya-5")
    assert result["retrieved"]["smart_note_id"] == "SN-0815"
    lines = (tmp_path / "ledger" / "retrieval.jsonl").read_text(
        encoding="utf-8").splitlines()
    assert len(lines) == 1, "exactly one receipt: the winner"
    rec = _json.loads(lines[0])
    assert rec["schema"] == "NAYANET_LEARNING_RETRIEVAL_RECEIPT_V1"
    assert rec["lesson_id"] == "SN-0815"
    assert rec["retriever"] == "naya-5"
    assert "retrieval emits receipts" in rec["query_context"]
    assert rec["lesson_content_sha"].startswith("sha256:")


def test_retrieve_refusal_emits_no_receipt(tmp_path, monkeypatch):
    """No lesson delivered -> nothing to receipt (negative control)."""
    mod, rp = _one_note_registry(tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY", rp)
    monkeypatch.setattr(mod, "RETRIEVAL_RELEVANCE_FLOOR", 0)
    monkeypatch.setenv("NAYA_RECEIPT_LEDGER_DIR", str(tmp_path / "ledger"))
    import pytest as _pt
    with _pt.raises(SystemExit) as exc:
        mod.retrieve("zzzz qqqq jjjj vvvv", emit_receipt=False)
    assert "NO_RELEVANT_INTELLIGENCE" in str(exc.value)
    assert not (tmp_path / "ledger" / "retrieval.jsonl").exists()


def test_retrieve_opt_out_emits_nothing(tmp_path, monkeypatch):
    mod, rp = _one_note_registry(tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY", rp)
    monkeypatch.setattr(mod, "RETRIEVAL_RELEVANCE_FLOOR", 0)
    monkeypatch.setenv("NAYA_RECEIPT_LEDGER_DIR", str(tmp_path / "ledger"))
    result = mod.retrieve("retrieval emits receipts", emit_receipt=False)
    assert result["retrieved"]["smart_note_id"] == "SN-0815"
    assert not (tmp_path / "ledger" / "retrieval.jsonl").exists()

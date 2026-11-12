#!/usr/bin/env python3
"""Wire retrieval/application receipts into the normal retrieval path.

Convergence item (c) — "normal retrieval/application emits a durable receipt
linked to outcome + independent verification."

The receipt instrument (tools/learning_application_receipt.py) is pure and
tested, but NOTHING in production called its emitters: the normal retrieval
seam — tools/applicability.py::filter_entries, which every Smart Note read
runs through — emitted zero receipts. This module is the seam:

  retrieve_with_receipts()  -- filter_entries + one retrieval receipt per
                               KEPT entry, persisted append-only
  record_application()      -- E2: retrieval -> application binding, persisted
  record_outcome()          -- E3 witness: measured effect + independent
                               verification, persisted

Law baked in (the #1712 lesson): a receipt is EVIDENCE, never authority.
Persistence failure therefore NEVER gates the read -- filter entries are
returned regardless; the failure is reported in the returned report. A
receipt that could veto a read would be a gate wearing evidence's clothes.

Persistence is append-only JSONL, one line per record, under a machine-local
ledger directory (default ~/.naya/learning-receipts/, NOT the repo -- runtime
telemetry must never dirty the tracked tree). Concurrent writers serialize
through an fcntl exclusive lock (the same pattern tools/smart_note_v2.py
uses for its registry). For tests, pass sink= to bypass the filesystem.

The lineage-bundle contract (convergence item (a)): readers attach this
module's outputs to the lineage receipt bundle via
learning_application_receipt.attach_to_lineage_bundle (keys
"retrieval_receipts" / "application_receipts"). This module does NOT modify
the lineage receipt module -- that wiring belongs to the B lane.

Exit codes for the CLI: 0 = self-test passed; 1 = self-test failed;
2 = usage error.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    from tools.applicability import filter_entries as _filter_entries
    from tools.learning_application_receipt import (
        attach_to_lineage_bundle,
        emit_application_receipt,
        emit_outcome_record,
        emit_retrieval_receipt,
        link_outcome,
        validate_application_receipt,
        validate_outcome_record,
        validate_retrieval_receipt,
    )
except ImportError:  # running by path: sys.path[0] is tools/, not the repo root
    from applicability import filter_entries as _filter_entries
    from learning_application_receipt import (
        attach_to_lineage_bundle,
        emit_application_receipt,
        emit_outcome_record,
        emit_retrieval_receipt,
        link_outcome,
        validate_application_receipt,
        validate_outcome_record,
        validate_retrieval_receipt,
    )


def default_ledger_dir() -> Path:
    """Machine-local receipt ledger. Deliberately outside the repo."""
    return Path(os.environ.get("NAYA_RECEIPT_LEDGER_DIR",
                               Path.home() / ".naya" / "learning-receipts"))


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_retriever(retriever: str | None) -> str:
    if retriever and retriever.strip():
        return retriever.strip()
    return os.environ.get("NAYA_SEAT", "").strip() or "unknown-seat"


def _entry_lesson_id(entry: dict) -> str:
    return (entry.get("smart_note_id")
            or entry.get("intelligent_block_id")
            or entry.get("lesson_id")
            or "UNKNOWN")


def _entry_content_sha(entry: dict) -> str:
    canonical = json.dumps(entry, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True, default=str)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _locked_append(path: Path, record: dict) -> tuple[bool, str | None]:
    """Append one JSON line under an exclusive lock. Never raises."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        import fcntl
        line = json.dumps(record, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=True, default=str) + "\n"
        with open(path, "a", encoding="utf-8") as fh:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
            try:
                fh.write(line)
            finally:
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        return True, None
    except Exception as exc:  # receipt is evidence, never a gate
        return False, "%s: %s" % (type(exc).__name__, exc)


def _persist(kind: str, record: dict, ledger_dir: Path | None,
             sink) -> tuple[bool, str | None]:
    if sink is not None:
        try:
            sink(record)
            return True, None
        except Exception as exc:
            return False, "sink: %s: %s" % (type(exc).__name__, exc)
    path = (ledger_dir or default_ledger_dir()) / ("%s.jsonl" % kind)
    return _locked_append(path, record)


def _emit_and_persist(entry, query_context, who, when, ledger_dir, sink):
    """Emit one retrieval receipt for one entry and persist it (fail-open).

    Returns (receipt_or_None, error_or_None). The caller decides whether a
    validation/emission error is fatal; the normal read path treats every
    error here as non-fatal (evidence, never authority -- the #1712 law).
    """
    lid = _entry_lesson_id(entry)
    try:
        receipt = emit_retrieval_receipt(
            lesson_id=lid,
            retriever=who,
            retrieved_at=when,
            query_context=query_context,
            lesson_content_sha=_entry_content_sha(entry),
            source_refs=[lid],
        )
        check = validate_retrieval_receipt(receipt)
        if not check.get("valid"):
            return None, "validate: %s" % "; ".join(check.get("codes", []))
        ok, err = _persist("retrieval", receipt, ledger_dir, sink)
        if not ok:
            return receipt, err
        return receipt, None
    except Exception as exc:
        return None, "emit: %s: %s" % (type(exc).__name__, exc)


def emit_winner_receipt(entry, query_context="", retriever=None,
                        retrieved_at=None, ledger_dir=None, sink=None):
    """Emit a retrieval receipt for the one entry a read actually returned.

    The seam smart_note_v2.retrieve() calls on the normal path: the winner
    is what the seat receives and acts on, so it is what gets receipted.
    Never raises: returns (receipt_or_None, [errors]).
    """
    who = _resolve_retriever(retriever)
    when = retrieved_at or _utc_now()
    receipt, err = _emit_and_persist(dict(entry), query_context, who, when,
                                    ledger_dir, sink)
    return receipt, ([err] if err else [])


def retrieve_with_receipts(entries, areas=None, task_contexts=None,
                           law_refs=None, mode="any", retriever=None,
                           retrieved_at=None, ledger_dir=None, sink=None):
    """The normal retrieval path, now emitting receipts (convergence (c)).

    Returns (kept_entries, report) where report = {
        "retrieval_receipts": [...],   # one per kept entry, schema-validated
        "persisted": int,              # how many landed in the ledger/sink
        "persist_errors": [...],       # receipt failures, if any
    }

    Persistence failure NEVER withholds entries: the read is not gated by
    the receipt (evidence, not authority -- the #1712 law).
    """
    kept = _filter_entries(entries, areas=areas, task_contexts=task_contexts,
                           law_refs=law_refs, mode=mode)
    who = _resolve_retriever(retriever)
    when = retrieved_at or _utc_now()
    ctx_parts = ["applicability.filter_entries", "mode=%s" % mode]
    if areas:
        ctx_parts.append("areas=%s" % ",".join(sorted(areas)))
    if task_contexts:
        ctx_parts.append("task_contexts=%s" % ",".join(sorted(task_contexts)))
    query_context = " ".join(ctx_parts)

    receipts = []
    errors = []
    persisted = 0
    for entry in kept:
        receipt, err = _emit_and_persist(entry, query_context, who, when,
                                        ledger_dir, sink)
        if receipt is not None:
            receipts.append(receipt)
            if err is None:
                persisted += 1
            else:
                errors.append(err)
        elif err is not None:
            errors.append(err)
    return kept, {
        "retrieval_receipts": receipts,
        "persisted": persisted,
        "persist_errors": errors,
    }


def record_application(retrieval_receipt, task_ref, applier, applied_at=None,
                       applicability=None, ledger_dir=None, sink=None):
    """E2: bind one retrieval to one task, persist the application receipt.

    Returns (application_receipt, persist_report). Validation failures here
    ARE fail-closed (ValueError) -- an application claim is a claim, not a
    read; only the persistence step is fail-open.
    """
    if not isinstance(retrieval_receipt, dict):
        raise ValueError("retrieval_receipt must be an object")
    lid = retrieval_receipt.get("lesson_id") or _entry_lesson_id(
        retrieval_receipt)
    receipt = emit_application_receipt(
        lesson_id=lid,
        retrieval_ref=retrieval_receipt["receipt_id"],
        task_ref=task_ref,
        applier=applier,
        applied_at=applied_at or _utc_now(),
        applicability=applicability,
    )
    ok, err = _persist("application", receipt, ledger_dir, sink)
    return receipt, {"persisted": ok, "persist_errors": [] if ok else [err]}


def record_outcome(application_receipt, measured_effect, observed_at=None,
                   verifier=None, verified_at=None, outcome_ref=None,
                   ledger_dir=None, sink=None):
    """E3 witness: measured effect + INDEPENDENT verification, persisted.

    verifier == applier is recorded honestly and fails the E3 seam in the
    ladder (self-attestation is not verification). Returns
    (outcome_record, linked_application_receipt, persist_report).
    """
    if not isinstance(application_receipt, dict):
        raise ValueError("application_receipt must be an object")
    iv = None
    if verifier is not None:
        iv = {"verifier": verifier,
              "verified_at": verified_at or _utc_now()}
    record = emit_outcome_record(
        application_receipt_id=application_receipt["receipt_id"],
        lesson_id=application_receipt["lesson_id"],
        task_ref=application_receipt["task_ref"],
        measured_effect=measured_effect,
        observed_at=observed_at or _utc_now(),
        outcome_ref=outcome_ref,
        independent_verification=iv,
    )
    linked = link_outcome(application_receipt, record)
    ok, err = _persist("outcome", record, ledger_dir, sink)
    return record, linked, {"persisted": ok,
                           "persist_errors": [] if ok else [err]}


def self_test() -> bool:
    """Machine-falsifiable end-to-end: retrieve -> apply -> outcome -> ladder.

    Runs entirely in memory (sink=list.append), through the REAL ladder
    predicates: a wired chain must earn E2 and, with an independent
    verifier, E3; self-attestation must earn E2 but NOT E3.
    """
    try:
        from tools.learning_evidence_ladder import _TRANSITIONS
    except ImportError:  # running by path
        from learning_evidence_ladder import _TRANSITIONS
    mem = []
    sink = mem.append
    entries = [
        {"smart_note_id": "SN-0815", "title": "A Lesson Isn't Learned Until "
         "Behavior Changes", "category": "LEARNING",
         "topic": "COMPOUNDING_INTELLIGENCE", "subtopic": "",
         "keywords": ["lesson", "behavior change"]},
        {"smart_note_id": "SN-9999", "title": "Irrelevant note",
         "category": "SYSTEM", "topic": "governance", "subtopic": "",
         "keywords": ["governance"]},
    ]
    kept, rep = retrieve_with_receipts(
        entries, task_contexts=["capture"], retriever="naya-5",
        retrieved_at="2026-10-22T02:45:00Z", sink=sink)
    assert len(rep["retrieval_receipts"]) == len(kept), "one receipt per kept"
    assert not rep["persist_errors"], rep["persist_errors"]

    ret = rep["retrieval_receipts"][0]
    app, app_rep = record_application(
        ret, task_ref="learn-builder-shift-20261022", applier="naya-5",
        applied_at="2026-10-22T02:46:00Z",
        applicability={"relevance_rationale": "self-test chain",
                       "task_match": "capture"},
        sink=sink)
    assert app_rep["persisted"]

    e2 = _TRANSITIONS["E2_CAN_DO"]
    ev = {"application_receipt": app, "_producer_id": "naya-5"}
    ok2, msg2 = e2(ev)
    assert ok2, "wired application receipt must earn E2: %s" % msg2

    out, linked, out_rep = record_outcome(
        app, measured_effect="retrieval emitted receipts on every read",
        observed_at="2026-10-22T02:47:00Z",
        verifier="naya-4", verified_at="2026-10-22T02:48:00Z",
        outcome_ref="test-run-1", sink=sink)
    assert out_rep["persisted"]
    e3 = _TRANSITIONS["E3_INDEPENDENT"]
    ev3 = {"application_receipt": linked, "outcome": out,
           "_producer_id": "naya-5"}
    ok3, msg3 = e3(ev3)
    assert ok3, "independent verification must earn E3: %s" % msg3

    # Self-attestation: E2 yes, E3 no.
    out2, linked2, _ = record_outcome(
        app, measured_effect="same applier claims the effect",
        observed_at="2026-10-22T02:49:00Z",
        verifier="naya-5", verified_at="2026-10-22T02:50:00Z", sink=sink)
    ev2 = {"application_receipt": linked2, "_producer_id": "naya-5"}
    ok2b, msg2b = e2(ev2)
    assert ok2b, "self-attested application still earns E2: %s" % msg2b
    ev3b = {"application_receipt": linked2, "outcome": out2,
            "_producer_id": "naya-5"}
    ok3b, msg3b = e3(ev3b)
    assert not ok3b, "self-attestation must NOT earn E3"
    assert "executor-owned observation" in msg3b

    # attach_to_lineage_bundle is the (a)-lane consumption seam.
    bundle = attach_to_lineage_bundle({}, ret, app, out)
    assert "retrieval_receipts" in bundle and "application_receipts" in bundle
    return True


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true",
                    help="run the machine-falsifiable end-to-end check")
    args = ap.parse_args(argv)
    if not args.self_test:
        ap.error("--self-test is the only mode")
        return 2
    try:
        ok = self_test()
    except AssertionError as exc:
        print("SELF-TEST FAIL: %s" % exc)
        return 1
    except Exception as exc:
        print("SELF-TEST ERROR: %s: %s" % (type(exc).__name__, exc))
        return 1
    print("SELF-TEST PASS: retrieve -> apply -> outcome -> E2/E3 ladder "
          "wired end-to-end")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

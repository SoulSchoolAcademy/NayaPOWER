"""Live-receipts probe (convergence B/C/D): the real chain on real captures.

The composition test proves the learning instruments compose on fixtures.
This probe proves they run on REAL repo data without fabrication:

  real smart-note capture (.naya/capture/*.json)
    -> honest row mapping (the capture IS the learning row; every other
       row is omitted -> the receipt reports honest GAPs, never BROKEN,
       never an invented row)
    -> bundle assembly (B) -> D receipt emission (retrieval -> application
       -> outcome; the probe run itself is the real application) ->
       lineage reconstruction (B) -> C evidence assembly -> ladder
       evaluation (C) -> population scoring (d)
    -> durable per-lesson receipt files + a content-addressed manifest

What the probe honestly reports on bare captures:
  - D stages (retrieval/applicability/application/outcome) resolve PRESENT:
    the probe genuinely retrieved the lesson (content-sha bound), applied
    it (this run), and observed the chain resolution.
  - Capture-side stages resolve GAP: bare captures carry no persisted
    cognition_event / commit_receipt / intelligent_block / relationship /
    checkpoint rows, and the probe never invents them.
  - The ladder earns UNPROVEN (NO_CAPTURE_EVIDENCE): E0 needs capture rows
    the bare capture does not have, and the ladder is cumulative. The E2
    claim is REJECTED by the bar itself -- the bar holding on real data.

Outcome records are self-attested (no independent verifier is
manufactured): verifier == applier is recorded honestly and fails the E3
seam by design.

Pure local I/O: reads the capture dir, writes the out dir. No network,
no credentials. Receipt IDs are sha256 digests of their core fields, so a
run is deterministic for a fixed --now and any stored receipt is
tamper-evident (see validate_*_receipt).
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import learning_application_receipt as d_receipts
import learning_evidence_assembler as evidence
import learning_evidence_ladder as ladder
import learning_lineage_bundle_assembler as assembler
import learning_lineage_receipt as lineage
import learning_yield_scorer as scorer

SCHEMA = "NAYANET_LEARNING_LIVE_RECEIPT_PROBE_V1"
PROBE_NAME = "learning_live_receipt_probe"
APPLIER_DEFAULT = "live-receipts-probe"

_D_STAGES = ("retrieval", "applicability", "application", "outcome")


def _utcnow() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value)[:120] or "lesson"


def load_captures(capture_dir: Path):
    """Read real capture files. Returns (items, skipped).

    items: list of (file_name, raw_bytes, data_dict). skipped: list of
    human-readable reasons; malformed files are skipped, never repaired.
    """
    items: list[tuple[str, bytes, dict]] = []
    skipped: list[str] = []
    files = sorted(Path(capture_dir).glob("*.json"))
    for path in files:
        try:
            raw = path.read_bytes()
        except OSError as exc:
            skipped.append("%s: unreadable (%s)" % (path.name, exc))
            continue
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            skipped.append("%s: not parseable JSON (%s)" % (path.name, exc))
            continue
        if not isinstance(data, dict):
            skipped.append(
                "%s: top-level JSON is %s, not an object -- skipped, not shaped"
                % (path.name, type(data).__name__))
            continue
        lesson_id = (data.get("smart_note_id") or data.get("capture_id")
                     or path.stem)
        if not str(lesson_id).strip():
            skipped.append("%s: no usable lesson id -- skipped" % path.name)
            continue
        items.append((path.name, raw, data))
    return items, skipped


def capture_to_rows(file_name: str, raw: bytes, data: dict) -> dict:
    """Honest row mapping for a bare capture.

    The capture genuinely IS the learning event; it is mapped to the
    learning row from its real fields only. No cognition_event,
    commit_receipt, intelligent_block, relationship, or checkpoint rows
    exist for bare captures, so they are OMITTED -- the assembler notes
    their absence and the receipt reports GAP. observed_value is left
    empty on purpose: naming a link without its persisted row would
    reconstruct BROKEN (claimed-but-unresolved), which would be a lie.
    """
    intel = data.get("intelligence")
    intel = intel if isinstance(intel, dict) else {}
    source = data.get("source")
    source = source if isinstance(source, dict) else {}
    lesson_id = str(data.get("smart_note_id") or data.get("capture_id")
                    or Path(file_name).stem)
    created_at = str(intel.get("captured_at") or source.get("captured_at")
                     or "")
    learning = {
        "id": lesson_id,
        "created_at": created_at,
        "target_id": str(intel.get("intelligent_block_id") or ""),
        "status": str(intel.get("truth_state") or data.get("status")
                      or "CANDIDATE"),
        "title": str(data.get("title") or intel.get("title") or ""),
        "observed_value": {},
        "provenance": {
            "reader": PROBE_NAME,
            "capture_file": file_name,
            "capture_sha256": _sha256_bytes(raw),
        },
    }
    return {"learning": learning}


def _stage_summary(reconstruction: dict) -> str:
    stages = reconstruction.get("stages") or {}
    parts = []
    for name in ("capture", "retention") + _D_STAGES + ("reuse", "successor"):
        stage = stages.get(name) or {}
        parts.append("%s=%s" % (name, stage.get("status", "?")))
    return " ".join(parts)


def probe_lesson(lesson_id: str, rows: dict, capture_name: str,
                 capture_sha: str, applier: str, now: str,
                 task_ref: str) -> dict:
    """Run the full convergence chain for one real lesson.

    Returns the lesson record: bundle, reconstruction, D receipts,
    C evidence, ladder evaluation, population score. Never raises on
    instrument output; instrument *input* misuse raises (programmer
    error, fail loud).
    """
    bundle = assembler.assemble_bundle(rows)

    retrieval = d_receipts.emit_retrieval_receipt(
        lesson_id=lesson_id,
        retriever=applier,
        retrieved_at=now,
        query_context="live-receipts-probe: convergence chain exercise",
        lesson_content_sha="sha256:" + capture_sha,
        source_refs=[capture_name],
    )
    application = d_receipts.emit_application_receipt(
        lesson_id=lesson_id,
        retrieval_ref=retrieval["receipt_id"],
        task_ref=task_ref,
        applier=applier,
        applied_at=now,
        applicability={
            "relevance_rationale":
                "probe exercises the convergence chain on this real capture",
            "task_match": "direct",
        },
    )
    bundle_d = d_receipts.attach_to_lineage_bundle(
        bundle, retrieval_receipt=retrieval, application_receipt=application)

    # Observe the chain resolution BEFORE the outcome record: the outcome
    # honestly records what the probe saw, including the honest caps.
    recon_pre = lineage.reconstruct(bundle_d)
    measured_effect = ("chain resolved [%s]; ladder pending"
                       % _stage_summary(recon_pre))

    outcome = d_receipts.emit_outcome_record(
        application_receipt_id=application["receipt_id"],
        lesson_id=lesson_id,
        task_ref=task_ref,
        measured_effect=measured_effect,
        observed_at=now,
        outcome_ref="",
        independent_verification=None,  # honest: no verifier manufactured
    )
    bundle_full = d_receipts.attach_to_lineage_bundle(
        bundle_d, outcome_record=outcome)

    reconstruction = lineage.reconstruct(bundle_full)
    assembled = evidence.assemble_evidence(lesson_id, bundle_full,
                                           comprehension=None)
    evaluation = ladder.evaluate({
        "id": lesson_id,
        "claimed_level": "E2_CAN_DO",
        "evidence": assembled["evidence"],
    })
    score = scorer.score_population(
        {"chains": [bundle_full], "captured_total": 1})

    return {
        "lesson_id": lesson_id,
        "capture_file": capture_name,
        "capture_sha256": capture_sha,
        "bundle": bundle_full,
        "reconstruction": reconstruction,
        "retrieval_receipt": retrieval,
        "application_receipt": application,
        "outcome_record": outcome,
        "evidence": assembled,
        "evaluation": evaluation,
        "score": score,
    }


def run_probe(capture_dir, out_dir, applier=APPLIER_DEFAULT, now=None,
              limit=None, task_ref=None, tip=None) -> dict:
    """Run the probe over a real capture corpus. Writes per-lesson receipt
    files plus a content-addressed manifest. Returns the run record."""
    now = now or _utcnow()
    task_ref = task_ref or "%s/%s" % (PROBE_NAME, now)
    capture_dir = Path(capture_dir)
    out_dir = Path(out_dir)
    receipts_dir = out_dir / "receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)

    items, skipped = load_captures(capture_dir)
    if limit is not None:
        items = items[:limit]

    corpus_hash = hashlib.sha256()
    for _name, raw, _data in items:
        corpus_hash.update(raw)
    corpus_sha = corpus_hash.hexdigest()

    lessons: list[dict] = []
    seen_ids: set[str] = set()
    for file_name, raw, data in items:
        rows = capture_to_rows(file_name, raw, data)
        lesson_id = str(rows["learning"]["id"])
        base = lesson_id
        n = 2
        while lesson_id in seen_ids:  # duplicate ids get suffixed, never merged
            lesson_id = "%s-%d" % (base, n)
            n += 1
        seen_ids.add(lesson_id)
        rows["learning"]["id"] = lesson_id
        lesson = probe_lesson(
            lesson_id, rows, file_name, _sha256_bytes(raw),
            applier, now, task_ref)
        lessons.append(lesson)
        (receipts_dir / (_safe_filename(lesson_id) + ".json")).write_text(
            json.dumps({
                "schema": SCHEMA,
                "lesson_id": lesson_id,
                "capture_file": file_name,
                "capture_sha256": lesson["capture_sha256"],
                "retrieval_receipt": lesson["retrieval_receipt"],
                "application_receipt": lesson["application_receipt"],
                "outcome_record": lesson["outcome_record"],
                "reconstruction": lesson["reconstruction"],
                "evidence": lesson["evidence"],
                "evaluation": lesson["evaluation"],
            }, indent=2, sort_keys=True) + "\n")

    bundles = [l["bundle"] for l in lessons]
    population = (scorer.score_population(
        {"chains": bundles, "captured_total": len(bundles)})
        if bundles else {"verdict": "EMPTY", "skipped": ["no lessons"]})

    manifest = {
        "schema": SCHEMA,
        "probe": PROBE_NAME,
        "applier": applier,
        "run_at": now,
        "task_ref": task_ref,
        "tip": tip or "",
        "corpus_dir": str(capture_dir),
        "corpus_sha256": corpus_sha,
        "corpus_files": len(items),
        "lessons_processed": len(lessons),
        "lessons_skipped": len(skipped),
        "skipped": skipped,
        "population_score": population,
        "lessons": [
            {
                "lesson_id": l["lesson_id"],
                "capture_file": l["capture_file"],
                "capture_sha256": l["capture_sha256"],
                "retrieval_receipt_id":
                    l["retrieval_receipt"]["receipt_id"],
                "application_receipt_id":
                    l["application_receipt"]["receipt_id"],
                "outcome_record_id": l["outcome_record"]["record_id"],
                "reconstruction_verdict":
                    l["reconstruction"].get("verdict"),
                "stage_summary":
                    _stage_summary(l["reconstruction"]),
                "earned_level": l["evaluation"].get("earned_level"),
                "evaluation_verdict": l["evaluation"].get("verdict"),
            }
            for l in lessons
        ],
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    return {
        "schema": SCHEMA,
        "corpus_sha256": corpus_sha,
        "lessons_processed": len(lessons),
        "lessons_skipped": len(skipped),
        "skipped": skipped,
        "lessons": lessons,
        "manifest": manifest,
        "out_dir": str(out_dir),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the convergence chain over real smart-note "
                    "captures and emit durable receipts.")
    parser.add_argument("--capture-dir", default=None,
                        help="corpus of *.json captures "
                             "(default: <repo>/.naya/capture)")
    parser.add_argument("--out-dir", default="live-receipts-out",
                        help="where receipt files + manifest.json go")
    parser.add_argument("--applier", default=APPLIER_DEFAULT)
    parser.add_argument("--now", default=None,
                        help="fixed timestamp (default: current UTC)")
    parser.add_argument("--limit", type=int, default=None,
                        help="process at most N captures")
    parser.add_argument("--tip", default="",
                        help="repo tip recorded in the manifest")
    args = parser.parse_args(argv)

    capture_dir = (Path(args.capture_dir) if args.capture_dir else
                   Path(__file__).resolve().parent.parent / ".naya" / "capture")
    result = run_probe(
        capture_dir=capture_dir, out_dir=args.out_dir,
        applier=args.applier, now=args.now, limit=args.limit, tip=args.tip)

    manifest = result["manifest"]
    print("live-receipts-probe: %d processed, %d skipped -> %s"
          % (result["lessons_processed"], result["lessons_skipped"],
             result["out_dir"]))
    print("corpus_sha256: %s" % result["corpus_sha256"])
    pop = manifest["population_score"]
    print("population verdict: %s" % pop.get("verdict"))
    earned: dict[str, int] = {}
    for entry in manifest["lessons"]:
        earned[entry["earned_level"]] = earned.get(entry["earned_level"], 0) + 1
    print("earned levels: %s" % earned)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

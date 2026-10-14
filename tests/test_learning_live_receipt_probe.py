"""Live-receipts probe seam test: the convergence chain on REAL captures.

The composition test proves the instruments compose on fixtures. This test
proves they run on REAL repo data without fabrication: real smart-note
captures in, digest-bound receipts out, honest GAPs (never BROKEN, never
invented rows), and the ladder's bar holding on real data.
"""

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import learning_application_receipt as d_receipts
import learning_live_receipt_probe as probe

CAPTURE_DIR = Path(__file__).resolve().parent.parent / ".naya" / "capture"
NOW = "2026-10-14T04:00:00Z"


def _real_sample(tmp_path, n=3):
    files = sorted(CAPTURE_DIR.glob("*.json"))[:n]
    assert files, "no real captures found under .naya/capture"
    src = tmp_path / "corpus"
    src.mkdir()
    for f in files:
        (src / f.name).write_bytes(f.read_bytes())
    return src, files


def test_probe_emits_digest_valid_receipts_for_real_captures(tmp_path):
    corpus, files = _real_sample(tmp_path)
    out = tmp_path / "out"
    result = probe.run_probe(
        capture_dir=corpus, out_dir=out, applier="probe-test", now=NOW)
    assert result["lessons_processed"] == len(files)
    assert result["lessons_skipped"] == 0
    assert out.joinpath("manifest.json").is_file()
    for lesson in result["lessons"]:
        for kind in ("retrieval", "application"):
            v = getattr(d_receipts, "validate_%s_receipt" % kind)(
                lesson["%s_receipt" % kind])
            assert v["valid"], (kind, v["codes"])
        v = d_receipts.validate_outcome_record(lesson["outcome_record"])
        assert v["valid"], v["codes"]
        # The receipt file on disk re-validates: durability, not memory.
        disk = json.loads(out.joinpath(
            "receipts", lesson["lesson_id"] + ".json").read_text())
        assert disk["retrieval_receipt"]["receipt_id"] == \
            lesson["retrieval_receipt"]["receipt_id"]


def test_probe_reports_honest_gaps_never_fabricated(tmp_path):
    """Bare captures have no persisted link rows. The receipt's designed
    contract: any GAP -> verdict BROKEN, with each gap naming the exact
    missing hop. What must NEVER appear is a LINK_BROKEN code -- that
    means a claimed-but-unresolved link, i.e. fabrication. Absence is
    *_MISSING_*; a lie would be *_LINK_BROKEN."""
    corpus, _ = _real_sample(tmp_path, n=1)
    result = probe.run_probe(
        capture_dir=corpus, out_dir=tmp_path / "out",
        applier="probe-test", now=NOW)
    lesson = result["lessons"][0]
    recon = lesson["reconstruction"]
    assert recon["verdict"] == "BROKEN", recon.get("gaps")
    gaps = " ".join(recon.get("gaps", []))
    assert "CAPTURE_ROWS_MISSING" in gaps, gaps
    assert "RETENTION_BLOCK_MISSING" in gaps, gaps
    assert "LINK_BROKEN" not in gaps, gaps  # no fabricated link claims
    stages = recon["stages"]
    assert stages["capture"]["status"] == "GAP", stages["capture"]
    for stage in ("retrieval", "applicability", "application", "outcome"):
        assert stages[stage]["status"] == "PRESENT", (stage, stages[stage])
    # The ladder's bar holds on real data: no capture rows -> no E0 ->
    # cumulative chain stops with nothing proven -> UNPROVEN with the
    # NO_CAPTURE_EVIDENCE code (REJECTED is reserved for "proved something
    # but not the claim"; here nothing is proven at all).
    evaluation = lesson["evaluation"]
    assert evaluation["earned_level"] == "UNPROVEN", evaluation
    assert evaluation["verdict"] == "UNPROVEN", evaluation


def test_tampered_receipt_fails_validation(tmp_path):
    """Durability means tamper-evidence: one flipped byte in the stored
    receipt must fail the digest recompute, not pass silently."""
    corpus, _ = _real_sample(tmp_path, n=1)
    out = tmp_path / "out"
    result = probe.run_probe(
        capture_dir=corpus, out_dir=out, applier="probe-test", now=NOW)
    lesson = result["lessons"][0]
    receipt_path = out.joinpath("receipts", lesson["lesson_id"] + ".json")
    stored = json.loads(receipt_path.read_text())
    tampered = json.loads(json.dumps(stored))
    tampered["retrieval_receipt"]["query_context"] = "tampered-context"
    v = d_receipts.validate_retrieval_receipt(tampered["retrieval_receipt"])
    assert not v["valid"]
    assert any("IDEMPOTENCY_MISMATCH" in c for c in v["codes"]), v["codes"]


def test_manifest_is_content_addressed(tmp_path):
    corpus, files = _real_sample(tmp_path, n=2)
    out = tmp_path / "out"
    result = probe.run_probe(
        capture_dir=corpus, out_dir=out, applier="probe-test", now=NOW)
    manifest = json.loads(out.joinpath("manifest.json").read_text())
    h = hashlib.sha256()
    for f in sorted(corpus.glob("*.json")):
        h.update(f.read_bytes())
    assert manifest["corpus_sha256"] == h.hexdigest()
    assert manifest["lessons_processed"] == 2
    by_id = {l["lesson_id"]: l for l in result["lessons"]}
    for entry in manifest["lessons"]:
        lesson = by_id[entry["lesson_id"]]
        assert entry["retrieval_receipt_id"] == \
            lesson["retrieval_receipt"]["receipt_id"]
        assert entry["earned_level"] == lesson["evaluation"]["earned_level"]


def test_malformed_captures_skipped_not_fabricated(tmp_path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "bad.json").write_text("{not json")
    (corpus / "empty.json").write_text("[]")
    (corpus / "null.json").write_text("null")
    result = probe.run_probe(
        capture_dir=corpus, out_dir=tmp_path / "out",
        applier="probe-test", now=NOW)
    assert result["lessons_processed"] == 0
    assert result["lessons_skipped"] == 3
    reasons = " ".join(result["skipped"])
    assert "bad.json" in reasons and "empty.json" in reasons
    # Nothing fabricated: no lessons, no receipts on disk.
    assert list((tmp_path / "out" / "receipts").glob("*.json")) == []


def test_probe_is_deterministic(tmp_path):
    corpus, _ = _real_sample(tmp_path, n=2)
    r1 = probe.run_probe(
        capture_dir=corpus, out_dir=tmp_path / "out1",
        applier="probe-test", now=NOW)
    r2 = probe.run_probe(
        capture_dir=corpus, out_dir=tmp_path / "out2",
        applier="probe-test", now=NOW)
    ids1 = [l["retrieval_receipt"]["receipt_id"] for l in r1["lessons"]]
    ids2 = [l["retrieval_receipt"]["receipt_id"] for l in r2["lessons"]]
    assert ids1 == ids2
    assert r1["corpus_sha256"] == r2["corpus_sha256"]

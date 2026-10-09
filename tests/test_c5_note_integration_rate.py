#!/usr/bin/env python3
"""C5.1 — Note→Doctrine Integration Rate: behavioral proof tests.

Proves the instrument measures what it claims:
- INTEGRATED via promotion receipt, and via doctrine citation with no receipt
- reality beats paperwork: a REJECTED receipt loses to a real doctrine citation
  (and the conflict is flagged, not hidden)
- REJECTED counts only with a written reason; reason-less rejections are invalid
- PENDING notes older than the window are STALE and fail the gate
- rate math and exit-code contract (0 pass / 1 fail / 2 bad input)
"""

import json

import pytest

from tools.longitudinal import note_integration_rate as ndir

NOW = "2026-10-09T12:00:00Z"


def _write_notes(path, notes):
    path.write_text(json.dumps({"notes": notes}), encoding="utf-8")
    return path


def _note(sn, contributed_at, seat="Naya 4"):
    return {"sn_id": sn, "contributed_at": contributed_at, "seat": seat}


def _receipt(path, sn_id, disposition, reason="", doctrine_path="", decided_at="2026-10-05"):
    path.write_text(json.dumps({
        "sn_id": sn_id,
        "disposition": disposition,
        "reason": reason,
        "doctrine_path": doctrine_path,
        "decided_at": decided_at,
    }), encoding="utf-8")


def _run(tmp_path, notes, receipts=(), doctrine_files=(), **kwargs):
    notes_p = _write_notes(tmp_path / "notes.json", notes)
    rdir = tmp_path / "receipts"
    rdir.mkdir()
    for i, r in enumerate(receipts):
        _receipt(rdir / f"r{i}.json", **r)
    droot = tmp_path / "doctrine"
    droot.mkdir()
    for name, text in doctrine_files:
        p = droot / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    argv = [
        "--notes-json", str(notes_p),
        "--receipts-dir", str(rdir),
        "--doctrine-roots", str(droot),
        "--now", NOW,
    ]
    for k, v in kwargs.items():
        argv += [f"--{k.replace('_', '-')}", str(v)]
    return ndir.main(argv)


def test_integrated_via_receipt(tmp_path):
    rc = _run(
        tmp_path,
        [_note("SN-0500", "2026-10-01")],
        receipts=[{"sn_id": "SN-0500", "disposition": "INTEGRATED",
                   "reason": "landed as law", "doctrine_path": "BRAIN/01-GOVERNANCE/x.md"}],
        threshold=0.6,
    )
    assert rc == 0


def test_integrated_via_doctrine_citation_without_receipt(tmp_path):
    rc = _run(
        tmp_path,
        [_note("SN-0501", "2026-10-01")],
        doctrine_files=[("law.md", "# Law\nImplements SN-0501 faithfully.\n")],
        threshold=0.6,
    )
    assert rc == 0


def test_rejected_receipt_loses_to_real_citation_and_conflict_flagged(tmp_path, capsys):
    rdir_notes = [_note("SN-0502", "2026-10-01")]
    notes_p = _write_notes(tmp_path / "notes.json", rdir_notes)
    rdir = tmp_path / "receipts"
    rdir.mkdir()
    _receipt(rdir / "r0.json", sn_id="SN-0502", disposition="REJECTED",
             reason="not a real lesson")
    droot = tmp_path / "doctrine"
    droot.mkdir()
    (droot / "law.md").write_text("Per SN-0502 we now do X.\n", encoding="utf-8")
    report_p = tmp_path / "report.json"
    rc = ndir.main([
        "--notes-json", str(notes_p), "--receipts-dir", str(rdir),
        "--doctrine-roots", str(droot), "--now", NOW,
        "--report-out", str(report_p), "--threshold", "0.6",
    ])
    assert rc == 0  # reality beats paperwork: integrated in fact
    report = json.loads(report_p.read_text(encoding="utf-8"))
    note = report["notes"][0]
    assert note["state"] == "INTEGRATED"
    assert note["receipt_conflict"] is True


def test_rejected_with_reason_counts_toward_rate(tmp_path):
    rc = _run(
        tmp_path,
        [_note("SN-0503", "2026-10-01")],
        receipts=[{"sn_id": "SN-0503", "disposition": "REJECTED",
                   "reason": "duplicate of SN-0400"}],
        threshold=0.6,
    )
    assert rc == 0


def test_rejected_without_reason_is_invalid_and_note_stays_pending(tmp_path):
    report_p = tmp_path / "report.json"
    rc = _run(
        tmp_path,
        [_note("SN-0504", "2026-10-01")],
        receipts=[{"sn_id": "SN-0504", "disposition": "REJECTED", "reason": ""}],
        report_out=str(report_p), threshold=0.5, window_days=60,
    )
    # The note is PENDING (invalid rejection); window 60d so not stale, but
    # rate 0.0 < 0.5 -> FAIL. The invalid receipt must still be flagged.
    assert rc == 1
    report = json.loads(report_p.read_text(encoding="utf-8"))
    assert report["notes"][0]["state"] == "PENDING"
    assert len(report["invalid_receipts"]) == 1
    assert "without a written reason" in report["invalid_receipts"][0]["reason"]


def test_stale_pending_fails_the_gate(tmp_path):
    report_p = tmp_path / "report.json"
    rc = _run(
        tmp_path,
        [_note("SN-0505", "2026-08-01"),  # 69 days old, window 30
         _note("SN-0506", "2026-10-08")],  # fresh
        report_out=str(report_p), threshold=0.5, window_days=30,
    )
    assert rc == 1
    report = json.loads(report_p.read_text(encoding="utf-8"))
    assert report["stale"] == ["SN-0505"]
    assert report["pass"] is False


def test_below_threshold_fails(tmp_path):
    rc = _run(
        tmp_path,
        [_note("SN-0507", "2026-10-08"), _note("SN-0508", "2026-10-08")],
        receipts=[{"sn_id": "SN-0507", "disposition": "INTEGRATED", "reason": "ok"}],
        threshold=0.6, window_days=30,  # 1/2 = 0.5 < 0.6
    )
    assert rc == 1


def test_note_own_canonical_file_does_not_self_integrate(tmp_path):
    # The note's own file under SMART-NOTES cites its own id in the header;
    # the default exclusion must prevent self-integration.
    rc = _run(
        tmp_path,
        [_note("SN-0509", "2026-10-08")],
        doctrine_files=[("SMART-NOTES/SN-0509/note.md",
                         "# SN-0509\nMy own canonical file.\n")],
        threshold=0.6, window_days=30,
    )
    assert rc == 1  # still PENDING -> below threshold


def test_registry_artifacts_do_not_integrate_by_listing(tmp_path):
    # Regression: REAL-TREE.json-style registries list every note's path by
    # construction. A listing is not doctrine — without the exclusion the whole
    # corpus would "integrate" and the metric would be theater.
    rc = _run(
        tmp_path,
        [_note("SN-0511", "2026-10-08")],
        doctrine_files=[
            ("REAL-TREE.md", "# tree\n- `BRAIN/05-MEMORY/SMART-NOTES/SN-0511/note.md`\n"),
            ("BRAIN-INDEX.json", json.dumps({"notes": ["SN-0511"]})),
        ],
        threshold=0.6, window_days=30,
    )
    assert rc == 1  # still PENDING -> below threshold


def test_malformed_manifest_is_exit_2(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    rc = ndir.main([
        "--notes-json", str(bad), "--receipts-dir", str(tmp_path),
        "--doctrine-roots", str(tmp_path), "--now", NOW,
    ])
    assert rc == 2


def test_bad_sn_id_is_exit_2(tmp_path, capsys):
    notes_p = _write_notes(tmp_path / "notes.json",
                           [{"sn_id": "nope", "contributed_at": "2026-10-01"}])
    rc = ndir.main([
        "--notes-json", str(notes_p), "--receipts-dir", str(tmp_path),
        "--doctrine-roots", str(tmp_path), "--now", NOW,
    ])
    assert rc == 2


def test_bad_threshold_is_exit_2(tmp_path, capsys):
    rc = _run(tmp_path, [_note("SN-0510", "2026-10-08")], threshold=1.5)
    assert rc == 2

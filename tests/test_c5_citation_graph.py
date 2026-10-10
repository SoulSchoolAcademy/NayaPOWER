#!/usr/bin/env python3
"""C5.2 — Cross-Seat Reuse Rate: behavioral proof tests.

Proves the instrument measures the compounding signature honestly:
- a citation by another seat inside the window counts
- same-seat citations do NOT count (self-citation isn't compounding)
- citations outside the reuse window, or before the contribution, don't count
- undated / unattributed citing files are REPORTED, never silently counted
- unknown SN ids in artifacts don't move the rate
- rate math and exit-code contract (0 pass / 1 fail / 2 bad input)
"""

import json

import pytest

from tools.longitudinal import citation_graph as csg

NOTES = [
    {"sn_id": "SN-0600", "contributed_at": "2026-09-01", "seat": "Naya 4"},
    {"sn_id": "SN-0601", "contributed_at": "2026-09-01", "seat": "Naya 4"},
]


def _setup(tmp_path, notes, files):
    notes_p = tmp_path / "notes.json"
    notes_p.write_text(json.dumps({"notes": notes}), encoding="utf-8")
    aroot = tmp_path / "artifacts"
    aroot.mkdir()
    for name, text in files:
        p = aroot / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return notes_p, aroot


def _run(tmp_path, notes, files, **kwargs):
    notes_p, aroot = _setup(tmp_path, notes, files)
    argv = ["--notes-json", str(notes_p), "--artifacts-root", str(aroot)]
    for k, v in kwargs.items():
        argv += [f"--{k.replace('_', '-')}", str(v)]
    return csg.main(argv)


def _header(seat=None, date=None):
    lines = ["---"]
    if seat:
        lines.append(f"seat: {seat}")
    if date:
        lines.append(f"date: {date}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def test_cross_seat_citation_counts(tmp_path):
    rc = _run(
        tmp_path, NOTES[:1],
        [("brief.md", _header("Naya 2", "2026-09-15") + "Built on SN-0600.\n")],
        threshold=0.25,
    )
    assert rc == 0


def test_same_seat_citation_does_not_count(tmp_path):
    rc = _run(
        tmp_path, NOTES[:1],
        [("mine.md", _header("Naya 4", "2026-09-15") + "Cites SN-0600 myself.\n")],
        threshold=0.25,
    )
    assert rc == 1  # 0/1 < 0.25


def test_citation_outside_window_does_not_count(tmp_path):
    rc = _run(
        tmp_path, NOTES[:1],
        [("late.md", _header("Naya 2", "2026-12-01") + "Late to SN-0600.\n")],
        threshold=0.25, reuse_window_days=60,  # contributed 09-01, cited 12-01
    )
    assert rc == 1


def test_citation_before_contribution_does_not_count(tmp_path):
    rc = _run(
        tmp_path, NOTES[:1],
        [("early.md", _header("Naya 2", "2026-08-01") + "SN-0600 before it existed.\n")],
        threshold=0.25,
    )
    assert rc == 1


def test_undated_file_is_reported_not_counted(tmp_path):
    report_p = tmp_path / "report.json"
    notes_p, aroot = _setup(
        tmp_path, NOTES[:1],
        [("nodate.md", _header("Naya 2") + "Uses SN-0600.\n")],
    )
    rc = csg.main([
        "--notes-json", str(notes_p), "--artifacts-root", str(aroot),
        "--threshold", "0.25", "--report-out", str(report_p),
    ])
    assert rc == 1
    report = json.loads(report_p.read_text(encoding="utf-8"))
    assert report["notes"][0]["reused_cross_seat"] is False
    assert any(f["path"] == "nodate.md" for f in report["undated_citing_files"])


def test_unattributed_file_is_reported_not_counted(tmp_path):
    report_p = tmp_path / "report.json"
    notes_p, aroot = _setup(
        tmp_path, NOTES[:1],
        [("anon.md", _header(date="2026-09-15") + "Uses SN-0600.\n")],
    )
    rc = csg.main([
        "--notes-json", str(notes_p), "--artifacts-root", str(aroot),
        "--threshold", "0.25", "--report-out", str(report_p),
    ])
    assert rc == 1
    report = json.loads(report_p.read_text(encoding="utf-8"))
    assert report["notes"][0]["reused_cross_seat"] is False
    assert any(f["path"] == "anon.md" for f in report["unattributed_citing_files"])


def test_unknown_sn_id_does_not_move_rate(tmp_path):
    rc = _run(
        tmp_path, NOTES[:1],
        [("other.md", _header("Naya 2", "2026-09-15") + "About SN-9999.\n")],
        threshold=0.25,
    )
    assert rc == 1  # SN-9999 isn't in the manifest; SN-0600 has no reuse


def test_rate_math_two_notes_one_reused(tmp_path):
    report_p = tmp_path / "report.json"
    notes_p, aroot = _setup(
        tmp_path, NOTES,
        [("use.md", _header("Naya 3", "2026-09-20") + "Applies SN-0600.\n")],
    )
    rc = csg.main([
        "--notes-json", str(notes_p), "--artifacts-root", str(aroot),
        "--threshold", "0.5", "--report-out", str(report_p),
    ])
    assert rc == 0  # 1/2 = 0.5 >= 0.5
    report = json.loads(report_p.read_text(encoding="utf-8"))
    by_id = {n["sn_id"]: n for n in report["notes"]}
    assert by_id["SN-0600"]["reused_cross_seat"] is True
    assert by_id["SN-0600"]["citing_seats"] == ["Naya 3"]
    assert by_id["SN-0601"]["reused_cross_seat"] is False
    assert report["rate"] == 0.5


def test_duplicate_sn_id_is_exit_2(tmp_path, capsys):
    notes_p = tmp_path / "notes.json"
    notes_p.write_text(json.dumps({"notes": [
        {"sn_id": "SN-0600", "contributed_at": "2026-09-01", "seat": "Naya 4"},
        {"sn_id": "SN-0600", "contributed_at": "2026-09-02", "seat": "Naya 2"},
    ]}), encoding="utf-8")
    aroot = tmp_path / "artifacts"
    aroot.mkdir()
    rc = csg.main(["--notes-json", str(notes_p), "--artifacts-root", str(aroot)])
    assert rc == 2


def test_bad_threshold_is_exit_2(tmp_path, capsys):
    notes_p, aroot = _setup(tmp_path, NOTES[:1], [])
    rc = csg.main([
        "--notes-json", str(notes_p), "--artifacts-root", str(aroot),
        "--threshold", "0",
    ])
    assert rc == 2

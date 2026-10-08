#!/usr/bin/env python3
"""Tests for tools/reporting/pdf_report.py.

All data is synthetic — no network, no Supabase, no GitHub.
Run: pytest tools/reporting/tests/test_pdf_report.py -q
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pdf_report import (  # noqa: E402
    _decisions,
    _headline,
    _score_color,
    _single_priority,
    _top_misses,
    _top_wins,
    build_pdf,
)
from report_generator import (  # noqa: E402
    TEAM_STRUCTURE,
    Item,
    ReportData,
    ScorePoint,
)

GREEN = "green-ish"
import reportlab.lib.colors as _c  # noqa: E402


def _now():
    return dt.datetime(2026, 10, 8, 14, 36, tzinfo=dt.timezone.utc)


def _sample_data() -> ReportData:
    now = _now()
    areas_scores = [
        ("Learning", 5.0, "authoritative"),
        ("Truth", 9.0, "claim"),
        ("Memory & Continuity", 8.0, "claim"),
        ("Human Value", 7.5, "claim"),
        ("Retrieval", 7.0, "claim"),
        ("Action & Execution", 8.7, "claim"),
        ("Authority & Governance", 8.0, "claim"),
        ("Safety", 7.5, "claim"),
        ("Voice & Experience", 8.5, "claim"),
        ("Production Readiness", 4.0, "claim"),
        ("Successor Reuse", 6.0, "claim"),
    ]
    scores = [ScorePoint(area=a, score=s, as_of=now, source="test",
                         status=st)
              for a, s, st in areas_scores]
    return ReportData(
        scores=scores,
        previous_scores={a: s - 0.5 for a, s, _ in areas_scores
                         if a != "Learning"},
        holes=[
            Item("Learning pipeline jammed: 13 candidates stuck",
                 "learn-builder", priority=9),
            Item("Supabase 401 on read-only queries", "memory:2026-10-08",
                 priority=7),
        ],
        achievements=[
            Item("Truth crossed 9.0: elevation audit landed",
                 "truth-builder"),
            Item("Memory metabolism built, 17/17 tests",
                 "memory-builder"),
            Item("Safety closed ACT bypass of harm gates",
                 "safety-builder"),
        ],
        next_actions=[
            Item("Write scorecard receipts for 13 candidates",
                 "learn-builder"),
        ],
        intelligence=[
            Item("Lesson: pin reconciled scores, never overwrite",
                 "memory:2026-10-08"),
        ],
        supabase_snapshot={"counts": {"CANDIDATE": 36, "ACTIVE": 107}},
        github_snapshot={"prs": [{"number": 1, "merged": True,
                                  "state": "closed", "title": "t1"},
                                 {"number": 2, "merged": False,
                                  "state": "open", "title": "t2"}],
                         "comments": [{}, {}, {}]},
        generated_at=now,
        since=now - dt.timedelta(hours=1),
        window_label="hourly",
    )


def _pdf_text(path: str) -> str:
    """Extract text from the PDF for assertions (pypdf if present,
    else pdfminer-free fallback via reportlab? no — use pypdf)."""
    try:
        from pypdf import PdfReader
    except ImportError:
        pytest.skip("pypdf not installed")
    reader = PdfReader(path)
    return "\n".join(p.extract_text() or "" for p in reader.pages)


@pytest.fixture()
def sample_pdf(tmp_path):
    pytest.importorskip("pypdf")
    out = str(tmp_path / "report.pdf")
    build_pdf(_sample_data(), "hourly", out)
    assert Path(out).exists()
    assert Path(out).stat().st_size > 5_000
    return out


def test_pdf_generates_and_has_pages(sample_pdf):
    from pypdf import PdfReader
    reader = PdfReader(sample_pdf)
    assert len(reader.pages) >= 1


def test_pdf_contains_title_and_timestamp(sample_pdf):
    text = _pdf_text(sample_pdf)
    assert "Team Naya Intelligence Report" in text
    assert "2026-10-08 14:36 UTC" in text
    assert "HOURLY" in text


def test_pdf_contains_all_nine_teams(sample_pdf):
    text = _pdf_text(sample_pdf)
    for t in TEAM_STRUCTURE:
        assert t["name"] in text, f"missing team {t['name']}"


def test_pdf_contains_scores(sample_pdf):
    text = _pdf_text(sample_pdf)
    # Spot-check several scores and the authoritative tag.
    assert "5.0" in text
    assert "9.0" in text
    assert "authoritative" in text
    assert "PROVE THAT THE BRAIN LEARNS" in text


def test_pdf_numbered_sections(sample_pdf):
    text = _pdf_text(sample_pdf)
    for n in ("1 · Scorecard", "2 · What got done",
              "3 · Where we're winning", "4 · Where we're missing",
              "5 · Decisions needed", "6 · Single priority"):
        assert n in text, f"missing section {n}"


def test_score_color_thresholds():
    assert _score_color(9.0).hexval() == _c.HexColor("#15803d").hexval()
    assert _score_color(9.5).hexval() == _c.HexColor("#15803d").hexval()
    assert _score_color(7.0).hexval() == _c.HexColor("#b45309").hexval()
    assert _score_color(8.9).hexval() == _c.HexColor("#b45309").hexval()
    assert _score_color(4.0).hexval() == _c.HexColor("#b91c1c").hexval()


def test_headline_mentions_movement():
    data = _sample_data()
    from report_generator import group_by_team
    sections, _ = group_by_team(data)
    hl = _headline(data, sections)
    # previous_scores fixture has every area 0.5 below current: some
    # movement must be named, with an arrow between old and new.
    assert "→" in hl and any(a in hl for a, _, _ in
                             [("Truth", 0, 0), ("Voice & Experience", 0, 0),
                              ("Memory & Continuity", 0, 0)])


def test_headline_empty_data():
    data = ReportData(window_label="hourly")
    hl = _headline(data, [])
    assert hl  # never empty


def test_top_wins_and_misses_bounded():
    from report_generator import group_by_team
    data = _sample_data()
    sections, unassigned = group_by_team(data)
    assert len(_top_wins(sections)) <= 6
    assert len(_top_misses(sections, unassigned)) <= 6


def test_single_priority_falls_back():
    data = ReportData(window_label="hourly")
    assert _single_priority([], {})  # never empty


def test_decisions_scan():
    from report_generator import group_by_team
    data = _sample_data()
    data.holes.append(Item("Merge needs Shawn's word (Scorecard Law)",
                           "learn-builder"))
    sections, unassigned = group_by_team(data)
    found = _decisions(sections, unassigned)
    assert any("Shawn" in it.text for _, it in found)


def test_pdf_empty_data_renders_honestly(tmp_path):
    pytest.importorskip("pypdf")
    out = str(tmp_path / "empty.pdf")
    data = ReportData(window_label="hourly",
                      generated_at=_now(),
                      since=_now() - dt.timedelta(hours=1))
    build_pdf(data, "hourly", out)
    text = _pdf_text(out)
    assert "Team Naya Intelligence Report" in text
    # Honest empties, not crashes.
    assert "Nothing recorded this window" in text or \
        "No recorded actions" in text or "none recorded" in text.lower()

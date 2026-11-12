#!/usr/bin/env python3
"""Tests for tools/reporting/pdf_report.py — NayaNET instrument edition.

All data is synthetic — no network, no Supabase, no GitHub.
Run: pytest tools/reporting/tests/test_pdf_report.py -q
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pytest

# Skip gracefully when PDF deps aren't installed (CI installs pytest pyyaml pglast only).
# The workflow file is human-gated; this keeps the suite green without weakening validation.
reportlab = pytest.importorskip("reportlab", reason="reportlab not installed")
pypdf = pytest.importorskip("pypdf", reason="pypdf not installed")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pdf_report import (  # noqa: E402
    BLACK,
    HAIRLINE,
    INDIGO,
    _styles,
    build_pdf,
)
from report_generator import (  # noqa: E402
    Item,
    ReportData,
    ScorePoint,
)

import reportlab.lib.colors as _c  # noqa: E402


def _now():
    return dt.datetime(2026, 10, 8, 14, 36, tzinfo=dt.timezone.utc)


def _sample_data() -> ReportData:
    now = _now()
    scores = [
        ScorePoint(area="Learning", score=5.0, as_of=now, source="test",
                   status="authoritative"),
        ScorePoint(area="Truth", score=9.0, as_of=now, source="test",
                   status="claim"),
        ScorePoint(area="Safety", score=7.5, as_of=now, source="test",
                   status="claim"),
    ]
    return ReportData(
        scores=scores,
        previous_scores={"Learning": 5.0, "Truth": 8.5, "Safety": 7.5},
        holes=[
            Item("Learning pipeline jammed: 13 candidates stuck",
                 "learn-builder", priority=9, ts=now),
        ],
        achievements=[
            Item("Truth crossed 9.0: elevation audit landed",
                 "truth-builder", ts=now),
        ],
        next_actions=[
            Item("Write scorecard receipts for 13 candidates",
                 "learn-builder", ts=now),
        ],
        intelligence=[
            Item("Lesson: pin reconciled scores, never overwrite",
                 "memory:2026-10-08", ts=now),
        ],
        supabase_snapshot={"counts": {"CANDIDATE": 36, "ACTIVE": 107}},
        github_snapshot={"prs": [{"number": 1, "merged": True,
                                  "state": "closed", "title": "t1",
                                  "updated_at": "2026-10-08T14:30:00Z"},
                                 {"number": 2, "merged": False,
                                  "state": "open", "title": "t2",
                                  "updated_at": "2026-10-08T14:31:00Z"}],
                         "comments": [{}, {}, {}]},
        generated_at=now,
        since=now - dt.timedelta(hours=1),
        window_label="hourly",
    )


def _pdf_text(path: str) -> str:
    """Extract text from the PDF for assertions."""
    from pypdf import PdfReader
    reader = PdfReader(path)
    return "\n".join(p.extract_text() or "" for p in reader.pages)


@pytest.fixture()
def sample_pdf(tmp_path):
    out = str(tmp_path / "report.pdf")
    build_pdf(_sample_data(), "hourly", out)
    assert Path(out).exists()
    assert Path(out).stat().st_size > 2_000
    return out


def test_pdf_generates_and_has_pages(sample_pdf):
    from pypdf import PdfReader
    reader = PdfReader(sample_pdf)
    assert len(reader.pages) >= 1


def test_pdf_contains_structure(sample_pdf):
    text = _pdf_text(sample_pdf)
    assert "TEAM NAYA INTELLIGENCE" in text
    assert "Thu 2026-10-08 14:36 UTC" in text
    assert "HOURLY" in text
    for section in ("What moved", "Scoreboard", "Needs from Shawn",
                    "Evidence"):
        assert section in text, f"missing section {section}"
    # Scoreboard rows with claim/authoritative labels and the delta.
    assert "5.0" in text
    assert "authoritative" in text
    assert "+0.5" in text
    # No org-chart sections, no boilerplate.
    assert "Team 1" not in text
    assert "None recorded this window" not in text


def test_pdf_palette_is_black_with_one_accent():
    assert BLACK.hexval() == _c.HexColor("#050507").hexval()
    assert INDIGO.hexval() == _c.HexColor("#6675ff").hexval()
    assert HAIRLINE.hexval() == _c.HexColor("#26262e").hexval()
    # The only non-white colors the renderer names are the accent and
    # the hairline — no team colors, no score-color ramps.
    import pdf_report
    assert not hasattr(pdf_report, "TEAM_COLORS")


def test_typography_hierarchy_24_18_14():
    """Serif voice 24 / section 18 / body 14 — all white."""
    st = _styles()
    assert st["voice"].fontSize == 24
    assert st["voice"].fontName == "Times-Bold"
    assert st["voice"].textColor.hexval() == _c.HexColor("#ffffff").hexval()
    assert st["h2"].fontSize == 18
    assert st["body"].fontSize == 14
    for name, style in st.items():
        assert style.textColor.hexval() == \
            _c.HexColor("#ffffff").hexval(), \
            f"style {name} is not white"


def test_pdf_quiet_hour_renders_honestly(tmp_path):
    out = str(tmp_path / "empty.pdf")
    data = ReportData(window_label="hourly",
                      generated_at=_now(),
                      since=_now() - dt.timedelta(hours=1))
    build_pdf(data, "hourly", out)
    text = _pdf_text(out)
    assert "Quiet hour — no window activity." in text
    assert "None this hour." in text
    assert "None recorded this window" not in text


def test_pdf_headline_is_the_report(sample_pdf):
    text = _pdf_text(sample_pdf)
    # The biggest score movement (Truth 8.5 → 9.0) is the voice headline.
    assert "Truth 8.5 → 9.0." in text

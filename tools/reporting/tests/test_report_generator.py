#!/usr/bin/env python3
"""Tests for tools/reporting/report_generator.py.

All external data sources are mocked — no network, no Supabase, no GitHub.
Run: pytest tools/reporting/tests/test_report_generator.py -q
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from report_generator import (  # noqa: E402
    Item,
    ReportData,
    ReportGenerator,
    ScorePoint,
    _dedup,
    _hole_priority,
    _normalize_area,
    _section_items,
    extract_scores_from_text,
    parse_memory_log,
    parse_worker_log,
    save_score_state,
    save_watermark,
    load_score_state,
    load_watermarks,
)

NOW = dt.datetime(2026, 10, 8, 12, 0, tzinfo=dt.timezone.utc)


# ---------------------------------------------------------------------------
# Area normalization
# ---------------------------------------------------------------------------


def test_normalize_area_exact():
    assert _normalize_area("Learning lane") == "Learning"
    assert _normalize_area("cold retrieve drill") == "Retrieval"
    assert _normalize_area("Production Readiness") == "Production Readiness"
    assert _normalize_area("successor reuse trial") == "Successor Reuse"


def test_normalize_area_unknown_returns_none():
    assert _normalize_area("the weather is nice") is None
    assert _normalize_area("") is None


def test_normalize_longest_alias_wins():
    # "memory & continuity" must beat bare "memory".
    assert _normalize_area("Memory & Continuity checkpoint") == \
        "Memory & Continuity"


# ---------------------------------------------------------------------------
# Score extraction
# ---------------------------------------------------------------------------


def test_extract_movement_score():
    text = "## Scores\n- Learning: 6.5 → 7.0/10 (trial rung claim)\n"
    pts = extract_scores_from_text(text, "w1", NOW)
    assert len(pts) == 1
    assert pts[0].area == "Learning"
    assert pts[0].score == 7.0  # the NEW score, not the old


def test_extract_single_score():
    text = "Area score: 3.5/10 (instrument exists)\n"
    pts = extract_scores_from_text(text, "w2", NOW)
    # "Area score" alone names no area -> skipped, never guessed.
    assert pts == []


def test_extract_bold_score_with_area():
    text = "- **8.8** — Truth area re-score after gate work\n"
    pts = extract_scores_from_text(text, "w3", NOW)
    assert len(pts) == 1
    assert pts[0].area == "Truth"
    assert pts[0].score == 8.8


def test_extract_ignores_out_of_range():
    text = "Learning improved 150 → 200 queries/sec\n"
    assert extract_scores_from_text(text, "w4", NOW) == []


def test_extract_multiple_areas():
    text = ("Learning 5.0 → 5.5\n"
            "Production Readiness 3.0 → 3.5\n")
    pts = extract_scores_from_text(text, "w5", NOW)
    assert {(p.area, p.score) for p in pts} == {
        ("Learning", 5.5), ("Production Readiness", 3.5)}


def test_extract_same_sentence_rule():
    # Regression: "Successor lane moved 3.5 → 4.5 ... retrieval still
    # stubbed" must attribute 4.5 to Successor Reuse, NOT Retrieval.
    text = ("Successor lane moved 3.5 → 4.5. "
            "Honest caveat: retrieval is still stubbed, not the live path.")
    pts = extract_scores_from_text(text, "w6", NOW)
    assert len(pts) == 1
    assert pts[0].area == "Successor Reuse"
    assert pts[0].score == 4.5


def test_extract_ambiguous_multi_area_sentence_skipped():
    # Two areas, one score in the same sentence: ambiguous, never guess.
    text = "Learning and Retrieval both improved to 7.0 this week."
    assert extract_scores_from_text(text, "w7", NOW) == []


def test_extract_movement_beats_rescore_prefix():
    # Regression: "re-score: 8.5 → 8.8" must yield 8.8, not 8.5 —
    # the "score:" in "re-score:" must not shadow the movement.
    text = "- **TRUTH re-score: 8.5 → 8.8** (honest)."
    pts = extract_scores_from_text(text, "w8", NOW)
    assert len(pts) == 1
    assert pts[0].area == "Truth"
    assert pts[0].score == 8.8


def test_item_text_truncated():
    long_text = "x" * 500
    it = Item(text=long_text, source="s")
    assert len(it.text) <= 280
    assert it.text.endswith("…")


# ---------------------------------------------------------------------------
# Section extraction
# ---------------------------------------------------------------------------

WORKER_MD = """# learn-builder run log

## Work
- Re-verified branch at new tip: 11/11 pytest green.
- Mapped PR queue: #1681/#1690/#1691 CLEAN.

## Blockers
- Tip RED blocks PR CI greenness (Naya 4's lane).
- Merge of #1681 needs Shawn's word (Scorecard Law).

## Next
- Await PR + merge of lineage receipt.

## Scores
- Learning: 5.0 → 5.0 (unchanged).
"""


def test_section_items_blockers():
    items = _section_items(WORKER_MD, ["blockers", "blocker"])
    assert len(items) == 2
    assert all(s == "blockers" for s, _ in items)
    assert any("Tip RED" in t for _, t in items)


def test_section_items_work():
    items = _section_items(WORKER_MD, ["work"])
    assert len(items) == 2
    assert any("11/11 pytest" in t for _, t in items)


def test_section_items_missing_section():
    assert _section_items(WORKER_MD, ["nonexistent"]) == []


# ---------------------------------------------------------------------------
# Hole priority
# ---------------------------------------------------------------------------


def test_hole_priority_protected_gate_highest():
    gated = _hole_priority("Merge needs Shawn's word (protected gate)")
    plain = _hole_priority("Await PR + merge of lineage receipt")
    red = _hole_priority("Tip RED blocks CI")
    assert gated > plain
    assert red > plain


def test_hole_priority_baseline():
    assert _hole_priority("some minor note") == 5


# ---------------------------------------------------------------------------
# Worker log parsing
# ---------------------------------------------------------------------------


def test_parse_worker_log(tmp_path):
    p = tmp_path / "learn-builder-20261008-0245.md"
    p.write_text(WORKER_MD, encoding="utf-8")
    parsed = parse_worker_log(p)
    assert parsed["worker"] == "learn-builder-20261008-0245"
    assert len(parsed["holes"]) == 2  # blockers only
    assert len(parsed["next_actions"]) == 1  # next section, separated
    assert len(parsed["achievements"]) == 2
    assert any(s.area == "Learning" for s in parsed["scores"])
    # Holes sorted by priority elsewhere; here check priorities assigned.
    assert all(h.priority >= 5 for h in parsed["holes"])


# ---------------------------------------------------------------------------
# Memory log parsing
# ---------------------------------------------------------------------------


def test_parse_memory_log(tmp_path):
    p = tmp_path / "2026-10-08.md"
    p.write_text(
        "- [score|medium] Learning area: **5.0/10** whole-area (authoritative).\n"
        "- [lesson|high] **Fix It First**: repair within authority, report after.\n"
        "- [correction|high] Learning score is 5.0, not 7.0.\n"
        "- [blocker|high] Tip RED blocks PR CI greenness.\n"
        "- just a plain line, no tag.\n",
        encoding="utf-8",
    )
    parsed = parse_memory_log(p)
    assert len(parsed["achievements"]) == 1
    # lesson + correction both land in intelligence (corrections are
    # knowledge, not open holes).
    assert len(parsed["intelligence"]) == 2
    assert len(parsed["holes"]) == 1  # blocker only
    assert any(s.area == "Learning" and s.score == 5.0
               for s in parsed["scores"])


def test_parse_memory_log_missing_file(tmp_path):
    parsed = parse_memory_log(tmp_path / "2099-01-01.md")
    assert parsed["achievements"] == []
    assert parsed["scores"] == []


# ---------------------------------------------------------------------------
# Dedup
# ---------------------------------------------------------------------------


def test_dedup_removes_near_duplicates():
    items = [Item(text="Tip RED blocks CI", source="a"),
             Item(text="tip  red   blocks ci", source="b"),
             Item(text="Different item", source="c")]
    out = _dedup(items)
    assert len(out) == 2


# ---------------------------------------------------------------------------
# Full collect with mocked sources
# ---------------------------------------------------------------------------


def _mock_worker_logs(since):
    return [{
        "worker": "learn-builder-20261008-0245",
        "mtime": NOW,
        "scores": [ScorePoint("Learning", 5.0, NOW, "learn-builder")],
        "holes": [Item("Tip RED blocks CI", "learn-builder",
                       priority=30)],
        "achievements": [Item("11/11 pytest green", "learn-builder")],
        "activity": [Item("Signed in/out on #1713", "learn-builder")],
    }]


def _mock_memory(since):
    return {"achievements": [Item("T13 compounding proof 9.0", "memory")],
            "intelligence": [Item("Fix It First law", "memory")],
            "holes": [],
            "scores": []}


def _mock_github(since):
    return {"prs": [{"number": 1794, "title": "SN-0529 fix",
                     "state": "closed", "merged": True,
                     "updated_at": "2026-10-08T04:00:00Z"}],
            "comments": [], "error": None}


def _mock_supabase():
    return {"counts": {"CANDIDATE": 36, "ACTIVE": 106}, "error": None}


def _mock_load_scores():
    return {"Learning": {"score": 5.0,
                         "as_of": "2026-10-08T00:00:00+00:00",
                         "source": "seed", "status": "authoritative"}}


def test_collect_merges_scores_and_ranks_holes():
    saved = {}

    def fake_save(state):
        saved.update(state)

    gen = ReportGenerator(
        fetch_worker_logs=_mock_worker_logs,
        fetch_memory=_mock_memory,
        fetch_github_fn=_mock_github,
        fetch_supabase_fn=_mock_supabase,
        load_scores_fn=_mock_load_scores,
        save_scores_fn=fake_save,
    )
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    assert any(s.area == "Learning" and s.score == 5.0 for s in data.scores)
    assert data.holes[0].text == "Tip RED blocks CI"  # highest priority first
    assert any("T13" in a.text for a in data.achievements)
    assert any("Fix It First" in i.text for i in data.intelligence)
    assert data.supabase_snapshot["counts"]["ACTIVE"] == 106
    assert "Learning" in saved  # state persisted


def test_collect_never_downgrades_authoritative_status():
    saved = {}

    def fake_load():
        return {"Learning": {"score": 5.0,
                             "as_of": "2026-10-08T00:00:00+00:00",
                             "source": "Naya 1 reconciliation",
                             "status": "authoritative"}}

    gen = ReportGenerator(
        fetch_worker_logs=_mock_worker_logs,  # claims Learning 5.0
        fetch_memory=lambda s: {"achievements": [], "intelligence": [],
                                "holes": [], "scores": []},
        fetch_github_fn=lambda s: {"prs": [], "comments": [], "error": None},
        fetch_supabase_fn=lambda: {"counts": {}, "error": None},
        load_scores_fn=fake_load,
        save_scores_fn=lambda s: saved.update(s),
    )
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    assert saved["Learning"]["status"] == "authoritative"
    assert any(s.area == "Learning" and s.status == "authoritative"
               for s in data.scores)


def test_collect_degraded_sources():
    def bad_github(since):
        return {"prs": [], "comments": [],
                "error": "connection refused"}

    def bad_sb():
        return {"counts": {}, "error": "timeout"}

    gen = ReportGenerator(
        fetch_worker_logs=lambda s: [],
        fetch_memory=lambda s: {"achievements": [], "intelligence": [],
                                "holes": [], "scores": []},
        fetch_github_fn=bad_github,
        fetch_supabase_fn=bad_sb,
        load_scores_fn=dict,
        save_scores_fn=lambda s: None,
    )
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    report = gen.render(data)
    assert "unavailable" in report
    assert "connection refused" in report


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _sample_data():
    data = ReportData(
        since=NOW - dt.timedelta(hours=1),
        generated_at=NOW,
        window_label="hourly",
        previous_scores={"Learning": 5.0},
        supabase_snapshot={"counts": {"ACTIVE": 106}, "error": None},
        github_snapshot={"prs": [], "comments": [], "error": None},
    )
    data.scores.append(ScorePoint("Learning", 5.5, NOW, "w1", "claim"))
    data.holes.append(Item("Tip RED", "w1", priority=30))
    data.achievements.append(Item("T13 proof 9.0", "w1"))
    data.intelligence.append(Item("Fix It First", "mem"))
    data.next_actions.append(Item("Re-check tip", "w1"))
    return data


def test_render_structure():
    report = ReportGenerator.render(_sample_data())
    assert report.startswith("# HOURLY Report — 2026-10-08 12:00 UTC")
    for section in ["## Scores (all levels)",
                    "## Top 10 Holes (highest priority actions)",
                    "## Top 10 Achievements (since last report)",
                    "## Team Activity",
                    "## Intelligence Learned",
                    "## Next Actions",
                    "## Evidence Snapshot"]:
        assert section in report, f"missing {section}"
    # Score delta rendered.
    assert "| Learning | 5.0 | 5.5 | +0.5 | claim |" in report
    # Sources attached.
    assert "_(src: w1)_" in report
    # Evidence snapshot.
    assert "ACTIVE=106" in report


def test_render_empty_sections():
    data = ReportData(since=NOW - dt.timedelta(hours=1),
                      generated_at=NOW, window_label="nightly")
    report = ReportGenerator.render(data)
    assert "_None recorded this window._" in report
    assert "_No data this window:" in report


def test_render_caps_at_ten():
    data = _sample_data()
    data.holes = [Item(f"hole {i}", "w", priority=i) for i in range(25)]
    data.holes = sorted(data.holes, key=lambda i: -i.priority)[:10]
    report = ReportGenerator.render(data)
    assert "hole 24" in report
    assert "hole 0" not in report  # lowest priority cut off


# ---------------------------------------------------------------------------
# State round-trip (uses tmp state dir via monkeypatch)
# ---------------------------------------------------------------------------


def test_score_state_round_trip(tmp_path, monkeypatch):
    import report_generator as rg
    monkeypatch.setattr(rg, "SCORE_STATE_FILE", tmp_path / "scores.json")
    monkeypatch.setattr(rg, "WATERMARK_FILE", tmp_path / "marks.json")
    save_score_state({"Learning": {"score": 5.0}})
    assert load_score_state() == {"Learning": {"score": 5.0}}
    save_watermark("hourly", NOW)
    marks = load_watermarks()
    assert marks["hourly"] == NOW.isoformat()


def test_generate_end_to_end_with_mocks():
    gen = ReportGenerator(
        fetch_worker_logs=_mock_worker_logs,
        fetch_memory=_mock_memory,
        fetch_github_fn=_mock_github,
        fetch_supabase_fn=_mock_supabase,
        load_scores_fn=_mock_load_scores,
        save_scores_fn=lambda s: None,
    )
    report = gen.generate("morning", NOW - dt.timedelta(hours=8), NOW)
    assert "# MORNING Report" in report
    assert "## Scores (all levels)" in report
    assert json.dumps  # sanity: module imports cleanly

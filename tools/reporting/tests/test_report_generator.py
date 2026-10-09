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
    AREAS,
    AREA_TO_TEAM,
    TEAM_STRUCTURE,
    Item,
    ReportData,
    ReportGenerator,
    ScorePoint,
    TeamSection,
    _dedup,
    _hole_priority,
    _normalize_area,
    _section_items,
    action_plan_text,
    attribute_team,
    extract_scores_from_text,
    group_by_team,
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
    # Nine team sections, in order.
    for i, team in enumerate(TEAM_STRUCTURE, 1):
        header = f"## Team {i}: {team['name']} ({team['manager']})"
        assert header in report, f"missing {header}"
    for section in ["**Holes (top 3):**",
                    "**Priorities (top 3):**",
                    "**Action plan to 10:**",
                    "**This hour:**",
                    "## Cross-team signals",
                    "## Evidence Snapshot"]:
        assert section in report, f"missing {section}"
    # Learning score lands in the Learning team section with delta.
    assert "Learning 5.5 (claim, Δ +0.5)" in report
    # Sources attached.
    assert "_(src: w1)_" in report
    # Evidence snapshot.
    assert "ACTIVE=106" in report


def test_render_empty_sections():
    data = ReportData(since=NOW - dt.timedelta(hours=1),
                      generated_at=NOW, window_label="nightly")
    report = ReportGenerator.render(data)
    assert "_None recorded this window._" in report
    assert "_Nothing recorded this window._" in report
    assert "_All items attributed to teams._" in report
    # Cross-cutting teams show no direct area score.
    assert "cross-cutting — no direct area score." in report


def test_render_caps_per_team():
    data = _sample_data()
    # 25 holes from the same worker: all attribute to Learning.
    data.holes = [Item(f"Learning hole {i}", "learn-builder", priority=i)
                  for i in range(25)]
    report = ReportGenerator.render(data)
    # Top-3 per team: highest priorities shown...
    assert "Learning hole 24" in report
    assert "Learning hole 23" in report
    assert "Learning hole 22" in report
    # ...rest cut off.
    assert "Learning hole 21" not in report
    assert "Learning hole 0" not in report


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
    assert "## Team 1: Learning (Naya 4)" in report
    assert "## Team 9: Innovation (Naya 3)" in report
    assert "## Cross-team signals" in report
    assert json.dumps  # sanity: module imports cleanly


# ---------------------------------------------------------------------------
# Score-extraction accuracy guards (2026-10-08: first-run monitoring caught
# two live mis-extractions — aspirational "3.0→10.0 drive" scored as 10.0,
# and a stale 2026-10-07 6.5 overwrote the current 7.0 via mtime)
# ---------------------------------------------------------------------------


def test_aspirational_drive_not_extracted():
    pts = extract_scores_from_text(
        "Production Readiness: issue #1771 was created for the 3.0→10.0 drive.",
        source="t", as_of=NOW)
    assert pts == []


def test_aspirational_must_move_not_extracted():
    pts = extract_scores_from_text(
        "Shawn said Production Readiness must move from 3.0 to 10.",
        source="t", as_of=NOW)
    assert pts == []


def test_ten_point_zero_never_extracted():
    pts = extract_scores_from_text(
        "Honest score: Production Readiness **10.0/10**.",
        source="t", as_of=NOW)
    assert pts == []


def test_ten_point_zero_movement_never_extracted():
    pts = extract_scores_from_text(
        "Production Readiness moved 3.5 → 10.0 this shift.",
        source="t", as_of=NOW)
    assert pts == []


def test_genuine_score_still_extracted():
    pts = extract_scores_from_text(
        "Honest score: Retrieval **6.5/10** (ratified baseline stands).",
        source="t", as_of=NOW)
    assert len(pts) == 1 and pts[0].score == 6.5


def test_memory_as_of_uses_filename_date(tmp_path):
    from report_generator import _memory_as_of
    p = tmp_path / "2026-10-07.md"
    p.write_text("x")
    as_of = _memory_as_of(p)
    assert (as_of.year, as_of.month, as_of.day) == (2026, 10, 7)
    assert as_of.tzinfo == dt.timezone.utc


def test_memory_as_of_falls_back_for_non_date(tmp_path):
    from report_generator import _memory_as_of
    p = tmp_path / "notes.md"
    p.write_text("x")
    before = dt.datetime.now(dt.timezone.utc)
    as_of = _memory_as_of(p)
    after = dt.datetime.now(dt.timezone.utc)
    assert before <= as_of <= after


def test_newer_memory_file_beats_older_despite_mtime(tmp_path):
    # The stale-score overwrite: 2026-10-07.md says 6.5, 2026-10-08.md
    # says 7.0. Newer-dated file must win even if mtimes are reversed.
    old = tmp_path / "2026-10-07.md"
    new = tmp_path / "2026-10-08.md"
    old.write_text("Honest score: Retrieval **6.5/10**.")
    new.write_text("Cold Retrieve moved 6.5 → 7.0 on the audit branch.")
    import os
    now_ts = dt.datetime.now().timestamp()
    os.utime(old, (now_ts, now_ts))          # old file touched LAST
    os.utime(new, (now_ts - 3600, now_ts - 3600))
    old_pts = parse_memory_log(old)["scores"]
    new_pts = parse_memory_log(new)["scores"]
    assert old_pts[0].score == 6.5
    assert new_pts[0].score == 7.0
    assert new_pts[0].as_of > old_pts[0].as_of


# ---------------------------------------------------------------------------
# 2026-10-08 (second pass, same run): bare-"production" alias removed and
# bold qualifier words allowed — the deck's 8.5/10 ("production 9" sub-score)
# must not be attributed to Production Readiness, while the honest
# "**3.0/10 unchanged**" statement must be extracted.
# ---------------------------------------------------------------------------


def test_bare_production_alias_not_an_area():
    pts = extract_scores_from_text(
        "Naya 5 scored it **8.5/10**: narrative 9, clarity 8.5, memorable "
        "lines 9, production 9, doctrinal accuracy 8.",
        source="t", as_of=NOW)
    assert pts == []


def test_bold_score_with_qualifier_extracted():
    pts = extract_scores_from_text(
        "Production Readiness area: **3.0/10 unchanged** (honest).",
        source="t", as_of=NOW)
    assert len(pts) == 1
    assert pts[0].area == "Production Readiness" and pts[0].score == 3.0


def test_full_area_name_still_matches():
    pts = extract_scores_from_text(
        "Production Readiness **3.5/10** (chain red).",
        source="t", as_of=NOW)
    assert len(pts) == 1 and pts[0].score == 3.5


def test_single_re_with_topic_phrase():
    # "Honest score: Retrieval 7.0/10 CLAIM" — the current live statement
    # missed by the old pattern, which let a stale 6.5 stand.
    pts = extract_scores_from_text(
        "Honest score: Retrieval 7.0/10 CLAIM (was 6.5).",
        source="t", as_of=NOW)
    assert len(pts) == 1
    assert pts[0].area == "Retrieval" and pts[0].score == 7.0


def test_single_re_still_rejects_rescore_and_scorecard():
    # "re-score" must not double-count via the single pattern; the movement
    # (8.5 → 8.8) wins and yields exactly one point.
    pts = extract_scores_from_text(
        "TRUTH re-score: 8.5 → 8.8 done.", source="t", as_of=NOW)
    assert [p.score for p in pts if p.area == "Truth"] == [8.8]


# ---------------------------------------------------------------------------
# Nine-team structure (2026-10-08): reports break down by team, not by
# flat area list. Shawn: "give me a briefing on each category."
# ---------------------------------------------------------------------------


def test_nine_teams_defined():
    assert len(TEAM_STRUCTURE) == 9
    names = [t["name"] for t in TEAM_STRUCTURE]
    assert names == [
        "Learning", "Brain/Memory", "Law/Governance",
        "Architecture/Engineering/Ops", "Evolution/Succession",
        "Interfaces/Hub", "Knowledge/Intelligence",
        "Proving/Verifying", "Innovation",
    ]


def test_every_area_maps_to_exactly_one_team():
    for area in AREAS:
        assert area in AREA_TO_TEAM, f"{area} has no team"
    # No area claimed twice.
    seen: dict[str, str] = {}
    for t in TEAM_STRUCTURE:
        for a in t["areas"]:
            assert a not in seen, f"{a} in two teams"
            seen[a] = t["name"]
    assert set(seen) == set(AREAS)


def test_cross_cutting_teams_have_no_areas():
    for t in TEAM_STRUCTURE:
        if t["name"] in ("Knowledge/Intelligence", "Innovation"):
            assert t["areas"] == []


def test_team_managers_match_roster():
    managers = {t["name"]: t["manager"] for t in TEAM_STRUCTURE}
    assert managers["Learning"] == "Naya 4"
    assert managers["Brain/Memory"] == "Naya 5"
    assert managers["Law/Governance"] == "Naya 2"
    assert managers["Evolution/Succession"] == "Naya 5"
    assert managers["Proving/Verifying"] == "Naya 1"


# ---------------------------------------------------------------------------
# Team attribution
# ---------------------------------------------------------------------------


def test_attribute_team_by_area_mention():
    it = Item("Tip RED blocks Retrieval CI", "learn-builder", priority=25)
    assert attribute_team(it, "hole") == "Architecture/Engineering/Ops"
    it2 = Item("Safety gate closed the ACT bypass", "safety-builder")
    assert attribute_team(it2, "achievement") == "Law/Governance"


def test_attribute_team_by_worker_prefix():
    # No area named: falls back to who did the work.
    it = Item("Tip RED blocks CI", "learn-builder", priority=25)
    assert attribute_team(it, "hole") == "Learning"
    it2 = Item("Fixed deck honesty", "voice-builder")
    assert attribute_team(it2, "achievement") == "Interfaces/Hub"
    it3 = Item("SR-P5 improved", "successor-builder")
    assert attribute_team(it3, "achievement") == "Evolution/Succession"


def test_attribute_team_area_beats_worker_prefix():
    # A learn-builder item ABOUT retrieval belongs to Arch/Eng/Ops,
    # not Learning — the subject wins over the author.
    it = Item("Retrieval probe 5/5 PASS", "learn-builder")
    assert attribute_team(it, "achievement") == "Architecture/Engineering/Ops"


def test_attribute_team_intelligence_defaults_to_knowledge():
    it = Item("Fix It First: repair it, then report what you did",
              "memory:2026-10-08")
    assert attribute_team(it, "intelligence") == "Knowledge/Intelligence"
    # But a lesson naming an area goes to that area's team.
    it2 = Item("Learning score is 5.0 authoritative, not 7.0",
               "memory:2026-10-08")
    assert attribute_team(it2, "intelligence") == "Learning"


def test_attribute_team_unassigned_not_guessed():
    it = Item("something vague happened", "unknown-source")
    assert attribute_team(it, "hole") is None
    assert attribute_team(it, "achievement") is None


def test_attribute_team_innovation_keyword():
    it = Item("Researched a new framework for the Hub", "memory:2026-10-08")
    assert attribute_team(it, "achievement") == "Innovation"


# ---------------------------------------------------------------------------
# Grouping
# ---------------------------------------------------------------------------


def _team_data():
    data = ReportData(since=NOW - dt.timedelta(hours=1),
                      generated_at=NOW, window_label="hourly",
                      previous_scores={})
    data.scores = [
        ScorePoint("Learning", 5.0, NOW, "pin", "authoritative"),
        ScorePoint("Truth", 9.0, NOW, "w", "claim"),
    ]
    data.holes = [
        Item("Learning pipeline jammed: 13 stuck", "learn-builder",
             priority=20),
        Item("mystery blocker", "???"),
    ]
    data.achievements = [
        Item("T13 proof 9.0", "learn-builder"),
    ]
    data.next_actions = [
        Item("Write scorecard receipts", "learn-builder"),
    ]
    data.intelligence = [
        Item("Fix It First law", "memory:2026-10-08"),
    ]
    return data


def test_group_by_team_order_and_scores():
    sections, unassigned = group_by_team(_team_data())
    assert [s.name for s in sections] == [t["name"] for t in TEAM_STRUCTURE]
    learning = sections[0]
    assert learning.manager == "Naya 4"
    assert [(s.area, s.score) for s in learning.scores] == [("Learning", 5.0)]
    proving = sections[7]
    assert [(s.area, s.score) for s in proving.scores] == [("Truth", 9.0)]
    # Cross-cutting team has no scores.
    ki = sections[6]
    assert ki.scores == []


def test_group_by_team_routes_items():
    sections, unassigned = group_by_team(_team_data())
    learning = sections[0]
    assert any("jammed" in h.text for h in learning.holes)
    assert any("receipts" in p.text for p in learning.priorities)
    assert any("T13" in a.text for a in learning.achievements)
    # The area-less lesson went to Knowledge/Intelligence's "This hour".
    ki = sections[6]
    assert any("Fix It First" in a.text for a in ki.achievements)
    # The truly unattributable hole surfaces under Cross-team signals.
    assert any("mystery" in h.text for h in unassigned["holes"])


def test_group_by_team_holes_sorted_by_priority():
    data = _team_data()
    data.holes = [
        Item("Learning minor note", "learn-builder", priority=5),
        Item("Learning pipeline jammed", "learn-builder", priority=20),
    ]
    sections, _ = group_by_team(data)
    assert sections[0].holes[0].priority == 20


# ---------------------------------------------------------------------------
# Action plan
# ---------------------------------------------------------------------------


def test_action_plan_names_top_hole_and_priority():
    sec = TeamSection(
        name="Learning", manager="Naya 4", feed="#1602",
        scores=[ScorePoint("Learning", 5.0, NOW, "pin", "authoritative")],
        holes=[Item("Pipeline jammed: 13 stuck", "w", priority=20)],
        priorities=[Item("Write scorecard receipts", "w")],
    )
    plan = action_plan_text(sec)
    assert "Pipeline jammed" in plan
    assert "Write scorecard receipts" in plan
    assert "independent verification" in plan


def test_action_plan_hold_when_above_nine():
    sec = TeamSection(
        name="Proving/Verifying", manager="Naya 1", feed="#1723",
        scores=[ScorePoint("Truth", 9.0, NOW, "w", "claim")],
    )
    plan = action_plan_text(sec)
    assert "hold 9.0+" in plan


def test_action_plan_empty_is_honest():
    sec = TeamSection(name="Innovation", manager="Naya 3", feed="#1607")
    plan = action_plan_text(sec)
    assert "No recorded actions this window" in plan


# ---------------------------------------------------------------------------
# Pinned Learning 5.0 survives the team restructure
# ---------------------------------------------------------------------------


def test_pinned_learning_in_team_section():
    saved = {}

    def fake_load():
        return {"Learning": {"score": 7.0,
                             "as_of": "2026-10-08T00:00:00+00:00",
                             "source": "stale", "status": "claim"}}

    gen = ReportGenerator(
        fetch_worker_logs=lambda s: [{
            "worker": "learn-builder", "mtime": NOW,
            "scores": [ScorePoint("Learning", 7.0, NOW, "learn-builder")],
            "holes": [], "achievements": [], "activity": [],
        }],
        fetch_memory=lambda s: {"achievements": [], "intelligence": [],
                                "holes": [], "scores": []},
        fetch_github_fn=lambda s: {"prs": [], "comments": [], "error": None},
        fetch_supabase_fn=lambda: {"counts": {}, "error": None},
        load_scores_fn=fake_load,
        save_scores_fn=lambda s: saved.update(s),
    )
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    sections, _ = group_by_team(data)
    learning = sections[0]
    assert len(learning.scores) == 1
    assert learning.scores[0].score == 5.0
    assert learning.scores[0].status == "authoritative"
    report = gen.render(data)
    assert "Learning 5.0 (authoritative" in report

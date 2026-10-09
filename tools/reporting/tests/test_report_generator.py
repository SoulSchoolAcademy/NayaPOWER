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
        "## Run notes — 00:08 UTC\n"
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
    # Section timestamps land on the items — nothing is timestamp-unknown.
    assert all(i.ts is not None for i in parsed["achievements"])
    assert parsed["achievements"][0].ts.hour == 0
    assert parsed["achievements"][0].ts.day == 8


def test_parse_memory_log_untimestamped_sections_yield_no_ts(tmp_path):
    # The freshness rule: a section header with no parseable time leaves
    # its items timestamp-unknown (ts None) — collect() drops them.
    p = tmp_path / "2026-10-08.md"
    p.write_text(
        "## UPDATE — scope notes (2026-10-08)\n"
        "- [event|high] Something happened at some point.\n",
        encoding="utf-8",
    )
    parsed = parse_memory_log(p)
    assert len(parsed["achievements"]) == 1
    assert parsed["achievements"][0].ts is None
    assert parsed["scores"] == []


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
        "ts": NOW,
        "scores": [ScorePoint("Learning", 5.0, NOW, "learn-builder")],
        "holes": [Item("Tip RED blocks CI", "learn-builder",
                       priority=30, ts=NOW)],
        "achievements": [Item("11/11 pytest green", "learn-builder",
                              ts=NOW)],
        "activity": [Item("Signed in/out on #1713", "learn-builder",
                          ts=NOW)],
    }]


def _mock_memory(since):
    return {"achievements": [Item("T13 compounding proof 9.0", "memory",
                                 ts=NOW)],
            "intelligence": [Item("Fix It First law", "memory", ts=NOW)],
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
    data.holes.append(Item("Tip RED", "w1", priority=30, ts=NOW))
    data.achievements.append(Item("T13 proof 9.0", "w1", ts=NOW))
    data.intelligence.append(Item("Fix It First", "mem", ts=NOW))
    data.next_actions.append(Item("Re-check tip", "w1", ts=NOW))
    return data


def test_render_structure():
    report = ReportGenerator.render(_sample_data())
    assert report.startswith("# HOURLY — Thu 2026-10-08 12:00 UTC")
    # The new structure — headline, four sections, nothing else.
    for section in ["## What moved",
                    "## Scoreboard",
                    "## Needs from Shawn",
                    "## Evidence"]:
        assert section in report, f"missing {section}"
    # No team sections, no org-chart boilerplate — ever.
    assert "## Team" not in report
    assert "Holes (top 3)" not in report
    assert "None recorded this window" not in report
    assert "Nothing recorded this window" not in report
    # Headline: biggest movement wins.
    assert report.splitlines()[2] == "Learning 5.0 → 5.5."
    # Scoreboard row with claim label, provenance, and delta.
    assert "| Learning | 5.5 | claim | 10-08 12:00 | w1 | +0.5 |" in report
    # Sources attached.
    assert "_(src: w1)_" in report
    # Evidence snapshot.
    assert "ACTIVE=106" in report


def test_render_quiet_hour_single_line():
    data = ReportData(since=NOW - dt.timedelta(hours=1),
                      generated_at=NOW, window_label="hourly")
    report = ReportGenerator.render(data)
    # Exactly one quiet line. No sections, no filler.
    assert report.count("Quiet hour — no window activity.") == 1
    assert "## Team" not in report
    assert "None recorded" not in report
    assert "None this hour." in report  # the Needs section stays honest
    assert "| _No scores recorded yet_ |" in report


def test_pr_update_is_movement_never_quiet():
    # An in-window PR update IS window activity: the headline must never
    # claim "quiet" while Evidence lists updated PRs.
    data = ReportData(
        since=NOW - dt.timedelta(hours=1),
        generated_at=NOW,
        window_label="hourly",
        github_snapshot={
            "prs": [{
                "number": 1967,
                "title": "148 new blocks from DESIGN uploads",
                "state": "open",
                "merged": False,
                "updated_at": NOW.isoformat(),
            }],
            "comments": [],
            "error": None,
        },
    )
    report = ReportGenerator.render(data)
    assert "Quiet hour — no window activity." not in report
    assert "PR #1967 updated: 148 new blocks from DESIGN uploads" in report
    # Headline carries the newest window event, not "Quiet hour."
    assert report.splitlines()[2] != "Quiet hour."


def test_render_no_boilerplate_with_partial_data():
    # Achievements but no holes: Needs says "None this hour." — never
    # "None recorded this window."
    data = _sample_data()
    data.holes = []
    report = ReportGenerator.render(data)
    assert "None this hour." in report
    assert "None recorded this window" not in report


def test_what_moved_capped_and_newest_first():
    data = _sample_data()
    data.achievements = [
        Item(f"Achievement {i:02d}", "w1",
             ts=NOW - dt.timedelta(minutes=i))
        for i in range(20)
    ]
    report = ReportGenerator.render(data)
    moved_section = report.split("## What moved")[1].split("## Scoreboard")[0]
    bullets = [l for l in moved_section.splitlines() if l.startswith("- ")]
    assert len(bullets) == 8  # capped
    assert "Achievement 00" in bullets[0]  # newest achievement first
    assert "Learning 5.0 → 5.5" in bullets[1]  # score movement alongside
    assert "Achievement 19" not in report  # oldest cut


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
    assert "# MORNING —" in report
    assert "## What moved" in report
    assert "## Scoreboard" in report
    assert "## Needs from Shawn" in report
    assert "## Evidence" in report
    # Fresh window items survive the filter.
    assert "11/11 pytest green" in report
    assert "Tip RED blocks CI" in report
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


def test_newer_section_beats_older_section(tmp_path):
    # Section timestamps decide: the 07:00 statement wins over the 06:00
    # one regardless of file mtime games.
    p = tmp_path / "2026-10-08.md"
    p.write_text("## Notes — 06:00 UTC\nHonest score: Retrieval **6.5/10**.\n"
                 "## Notes — 07:00 UTC\n"
                 "Cold Retrieve moved 6.5 → 7.0 on the audit branch.\n")
    pts = parse_memory_log(p)["scores"]
    by_score = {s.score: s for s in pts}
    assert set(by_score) == {6.5, 7.0}
    assert by_score[7.0].as_of > by_score[6.5].as_of


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


def test_pinned_learning_on_scoreboard():
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
    assert len(data.scores) == 1
    assert data.scores[0].score == 5.0
    assert data.scores[0].status == "authoritative"
    report = gen.render(data)
    # The pin keeps its REAL reconciliation timestamp (2026-10-08),
    # never the triggering window's time (the old code stamped 12:00).
    assert "| Learning | 5.0 | authoritative | 10-08 00:00 |" in report


def test_freshness_gate_drops_stale_and_unknown_items():
    # An item older than the window, an item with no timestamp, and a
    # fresh item: only the fresh one survives the window filter.
    stale = Item("Old news from this morning", "w1",
                 ts=NOW - dt.timedelta(hours=3))
    unknown = Item("Timestamp unknown", "w1")
    fresh = Item("Fresh news", "w1", ts=NOW - dt.timedelta(minutes=30))
    gen = ReportGenerator(
        fetch_worker_logs=lambda s: [{
            "worker": "w1", "mtime": NOW, "scores": [],
            "holes": [stale, unknown, fresh],
            "achievements": [], "activity": [],
        }],
        fetch_memory=lambda s: {"achievements": [], "intelligence": [],
                                "holes": [], "scores": []},
        fetch_github_fn=lambda s: {"prs": [], "comments": [], "error": None},
        fetch_supabase_fn=lambda: {"counts": {}, "error": None},
        load_scores_fn=lambda: {},
        save_scores_fn=lambda s: None,
    )
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    assert [h.text for h in data.holes] == ["Fresh news"]
    report = gen.render(data)
    assert "Old news from this morning" not in report
    assert "Timestamp unknown" not in report
    assert "Fresh news" in report


def test_stale_score_cannot_move_state():
    # A score stated before the window must not update the scoreboard.
    old_point = ScorePoint("Safety", 9.9, NOW - dt.timedelta(hours=5),
                           "w1", "claim")
    gen = ReportGenerator(
        fetch_worker_logs=lambda s: [{
            "worker": "w1", "mtime": NOW, "scores": [old_point],
            "holes": [], "achievements": [], "activity": [],
        }],
        fetch_memory=lambda s: {"achievements": [], "intelligence": [],
                                "holes": [], "scores": []},
        fetch_github_fn=lambda s: {"prs": [], "comments": [], "error": None},
        fetch_supabase_fn=lambda: {"counts": {}, "error": None},
        load_scores_fn=lambda: {"Safety": {"score": 8.8,
                                            "as_of": "2026-10-08T12:00:00+00:00",
                                            "source": "pin",
                                            "status": "authoritative"}},
        save_scores_fn=lambda s: None,
    )
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    assert [sp.score for sp in data.scores
            if sp.area == "Safety"] == [8.8]
    report = gen.render(data)
    assert "9.9" not in report




def test_headline_follows_most_important_window_event():
    from report_generator import _headline_text, _what_moved
    data = _sample_data()
    # _sample_data has a Learning movement 5.0 -> 5.5: it wins.
    assert _headline_text(data, _what_moved(data)) == "Learning 5.0 → 5.5."
    # No score movement: the newest moved item becomes the headline.
    data.previous_scores = {"Learning": 5.5}
    moved = _what_moved(data)
    hl = _headline_text(data, moved)
    assert hl != "Quiet hour."
    assert "_(src:" not in hl  # source tag stripped from the headline


# ---------------------------------------------------------------------------
# Score provenance — the staleness fix (2026-10-09).
# The 14:59 report showed Successor Reuse 4.5 as a bare "claim" while the
# lane had moved to 8.0: a 15h-old carried-forward score presented as
# current, with its age and source hidden. A number without provenance
# is a lie with formatting.
# ---------------------------------------------------------------------------


def _provenance_gen(state):
    return ReportGenerator(
        fetch_worker_logs=lambda s: [],
        fetch_memory=lambda s: {"achievements": [], "intelligence": [],
                                "holes": [], "scores": []},
        fetch_github_fn=lambda s: {"prs": [], "comments": [], "error": None},
        fetch_supabase_fn=lambda: {"counts": {}, "error": None},
        load_scores_fn=lambda: state,
        save_scores_fn=lambda s: None,
    )


def test_stale_claim_labeled_not_presented_as_current():
    # 30h-old heuristic claim: must render as stale WITH its age and
    # source — never as a current claim.
    state = {"Successor Reuse": {
        "score": 4.5,
        "as_of": (NOW - dt.timedelta(hours=30)).isoformat(),
        "source": "memory:2026-10-08", "status": "claim"}}
    gen = _provenance_gen(state)
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    sp = [s for s in data.scores if s.area == "Successor Reuse"][0]
    assert sp.status == "stale"
    assert sp.score == 4.5  # value preserved, judgment changed
    report = gen.render(data)
    assert "| Successor Reuse | 4.5 | stale |" in report
    assert "memory:2026-10-08" in report  # source traceable
    assert "Stale = claim not re-affirmed in 12h" in report


def test_fresh_claim_stays_claim():
    state = {"Safety": {
        "score": 8.8,
        "as_of": (NOW - dt.timedelta(hours=1)).isoformat(),
        "source": "safety-builder-20261008-1100", "status": "claim"}}
    gen = _provenance_gen(state)
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    sp = [s for s in data.scores if s.area == "Safety"][0]
    assert sp.status == "claim"
    report = gen.render(data)
    assert "| Safety | 8.8 | claim |" in report


def test_seed_labeled_as_seed_never_claim():
    # A seed value was never an observation — it must not wear "claim".
    state = {"Human Value": {
        "score": 7.5,
        "as_of": (NOW - dt.timedelta(hours=2)).isoformat(),
        "source": "seed 2026-10-08", "status": "claim"}}
    gen = _provenance_gen(state)
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    sp = [s for s in data.scores if s.area == "Human Value"][0]
    assert sp.status == "seed"
    report = gen.render(data)
    assert "| Human Value | 7.5 | seed |" in report


def test_authoritative_does_not_decay_with_age():
    # Authority is the warrant, not recency: Naya 1's pinned score stays
    # authoritative even when old.
    state = {"Learning": {
        "score": 5.0,
        "as_of": (NOW - dt.timedelta(hours=30)).isoformat(),
        "source": "Naya 1 reconciliation 2026-10-08 (pinned)",
        "status": "authoritative"}}
    gen = _provenance_gen(state)
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    sp = [s for s in data.scores if s.area == "Learning"][0]
    assert sp.status == "authoritative"
    report = gen.render(data)
    assert "| Learning | 5.0 | authoritative |" in report


def test_stale_boundary_twelve_hours():
    # 11h59m old: still a claim. 12h01m old: stale. The bound is real.
    for age_h, want in [(11, "claim"), (13, "stale")]:
        state = {"Truth": {
            "score": 9.0,
            "as_of": (NOW - dt.timedelta(hours=age_h)).isoformat(),
            "source": "truth-builder", "status": "claim"}}
        gen = _provenance_gen(state)
        data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
        sp = [s for s in data.scores if s.area == "Truth"][0]
        assert sp.status == want, f"age {age_h}h -> {sp.status}"


# ---------------------------------------------------------------------------
# Ingest-boundary guards — Pair G round 2 (2026-10-09).
# Round 1 fixed the render (provenance columns, stale/seed labels), but the
# Phase-2 attacker proved state could still be poisoned at ingest:
#   1. stale-value laundering — a historical restatement ("the 4.5 was the
#      old pre-trial baseline") extracted with a fresh timestamp overwrote
#      the true 8.0 and drove a fake-regression headline;
#   2. future-dated scores — as_of 3h ahead overwrote Truth 9.0 → 7.0 and
#      was immortal (negative age defeats the 12h staleness rule);
#   3. authoritative pin timestamp refresh — the Learning pin stamped the
#      triggering window's time, so a days-old 5.0 rendered as today.
# The lesson: check at the boundary where the bad value ENTERS (state
# ingest), not where it's displayed.
# ---------------------------------------------------------------------------


def _ingest_gen(state, points):
    """Generator whose worker log yields the given ScorePoints."""
    return ReportGenerator(
        fetch_worker_logs=lambda s: [{
            "worker": "w1", "mtime": NOW, "scores": points,
            "holes": [], "achievements": [], "activity": [],
        }],
        fetch_memory=lambda s: {"achievements": [], "intelligence": [],
                                "holes": [], "scores": []},
        fetch_github_fn=lambda s: {"prs": [], "comments": [], "error": None},
        fetch_supabase_fn=lambda: {"counts": {}, "error": None},
        load_scores_fn=lambda: state,
        save_scores_fn=lambda s: None,
    )


def test_historical_restatement_is_not_a_claim():
    # The attacker's exact laundering sentence.
    pts = extract_scores_from_text(
        "The Successor Reuse score of 4.5 was the old pre-trial baseline.",
        source="w1", as_of=NOW)
    assert len(pts) == 1
    assert pts[0].area == "Successor Reuse"
    assert pts[0].score == 4.5
    assert pts[0].status == "history"


def test_movement_arrow_stays_a_current_claim():
    # A movement arrow names the new value explicitly — always current.
    pts = extract_scores_from_text(
        "The old Successor Reuse baseline moved 4.5 → 8.0 after the trial.",
        source="w1", as_of=NOW)
    assert len(pts) == 1
    assert pts[0].area == "Successor Reuse"
    assert pts[0].score == 8.0
    assert pts[0].status == "claim"


def test_plain_current_claim_unaffected():
    pts = extract_scores_from_text(
        "Honest score: Retrieval 7.0/10.", source="w1", as_of=NOW)
    assert len(pts) == 1
    assert pts[0].status == "claim"


def test_historical_restatement_cannot_overwrite_state():
    # The full laundering attack: true 8.0 in state, fresh log restates
    # the old 4.5 as history. State must keep 8.0; no fake regression.
    state = {"Successor Reuse": {"score": 8.0,
                                 "as_of": (NOW - dt.timedelta(hours=2)).isoformat(),
                                 "source": "lane", "status": "claim"}}
    hist = ScorePoint("Successor Reuse", 4.5, NOW, "w1", "history")
    gen = _ingest_gen(state, [hist])
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    kept = [sp for sp in data.scores if sp.area == "Successor Reuse"]
    assert [sp.score for sp in kept] == [8.0]
    from report_generator import _headline_text, _what_moved
    assert "4.5" not in _headline_text(data, _what_moved(data))


def test_future_dated_score_rejected_at_ingest():
    # A score 3h in the future must never enter state — it would be
    # immortal (negative age defeats the 12h staleness rule).
    state = {"Truth": {"score": 9.0,
                       "as_of": (NOW - dt.timedelta(hours=2)).isoformat(),
                       "source": "lane", "status": "claim"}}
    future = ScorePoint("Truth", 7.0, NOW + dt.timedelta(hours=3),
                        "w1", "claim")
    gen = _ingest_gen(state, [future])
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    kept = [sp.score for sp in data.scores if sp.area == "Truth"]
    assert kept == [9.0]


def test_small_clock_skew_still_accepted():
    # Within the 10-minute skew allowance, a slightly-future point is fine.
    state = {"Truth": {"score": 9.0,
                       "as_of": (NOW - dt.timedelta(hours=2)).isoformat(),
                       "source": "lane", "status": "claim"}}
    skewed = ScorePoint("Truth", 9.5, NOW + dt.timedelta(minutes=5),
                        "w1", "claim")
    gen = _ingest_gen(state, [skewed])
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    kept = [sp.score for sp in data.scores if sp.area == "Truth"]
    assert kept == [9.5]


def test_authoritative_pin_keeps_real_timestamp():
    # The pin must never be re-stamped with the triggering window's time.
    pin_as_of = "2026-10-08T00:00:00+00:00"
    state = {"Learning": {"score": 5.0, "as_of": pin_as_of,
                          "source": "Naya 1 reconciliation 2026-10-08 (pinned)",
                          "status": "authoritative"}}
    trigger = ScorePoint("Learning", 7.0, NOW, "w1", "claim")
    gen = _ingest_gen(state, [trigger])
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    kept = [sp for sp in data.scores if sp.area == "Learning"]
    assert len(kept) == 1
    assert kept[0].score == 5.0
    assert kept[0].status == "authoritative"
    assert kept[0].as_of.isoformat() == pin_as_of


def test_authoritative_pin_first_write_uses_real_timestamp():
    # First time the pin is written, as_of is the reconciliation date —
    # never the window's timestamp.
    trigger = ScorePoint("Learning", 7.0, NOW, "w1", "claim")
    gen = _ingest_gen({}, [trigger])
    data = gen.collect("hourly", NOW - dt.timedelta(hours=1), NOW)
    kept = [sp for sp in data.scores if sp.area == "Learning"]
    assert len(kept) == 1
    assert kept[0].score == 5.0
    assert kept[0].as_of.isoformat() == "2026-10-08T00:00:00+00:00"

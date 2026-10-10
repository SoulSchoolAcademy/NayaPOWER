"""Tests for tools/waste_meter.py — Waste Meter v1.

Covers the pure seams only: aggregation math, the SN-stage keyword proxy,
and the plain-words renderer. Network collection is not unit-tested here;
every figure in the renderer must trace to aggregated input (no invented
numbers), and gaps must render as gaps.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import waste_meter as wm  # noqa: E402


def _raw(**over):
    base = {
        "window": {"since": "2026-10-03T00:00:00Z", "until": "2026-10-10T00:00:00Z"},
        "window_days": 7.0,
        "prs": [
            {"number": 1, "title": "a", "created_at": "2026-10-04T00:00:00Z",
             "merged_at": "2026-10-04T02:00:00Z"},
            {"number": 2, "title": "b", "created_at": "2026-10-05T00:00:00Z",
             "merged_at": "2026-10-06T00:00:00Z"},
            {"number": 3, "title": "c", "created_at": "2026-10-05T00:00:00Z",
             "merged_at": "2026-10-05T01:00:00Z"},
        ],
        "timelines": [
            {"number": 1, "commits": 1, "force_pushes": 0, "timeline_events": 3},
            {"number": 2, "commits": 9, "force_pushes": 2, "timeline_events": 14},
            {"number": 3, "commits": 3, "force_pushes": 0, "timeline_events": 5},
        ],
        "timeline_errors": 1,
        "ci_runs": [
            {"id": 1, "conclusion": "success", "run_attempt": 1, "minutes": 10.0},
            {"id": 2, "conclusion": "failure", "run_attempt": 3, "minutes": 20.0},
            {"id": 3, "conclusion": "success", "run_attempt": 2, "minutes": 5.0},
        ],
        "board_comments": [
            {"id": 1, "author": "svc", "created_at": "2026-10-04T00:00:00Z",
             "body": "[NAYA 4] Smart Note SN-0800 staged: waste meter spec"},
            {"id": 2, "author": "svc", "created_at": "2026-10-04T01:00:00Z",
             "body": "[NAYA 4] signing in for the day"},
            {"id": 3, "author": "svc", "created_at": "2026-10-05T00:00:00Z",
             "body": "[CODA 3] SN-0801 staged"},
            {"id": 4, "author": "svc", "created_at": "2026-10-05T01:00:00Z",
             "body": "untagged relay ping"},
        ],
        "reverts": [{"number": 99, "title": "Revert \"oops\""}],
        "stalled_prs": {"stalled": [{"number": 7, "title": "old work",
                                     "stale_days": 5.0}],
                        "open_total": 40},
        "local_logs": {"available": True, "files": 4, "bytes": 1024 * 1024},
    }
    base.update(over)
    return base


def test_aggregate_pr_math():
    m = wm.aggregate(_raw())
    assert m["prs_merged"] == 3
    assert m["prs_measured"] == 3
    cp = m["commits_per_pr"]
    assert cp["median"] == 3.0
    assert cp["mean"] == pytest.approx(13 / 3)
    assert cp["max"] == 9
    assert cp["buckets"]["1 commit (clean landing)"] == 1
    assert cp["buckets"]["9+ commits (heavy rework)"] == 1
    assert m["extra_commits_beyond_first"] == (0 + 8 + 2)
    assert m["force_pushes"] == 2
    assert m["prs_with_force_push"] == 1
    assert m["timeline_errors"] == 1
    # cycles: 2h, 24h, 1h -> median 2
    assert m["cycle_hours"]["median"] == 2.0
    assert m["cycle_hours"]["mean"] == pytest.approx(9.0)


def test_aggregate_ci_math():
    m = wm.aggregate(_raw())
    ci = m["ci"]
    assert ci["runs"] == 3
    assert ci["extra_attempts"] == (0 + 2 + 1)
    assert ci["rerun_rate"] == pytest.approx(1.0)
    assert ci["failed_runs"] == 1
    assert ci["conclusions"] == {"success": 2, "failure": 1}
    assert ci["wall_minutes"] == pytest.approx(35.0)


def test_aggregate_board_and_reverts():
    m = wm.aggregate(_raw())
    bd = m["board"]
    assert bd["comments"] == 4
    assert bd["sn_stage_posts"] == 2
    assert bd["active_authors"] == 1   # one service account for all lanes
    assert bd["active_lanes"] == 2     # NAYA 4 + CODA 3 from [TAG] signatures
    assert bd["untagged_posts"] == 1
    assert bd["top_lanes"] == [("NAYA 4", 2), ("CODA 3", 1)]
    assert bd["sn_posts_per_lane_day"] == pytest.approx(0.14)  # rounded to 2dp
    assert m["reverts"]["count"] == 1
    assert m["stalled_prs"]["count"] == 1
    assert m["stalled_prs"]["open_total"] == 40


def test_lane_tag_normalization():
    assert wm.lane_tag("[NAYA 4] SIGN IN") == "NAYA 4"
    assert wm.lane_tag("# [naya 4] sign in") == "NAYA 4"
    assert wm.lane_tag("[NAYA 4 → LEARNING] done") == "NAYA 4"
    assert wm.lane_tag("[NAYA 5 | VOICE-BUILDER] done") == "NAYA 5"
    assert wm.lane_tag("[NAYA 2 — BRAIN LOOP] done") == "NAYA 2"
    assert wm.lane_tag("no tag here") is None
    assert wm.lane_tag("") is None


def test_fmt_hours_uses_minutes_under_an_hour():
    assert wm._fmt_hours(None) == "n/a (no data)"
    assert wm._fmt_hours(0.0394) == "2.4 minutes"
    assert wm._fmt_hours(2.42) == "2.4 hours"


def test_aggregate_missing_timeline_excluded_honestly():
    raw = _raw()
    raw["timelines"] = [t for t in raw["timelines"] if t["number"] != 2]
    raw["timeline_errors"] = 2
    m = wm.aggregate(raw)
    assert m["prs_merged"] == 3          # still counted as landed
    assert m["prs_measured"] == 2        # but excluded from rework math
    assert m["timeline_errors"] == 2
    assert m["commits_per_pr"]["max"] == 3


def test_aggregate_empty_inputs_render_as_gaps_not_zeros():
    m = wm.aggregate(_raw(prs=[], timelines=[], ci_runs=[], board_comments=[],
                           reverts=[],
                           stalled_prs={"stalled": [], "open_total": 0},
                           local_logs={"available": False}))
    assert m["prs_merged"] == 0
    assert m["commits_per_pr"]["median"] is None
    assert m["ci"]["rerun_rate"] is None
    assert m["board"]["sn_posts_per_lane_day"] is None
    report = wm.render_markdown(m, {"repo": "O/R", "board_issue": 1354,
                                    "measured_at": "2026-10-10T00:00:00Z"})
    assert "n/a (no data)" in report
    assert "not available on this machine" in report


def test_waste_ranking_sorted_desc():
    m = wm.aggregate(_raw())
    counts = [w["wasted_events"] for w in m["waste_ranking"]]
    assert counts == sorted(counts, reverse=True)
    # extra commits (10) outranks re-runs (3) outranks reverts (1)
    names = [w["source"] for w in m["waste_ranking"]]
    assert names.index("Extra commits beyond the first on each PR (rework)") < \
        names.index("Reverted merges (redo — landed, then un-landed)")


def test_sn_stage_proxy_keywords():
    assert wm.is_sn_stage_post("Smart Note SN-0800 staged")
    assert wm.is_sn_stage_post("staged SN-1234 for review")
    assert wm.is_sn_stage_post("smart-note draft")
    assert not wm.is_sn_stage_post("signing in for the day")
    assert not wm.is_sn_stage_post("the snow is nice today")  # no false "sn-" hit


def test_render_every_figure_traces_to_input():
    m = wm.aggregate(_raw())
    report = wm.render_markdown(m, {"repo": "O/R", "board_issue": 1354,
                                    "measured_at": "2026-10-10T00:00:00Z"})
    # spot-check figures appear verbatim
    assert "**3 changes**" in report            # prs_merged
    assert "Revert \"oops\"" in report          # revert title
    assert "old work" in report                # stalled title
    assert "token / compute spend per decision — NOT measured" in report.lower() \
        or "NOT measured" in report
    # every table row names a source
    for line in report.splitlines():
        if line.startswith("| ") and "Figure" not in line and "---" not in line:
            assert line.count("|") >= 4, f"row without source column: {line}"


def test_render_plain_words_sections_present():
    m = wm.aggregate(_raw())
    report = wm.render_markdown(m, {"repo": "O/R", "board_issue": 1354,
                                    "measured_at": "2026-10-10T00:00:00Z"})
    for section in ("In a nutshell", "The numbers", "Where the waste went",
                    "What this doesn't show", "How this was measured"):
        assert section in report
    assert "docs/waste-meter-spec.md" in report


def test_cli_parsing_offline_flags():
    p = wm.build_parser()
    a = p.parse_args(["--days", "7", "--no-logs", "--max-pr-timelines", "5"])
    assert a.days == 7.0 and a.no_logs and a.max_pr_timelines == 5
    a = p.parse_args(["--since", "2026-10-03", "--until", "2026-10-10"])
    assert a.since == "2026-10-03" and a.until == "2026-10-10"

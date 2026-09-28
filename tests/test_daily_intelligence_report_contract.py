import json
from pathlib import Path

REPORT_ROOT = Path("BRAIN/90-OPERATIONS/REPORTS")
DAILY_MD = REPORT_ROOT / "DAILY/2026/09/2026-09-28-DAILY-INTELLIGENCE-REPORT.md"
DAILY_JSON = REPORT_ROOT / "DAILY/2026/09/2026-09-28-DAILY-INTELLIGENCE-REPORT.json"
DAILY_INDEX = REPORT_ROOT / "DAILY/INDEX.json"
EVENT = REPORT_ROOT / "EVENTS/REPORT-PUBLISHED-2026-09-28.json"


def test_daily_report_has_human_and_machine_views():
    assert DAILY_MD.exists()
    assert DAILY_JSON.exists()
    machine = json.loads(DAILY_JSON.read_text(encoding="utf-8"))
    assert machine["report_id"] == "DIR-2026-09-28-001"
    assert machine["status"] == "PUBLISHED"
    assert machine["reporting_period"] == "2026-09-28"
    assert machine["next_action"]["exactly_one"] is True


def test_daily_report_human_view_contains_required_sections():
    text = DAILY_MD.read_text(encoding="utf-8")
    required = [
        "Executive State",
        "What Changed",
        "Major Accomplishments",
        "Verified Evidence",
        "Important Discoveries",
        "Current Intelligence / Graph State",
        "Open Gaps / Blockers",
        "Decisions Locked",
        "Top-10 Priorities",
        "Exactly One Next Action",
        "Evidence / Receipt References",
        "Provenance / Source Boundary",
        "Report Status",
    ]
    for heading in required:
        assert heading in text


def test_machine_index_points_to_same_report_identity():
    index = json.loads(DAILY_INDEX.read_text(encoding="utf-8"))
    assert index["latest_report_id"] == "DIR-2026-09-28-001"
    assert index["reports"][0]["human_view"].endswith(DAILY_MD.as_posix())
    assert index["reports"][0]["machine_view"].endswith(DAILY_JSON.as_posix())
    assert index["reports"][0]["publication_event"].endswith(EVENT.as_posix())


def test_publication_event_binds_report():
    event = json.loads(EVENT.read_text(encoding="utf-8"))
    report = json.loads(DAILY_JSON.read_text(encoding="utf-8"))
    assert event["event_type"] == "REPORT_PUBLISHED"
    assert event["report_id"] == report["report_id"]
    assert event["source_commit"] == report["source_boundary"]["source_commit"]

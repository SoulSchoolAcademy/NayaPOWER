"""Tests for tools/build_mission_state.py + tools/check_mission_state_drift.py.

The parser runs against the REAL BRAIN/CURRENT-MISSION-STATE.md (the facts
asserted below are the snapshot's own stated facts at the tip this test
landed with — if the director refreshes the snapshot, update them from the
new snapshot's KEY NUMBERS line, never from memory).

Negative controls (required):
  * a mutated snapshot (one stated number changed) makes the drift check
    FAIL, naming the drifted field;
  * a twin missing a required field FAILS schema validation with
    MISSING/CURE lines, never a bare error;
  * the venue scrub: the serialized twin never names retired venue 2765.
"""
import json
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

import build_mission_state as bms  # noqa: E402
import check_mission_state_drift as drift  # noqa: E402
from operating_state import validate  # noqa: E402

MD_TEXT = (ROOT / "BRAIN" / "CURRENT-MISSION-STATE.md").read_text(encoding="utf-8")
SCHEMA = json.loads((TOOLS / "mission_state.schema.json").read_text(encoding="utf-8"))
FAKE_LIVE = {"derived_utc": "2026-10-22T00:00:00Z",
             "main_tip": "0" * 40,
             "open_pr_count": 1,
             "open_prs": [1],
             "board": {"issue": 2793, "comments": 1}}


def test_parser_extracts_the_snapshots_own_facts():
    snap = bms.parse_snapshot(MD_TEXT)
    assert snap["last_verified_utc"] == "2026-10-22T02:56:00Z"
    assert snap["main_tip"] == "6269864218b1865f5ed4ce69ef30559584f4f3e3"
    assert snap["tip_moved"] == {"from": "7bd2253549048e457ae56e8148a0908e90f91f70",
                                  "to": "6269864218b1865f5ed4ce69ef30559584f4f3e3"}
    assert snap["identity"] == {"repo": "SoulSchoolAcademy/NayaPOWER",
                                "live_board": 2793, "master_directive": 2601}
    kn = snap["key_numbers"]
    assert kn["board"] == {"issue": 2793, "comments": 1185,
                           "delta_since_watermark": 4, "watermark_comment": 6331260995}
    assert kn["open_prs_register"] == [2898, 2874, 2869]
    assert kn["smart_notes_rows"] == {"total": 353, "super": 71, "smart": 282}
    assert [it["rank"] for it in snap["standing_top10"]] == list(range(1, 11))
    assert snap["standing_top10"][0]["headline"].startswith("ESSENCE POSTURE")
    assert snap["standing_top10"][9]["carried"] is True
    assert [r["area"] for r in snap["team_status"]] == [
        "SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]
    assert snap["team_status"][5] == {"area": "CONNECT", "accomplished": None,
                                      "working_on": None, "plan": None}
    assert len(snap["pointers"]) == 4


def test_twin_validates_against_schema_and_is_scrubbed():
    twin = bms.build_twin(MD_TEXT, FAKE_LIVE, generated_utc="2026-10-22T00:00:00Z")
    assert validate(twin, SCHEMA) == []
    assert bms.RETIRED_VENUE not in json.dumps(twin, ensure_ascii=False)
    twin_offline = bms.build_twin(MD_TEXT, None, generated_utc="2026-10-22T00:00:00Z")
    assert validate(twin_offline, SCHEMA) == []
    assert twin_offline["live"] is None


def test_drift_check_passes_on_the_committed_pair(tmp_path):
    twin = bms.build_twin(MD_TEXT, FAKE_LIVE, generated_utc="2026-10-22T00:00:00Z")
    json_path = tmp_path / "MISSION-STATE.json"
    json_path.write_text(json.dumps(twin, indent=1, ensure_ascii=False), encoding="utf-8")
    md_path = tmp_path / "CURRENT-MISSION-STATE.md"
    md_path.write_text(MD_TEXT, encoding="utf-8")
    code, lines = drift.run_check(md_path, json_path)
    assert code == 0, lines


def test_negative_control_mutated_snapshot_fails_drift(tmp_path):
    twin = bms.build_twin(MD_TEXT, FAKE_LIVE, generated_utc="2026-10-22T00:00:00Z")
    json_path = tmp_path / "MISSION-STATE.json"
    json_path.write_text(json.dumps(twin, indent=1, ensure_ascii=False), encoding="utf-8")
    mutated = MD_TEXT.replace("(1185 count,", "(1186 count,", 1)
    assert mutated != MD_TEXT
    md_path = tmp_path / "CURRENT-MISSION-STATE.md"
    md_path.write_text(mutated, encoding="utf-8")
    code, lines = drift.run_check(md_path, json_path)
    assert code == 1
    assert any("key_numbers.board.comments" in ln for ln in lines), lines


def test_negative_control_missing_field_fails_schema_with_cure_lines():
    twin = bms.build_twin(MD_TEXT, FAKE_LIVE, generated_utc="2026-10-22T00:00:00Z")
    del twin["snapshot"]["main_tip"]
    errors = validate(twin, SCHEMA)
    assert any("main_tip is required" in e and "CURE:" in e for e in errors), errors


def test_parser_fails_loud_when_key_numbers_vanish():
    broken = "\n".join(ln for ln in MD_TEXT.splitlines() if "**KEY NUMBERS" not in ln)
    with pytest.raises(bms.SnapshotError):
        bms.parse_snapshot(broken)

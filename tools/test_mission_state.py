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
    # The snapshot states its instant seconds-less (2026-10-22T20:15Z);
    # the parser accepts the form and normalizes to :00 (ruling, Option C).
    assert snap["last_verified_utc"] == "2026-10-22T20:15:00Z"
    assert snap["main_tip"] == "4b49c86662203d6cbde266cbba1778cbe42dd620"
    # TIP MOVED is a stated form: from != to, anchored at the 'to' tip.
    assert snap["tip_moved"] == {"from": "91e2de5dcda5e6567dd2758c06a38b07223b88b7",
                                  "to": "4b49c86662203d6cbde266cbba1778cbe42dd620"}
    assert snap["identity"] == {"repo": "SoulSchoolAcademy/NayaPOWER",
                                "live_board": 2793, "master_directive": 2601}
    kn = snap["key_numbers"]
    # The board delta is stated as '+9 ids since watermark …' — accepted form.
    assert kn["board"] == {"issue": 2793, "comments": 1551,
                           "delta_since_watermark": 9, "watermark_comment": 6349561649}
    # The register is machine-derived at emit time (ruling, Option C):
    # the parser no longer reads it from the snapshot, and the snapshot
    # no longer states the Smart Notes wall rows either.
    assert "open_prs_register" not in kn
    assert "smart_notes_rows" not in kn
    assert [it["rank"] for it in snap["standing_top10"]] == list(range(1, 11))
    assert snap["standing_top10"][0]["headline"].startswith("THE 100% ALIGNMENT CHARGE")
    assert snap["standing_top10"][8]["carried"] is True
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
    # The register in the twin is the live derivation's list, verbatim.
    assert twin["snapshot"]["key_numbers"]["open_prs_register"] == FAKE_LIVE["open_prs"]


def test_offline_build_fails_loud_on_the_derived_register():
    # No live derivation -> no honest register -> no twin (ruling,
    # Option C: fail loud in the MISSING/CURE form, never guess).
    with pytest.raises(bms.SnapshotError, match="open_prs_register"):
        bms.build_twin(MD_TEXT, None, generated_utc="2026-10-22T00:00:00Z")


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
    mutated = MD_TEXT.replace("(1551 count,", "(1552 count,", 1)
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

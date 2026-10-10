"""Tests for tools/score_fill_ship.py — Operating Code V2 §3.1.

Run: python -m pytest tests/test_score_fill_ship.py -q   (from repo root)
"""

import json
import subprocess
import sys

import pytest

from tools.score_fill_ship import (
    AAA_THRESHOLD,
    MAX_ROUNDS,
    NOT_STARTED,
    SHIP,
    SHIP_BELOW_FLOOR,
    SHIP_FLOOR,
    SHIP_HOLES_OPEN,
    SHIP_HOLES_UNNAMED,
    SHIP_RESCORE_MISSING,
    SHIP_ROUNDS_EXCEEDED,
    SHIP_SELF_VERIFIED,
    Hole,
    ScoreRound,
    evaluate_shipment,
    parse_work_state,
)


def hole(hid="H1", filled=True):
    return Hole(hole_id=hid, description=f"gap {hid}",
                fill_evidence="fixed and re-verified" if filled else "")


def rnd(no, score, holes=(), scorer="naya-4", verifier="naya-2"):
    return ScoreRound(round_no=no, score=score, holes=tuple(holes),
                      scorer=scorer, verifier=verifier)


# ---- Happy paths -------------------------------------------------------------


def test_ship_at_floor_with_filled_holes():
    v = evaluate_shipment([rnd(1, 8.5, [hole("H1", filled=False)]),
                           rnd(2, 9.0, [hole("H1")])])
    assert v.ship is True and v.grade == "PASS"


def test_ship_aaa_at_95():
    # 9.5 < 10: the 0.5 gap must be NAMED and filled (V2 §3.1), then it ships.
    v = evaluate_shipment([rnd(1, 9.5, [hole("H1")])])
    assert v.ship is True and v.grade == "AAA"


def test_ship_perfect_ten_no_holes_needed():
    v = evaluate_shipment([rnd(1, 10.0)])
    assert v.ship is True and v.grade == "AAA"


def test_constants_match_v2():
    assert SHIP_FLOOR == 9.0
    assert AAA_THRESHOLD == 9.5
    assert MAX_ROUNDS == 3


# ---- Named refusals ----------------------------------------------------------


def test_no_rounds_is_not_started():
    v = evaluate_shipment([])
    assert v.ship is False
    assert v.reasons == (NOT_STARTED,)


def test_below_floor_does_not_ship():
    v = evaluate_shipment([rnd(1, 8.9, [hole("H1")])])
    assert v.ship is False
    assert any(SHIP_BELOW_FLOOR in r for r in v.reasons)


def test_score_below_10_with_no_holes_named_is_refused():
    v = evaluate_shipment([rnd(1, 9.2)])
    assert v.ship is False
    assert any(SHIP_HOLES_UNNAMED in r for r in v.reasons)


def test_open_holes_block_shipment():
    v = evaluate_shipment([rnd(1, 9.1, [hole("H1", filled=False), hole("H2")])])
    assert v.ship is False
    assert any(SHIP_HOLES_OPEN in r and "H1" in r for r in v.reasons)


def test_self_verification_is_refused():
    v = evaluate_shipment([rnd(1, 9.5, scorer="naya-4", verifier="naya-4")])
    assert v.ship is False
    assert any(SHIP_SELF_VERIFIED in r for r in v.reasons)


def test_missing_verifier_is_refused():
    v = evaluate_shipment([rnd(1, 9.5, verifier="")])
    assert v.ship is False
    assert any(SHIP_SELF_VERIFIED in r for r in v.reasons)


def test_rounds_exceeded_is_refused():
    rounds = [rnd(1, 8.0, [hole("H1", filled=False)]),
              rnd(2, 8.5, [hole("H1", filled=False)]),
              rnd(3, 9.0, [hole("H1", filled=False)]),
              rnd(4, 9.1, [hole("H1", filled=False)])]
    v = evaluate_shipment(rounds)
    assert v.ship is False
    assert any(SHIP_ROUNDS_EXCEEDED in r for r in v.reasons)


def test_rescore_must_improve_after_fills():
    v = evaluate_shipment([rnd(1, 8.0, [hole("H1", filled=False)]),
                           rnd(2, 8.0, [hole("H1")])])
    assert v.ship is False
    assert any(SHIP_RESCORE_MISSING in r for r in v.reasons)


def test_rounds_must_be_sequential():
    v = evaluate_shipment([rnd(1, 9.5), rnd(3, 9.6)])
    assert v.ship is False
    assert any("ROUND_OUT_OF_ORDER" in r for r in v.reasons)


def test_out_of_range_score_is_refused():
    v = evaluate_shipment([ScoreRound(1, 11.0, (), "a", "b")])
    assert v.ship is False
    assert any("OUT_OF_RANGE" in r for r in v.reasons)


# ---- Parsing -----------------------------------------------------------------


def test_parse_work_state_round_trip():
    state = {"rounds": [
        {"round_no": 1, "score": 8.5, "scorer": "naya-4", "verifier": "naya-2",
         "holes": [{"hole_id": "H1", "description": "x", "fill_evidence": ""}]},
        {"round_no": 2, "score": 9.2, "scorer": "naya-4", "verifier": "naya-2",
         "holes": [{"hole_id": "H1", "description": "x", "fill_evidence": "done"}]},
    ]}
    rounds = parse_work_state(state)
    assert len(rounds) == 2
    v = evaluate_shipment(rounds)
    assert v.ship is True


def test_parse_rejects_non_object():
    with pytest.raises(ValueError):
        parse_work_state([1, 2])


def test_parse_rejects_hole_without_id():
    with pytest.raises(ValueError):
        parse_work_state({"rounds": [{"round_no": 1, "score": 9.0, "scorer": "a",
                                       "verifier": "b", "holes": [{"description": "x"}]}]})


# ---- CLI ----------------------------------------------------------------------


def run_cli(state, tmp_path):
    p = tmp_path / "state.json"
    p.write_text(json.dumps(state))
    proc = subprocess.run([sys.executable, "tools/score_fill_ship.py", str(p)],
                          capture_output=True, text=True, cwd=".")
    return proc.returncode, json.loads(proc.stdout)


def test_cli_ship_exit_zero(tmp_path):
    state = {"rounds": [{"round_no": 1, "score": 9.5, "scorer": "naya-4",
                         "verifier": "naya-2",
                         "holes": [{"hole_id": "H1", "description": "minor gap",
                                    "fill_evidence": "filled and re-verified"}]}]}
    code, out = run_cli(state, tmp_path)
    assert code == 0
    assert out["ship"] is True and out["grade"] == "AAA"


def test_cli_no_ship_exit_one(tmp_path):
    state = {"rounds": [{"round_no": 1, "score": 8.0, "scorer": "naya-4",
                         "verifier": "naya-2",
                         "holes": [{"hole_id": "H1", "description": "x", "fill_evidence": ""}]}]}
    code, out = run_cli(state, tmp_path)
    assert code == 1
    assert out["ship"] is False
    assert any(SHIP_BELOW_FLOOR in r for r in out["reasons"])


def test_cli_bad_input_exit_two(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{not json")
    proc = subprocess.run([sys.executable, "tools/score_fill_ship.py", str(p)],
                          capture_output=True, text=True, cwd=".")
    assert proc.returncode == 2

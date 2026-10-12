"""Tests for tools/decision_calculator.py.

The calculator is a thin wrapper over kernel/value_calculus.py — these tests
prove the wrapper's own responsibilities: wisdom classification, input
validation, gate mapping, plain-language output, batch, dry-run, and the
learning loop. Engine math itself is tested in the kernel's suite.
"""

import json
import os
import subprocess
import sys
import tempfile

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO_ROOT, "tools", "decision_calculator.py")
sys.path.insert(0, REPO_ROOT)

from tools.decision_calculator import (  # noqa: E402
    classify_weight,
    clarifying_questions,
    decide_payload,
)


def run_cli(*argv, stdin_text=None, cwd=REPO_ROOT):
    return subprocess.run(
        [sys.executable, TOOL, *argv],
        input=stdin_text,
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=30,
    )


def base_payload(**over):
    p = {
        "question": "Which option?",
        "objective": "Test objective",
        "options": [
            {"id": "a", "description": "Option A", "value_estimate": 8.0,
             "evidence": ["e1", "e2"], "reversible": True, "authorized": True},
            {"id": "b", "description": "Option B", "value_estimate": 6.0,
             "evidence": ["e1", "e2"], "reversible": True, "authorized": True},
        ],
        "context": {"reversibility": "high", "stakes": "low"},
    }
    p.update(over)
    return p


# --- Wisdom classification -------------------------------------------------

def test_wisdom_five_minute():
    tier, _ = classify_weight({"reversibility": "high", "stakes": "low"},
                              [{"reversible": True}])
    assert tier == "five-minute"


def test_wisdom_standard():
    tier, _ = classify_weight({"reversibility": "high", "stakes": "high"},
                              [{"reversible": True}])
    assert tier == "standard"


def test_wisdom_foundational_irreversible():
    tier, why = classify_weight({"reversibility": "high", "stakes": "low"},
                                [{"reversible": False}])
    assert tier == "foundational"


def test_wisdom_foundational_consequential():
    tier, _ = classify_weight({"reversibility": "high", "stakes": "consequential"},
                              [{"reversible": True}])
    assert tier == "foundational"


def test_wisdom_ignores_disqualified_options():
    # A forbidden irreversible option shouldn't force foundational —
    # it will never compete.
    tier, _ = classify_weight({"reversibility": "high", "stakes": "low"},
                              [{"reversible": False, "forbidden": True}])
    assert tier == "five-minute"


def test_foundational_recommends_human_review():
    p = base_payload(context={"reversibility": "low", "stakes": "low"})
    r = decide_payload(p)
    assert r["wisdom"]["tier"] == "foundational"
    assert r["wisdom"]["human_review_recommended"] is True
    assert "human should review" in r["explanation"]


# --- Hard gates -------------------------------------------------------------

def test_harmful_option_disqualified_not_outscored():
    p = base_payload(options=[
        {"id": "safe", "value_estimate": 5.0, "evidence": ["e1", "e2"],
         "reversible": True, "authorized": True},
        {"id": "harmful", "value_estimate": 10.0, "evidence": ["e1", "e2"],
         "reversible": True, "authorized": True,
         "harm": {"severity": 9.5, "probability": 0.5}},
    ])
    r = decide_payload(p)
    dq = [d["id"] for d in r["disqualified"]]
    assert "harmful" in dq
    assert r["winner"] == "safe"
    assert "not outscored, excluded" in r["explanation"]


def test_deceptive_option_disqualified():
    p = base_payload(options=[
        {"id": "honest", "value_estimate": 7.0, "evidence": ["e1", "e2"],
         "reversible": True, "authorized": True},
        {"id": "liar", "value_estimate": 10.0, "evidence": ["e1", "e2"],
         "reversible": True, "authorized": True, "deceptive": True},
    ])
    r = decide_payload(p)
    assert "liar" in [d["id"] for d in r["disqualified"]]
    assert r["winner"] == "honest"


def test_forbidden_option_disqualified():
    p = base_payload(options=[
        {"id": "ok", "value_estimate": 7.0, "evidence": ["e1", "e2"],
         "reversible": True, "authorized": True},
        {"id": "banned", "value_estimate": 10.0, "evidence": ["e1", "e2"],
         "reversible": True, "authorized": True, "forbidden": True},
    ])
    r = decide_payload(p)
    assert "banned" in [d["id"] for d in r["disqualified"]]


def test_unauthorized_consequential_asks():
    p = base_payload(
        options=[{"id": "big", "value_estimate": 9.0, "evidence": ["e1", "e2", "e3"],
                  "reversible": True, "authorized": True, "stakes": "consequential"}],
        context={"reversibility": "high", "stakes": "consequential"})
    r = decide_payload(p)
    assert r["engine_decision"] == "ASK"
    assert "human decision" in r["explanation"]


def test_all_disqualified_refuses():
    p = base_payload(options=[
        {"id": "x", "value_estimate": 10.0, "evidence": ["e1"],
         "forbidden": True, "reversible": True, "authorized": True},
    ])
    r = decide_payload(p)
    assert r["engine_decision"] == "REFUSE"
    assert "refuse" in r["explanation"].lower()


# --- Winner selection & explanation ------------------------------------------

def test_higher_value_wins_among_admissible():
    r = decide_payload(base_payload())
    assert r["engine_decision"] == "ACT"
    assert r["winner"] == "a"
    assert "won because" in r["explanation"]
    assert r["winner_confidence"] is not None


def test_receipt_complete():
    r = decide_payload(base_payload())
    for key in ("decision_id", "question", "engine_decision", "winner", "ranking",
                "disqualified", "deferred", "explanation", "wisdom",
                "assumptions", "calculator_version", "engine_version",
                "kernel_receipt"):
        assert key in r, f"missing receipt field: {key}"
    assert r["wisdom"]["thought_seconds"] < 1.0
    assert r["engine_version"] == "DECISION-VALUE-CALCULUS-V2.1"


# --- Honest uncertainty ------------------------------------------------------

def test_thin_evidence_says_i_dont_know():
    p = base_payload(options=[
        {"id": "thin", "value_estimate": 8.0, "evidence": [],
         "reversible": True, "authorized": True},
    ])
    r = decide_payload(p)
    assert r["engine_decision"] == "READ_MORE"
    assert "don't know yet" in r["explanation"]
    assert "evidence" in r["explanation"].lower()


def test_no_value_no_evidence_asks_first():
    qs = clarifying_questions({"question": "Q?", "options": [{"id": "x"}]})
    assert any("expected value" in q for q in qs)


# --- Clarifying questions ----------------------------------------------------

def test_missing_question_asks():
    qs = clarifying_questions({"options": [{"id": "a", "value_estimate": 5}]})
    assert any("trying to make" in q for q in qs)


def test_missing_options_asks():
    qs = clarifying_questions({"question": "Q?"})
    assert len(qs) > 0


def test_duplicate_ids_asks():
    qs = clarifying_questions({"question": "Q?", "options": [
        {"id": "a", "value_estimate": 5}, {"id": "a", "value_estimate": 6}]})
    assert any("unique id" in q for q in qs)


def test_cli_clarification_exit_code():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"options": []}, f)
        path = f.name
    try:
        r = run_cli("decide", "--input", path, "--no-record")
        assert r.returncode == 2
        assert "?" in r.stdout
    finally:
        os.unlink(path)


# --- Batch / dry-run ----------------------------------------------------------

def test_batch_two_decisions():
    payload = {"decisions": [base_payload(), base_payload(question="Second?")]}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        path = f.name
    try:
        r = run_cli("batch", "--input", path, "--json", "--no-record")
        assert r.returncode == 0
        out = json.loads(r.stdout)
        assert out["count"] == 2
        assert all(x["status"] == "decided" for x in out["results"])
    finally:
        os.unlink(path)


def test_dry_run_records_nothing(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(base_payload(), f)
        path = f.name
    try:
        r = run_cli("decide", "--input", path, "--dry-run", "--json",
                    "--ledger", ledger)
        assert r.returncode == 0
        out = json.loads(r.stdout)
        assert out["dry_run"] is True
        assert not os.path.exists(ledger)
    finally:
        os.unlink(path)


def test_record_then_outcome_then_calibrate(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(base_payload(), f)
        path = f.name
    try:
        r = run_cli("decide", "--input", path, "--json", "--ledger", ledger)
        assert r.returncode == 0
        did = json.loads(r.stdout)["decision_id"]
        r2 = run_cli("outcome", "--decision-id", did, "--actual-delta", "3.0",
                     "--ledger", ledger)
        assert r2.returncode == 0
        r3 = run_cli("calibrate", "--ledger", ledger)
        assert r3.returncode == 0
        assert "Decisions with outcomes: 1" in r3.stdout
        assert "Mean absolute error" in r3.stdout
    finally:
        os.unlink(path)


def test_stdin_input():
    r = run_cli("decide", "--no-record", stdin_text=json.dumps(base_payload()))
    assert r.returncode == 0
    assert "Decision:" in r.stdout


def test_example_flag():
    r = run_cli("decide", "--example")
    assert r.returncode == 0
    ex = json.loads(r.stdout)
    assert "question" in ex and "options" in ex


def test_malformed_json_exit_code():
    r = run_cli("decide", "--no-record", stdin_text="{not json")
    assert r.returncode == 2
    assert "Input error" in r.stdout


def test_runs_under_one_second():
    import time
    t0 = time.perf_counter()
    decide_payload(base_payload())
    assert time.perf_counter() - t0 < 1.0


# --- Round 2: input hardening --------------------------------------------------

def test_negative_value_asks_not_crashes():
    qs = clarifying_questions({"question": "Q?", "options": [
        {"id": "a", "value_estimate": -3, "evidence": ["e1"]}]})
    assert any("0 and 10" in q for q in qs)
    r = decide_payload({"question": "Q?", "options": [
        {"id": "a", "value_estimate": -3, "evidence": ["e1"]}]})
    assert r["status"] == "needs_clarification"


def test_probability_over_one_asks():
    qs = clarifying_questions({"question": "Q?", "options": [
        {"id": "a", "value_estimate": 5, "evidence": ["e1"],
         "harm": {"severity": 2, "probability": 1.5}}]})
    assert any("0 and 1" in q for q in qs)


def test_single_option_dict_tolerated():
    r = decide_payload({"question": "Q?", "options": {"id": "solo", "value_estimate": 7,
                                                       "evidence": ["e1", "e2"]}})
    assert r["status"] == "decided"


def test_bare_list_tolerated():
    r = decide_payload([{"id": "solo", "value_estimate": 7, "evidence": ["e1", "e2"]}])
    assert r["status"] in ("decided", "needs_clarification")
    if r["status"] == "needs_clarification":
        # bare list without question → asks for the question, doesn't crash
        assert any("trying to make" in q for q in r["questions"])

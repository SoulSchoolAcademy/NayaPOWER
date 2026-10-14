"""Tests for tools/decision_cli.py — the front door to value_calculus.

The engine already exists and is tested (61/61 in
tests/test_value_calculus.py). These tests pin the TRANSLATION:
Shawn's format in, engine math out — pros/cons carried, defaults
disclosed, no silent fabrication.
"""

import json
import subprocess
import sys

sys.path.insert(0, "tools")
from decision_cli import decide  # noqa: E402


def full_opt(name, pv_b, pros, cons, refs=2):
    return {
        "name": name,
        "pros": pros,
        "cons": cons,
        "evidence_refs": ["r%d" % i for i in range(refs)],
        "reversible": True,
        "blast_radius": "low",
        "quality": {"objective_fit": 9.5, "applicability": 9.5,
                    "simplicity": 9.5},
        "confidence": {d: 0.9 for d in
                       ("objective_fit", "evidence_sufficiency",
                        "applicability", "robustness", "reversibility",
                        "blast_containment", "simplicity")},
        "pv": {"B": pv_b, "H": 1, "C": 1, "R": 0,
               "confidence": {"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9}},
    }


def test_full_decision_selects_best_pv():
    report = decide({
        "situation": "pick a path",
        "options": [
            full_opt("A", 10, ["fast", "cheap"], []),
            full_opt("B", 5, ["fast"], ["slow"]),
            full_opt("C", 3, [], ["slow", "risky"]),
        ],
    })
    assert report["decision"] == "ACT"
    assert report["selected"] == "A"


def test_no_pv_means_read_more():
    opt = full_opt("A", 10, ["fast"], [])
    del opt["pv"]
    report = decide({"situation": "pick", "options": [opt]})
    assert report["decision"] == "READ_MORE"
    assert report["selected"] is None
    assert any("pv not provided" in note for note in report["assumed"])


def test_pros_cons_carried_in_report():
    report = decide({
        "situation": "pick",
        "options": [full_opt("A", 10, ["my special pro"], ["my special con"])],
    })
    assert report["pros_cons"]["A"]["pros"] == ["my special pro"]
    assert report["pros_cons"]["A"]["cons"] == ["my special con"]


def test_assumed_dimensions_disclosed():
    opt = full_opt("A", 10, ["fast"], [])
    del opt["quality"]
    report = decide({"situation": "pick", "options": [opt]})
    assert any("assumed" in note for note in report["assumed"])


def test_unreadable_input():
    report = decide(None)
    assert report["decision"] is None


def test_cli_act_exit_0_and_pros_in_output():
    payload = json.dumps({
        "situation": "pick",
        "options": [full_opt("A", 10, ["visible pro"], []),
                    full_opt("B", 5, ["fast"], [])]})
    out = subprocess.run(
        [sys.executable, "tools/decision_cli.py"],
        input=payload, capture_output=True, text=True)
    assert out.returncode == 0
    assert "visible pro" in out.stdout
    assert "Engine: ACT" in out.stdout


def test_cli_read_more_exit_1():
    opt = full_opt("A", 10, ["fast"], [])
    del opt["pv"]
    payload = json.dumps({"situation": "pick", "options": [opt]})
    out = subprocess.run(
        [sys.executable, "tools/decision_cli.py"],
        input=payload, capture_output=True, text=True)
    assert out.returncode == 1
    assert "READ_MORE" in out.stdout


def test_cli_unreadable_exit_2():
    out = subprocess.run(
        [sys.executable, "tools/decision_cli.py"],
        input="not json", capture_output=True, text=True)
    assert out.returncode == 2

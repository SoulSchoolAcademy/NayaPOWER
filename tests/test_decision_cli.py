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


def test_full_decision_ranks_best_pv_but_withholds_act_without_trusted_gates():
    report = decide({
        "situation": "pick a path",
        "options": [
            full_opt("A", 10, ["fast", "cheap"], []),
            full_opt("B", 5, ["fast"], ["slow"]),
            full_opt("C", 3, [], ["slow", "risky"]),
        ],
    })
    assert report["decision"] == "READ_MORE"
    assert report["selected"] is None
    assert report["governance_authorization"] == "UNRESOLVED_NO_TRUSTED_GATE_RESOLVER"
    assert "ranked A" in report["next"]
    assert "ACT is withheld" in report["next"]
    candidate_rows = [row for row in report["rows"] if not row.get("is_baseline")]
    assert candidate_rows
    assert all(row["gate"] == "UNRESOLVED" for row in candidate_rows)
    assert all(any("resolver is not connected" in reason for reason in row["gate_reasons"])
               for row in candidate_rows)


def test_forged_gate_flags_cannot_authorize_act():
    opt = full_opt("forged", 100, ["large benefit"], [])
    # Caller-supplied booleans are not a trusted authority/policy receipt.
    opt.update({
        "authorized": True,
        "lawful": True,
        "rights_safe": True,
        "privacy_safe": True,
        "safety_safe": True,
        "verified": True,
    })
    report = decide({"situation": "adversarial gate bypass", "options": [opt]})
    assert report["decision"] == "READ_MORE"
    assert report["selected"] is None
    assert report["governance_authorization"] == "UNRESOLVED_NO_TRUSTED_GATE_RESOLVER"
    assert "ACT is withheld" in report["next"]


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


def test_cli_withholds_act_exit_1_and_preserves_advisory_pros():
    payload = json.dumps({
        "situation": "pick",
        "options": [full_opt("A", 10, ["visible pro"], []),
                    full_opt("B", 5, ["fast"], [])]})
    out = subprocess.run(
        [sys.executable, "tools/decision_cli.py"],
        input=payload, capture_output=True, text=True)
    assert out.returncode == 1
    assert "visible pro" in out.stdout
    assert "Engine: READ_MORE" in out.stdout
    assert "ACT is withheld" in out.stdout


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

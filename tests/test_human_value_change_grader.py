"""Tests for the Human Value change-grade instrument (tools/human_value/instrument.py).

The change grader is the companion to the event-ledger instrument
(tools/human_value/schema.py + compute_hv.py): it grades individual shipped
changes at merge time; `to-event` exports REAL VALUE+ scorecards as
schema-valid ledger events.

Contract:
- a known-good change grades HIGH (>= 8.0)
- a known-useless change grades LOW (< 5.0), even when the grader inflates scores
- malformed input fails SAFE (raises InstrumentError / exit 2, never a score)
- the harm gate disqualifies regardless of scores
- evidence rules are enforced mechanically (caps + flags)
- to-event mints NOTHING below REAL VALUE, and every minted event validates
  against the existing schema.py
"""

import json
import os
import subprocess
import sys
import tempfile

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "human_value"))
sys.path.insert(0, REPO_ROOT)
import instrument  # noqa: E402
from tools.human_value.schema import validate_event  # noqa: E402


def _git(cwd, *args):
    r = subprocess.run(["git", "-C", cwd, *args],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, f"git {' '.join(args)} failed: {r.stderr}"
    return r.stdout.strip()


@pytest.fixture()
def repo():
    """A tiny throwaway git repo with a test file, a doc, and a module."""
    d = tempfile.mkdtemp(prefix="hvcg-")
    _git(d, "init", "-q")
    _git(d, "config", "user.email", "test@naya.local")
    _git(d, "config", "user.name", "hvcg-test")
    _git(d, "commit", "-q", "--allow-empty", "-m", "root")
    os.makedirs(os.path.join(d, "tests"), exist_ok=True)
    with open(os.path.join(d, "widget.py"), "w") as f:
        f.write("def run():\n    return 42\n")
    with open(os.path.join(d, "tests", "test_widget.py"), "w") as f:
        f.write("def test_run():\n    assert True\n")
    with open(os.path.join(d, "README.md"), "w") as f:
        f.write("# widget\n\nIt runs.\n")
    _git(d, "add", "-A")
    _git(d, "commit", "-qm", "add widget with tests and docs")
    sha = _git(d, "rev-parse", "HEAD")
    return d, sha


def _packet(repo_sha, judgments, harm_found=False):
    return {
        "packet_version": 1,
        "change_id": "PR-TEST",
        "title": "test change",
        "merge_sha": repo_sha,
        "grader": "test",
        "harm_check": {"found": harm_found, "note": ""},
        "judgments": judgments,
    }


def _j(dim, score, evidence=()):
    return {"dimension": dim, "score": score, "rationale": "t",
            "evidence": list(evidence)}


def _file_ev(path, lines="1-2"):
    return {"kind": "file", "path": path, "lines": lines, "note": "t"}


def _test_ev(path, lines="1-2"):
    return {"kind": "test", "path": path, "lines": lines, "note": "t"}


def _sha_ev(sha):
    return {"kind": "sha", "sha": sha, "note": "t"}


# ---------------------------------------------------------------- happy path

def test_known_good_scores_high(repo):
    """A change with tests, docs, and verified evidence grades >= 8.0."""
    d, sha = repo
    judgments = [
        _j("USE", 9, [_file_ev("widget.py"), _test_ev("tests/test_widget.py")]),
        _j("DELTA", 8, [_sha_ev(sha)]),
        _j("PROOF", 9, [_test_ev("tests/test_widget.py")]),
        _j("DURABLE", 8, [_file_ev("README.md")]),
        _j("CLEAN", 9, [_sha_ev(sha)]),
    ]
    card = instrument.grade_packet(_packet(sha, judgments), d, sha)
    assert card["disqualified"] is False
    assert card["score"] >= 8.0
    assert card["verdict"] in ("HIGH VALUE", "REAL VALUE")
    assert all(j["applied"] == j["claimed"] for j in card["judgments"])
    assert all(not j["flags"] for j in card["judgments"])


def test_known_useless_scores_low_despite_inflation(repo):
    """No evidence + inflated 9s still lands < 5.0. The cap is the point."""
    d, sha = repo
    judgments = [_j(dim, 9) for dim in instrument.DIMENSIONS]
    card = instrument.grade_packet(_packet(sha, judgments), d, sha)
    assert card["score"] < 5.0
    assert card["verdict"] == "NO VALUE"
    assert all(j["applied"] == 3.0 for j in card["judgments"])
    assert all(j["flags"] == ["NO_EVIDENCE_CAP"] for j in card["judgments"])


def test_known_useless_honest_scores_low(repo):
    d, sha = repo
    judgments = [_j(dim, 2) for dim in instrument.DIMENSIONS]
    card = instrument.grade_packet(_packet(sha, judgments), d, sha)
    assert card["score"] == 2.0
    assert card["verdict"] == "NO VALUE"


# ---------------------------------------------------------------- fail safe

def _bad_packet_cases(sha):
    base = _packet(sha, [_j(dim, 5, [_file_ev("widget.py")])
                        for dim in instrument.DIMENSIONS])
    cases = {}
    cases["not_an_object"] = [1, 2, 3]
    p = dict(base); p.pop("judgments"); cases["missing_judgments"] = p
    p = dict(base); p["packet_version"] = 2; cases["wrong_version"] = p
    p = dict(base); p["merge_sha"] = "zzz"; cases["bad_sha"] = p
    p = dict(base); p["judgments"] = [dict(j) for j in base["judgments"][:4]]
    cases["missing_dimension"] = p
    p = dict(base); p["judgments"] = [dict(j) for j in base["judgments"]]
    p["judgments"][0] = _j("USEFULNESS", 5); cases["unknown_dimension"] = p
    p = dict(base); p["judgments"] = [dict(j) for j in base["judgments"]]
    p["judgments"][0] = _j("USE", 11, [_file_ev("widget.py")]); cases["score_too_high"] = p
    p = dict(base); p["judgments"] = [dict(j) for j in base["judgments"]]
    p["judgments"][0] = _j("USE", "nine", [_file_ev("widget.py")]); cases["score_not_number"] = p
    p = dict(base); p["judgments"] = [dict(j) for j in base["judgments"]]
    p["judgments"][0] = _j("USE", None, [_file_ev("widget.py")]); cases["score_null"] = p
    p = dict(base); p["judgments"] = [dict(j) for j in base["judgments"]]
    p["judgments"][0]["evidence"] = [{"kind": "telepathy"}]; cases["bad_evidence_kind"] = p
    p = dict(base); p["harm_check"] = {"found": "maybe"}; cases["bad_harm"] = p
    return cases


@pytest.mark.parametrize("name", [
    "not_an_object", "missing_judgments", "wrong_version", "bad_sha",
    "missing_dimension", "unknown_dimension", "score_too_high",
    "score_not_number", "score_null", "bad_evidence_kind", "bad_harm",
])
def test_malformed_fails_safe(repo, name):
    """Every malformed packet raises InstrumentError — never a score."""
    d, sha = repo
    pkt = _bad_packet_cases(sha)[name]
    with pytest.raises(instrument.InstrumentError):
        instrument.grade_packet(pkt, d, sha)


def test_malformed_json_file_fails_safe_cli(repo, tmp_path):
    d, _ = repo
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    r = subprocess.run(
        [sys.executable, os.path.join(REPO_ROOT, "tools", "human_value",
                                      "instrument.py"),
         "score", "--packet", str(bad), "--repo", d, "--ref", "HEAD"],
        capture_output=True, text=True, timeout=60)
    assert r.returncode == 2
    assert "score" not in r.stdout  # no score emitted


def test_bad_ref_fails_safe(repo):
    d, sha = repo
    judgments = [_j(dim, 5, [_file_ev("widget.py")]) for dim in instrument.DIMENSIONS]
    with pytest.raises(instrument.InstrumentError):
        instrument.grade_packet(_packet(sha, judgments), d, "deadbee")


# ---------------------------------------------------------------- gates & caps

def test_harm_gate_disqualifies_regardless_of_scores(repo):
    d, sha = repo
    judgments = [_j(dim, 10, [_file_ev("widget.py")]) for dim in instrument.DIMENSIONS]
    card = instrument.grade_packet(_packet(sha, judgments, harm_found=True), d, sha)
    assert card["disqualified"] is True
    assert card["score"] is None
    assert card["verdict"] == "DISQUALIFIED"


def test_attested_only_evidence_caps_at_five(repo):
    """Word-only evidence (command/url) can carry a dimension to 5, not beyond."""
    d, sha = repo
    att = {"kind": "command", "note": "someone ran it, trust me"}
    judgments = [_j(dim, 9, [att]) for dim in instrument.DIMENSIONS]
    card = instrument.grade_packet(_packet(sha, judgments), d, sha)
    assert all(j["applied"] == 5.0 for j in card["judgments"])
    assert all(j["flags"] == ["UNCITED_CAP"] for j in card["judgments"])
    assert card["score"] == 5.0


def test_invented_file_citation_does_not_verify(repo):
    """A citation to a file that isn't at the ref is UNVERIFIABLE -> capped."""
    d, sha = repo
    judgments = [_j(dim, 9, [_file_ev("nope/missing.py")]) for dim in instrument.DIMENSIONS]
    card = instrument.grade_packet(_packet(sha, judgments), d, sha)
    assert all(j["applied"] == 5.0 for j in card["judgments"])
    assert all(s["status"] == "UNVERIFIABLE" for s in card["evidence_ledger"])


def test_out_of_range_lines_rejected(repo):
    d, sha = repo
    judgments = [_j(dim, 6, [_file_ev("widget.py", lines="1-9999")])
                    for dim in instrument.DIMENSIONS]
    card = instrument.grade_packet(_packet(sha, judgments), d, sha)
    # citation unverifiable -> claimed 6 capped to 5
    assert all(j["applied"] == 5.0 for j in card["judgments"])


def test_mechanical_signals_come_from_git(repo):
    d, sha = repo
    mech = instrument.mechanical_signals(d, sha)
    assert mech["files_changed"] == 3
    assert mech["insertions"] > 0
    assert mech["test_files"] == 1
    assert mech["doc_files"] == 1


def test_mechanical_unavailable_does_not_fail_grade(tmp_path):
    """A root commit (no parent) still grades — mechanical reports UNAVAILABLE."""
    d = str(tmp_path / "rootrepo")
    os.makedirs(d, exist_ok=True)
    _git(d, "init", "-q")
    _git(d, "config", "user.email", "t@n.l")
    _git(d, "config", "user.name", "t")
    with open(os.path.join(d, "a.py"), "w") as f:
        f.write("x = 1\n")
    _git(d, "add", "-A")
    _git(d, "commit", "-qm", "root")
    sha = _git(d, "rev-parse", "HEAD")
    assert "unavailable" in instrument.mechanical_signals(d, sha)
    judgments = [_j(dim, 6, [_file_ev("a.py", lines="1-1")])
                 for dim in instrument.DIMENSIONS]
    card = instrument.grade_packet(_packet(sha, judgments), d, sha)
    assert card["score"] == 6.0  # graded fine; mechanical just unavailable


def test_pilot_skeleton_builds_from_real_merge():
    skel = instrument.build_skeleton(REPO_ROOT, "HEAD", pr="0", title="t")
    assert skel["packet_version"] == 1
    assert skel["change_id"] == "PR-0"
    assert len(skel["judgments"]) == 5
    assert all(j["score"] is None for j in skel["judgments"])
    assert skel["_mechanical_preview"]["files_changed"] >= 1


# ---------------------------------------------------------------- to-event bridge

def _real_value_card():
    return {
        "packet_version": 1,
        "change_id": "PR-TEST",
        "title": "test change",
        "merge_sha": "abc1234",
        "grader": "test",
        "disqualified": False,
        "score": 8.8,
        "verdict": "REAL VALUE",
        "why_not_10": "PROOF=8.0 — t",
    }


def test_to_event_mints_schema_valid_event(repo):
    event = instrument.to_ledger_event(
        _real_value_card(), recorded_at="2026-10-11",
        receipt_ref="tools/human_value/pilot/packets.json",
        pr_url="https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1")
    validated = validate_event(event)  # the REAL schema.py — must not raise
    assert validated["event_id"] == "HV-20261011-PR-TEST"
    assert validated["value_type"] == "useful_outcome"
    assert validated["value_units"] == 1.0
    assert validated["beneficiary"] == "team"
    assert validated["delta_v_actual"] == pytest.approx(7.6)
    assert len(validated["evidence"]) == 2


def test_to_event_delta_v_mapping():
    card = _real_value_card()
    for score, expected in ((10.0, 10.0), (8.8, 7.6), (7.0, 4.0), (5.0, 0.0)):
        card["score"] = score
        event = instrument.to_ledger_event(
            card, recorded_at="2026-10-11", receipt_ref="x")
        assert event["delta_v_actual"] == pytest.approx(expected), score


@pytest.mark.parametrize("verdict", ["THIN", "NO VALUE"])
def test_to_event_refuses_below_real_value(verdict):
    card = _real_value_card()
    card["verdict"] = verdict
    card["score"] = 6.0
    with pytest.raises(instrument.InstrumentError, match="mints no event"):
        instrument.to_ledger_event(card, recorded_at="2026-10-11",
                                   receipt_ref="x")


def test_to_event_refuses_disqualified():
    card = _real_value_card()
    card["disqualified"] = True
    with pytest.raises(instrument.InstrumentError, match="DISQUALIFIED"):
        instrument.to_ledger_event(card, recorded_at="2026-10-11",
                                   receipt_ref="x")


def test_to_event_needs_evidence_pointer():
    with pytest.raises(instrument.InstrumentError, match="evidence pointer"):
        instrument.to_ledger_event(_real_value_card(), recorded_at="2026-10-11")


def test_to_event_bad_score_fails_safe():
    card = _real_value_card()
    card["score"] = "lots"
    with pytest.raises(instrument.InstrumentError, match="unusable score"):
        instrument.to_ledger_event(card, recorded_at="2026-10-11",
                                   receipt_ref="x")


def test_to_event_cli_refuses_thin_with_exit_2(repo, tmp_path):
    """CLI: THIN scorecard -> exit 2, no event file created. Fail safe."""
    d, sha = repo
    judgments = [_j(dim, 6, [_file_ev("widget.py")]) for dim in instrument.DIMENSIONS]
    card = instrument.grade_packet(_packet(sha, judgments), d, sha)
    assert card["verdict"] == "THIN"
    card_path = tmp_path / "thin.json"
    card_path.write_text(json.dumps(card))
    out_path = tmp_path / "event.json"
    r = subprocess.run(
        [sys.executable, os.path.join(REPO_ROOT, "tools", "human_value",
                                      "instrument.py"),
         "to-event", "--scorecard", str(card_path), "--out", str(out_path),
         "--date", "2026-10-11", "--receipt-ref", "x"],
        capture_output=True, text=True, timeout=60)
    assert r.returncode == 2
    assert not out_path.exists()
    assert "mints no event" in r.stderr

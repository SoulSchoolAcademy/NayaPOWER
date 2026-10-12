"""Hardening tests for the human-value change-grade instrument v2 (2026-10-11).

Covers the three fixes the full 28-change observatory run exposed as the
instrument's sharpest weaknesses:

F1. Receipts as first-class evidence (the attested loophole): a committed,
    machine-readable receipt is verified-but-soft evidence — it carries a
    judgment up to 8, flagged RECEIPT_SOFT_CAP above that; a malformed
    receipt verifies to nothing.
F2. Second-seat grading (correlated single-grader judgment): `compare`
    reports agreement bands per dimension instead of averaging disagreement
    away.
F3. Durability re-grade loop (DURABLE was a prediction, never re-checked):
    `recheck` re-verifies every cited piece of evidence at a later ref and
    reports HELD / ROTTED / MIXED per dimension.
Also: mechanical branch deltas (pre-merge branch heads diff against
merge-base, not head^1), and the durable_check_due_utc stamp on scorecards.
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


def _git(cwd, *args):
    r = subprocess.run(["git", "-C", cwd, *args],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, f"git {' '.join(args)} failed: {r.stderr}"
    return r.stdout.strip()


@pytest.fixture()
def repo():
    d = tempfile.mkdtemp(prefix="hvh2-")
    _git(d, "init", "-q")
    _git(d, "config", "user.email", "test@naya.local")
    _git(d, "config", "user.name", "hvh2-test")
    _git(d, "commit", "-q", "--allow-empty", "-m", "root")
    os.makedirs(os.path.join(d, "tests"), exist_ok=True)
    os.makedirs(os.path.join(d, "receipts"), exist_ok=True)
    with open(os.path.join(d, "widget.py"), "w") as f:
        f.write("def run():\n    return 42\n")
    with open(os.path.join(d, "tests", "test_widget.py"), "w") as f:
        f.write("def test_run():\n    assert True\n")
    receipt = {
        "receipt_version": 1,
        "change_id": "PR-TEST",
        "recorded_at": "2026-10-11",
        "metrics": [
            {"name": "checks passing", "before": 10, "after": 42,
             "unit": "count", "how_measured": "pytest -q tail line"},
        ],
        "notes": "before/after from the same suite command",
    }
    with open(os.path.join(d, "receipts", "PR-TEST.json"), "w") as f:
        json.dump(receipt, f)
    _git(d, "add", "-A")
    _git(d, "commit", "-qm", "add widget with tests and receipt")
    sha = _git(d, "rev-parse", "HEAD")
    return d, sha


def _packet(sha, judgments, change_id="PR-TEST"):
    return {
        "packet_version": 1,
        "change_id": change_id,
        "title": "test change",
        "merge_sha": sha,
        "grader": "test",
        "harm_check": {"found": False, "note": ""},
        "judgments": judgments,
    }


def _j(dim, score, evidence=()):
    return {"dimension": dim, "score": score, "rationale": "t",
            "evidence": list(evidence)}


def _receipt_ev(path="receipts/PR-TEST.json"):
    return {"kind": "receipt", "path": path, "note": "t"}


def _test_ev(path="tests/test_widget.py", lines="1-2"):
    return {"kind": "test", "path": path, "lines": lines, "note": "t"}


# ---------------------------------------------------------------- F1: receipts

def test_receipt_verifies_and_carries_delta_to_eight(repo):
    """A valid in-repo receipt is verified evidence — DELTA can reach 8."""
    d, sha = repo
    card = instrument.grade_packet(_packet(sha, [
        _j("USE", 8, [_test_ev()]),
        _j("DELTA", 8, [_receipt_ev()]),
        _j("PROOF", 8, [_test_ev()]),
        _j("DURABLE", 7, [_test_ev()]),
        _j("CLEAN", 8, [_test_ev()]),
    ]), d, sha)
    delta = next(j for j in card["judgments"] if j["dimension"] == "DELTA")
    assert delta["applied"] == 8.0
    assert delta["flags"] == []
    ledger = [e for e in card["evidence_ledger"]
              if e["dimension"] == "DELTA"]
    assert ledger[0]["status"] == "VERIFIED"


def test_receipt_soft_cap_above_eight(repo):
    """Receipt-only evidence cannot push a judgment above 8."""
    d, sha = repo
    card = instrument.grade_packet(_packet(sha, [
        _j("USE", 8, [_test_ev()]),
        _j("DELTA", 10, [_receipt_ev()]),
        _j("PROOF", 8, [_test_ev()]),
        _j("DURABLE", 7, [_test_ev()]),
        _j("CLEAN", 8, [_test_ev()]),
    ]), d, sha)
    delta = next(j for j in card["judgments"] if j["dimension"] == "DELTA")
    assert delta["applied"] == 8.0
    assert delta["flags"] == ["RECEIPT_SOFT_CAP"]


def test_receipt_plus_hard_evidence_has_no_soft_cap(repo):
    """Receipt alongside harder evidence (tests) is not soft-capped."""
    d, sha = repo
    card = instrument.grade_packet(_packet(sha, [
        _j("USE", 9, [_test_ev()]),
        _j("DELTA", 9, [_receipt_ev(), _test_ev()]),
        _j("PROOF", 8, [_test_ev()]),
        _j("DURABLE", 7, [_test_ev()]),
        _j("CLEAN", 8, [_test_ev()]),
    ]), d, sha)
    delta = next(j for j in card["judgments"] if j["dimension"] == "DELTA")
    assert delta["applied"] == 9.0
    assert delta["flags"] == []


def test_malformed_receipt_verifies_to_nothing(repo):
    """A receipt file with no before/after metrics is UNVERIFIABLE."""
    d, sha = repo
    with open(os.path.join(d, "receipts", "PR-BAD.json"), "w") as f:
        json.dump({"receipt_version": 1, "metrics": []}, f)
    _git(d, "add", "-A")
    _git(d, "commit", "-qm", "bad receipt")
    sha2 = _git(d, "rev-parse", "HEAD")
    card = instrument.grade_packet(_packet(sha2, [
        _j("USE", 8, [_test_ev()]),
        _j("DELTA", 7, [_receipt_ev("receipts/PR-BAD.json")]),
        _j("PROOF", 8, [_test_ev()]),
        _j("DURABLE", 7, [_test_ev()]),
        _j("CLEAN", 8, [_test_ev()]),
    ], change_id="PR-BAD"), d, sha2)
    delta = next(j for j in card["judgments"] if j["dimension"] == "DELTA")
    # no verified evidence -> the ordinary UNCITED_CAP applies, not the soft cap
    assert delta["applied"] == 5.0
    assert delta["flags"] == ["UNCITED_CAP"]
    ledger = [e for e in card["evidence_ledger"]
              if e["dimension"] == "DELTA"]
    assert ledger[0]["status"] == "UNVERIFIABLE"


def test_missing_receipt_file_unverifiable(repo):
    d, sha = repo
    status, _ = instrument.verify_evidence(
        {"kind": "receipt", "path": "receipts/NOPE.json"}, d, sha)
    assert status == "UNVERIFIABLE"


def test_receipt_template_is_schema_valid():
    tpl = instrument.receipt_template("PR-X")
    assert tpl["receipt_version"] == 1
    assert tpl["change_id"] == "PR-X"
    assert isinstance(tpl["metrics"], list) and tpl["metrics"]
    m = tpl["metrics"][0]
    assert "before" in m and "after" in m and "name" in m


# ---------------------------------------------------------------- F2: compare

def _card(grader, applied, verdict, score):
    return {
        "change_id": "PR-CMP",
        "grader": grader,
        "score": score,
        "verdict": verdict,
        "judgments": [
            {"dimension": dim, "applied": v, "claimed": v}
            for dim, v in zip(
                ("USE", "DELTA", "PROOF", "DURABLE", "CLEAN"), applied)
        ],
    }


def test_compare_identical_is_trust():
    a = _card("g1", (8, 8, 8, 8, 8), "REAL VALUE", 8.0)
    b = _card("g2", (8, 8, 8, 8, 8), "REAL VALUE", 8.0)
    r = instrument.compare_scorecards(a, b)
    assert r["standing"] == "TRUST"
    assert r["n_agree"] == 5 and r["n_dispute"] == 0
    assert r["verdict_match"] is True


def test_compare_small_gap_is_review():
    a = _card("g1", (8, 8, 8, 8, 8), "REAL VALUE", 8.0)
    b = _card("g2", (8, 6, 8, 8, 8), "THIN", 7.6)
    r = instrument.compare_scorecards(a, b)
    delta = next(d for d in r["dimensions"] if d["dimension"] == "DELTA")
    assert delta["band"] == "review"
    assert r["verdict_match"] is False
    assert r["standing"] == "REVIEW"  # disagreement visible, not averaged


def test_compare_large_gap_is_dispute():
    a = _card("g1", (9, 9, 9, 9, 9), "HIGH VALUE", 9.0)
    b = _card("g2", (9, 4, 9, 9, 9), "REAL VALUE", 8.0)
    r = instrument.compare_scorecards(a, b)
    delta = next(d for d in r["dimensions"] if d["dimension"] == "DELTA")
    assert delta["band"] == "dispute"
    assert r["n_dispute"] == 1
    assert r["standing"] == "DISPUTE"


def test_compare_needs_matching_dimensions():
    a = _card("g1", (8, 8, 8, 8, 8), "REAL VALUE", 8.0)
    b = dict(a)
    b["judgments"] = b["judgments"][:4]
    with pytest.raises(instrument.InstrumentError):
        instrument.compare_scorecards(a, b)


# ---------------------------------------------------------------- F3: recheck

def _full_card(repo_sha, evidence):
    return _packet(repo_sha, [
        _j("USE", 8, evidence), _j("DELTA", 7, evidence),
        _j("PROOF", 8, evidence), _j("DURABLE", 7, evidence),
        _j("CLEAN", 8, evidence),
    ])


def test_recheck_held_at_same_ref(repo):
    d, sha = repo
    card = instrument.grade_packet(
        _full_card(sha, [_test_ev()]), d, sha)
    r = instrument.recheck_scorecard(card, d, sha)
    assert r["per_dimension"]["DURABLE"] == "HELD"
    assert r["rotted"] == 0
    assert "HELD" in r["durability_reading"]


def test_recheck_rotted_after_deletion(repo):
    d, sha = repo
    card = instrument.grade_packet(
        _full_card(sha, [_test_ev()]), d, sha)
    os.remove(os.path.join(d, "tests", "test_widget.py"))
    _git(d, "add", "-A")
    _git(d, "commit", "-qm", "remove the test")
    later = _git(d, "rev-parse", "HEAD")
    r = instrument.recheck_scorecard(card, d, later)
    assert r["per_dimension"]["USE"] == "ROTTED"
    assert r["rotted"] == 5
    assert "ROTTED" in r["durability_reading"]


def test_recheck_mixed_when_partly_rotted(repo):
    d, sha = repo
    card = instrument.grade_packet(
        _full_card(sha, [_test_ev(), _receipt_ev()]), d, sha)
    os.remove(os.path.join(d, "tests", "test_widget.py"))
    _git(d, "add", "-A")
    _git(d, "commit", "-qm", "remove the test only")
    later = _git(d, "rev-parse", "HEAD")
    r = instrument.recheck_scorecard(card, d, later)
    assert r["per_dimension"]["USE"] == "MIXED"
    assert r["held"] == 5 and r["rotted"] == 5


def test_recheck_attested_is_not_recheckable(repo):
    d, sha = repo
    card = instrument.grade_packet(
        _full_card(sha, [{"kind": "command", "note": "someone ran it"}]), d, sha)
    r = instrument.recheck_scorecard(card, d, sha)
    assert r["per_dimension"]["USE"] == "NOT_RECHECKABLE"


def test_recheck_detects_content_drift(repo):
    """A file that still exists but says something different is flagged:
    the 'regens rot' case — HELD but CHANGED."""
    d, sha = repo
    card = instrument.grade_packet(
        _full_card(sha, [_test_ev()]), d, sha)
    with open(os.path.join(d, "tests", "test_widget.py"), "a") as f:
        f.write("\ndef test_also():\n    assert True\n")
    _git(d, "add", "-A")
    _git(d, "commit", "-qm", "extend the test file")
    later = _git(d, "rev-parse", "HEAD")
    r = instrument.recheck_scorecard(card, d, later)
    assert r["per_dimension"]["USE"] == "HELD"
    assert r["content_drifted"] == 5
    assert r["items"][0]["content_drift"] == "CHANGED"
    assert "partly rotted" in r["durability_reading"]


def test_scorecard_carries_durability_due_date(repo):
    d, sha = repo
    card = instrument.grade_packet(
        _full_card(sha, [_test_ev()]), d, sha)
    assert "durable_check_due_utc" in card
    assert card["durable_check_due_utc"] > card["graded_at_utc"]


# ---------------------------------------------------------------- branch mechanical

def test_mechanical_branch_head_uses_merge_base():
    """A pre-merge branch head diffs against merge-base, not head^1."""
    d = tempfile.mkdtemp(prefix="hvbr-")
    _git(d, "init", "-q")
    _git(d, "config", "user.email", "test@naya.local")
    _git(d, "config", "user.name", "hvbr-test")
    _git(d, "commit", "-q", "--allow-empty", "-m", "root")
    with open(os.path.join(d, "main.py"), "w") as f:
        f.write("x=1\n")
    _git(d, "add", "-A")
    _git(d, "commit", "-qm", "main work")
    main_tip = _git(d, "rev-parse", "HEAD")
    # origin/main ref, as a fetched remote would have it
    _git(d, "update-ref", "refs/remotes/origin/main", main_tip)
    _git(d, "checkout", "-qb", "feature")
    with open(os.path.join(d, "a.py"), "w") as f:
        f.write("a=1\n")
    _git(d, "add", "-A")
    _git(d, "commit", "-qm", "branch commit 1")
    with open(os.path.join(d, "b.py"), "w") as f:
        f.write("b=2\n")
    _git(d, "add", "-A")
    _git(d, "commit", "-qm", "branch commit 2")
    head = _git(d, "rev-parse", "HEAD")
    mech = instrument.mechanical_signals(d, head)
    names = set(mech["files"])
    assert names == {"a.py", "b.py"}, f"branch delta understated: {names}"
    assert mech["insertions"] == 2

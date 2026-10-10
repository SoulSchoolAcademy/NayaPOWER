"""Tests for tools/evolve_proposals.py — EVOLVE proposal-lifecycle ledger.

Hermetic: every test gets its own tmp root; the repo itself is never
mutated. The tool is exercised through its real CLI so the fail-closed
exit codes (0=ok, 1=operational refusal, 2=forbidden) are part of the
contract being tested.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "evolve_proposals.py"


def run_tool(root: Path, *argv: str):
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root), *argv],
        capture_output=True,
        text=True,
        timeout=60,
    )


def record(root: Path, pid: str = "gap-1", actor: str = "naya-4"):
    return run_tool(
        root,
        "record",
        "--id",
        pid,
        "--title",
        "Test proposal",
        "--gap",
        "the system cannot see its own improvement rate",
        "--actor",
        actor,
    )


def transition(root: Path, pid: str, to: str, actor: str = "naya-4"):
    return run_tool(
        root,
        "transition",
        "--id",
        pid,
        "--to",
        to,
        "--actor",
        actor,
        "--reason",
        f"test move to {to}",
    )


def status_of(root: Path, pid: str) -> dict:
    r = run_tool(root, "status", "--id", pid)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


# ---------------------------------------------------------------------------
# record
# ---------------------------------------------------------------------------


def test_record_creates_observed_gap(tmp_path):
    r = record(tmp_path)
    assert r.returncode == 0, r.stderr
    body = json.loads(r.stdout)
    assert body == {"id": "gap-1", "state": "OBSERVED_GAP"}
    ledger = tmp_path / ".naya" / "evolve" / "proposals" / "gap-1" / "ledger.jsonl"
    assert ledger.exists()
    lines = ledger.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["to"] == "OBSERVED_GAP" and entry["from"] is None


def test_record_duplicate_is_operational_refusal(tmp_path):
    assert record(tmp_path).returncode == 0
    r = record(tmp_path)
    assert r.returncode == 1
    assert "already recorded" in r.stderr


def test_record_rejects_bad_id(tmp_path):
    r = run_tool(
        tmp_path, "record", "--id", "BAD ID!", "--title", "t", "--gap", "g",
        "--actor", "a",
    )
    assert r.returncode == 2
    assert "invalid proposal id" in r.stderr


# ---------------------------------------------------------------------------
# transition
# ---------------------------------------------------------------------------


def test_valid_transition_moves_state(tmp_path):
    assert record(tmp_path).returncode == 0
    r = transition(tmp_path, "gap-1", "PROPOSED")
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout) == {
        "id": "gap-1",
        "from": "OBSERVED_GAP",
        "to": "PROPOSED",
    }
    assert status_of(tmp_path, "gap-1")["state"] == "PROPOSED"


def test_forbidden_transition_is_fail_closed_and_names_allowed(tmp_path):
    assert record(tmp_path).returncode == 0
    r = transition(tmp_path, "gap-1", "ADOPTED")
    assert r.returncode == 2
    assert "forbidden transition OBSERVED_GAP -> ADOPTED" in r.stderr
    assert "PROPOSED" in r.stderr and "REJECTED" in r.stderr
    # state unchanged after the refused transition
    assert status_of(tmp_path, "gap-1")["state"] == "OBSERVED_GAP"


def test_transition_unknown_proposal_is_operational_refusal(tmp_path):
    r = transition(tmp_path, "nope", "PROPOSED")
    assert r.returncode == 1
    assert "not found" in r.stderr


def test_transition_unknown_state_is_fail_closed(tmp_path):
    assert record(tmp_path).returncode == 0
    r = transition(tmp_path, "gap-1", "ASCENDED")
    assert r.returncode == 2
    assert "unknown state" in r.stderr


def test_terminal_state_accepts_no_transitions(tmp_path):
    assert record(tmp_path).returncode == 0
    assert transition(tmp_path, "gap-1", "REJECTED").returncode == 0
    r = transition(tmp_path, "gap-1", "PROPOSED")
    assert r.returncode == 2
    assert "terminal (REJECTED)" in r.stderr


def test_full_lifecycle_to_adopted(tmp_path):
    assert record(tmp_path).returncode == 0
    path = [
        "PROPOSED",
        "ANALYZED",
        "NEEDS_AUTHORITY",
        "AUTHORIZED",
        "IMPLEMENTED",
        "VERIFIED",
    ]
    for state in path:
        r = transition(tmp_path, "gap-1", state)
        assert r.returncode == 0, (state, r.stderr)
    # The ADOPT gate: adoption requires a measured-improvement receipt.
    receipt = write_receipt(tmp_path / "receipt.json")
    r = adopt(tmp_path, "gap-1", receipt)
    assert r.returncode == 0, r.stderr
    summary = status_of(tmp_path, "gap-1")
    assert summary["state"] == "ADOPTED"
    assert summary["transitions"] == len(path) + 1


def test_rolled_back_can_be_reproposed(tmp_path):
    # Rollback is a governed state, not death: the proposal may return to
    # PROPOSED with its full history intact.
    assert record(tmp_path).returncode == 0
    for state in ["PROPOSED", "ANALYZED", "AUTHORIZED", "IMPLEMENTED"]:
        assert transition(tmp_path, "gap-1", state).returncode == 0
    assert transition(tmp_path, "gap-1", "ROLLED_BACK").returncode == 0
    r = transition(tmp_path, "gap-1", "PROPOSED")
    assert r.returncode == 0, r.stderr
    assert status_of(tmp_path, "gap-1")["state"] == "PROPOSED"
    audit = run_tool(tmp_path, "audit", "--id", "gap-1")
    assert audit.returncode == 0
    states = [e["to"] for e in json.loads(audit.stdout)]
    assert "ROLLED_BACK" in states


# ---------------------------------------------------------------------------
# status / list / audit
# ---------------------------------------------------------------------------


def test_status_reports_current_state_and_history(tmp_path):
    assert record(tmp_path).returncode == 0
    assert transition(tmp_path, "gap-1", "PROPOSED").returncode == 0
    s = status_of(tmp_path, "gap-1")
    assert s["id"] == "gap-1"
    assert s["title"] == "Test proposal"
    assert s["state"] == "PROPOSED"
    assert s["transitions"] == 1
    assert s["last_actor"] == "naya-4"


def test_status_unknown_proposal_is_operational_refusal(tmp_path):
    r = run_tool(tmp_path, "status", "--id", "ghost")
    assert r.returncode == 1


def test_list_filters_by_state(tmp_path):
    assert record(tmp_path, pid="a").returncode == 0
    assert record(tmp_path, pid="b").returncode == 0
    assert transition(tmp_path, "a", "PROPOSED").returncode == 0
    r = run_tool(tmp_path, "list")
    assert r.returncode == 0
    assert {p["id"] for p in json.loads(r.stdout)} == {"a", "b"}
    r = run_tool(tmp_path, "list", "--state", "PROPOSED")
    assert r.returncode == 0
    assert [p["id"] for p in json.loads(r.stdout)] == ["a"]


def test_audit_returns_ordered_history(tmp_path):
    assert record(tmp_path).returncode == 0
    assert transition(tmp_path, "gap-1", "PROPOSED").returncode == 0
    r = run_tool(tmp_path, "audit", "--id", "gap-1")
    assert r.returncode == 0
    entries = json.loads(r.stdout)
    assert [e["to"] for e in entries] == ["OBSERVED_GAP", "PROPOSED"]
    assert all("ts" in e and "actor" in e and "reason" in e for e in entries)


def test_evidence_link_recorded_on_transition(tmp_path):
    assert record(tmp_path).returncode == 0
    r = run_tool(
        tmp_path,
        "transition",
        "--id",
        "gap-1",
        "--to",
        "PROPOSED",
        "--actor",
        "naya-4",
        "--reason",
        "gap analyzed",
        "--evidence",
        "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1734",
    )
    assert r.returncode == 0, r.stderr
    audit = json.loads(run_tool(tmp_path, "audit", "--id", "gap-1").stdout)
    assert audit[-1]["evidence"].endswith("/pull/1734")


def test_state_derives_from_ledger_not_a_cache(tmp_path):
    # There is no index file anywhere: current state must come from the
    # ledger tail alone, so it can never drift from it.
    assert record(tmp_path).returncode == 0
    assert transition(tmp_path, "gap-1", "PROPOSED").returncode == 0
    store = tmp_path / ".naya" / "evolve" / "proposals"
    files = [p.name for p in store.rglob("*") if p.is_file()]
    assert files == ["ledger.jsonl"], files


# ---------------------------------------------------------------------------
# ADOPT gate — measured improvement proof, not asserted improvement
# ---------------------------------------------------------------------------


def walk_to_verified(root: Path, pid: str = "gap-1"):
    assert record(root, pid=pid).returncode == 0
    for state in [
        "PROPOSED",
        "ANALYZED",
        "NEEDS_AUTHORITY",
        "AUTHORIZED",
        "IMPLEMENTED",
        "VERIFIED",
    ]:
        r = transition(root, pid, state)
        assert r.returncode == 0, (state, r.stderr)


def write_receipt(path: Path, pid: str = "gap-1", **overrides) -> Path:
    receipt = {
        "proposal_id": pid,
        "verdict": "improved",
        "measured": [
            {
                "metric": "improvement coverage",
                "before": 0.0,
                "after": 1.0,
                "method": "hermetic before/after measurement",
            }
        ],
        "measured_at": "2026-10-08T20:50:00+00:00",
    }
    receipt.update(overrides)
    path.write_text(json.dumps(receipt), encoding="utf-8")
    return path


def adopt(root: Path, pid: str, receipt: Path | None):
    argv = [
        "transition",
        "--id",
        pid,
        "--to",
        "ADOPTED",
        "--actor",
        "naya-4",
        "--reason",
        "measured improvement proven",
    ]
    if receipt is not None:
        argv += ["--receipt", str(receipt)]
    return run_tool(root, *argv)


def test_adopt_without_receipt_is_refused(tmp_path):
    walk_to_verified(tmp_path)
    r = adopt(tmp_path, "gap-1", None)
    assert r.returncode == 2
    assert "requires a measured-improvement receipt" in r.stderr
    # state unchanged after the refused adoption
    assert status_of(tmp_path, "gap-1")["state"] == "VERIFIED"


def test_adopt_with_unreadable_receipt_is_refused(tmp_path):
    walk_to_verified(tmp_path)
    r = adopt(tmp_path, "gap-1", tmp_path / "missing.json")
    assert r.returncode == 2
    assert "cannot read receipt" in r.stderr
    assert status_of(tmp_path, "gap-1")["state"] == "VERIFIED"


def test_adopt_with_malformed_receipt_is_refused(tmp_path):
    walk_to_verified(tmp_path)
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    r = adopt(tmp_path, "gap-1", bad)
    assert r.returncode == 2
    assert "not valid JSON" in r.stderr


def test_adopt_with_non_improved_verdict_is_refused(tmp_path):
    walk_to_verified(tmp_path)
    rp = write_receipt(tmp_path / "r.json", verdict="no_change")
    r = adopt(tmp_path, "gap-1", rp)
    assert r.returncode == 2
    assert "verdict is 'no_change'" in r.stderr
    assert "speculative adoption refused" in r.stderr


def test_adopt_with_empty_measured_is_refused(tmp_path):
    walk_to_verified(tmp_path)
    rp = write_receipt(tmp_path / "r.json", measured=[])
    r = adopt(tmp_path, "gap-1", rp)
    assert r.returncode == 2
    assert "no measured deltas" in r.stderr


def test_adopt_with_missing_delta_fields_is_refused(tmp_path):
    walk_to_verified(tmp_path)
    rp = write_receipt(
        tmp_path / "r.json", measured=[{"metric": "x", "before": 1}]
    )
    r = adopt(tmp_path, "gap-1", rp)
    assert r.returncode == 2
    assert "missing 'after'" in r.stderr


def test_adopt_with_id_mismatch_is_refused(tmp_path):
    walk_to_verified(tmp_path)
    rp = write_receipt(tmp_path / "r.json", pid="other-proposal")
    r = adopt(tmp_path, "gap-1", rp)
    assert r.returncode == 2
    assert "does not match" in r.stderr


def test_adopt_with_valid_receipt_succeeds_and_seals_hash(tmp_path):
    walk_to_verified(tmp_path)
    rp = write_receipt(tmp_path / "r.json")
    r = adopt(tmp_path, "gap-1", rp)
    assert r.returncode == 0, r.stderr
    assert status_of(tmp_path, "gap-1")["state"] == "ADOPTED"
    audit = json.loads(run_tool(tmp_path, "audit", "--id", "gap-1").stdout)
    last = audit[-1]
    assert last["receipt_sha256"] == hashlib.sha256(rp.read_bytes()).hexdigest()
    assert last["receipt_verdict"] == "improved"


def test_receipt_on_non_adopted_transition_is_refused(tmp_path):
    # --receipt on any other transition signals a mistyped target state.
    assert record(tmp_path).returncode == 0
    rp = write_receipt(tmp_path / "r.json")
    r = run_tool(
        tmp_path,
        "transition",
        "--id",
        "gap-1",
        "--to",
        "PROPOSED",
        "--actor",
        "naya-4",
        "--reason",
        "x",
        "--receipt",
        str(rp),
    )
    assert r.returncode == 2
    assert "only meaningful on the ADOPTED transition" in r.stderr


def test_rolled_back_from_verified_needs_no_receipt(tmp_path):
    # The gate is ADOPTED-specific: rejecting an implementation stays free.
    walk_to_verified(tmp_path)
    r = transition(tmp_path, "gap-1", "ROLLED_BACK")
    assert r.returncode == 0, r.stderr
    assert status_of(tmp_path, "gap-1")["state"] == "ROLLED_BACK"

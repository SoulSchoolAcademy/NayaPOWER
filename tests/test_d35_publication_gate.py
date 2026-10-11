"""Tests for the D35 publication-boundary gate (tools/d35_publication_gate.py).

Every test runs against the REAL D35 engine (drift_canary/d35_publication).
The gate is fail-closed: unknown shapes are BROKEN, refused content is
VIOLATION, and only an exact asserted==actual match passes.
"""

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools import d35_publication_gate as gate  # noqa: E402


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": claims}), encoding="utf-8")
    return str(p)


def _claim(cid, asserts, steps, attempt, obligation="test-obligation"):
    return {
        "id": cid,
        "obligation_id": obligation,
        "asserts": asserts,
        "model": {"steps": steps, "attempt": attempt},
    }


def _setup(claim_id="C", ev="E1", worker="W"):
    return [
        {"op": "register_evidence", "ev_id": ev},
        {"op": "qualify", "claim_id": claim_id, "verdict": "REQUALIFIED",
         "evidence_ids": [ev], "scope": ["s1"]},
        {"op": "read", "claim_id": claim_id, "worker_id": worker,
         "as": "m1"},
    ]


def _publish_attempt(manifest="m1", scope=("s1",)):
    return {"op": "publish_summary", "use": manifest, "content": "proj",
            "scope": list(scope)}


# ------------------------------------------------------------------
# Exit-contract: DORMANT
# ------------------------------------------------------------------

def test_dormant_on_zero_claims(tmp_path):
    m = _write_manifest(tmp_path, [])
    assert gate.main(["--manifest", m]) == 0


def test_dormant_on_absent_manifest(tmp_path):
    m = str(tmp_path / "no-such-manifest.json")
    assert gate.main(["--manifest", m]) == 0


# ------------------------------------------------------------------
# GREEN: the engine certifies honest scenarios
# ------------------------------------------------------------------

def test_pass_honest_publication(tmp_path):
    m = _write_manifest(tmp_path, [
        _claim("honest", "PUBLISHED", _setup(), _publish_attempt())])
    assert gate.main(["--manifest", m, "--json"]) == 0


def test_pass_stale_refusal_asserted(tmp_path):
    # The fraud, asserted honestly: the claimant says what the law will
    # do — reject the stale write. The engine agrees: PASS.
    steps = _setup() + [{"op": "revoke_evidence", "ev_id": "E1"}]
    m = _write_manifest(tmp_path, [
        _claim("honest-stale", "STALE_DEPENDENCY", steps,
               _publish_attempt())])
    assert gate.main(["--manifest", m]) == 0


def test_pass_smart_note_replay_asserted_duplicate(tmp_path):
    steps = [
        {"op": "register_evidence", "ev_id": "E1"},
        {"op": "append_smart_note", "event_id": "ev-1",
         "claim_id": "C", "content": "note"},
    ]
    attempt = {"op": "publish_smart_note", "event_id": "ev-1",
               "claim_id": "C", "content": "note"}
    m = _write_manifest(tmp_path, [
        _claim("replay", "DUPLICATE_EVENT", steps, attempt)])
    assert gate.main(["--manifest", m]) == 0


def test_pass_index_pointer_conflict_asserted(tmp_path):
    steps = [{"op": "replace_index_pointer", "new_pointer": "p1",
              "expected_old": None}]
    attempt = {"op": "replace_index_pointer", "new_pointer": "p2",
               "expected_old": "stale-pointer"}
    m = _write_manifest(tmp_path, [
        _claim("index-conflict", "WRITE_CONFLICT", steps, attempt)])
    assert gate.main(["--manifest", m]) == 0


# ------------------------------------------------------------------
# RED: real violations get blocked
# ------------------------------------------------------------------

def _worked_fraud_claim(asserts="PUBLISHED"):
    """The exact worked fraud from the manifest: valid token, revoked
    evidence, delayed write."""
    steps = _setup() + [{"op": "revoke_evidence", "ev_id": "E1"}]
    return _claim("D35-WORKED-STALE-WRITE-AS-PUBLISHED", asserts, steps,
                  _publish_attempt())


def test_violation_worked_fraud_blocked(tmp_path, capsys):
    # The manifest's worked example registered as a claim: the naive
    # checker asserts PUBLISHED, the real engine says STALE_DEPENDENCY.
    m = _write_manifest(tmp_path, [_worked_fraud_claim()])
    assert gate.main(["--manifest", m]) == 1
    out = capsys.readouterr().out
    assert "STALE_DEPENDENCY" in out
    assert "D35-WORKED-STALE-WRITE-AS-PUBLISHED" in out


def test_violation_honest_scenario_falsely_refused(tmp_path):
    # Asserting STALE_DEPENDENCY on an honest publication: the engine
    # commits, so the false refusal is blocked too.
    m = _write_manifest(tmp_path, [
        _claim("false-refusal", "STALE_DEPENDENCY", _setup(),
               _publish_attempt())])
    assert gate.main(["--manifest", m]) == 1


def test_violation_scope_widening(tmp_path, capsys):
    # The writer publishes a scope wider than the read-time pin.
    m = _write_manifest(tmp_path, [
        _claim("scope", "PUBLISHED", _setup(),
               _publish_attempt(scope=("s1", "s2")))])
    assert gate.main(["--manifest", m]) == 1
    assert "SCOPE_VIOLATION" in capsys.readouterr().out


def test_violation_write_conflict(tmp_path, capsys):
    # A second writer moves the projection head between W1's read and
    # W1's write (the head-mover appends a smart note in setup). W1's
    # CAS against the pinned head must fail.
    steps2 = _setup() + [
        {"op": "append_smart_note", "event_id": "ev-head",
         "claim_id": "C", "content": "head mover"},
    ]
    m = _write_manifest(tmp_path, [
        _claim("conflict", "PUBLISHED", steps2,
               _publish_attempt(manifest="m1"))])
    assert gate.main(["--manifest", m]) == 1
    assert "WRITE_CONFLICT" in capsys.readouterr().out


def test_violation_forged_token(tmp_path, capsys):
    # A token issued by a foreign authority: the boundary rejects it.
    steps = [
        {"op": "register_evidence", "ev_id": "E1"},
        {"op": "read_foreign", "claim_id": "C", "worker_id": "W",
         "as": "mF"},
    ]
    m = _write_manifest(tmp_path, [
        _claim("forged", "PUBLISHED", steps,
               _publish_attempt(manifest="mF"))])
    assert gate.main(["--manifest", m]) == 1
    assert "TOKEN_REJECTED" in capsys.readouterr().out


def test_violation_stale_successor_package(tmp_path, capsys):
    # A successor package sealed at R5 must fail reconciliation at R8.
    steps = [
        {"op": "register_evidence", "ev_id": "E1"},
        {"op": "qualify", "claim_id": "C", "verdict": "REQUALIFIED",
         "evidence_ids": ["E1"], "scope": ["s1"]},
        {"op": "seal_package", "claim_id": "C", "as": "p1"},
        {"op": "revoke_evidence", "ev_id": "E1"},
    ]
    attempt = {"op": "reconcile_package", "use": "p1"}
    m = _write_manifest(tmp_path, [
        _claim("stale-package", "PUBLISHED", steps, attempt)])
    assert gate.main(["--manifest", m]) == 1
    assert "STALE_DEPENDENCY" in capsys.readouterr().out


# ------------------------------------------------------------------
# Fail-closed: BROKEN, never defaulted
# ------------------------------------------------------------------

def test_broken_corrupt_manifest(tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json", encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_broken_unknown_assertion(tmp_path):
    m = _write_manifest(tmp_path, [
        _claim("x", "MAYBE", _setup(), _publish_attempt())])
    assert gate.main(["--manifest", str(m)]) == 2


def test_broken_duplicate_claim_id(tmp_path):
    c = _claim("dup", "PUBLISHED", _setup(), _publish_attempt())
    m = _write_manifest(tmp_path, [c, dict(c)])
    assert gate.main(["--manifest", str(m)]) == 2


def test_broken_unknown_setup_op(tmp_path):
    steps = [{"op": "time_travel", "to": "yesterday"}]
    m = _write_manifest(tmp_path, [
        _claim("x", "PUBLISHED", steps, _publish_attempt())])
    assert gate.main(["--manifest", str(m)]) == 2


def test_broken_unknown_attempt_op(tmp_path):
    attempt = {"op": "publish_telepathy", "use": "m1"}
    m = _write_manifest(tmp_path, [
        _claim("x", "PUBLISHED", _setup(), attempt)])
    assert gate.main(["--manifest", str(m)]) == 2


def test_broken_engine_construction_failure(tmp_path):
    # Qualifying on unknown evidence: the engine cannot construct the
    # scenario — the manifest is untrustworthy, not the content.
    steps = [{"op": "qualify", "claim_id": "C", "verdict": "REQUALIFIED",
              "evidence_ids": ["NOPE"], "scope": ["s1"]}]
    m = _write_manifest(tmp_path, [
        _claim("x", "PUBLISHED", steps, _publish_attempt())])
    assert gate.main(["--manifest", str(m)]) == 2


def test_broken_mechanism_missing_with_claims(tmp_path, monkeypatch):
    m = _write_manifest(tmp_path, [
        _claim("x", "PUBLISHED", _setup(), _publish_attempt())])

    def _missing():
        raise gate.MechanismMissing("simulated absent engine")

    monkeypatch.setattr(gate, "_load_mechanism", _missing)
    assert gate.main(["--manifest", str(m)]) == 2


def test_broken_missing_manifest_fields(tmp_path):
    m = _write_manifest(tmp_path, [{"id": "x"}])  # no model/obligation
    assert gate.main(["--manifest", str(m)]) == 2


# ------------------------------------------------------------------
# The manifest's worked examples, end to end
# ------------------------------------------------------------------

def test_manifest_example_fraud_would_block(tmp_path, capsys):
    example = json.loads(
        (REPO_ROOT / "tools" / "d35_publication_manifest.json")
        .read_text(encoding="utf-8"))["_example"]
    m = _write_manifest(tmp_path, [example])
    assert gate.main(["--manifest", str(m)]) == 1
    assert "STALE_DEPENDENCY" in capsys.readouterr().out


def test_manifest_example_honest_would_pass(tmp_path):
    example = json.loads(
        (REPO_ROOT / "tools" / "d35_publication_manifest.json")
        .read_text(encoding="utf-8"))["_example_honest"]
    m = _write_manifest(tmp_path, [example])
    assert gate.main(["--manifest", str(m)]) == 0

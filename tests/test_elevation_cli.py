"""Elevation CLI (GAP 1, 9-node wiring Phase 1): elevate / ratify / activate.

Operational path for VERIFIED->RATIFIED->ACTIVE->LEARNED through
truth_state_guard.apply_elevation(). The guard enforces every rule; the CLI
is a pass-through. Every test runs against a temp registry copy — the
canonical registry is never touched.
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

SPEC = importlib.util.spec_from_file_location("smart_note_v2_elev", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

GUARD_SPEC = importlib.util.spec_from_file_location("truth_state_guard_elev", ROOT / "tools" / "truth_state_guard.py")
guard = importlib.util.module_from_spec(GUARD_SPEC)
GUARD_SPEC.loader.exec_module(guard)


def _item(typ="independent_verification", source="naya-1"):
    return {
        "type": typ,
        "source": source,
        "content_hash": hashlib.sha256(f"{typ}:{source}".encode("utf-8")).hexdigest(),
    }


def _entry(sn="SN-E1", ib="IB-E1", state="VERIFIED", scope="PRIVATE"):
    return {
        "smart_note_id": sn,
        "intelligent_block_id": ib,
        "title": "Elevation test note",
        "truth_state": state,
        "lifecycle_state": "ACTIVE",
        "scope": scope,
        "elevation_history": [
            {
                "from": "CANDIDATE", "to": "VERIFIED", "authority": "Naya 1",
                "evidence_hashes": [_item()["content_hash"]],
                "evidence_types": ["independent_verification"],
                "at": "20261009T120000Z", "kind": "elevation",
            }
        ],
    }


def _write_registry(tmp_path, entries):
    p = tmp_path / "index.json"
    p.write_text(json.dumps({"entries": entries}, indent=2), encoding="utf-8")
    return p


def _read_entry(registry_path, sn):
    reg = json.loads(registry_path.read_text(encoding="utf-8"))
    return next(e for e in reg["entries"] if e["smart_note_id"] == sn)


def _predecessor_receipt(sn):
    body = {"note_id": sn, "new_state": "VERIFIED",
            "promoter": "Naya 1", "promoted_at": "20261009T120000Z"}
    body["receipt_hash"] = guard._canonical_hash(body)
    return body


def _run_cli(*argv, cwd):
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / "smart_note_v2.py"), *argv],
        cwd=cwd, capture_output=True, text=True, timeout=120,
    )


# --- VERIFIED -> RATIFIED (grant-gated) -------------------------------------

def test_elevate_verified_to_ratified_with_grant(tmp_path):
    rp = _write_registry(tmp_path, [_entry()])
    grant = guard.make_grant("SN-E1", target_state="RATIFIED")
    result = mod.elevate_note(
        "SN-E1", "RATIFIED", authority="Naya 4",
        evidence={"items": [_item()]}, grant=grant,
        registry_path=str(rp),
    )
    assert result["elevated"] is True
    assert result["record"]["reason_code"] == "ELEVATED"
    assert result["old_state"] == "VERIFIED" and result["new_state"] == "RATIFIED"
    stored = _read_entry(rp, "SN-E1")
    assert stored["truth_state"] == "RATIFIED"
    last = stored["elevation_history"][-1]
    assert last["from"] == "VERIFIED" and last["to"] == "RATIFIED"
    assert last["elevation_grant_id"] == grant["grant_id"]


def test_elevate_verified_to_ratified_refused_without_grant(tmp_path):
    rp = _write_registry(tmp_path, [_entry()])
    before = rp.read_bytes()
    result = mod.elevate_note(
        "SN-E1", "RATIFIED", authority="Naya 4",
        evidence={"items": [_item()]}, registry_path=str(rp),
    )
    assert result["elevated"] is False
    assert result["record"]["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"
    # Rejection is a non-event: registry byte-identical.
    assert rp.read_bytes() == before


def test_ratify_subcommand_end_to_end(tmp_path):
    rp = _write_registry(tmp_path, [_entry()])
    grant = guard.make_grant("SN-E1", target_state="RATIFIED")
    grant_p = tmp_path / "grant.json"
    grant_p.write_text(json.dumps(grant), encoding="utf-8")
    ev_p = tmp_path / "evidence.json"
    ev_p.write_text(json.dumps({"items": [_item()]}), encoding="utf-8")
    r = _run_cli("ratify", "--note", "SN-E1", "--authority", "Naya 4",
                 "--evidence", str(ev_p), "--grant", str(grant_p),
                 "--registry", str(rp), cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["elevated"] is True
    assert out["record"]["reason_code"] == "ELEVATED"
    assert _read_entry(rp, "SN-E1")["truth_state"] == "RATIFIED"


def test_elevate_subcommand_end_to_end_with_inline_json(tmp_path):
    rp = _write_registry(tmp_path, [_entry()])
    grant = guard.make_grant("SN-E1", target_state="RATIFIED")
    r = _run_cli("elevate", "--note", "SN-E1", "--to", "RATIFIED",
                 "--authority", "Naya 4",
                 "--evidence", json.dumps({"items": [_item()]}),
                 "--grant", json.dumps(grant),
                 "--registry", str(rp), cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["elevated"] is True
    assert _read_entry(rp, "SN-E1")["truth_state"] == "RATIFIED"


# --- RATIFIED -> ACTIVE (verified-predecessor receipt) -----------------------

def test_elevate_ratified_to_active(tmp_path):
    rp = _write_registry(tmp_path, [_entry(state="RATIFIED")])
    evidence = {"items": [_item()], "predecessor_receipt": _predecessor_receipt("SN-E1")}
    result = mod.elevate_note("SN-E1", "ACTIVE", authority="Naya 4",
                              evidence=evidence, registry_path=str(rp))
    assert result["elevated"] is True
    assert _read_entry(rp, "SN-E1")["truth_state"] == "ACTIVE"


def test_activate_subcommand_end_to_end(tmp_path):
    rp = _write_registry(tmp_path, [_entry(state="RATIFIED")])
    ev_p = tmp_path / "evidence.json"
    ev_p.write_text(json.dumps(
        {"items": [_item()], "predecessor_receipt": _predecessor_receipt("SN-E1")}),
        encoding="utf-8")
    r = _run_cli("activate", "--note", "SN-E1", "--authority", "Naya 4",
                 "--evidence", str(ev_p), "--registry", str(rp), cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["elevated"] is True
    assert _read_entry(rp, "SN-E1")["truth_state"] == "ACTIVE"


def test_activate_refused_without_predecessor_receipt(tmp_path):
    rp = _write_registry(tmp_path, [_entry(state="RATIFIED")])
    result = mod.elevate_note("SN-E1", "ACTIVE", authority="Naya 4",
                              evidence={"items": [_item()]},
                              registry_path=str(rp))
    assert result["elevated"] is False
    assert result["record"]["reason_code"] == "ACTIVE_REQUIRES_VERIFIED_PREDECESSOR"
    assert _read_entry(rp, "SN-E1")["truth_state"] == "RATIFIED"


# --- ACTIVE -> LEARNED (behavioral evidence) ---------------------------------

def test_elevate_active_to_learned_with_behavioral_evidence(tmp_path):
    rp = _write_registry(tmp_path, [_entry(state="ACTIVE")])
    evidence = {"items": [_item(), _item(typ="behavioral", source="learning-loop")]}
    result = mod.elevate_note("SN-E1", "LEARNED", authority="Naya 4",
                              evidence=evidence, registry_path=str(rp))
    assert result["elevated"] is True
    assert _read_entry(rp, "SN-E1")["truth_state"] == "LEARNED"


def test_learned_refused_without_behavioral_evidence(tmp_path):
    rp = _write_registry(tmp_path, [_entry(state="ACTIVE")])
    result = mod.elevate_note("SN-E1", "LEARNED", authority="Naya 4",
                              evidence={"items": [_item()]},
                              registry_path=str(rp))
    assert result["elevated"] is False
    assert result["record"]["reason_code"] == "LEARNED_REQUIRES_BEHAVIORAL_EVIDENCE"


# --- Guard rails: dry-run, invalid transitions, demotion --------------------

def test_dry_run_reports_without_writing(tmp_path):
    rp = _write_registry(tmp_path, [_entry()])
    before = rp.read_bytes()
    grant = guard.make_grant("SN-E1", target_state="RATIFIED")
    result = mod.elevate_note(
        "SN-E1", "RATIFIED", authority="Naya 4",
        evidence={"items": [_item()]}, grant=grant,
        registry_path=str(rp), dry_run=True,
    )
    assert result["elevated"] is True
    assert result["dry_run"] is True
    assert result["record"]["reason_code"] == "ELEVATED"
    assert rp.read_bytes() == before
    assert _read_entry(rp, "SN-E1")["truth_state"] == "VERIFIED"


def test_dry_run_subcommand_flag(tmp_path):
    rp = _write_registry(tmp_path, [_entry()])
    before = rp.read_bytes()
    grant = guard.make_grant("SN-E1", target_state="RATIFIED")
    r = _run_cli("elevate", "--note", "SN-E1", "--to", "RATIFIED",
                 "--authority", "Naya 4",
                 "--evidence", json.dumps({"items": [_item()]}),
                 "--grant", json.dumps(grant),
                 "--registry", str(rp), "--dry-run", cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["elevated"] is True and out["dry_run"] is True
    assert rp.read_bytes() == before


def test_invalid_transition_candidate_to_ratified_refused(tmp_path):
    rp = _write_registry(tmp_path, [_entry(state="CANDIDATE")])
    before = rp.read_bytes()
    grant = guard.make_grant("SN-E1", target_state="RATIFIED")
    result = mod.elevate_note(
        "SN-E1", "RATIFIED", authority="Shawn Vibert",
        evidence={"items": [_item()]}, grant=grant,
        registry_path=str(rp),
    )
    assert result["elevated"] is False
    assert result["record"]["reason_code"] == "RATIFIED_REQUIRES_VERIFIED_PREDECESSOR"
    assert rp.read_bytes() == before


def test_refused_cli_exits_nonzero_with_receipt(tmp_path):
    rp = _write_registry(tmp_path, [_entry(state="CANDIDATE")])
    r = _run_cli("ratify", "--note", "SN-E1", "--authority", "Naya 4",
                 "--evidence", json.dumps({"items": [_item()]}),
                 "--registry", str(rp), cwd=tmp_path)
    assert r.returncode == 1
    out = json.loads(r.stdout)
    assert out["elevated"] is False
    assert out["record"]["reason_code"] == "RATIFIED_REQUIRES_VERIFIED_PREDECESSOR"


def test_demotion_always_permitted_without_authority_or_evidence(tmp_path):
    rp = _write_registry(tmp_path, [_entry(state="RATIFIED")])
    result = mod.elevate_note("SN-E1", "CANDIDATE", registry_path=str(rp))
    assert result["elevated"] is True
    assert result["record"]["reason_code"] == "DEMOTION_PERMITTED"
    stored = _read_entry(rp, "SN-E1")
    assert stored["truth_state"] == "CANDIDATE"
    assert stored["elevation_history"][-1]["kind"] == "demotion"


def test_elevate_note_not_found_raises(tmp_path):
    rp = _write_registry(tmp_path, [_entry()])
    with pytest.raises(SystemExit) as ei:
        mod.elevate_note("SN-NOPE", "RATIFIED", authority="Naya 4",
                         evidence={"items": [_item()]}, registry_path=str(rp))
    assert "ELEVATION_NOTE_NOT_FOUND" in str(ei.value.code)


def test_elevate_registry_not_found_raises(tmp_path):
    with pytest.raises(SystemExit) as ei:
        mod.elevate_note("SN-E1", "RATIFIED", authority="Naya 4",
                         evidence={"items": [_item()]},
                         registry_path=str(tmp_path / "missing.json"))
    assert "ELEVATION_REGISTRY_NOT_FOUND" in str(ei.value.code)


def test_noop_same_state_reports_without_write(tmp_path):
    rp = _write_registry(tmp_path, [_entry(state="VERIFIED")])
    before = rp.read_bytes()
    result = mod.elevate_note("SN-E1", "VERIFIED", authority="Naya 4",
                              evidence={"items": [_item()]},
                              registry_path=str(rp))
    assert result["elevated"] is True
    assert result["record"]["reason_code"] == "NOOP_SAME_STATE"
    assert rp.read_bytes() == before

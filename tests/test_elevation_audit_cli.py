"""Elevation-history audit: CI enforcement + grandfathered backfill honesty.

Pins the W1/W2 truth wiring (2026-10-08, Naya 5):
- The read-side semantic audit runs against the REAL registry and passes.
- A hand-edited CANDIDATE->RATIFIED elevation with no history fails the
  audit (the #1468 hole class the write-time guard cannot see).
- The CLI fails closed: unreadable registry -> exit 2, never a pass.
- The grandfathered backfill is honest: kind="backfill" (never "elevation"),
  named Human-Director authority, real evidence hashes, historical `at`
  dates, and no manufactured note bytes (SN-0522's missing file is declared).

The guard module is loaded standalone via importlib so the audit is verified
independently of the promotion machinery.
"""
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "tools" / "truth_state_guard.py"
REGISTRY = ROOT / ".naya" / "memory" / "smart-notes" / "index.json"

spec = importlib.util.spec_from_file_location("truth_state_guard", GUARD)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

GRANDFATHERED = ["SN-016", "SN-0340", "SN-0399", "SN-0400",
                 "SN-0408", "SN-0459", "SN-0522", "SN-NET-POWER-MAGIC-001"]


def _registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def _by_id(registry):
    return {str(e.get("smart_note_id")): e
            for e in registry.get("entries", []) if isinstance(e, dict)}


def test_real_registry_passes_semantic_audit():
    r = g.audit_registry_semantics(_registry())
    assert r["ok"], f"defects on real registry: {r['defects']}"
    assert r["entries_scanned"] > 600


def test_grandfathered_entries_carry_honest_history():
    by_id = _by_id(_registry())
    for sid in GRANDFATHERED:
        entry = by_id.get(sid)
        assert entry is not None, f"{sid} missing from registry"
        hist = entry.get("elevation_history") or []
        assert hist, f"{sid} has no elevation history"
        rec = hist[-1]
        assert rec["kind"] == "backfill", f"{sid}: kind must be backfill, not elevation"
        assert rec["authority"] == "Human Director"
        assert rec["evidence_hashes"], f"{sid}: evidence hashes must be real"
        assert all(h.startswith("sha256:") for h in rec["evidence_hashes"])
        assert rec["from"] == "CANDIDATE" and rec["to"] == "RATIFIED"
        # `at` is the historical ratification date, not the backfill date
        assert rec["at"] < rec["recorded_at"]
        assert "constitutional_basis" in rec


def test_sn0522_declares_missing_note_file():
    by_id = _by_id(_registry())
    rec = by_id["SN-0522"]["elevation_history"][-1]
    assert rec["evidence_types"] == ["ratification-record"]
    assert "absent on main" in rec["evidence_sources"][0]


def test_hand_edited_elevation_without_history_fails_audit():
    registry = _registry()
    by_id = _by_id(registry)
    entry = by_id["SN-016"]
    forged = copy.deepcopy(entry)
    forged["truth_state"] = "LEARNED"  # fabricated escalation
    forged.pop("elevation_history", None)
    probe = {"entries": [forged]}
    r = g.audit_registry_semantics(probe)
    assert not r["ok"]
    assert r["defects"]["elevated_without_provenance"] == ["SN-016"]


def test_backfill_is_idempotent():
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        from backfill_grandfathered_elevations import build_record
    finally:
        sys.path.pop(0)
    by_id = _by_id(_registry())
    for sid in GRANDFATHERED:
        record, msg = build_record(by_id[sid])
        assert record is None, f"{sid} should be skipped on re-run: {msg}"


def _run_cli(*args):
    return subprocess.run([sys.executable, str(GUARD), *args],
                          capture_output=True, text=True, cwd=str(ROOT))


def test_cli_exit_zero_on_clean_registry(tmp_path):
    dest = tmp_path / "index.json"
    dest.write_text(REGISTRY.read_text(encoding="utf-8"), encoding="utf-8")
    p = _run_cli("--audit", "--registry", str(dest))
    assert p.returncode == 0, p.stdout + p.stderr
    assert "defects=0" in p.stdout


def test_cli_exit_one_on_elevated_without_history(tmp_path):
    registry = _registry()
    by_id = _by_id(registry)
    forged = copy.deepcopy(by_id["SN-016"])
    forged.pop("elevation_history", None)
    registry["entries"] = [forged]
    dest = tmp_path / "index.json"
    dest.write_text(json.dumps(registry), encoding="utf-8")
    p = _run_cli("--audit", "--registry", str(dest))
    assert p.returncode == 1, p.stdout + p.stderr
    assert "elevated_without_provenance" in p.stdout


def test_cli_exit_two_on_missing_registry():
    p = _run_cli("--audit", "--registry", "/nonexistent/index.json")
    assert p.returncode == 2
    assert "AUDIT_ENVIRONMENT_FAILURE" in p.stdout

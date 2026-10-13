"""B-51 fail-loud index validation — corpus fingerprint tests (Naya Beta, 2026-10-13).

The Smart Note registry (index.json) carries a corpus fingerprint
(commit SHA + active-entry count + payload hash). load_registry() verifies it
at read time and raises IndexDriftError with the exact code B51_INDEX_DRIFT
on ANY mismatch — a drifted index never yields answers silently.
"""
import copy
import importlib.util
import json
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("smart_note_v2_fp", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

REAL_INDEX = ROOT / ".naya" / "memory" / "smart-notes" / "index.json"
EXACT_CODE = "B51_INDEX_DRIFT"


def _stamped_copy(tmp_path):
    """A stamped copy of the real index (commit_sha=None: no git in tmp)."""
    dst = tmp_path / "index.json"
    shutil.copy(REAL_INDEX, dst)
    fp = mod.stamp_registry_file(dst, commit_sha=None)
    assert fp["schema"] == mod.FINGERPRINT_SCHEMA
    return dst


def test_clean_tip_load_passes(tmp_path):
    """MISSION TEST 1: a freshly stamped index loads with zero refusals."""
    dst = _stamped_copy(tmp_path)
    registry = mod.load_registry(dst)
    assert len(registry["entries"]) == 631
    assert registry["corpus_fingerprint"]["active_entry_count"] == 603
    assert registry["_validation"]["corpus_fingerprint"] == "skipped_no_provenance"


def test_committed_index_carries_valid_fingerprint():
    """The index.json committed on this branch verifies against live git."""
    registry = mod.load_registry()  # module default REGISTRY = repo's real index
    fp = registry["corpus_fingerprint"]
    assert fp["schema"] == mod.FINGERPRINT_SCHEMA
    assert isinstance(fp["commit_sha"], str) and len(fp["commit_sha"]) == 40
    assert fp["active_entry_count"] == 603
    assert registry["_validation"]["corpus_fingerprint"] == "verified"


def test_drifted_index_refuses_with_exact_code(tmp_path):
    """MISSION TEST 2: entries removed -> exact refusal code, no silent answer."""
    dst = _stamped_copy(tmp_path)
    drifted = json.loads(dst.read_text(encoding="utf-8"))
    drifted["entries"] = drifted["entries"][:-5]  # silent local drift
    dst.write_text(json.dumps(drifted), encoding="utf-8")
    with pytest.raises(mod.IndexDriftError) as exc_info:
        mod.load_registry(dst)
    assert exc_info.value.code == EXACT_CODE
    assert exc_info.value.reason == "active-entry count mismatch — index drifted relative to its fingerprint"


def test_tampered_payload_refuses_with_exact_code(tmp_path):
    """Content edited with count preserved -> hash check refuses."""
    dst = _stamped_copy(tmp_path)
    tampered = json.loads(dst.read_text(encoding="utf-8"))
    tampered["entries"][0]["title"] = "FORGED TITLE"
    dst.write_text(json.dumps(tampered), encoding="utf-8")
    with pytest.raises(mod.IndexDriftError) as exc_info:
        mod.load_registry(dst)
    assert exc_info.value.code == EXACT_CODE
    assert exc_info.value.reason == "payload hash mismatch — index content changed after stamping"


def test_missing_fingerprint_refuses_with_exact_code(tmp_path):
    """A pre-B-51 index with no fingerprint is refused, not trusted."""
    dst = tmp_path / "index.json"
    shutil.copy(REAL_INDEX, dst)
    stripped = json.loads(dst.read_text(encoding="utf-8"))
    stripped.pop("corpus_fingerprint", None)
    dst.write_text(json.dumps(stripped), encoding="utf-8")
    with pytest.raises(mod.IndexDriftError) as exc_info:
        mod.load_registry(dst)
    assert exc_info.value.code == EXACT_CODE


def test_foreign_commit_refuses_with_exact_code(tmp_path, monkeypatch):
    """An index stamped on a commit foreign to this checkout is refused."""
    dst = _stamped_copy(tmp_path)
    registry = json.loads(dst.read_text(encoding="utf-8"))
    registry["corpus_fingerprint"]["commit_sha"] = "0" * 40
    dst.write_text(json.dumps(registry), encoding="utf-8")
    monkeypatch.setattr(mod, "_git_is_ancestor", lambda commit, near: False)
    with pytest.raises(mod.IndexDriftError) as exc_info:
        mod.load_registry(dst)
    assert exc_info.value.code == EXACT_CODE
    assert exc_info.value.details["reason"] == "commit_mismatch"


def test_transaction_write_restamps_and_stays_loadable(tmp_path, monkeypatch):
    """Writer-side: registry_transaction re-stamps on commit; reads stay green."""
    monkeypatch.setattr(mod, "REGISTRY", tmp_path / "index.json")
    with mod.registry_transaction() as reg:
        reg["entries"] = [
            {"smart_note_id": "SN-1", "lifecycle_state": "ACTIVE"},
            {"smart_note_id": "SN-2", "lifecycle_state": "SUPERSEDED"},
        ]
    loaded = mod.load_registry()
    assert loaded["corpus_fingerprint"]["active_entry_count"] == 1
    assert loaded["corpus_fingerprint"]["payload_sha256"] == mod._payload_sha256(loaded)


def test_error_message_carries_code_and_reason(tmp_path):
    """The refusal is greppable: code + reason in the message, details on the object."""
    dst = _stamped_copy(tmp_path)
    drifted = json.loads(dst.read_text(encoding="utf-8"))
    drifted["entries"] = []
    dst.write_text(json.dumps(drifted), encoding="utf-8")
    try:
        mod.load_registry(dst)
        raise AssertionError("must refuse")
    except mod.IndexDriftError as e:
        assert EXACT_CODE in str(e)
        assert e.code == EXACT_CODE
        assert e.details["reason"] == "active_count_mismatch"
        assert e.details["expected"] == 603
        assert e.details["actual"] == 0

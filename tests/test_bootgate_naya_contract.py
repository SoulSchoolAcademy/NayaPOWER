"""
Red-team tests for the Naya Contract boot-gate wiring (Naya 5, 2026-10-13).

Claims under test:
1. kernel/protocol/protocol_integrity_gate.py verifies the Naya Contract
   (NAYA-CONTRACT-V1.md + naya-contract.json) against pinned manifest hashes.
2. A TAMPERED contract is rejected, not trusted (fail closed).
3. Missing/unreadable contract files refuse boot (fail closed).
4. A manifest without the contract section refuses boot (fail closed).

Positive AND negative controls.
"""
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

import kernel.protocol.protocol_integrity_gate as gate  # noqa: E402


@pytest.fixture(scope="module")
def manifest():
    with open(os.path.join(REPO_ROOT, "kernel", "protocol",
                            "protocol_manifest.json")) as f:
        return json.load(f)


def test_contract_section_present(manifest):
    assert "naya_contract" in manifest
    pins = manifest["naya_contract"]["pinned_sha256"]
    assert len(pins) == 2
    assert "NAYA-ACTIVATION/NAYA-CONTRACT-V1.md" in pins


def test_contract_passes_honest(manifest):
    passed, detail = gate.check_naya_contract(manifest)
    assert passed, f"honest contract should pass: {detail}"
    assert "contract law" in detail


def test_contract_drift_fails_closed(manifest, monkeypatch, tmp_path):
    # Tamper one byte in a scratch copy; point the gate at it.
    for rel in manifest["naya_contract"]["pinned_sha256"]:
        src = os.path.join(REPO_ROOT, rel)
        dst = tmp_path / rel.replace("/", "_")
        shutil.copy(src, dst)
        with open(dst, "ab") as f:
            f.write(b" ")
        break
    real_root = gate.ROOT

    class FakeRoot:
        def __truediv__(self, rel):
            from pathlib import Path
            # Serve the tampered file for the first pinned path, real for rest
            first = next(iter(manifest["naya_contract"]["pinned_sha256"]))
            if rel == first:
                return tmp_path / rel.replace("/", "_")
            return real_root / rel

    monkeypatch.setattr(gate, "ROOT", FakeRoot())
    passed, detail = gate.check_naya_contract(manifest)
    assert not passed, "tampered contract must fail closed"
    assert "DRIFT" in detail


def test_contract_missing_file_fails_closed(manifest, monkeypatch):
    real_root = gate.ROOT

    class FakeRoot:
        def __truediv__(self, rel):
            from pathlib import Path
            return Path("/nonexistent") / rel

    monkeypatch.setattr(gate, "ROOT", FakeRoot())
    passed, detail = gate.check_naya_contract(manifest)
    assert not passed, "missing contract files must fail closed"
    assert "unreadable" in detail


def test_contract_missing_section_fails_closed(manifest):
    bare = {k: v for k, v in manifest.items() if k != "naya_contract"}
    passed, detail = gate.check_naya_contract(bare)
    assert not passed, "manifest without contract section must fail closed"


def test_contract_json_is_valid_machine_law():
    with open(os.path.join(REPO_ROOT, "NAYA-ACTIVATION",
                            "naya-contract.json")) as f:
        c = json.load(f)
    assert c["contract"] == "NAYA-CONTRACT-V1"
    assert c["status"] == "contract-law"
    assert len(c["behavior"]["do"]) == 8
    assert len(c["behavior"]["do_not"]) == 8
    assert c["process"]["loop"].startswith("attune")
    assert c["amendment"].startswith("Only by Shawn")

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
    assert len(pins) == 11
    assert "NAYA-ACTIVATION/NAYA-CONTRACT-V1.md" in pins


def test_identity_files_pinned(manifest):
    # Naya 3 (2026-10-13): the gate said PASS with oath/doctrine absent.
    # The contract declares them mandatory — so the manifest must pin them.
    pins = manifest["naya_contract"]["pinned_sha256"]
    for rel in manifest["naya_contract"]["identity_files"]:
        assert rel in pins, f"identity file not pinned: {rel}"
    assert "NAYA-ACTIVATION/OATH-OF-THE-NAYA-V1.md" in pins
    assert "CONSTITUTION/NAYA-DOCTRINE-V1.md" in pins
    assert "CONSTITUTION/naya-doctrine.json" in pins


def test_missing_oath_fails_closed(manifest, monkeypatch):
    # Naya 3's falsifier, now a permanent regression test: with the oath
    # absent from the fixture, the gate must FAIL — never PASS.
    real_root = gate.ROOT

    class FakeRoot:
        def __truediv__(self, rel):
            from pathlib import Path
            if "OATH-OF-THE-NAYA" in rel:
                return Path("/nonexistent") / rel
            return real_root / rel

    monkeypatch.setattr(gate, "ROOT", FakeRoot())
    passed, detail = gate.check_naya_contract(manifest)
    assert not passed, "gate must not PASS with the oath absent"
    assert "unreadable" in detail


def test_manifest_missing_identity_pin_fails_closed(manifest):
    # If the manifest ever drops an identity pin, the gate fails closed —
    # a tampered manifest cannot silently narrow the check.
    import copy
    narrowed = copy.deepcopy(manifest)
    pins = narrowed["naya_contract"]["pinned_sha256"]
    pins.pop("NAYA-ACTIVATION/OATH-OF-THE-NAYA-V1.md")
    passed, detail = gate.check_naya_contract(narrowed)
    assert not passed, "manifest missing an identity pin must fail closed"
    assert "missing identity pins" in detail


def test_crlf_checkout_passes(manifest, monkeypatch, tmp_path):
    # Naya 3 (2026-10-13, Windows desktop): CRLF checkouts falsely refused.
    # Equivalent platform line endings must PASS; the gate is not weakened.
    real_root = gate.ROOT
    crlf_dir = tmp_path / "crlf"
    crlf_dir.mkdir()
    for rel in manifest["naya_contract"]["pinned_sha256"]:
        src = real_root / rel
        body = src.read_bytes().replace(b"\n", b"\r\n")
        dst = crlf_dir / rel.replace("/", "_")
        dst.write_bytes(body)

    class FakeRoot:
        def __truediv__(self, rel):
            from pathlib import Path
            return crlf_dir / rel.replace("/", "_")

    monkeypatch.setattr(gate, "ROOT", FakeRoot())
    passed, detail = gate.check_naya_contract(manifest)
    assert passed, f"CRLF-equivalent checkout must pass: {detail}"


def test_crlf_with_tamper_still_fails(manifest, monkeypatch, tmp_path):
    # The CRLF tolerance must not become a tampering loophole: CRLF bytes
    # PLUS one changed byte must still fail closed.
    real_root = gate.ROOT
    crlf_dir = tmp_path / "crlf_tamper"
    crlf_dir.mkdir()
    for i, rel in enumerate(manifest["naya_contract"]["pinned_sha256"]):
        src = real_root / rel
        body = src.read_bytes().replace(b"\n", b"\r\n")
        if i == 0:
            body += b"tampered"
        dst = crlf_dir / rel.replace("/", "_")
        dst.write_bytes(body)

    class FakeRoot:
        def __truediv__(self, rel):
            from pathlib import Path
            return crlf_dir / rel.replace("/", "_")

    monkeypatch.setattr(gate, "ROOT", FakeRoot())
    passed, detail = gate.check_naya_contract(manifest)
    assert not passed, "CRLF + tampered content must fail closed"
    assert "DRIFT" in detail


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


def test_enforcer_live_passes():
    # The runtime enforcer must self-verify as part of boot — one system.
    passed, detail = gate.check_contract_enforcer_live()
    assert passed, f"enforcer should be live on the honest tree: {detail}"
    assert "one system" in detail


def test_enforcer_missing_fails_closed(monkeypatch, tmp_path):
    # No enforcer file = no boot. Fail closed, never silently skip.
    from pathlib import Path

    class FakeRoot:
        def __truediv__(self, rel):
            return Path("/nonexistent") / rel

    monkeypatch.setattr(gate, "ROOT", FakeRoot())
    passed, detail = gate.check_contract_enforcer_live()
    assert not passed, "missing enforcer must fail closed"
    assert "boot refused" in detail


def test_enforcer_integrity_failure_fails_closed(monkeypatch):
    # If the enforcer's own self-check fails, the gate must fail —
    # a broken enforcer is not a live enforcer.
    import subprocess as real_subprocess

    class BadResult:
        returncode = 1
        stdout = ""
        stderr = "VIOLATION: contract bytes changed"

    monkeypatch.setattr(gate.subprocess, "run", lambda *a, **k: BadResult())
    passed, detail = gate.check_contract_enforcer_live()
    assert not passed, "failed enforcer integrity must fail the gate"
    assert "boot refused" in detail

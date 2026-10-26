"""Adversarial proofs for NIA behavioral contract activation.

These tests check the *real* boot seam. A valid document alone is not an
agent behavior proof; the runtime action/scorecard/authority/proof checkers
remain separately required for any actual action.
"""
import hashlib
import json
import shutil
from pathlib import Path

from kernel.protocol import nia_protocol_gate


ROOT = Path(__file__).resolve().parents[1]


def _copy_contract(tmp_path):
    for name in (
        *nia_protocol_gate.CONTRACTS.keys(),
        nia_protocol_gate.CONSTITUTION,
        "PROTOCOL.md",
    ):
        src, dst = ROOT / name, tmp_path / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    return tmp_path


def test_current_machine_and_human_contract_are_pinned():
    ok, detail = nia_protocol_gate.check_contract(ROOT)
    assert ok, detail


def test_machine_contract_parseable_and_canonical_parent_exists():
    data = json.loads((ROOT / "GOVERNANCE/NIA-PROTOCOL-V1.json").read_text(
        encoding="utf-8"))
    assert data["amends_constitution"] is False
    assert (ROOT / nia_protocol_gate.CONSTITUTION).is_file()
    assert len(data["protocol_steps"]) == 10


def test_human_text_tamper_is_refused(tmp_path):
    root = _copy_contract(tmp_path)
    path = root / "GOVERNANCE/NIA-PROTOCOL-V1.md"
    path.write_bytes(path.read_bytes() + b"\nINVALID CHANGE")
    ok, detail = nia_protocol_gate.check_contract(root)
    assert not ok and "re-pin" in detail


def test_machine_text_tamper_is_refused(tmp_path):
    root = _copy_contract(tmp_path)
    path = root / "GOVERNANCE/NIA-PROTOCOL-V1.json"
    path.write_bytes(path.read_bytes().replace(b'"amends_constitution":false',
                                              b'"amends_constitution":true'))
    ok, detail = nia_protocol_gate.check_contract(root)
    assert not ok and "re-pin" in detail


def test_missing_constitution_is_refused(tmp_path):
    root = _copy_contract(tmp_path)
    (root / nia_protocol_gate.CONSTITUTION).unlink()
    ok, detail = nia_protocol_gate.check_contract(root)
    assert not ok and "parent" in detail


def test_repin_does_not_make_self_amendment_admissible(tmp_path, monkeypatch):
    root = _copy_contract(tmp_path)
    path = root / "GOVERNANCE/NIA-PROTOCOL-V1.json"
    content = path.read_bytes().replace(b'"amends_constitution":false',
                                        b'"amends_constitution":true')
    path.write_bytes(content)
    approved = dict(nia_protocol_gate.CONTRACTS)
    approved["GOVERNANCE/NIA-PROTOCOL-V1.json"] = hashlib.sha256(content).hexdigest()
    monkeypatch.setattr(nia_protocol_gate, "CONTRACTS", approved)
    ok, detail = nia_protocol_gate.check_contract(root)
    assert not ok and "self-amend" in detail


def test_real_boot_gate_includes_nia_integrity():
    from kernel.protocol import protocol_integrity_gate
    verdict = protocol_integrity_gate.run_gate("nia-test")
    nia = [c for c in verdict["checks"] if c["name"] == "nia_protocol_integrity"]
    assert len(nia) == 1 and nia[0]["pass"], nia

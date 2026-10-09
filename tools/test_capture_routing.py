"""Tests for the canonical capture entry point (A6 wiring).

Per SN-0435, a script nobody calls is not enforcement: Shawn's
"smart note this" must actually reach instant_activation.activate()
through the capture flow. These tests prove the routing in
smart_note_v2.capture():
  - shawn_direct-marked capture -> the instant path (real activation);
  - unmarked capture + verify bundle -> the standard project path;
  - unmarked capture with neither -> fail-closed refusal with guidance.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import smart_note_v2 as sn2


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _marked_capture():
    return {
        "title": "Test law: routing reaches the instant path",
        "lesson": "When Shawn says smart note this, the capture flow routes instantly.",
        "category": "governance",
        "topic": "verification",
        "subtopic": "routing",
        "source": {"captured_at": _now_iso(), "origin": "test"},
        "projection": {"human_director_authorized_publication": True},
        "verification": {
            "source": "shawn_direct",
            "verifier": "Shawn",
            "verifier_role": "human_director",
            "directive_quote": "smart note this: routing reaches the instant path",
            "directed_at": _now_iso(),
            "directive_ref": "chat:test-routing-001",
        },
    }


def _plain_capture():
    cap = _marked_capture()
    del cap["verification"]
    return cap


@pytest.fixture()
def env(tmp_path):
    return {
        "registry": str(tmp_path / "index.json"),
        "receipt_dir": str(tmp_path / "receipts"),
        "brain_root": str(tmp_path / "brain"),
        "private_root": str(tmp_path / "private"),
    }


def test_capture_routes_shawn_direct_to_instant(env, tmp_path):
    cap_path = tmp_path / "capture.json"
    cap_path.write_text(json.dumps(_marked_capture()), encoding="utf-8")
    out = sn2.capture(str(cap_path), registry_path=env["registry"],
                      receipt_dir=env["receipt_dir"],
                      brain_root=env["brain_root"],
                      private_root=env["private_root"])
    assert out["path"] == "instant"
    assert out["result"]["activated"] is True
    assert out["result"]["truth_state"] == "VERIFIED"
    assert out["result"]["verification_method"] == "shawn_direct_verification"


def test_capture_refuses_unmarked_without_verify_bundle(env, tmp_path):
    cap_path = tmp_path / "capture.json"
    cap_path.write_text(json.dumps(_plain_capture()), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        sn2.capture(str(cap_path), registry_path=env["registry"],
                    receipt_dir=env["receipt_dir"],
                    brain_root=env["brain_root"])
    assert "NOT_SHAWN_VERIFIED" in str(exc.value)
    # Fail-closed: nothing written anywhere.
    assert not Path(env["registry"]).exists()
    assert not Path(env["receipt_dir"]).exists()


def test_capture_routes_unmarked_with_verify_to_standard(tmp_path, monkeypatch):
    # The standard project path writes the canonical registry; routing is
    # what's under test, so project_capture is observed, not executed.
    calls = []

    def _fake_project(cap, ver, private_root=None, sn_id=None):
        calls.append({"cap": cap, "ver": ver})
        return {"projection_path": "/tmp/x", "entry": {"smart_note_id": "SN-1"}}

    monkeypatch.setattr(sn2, "project_capture", _fake_project)
    cap_path = tmp_path / "capture.json"
    cap_path.write_text(json.dumps(_plain_capture()), encoding="utf-8")
    ver_path = tmp_path / "verify.json"
    ver_path.write_text(json.dumps({"persisted": {"block": {}}}), encoding="utf-8")
    out = sn2.capture(str(cap_path), str(ver_path))
    assert out["path"] == "standard"
    assert len(calls) == 1
    assert calls[0]["ver"] == {"persisted": {"block": {}}}


def test_cli_capture_dispatches_to_instant(env, tmp_path, capsys):
    cap_path = tmp_path / "capture.json"
    cap_path.write_text(json.dumps(_marked_capture()), encoding="utf-8")
    rc = sn2.main(["capture", "--capture", str(cap_path),
                   "--registry", env["registry"],
                   "--receipt-dir", env["receipt_dir"],
                   "--brain-root", env["brain_root"],
                   "--private-root", env["private_root"]])
    assert rc in (0, None)
    out = json.loads(capsys.readouterr().out)
    assert out["captured"] is True and out["path"] == "instant"
    assert out["truth_state"] == "VERIFIED"


def test_cli_capture_refuses_unmarked(env, tmp_path, capsys):
    cap_path = tmp_path / "capture.json"
    cap_path.write_text(json.dumps(_plain_capture()), encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        sn2.main(["capture", "--capture", str(cap_path),
                  "--registry", env["registry"],
                  "--receipt-dir", env["receipt_dir"],
                  "--brain-root", env["brain_root"]])
    assert exc.value.code == 3
    out = json.loads(capsys.readouterr().out)
    assert out["captured"] is False
    assert "NOT_SHAWN_VERIFIED" in out["error"]

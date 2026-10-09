"""Tests for the instant-activation path (Shawn's Verification Law).

Shawn's Verification Law (2026-10-09): when Shawn says "smart note this,"
THAT IS THE VERIFICATION -- it activates instantly, no queue, no second
verification. These tests prove:
  1. a Shawn-verified capture activates end-to-end in one motion
     (receipt minted, smart link produced, truth_state VERIFIED);
  2. a NON-Shawn capture NEVER takes the instant path (fail-closed),
     including forged markers.
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import instant_activation as ia
import smart_note_v2 as sn2
from smart_link import validate_shape


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _shawn_capture(**overrides):
    cap = {
        "title": "Test law: instant activation is the verification",
        "lesson": "When Shawn says smart note this, his word is the verification.",
        "category": "governance",
        "topic": "verification",
        "subtopic": "instant-activation",
        "source": {"captured_at": _now_iso(), "origin": "test"},
        "projection": {"human_director_authorized_publication": True},
        "verification": {
            "source": "shawn_direct",
            "verifier": "Shawn",
            "verifier_role": "human_director",
            "directive_quote": "smart note this: instant activation is the verification",
            "directed_at": _now_iso(),
            "directive_ref": "test-directive-001",
        },
    }
    cap.update(overrides)
    return cap


@pytest.fixture()
def env(tmp_path):
    brain_root = tmp_path / "brain"
    return {
        "registry": str(tmp_path / "index.json"),
        "receipt_dir": str(tmp_path / "receipts"),
        "brain_root": str(brain_root),
        "private_root": str(tmp_path / "private"),
    }


def _activate(cap, env):
    return ia.activate(cap, registry_path=env["registry"],
                       receipt_dir=env["receipt_dir"],
                       brain_root=env["brain_root"],
                       private_root=env["private_root"])


# ------------------------------------------------------------------
# 1. The honest path: Shawn-verified activates end-to-end, one motion
# ------------------------------------------------------------------

def test_shawn_verified_activates_end_to_end(env):
    cap = _shawn_capture()
    result = _activate(cap, env)

    assert result["activated"] is True
    assert result["truth_state"] == "VERIFIED"
    assert result["verification_method"] == "shawn_direct_verification"
    assert result["sn_id"].startswith("SN-")

    # Receipt minted, on disk, hash-verified.
    rp = Path(result["receipt_path"])
    assert rp.exists()
    receipt = json.loads(rp.read_text(encoding="utf-8"))
    assert receipt["schema"] == ia.RECEIPT_SCHEMA
    assert receipt["receipt_hash"] == ia._hash_receipt(receipt)
    assert receipt["verification"]["directive_quote"].startswith("smart note this")

    # Registry entry: VERIFIED, stamped with the Shawn provenance.
    reg = json.loads(Path(env["registry"]).read_text(encoding="utf-8"))
    entries = [e for e in reg["entries"]
               if e["intelligent_block_id"] == result["intelligent_block_id"]]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["truth_state"] == "VERIFIED"
    assert entry["verification_method"] == "shawn_direct_verification"
    assert entry["verified_by"] == "Shawn (Human Director)"
    assert entry["activation_receipt_id"] == receipt["receipt_id"]

    # Smart link produced, canonical shape.
    assert validate_shape(result["smart_link"])
    assert result["smart_link"].startswith(
        "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/05-MEMORY/SMART-NOTES/")

    # Projection rendered.
    assert Path(result["projection_path"]).exists()


def test_user_direct_capture_request_takes_instant_path(env):
    # The law covers any user's direct capture request the same way:
    # the ask is the verification. The marker carries the user's words.
    cap = _shawn_capture()
    cap["verification"]["directive_quote"] = "bank this: never ship without the receipt"
    result = _activate(cap, env)
    assert result["activated"] is True
    assert result["truth_state"] == "VERIFIED"


def test_private_scope_activates_without_canonical_link(env):
    # PRIVATE-scope captures still activate instantly; they just don't get
    # a canonical link (a 404-for-strangers link is never fabricated).
    cap = _shawn_capture()
    del cap["projection"]
    result = _activate(cap, env)
    assert result["activated"] is True
    assert result["truth_state"] == "VERIFIED"
    assert result["smart_link"] is None
    assert result["receipt"]["smart_link_status"] == "PENDING_PRIVATE_PROJECTION"


def test_reactivation_is_idempotent_at_registry(env):
    cap = _shawn_capture()
    r1 = _activate(cap, env)
    r2 = _activate(cap, env)
    assert r1["sn_id"] == r2["sn_id"]
    assert r1["intelligent_block_id"] == r2["intelligent_block_id"]
    reg = json.loads(Path(env["registry"]).read_text(encoding="utf-8"))
    matches = [e for e in reg["entries"]
               if e["intelligent_block_id"] == r1["intelligent_block_id"]]
    assert len(matches) == 1
    assert matches[0]["truth_state"] == "VERIFIED"


def test_cli_activate_end_to_end(env, tmp_path):
    cap_path = tmp_path / "capture.json"
    cap_path.write_text(json.dumps(_shawn_capture()), encoding="utf-8")
    out_path = tmp_path / "out.json"
    rc = ia.main(["activate", "--capture", str(cap_path),
                  "--registry", env["registry"],
                  "--receipt-dir", env["receipt_dir"],
                  "--brain-root", env["brain_root"],
                  "--private-root", env["private_root"],
                  "--out", str(out_path)])
    assert rc == 0
    out = json.loads(out_path.read_text(encoding="utf-8"))
    assert out["activated"] is True
    assert out["truth_state"] == "VERIFIED"


# ------------------------------------------------------------------
# 2. Fail-closed: non-Shawn captures NEVER take the instant path
# ------------------------------------------------------------------

def _refused(cap, env, code="NOT_SHAWN_VERIFIED"):
    with pytest.raises(ia.InstantActivationRefused) as exc:
        _activate(cap, env)
    assert exc.value.code == code
    # Nothing partial may be left behind: no registry, no receipt, no projection.
    assert not Path(env["registry"]).exists()
    assert not any(Path(env["receipt_dir"]).glob("*.json")) if Path(env["receipt_dir"]).exists() else True
    return exc.value


def test_missing_marker_refused(env):
    cap = _shawn_capture()
    del cap["verification"]
    _refused(cap, env)


def test_system_captured_source_refused(env):
    cap = _shawn_capture()
    cap["verification"]["source"] = "system_captured"
    _refused(cap, env)


def test_agent_self_asserted_verifier_refused(env):
    # An agent claiming its own verification is not Shawn's.
    cap = _shawn_capture()
    cap["verification"]["verifier"] = "Naya 5"
    _refused(cap, env)


def test_empty_directive_quote_refused(env):
    cap = _shawn_capture()
    cap["verification"]["directive_quote"] = "   "
    _refused(cap, env)


def test_forged_marker_without_quote_refused(env):
    # The forgery shape: correct source string, but no directive evidence.
    cap = _shawn_capture()
    del cap["verification"]["directive_quote"]
    _refused(cap, env)


def test_future_directed_at_refused(env):
    cap = _shawn_capture()
    cap["verification"]["directed_at"] = (
        datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    _refused(cap, env)


def test_malformed_verification_block_refused(env):
    cap = _shawn_capture()
    cap["verification"] = "shawn_direct"  # not a dict: fail closed
    _refused(cap, env)


def test_cli_refuses_non_shawn_capture(env, tmp_path, capsys):
    cap = _shawn_capture()
    cap["verification"]["source"] = "agent_inferred"
    cap_path = tmp_path / "capture.json"
    cap_path.write_text(json.dumps(cap), encoding="utf-8")
    rc = ia.main(["activate", "--capture", str(cap_path),
                  "--registry", env["registry"],
                  "--receipt-dir", env["receipt_dir"],
                  "--brain-root", env["brain_root"]])
    assert rc == 3
    out = json.loads(capsys.readouterr().out)
    assert out["activated"] is False
    assert out["code"] == "NOT_SHAWN_VERIFIED"


# ------------------------------------------------------------------
# 3. Receipt integrity
# ------------------------------------------------------------------

def test_receipt_hash_detects_tampering(env):
    result = _activate(_shawn_capture(), env)
    receipt = result["receipt"]
    good = receipt["receipt_hash"]
    receipt["title"] = "TAMPERED TITLE"
    assert ia._hash_receipt(receipt) != good

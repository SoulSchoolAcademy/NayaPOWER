"""Demo-1 P1 RED: a real bounded executor behind ACT's seam.

Replaces the echo/test executor with an actual bounded operation whose
capability is declared in the canonical Smart Door registry — never in a
parallel registry.

Stated boundary (not smuggled): the ACT-verb decision receipt below is
built with the suite's make_decision_receipt helper carrying an explicit
authority_basis of kind director_order — the same receipt shape the LAW
runtime mints in production. Full LAW-side minting inside the Python
kernel is a named follow-up gap; what THIS file proves is the executor
seam: a real effect, externally observable, idempotent under replay,
with violations refused and receipted.

RED state: naya_kernel.smart_door does not exist, DOOR-LOCAL-STAGING is
not in the canonical registry, and no real executor exists — every test
here must FAIL until the GREEN implementation lands.
"""

import json
from pathlib import Path

import pytest

from naya_kernel import smart_door
from naya_kernel.nodes import act_node

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json"

DOOR_ID = "DOOR-LOCAL-STAGING"
OPERATION = "staging.write_file"
TOOL_ID = "staging.write_file"

NOW = "2026-10-01T04:00:00+00:00"
CONTENT = "# Demo-1 staging note\n\nA real bounded effect.\n"


def _receipt(filename, content):
    return act_node.make_decision_receipt(
        receipt_id="dec-demo1-staging-001",
        issued_at="2026-10-01T02:00:00+00:00",
        valid_until="2026-10-02T00:00:00+00:00",
        winner={"tool_id": TOOL_ID, "version": "1.0",
                "params": {"filename": filename, "content": content}},
        authority_basis={"kind": "director_order", "ref": "order-demo-1",
                         "revoked": False},
    )


def _registry():
    reg = smart_door.load_registry(REGISTRY_PATH)
    door, operation = smart_door.find_operation(reg, DOOR_ID, OPERATION)
    entry = smart_door.project_act_tool_entry(door, operation)
    return {TOOL_ID: entry}


def _act_state(receipt, tmp_path):
    return {
        "decision_receipt": receipt,
        "tool_registry": _registry(),
        "execution_ledger": {},
        "now": NOW,
        "_staging_root": str(tmp_path),
    }


# ---------------------------------------------------------------------------
# 1. The capability is declared in the canonical registry (not a parallel one)
# ---------------------------------------------------------------------------

def test_staging_write_declared_in_canonical_smart_door_registry():
    raw = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    assert raw["source_of_truth"] == \
        "BRAIN/10-INTERFACES/0001-SMART-DOOR-CONTRACT-V1.json"
    door = next(d for d in raw["doors"] if d["door_id"] == DOOR_ID)
    op = next(o for o in door["operations"] if o["operation"] == OPERATION)
    assert op["authority_action"] == "staging_write"
    assert op["verification_required"] is True
    assert op["mode"] == "WRITE"
    assert door["required_authority"] == "LAW decision per operation"
    # Honest status: registered for the demo path, NOT production-live.
    assert door["status"] == "REGISTERED_DEMO"


def test_projection_binds_registry_declaration_to_act_admission():
    reg = smart_door.load_registry(REGISTRY_PATH)
    door, operation = smart_door.find_operation(reg, DOOR_ID, OPERATION)
    entry = smart_door.project_act_tool_entry(door, operation)
    # Capability facts come from the registry, not invented in code.
    assert entry["authority_action"] == "staging_write"
    assert entry["target"] == "demo-staging/"
    assert entry["max_bytes"] == 65536
    assert entry["overwrite"] is False
    # ACT-side treatment (how ACT admits and invokes the tool).
    assert entry["authority_class"] == act_node.TOOL_CLASS_WRITE_SCOPED
    assert entry["required_authority"] == "director_order"
    assert entry["idempotent"] is True
    assert entry["evidence_capture"] == "return_value"


# ---------------------------------------------------------------------------
# 2. The executor performs a real, externally observable effect
# ---------------------------------------------------------------------------

def test_real_executor_writes_observable_file(tmp_path):
    import hashlib

    receipt = _receipt("sn-candidate-demo1.md", CONTENT)
    node = act_node.ActNode(
        executor=smart_door.make_staging_executor(str(tmp_path)))
    handoff = node.execute(_act_state(receipt, tmp_path))

    assert handoff["path"] == "EXECUTED", handoff
    target = tmp_path / "demo-staging" / "sn-candidate-demo1.md"
    assert target.is_file(), "the effect must be externally observable on disk"
    assert target.read_bytes() == CONTENT.encode("utf-8")
    digest = hashlib.sha256(CONTENT.encode("utf-8")).hexdigest()
    assert digest in str(handoff["receipt"].get("effects_observed", "")), \
        "the receipt must bind the observed artifact's content hash"


def test_replay_cannot_produce_a_second_effect(tmp_path):
    receipt = _receipt("sn-candidate-demo1.md", CONTENT)
    mk = lambda: act_node.ActNode(
        executor=smart_door.make_staging_executor(str(tmp_path)))
    first = mk().execute(_act_state(receipt, tmp_path))
    target = tmp_path / "demo-staging" / "sn-candidate-demo1.md"
    mtime_before = target.stat().st_mtime_ns

    # Same receipt replayed: ACT's idempotency key returns the existing
    # outcome — the executor must not run again.
    second = mk().execute(_act_state(receipt, tmp_path))
    assert second["execution_id"] == first["execution_id"]
    assert target.stat().st_mtime_ns == mtime_before

    # Same content under a fresh receipt: content-hash idempotency —
    # observable state is already exactly this; no second write occurs.
    receipt2 = _receipt("sn-candidate-demo1.md", CONTENT)
    receipt2["receipt_id"] = "dec-demo1-staging-002"
    receipt2["receipt_hash"] = act_node._sha256(
        {k: v for k, v in receipt2.items() if k != "receipt_hash"})
    third = mk().execute(_act_state(receipt2, tmp_path))
    assert third["path"] == "EXECUTED"
    assert target.stat().st_mtime_ns == mtime_before
    assert target.read_bytes() == CONTENT.encode("utf-8")


# ---------------------------------------------------------------------------
# 3. Violations are refused with receipts — no effect, no invention
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filename", [
    "../escape.md",
    "/abs/path.md",
    "sn-candidate-evil/../../x.md",
    "wrong-prefix.md",
    "sn-candidate-noext",
])
def test_escape_or_shape_violation_refused_without_effect(tmp_path, filename):
    receipt = _receipt(filename, CONTENT)
    node = act_node.ActNode(
        executor=smart_door.make_staging_executor(str(tmp_path)))
    handoff = node.execute(_act_state(receipt, tmp_path))

    assert handoff["path"] != "EXECUTED", handoff
    assert handoff.get("receipt") is not None, \
        "failure must be receipted, never silent"
    leftovers = list(tmp_path.rglob("*"))
    assert leftovers == [] or all(p.is_dir() for p in leftovers), \
        f"no file may be created on violation: {leftovers}"


def test_oversize_content_refused_without_effect(tmp_path):
    big = "x" * (65536 + 1)
    receipt = _receipt("sn-candidate-big.md", big)
    node = act_node.ActNode(
        executor=smart_door.make_staging_executor(str(tmp_path)))
    handoff = node.execute(_act_state(receipt, tmp_path))
    assert handoff["path"] != "EXECUTED"
    assert not (tmp_path / "demo-staging" / "sn-candidate-big.md").exists()


def test_conflicting_content_never_overwrites(tmp_path):
    node = act_node.ActNode(
        executor=smart_door.make_staging_executor(str(tmp_path)))
    ok = node.execute(_act_state(
        _receipt("sn-candidate-demo1.md", CONTENT), tmp_path))
    assert ok["path"] == "EXECUTED"

    rival = _receipt("sn-candidate-demo1.md", "rival content")
    rival["receipt_id"] = "dec-demo1-staging-rival"
    rival["receipt_hash"] = act_node._sha256(
        {k: v for k, v in rival.items() if k != "receipt_hash"})
    handoff = node.execute(_act_state(rival, tmp_path))
    assert handoff["path"] != "EXECUTED", \
        "no-overwrite: conflicting content must not replace the artifact"
    target = tmp_path / "demo-staging" / "sn-candidate-demo1.md"
    assert target.read_bytes() == CONTENT.encode("utf-8")


def test_unregistered_tool_never_reaches_any_executor(tmp_path):
    calls = []

    def spy(tool_id, params):
        calls.append(tool_id)
        return {"status": "ok", "effects": "should never happen",
                "error_class": None}

    receipt = _receipt("sn-candidate-demo1.md", CONTENT)
    receipt["winner"] = {"tool_id": "phantom_tool", "version": "9.9",
                         "params": {}}
    receipt["receipt_hash"] = act_node._sha256(
        {k: v for k, v in receipt.items() if k != "receipt_hash"})
    node = act_node.ActNode(executor=spy)
    handoff = node.execute(_act_state(receipt, tmp_path))
    assert handoff["path"] != "EXECUTED"
    assert calls == [], \
        "§4.3: unregistered tools refuse at admission — the executor is unreachable"

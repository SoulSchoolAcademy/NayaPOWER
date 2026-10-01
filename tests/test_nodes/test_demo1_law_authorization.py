"""Demo-1 LAW authorization boundary tests (move 2).

The executable path now authorizes via the REAL LawNode.gate() against a
director-transcribed grant. These tests prove the six refusal cases from
the directive: absent, expired, and revoked grants, plus wrong-action,
wrong-target, and broader-scope invocations, must all prevent executor
invocation. Each test reseals the receipt after mutation (like a real
tamperer would) so the refusal comes from the grant/envelope checks,
not from a broken seal.

The honest control proves a real envelope + valid grant is admitted.
"""

from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from naya_kernel import smart_door
from naya_kernel.node_base import GateVerdict
from naya_kernel.nodes import act_node
from scripts.demo1 import law_authorize

NOW = "2026-10-01T16:00:00+00:00"  # before the demo grant's expiry
FILENAME = "sn-candidate-law-test.md"
CONTENT = "law-boundary test content"


def _reseal(receipt):
    body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    receipt["receipt_hash"] = act_node._sha256(body)
    return receipt


@pytest.fixture()
def authz():
    """A real LAW authorization: proposal -> gate -> ADMISSIBLE envelope."""
    return law_authorize.authorize(FILENAME, CONTENT.encode("utf-8"))


@pytest.fixture()
def registry():
    return smart_door.staging_tool_registry()


def _receipt(authz, winner_override=None):
    winner = {"tool_id": "staging.write_file", "version": "1.0",
              "params": {"filename": FILENAME, "content": CONTENT}}
    if winner_override:
        winner.update(winner_override)
    return act_node.make_decision_receipt(
        receipt_id="dec-law-test-001",
        issued_at=NOW,
        valid_until=authz["grant"]["expiry"],
        winner=winner,
        authority_basis=dict(authz["authority_basis"]),
        law_envelope=copy.deepcopy(authz["envelope"]),
    )


def _admit(receipt, registry, grants):
    node = act_node.ActNode()
    return node._admit(receipt, registry, NOW, grants=grants)


def test_honest_law_path_admitted(authz, registry):
    """Control: real envelope + valid grant passes admission."""
    verdict, reasons = _admit(_receipt(authz), registry, [authz["grant"]])
    assert verdict == GateVerdict.PASS, reasons
    assert any("ENVELOPE-BOUND" in r for r in reasons)


def test_absent_grant_refused(authz, registry):
    """A basis ref that resolves to no grant is refused (forgery pattern)."""
    receipt = _receipt(authz)
    receipt["authority_basis"] = {"kind": "director_order",
                                  "ref": "grant-that-does-not-exist",
                                  "revoked": False}
    _reseal(receipt)
    verdict, reasons = _admit(receipt, registry, [authz["grant"]])
    assert verdict == GateVerdict.FAIL
    assert any("absent grant" in r for r in reasons)


def test_expired_grant_refused(authz, registry):
    """A grant past its expiry is refused — the real clock gates the executor."""
    grant = copy.deepcopy(authz["grant"])
    grant["expiry"] = "2026-09-01T00:00:00+00:00"  # before NOW
    verdict, reasons = _admit(_receipt(authz), registry, [grant])
    assert verdict == GateVerdict.FAIL
    assert any("expired" in r for r in reasons)


def test_revoked_grant_refused(authz, registry):
    """A revoked grant is refused even though LAW admitted it earlier."""
    grant = copy.deepcopy(authz["grant"])
    grant["revoked"] = True
    verdict, reasons = _admit(_receipt(authz), registry, [grant])
    assert verdict == GateVerdict.FAIL
    assert any("revoked" in r for r in reasons)


def test_wrong_action_refused(authz, registry):
    """A receipt retargeted to a different registered tool is refused."""
    other = copy.deepcopy(registry["staging.write_file"])
    registry = dict(registry)
    registry["other.tool"] = dict(other, tool_id="other.tool")
    receipt = _receipt(authz, winner_override={"tool_id": "other.tool"})
    _reseal(receipt)
    verdict, reasons = _admit(receipt, registry, [authz["grant"]])
    assert verdict == GateVerdict.FAIL
    assert any("wrong action" in r for r in reasons)


def test_wrong_target_refused(authz, registry):
    """A tool entry pointed at a target outside the envelope is refused."""
    moved = copy.deepcopy(registry["staging.write_file"])
    moved["target"] = "elsewhere/"
    registry = {"staging.write_file": moved}
    verdict, reasons = _admit(_receipt(authz), registry, [authz["grant"]])
    assert verdict == GateVerdict.FAIL
    assert any("wrong target" in r for r in reasons)


def test_broader_scope_filename_refused(authz, registry):
    """A filename outside the envelope pattern is refused."""
    receipt = _receipt(
        authz, winner_override={"params": {"filename": "evil.txt",
                                           "content": CONTENT}})
    _reseal(receipt)
    verdict, reasons = _admit(receipt, registry, [authz["grant"]])
    assert verdict == GateVerdict.FAIL
    assert any("broader scope" in r for r in reasons)


def test_broader_scope_size_refused(authz, registry):
    """Content exceeding the envelope max_bytes is refused."""
    big = "x" * 70000  # grant allows 65536
    receipt = _receipt(
        authz, winner_override={"params": {"filename": FILENAME,
                                           "content": big}})
    _reseal(receipt)
    verdict, reasons = _admit(receipt, registry, [authz["grant"]])
    assert verdict == GateVerdict.FAIL
    assert any("broader scope" in r for r in reasons)


def test_full_execute_with_real_law_authorization(tmp_path, authz, registry):
    """End to end: LAW gate -> admission -> real executor -> artifact."""
    receipt = _receipt(authz)
    node = act_node.ActNode(
        executor=smart_door.make_staging_executor(str(tmp_path)))
    handoff = node.execute({
        "decision_receipt": receipt,
        "tool_registry": registry,
        "grants": [authz["grant"]],
        "execution_ledger": {},
        "now": NOW,
    })
    assert handoff["path"] == "EXECUTED", handoff["receipt"]
    artifact = tmp_path / "demo-staging" / FILENAME
    assert artifact.is_file()
    assert json.loads(json.dumps(handoff["receipt"]))["execution_id"]

"""Demo-1 P2 RED: ACT→KNOW handoff for a real staging execution receipt.

The staging ACT execution receipt is verified (seal recompute + artifact
re-hash against the receipt's bound SHA-256) BEFORE KNOW ever sees it. The
verified observation becomes a KNOW ingestion candidate through the kernel's
KNOW gate during decide(); the resulting kernel decision receipt satisfies
the persistence seam's input contract (Naya 2's project_kernel_receipt,
PR #1243) — exercised read-only, no production write.

Stated boundaries (not smuggled):
- The KNOW store is in-memory (test/runtime-local), never the production
  ledger. The seam projection is project-only; no database call is made.
- The owner_id used for the projection check is a format-valid test uuid,
  NOT a real auth.users identity — the real demo identity binding is a
  named open question for Shawn (Naya 2 cannot mint it; neither can I).
- The ACT-verb decision receipt authorizing the staging execution still
  carries the suite's director_order test attestation (P1 boundary); full
  LAW-side minting inside the Python kernel remains a named gap.

RED state: naya_kernel.act_know_handoff does not exist — every test here
must FAIL until the GREEN implementation lands.
"""

import copy
import hashlib
import json
from pathlib import Path

import pytest

from naya_kernel import act_know_handoff as handoff  # noqa: F401 — RED
from naya_kernel import smart_door
from naya_kernel.kernel import Kernel, verify_decision_receipt
from naya_kernel.nodes import act_node

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json"

TOOL_ID = "staging.write_file"
CONTENT = "# Demo-1 handoff note\n\nACT→KNOW.\n"
FILENAME = "sn-candidate-handoff.md"

PRINCIPAL = {"identity": "naya-demo", "entitled_scopes": ["public", "team"]}


def _auth_receipt(filename, content):
    return act_node.make_decision_receipt(
        receipt_id="dec-demo1-handoff-001",
        issued_at="2026-10-01T02:00:00+00:00",
        valid_until="2026-10-02T00:00:00+00:00",
        winner={"tool_id": TOOL_ID, "version": "1.0",
                "params": {"filename": filename, "content": content}},
        authority_basis={"kind": "director_order", "ref": "order-demo-1",
                         "revoked": False},
    )


def _registry():
    reg = smart_door.load_registry(REGISTRY_PATH)
    door, operation = smart_door.find_operation(
        reg, "DOOR-LOCAL-STAGING", "staging.write_file")
    return {TOOL_ID: smart_door.project_act_tool_entry(door, operation)}


def _execute(filename=FILENAME, content=CONTENT, tmp_path=None):
    """A real ACT staging execution; returns the execution receipt."""
    node = act_node.ActNode(
        executor=smart_door.make_staging_executor(str(tmp_path)))
    out = node.execute({
        "decision_receipt": _auth_receipt(filename, content),
        "tool_registry": _registry(),
        "execution_ledger": {},
        "now": "2026-10-01T04:00:00+00:00",
        "_staging_root": str(tmp_path),
    })
    assert out["path"] == "EXECUTED", out
    return out["receipt"]


def _gate_states():
    """Full decide() gate states (P3 fixture pattern); KNOW is replaced by
    the handoff module per test."""
    import sys
    sys.path.insert(0, str(REPO_ROOT / "tests"))
    import test_nodes.test_kernel_nine_node as T
    k = Kernel()
    return k, {
        "SELF": T.self_state(), "LAW": T.law_state(), "ACT": T.act_state(),
        "PROVE": T.prove_state(k), "CONNECT": T.connect_state(),
        "VERIFY": T.verify_state(k), "LEARN": T.learn_state(k),
        "EVOLVE": {"action": "metrics"},
    }


# ---------------------------------------------------------------------------
# 1. A tampered ACT receipt never reaches KNOW
# ---------------------------------------------------------------------------

def test_tampered_act_receipt_refuses_before_know(tmp_path):
    receipt = _execute(tmp_path=tmp_path)
    bad = copy.deepcopy(receipt)
    # Any post-issuance modification breaks the ACT seal.
    bad["effects_observed"] = bad["effects_observed"] + " (tampered)"

    kernel, gates = _gate_states()
    with pytest.raises(handoff.HandoffRefused) as exc:
        handoff.handoff_act_to_know(
            kernel, bad, staging_root=str(tmp_path),
            principal=PRINCIPAL, gate_states=gates,
            decision_id="demo1-act-know-tampered")
    assert "seal" in str(exc.value).lower() or "mismatch" in str(exc.value).lower()
    assert kernel.nodes["KNOW"].blocks == {}, \
        "KNOW must hold nothing from a refused handoff"
    assert kernel.nodes["KNOW"].ingestion_log == []


# ---------------------------------------------------------------------------
# 2. A missing artifact refuses (observation must be re-observable)
# ---------------------------------------------------------------------------

def test_missing_artifact_refuses(tmp_path):
    receipt = _execute(tmp_path=tmp_path)
    target = tmp_path / "demo-staging" / FILENAME
    assert target.is_file()
    target.unlink()

    kernel, gates = _gate_states()
    with pytest.raises(handoff.HandoffRefused):
        handoff.handoff_act_to_know(
            kernel, receipt, staging_root=str(tmp_path),
            principal=PRINCIPAL, gate_states=gates,
            decision_id="demo1-act-know-missing")


# ---------------------------------------------------------------------------
# 3. Changed artifact content refuses (hash binding is enforced)
# ---------------------------------------------------------------------------

def test_artifact_content_changed_refuses(tmp_path):
    receipt = _execute(tmp_path=tmp_path)
    target = tmp_path / "demo-staging" / FILENAME
    with target.open("ab") as fh:
        fh.write(b"\nTampered after execution.\n")

    kernel, gates = _gate_states()
    with pytest.raises(handoff.HandoffRefused) as exc:
        handoff.handoff_act_to_know(
            kernel, receipt, staging_root=str(tmp_path),
            principal=PRINCIPAL, gate_states=gates,
            decision_id="demo1-act-know-changed")
    assert "sha" in str(exc.value).lower()


# ---------------------------------------------------------------------------
# 4. The valid handoff: verified → KNOW ingests → decision binds → retrievable
# ---------------------------------------------------------------------------

def test_valid_handoff_ingests_and_retrieves(tmp_path):
    receipt = _execute(tmp_path=tmp_path)
    kernel, gates = _gate_states()
    result = handoff.handoff_act_to_know(
        kernel, receipt, staging_root=str(tmp_path),
        principal=PRINCIPAL, gate_states=gates,
        decision_id="demo1-act-know-001")

    assert result["know_verdict"] == "PASS", result["know_gate_reasons"]
    know = kernel.nodes["KNOW"]
    assert result["block_id"] in know.blocks, "KNOW must persist the observation"

    # KNOW serves the observation back through its own retrieval gates.
    served = know.retrieve(
        {"text": "staging.write_file executed",
         "requested_scopes": ["public"],
         "identity_binding": {"verified": True}},
        PRINCIPAL)
    assert served["admitted"] is True
    assert any(b["id"] == result["block_id"] for b in served["blocks"]), \
        "the handed-off observation must be retrievable"


# ---------------------------------------------------------------------------
# 5. Backstop: KNOW's own gate refuses an unprovenanced claim even when the
#    handoff module is bypassed
# ---------------------------------------------------------------------------

def test_unprovenanced_claim_refused_by_know_gate():
    know_node = Kernel().nodes["KNOW"]
    receipt = know_node.ingest(
        {"content": "ACT did something, trust me.",
         "proposed_class": "EPHEMERAL",
         "class_signals": [{"signal": "s", "value": 1.0}],
         "classifier": "auto",
         "identity_binding": {"verified": True},
         "owner_scope": "public"},
        PRINCIPAL)
    assert receipt["operation"] == "REFUSE", \
        "KNOW must refuse provenance-free claims at its own gate"
    assert know_node.blocks == {}


# ---------------------------------------------------------------------------
# 6. The decision receipt satisfies the persistence seam's input contract
#    (Naya 2's project_kernel_receipt validation rules, PR #1243 — asserted
#    here without vendoring her in-flight module)
# ---------------------------------------------------------------------------

SEAM_REQUIRED_FIELDS = ("receipt_hash", "receipt_id", "decision_id",
                        "issued_at", "kernel_version", "verdict")


def test_decision_receipt_satisfies_seam_input_contract(tmp_path):
    receipt = _execute(tmp_path=tmp_path)
    kernel, gates = _gate_states()
    result = handoff.handoff_act_to_know(
        kernel, receipt, staging_root=str(tmp_path),
        principal=PRINCIPAL, gate_states=gates,
        decision_id="demo1-act-know-002")
    decision_receipt = result["decision_receipt"]
    input_state = result["input_state"]

    for field in SEAM_REQUIRED_FIELDS:
        assert decision_receipt.get(field), \
            f"seam requires non-empty {field}; the handoff decision must mint it"

    # The seam recomputes receipt_hash over the canonical body.
    assert verify_decision_receipt(decision_receipt)["result"] == "MATCH"

    # The seam recomputes inputs_hash over the submitted input state and
    # rejects mismatch: prove the submitted state reproduces it exactly.
    canon = json.dumps(input_state, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True).encode("utf-8")
    assert hashlib.sha256(canon).hexdigest() == decision_receipt["inputs_hash"]

    # The handoff is bound into the decision through inputs_hash: the decided
    # input state carries the full KNOW candidate (with its ACTION_OUTCOME
    # provenance ref), and the seam's p_value (the full native receipt)
    # carries the receipt that binds that same hash. The block id itself
    # lives in KNOW's store, located by provenance ref — never invented.
    provenance_ref = "act-execution:%s" % result["observation"]["execution_id"]
    assert provenance_ref in json.dumps(input_state)
    assert hashlib.sha256(canon).hexdigest() == decision_receipt["inputs_hash"]

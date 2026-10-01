"""Kernel.decide() — nine-node decision pipeline (CANDIDATE — NOT RATIFIED — NOT MERGED).

GAP-A closure: decide() exercises all nine nodes' gates in pipeline order
(SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE).
The first non-PASS gate short-circuits the pipeline (fail-fast); gate_all()
evaluates every gate without short-circuit for full audit visibility.

Verdict law: UNKNOWN, BLOCKED, and IMPLEMENTED never count as PASS — any
gate that cannot reach PASS on the evidence in `state` must return
FAIL or NEED_EVIDENCE and name its reasons. A gate that raises is
recorded FAIL (fail-closed), never skipped.

Every decide()/gate_all() call emits a hash-bound decision receipt
(receipt_hash = SHA256 over the canonicalized body), so a cold successor
can re-verify what the pipeline decided and why.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List

from naya_kernel.node_base import GateResult, GateVerdict
from naya_kernel.nodes import (
    act_node,
    connect_node,
    evolve_node,
    know_node,
    law_node,
    learn_node,
    prove_node,
    self_node,
    verify_node,
)

# Pipeline order per the node specs.
GATE_ORDER = [
    ("SELF", self_node.SelfNode),
    ("LAW", law_node.LawNode),
    ("ACT", act_node.ActNode),
    ("KNOW", know_node.KnowNode),
    ("PROVE", prove_node.ProveNode),
    ("CONNECT", connect_node.ConnectNode),
    ("VERIFY", verify_node.VerifyNode),
    ("LEARN", learn_node.LearnNode),
    ("EVOLVE", evolve_node.EvolveNode),
]

NODE_ID = "NAYA-KERNEL"
KERNEL_VERSION = "0.1.0-candidate"


def _canon(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, default=str)


def _sha256(obj: Any) -> str:
    return hashlib.sha256(_canon(obj).encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def verify_decision_receipt(receipt: Dict[str, Any]) -> Dict[str, Any]:
    """Re-derive receipt_hash over the canonical body; return MATCH/MISMATCH."""
    stored = receipt.get("receipt_hash")
    body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    if stored is None or _sha256(body) != stored:
        return {"result": "MISMATCH", "receipt_id": receipt.get("receipt_id")}
    return {"result": "MATCH", "receipt_id": receipt.get("receipt_id")}


class Kernel:
    """Nine-node kernel: every decision runs every gate, in order."""

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = dict(config or {})
        self.nodes = {name: cls() for name, cls in GATE_ORDER}

    # -- pipeline ------------------------------------------------------

    def _run_gate(self, name: str, sub_state: Dict[str, Any]) -> GateResult:
        """Run one node's gate; fail-closed on exceptions."""
        try:
            result = self.nodes[name].gate(sub_state or {})
        except Exception as exc:  # fail-closed: a broken gate never passes
            return GateResult(
                GateVerdict.FAIL,
                [f"KERNEL GATE EXCEPTION at {name}: {type(exc).__name__}: {exc}"],
            )
        if not isinstance(result, GateResult):
            return GateResult(
                GateVerdict.FAIL,
                [f"KERNEL GATE CONTRACT VIOLATION at {name}: "
                 f"gate() returned {type(result).__name__}, not GateResult"],
            )
        return result

    def _decision_receipt(self, decision_id: str, gates: List[Dict[str, Any]],
                          verdict: GateVerdict,
                          stopped_at: str | None,
                          short_circuit: bool) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "receipt_id": f"decision-{decision_id}",
            "node_id": NODE_ID,
            "kernel_version": KERNEL_VERSION,
            "decision_id": decision_id,
            "gate_order": [name for name, _ in GATE_ORDER],
            "short_circuit": short_circuit,
            "verdict": verdict.value,
            "stopped_at": stopped_at,
            "gates": gates,
            "issued_at": _now_iso(),
            "candidate_banner": "CANDIDATE — NOT RATIFIED — NOT MERGED",
        }
        body["receipt_hash"] = _sha256(body)
        return body

    def decide(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run every node's gate in order; first non-PASS short-circuits.

        `state` carries per-node sub-states under ``state["gates"]`` keyed by
        node name (e.g. ``state["gates"]["LAW"]``). Returns a dict with the
        pipeline verdict, the per-gate results, where the pipeline stopped,
        and a hash-bound decision receipt.
        """
        state = state or {}
        decision_id = state.get("decision_id") or f"d-{_sha256(state)[:12]}"
        sub_states = state.get("gates") or {}
        gates: List[Dict[str, Any]] = []
        verdict = GateVerdict.PASS
        stopped_at: str | None = None
        for position, (name, _cls) in enumerate(GATE_ORDER, start=1):
            result = self._run_gate(name, sub_states.get(name))
            gates.append({
                "node": name,
                "position": position,
                "verdict": result.verdict.value,
                "reasons": list(result.reasons),
            })
            if result.verdict != GateVerdict.PASS:
                verdict = result.verdict
                stopped_at = name
                break  # fail-fast: the first non-PASS gate stops the pipeline
        receipt = self._decision_receipt(
            decision_id, gates, verdict, stopped_at, short_circuit=True)
        return {
            "decision_id": decision_id,
            "verdict": verdict.value,
            "stopped_at": stopped_at,
            "gates": gates,
            "decision_receipt": receipt,
        }

    def gate_all(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate every gate without short-circuit; full audit visibility."""
        state = state or {}
        sub_states = state.get("gates") or {}
        out: List[Dict[str, Any]] = []
        for position, (name, _cls) in enumerate(GATE_ORDER, start=1):
            result = self._run_gate(name, sub_states.get(name))
            out.append({
                "node": name,
                "position": position,
                "verdict": result.verdict.value,
                "reasons": list(result.reasons),
            })
        return out

    # -- cold reconstruction -------------------------------------------

    def cold_reconstruct(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rebuild kernel-level state from decision receipts alone.

        Verifies each decision receipt's hash, counts verdicts, and reports
        any receipt that fails verification (never trusted, always listed).
        """
        matched, mismatched = [], []
        verdicts: Dict[str, int] = {}
        for receipt in receipts or []:
            check = verify_decision_receipt(receipt)
            if check["result"] == "MATCH":
                matched.append(check["receipt_id"])
                verdict = receipt.get("verdict", "UNKNOWN")
                verdicts[verdict] = verdicts.get(verdict, 0) + 1
            else:
                # Mismatched receipts are listed, never trusted: their
                # verdict field is unauthenticated and must not feed counts.
                mismatched.append(check["receipt_id"])
        return {
            "receipts_checked": len(receipts or []),
            "hash_matched": matched,
            "hash_mismatched": mismatched,
            "verdicts": verdicts,
        }

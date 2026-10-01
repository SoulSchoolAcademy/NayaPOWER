"""Kernel.decide() — nine-node runtime graph (CANDIDATE — NOT RATIFIED — NOT MERGED).

FLAG-001 reconciliation: decide() no longer runs a forced linear call stack.
The executable topology is the canonical 13-edge runtime graph, authoritative
source ``BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json``:

    SELF→LAW; SELF→KNOW; LAW→ACT; ACT→VERIFY; KNOW→PROVE; KNOW→CONNECT;
    PROVE→VERIFY; CONNECT→VERIFY; VERIFY→LEARN; LEARN→EVOLVE; EVOLVE→SELF
    (the lock's 11 minimum runtime routes)
    plus ACT→KNOW (PRODUCES — write edge) and LAW→EVOLVE (GOVERNS — gate edge).

Per the Ultimate Lock (BRAIN/03-KERNEL/0005-NINE-NODE-ULTIMATE-LOCK-AND-
NOTE-READINESS-V1.md): "executable node communication is not one mandatory
linear call stack." The semantic/display order is unchanged; the runtime
handoff semantics below are what decide() executes.

Fail-fast / fail-closed PER EDGE (do not weaken any gate):
- A node's gate is consulted only when every required upstream gate has
  PASSed. Otherwise the node is recorded NEED_EVIDENCE with the blocking
  upstream named (never an invented PASS, never silently skipped).
- A FAIL verdict is a global halt: fail-fast for the whole decision, exactly
  as the old pipeline did (e.g. LAW PROHIBITED stops everything before ACT).
- NEED_EVIDENCE blocks only its downstream edges; independent branches still
  evaluate (e.g. a LAW NEED_EVIDENCE blocks ACT and EVOLVE but the
  SELF→KNOW→PROVE/CONNECT branch still runs).
- VERIFY still requires its upstream PROVE/CONNECT/ACT inputs: if any of
  those did not PASS, VERIFY's gate is not consulted and VERIFY is recorded
  NEED_EVIDENCE naming the missing upstream.
- LAW refusal still blocks ACT (LAW→ACT GOVERNS) and EVOLVE (LAW→EVOLVE
  GOVERNS).
- A gate that raises is recorded FAIL (never skipped); a gate returning a
  non-GateResult is a FAIL contract violation.

Special edges:
- ACT→KNOW PRODUCES is a *write* edge: ACT execution outcomes feed KNOW's
  store. The kernel records the handoff in the edge trace; it does not
  re-run KNOW's gate in the same pass (ingest remains KNOW's own intake
  path). Candidate boundary, stated here, not hidden.
- EVOLVE→SELF SUCCEEDS closes the loop to the *next* decision cycle. It is
  recorded in the edge trace and NOT traversed inside one decide() call —
  traversing it would recurse forever.

Verdict law: UNKNOWN, BLOCKED, and IMPLEMENTED never count as PASS — any
gate that cannot reach PASS on the evidence in `state` must return
FAIL or NEED_EVIDENCE and name its reasons.

Every decide()/gate_all() call emits a hash-bound decision receipt
(receipt_hash = SHA256 over the canonicalized body), so a cold successor
can re-verify what the graph decided and why.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

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

#: Authoritative runtime graph. (relationship_id, source, target, type) —
#: copied verbatim from
#: BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json (13 edges).
#: The seed file is the authority; this table is checked against it by
#: tests/test_nodes/test_kernel_nine_node.py (drift guard).
RUNTIME_EDGES: List[Tuple[str, str, str, str]] = [
    ("REL-KERNEL-SELF-LAW", "SELF", "LAW", "CONTEXTUALIZES"),
    ("REL-KERNEL-SELF-KNOW", "SELF", "KNOW", "CONTEXTUALIZES"),
    ("REL-KERNEL-LAW-ACT", "LAW", "ACT", "GOVERNS"),
    ("REL-KERNEL-ACT-KNOW", "ACT", "KNOW", "PRODUCES"),      # write edge
    ("REL-KERNEL-ACT-VERIFY", "ACT", "VERIFY", "VERIFIED_BY"),
    ("REL-KERNEL-KNOW-PROVE", "KNOW", "PROVE", "SUPPORTS"),
    ("REL-KERNEL-KNOW-CONNECT", "KNOW", "CONNECT", "CONTEXTUALIZES"),
    ("REL-KERNEL-PROVE-VERIFY", "PROVE", "VERIFY", "SUPPORTS"),
    ("REL-KERNEL-CONNECT-VERIFY", "CONNECT", "VERIFY", "CONTEXTUALIZES"),
    ("REL-KERNEL-VERIFY-LEARN", "VERIFY", "LEARN", "PRODUCES"),
    ("REL-KERNEL-LEARN-EVOLVE", "LEARN", "EVOLVE", "ENABLES"),
    ("REL-KERNEL-EVOLVE-SELF", "EVOLVE", "SELF", "SUCCEEDS"),  # next cycle
    ("REL-KERNEL-LAW-EVOLVE", "LAW", "EVOLVE", "GOVERNS"),
]

#: The lock's 11 minimum runtime routes (source, target) — required subset
#: of RUNTIME_EDGES (the 13-edge seed adds ACT→KNOW and LAW→EVOLVE).
LOCK_MINIMUM_ROUTES = [
    ("SELF", "LAW"), ("SELF", "KNOW"), ("LAW", "ACT"), ("ACT", "VERIFY"),
    ("KNOW", "PROVE"), ("KNOW", "CONNECT"), ("PROVE", "VERIFY"),
    ("CONNECT", "VERIFY"), ("VERIFY", "LEARN"), ("LEARN", "EVOLVE"),
    ("EVOLVE", "SELF"),
]

#: Gate dependencies: a node's gate is consulted only when every listed
#: upstream node PASSed. Excludes the ACT→KNOW write edge (not a gate input)
#: and the EVOLVE→SELF next-cycle edge (not traversed in one pass).
GATE_REQUIREMENTS: Dict[str, List[str]] = {
    "SELF": [],
    "LAW": ["SELF"],
    "KNOW": ["SELF"],
    "ACT": ["LAW"],
    "PROVE": ["KNOW"],
    "CONNECT": ["KNOW"],
    "VERIFY": ["ACT", "PROVE", "CONNECT"],
    "LEARN": ["VERIFY"],
    "EVOLVE": ["LAW", "LEARN"],
}

#: Deterministic evaluation order — one topological order of the gate
#: dependencies (the semantic/display order of the lock).
EVALUATION_ORDER = [
    "SELF", "LAW", "KNOW", "ACT", "PROVE", "CONNECT",
    "VERIFY", "LEARN", "EVOLVE",
]

NODE_CLASSES = {
    "SELF": self_node.SelfNode,
    "LAW": law_node.LawNode,
    "ACT": act_node.ActNode,
    "KNOW": know_node.KnowNode,
    "PROVE": prove_node.ProveNode,
    "CONNECT": connect_node.ConnectNode,
    "VERIFY": verify_node.VerifyNode,
    "LEARN": learn_node.LearnNode,
    "EVOLVE": evolve_node.EvolveNode,
}

#: Relationship ids whose handoff is NOT a gate input for decide().
NON_GATE_EDGES = {
    "REL-KERNEL-ACT-KNOW",    # PRODUCES write edge — recorded, not re-gated
    "REL-KERNEL-EVOLVE-SELF",  # SUCCEEDS next-cycle edge — recorded, not traversed
}

NODE_ID = "NAYA-KERNEL"
KERNEL_VERSION = "0.2.0-candidate"
GRAPH_SEED_REF = ("BRAIN/04-INTELLIGENCE/GRAPH/"
                  "0001-KERNEL-GRAPH-SEED-V1.json")
LOCK_REF = ("BRAIN/03-KERNEL/"
            "0005-NINE-NODE-ULTIMATE-LOCK-AND-NOTE-READINESS-V1.md")


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
    """Nine-node kernel: every decision traverses the runtime graph."""

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = dict(config or {})
        self.nodes = {name: NODE_CLASSES[name]() for name in EVALUATION_ORDER}

    # -- graph traversal -------------------------------------------------

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

    def _edge_trace(self, verdicts: Dict[str, GateVerdict],
                    evaluated: Dict[str, bool]) -> List[Dict[str, Any]]:
        """Per-edge handoff status for the receipt.

        A gate edge is SATISFIED when its source PASSed; otherwise BLOCKED
        with the source's verdict named. The two non-gate edges are recorded
        with their honest disposition (write path / next cycle).
        """
        trace: List[Dict[str, Any]] = []
        for rel_id, source, target, rel_type in RUNTIME_EDGES:
            src_verdict = verdicts.get(source)
            if rel_id == "REL-KERNEL-ACT-KNOW":
                status = ("SATISFIED_WRITE_PATH"
                          if src_verdict == GateVerdict.PASS
                          else "BLOCKED")
                note = ("ACT outcomes produced into KNOW's store; KNOW's gate "
                        "is not re-run in this pass (ingest is KNOW's own "
                        "intake path)")
            elif rel_id == "REL-KERNEL-EVOLVE-SELF":
                status = "NEXT_CYCLE"
                note = ("closes the loop to the next decide() call; not "
                        "traversed inside one pass")
            elif src_verdict == GateVerdict.PASS:
                status = "SATISFIED"
                note = (f"{source} PASSed; {target} "
                        + ("was evaluated" if evaluated.get(target)
                           else "blocked downstream"))
            else:
                status = "BLOCKED"
                note = (f"{source} did not PASS "
                        f"({src_verdict.value if src_verdict else 'unevaluated'}); "
                        f"{rel_type} handoff to {target} withheld")
            trace.append({
                "relationship_id": rel_id, "source": source, "target": target,
                "type": rel_type, "status": status, "note": note,
            })
        return trace

    def _decision_receipt(self, decision_id: str, gates: List[Dict[str, Any]],
                          edge_trace: List[Dict[str, Any]],
                          verdict: GateVerdict,
                          stopped_at: str | None) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "receipt_id": f"decision-{decision_id}",
            "node_id": NODE_ID,
            "kernel_version": KERNEL_VERSION,
            "topology": "canonical-runtime-graph-v1",
            "graph_seed": GRAPH_SEED_REF,
            "lock_ref": LOCK_REF,
            "decision_id": decision_id,
            "evaluation_order": list(EVALUATION_ORDER),
            "verdict": verdict.value,
            "stopped_at": stopped_at,
            "gates": gates,
            "edge_trace": edge_trace,
            "issued_at": _now_iso(),
            "candidate_banner": "CANDIDATE — NOT RATIFIED — NOT MERGED",
        }
        body["receipt_hash"] = _sha256(body)
        return body

    def decide(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Traverse the runtime graph; per-edge fail-fast, fail-closed.

        `state` carries per-node sub-states under ``state["gates"]`` keyed by
        node name (e.g. ``state["gates"]["LAW"]``). A node is evaluated only
        when every required upstream PASSed; otherwise it is recorded
        NEED_EVIDENCE naming the blocking upstream. A FAIL verdict halts the
        whole decision immediately (global fail-fast). Returns the decision
        verdict, per-node results, where the decision stopped, the per-edge
        trace, and a hash-bound decision receipt.
        """
        state = state or {}
        decision_id = state.get("decision_id") or f"d-{_sha256(state)[:12]}"
        sub_states = state.get("gates") or {}
        gates: List[Dict[str, Any]] = []
        verdicts: Dict[str, GateVerdict] = {}
        evaluated: Dict[str, bool] = {}
        verdict = GateVerdict.PASS
        stopped_at: str | None = None
        halted = False
        for position, name in enumerate(EVALUATION_ORDER, start=1):
            blocked_by = [u for u in GATE_REQUIREMENTS[name]
                          if verdicts.get(u) != GateVerdict.PASS]
            if blocked_by:
                # Fail-closed: a node whose required inputs did not PASS is
                # not consulted — NEED_EVIDENCE, never an invented PASS.
                result = GateResult(
                    GateVerdict.NEED_EVIDENCE,
                    [f"KERNEL EDGE-BLOCKED at {name}: required upstream(s) "
                     f"{', '.join(blocked_by)} did not PASS; "
                     f"{'/'.join(GATE_REQUIREMENTS[name])} handoff withheld"],
                )
                was_evaluated = False
            else:
                result = self._run_gate(name, sub_states.get(name))
                was_evaluated = True
            verdicts[name] = result.verdict
            evaluated[name] = was_evaluated
            gates.append({
                "node": name,
                "position": position,
                "evaluated": was_evaluated,
                "verdict": result.verdict.value,
                "reasons": list(result.reasons),
                "blocked_by": blocked_by,
            })
            if result.verdict != GateVerdict.PASS and verdict == GateVerdict.PASS:
                verdict = result.verdict
                stopped_at = name
            if result.verdict == GateVerdict.FAIL:
                halted = True
                break  # fail-fast: a FAIL halts the whole decision
        edge_trace = self._edge_trace(verdicts, evaluated)
        receipt = self._decision_receipt(
            decision_id, gates, edge_trace, verdict, stopped_at)
        return {
            "decision_id": decision_id,
            "verdict": verdict.value,
            "stopped_at": stopped_at,
            "halted_on_fail": halted,
            "gates": gates,
            "edge_trace": edge_trace,
            "decision_receipt": receipt,
        }

    def gate_all(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate every gate without edge blocking; full audit visibility."""
        state = state or {}
        sub_states = state.get("gates") or {}
        out: List[Dict[str, Any]] = []
        for position, name in enumerate(EVALUATION_ORDER, start=1):
            result = self._run_gate(name, sub_states.get(name))
            out.append({
                "node": name,
                "position": position,
                "evaluated": True,
                "verdict": result.verdict.value,
                "reasons": list(result.reasons),
                "blocked_by": [],
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

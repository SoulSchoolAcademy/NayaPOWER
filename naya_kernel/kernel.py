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

Every decide()/gate_all() call emits a hash-bound receipt
(receipt_hash = SHA256 over the canonicalized body), so a cold successor
can re-verify what the graph decided and why. decide() emits a decision
receipt; gate_all() emits an AUDIT receipt (``audit-`` prefix, mode AUDIT)
that is verified but never counted as a decision verdict.
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
#: Also the partition key for the per-edge trace: every member must have a
#: recorded disposition in _edge_trace. A member with no recorded
#: disposition is labeled DISPOSITION_UNDEFINED, never silently
#: re-classified as a gate edge (guarded by test_non_gate_edges_partition_closed).
NON_GATE_EDGES = {
    "REL-KERNEL-ACT-KNOW",    # PRODUCES write edge — recorded, not re-gated
    "REL-KERNEL-EVOLVE-SELF",  # SUCCEEDS next-cycle edge — recorded, not traversed
}

NODE_ID = "NAYA-KERNEL"
KERNEL_VERSION = "0.3.0-candidate"
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


def _gate_states(state: Dict[str, Any]) -> Dict[str, Any]:
    """Return the per-node sub-states mapping, fail-closed on a malformed
    container: a non-dict ``state["gates"]`` is treated as absent (no gate
    is consulted with it) instead of crashing the kernel."""
    sub_states = (state or {}).get("gates") or {}
    if not isinstance(sub_states, dict):
        return {}
    return sub_states


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
        self.nodes = {}
        for name in EVALUATION_ORDER:
            if name == "LEARN":
                # Runtime VERIFY -> LEARN composition (P9 seam): LEARN's
                # intake resolver is construction-owned and bound to this
                # kernel's VERIFY node. No fixture path, no caller-supplied
                # resolver, no setter.
                verify_node = self.nodes["VERIFY"]
                self.nodes[name] = learn_node.LearnNode(
                    verify_resolver=verify_node.reference_resolver())
            else:
                self.nodes[name] = NODE_CLASSES[name]()

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
        with the source's verdict named. The non-gate edges (NON_GATE_EDGES,
        the single source of truth for the partition) are recorded with
        their honest disposition (write path / next cycle).
        """
        trace: List[Dict[str, Any]] = []
        for rel_id, source, target, rel_type in RUNTIME_EDGES:
            src_verdict = verdicts.get(source)
            if rel_id in NON_GATE_EDGES:
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
                else:
                    # Fail-closed labeling: a partition member with no
                    # recorded disposition must never be silently treated
                    # as a gate edge.
                    status = "DISPOSITION_UNDEFINED"
                    note = (f"non-gate edge {rel_id} has no recorded "
                            "disposition; not treated as a gate edge")
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
                          stopped_at: str | None,
                          unexpected_gate_keys: List[str] | None = None,
                          first_non_pass: GateVerdict | None = None,
                          first_non_pass_at: str | None = None,
                          inputs_hash: str | None = None
                          ) -> Dict[str, Any]:
        """Hash-bound decision receipt.

        ``unexpected_gate_keys`` names any ``state["gates"]`` keys that are
        not node names: they were recorded here, never consulted by any
        gate, and never steered the decision. Evidence-law honesty: a
        dropped input must be visible, not silent.

        ``first_non_pass`` / ``first_non_pass_at`` preserve the diagnostic
        record of the first gate that did not PASS, even when a later
        halting FAIL dominates the verdict (FAIL dominance, Brief 3,
        2026-10-01): the verdict answers "did it pass?", the preserved
        fields answer "where did it first wobble?".

        ``inputs_hash`` is the full SHA-256 over the canonical evaluated
        input state (the decide() input), bound into the body BEFORE
        receipt_hash is computed, so receipt_hash covers it. The
        persistence adapter independently recomputes this over the
        submitted state and rejects mismatch (naya-receipt-contract/1):
        the kernel produces it; the adapter verifies it; neither side
        invents it.
        """
        body: Dict[str, Any] = {
            "receipt_id": f"decision-{decision_id}",
            "node_id": NODE_ID,
            "kernel_version": KERNEL_VERSION,
            "topology": "canonical-runtime-graph-v1",
            "graph_seed": GRAPH_SEED_REF,
            "lock_ref": LOCK_REF,
            "decision_id": decision_id,
            "inputs_hash": inputs_hash,
            "evaluation_order": list(EVALUATION_ORDER),
            "verdict": verdict.value,
            "stopped_at": stopped_at,
            "first_non_pass": first_non_pass.value if first_non_pass else None,
            "first_non_pass_at": first_non_pass_at,
            "gates": gates,
            "edge_trace": edge_trace,
            "unexpected_gate_keys": list(unexpected_gate_keys or []),
            "issued_at": _now_iso(),
            "candidate_banner": "CANDIDATE — NOT RATIFIED — NOT MERGED",
        }
        body["receipt_hash"] = _sha256(body)
        return body

    def _audit_receipt(self, decision_id: str, gates: List[Dict[str, Any]],
                       verdict: GateVerdict,
                       unexpected_gate_keys: List[str] | None = None
                       ) -> Dict[str, Any]:
        """Hash-bound audit receipt for gate_all().

        Distinguished from decide()'s decision receipts by ``mode: "AUDIT"``
        and the ``audit-`` receipt_id prefix: the audit verdict aggregates an
        all-gates-consulted view (no fail-fast, no edge blocking) and must
        never be counted as a decision verdict — see cold_reconstruct().
        ``unexpected_gate_keys`` names any ``state["gates"]`` keys that are
        not node names: recorded here, never consulted by any gate, never
        steering the audit. Evidence-law honesty: a dropped input must be
        visible, not silent.
        """
        body: Dict[str, Any] = {
            "receipt_id": f"audit-{decision_id}",
            "node_id": NODE_ID,
            "kernel_version": KERNEL_VERSION,
            "mode": "AUDIT",
            "topology": "canonical-runtime-graph-v1",
            "graph_seed": GRAPH_SEED_REF,
            "lock_ref": LOCK_REF,
            "decision_id": decision_id,
            "evaluation_order": list(EVALUATION_ORDER),
            "verdict": verdict.value,
            "gates": gates,
            "unexpected_gate_keys": list(unexpected_gate_keys or []),
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
        whole decision immediately (global fail-fast) and dominates the
        decision verdict: the verdict names the halting FAIL even when an
        earlier gate returned NEED_EVIDENCE (Brief 3, 2026-10-01) — the
        first non-PASS is preserved in ``first_non_pass`` /
        ``first_non_pass_at`` for diagnostics. Returns the decision
        verdict, per-node results, where the decision stopped, the per-edge
        trace, and a hash-bound decision receipt.
        """
        state = state or {}
        decision_id = state.get("decision_id") or f"d-{_sha256(state)[:12]}"
        # P3 (naya-receipt-contract/1, 2026-10-01): the kernel binds the
        # full SHA-256 over the canonical evaluated input state into the
        # decision receipt. The persistence adapter independently
        # recomputes this over the state it submitted and rejects
        # mismatch; the kernel produces it, the adapter verifies it.
        inputs_hash = _sha256(state)
        sub_states = _gate_states(state)
        # Fail-visible (not fail-silent): caller-supplied gate keys that are
        # not node names are recorded in the receipt. They were NOT consulted
        # by any gate and never steered the decision.
        unexpected_gate_keys = sorted(
            k for k in sub_states if k not in EVALUATION_ORDER)
        gates: List[Dict[str, Any]] = []
        verdicts: Dict[str, GateVerdict] = {}
        evaluated: Dict[str, bool] = {}
        verdict = GateVerdict.PASS
        stopped_at: str | None = None
        first_non_pass: GateVerdict | None = None
        first_non_pass_at: str | None = None
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
            if result.verdict != GateVerdict.PASS and first_non_pass is None:
                # Diagnostic record: the first gate that did not PASS, kept
                # even when a later halting FAIL dominates the verdict.
                first_non_pass = result.verdict
                first_non_pass_at = name
            if result.verdict == GateVerdict.FAIL:
                halted = True
                # FAIL dominance (Brief 3, decided 2026-10-01 under the
                # Decision Protocol): a halting FAIL is the decision-relevant
                # fact, so the verdict names the FAIL — never an earlier
                # NEED_EVIDENCE. A naive consumer must not misread a decided
                # NO as "couldn't decide".
                verdict = GateVerdict.FAIL
                stopped_at = name
                break  # fail-fast: a FAIL halts the whole decision
            if verdict == GateVerdict.PASS and result.verdict != GateVerdict.PASS:
                verdict = result.verdict
                stopped_at = name
        edge_trace = self._edge_trace(verdicts, evaluated)
        receipt = self._decision_receipt(
            decision_id, gates, edge_trace, verdict, stopped_at,
            unexpected_gate_keys,
            first_non_pass=first_non_pass,
            first_non_pass_at=first_non_pass_at,
            inputs_hash=inputs_hash)
        return {
            "decision_id": decision_id,
            "verdict": verdict.value,
            "stopped_at": stopped_at,
            "first_non_pass": first_non_pass.value if first_non_pass else None,
            "first_non_pass_at": first_non_pass_at,
            "halted_on_fail": halted,
            "gates": gates,
            "edge_trace": edge_trace,
            "unexpected_gate_keys": unexpected_gate_keys,
            "decision_receipt": receipt,
        }

    def gate_all(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate every gate without edge blocking; full audit visibility.

        Unlike decide() there is no fail-fast and no edge blocking: every
        gate is consulted on its own sub-state. Returns the per-gate
        results, any unexpected gate keys (fail-visible: recorded here,
        never consulted, never steering), the audit verdict (first non-PASS
        in evaluation order, mirroring decide()'s naming rule — marked
        AUDIT, not a decision), and a hash-bound AUDIT receipt (verifiable
        with verify_decision_receipt(); kept out of cold_reconstruct()'s
        decision-verdict tallies by the ``audit-`` receipt_id prefix).
        """
        state = state or {}
        decision_id = state.get("decision_id") or f"d-{_sha256(state)[:12]}"
        sub_states = _gate_states(state)
        # Fail-visible (not fail-silent): caller-supplied gate keys that are
        # not node names are recorded in the receipt. They were NOT consulted
        # by any gate and never steered the audit.
        unexpected_gate_keys = sorted(
            k for k in sub_states if k not in EVALUATION_ORDER)
        out: List[Dict[str, Any]] = []
        verdict = GateVerdict.PASS
        for position, name in enumerate(EVALUATION_ORDER, start=1):
            result = self._run_gate(name, sub_states.get(name))
            if result.verdict != GateVerdict.PASS \
                    and verdict == GateVerdict.PASS:
                verdict = result.verdict
            out.append({
                "node": name,
                "position": position,
                "evaluated": True,
                "verdict": result.verdict.value,
                "reasons": list(result.reasons),
                "blocked_by": [],
            })
        receipt = self._audit_receipt(
            decision_id, out, verdict, unexpected_gate_keys)
        return {
            "decision_id": decision_id,
            "verdict": verdict.value,
            "gates": out,
            "unexpected_gate_keys": unexpected_gate_keys,
            "audit_receipt": receipt,
        }

    # -- cold reconstruction -------------------------------------------

    def cold_reconstruct(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rebuild kernel-level state from decision receipts alone.

        Verifies each decision receipt's hash, counts verdicts, and reports
        any receipt that fails verification (never trusted, always listed).
        gate_all() AUDIT receipts (``audit-`` receipt_id prefix) are hash-
        verified and reported separately — an audit verdict aggregates an
        all-gates-consulted view, not a decision, so it must never feed the
        decision-verdict tallies.
        """
        matched, mismatched = [], []
        audit_matched, audit_mismatched = [], []
        verdicts: Dict[str, int] = {}
        for receipt in receipts or []:
            check = verify_decision_receipt(receipt)
            rid = check["receipt_id"]
            is_audit = str(rid).startswith("audit-")
            if check["result"] == "MATCH":
                if is_audit:
                    audit_matched.append(rid)
                else:
                    matched.append(rid)
                    verdict = receipt.get("verdict", "UNKNOWN")
                    verdicts[verdict] = verdicts.get(verdict, 0) + 1
            else:
                # Mismatched receipts are listed, never trusted: their
                # verdict field is unauthenticated and must not feed counts.
                (audit_mismatched if is_audit else mismatched).append(rid)
        return {
            "receipts_checked": len(receipts or []),
            "hash_matched": matched,
            "hash_mismatched": mismatched,
            "audit_receipts_verified": audit_matched,
            "audit_receipts_mismatched": audit_mismatched,
            "verdicts": verdicts,
        }

"""
NayaPOWER Kernel Behavior Engine V2

Contract-first reference implementation of the nine-node kernel.
This module is intentionally fail-closed: it never turns missing evidence,
authority, observation, or persistence into a PASS/VERIFIED claim.

Status: IMPLEMENTED — runtime production proof remains separate.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Optional


NODE_ORDER = ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]
FAILURE_STATUSES = {"BLOCKED", "FAILED", "INCONCLUSIVE", "DEFERRED"}


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass
class NodeReceipt:
    node_id: str
    execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    input_hash: Optional[str] = None
    output_hash: Optional[str] = None
    status: str = "NOT_STARTED"
    rules_enforced: list[str] = field(default_factory=list)
    rules_checked: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    state_transition: Optional[dict[str, str]] = None

    def transition(self, from_state: str, to_state: str) -> None:
        self.state_transition = {"from": from_state, "to": to_state}

    def check(self, rule: str) -> None:
        self.rules_checked.append(rule)

    def enforce(self, rule: str) -> None:
        self.rules_enforced.append(rule)

    def add_evidence(self, evidence: str) -> None:
        self.evidence.append(evidence)

    def finish(self, status: str, output: Mapping[str, Any]) -> dict[str, Any]:
        self.status = status
        self.output_hash = canonical_hash(output)
        return self.to_dict()

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "execution_id": self.execution_id,
            "timestamp": self.timestamp,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "status": self.status,
            "rules_enforced": list(self.rules_enforced),
            "rules_checked": list(self.rules_checked),
            "state_transition": self.state_transition,
            "evidence": list(self.evidence),
        }


class KernelBehaviorEngine:
    """
    Executes a governed nine-node cognitive cycle.

    The engine is deliberately an orchestration/reference layer. Real
    persistence, authentication, authorization, and independent verification
    must be supplied by adapters and proven by runtime receipts.
    """

    def __init__(
        self,
        *,
        identity_resolver: Optional[Callable[[dict[str, Any]], Optional[dict[str, Any]]]] = None,
        authority_checker: Optional[Callable[[dict[str, Any], dict[str, Any]], bool]] = None,
        intelligence_reader: Optional[Callable[[str, str], list[dict[str, Any]]]] = None,
    ) -> None:
        self.identity_resolver = identity_resolver
        self.authority_checker = authority_checker
        self.intelligence_reader = intelligence_reader
        self.receipts: dict[str, NodeReceipt] = {}
        self.outputs: dict[str, dict[str, Any]] = {}
        self.cycle_id = str(uuid.uuid4())
        self.start_time = datetime.now(timezone.utc)

    def _begin(self, node_id: str, input_value: Any) -> NodeReceipt:
        receipt = self.receipts.setdefault(node_id, NodeReceipt(node_id))
        receipt.input_hash = canonical_hash(input_value)
        return receipt

    def _finish(self, node_id: str, status: str, output: dict[str, Any]) -> dict[str, Any]:
        self.outputs[node_id] = output
        self.receipts[node_id].finish(status, output)
        return output

    def process_self(self, input_context: dict[str, Any]) -> dict[str, Any]:
        r = self._begin("SELF", input_context)
        r.transition("UNINITIALIZED", "VALIDATING")
        r.check("Identity must be explicit and verifiable")
        r.check("Mission must be explicit")
        r.check("Continuity must be represented separately from authority")

        identity = dict(input_context.get("identity") or {})
        mission = dict(input_context.get("mission") or {})
        if self.identity_resolver:
            resolved = self.identity_resolver(input_context)
            if resolved:
                identity = resolved

        if not identity.get("actor_id") or not identity.get("system_id"):
            r.enforce("FAIL CLOSED: missing canonical identity")
            return self._finish("SELF", "BLOCKED", {"status": "BLOCKED", "reason": "identity_missing"})
        if not mission.get("mission") or not mission.get("objective"):
            r.enforce("FAIL CLOSED: missing mission")
            return self._finish("SELF", "BLOCKED", {"status": "BLOCKED", "reason": "mission_missing"})

        r.enforce("Identity resolved without inferring ownership from similarity or names")
        r.enforce("Continuity is context, not authority")
        r.transition("VALIDATING", "READY")
        r.add_evidence(f"identity:{identity['actor_id']}")
        return self._finish("SELF", "READY", {
            "status": "READY",
            "identity_context": identity,
            "mission_context": mission,
            "continuity_context": input_context.get("continuity", {}),
            "known_unknown_blocked": input_context.get("known_unknown_blocked", {}),
        })

    def process_law(self, input_context: dict[str, Any], self_output: dict[str, Any]) -> dict[str, Any]:
        r = self._begin("LAW", {"input": input_context, "self": self_output})
        r.transition("UNINITIALIZED", "VALIDATING")
        r.check("Authorization is action-specific")
        r.check("Revocation and expiry are checked before execution")
        r.check("Capability, retrieval, role text, and prior success never create authority")

        action = dict(input_context.get("proposed_action") or {})
        authority = dict(input_context.get("authority") or {})
        if not action:
            r.enforce("DENY: no proposed action")
            return self._finish("LAW", "BLOCKED", {"status": "BLOCKED", "reason": "action_missing"})
        if not authority.get("grant_id"):
            r.enforce("DENY: no authority grant")
            return self._finish("LAW", "BLOCKED", {"status": "BLOCKED", "reason": "authority_missing"})
        if authority.get("revoked") is True:
            r.enforce("DENY: authority revoked")
            return self._finish("LAW", "BLOCKED", {"status": "BLOCKED", "reason": "authority_revoked"})
        if authority.get("expires_at") not in (None, ""):
            # A caller that supplies an expired grant must explicitly mark it expired.
            if authority.get("expired") is True:
                r.enforce("DENY: authority expired")
                return self._finish("LAW", "BLOCKED", {"status": "BLOCKED", "reason": "authority_expired"})
        if self.authority_checker and not self.authority_checker(authority, action):
            r.enforce("DENY: external authority checker rejected action")
            return self._finish("LAW", "BLOCKED", {"status": "BLOCKED", "reason": "authority_scope_mismatch"})

        r.enforce("Authorization decision is explicit and auditable")
        r.transition("VALIDATING", "AUTHORIZED")
        return self._finish("LAW", "AUTHORIZED", {
            "status": "AUTHORIZED",
            "authority_context": authority,
            "action_context": action,
        })

    def process_act(self, input_context: dict[str, Any], law_output: dict[str, Any]) -> dict[str, Any]:
        r = self._begin("ACT", {"input": input_context, "law": law_output})
        r.transition("UNINITIALIZED", "PLANNING")
        r.check("No execution without LAW authorization")
        r.check("Expected outcome and proof requirements are defined before execution")
        r.check("Minimum sufficient action and idempotency are explicit")

        if law_output.get("status") != "AUTHORIZED":
            r.enforce("FAIL CLOSED: authorization missing")
            return self._finish("ACT", "BLOCKED", {"status": "BLOCKED", "reason": "not_authorized"})

        action = dict(law_output.get("action_context") or {})
        if not action.get("type"):
            r.enforce("FAIL CLOSED: action type missing")
            return self._finish("ACT", "BLOCKED", {"status": "BLOCKED", "reason": "action_type_missing"})

        execution_id = str(uuid.uuid4())
        expected = action.get("expected_outcome")
        proof_requirements = action.get("proof_requirements") or []
        r.enforce("Action is bound to the preceding authorization decision")
        r.transition("PLANNING", "READY")
        return self._finish("ACT", "READY", {
            "status": "READY",
            "execution_id": execution_id,
            "action": action,
            "expected_outcome": expected,
            "proof_requirements": proof_requirements,
            "idempotency_key": action.get("idempotency_key", execution_id),
            "execution_state": "READY_TO_EXECUTE",
        })

    def process_know(self, input_context: dict[str, Any], self_output: dict[str, Any]) -> dict[str, Any]:
        r = self._begin("KNOW", {"input": input_context, "self": self_output})
        r.transition("UNINITIALIZED", "RESTORING")
        query = str(input_context.get("query") or "")
        owner_id = str(self_output.get("identity_context", {}).get("owner_id")
                        or self_output.get("identity_context", {}).get("actor_id") or "")
        block_id = str(input_context.get("intelligent_block_id") or "")

        if self.intelligence_reader:
            if not owner_id or not block_id:
                r.enforce("FAIL CLOSED: owner and block identity required for durable retrieval")
                return self._finish("KNOW", "BLOCKED", {"status": "BLOCKED", "reason": "retrieval_identity_missing"})
            results = self.intelligence_reader(block_id, owner_id)
        else:
            results = list(input_context.get("intelligence") or [])

        r.check("Durable intelligence must retain stable identity and provenance")
        r.check("Retrieval must preserve owner scope and epistemic state")
        r.enforce("Similarity never becomes truth")
        r.enforce("Cross-owner retrieval is prohibited")
        r.transition("RESTORING", "READY")
        r.add_evidence(f"retrieval_count:{len(results)}")
        return self._finish("KNOW", "READY", {
            "status": "READY",
            "retrieval_context": {
                "query": query,
                "intelligent_block_id": block_id or None,
                "owner_id": owner_id or None,
                "results": results,
            },
        })

    def process_prove(self, input_context: dict[str, Any], know_output: dict[str, Any]) -> dict[str, Any]:
        r = self._begin("PROVE", {"input": input_context, "know": know_output})
        r.transition("UNINITIALIZED", "ASSESSING")
        evidence = list(input_context.get("evidence") or [])
        claim = str(input_context.get("claim") or "")
        r.check("Evidence provenance is explicit")
        r.check("Claim strength cannot exceed evidence strength")
        r.check("Limitations and conflicts are preserved")
        if not claim:
            r.enforce("FAIL CLOSED: claim missing")
            return self._finish("PROVE", "BLOCKED", {"status": "BLOCKED", "reason": "claim_missing"})
        if not evidence:
            r.enforce("NOT PROVEN: no evidence supplied")
            return self._finish("PROVE", "INCONCLUSIVE", {
                "status": "INCONCLUSIVE",
                "proof_context": {"claim": claim, "epistemic_state": "UNKNOWN", "reason": "evidence_missing"},
            })
        if any(not item.get("provenance") for item in evidence if isinstance(item, dict)):
            r.enforce("NOT PROVEN: evidence without provenance")
            return self._finish("PROVE", "INCONCLUSIVE", {
                "status": "INCONCLUSIVE",
                "proof_context": {"claim": claim, "epistemic_state": "UNKNOWN", "reason": "provenance_missing"},
            })
        r.transition("ASSESSING", "ASSESSED")
        return self._finish("PROVE", "ASSESSED", {
            "status": "ASSESSED",
            "proof_context": {
                "claim": claim,
                "epistemic_state": input_context.get("epistemic_state", "SUPPORTED"),
                "evidence_strength": input_context.get("evidence_strength", "MODERATE"),
                "limitations": list(input_context.get("limitations") or []),
            },
        })

    def process_connect(self, input_context: dict[str, Any], know_output: dict[str, Any], prove_output: dict[str, Any]) -> dict[str, Any]:
        r = self._begin("CONNECT", {"input": input_context, "know": know_output, "prove": prove_output})
        r.transition("UNINITIALIZED", "RESOLVING")
        relationships = list(input_context.get("relationships") or [])
        valid = [x for x in relationships if isinstance(x, dict) and x.get("type") and x.get("source") and x.get("target")]
        r.check("Relationships are typed and provenance-bound")
        r.check("Contradiction and supersession are explicit")
        r.check("Applicability is contextual, never inferred as authority")
        r.enforce("No trust is created by proximity or similarity alone")
        r.transition("RESOLVING", "CONNECTED")
        return self._finish("CONNECT", "CONNECTED", {
            "status": "CONNECTED",
            "connection_context": {
                "relationships": valid,
                "relationship_count": len(valid),
                "applicability": input_context.get("applicability", "contextual"),
            },
        })

    def process_verify(self, input_context: dict[str, Any], act_output: dict[str, Any], prove_output: dict[str, Any]) -> dict[str, Any]:
        r = self._begin("VERIFY", {"input": input_context, "act": act_output, "prove": prove_output})
        r.transition("UNINITIALIZED", "VERIFYING")
        expected = act_output.get("expected_outcome")
        observed = input_context.get("observed_outcome")
        independent = list(input_context.get("independent_evidence") or [])
        r.check("Expected and observed outcomes are compared explicitly")
        r.check("Independent evidence is required for independent verification")
        r.check("Causality is not inferred from sequence alone")

        if expected in (None, "") or observed in (None, ""):
            r.enforce("INCONCLUSIVE: expected or observed outcome missing")
            return self._finish("VERIFY", "INCONCLUSIVE", {"status": "INCONCLUSIVE", "reason": "observation_missing"})
        if not independent:
            r.enforce("INCONCLUSIVE: independent evidence missing")
            return self._finish("VERIFY", "INCONCLUSIVE", {
                "status": "INCONCLUSIVE",
                "verification_context": {"expected_outcome": expected, "observed_outcome": observed},
                "reason": "independent_evidence_missing",
            })
        outcome_status = "SUCCESS" if expected == observed else "MISMATCH"
        verification_status = "VERIFIED" if outcome_status == "SUCCESS" else "INCONCLUSIVE"
        r.enforce(f"Outcome classification: {outcome_status}")
        r.transition("VERIFYING", verification_status)
        return self._finish("VERIFY", verification_status, {
            "status": verification_status,
            "verification_context": {
                "expected_outcome": expected,
                "observed_outcome": observed,
                "outcome_status": outcome_status,
                "independent_evidence": independent,
                "causality": input_context.get("causality", "NOT_ESTABLISHED"),
            },
        })

    def process_learn(self, input_context: dict[str, Any], verify_output: dict[str, Any]) -> dict[str, Any]:
        r = self._begin("LEARN", {"input": input_context, "verify": verify_output})
        r.transition("UNINITIALIZED", "CANDIDATE")
        r.check("Only verified outcomes may enter promotion")
        r.check("Holdout evidence is required for behavioral promotion")
        r.check("Contradictions and rejected candidates remain traceable")
        if verify_output.get("status") != "VERIFIED":
            r.enforce("DECLINE PROMOTION: outcome not verified")
            return self._finish("LEARN", "DEFERRED", {
                "status": "DEFERRED",
                "learning_context": {"learning_state": "CANDIDATE", "promotion": "DECLINED"},
            })
        holdout = input_context.get("holdout_result")
        if holdout is not True:
            r.enforce("DECLINE PROMOTION: held-out improvement not proven")
            return self._finish("LEARN", "DEFERRED", {
                "status": "DEFERRED",
                "learning_context": {"learning_state": "CANDIDATE", "promotion": "DECLINED", "reason": "holdout_not_passed"},
            })
        r.transition("CANDIDATE", "PROMOTED")
        return self._finish("LEARN", "PROMOTED", {
            "status": "PROMOTED",
            "learning_context": {
                "candidate_id": str(uuid.uuid4()),
                "learning_state": "PROMOTED",
                "applicability_conditions": list(input_context.get("applicability_conditions") or ["contextual"]),
            },
        })

    def process_evolve(self, input_context: dict[str, Any], self_output: dict[str, Any], learn_output: dict[str, Any]) -> dict[str, Any]:
        r = self._begin("EVOLVE", {"input": input_context, "self": self_output, "learn": learn_output})
        r.transition("UNINITIALIZED", "CONSTRUCTING")
        r.check("Successor package preserves current truth, unknowns, blockers, proof and learning")
        r.check("Successor receives continuity but not inherited authority")
        if self_output.get("status") != "READY":
            r.enforce("BLOCK: SELF is not ready")
            return self._finish("EVOLVE", "BLOCKED", {"status": "BLOCKED", "reason": "self_not_ready"})
        package = {
            "kernel_revision": input_context.get("kernel_revision"),
            "current_truth": input_context.get("current_state", {}),
            "unknowns": input_context.get("unknowns", []),
            "blockers": input_context.get("blockers", []),
            "intelligent_block_ids": input_context.get("intelligent_block_ids", []),
            "relationships": input_context.get("relationships", []),
            "last_verified_outcome": input_context.get("observed_outcome"),
            "learning": learn_output.get("learning_context", {}),
            "next_action": input_context.get("next_action"),
            "authority_context": {"inherited_authority": False},
        }
        r.enforce("Continuity transfers intelligence, not permission")
        r.transition("CONSTRUCTING", "READY")
        return self._finish("EVOLVE", "READY", {
            "status": "READY",
            "evolution_context": {"successor_package": package, "improvement_proposals": input_context.get("improvement_proposals", [])},
        })

    def execute_cycle(self, input_context: dict[str, Any]) -> dict[str, Any]:
        self_result = self.process_self(input_context)
        if self_result["status"] != "READY":
            return self._cycle_result("BLOCKED", "SELF blocked")

        law_result = self.process_law(input_context, self_result)
        if law_result["status"] != "AUTHORIZED":
            return self._cycle_result("BLOCKED", f"LAW blocked: {law_result.get('reason', 'unknown')}")

        act_result = self.process_act(input_context, law_result)
        if act_result["status"] != "READY":
            return self._cycle_result("BLOCKED", "ACT blocked")

        know_result = self.process_know(input_context, self_result)
        if know_result["status"] != "READY":
            return self._cycle_result("BLOCKED", "KNOW blocked")

        prove_result = self.process_prove(input_context, know_result)
        connect_result = self.process_connect(input_context, know_result, prove_result)
        verify_result = self.process_verify(input_context, act_result, prove_result)
        learn_result = self.process_learn(input_context, verify_result)
        evolve_result = self.process_evolve(input_context, self_result, learn_result)

        final_status = "COMPLETED"
        if verify_result["status"] != "VERIFIED":
            final_status = "INCONCLUSIVE"
        return self._cycle_result(final_status, "Nine-node cycle completed with explicit proof state")

    def _cycle_result(self, status: str, message: str) -> dict[str, Any]:
        end_time = datetime.now(timezone.utc)
        duration_ms = (end_time - self.start_time).total_seconds() * 1000
        return {
            "schema": "naya.kernel.cycle-result.v2",
            "cycle_id": self.cycle_id,
            "status": status,
            "message": message,
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_ms": round(duration_ms, 2),
            "node_receipts": {nid: receipt.to_dict() for nid, receipt in self.receipts.items()},
            "nodes_processed": list(self.receipts.keys()),
            "overall_status": status,
        }

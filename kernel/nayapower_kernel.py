from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from runtime.canonical_memory import RetrievedIntelligentBlock, RetrievedRelationship


class Node(str, Enum):
    SELF = "SELF"
    LAW = "LAW"
    ACT = "ACT"
    KNOW = "KNOW"
    PROVE = "PROVE"
    CONNECT = "CONNECT"
    VERIFY = "VERIFY"
    LEARN = "LEARN"
    EVOLVE = "EVOLVE"


class TruthState(str, Enum):
    UNKNOWN = "UNKNOWN"
    VERIFIED = "VERIFIED"
    BLOCKED = "BLOCKED"


CANONICAL_NODE_ORDER = tuple(Node)
CANONICAL_NODE_IDS = tuple(f"NAYA-KERNEL-{node.value}" for node in CANONICAL_NODE_ORDER)


@dataclass(frozen=True)
class Authority:
    scope: str


@dataclass(frozen=True)
class DecisionContext:
    action: str
    consequential: bool
    authority: Authority | None
    task_target: str | None = None
    intelligence: tuple["RetrievedIntelligentBlock", ...] = ()
    relationships: tuple["RetrievedRelationship", ...] = ()


@dataclass(frozen=True)
class DecisionResult:
    allowed: bool
    executed: bool
    truth_state: TruthState
    blocked_by: Node | None = None
    trace: tuple[Node, ...] = ()
    evidence: tuple[str, ...] = ()
    outcome: str | None = None
    next_state: dict[str, str] = field(default_factory=dict)
    learning_candidate: str | None = None


class Kernel:
    _NODE_ORDER = CANONICAL_NODE_ORDER

    def __init__(self, *, kernel_id: str = "NAYAPOWER-MASTER-KERNEL-V1", source_manifest: str | None = None):
        self.kernel_id = kernel_id
        self.source_manifest = source_manifest

    @classmethod
    def from_brain(cls, root: Path) -> "Kernel":
        manifest_path = Path(root) / "BRAIN/03-KERNEL/MANIFEST.json"
        if not manifest_path.exists():
            raise ValueError("canonical brain manifest is missing")
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        node_names = tuple(node.get("name") for node in data.get("nodes", []))
        if node_names != tuple(node.value for node in CANONICAL_NODE_ORDER):
            raise ValueError("manifest does not match canonical nine-node order")
        node_ids = tuple(node.get("id") for node in data.get("nodes", []))
        if node_ids != CANONICAL_NODE_IDS:
            raise ValueError("manifest node IDs do not match canonical nine-node identity")
        if data.get("kernel_id") != "NAYAPOWER-MASTER-KERNEL-V1":
            raise ValueError("manifest kernel identity is not canonical")
        if data.get("runtime_entrypoint") != "runtime/cold_runtime.py":
            raise ValueError("manifest runtime entrypoint is not canonical")
        if data.get("runtime_loader") != "Kernel.from_brain":
            raise ValueError("manifest runtime loader is not canonical")
        if data.get("canonical_persistence_adapter") != "runtime/canonical_memory.py":
            raise ValueError("manifest persistence adapter is not canonical")
        return cls(kernel_id=data["kernel_id"], source_manifest="BRAIN/03-KERNEL/MANIFEST.json")

    @classmethod
    def node_order(cls):
        return cls._NODE_ORDER

    def decide(self, context: DecisionContext) -> DecisionResult:
        trace = (Node.SELF, Node.LAW)

        if context.consequential and (
            context.authority is None
            or context.authority.scope != context.action
        ):
            return DecisionResult(
                allowed=False,
                executed=False,
                truth_state=TruthState.BLOCKED,
                blocked_by=Node.LAW,
                trace=trace,
            )

        trace = self._NODE_ORDER
        evidence = [
            f"LAW.authority:{context.action}",
            f"KNOW.context:{context.action}",
            f"CONNECT.relevance:{context.action}",
            f"PROVE.action:{context.action}",
        ]

        candidates = tuple(
            block
            for block in context.intelligence
            if block.understanding_state == "VERIFIED"
            and block.status not in {"DELETED", "SUPERSEDED"}
            and block.is_applicable_to(context.task_target)
        )
        applicable_blocks = []
        for block in candidates:
            supporting_relationships = tuple(
                relationship
                for relationship in context.relationships
                if relationship.is_verified_support_for(block.intelligent_block_id)
            )
            if not supporting_relationships:
                continue
            applicable_blocks.append((block, supporting_relationships))
            evidence.append(
                f"KNOW.retained_intelligence:{block.evidence_key()}"
            )
            evidence.extend(
                f"CONNECT.applicability:{block.intelligent_block_id}:{context.task_target}"
                for _ in supporting_relationships
            )
            evidence.extend(
                f"CONNECT.relationship:{relationship.relationship_id}:{relationship.relationship_type}"
                for relationship in supporting_relationships
            )
        applicable = tuple(block for block, _ in applicable_blocks)

        # Execution is an observation, not proof that the intended outcome
        # occurred. VERIFY must establish outcome before truth can be promoted.
        outcome = (
            "executed_with_relationship_aware_intelligence"
            if applicable
            else "executed"
        )
        next_state = {"last_action": context.action}
        if applicable:
            next_state["retained_intelligence_applied"] = "true"
            next_state["retained_intelligence_ids"] = ",".join(
                block.intelligent_block_id for block in applicable
            )

        return DecisionResult(
            allowed=True,
            executed=True,
            truth_state=TruthState.UNKNOWN,
            trace=trace,
            evidence=tuple(evidence),
            outcome=outcome,
            next_state=next_state,
            learning_candidate=None,
        )

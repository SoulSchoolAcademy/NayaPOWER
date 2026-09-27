from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

from kernel.runtime_boot import load_runtime_manifest

if TYPE_CHECKING:
    from kernel.supabase_intelligent_blocks import (
        IntelligentBlock,
        IntelligentRelationship,
        SupabaseIntelligentBlockReader,
    )


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


@dataclass(frozen=True)
class Authority:
    scope: str


@dataclass(frozen=True)
class DecisionContext:
    action: str
    consequential: bool
    authority: Authority | None
    task_target: str | None = None
    intelligence: tuple["IntelligentBlock", ...] = ()
    relationships: tuple["IntelligentRelationship", ...] = ()


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
    _NODE_ORDER = (
        Node.SELF,
        Node.LAW,
        Node.ACT,
        Node.KNOW,
        Node.PROVE,
        Node.CONNECT,
        Node.VERIFY,
        Node.LEARN,
        Node.EVOLVE,
    )

    def __init__(self, brain_root: Path | None = None):
        manifest = load_runtime_manifest(brain_root)
        self._manifest = manifest
        self._NODE_ORDER = tuple(Node(node["name"]) for node in manifest["nodes"])

    @property
    def manifest(self) -> dict:
        return self._manifest

    @property
    def node_trace(self):
        return self._NODE_ORDER

    def retrieve_intelligent_context(
        self,
        reader: "SupabaseIntelligentBlockReader",
        *,
        intelligent_block_id: str,
        owner_id: str,
    ) -> tuple["IntelligentBlock | None", tuple["IntelligentRelationship", ...]]:
        """Cross the canonical persistence boundary and load CONNECT context."""
        return reader.get_context(
            intelligent_block_id=intelligent_block_id,
            owner_id=owner_id,
        )

    @classmethod
    def node_order(cls):
        return cls._NODE_ORDER

    def retrieve_intelligent_block(
        self,
        reader: "SupabaseIntelligentBlockReader",
        *,
        intelligent_block_id: str,
        owner_id: str,
    ) -> "IntelligentBlock | None":
        """Retrieve canonical retained intelligence through the persistence boundary."""
        return reader.get_by_intelligent_block_id(
            intelligent_block_id=intelligent_block_id,
            owner_id=owner_id,
        )

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
        evidence = (
            f"LAW.authority:{context.action}",
            f"KNOW.context:{context.action}",
            f"CONNECT.relevance:{context.action}",
            f"PROVE.action:{context.action}",
        )

        applicable = []
        for block in context.intelligence:
            if not block.is_applicable_to(context.task_target):
                continue
            supporting_relationships = tuple(
                relationship
                for relationship in context.relationships
                if relationship.is_verified_support_for(block.intelligent_block_id)
            )
            if not supporting_relationships:
                continue
            applicable.append((block, supporting_relationships))

        outcome = (
            "executed_with_relationship_aware_intelligence"
            if applicable
            else "executed"
        )
        next_state = {"last_action": context.action}
        if applicable:
            next_state["retained_intelligence_applied"] = "true"
            next_state["retained_intelligence_ids"] = ",".join(
                block.intelligent_block_id for block, _ in applicable
            )
            evidence = evidence + tuple(
                evidence_item
                for block, relationships in applicable
                for evidence_item in (
                    f"KNOW.retained_intelligence:{block.evidence_key()}",
                    *(
                        f"CONNECT.relationship:{relationship.relationship_id}:{relationship.relationship_type}"
                        for relationship in relationships
                    ),
                )
            )

        return DecisionResult(
            allowed=True,
            executed=True,
            truth_state=TruthState.UNKNOWN,
            trace=trace,
            evidence=evidence,
            outcome=outcome,
            next_state=next_state,
            learning_candidate=None,
        )

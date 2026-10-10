from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

from kernel.runtime_boot import load_runtime_manifest

if TYPE_CHECKING:
    from kernel.supabase_intelligent_blocks import IntelligentBlock, SupabaseIntelligentBlockReader


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

    @property
    def manifest(self) -> dict:
        return self._manifest

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
        """Return a governed decision. This method does not execute the action.

        Execution is a separate boundary and must be proven by an executor/runtime
        receipt. Authority to act is not evidence that execution occurred.
        """
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

        # This reference kernel has established only the decision/authority
        # boundary. It must not claim ACT/KNOW/PROVE/CONNECT/VERIFY/LEARN/EVOLVE
        # ran, and it must not manufacture an execution outcome without an
        # injected executor plus observed evidence.
        evidence = (
            f"LAW.authority:{context.action}",
            "DECISION.authorized_not_executed",
        )

        return DecisionResult(
            allowed=True,
            executed=False,
            truth_state=TruthState.UNKNOWN,
            trace=trace,
            evidence=evidence,
            outcome=None,
            next_state={},
            learning_candidate=None,
        )

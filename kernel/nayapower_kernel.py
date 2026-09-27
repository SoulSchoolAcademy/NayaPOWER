from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from pathlib import Path

from kernel.brain_registry import (
    BrainIntegrityError,
    load_canonical_node_names,
    repo_root,
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


class KernelIntegrityError(RuntimeError):
    """The canonical kernel manifest could not be trusted to describe the kernel.

    Distinct from BrainIntegrityError so callers can tell "the brain is broken"
    from "the brain says something this runtime cannot represent" -- the second
    is a code/manifest mismatch and must never be silently tolerated.
    """


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
    """Governed decision kernel whose node order comes from the canonical manifest.

    The nine Master Nodes are defined by BRAIN/03-KERNEL/MANIFEST.json. This
    class holds no copy of that order: a hardcoded tuple here would be a second
    canonical store that can drift from the manifest with nothing failing.
    """

    @classmethod
    @lru_cache(maxsize=None)
    def _manifest_order(cls, root: str | None) -> tuple[Node, ...]:
        base = Path(root) if root is not None else repo_root()
        names = load_canonical_node_names(base)
        order: list[Node] = []
        for name in names:
            try:
                order.append(Node(name))
            except ValueError as exc:
                raise KernelIntegrityError(
                    f"manifest_declares_node_this_runtime_cannot_represent:{name}"
                ) from exc
        return tuple(order)

    @classmethod
    def node_order(cls, root: Path | None = None) -> tuple[Node, ...]:
        """The nine Master Nodes, read from the canonical manifest.

        Raises KernelIntegrityError if the manifest is missing, malformed, or
        names a node this runtime does not implement.
        """
        return cls._manifest_order(str(root) if root is not None else None)

    @classmethod
    def clear_cache(cls) -> None:
        """Drop the memoised manifest order (tests that mutate the manifest)."""
        cls._manifest_order.cache_clear()

    def decide(self, context: DecisionContext, root: Path | None = None) -> DecisionResult:
        # Fail closed before anything else. A kernel that cannot prove what its
        # own nodes are must not authorize an action, however well-scoped the
        # authority looks.
        try:
            node_order = self.node_order(root)
        except (BrainIntegrityError, KernelIntegrityError) as exc:
            return DecisionResult(
                allowed=False,
                executed=False,
                truth_state=TruthState.BLOCKED,
                blocked_by=Node.KNOW,
                trace=(Node.SELF, Node.KNOW),
                evidence=(f"KNOW.kernel_integrity:{exc}",),
            )

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

        trace = node_order
        evidence = (
            f"LAW.authority:{context.action}",
            f"KNOW.context:{context.action}",
            f"CONNECT.relevance:{context.action}",
            f"PROVE.action:{context.action}",
        )

        # Execution is an observation, not proof that the intended outcome
        # occurred. VERIFY must establish outcome before truth can be promoted.
        outcome = "executed"
        next_state = {"last_action": context.action}

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

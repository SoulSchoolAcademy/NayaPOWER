from dataclasses import dataclass, field
from enum import Enum


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

    @classmethod
    def node_order(cls):
        return cls._NODE_ORDER

    def decide(self, context: DecisionContext) -> DecisionResult:
        if context.consequential and (
            context.authority is None
            or context.authority.scope != context.action
        ):
            return DecisionResult(
                allowed=False,
                executed=False,
                truth_state=TruthState.BLOCKED,
                blocked_by=Node.LAW,
            )

        evidence = (
            f"LAW.authority:{context.action}",
            f"PROVE.action:{context.action}",
        )
        outcome = "executed"
        next_state = {"last_action": context.action}

        return DecisionResult(
            allowed=True,
            executed=True,
            truth_state=TruthState.VERIFIED,
            evidence=evidence,
            outcome=outcome,
            next_state=next_state,
            learning_candidate=None,
        )

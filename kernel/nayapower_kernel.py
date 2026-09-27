from dataclasses import dataclass, field
from datetime import datetime, timezone
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


class LawDecision(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    DENIED = "DENIED"
    REQUIRES_CONFIRMATION = "REQUIRES_CONFIRMATION"
    AMBIGUOUS = "AMBIGUOUS"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


class TruthState(str, Enum):
    UNKNOWN = "UNKNOWN"
    VERIFIED = "VERIFIED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class Authority:
    scope: str
    consent_granted: bool = True
    requires_confirmation: bool = False
    revoked: bool = False
    expires_at: datetime | None = None


@dataclass(frozen=True)
class DecisionContext:
    action: str
    consequential: bool
    authority: Authority | None
    confirmation_granted: bool = False


@dataclass(frozen=True)
class DecisionResult:
    allowed: bool
    executed: bool
    truth_state: TruthState
    law_decision: LawDecision = LawDecision.AMBIGUOUS
    blocked_by: Node | None = None
    trace: tuple[Node, ...] = ()
    evidence: tuple[str, ...] = ()
    outcome: str | None = None
    next_state: dict[str, str] = field(default_factory=dict)
    learning_candidate: str | None = None
    audit_receipt: dict[str, object] = field(default_factory=dict)


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

    def _law_decide(self, context: DecisionContext) -> tuple[LawDecision, str]:
        if not context.consequential:
            return LawDecision.AUTHORIZED, "action is non-consequential"
        authority = context.authority
        if authority is None:
            return LawDecision.AMBIGUOUS, "authority could not be resolved"
        if authority.revoked:
            return LawDecision.REVOKED, "authority is revoked"
        if authority.expires_at is not None and authority.expires_at <= datetime.now(timezone.utc):
            return LawDecision.EXPIRED, "authority has expired"
        if authority.consent_granted is False:
            return LawDecision.DENIED, "explicit consent is absent"
        if authority.scope != context.action:
            return LawDecision.OUT_OF_SCOPE, "authority scope does not cover action"
        if authority.requires_confirmation and not context.confirmation_granted:
            return LawDecision.REQUIRES_CONFIRMATION, "explicit confirmation is required"
        return LawDecision.AUTHORIZED, "live authority covers the requested action"

    def decide(self, context: DecisionContext) -> DecisionResult:
        law_decision, rationale = self._law_decide(context)
        trace = (Node.SELF, Node.LAW)
        audit_receipt = {
            "node": Node.LAW.value,
            "action": context.action,
            "decision": law_decision.value,
            "rationale": rationale,
            "consequential": context.consequential,
            "authority_scope": context.authority.scope if context.authority else None,
        }
        if law_decision is not LawDecision.AUTHORIZED:
            return DecisionResult(
                allowed=False,
                executed=False,
                truth_state=TruthState.BLOCKED,
                law_decision=law_decision,
                blocked_by=Node.LAW,
                trace=trace,
                audit_receipt=audit_receipt,
            )
        trace = self._NODE_ORDER
        evidence = (
            f"LAW.authorization:{context.action}",
            f"KNOW.context:{context.action}",
            f"CONNECT.relevance:{context.action}",
            f"PROVE.action:{context.action}",
        )
        outcome = "executed"
        next_state = {"last_action": context.action}
        return DecisionResult(
            allowed=True,
            executed=True,
            truth_state=TruthState.UNKNOWN,
            law_decision=law_decision,
            trace=trace,
            evidence=evidence,
            outcome=outcome,
            next_state=next_state,
            learning_candidate=None,
            audit_receipt=audit_receipt,
        )

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any
import logging

from kernel.knowledge_query import retrieve_applicable_intelligence
from kernel.runtime_boot import load_runtime_manifest
from kernel.value_calculus import (
    QualityProfile,
    RiskPolicy,
    evaluate_candidates,
)

logger = logging.getLogger(__name__)

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
    next_state: dict[str, Any] = field(default_factory=dict)
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

        # Phase 2 wiring (ACT -> KNOW): consult KNOW's memory for intelligence
        # applicable to the pending decision. LAW's verdict stands alone --
        # if KNOW is unavailable the decision proceeds without intelligence.
        try:
            intelligence = retrieve_applicable_intelligence(
                context, truth_floor="VERIFIED", max_results=5
            )
        except Exception as exc:  # never let KNOW take down a decision
            logger.warning("KNOW unavailable during decide(): %s", exc)
            intelligence = []

        if intelligence:
            trace = (Node.SELF, Node.LAW, Node.KNOW)

        next_state: dict[str, Any] = {
            "intelligence_consulted": intelligence,
            "intelligence_count": len(intelligence),
        }

        # Value-calculus scoring of candidate options, when the context
        # carries any. DecisionContext has no candidates field today, so this
        # skips gracefully; it activates if a candidates/options field is
        # added later. LAW PROHIBITED already short-circuited above.
        self._score_candidates_if_present(context, next_state)

        # This reference kernel has established only the decision/authority
        # boundary. It must not claim ACT/PROVE/CONNECT/VERIFY/LEARN/EVOLVE
        # ran, and it must not manufacture an execution outcome without an
        # injected executor plus observed evidence.
        evidence = (
            f"LAW.authority:{context.action}",
            "DECISION.authorized_not_executed",
            f"KNOW.intelligence:{len(intelligence)}_blocks_consulted",
        )

        return DecisionResult(
            allowed=True,
            executed=False,
            truth_state=TruthState.UNKNOWN,
            trace=trace,
            evidence=evidence,
            outcome=None,
            next_state=next_state,
            learning_candidate=None,
        )

    @staticmethod
    def _score_candidates_if_present(
        context: DecisionContext, next_state: dict[str, Any]
    ) -> None:
        """Score candidate options with the V2.1 value calculus, if present.

        No-op when the context carries no candidates/options field.
        Failures are logged and recorded, never raised: candidate scoring is
        advisory and must not block LAW's decision.
        """
        candidates = getattr(context, "candidates", None) or getattr(
            context, "options", None
        )
        if not candidates:
            return
        try:
            baseline = next(
                (c for c in candidates if getattr(c, "is_baseline", False)), None
            )
            baseline_id = (
                baseline.candidate_id
                if baseline is not None
                else getattr(candidates[0], "candidate_id", None)
            )
            profile = getattr(context, "quality_profile", None) or QualityProfile(
                profile_id="kernel-default",
                version="1",
                objective=getattr(context, "action", "decision"),
            )
            risk_policy = getattr(context, "risk_policy", None) or RiskPolicy()
            evaluation = evaluate_candidates(
                candidates, baseline_id, profile, risk_policy
            )
            selected_id = evaluation.get("selected")
            winner = next(
                (
                    r
                    for r in evaluation.get("rows", [])
                    if r["candidate_id"] == selected_id
                ),
                None,
            )
            next_state["candidate_evaluation"] = {
                "decision": evaluation.get("decision"),
                "selected": selected_id,
                "winner_v_safe": winner["v_safe"] if winner else None,
                "winner_q": winner["q"]["Q"] if winner else None,
                "frontier_size": len(evaluation.get("frontier", [])),
            }
        except Exception as exc:
            logger.warning("candidate evaluation skipped: %s", exc)
            next_state["candidate_evaluation"] = {"skipped": str(exc)}

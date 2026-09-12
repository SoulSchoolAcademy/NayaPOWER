"""Authorized Host Executor Bridge for Naya Power.

The bridge closes the runtime loop without creating a new authority layer:

RESTORE → PLAN → AUTHORIZE → EXECUTE → OBSERVE → VERIFY → SCORE/OSCAR → PERSIST → CONTINUE

The bridge never grants authority. The host must provide an executor explicitly and
must return an ExecutionReceipt containing independently observed evidence. Human-
required actions are surfaced as a handoff rather than silently bypassed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Sequence

from mission_state_store import LeadModeEngine
from naya_power_runtime import ActionCandidate, ActionPlan, ExecutionReceipt
from quality_gate import OscarReview, Scorecard, apply_quality_decision, evaluate_quality


Executor = Callable[[ActionPlan], ExecutionReceipt]
CandidateProvider = Callable[[dict], Sequence[ActionCandidate]]
ScorecardProvider = Callable[[object, ExecutionReceipt], Scorecard]
OscarProvider = Callable[[object, ExecutionReceipt, Scorecard], OscarReview]


@dataclass(frozen=True)
class HumanHandoff:
    """The smallest possible request when execution cannot responsibly continue."""

    reason: str
    requested_decision: str


@dataclass(frozen=True)
class LeadCycleResult:
    status: str
    plan: ActionPlan | None = None
    receipt: ExecutionReceipt | None = None
    handoff: HumanHandoff | None = None
    quality_promoted: bool = False
    next_action: str | None = None


class HostExecutorBridge:
    """Closed-loop host adapter; tool capability remains outside the bridge."""

    def __init__(
        self,
        engine: LeadModeEngine,
        candidate_provider: CandidateProvider,
        executor: Executor,
        scorecard_provider: ScorecardProvider | None = None,
        oscar_provider: OscarProvider | None = None,
    ) -> None:
        self.engine = engine
        self.candidate_provider = candidate_provider
        self.executor = executor
        self.scorecard_provider = scorecard_provider
        self.oscar_provider = oscar_provider

    def cycle(self) -> LeadCycleResult:
        """Execute exactly one authorized cycle, then persist its continuation state."""
        restored = self.engine.restore()
        state = self.engine.store.load()
        candidates = self.candidate_provider(restored)

        try:
            plan = self.engine.choose(candidates)
        except RuntimeError as error:
            return LeadCycleResult(
                status="HUMAN_OR_EXTERNAL_INPUT_REQUIRED",
                handoff=HumanHandoff(
                    reason=str(error),
                    requested_decision="Provide authority, evidence, dependency resolution, or the required external action.",
                ),
                next_action=state.next_action,
            )

        receipt = self.executor(plan)
        updated = self.engine.accept_execution(plan, receipt)

        if not receipt.verified:
            return LeadCycleResult(
                status="VERIFICATION_REQUIRED",
                plan=plan,
                receipt=receipt,
                next_action=updated.next_action,
            )

        if self.scorecard_provider is None or self.oscar_provider is None:
            return LeadCycleResult(
                status="QUALITY_REVIEW_REQUIRED",
                plan=plan,
                receipt=receipt,
                next_action=updated.next_action,
            )

        scorecard = self.scorecard_provider(updated, receipt)
        oscar = self.oscar_provider(updated, receipt, scorecard)
        decision = evaluate_quality(updated, scorecard, oscar, receipt.next_action)
        apply_quality_decision(updated, decision)
        self.engine.store.save(updated)

        return LeadCycleResult(
            status="CONTINUE" if decision.promoted else "REPAIR_REQUIRED",
            plan=plan,
            receipt=receipt,
            quality_promoted=decision.promoted,
            next_action=decision.next_action,
        )

    def run_until_handoff(self, max_cycles: int = 10) -> list[LeadCycleResult]:
        """Continue automatically, with a bounded safety valve for each host invocation."""
        if max_cycles < 1:
            raise ValueError("max_cycles must be >= 1")

        results: list[LeadCycleResult] = []
        for _ in range(max_cycles):
            result = self.cycle()
            results.append(result)
            if result.status != "CONTINUE":
                break
        return results

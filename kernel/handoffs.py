"""ACT -> KNOW feedback arc: the execution handoff contract.

An ExecutionHandoff is the structured record a completed ACT execution emits
for the KNOW node to ingest. It closes the loop: what was decided (LAW),
what was done (ACT), what was observed at execution time. The handoff carries
the prediction (expected outcome from the plan) next to the observation so
the PROVE step can later verify outcome against prediction.

Handoffs always enter KNOW as CANDIDATE — the KNOW node's own machinery
(verification, proof, promotion) decides whether they ever rise above that.

Schema: naya.execution-handoff.v1
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class ExecutionHandoff:
    schema: str = "naya.execution-handoff.v1"
    execution_id: str = ""
    decision_ref: str = ""       # links to the DecisionResult / LAW receipt
    action_taken: str = ""
    outcome_observed: str = ""
    predicted_outcome: str = ""  # what the plan expected (compared by PROVE)
    timestamp: str = ""          # UTC ISO
    provenance: dict = field(default_factory=dict)  # law_receipt_id, act_receipt_id
    truth_state: str = "CANDIDATE"  # handoffs enter as CANDIDATE, never higher

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


def emit_execution_handoff(execution_id: str,
                           action_taken: str,
                           *,
                           decision_ref: str = "",
                           outcome_observed: str = "",
                           predicted_outcome: str = "",
                           provenance: Optional[dict] = None,
                           truth_state: str = "CANDIDATE") -> ExecutionHandoff:
    """Construct an ExecutionHandoff, stamped with the current UTC time.

    Fail-closed constructor: execution_id and action_taken must be non-empty
    (raises ValueError otherwise), and truth_state may never enter above
    CANDIDATE.
    """
    if not str(execution_id or "").strip():
        raise ValueError("execution_id is required and must be non-empty")
    if not str(action_taken or "").strip():
        raise ValueError("action_taken is required and must be non-empty")
    if str(truth_state or "").upper() != "CANDIDATE":
        raise ValueError(
            f"handoffs enter KNOW as CANDIDATE, never {truth_state!r}")
    return ExecutionHandoff(
        execution_id=str(execution_id),
        decision_ref=str(decision_ref or ""),
        action_taken=str(action_taken),
        outcome_observed=str(outcome_observed or ""),
        predicted_outcome=str(predicted_outcome or ""),
        timestamp=datetime.now(timezone.utc).isoformat(),
        provenance=dict(provenance or {}),
        truth_state="CANDIDATE",
    )

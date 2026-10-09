"""Data models for successor ingestion. Pure — no DB, no network."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Lesson:
    """A verified learned law retrieved from the canonical store.

    retrieved_at / query are the provenance of THIS retrieval — a lesson
    without retrieval provenance cannot enter the reuse path.
    """

    id: str
    target_id: str
    level: str
    status: str
    provenance: str
    verification_method: str
    claim_text: str
    retrieved_at: str
    query: str


@dataclass(frozen=True)
class Applicability:
    verdict: str  # APPLICABLE | NOT_APPLICABLE
    reason: str


@dataclass(frozen=True)
class StageResult:
    stage: str
    state: str  # PRESENT | PENDING | GAP | UNINSTRUMENTED (lineage vocabulary)
    detail: str


@dataclass
class ChainReport:
    """The 11-stage walk for one reuse event."""

    task_family: str
    stages: list = field(default_factory=list)
    verdict: str = "UNRUN"

    def to_dict(self) -> dict:
        return {
            "task_family": self.task_family,
            "verdict": self.verdict,
            "stages": [
                {"stage": s.stage, "state": s.state, "detail": s.detail}
                for s in self.stages
            ],
        }

"""Data models for the Learn-Once Loop.

A Lesson moves through stages:
    CAPTURED -> DISTILLED -> ENCODED -> VERIFIED -> ACTIVE
with failure states:
    FAILED    — a re-tell was recorded (the teacher had to repeat the teaching).
                This is a loop failure and is filed as a bug.
    REGRESSED — a previously passing behavioral check now fails.

The metric of learning is zero re-tells. Silence is the test.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum


class Stage(str, Enum):
    CAPTURED = "CAPTURED"
    DISTILLED = "DISTILLED"
    ENCODED = "ENCODED"
    VERIFIED = "VERIFIED"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"
    REGRESSED = "REGRESSED"


# Forward-only happy path. FAILED/REGRESSED are entered from any encoded stage.
STAGE_ORDER = [
    Stage.CAPTURED,
    Stage.DISTILLED,
    Stage.ENCODED,
    Stage.VERIFIED,
    Stage.ACTIVE,
]

TERMINAL_BAD = {Stage.FAILED, Stage.REGRESSED}
LEARNED_STAGES = {Stage.VERIFIED, Stage.ACTIVE}


@dataclass
class IntelligentBlock:
    """Distilled essence of a teaching. Multiple perspectives, actionable."""

    essence: str  # one or two sentences: the irreducible core
    perspectives: dict  # e.g. {"human": ..., "learner": ..., "machine": ...}
    actionable_rule: str  # what to DO, stated as a rule
    machine_check: str  # how the machine verifies the rule is live
    beneficiary_value: str = ""  # what's in it for the learner

    def validate(self) -> list[str]:
        issues = []
        if not self.essence or len(self.essence.strip()) < 10:
            issues.append("essence must be a substantive statement, not a fragment")
        required = {"human", "learner", "machine"}
        missing = required - set(self.perspectives or {})
        if missing:
            issues.append(
                f"IB requires human/learner/machine perspectives; missing: {sorted(missing)}"
            )
        if not self.actionable_rule or len(self.actionable_rule.strip()) < 10:
            issues.append("actionable_rule must state what to DO")
        if not self.machine_check:
            issues.append("machine_check must name how the machine verifies the rule")
        return issues


@dataclass
class EncodingTarget:
    """One place in the machine where the lesson must live."""

    kind: str  # law_file | gate | test | cron_body | manifest_entry
    location: str | None = None
    status: str = "TODO"  # DONE | NA | TODO
    note: str = ""


@dataclass
class EncodingRecord:
    """The encoding checklist. A lesson is NOT learned until it lives in the
    machine — a note alone never counts."""

    law_file: EncodingTarget = field(
        default_factory=lambda: EncodingTarget(kind="law_file")
    )
    gate: EncodingTarget = field(default_factory=lambda: EncodingTarget(kind="gate"))
    test: EncodingTarget = field(default_factory=lambda: EncodingTarget(kind="test"))
    cron_body: EncodingTarget = field(
        default_factory=lambda: EncodingTarget(kind="cron_body")
    )
    manifest_entry: EncodingTarget = field(
        default_factory=lambda: EncodingTarget(kind="manifest_entry")
    )

    def targets(self) -> list[EncodingTarget]:
        return [self.law_file, self.gate, self.test, self.cron_body, self.manifest_entry]


# Targets that put the lesson in executable machine surface (not just prose).
MACHINE_TARGETS = {"law_file", "gate", "cron_body", "manifest_entry"}


@dataclass
class Lesson:
    lesson_id: str
    title: str
    teacher: str
    source: str  # where the teaching entered from (chat, feed, smart note, ...)
    taught_at: str  # ISO-8601 UTC
    raw_teaching: str
    stage: str = Stage.CAPTURED.value
    ib: dict | None = None
    encoding: dict | None = None
    check: dict | None = None  # {"kind": "python"|"shell", "name"/"cmd": ...}
    re_tells: int = 0
    bug_refs: list = field(default_factory=list)
    history: list = field(default_factory=list)  # append-only stage transitions

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Lesson":
        return cls(**d)

    def log(self, event: str) -> None:
        self.history.append(event)

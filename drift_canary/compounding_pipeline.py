"""Compounding Intelligence Pipeline (spec).

Shawn's canonical 10-stage process (The_compounding_process.svg):
EXPERIENCE → CAPTURE → UNDERSTAND → QUALIFY → RETRIEVE → APPLY
→ MEASURE → VERIFY → PROMOTE → COLD_REUSE

MEASURE stage encodes the experiment-outcomes property (Shawn's chart):
a correct lesson must outperform control, and a wrong lesson must
underperform control. Per ratified SN-042 (Epistemic Calibration Law):
"For strong learning claims, use a control without the lesson and
treatment with the lesson when feasible. Add an adversarial
wrong/malicious-memory arm for high-value learning/security tests."

VERIFY requires independent causal evidence — per process_smart_flow.svg,
repetition within one evidence family (Naya 2 summary + Naya 5 evaluation
of the same unverified claim A) does NOT qualify. Only an independent
observation B (separate measurement or authoritative source) breaks the
single-family trap.

PROMOTE issues an interaction proof receipt per the System Intelligence
Review: interaction_id, participants, invariant, preconditions,
environment, proof (positive/negative/independent), qualification.

COLD_REUSE: a successor must independently reconstruct which components
passed, which interaction failed, which repair was verified.

Guards (from Process_flow.svg — the self-reinforcing error loop):
a claim that was captured but never independently verified must NOT be
promoted merely because multiple agents repeated it (anti-citogenesis).

SPEC ONLY. Not wired into kernel/, KNOW, LAW, ACT, or any live path.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Stage(Enum):
    EXPERIENCE = "EXPERIENCE"
    CAPTURE = "CAPTURE"
    UNDERSTAND = "UNDERSTAND"
    QUALIFY = "QUALIFY"
    RETRIEVE = "RETRIEVE"
    APPLY = "APPLY"
    MEASURE = "MEASURE"
    VERIFY = "VERIFY"
    PROMOTE = "PROMOTE"
    COLD_REUSE = "COLD_REUSE"


PIPELINE_ORDER = tuple(Stage)


class MeasureVerdict(Enum):
    LESSON_IMPROVES = "LESSON_IMPROVES"      # treatment > control > wrong
    LESSON_NEUTRAL = "LESSON_NEUTRAL"        # no meaningful difference
    LESSON_HARMS = "LESSON_HARMS"            # treatment < control
    INCONCLUSIVE = "INCONCLUSIVE"            # ordering violated / data bad


class EvidenceFamily(Enum):
    """Per process_smart_flow.svg: which family does evidence belong to?"""
    SAME_FAMILY = "SAME_FAMILY"              # repetition of claim A
    INDEPENDENT_OBSERVATION = "INDEPENDENT_OBSERVATION"  # observation B


@dataclass(frozen=True)
class ExperimentArms:
    """Control / treatment / wrong-lesson arms for the MEASURE stage."""
    control_rate: float        # no lesson
    treatment_rate: float      # correct lesson applied
    wrong_lesson_rate: float   # adversarial wrong lesson
    # Minimum meaningful separation (avoids noise-driven promotion)
    min_separation: float = 0.05


@dataclass(frozen=True)
class ProofReceipt:
    """Interaction proof receipt (System Intelligence Review §8)."""
    interaction_id: str
    participants: tuple
    invariant: str
    preconditions: tuple
    environment_sha: str
    positive_test: str
    negative_test: str
    independent_verification: str  # receipt id or "PENDING"
    qualification: str = "NOT_YET_ESTABLISHED"


@dataclass
class PipelineState:
    """Mutable traversal state through the 10 stages."""
    stage: Stage = Stage.EXPERIENCE
    history: list = field(default_factory=list)
    blocked_reason: Optional[str] = None

    def advance(self) -> None:
        idx = PIPELINE_ORDER.index(self.stage)
        self.history.append(self.stage)
        if idx + 1 < len(PIPELINE_ORDER):
            self.stage = PIPELINE_ORDER[idx + 1]

    def block(self, reason: str) -> None:
        self.blocked_reason = reason


def measure_lesson(arms: ExperimentArms) -> MeasureVerdict:
    """MEASURE stage: control vs treatment vs wrong lesson.

    Shawn's chart property: correct lesson > control > wrong lesson.
    Per the System Intelligence Review: "For a claim that learning
    improves outcomes, include a comparable control without the lesson
    and a treatment with the lesson. Where meaningful, include a
    wrong-lesson condition. Otherwise, demonstrating that the lesson
    passed through the system does not establish causal improvement."
    """
    c, t, w = arms.control_rate, arms.treatment_rate, arms.wrong_lesson_rate
    s = arms.min_separation

    # Guard: rates must be valid probabilities
    for r in (c, t, w):
        if not (0.0 <= r <= 1.0):
            return MeasureVerdict.INCONCLUSIVE

    # The canonical ordering: treatment beats control by margin,
    # control beats wrong-lesson by margin.
    if t - c >= s and c - w >= s:
        return MeasureVerdict.LESSON_IMPROVES
    if c - t >= s:
        return MeasureVerdict.LESSON_HARMS
    if abs(t - c) < s and abs(c - w) < s:
        return MeasureVerdict.LESSON_NEUTRAL
    # Ordering violated (e.g. wrong beats control): data suspect
    return MeasureVerdict.INCONCLUSIVE


def verify_independent(evidence: list[EvidenceFamily]) -> bool:
    """VERIFY stage: independent causal evidence required.

    Per process_smart_flow.svg: Naya 2's summary + Naya 5's evaluation
    of the same unverified claim A is still ONE evidence family.
    Only an INDEPENDENT_OBSERVATION (separate measurement or
    authoritative source) qualifies. Per AGENTS.md anti-citogenesis:
    internal repetition is not independent corroboration.
    """
    return EvidenceFamily.INDEPENDENT_OBSERVATION in evidence


def self_reinforcing_error_guard(
    repeat_count: int,
    independent_evidence: bool,
) -> bool:
    """Guard from Process_flow.svg: the self-reinforcing error loop.

    A claim that has been captured and repeated by N agents but never
    independently verified must NOT be promoted. Returns True if the
    pipeline must BLOCK (error loop detected), False if safe to continue.
    """
    # Repeated without independent evidence = the loop in the diagram
    # (CAPTURE → RETRIEVAL → SELF-EVALUATION → FALSE PROMOTION)
    return repeat_count >= 2 and not independent_evidence


def run_pipeline(
    arms: ExperimentArms,
    evidence: list[EvidenceFamily],
    repeat_count: int = 0,
) -> tuple[PipelineState, Optional[MeasureVerdict]]:
    """Run the full 10-stage pipeline. Returns final state + measure verdict.

    Blocks at MEASURE if the lesson doesn't improve, at VERIFY if no
    independent evidence, and immediately if the self-reinforcing
    error guard fires.
    """
    state = PipelineState()

    # Guard first: never promote a self-reinforced claim
    if self_reinforcing_error_guard(repeat_count, verify_independent(evidence)):
        state.block("self-reinforcing error loop: repeated without independent evidence")
        return state, None

    # Advance through EXPERIENCE..APPLY (stages 1-6 assumed satisfied by caller)
    for _ in range(6):
        state.advance()
    assert state.stage == Stage.MEASURE

    verdict = measure_lesson(arms)
    if verdict != MeasureVerdict.LESSON_IMPROVES:
        state.block(f"MEASURE failed: {verdict.value} — lesson does not causally improve")
        return state, verdict
    state.advance()  # → VERIFY

    if not verify_independent(evidence):
        state.block("VERIFY failed: no independent observation (single evidence family)")
        return state, verdict
    state.advance()  # → PROMOTE
    state.advance()  # → COLD_REUSE

    return state, verdict

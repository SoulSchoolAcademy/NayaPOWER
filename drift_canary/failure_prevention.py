"""Failure-to-Prevention Acceptance Contract (spec).

Source: The Mirror (100 failures, 100 solutions, 10 families, 2026-10-10).
Recommendation implemented: build the Acceptance Contract FIRST.

This is the contract definition — the framework that future repairs plug
into. It is NOT the implementation of all 100 solutions.

The contract defines:
1. Failure taxonomy (10 families, failures 01-100)
2. Canonical failure record fields
3. The 8-step failure-to-improvement loop as executable checks
4. Prioritization classes A/B/C/D
5. Binding to existing systems (Constitution, value_calculus, duplicate_detector,
   learning_evidence_ladder, Smart Note pipeline) — no duplication

SPEC ONLY. Not wired into kernel/, KNOW, LAW, ACT, or any live path.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# 1. FAILURE TAXONOMY — 10 families from the Mirror
# ---------------------------------------------------------------------------

class FailureFamily(Enum):
    """The 10 failure families. Each covers 10 numbered failures."""
    F1_UNDERSTANDING = "F1"       # 01-10: does not correctly understand the job
    F2_TRUTH = "F2"               # 11-20: cannot distinguish true from plausible
    F3_REASONING = "F3"           # 21-30: has information, reaches poor conclusion
    F4_PLANNING = "F4"           # 31-40: works hard, not on the most valuable thing
    F5_TOOL_USE = "F5"           # 41-50: knows what to do, executes incorrectly
    F6_VERIFICATION = "F6"       # 51-60: produces something, cannot prove it works
    F7_MEMORY = "F7"             # 61-70: solves problems, fails to benefit later
    F8_ALIGNMENT = "F8"          # 71-80: crosses a boundary that should not be crossed
    F9_COMMUNICATION = "F9"      # 81-90: correct work, difficult to understand/use
    F10_IMPROVEMENT = "F10"      # 91-100: fails to convert experience into improvement


# Keyword anchors for classification. Each family maps to characteristic
# signals in a failure description. First match wins; order reflects the
# Mirror's family precedence (safety/authority signals checked first).
_FAMILY_KEYWORDS: dict[FailureFamily, tuple[str, ...]] = {
    FailureFamily.F8_ALIGNMENT: (
        "authority", "permission", "unauthorized", "privacy", "consent",
        "safety", "harmful", "malicious", "leak", "irreversible",
        "fabricat", "identity", "boundary", "bypass",
    ),
    FailureFamily.F2_TRUTH: (
        "hallucinat", "invent", "fabricat", "false claim", "unsupported",
        "stale evidence", "confidence", "unknown", "plausible",
        "citation", "corroborat",
    ),
    FailureFamily.F6_VERIFICATION: (
        "not test", "no test", "unverif", "mock", "regression",
        "handoff", "acceptance", "proof", "production",
    ),
    FailureFamily.F1_UNDERSTANDING: (
        "misunderst", "ambigu", "wrong format", "requirement",
        "intent", "literal", "assum",
    ),
    FailureFamily.F3_REASONING: (
        "edge case", "correlation", "causation", "contradict",
        "alternative", "scoring", "uncertainty",
    ),
    FailureFamily.F4_PLANNING: (
        "priorit", "mission", "urgency", "dependenc", "stop condition",
        "opportunity cost",
    ),
    FailureFamily.F5_TOOL_USE: (
        "tool", "argument", "retry", "permission denied", "stale branch",
        "wrong file", "partial",
    ),
    FailureFamily.F7_MEMORY: (
        "memory", "lesson", "context", "successor", "stale lesson",
        "forget", "relearn",
    ),
    FailureFamily.F9_COMMUNICATION: (
        "unclear", "verbose", "terse", "terminology", "escalat",
        "question", "report",
    ),
    FailureFamily.F10_IMPROVEMENT: (
        "repeat", "recur", "same mistake", "symptom", "rebuild",
        "metric", "regress", "transfer",
    ),
}


def classify_failure(description: str) -> FailureFamily:
    """Map a failure description to its primary family (1-10).

    Keyword-anchored, deterministic. F8 (alignment/safety) is checked
    first: a safety signal anywhere in the description takes precedence,
    per the Mirror's Class A hard-boundary rule.
    Returns F6_VERIFICATION as the default when no signal matches —
    an unclassifiable failure is itself a verification gap.
    """
    text = description.lower()
    for family, keywords in _FAMILY_KEYWORDS.items():
        if any(k in text for k in keywords):
            return family
    return FailureFamily.F6_VERIFICATION


# ---------------------------------------------------------------------------
# 2. CANONICAL FAILURE RECORD FIELDS (Mirror §4)
# ---------------------------------------------------------------------------

class RecordState(Enum):
    """Lifecycle states of a failure record."""
    OBSERVED = "OBSERVED"
    DIAGNOSED = "DIAGNOSED"
    REPAIR_CANDIDATE = "REPAIR_CANDIDATE"
    VERIFIED = "VERIFIED"
    BEHAVIORALLY_PROVEN = "BEHAVIORALLY_PROVEN"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class FailureRecord:
    """Canonical failure record. Every material failure gets one.

    Fields per Mirror §4. Immutable: updates create a new record with
    supersedes pointing at the prior one (provenance preserved).
    """
    # What should have happened?
    expected_behavior: str
    # What happened, supported by evidence?
    actual_behavior: str
    # Which of the 100 families (primary root cause)?
    failure_family: FailureFamily
    # Why did the system fail? (distinct from the visible symptom)
    root_cause: str
    # Which task, tool result, source, code version produced the finding?
    evidence_provenance: str
    # What will stop or detect recurrence?
    prevention_control: str = ""
    # What must pass for the repair to be accepted?
    acceptance_test: str = ""
    # Does the repair transfer to future tasks?
    behavioral_test: str = ""
    # Which existing file, mechanism, or governed contract owns the fix?
    canonical_owner: str = ""
    # Lifecycle state
    state: RecordState = RecordState.OBSERVED
    # Has this failure class occurred before, under what conditions?
    recurrence: str = ""
    # Prior record this one supersedes (empty for first observation)
    supersedes: str = ""
    # Contributing families beyond the primary (comma-separated family codes)
    contributing_families: str = ""


# ---------------------------------------------------------------------------
# 3. THE 8-STEP LOOP as executable state checks
# ---------------------------------------------------------------------------

class LoopStep(Enum):
    """The 8 steps of the failure-to-improvement loop."""
    OBSERVE = "OBSERVE"
    DIAGNOSE = "DIAGNOSE"
    PRIORITIZE = "PRIORITIZE"
    REPAIR = "REPAIR"
    VERIFY = "VERIFY"
    INTERNALIZE = "INTERNALIZE"
    PROVE_TRANSFER = "PROVE_TRANSFER"
    FREEZE_MEASURE_REPEAT = "FREEZE_MEASURE_REPEAT"


# Each step's entry requirement: the record fields that must be non-empty
# before the step can begin. The contract at every transition.
_STEP_REQUIREMENTS: dict[LoopStep, tuple[str, ...]] = {
    LoopStep.OBSERVE: ("expected_behavior", "actual_behavior", "evidence_provenance"),
    LoopStep.DIAGNOSE: ("failure_family", "root_cause"),
    LoopStep.PRIORITIZE: (),  # prioritization reads the diagnosis; no new fields
    LoopStep.REPAIR: ("prevention_control", "canonical_owner"),
    LoopStep.VERIFY: ("acceptance_test",),
    LoopStep.INTERNALIZE: (),  # preservation via Smart Note pipeline
    LoopStep.PROVE_TRANSFER: ("behavioral_test",),
    LoopStep.FREEZE_MEASURE_REPEAT: ("recurrence",),
}

_STEP_ORDER: tuple[LoopStep, ...] = tuple(LoopStep)


def step_ready(record: FailureRecord, step: LoopStep) -> tuple[bool, tuple[str, ...]]:
    """Check whether a record satisfies a loop step's entry requirements.

    Returns (ready, missing_fields). A step cannot begin until its
    requirements are met — this is the contract at every transition.
    """
    missing = tuple(
        f for f in _STEP_REQUIREMENTS[step] if not getattr(record, f)
    )
    return (len(missing) == 0, missing)


def next_step(record: FailureRecord) -> Optional[LoopStep]:
    """Return the next loop step the record is ready for, or None if done.

    Steps must be taken in order. A record that satisfies every step's
    requirements through PROVE_TRANSFER is ready for FREEZE_MEASURE_REPEAT.
    """
    for step in _STEP_ORDER:
        ready, _ = step_ready(record, step)
        if not ready:
            return step
    return None  # all steps satisfied


# ---------------------------------------------------------------------------
# 4. PRIORITIZATION CLASSES A/B/C/D (Mirror §5)
# ---------------------------------------------------------------------------

class PriorityClass(Enum):
    """Repair priority classes. Hard boundaries first, always."""
    A_HARD_BOUNDARY = "A"   # safety, privacy, authority, consent, fabricated proof
    B_RECURRENT = "B"       # known mistakes happening repeatedly
    C_HIGH_LEVERAGE = "C"   # prevents multiple families at once
    D_UNCERTAIN = "D"       # investigate cheaply before repairing


def prioritize(
    family: FailureFamily,
    is_recurrent: bool = False,
    spans_multiple_families: bool = False,
    cause_established: bool = True,
) -> PriorityClass:
    """Assign a priority class per Mirror §5.

    Precedence (first match wins):
    1. F8 alignment/safety failures are ALWAYS Class A — a high value
       score can never make a prohibited repair admissible.
    2. Recurrent failures are Class B — repair the shared cause.
    3. Multi-family leverage is Class C — one control, many failures.
    4. Unestablished cause is Class D — investigate before repairing.
    5. Default is Class C (single-family, established cause, not recurrent).
    """
    if family == FailureFamily.F8_ALIGNMENT:
        return PriorityClass.A_HARD_BOUNDARY
    if is_recurrent:
        return PriorityClass.B_RECURRENT
    if spans_multiple_families:
        return PriorityClass.C_HIGH_LEVERAGE
    if not cause_established:
        return PriorityClass.D_UNCERTAIN
    return PriorityClass.C_HIGH_LEVERAGE


# ---------------------------------------------------------------------------
# 5. ACCEPTANCE CONTRACT — validate that a repair is complete
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ContractResult:
    """Result of validating a repair against the acceptance contract."""
    accepted: bool
    missing: tuple[str, ...]
    # Human-readable reason, suitable for posting to the team feed
    reason: str


# Every accepted repair must have these elements. No exceptions.
_CONTRACT_REQUIRED: tuple[str, ...] = (
    "prevention_control",   # what stops or detects recurrence
    "acceptance_test",      # what must pass for the repair to be accepted
    "behavioral_test",      # does the repair transfer to future tasks
    "canonical_owner",      # which existing mechanism owns the fix
    "evidence_provenance",  # what produced the finding
)


def acceptance_contract(record: FailureRecord) -> ContractResult:
    """Validate that a repair satisfies the acceptance contract.

    A repair is accepted only when ALL required elements are present:
    - prevention_control: the mechanism, not just an explanation
    - acceptance_test: the bar the repair must clear
    - behavioral_test: proof the lesson transfers (not just memorized)
    - canonical_owner: bound to an existing system, not a new brain
    - evidence_provenance: the finding is traceable

    Writing down an explanation is not a repair. One passing test is not
    a permanent law. A retained lesson without behavioral evidence is not
    learned. The contract enforces all three.
    """
    missing = tuple(f for f in _CONTRACT_REQUIRED if not getattr(record, f))
    if missing:
        return ContractResult(
            accepted=False,
            missing=missing,
            reason=(
                f"Repair rejected: missing {', '.join(missing)}. "
                "An explanation is not a repair; add the missing elements."
            ),
        )
    return ContractResult(
        accepted=True,
        missing=(),
        reason="Repair accepted: control, tests, owner, and provenance all present.",
    )


# ---------------------------------------------------------------------------
# 6. BINDING TO EXISTING SYSTEMS (no duplication)
# ---------------------------------------------------------------------------

# Canonical bindings. The contract REUSES these systems; it does not
# reimplement them. Each binding names the system and its responsibility.
SYSTEM_BINDINGS: dict[str, str] = {
    "authority_safety": (
        "Constitution (Team Naya Operating Protocol): truth, authority, "
        "safety, proof, and learning boundaries. Class A hard gates live here."
    ),
    "prioritization_math": (
        "kernel/value_calculus.py (V2.1): the canonical decision mathematics. "
        "Failure prevention reuses it; no competing scorecards."
    ),
    "duplicate_prevention": (
        "tools/duplicate_detector.py + tools/solved_problem_registry.json: "
        "check before building any new prevention mechanism."
    ),
    "behavioral_proof": (
        "tools/learning_evidence_ladder.py: the route for testing whether a "
        "retained lesson actually changes behavior (held-out tasks, controls)."
    ),
    "lesson_preservation": (
        "Smart Note pipeline (.naya/capture/): durable, provenance-bearing "
        "preservation. The failure record feeds it; it does not replace it."
    ),
}


def binding_for(responsibility: str) -> Optional[str]:
    """Return the canonical system binding for a responsibility, if one exists.

    Use this before building anything new. If a binding exists, extend the
    existing system. If none exists, the repair may define a new mechanism —
    but it must still name a canonical_owner in the failure record.
    """
    return SYSTEM_BINDINGS.get(responsibility)

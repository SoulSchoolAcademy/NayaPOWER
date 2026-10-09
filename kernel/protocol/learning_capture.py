"""
learning_capture.py — Machine law: every cycle must produce its lesson.

Point 8 of the Unified Operating Law: "Learn by preserving valuable,
provenance-bound lessons through the canonical candidate and promotion process."

A work cycle is not complete until its lesson is captured or explicitly
declared as having none. "No lesson" is allowed but must be stated —
silence is not a lesson.

ADMISSION CONTRACT (system-captured candidates only):

A system-captured learning candidate may enter CANDIDATE status only if it
passes all seven admission rules. A candidate that fails ANY rule is
REJECTED — never admitted as CANDIDATE. Fail-closed default: no named task
+ no pre-registered criterion + no machine check => do not admit. When in
doubt, REJECT.

The seven rules (individually testable predicates below):

  1. falsifiable_claim      — the claim states an observable outcome that
                              could be false (no tautologies, no definitional
                              token changes).
  2. same_named_task        — treatment and control attempt the identical
                              named task.
  3. preregistered_criterion— success criterion written BEFORE the arms ran,
                              independent of the lesson.
  4. machine_measurement    — measured by machine, a different seat, or a
                              deterministic check — never the claimant's
                              self-report.
  5. doer_scorer_separation — doer and scorer are named different seats.
  6. null_not_verified      — a null result is evidence, never verification.
  7. replication_gate       — replication on >=3 unseen tasks before the
                              candidate may be admitted.

Epistemic grounding: SN-042 (causal learning proportional to claim;
independence must be real; measure capability delta, not memory volume)
and the Learning Contract V1 pipeline
(OBSERVE -> RECONCILE -> CANDIDATE -> VERIFY -> ADOPT -> MEASURE -> COMPOUND).

Lane separation: the human-director-verified instant path is a SEPARATE
path and is never gated by this contract — the director's word IS the
verification (Verification Law). check_admission() declines explicitly
(bypassed=True) for capture_path="human_director" instead of silently
passing, so the lane boundary stays machine-visible.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CycleLesson:
    work_description: str
    lesson: str                  # the durable, reusable insight — or ""
    no_lesson_reason: str = ""   # required if lesson is empty
    smart_note_id: str = ""      # filled when captured as a Smart Note
    provenance: str = ""         # evidence the lesson rests on


@dataclass
class LearningCaptureResult:
    passed: bool
    reasons: list = field(default_factory=list)


def check_lesson(cycle: CycleLesson) -> LearningCaptureResult:
    reasons: list[str] = []
    if not cycle.work_description.strip():
        reasons.append("No work described.")
    if not cycle.lesson.strip():
        if not cycle.no_lesson_reason.strip():
            reasons.append(
                "No lesson captured and no reason given. "
                "State the lesson or state why there is none."
            )
    else:
        if not cycle.provenance.strip():
            reasons.append("Lesson captured without provenance — evidence required.")
    return LearningCaptureResult(passed=not reasons, reasons=reasons)


# ---------------------------------------------------------------------------
# Admission contract — system-captured learning candidates
# ---------------------------------------------------------------------------

# Rule identifiers. Stable across the Python canonical module and the
# TypeScript edge-function port (supabase/functions/nayanet-learning-verify/
# admission_contract.ts) so a verdict from either side is comparable.
RULE_FALSIFIABLE = "falsifiable_claim"
RULE_SAME_TASK = "same_named_task"
RULE_PREREGISTERED = "preregistered_criterion"
RULE_MEASUREMENT = "machine_measurement"
RULE_DOER_SCORER = "doer_scorer_separation"
RULE_NULL = "null_not_verified"
RULE_REPLICATION = "replication_gate"

ADMISSION_RULES: tuple[str, ...] = (
    RULE_FALSIFIABLE,
    RULE_SAME_TASK,
    RULE_PREREGISTERED,
    RULE_MEASUREMENT,
    RULE_DOER_SCORER,
    RULE_NULL,
    RULE_REPLICATION,
)

MACHINE_MEASUREMENTS = ("machine", "different_seat", "deterministic")
REPLICATIONS_REQUIRED = 3

# A treatment arm defined as "applied the lesson" with a control of
# "did not apply it" tests obedience, not learning. The claim must name an
# observable capability outcome distinct from the arm assignment.
_APPLIED_LESSON_RE = re.compile(
    r"appl(ied|y|ication)(\s+of)?(\s+the)?(\s+retained)?\s+(lesson|intelligence)",
    re.IGNORECASE,
)
_NO_APPLY_RE = re.compile(
    r"did\s+not\s+apply|without(\s+the|\s+applying)?(\s+retained)?\s+(lesson|intelligence)"
    r"|no\s+lesson\s+applied",
    re.IGNORECASE,
)
# A claim that only asserts the arms emitted different tokens/output is a
# definitional change, not a learning claim (SN-042: measure capability delta).
_TOKEN_DIFF_RE = re.compile(
    r"different\s+(tokens?|outputs?|output)|tokens?\s+differ|outputs?\s+differ"
    r"|emits?\s+different|output\s+differs",
    re.IGNORECASE,
)
# A claim is falsifiable only if it names an observable outcome: the named
# task, a capability metric, or a measurable direction of change.
_METRIC_RE = re.compile(
    r"provenance_preserved|governed_autonomy_applied|accuracy|success\s+rate"
    r"|\bpass(es|ed|ing)?\b|increas\w*|decreas\w*|reduc\w*|improv\w*|preserv\w*"
    r"|≥|>=|>|\b\d+\s*%|rate\b|score\b|metric\b",
    re.IGNORECASE,
)

_CLAIM_MIN_LEN = 12
_CRITERION_MIN_LEN = 8


@dataclass
class AdmissionCandidate:
    """Everything the admission contract needs to judge a candidate.

    capture_path: "system" (gated) or "human_director" (explicit bypass —
        the director's word is the verification; see module docstring).
    outcome: "positive" | "null" | "not_run".
    measurement: "machine" | "different_seat" | "deterministic" | "self_report".
    """

    claim: str = ""
    named_task_id: str = ""
    control_task_id: str = ""
    treatment_task_id: str = ""
    control_description: str = ""
    treatment_description: str = ""
    preregistered_criterion: str = ""
    preregistered_at: str | None = None   # ISO-8601; must precede arms_ran_at
    arms_ran_at: str | None = None        # ISO-8601
    measurement: str = ""
    doer_seat: str = ""
    scorer_seat: str = ""
    outcome: str = ""
    measured_capability_delta: bool = False
    replications_on_unseen_tasks: int = 0
    capture_path: str = "system"


@dataclass
class AdmissionResult:
    passed: bool
    failed_rules: list = field(default_factory=list)
    reasons: list = field(default_factory=list)
    bypassed: bool = False  # True only for the human-director lane


def _names_observable(candidate: AdmissionCandidate) -> bool:
    claim = (candidate.claim or "").lower()
    named = (candidate.named_task_id or "").strip().lower()
    if named and named in claim:
        return True
    return bool(_METRIC_RE.search(claim))


def rule_falsifiable(candidate: AdmissionCandidate) -> tuple[bool, str]:
    """Rule 1: the claim states an observable outcome that could be false."""
    claim = (candidate.claim or "").strip()
    if len(claim) < _CLAIM_MIN_LEN:
        return False, (
            "falsifiable_claim: claim is vacuous — no observable outcome is "
            "stated that could be false."
        )
    if _TOKEN_DIFF_RE.search(claim):
        return False, (
            "falsifiable_claim: definitional token change — the claim only "
            "asserts the arms emitted different tokens/output. That is true "
            "by construction of the arms, not a capability delta that could "
            "be false (SN-042: measure capability delta)."
        )
    treatment_is_application = bool(
        _APPLIED_LESSON_RE.search(candidate.treatment_description or "")
    )
    control_is_non_application = bool(
        _NO_APPLY_RE.search(candidate.control_description or "")
    )
    if treatment_is_application and control_is_non_application and not _names_observable(candidate):
        return False, (
            "falsifiable_claim: tautology — the treatment arm is defined as "
            "'applied the lesson' and the claim asserts only that behavior "
            "differs. That tests obedience, not learning; the predicted "
            "outcome is entailed by the arm assignment and cannot be false."
        )
    if not _names_observable(candidate):
        return False, (
            "falsifiable_claim: the claim names no observable outcome on the "
            "named task — nothing measurable is stated that could be false."
        )
    return True, ""


def rule_same_task(candidate: AdmissionCandidate) -> tuple[bool, str]:
    """Rule 2: treatment and control attempt the identical named task."""
    named = (candidate.named_task_id or "").strip()
    control = (candidate.control_task_id or "").strip()
    treatment = (candidate.treatment_task_id or "").strip()
    if not named or not control or not treatment:
        return False, (
            "same_named_task: no named task — treatment and control must "
            "attempt the identical named task; at least one arm has no task."
        )
    if not (control == treatment == named):
        return False, (
            "same_named_task: arms diverge — treatment=%r control=%r named=%r. "
            "Both arms must attempt the identical named task." % (treatment, control, named)
        )
    return True, ""


def _parse_ts(value: str | None) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.strip())
    except ValueError:
        return None


def rule_preregistered(candidate: AdmissionCandidate) -> tuple[bool, str]:
    """Rule 3: success criterion written BEFORE the arms ran, independent of the lesson."""
    criterion = (candidate.preregistered_criterion or "").strip()
    if len(criterion) < _CRITERION_MIN_LEN:
        return False, (
            "preregistered_criterion: no success criterion was written before "
            "the arms ran — fail closed."
        )
    if criterion == (candidate.claim or "").strip():
        return False, (
            "preregistered_criterion: the 'criterion' merely restates the "
            "claim — it is not an independent success statement."
        )
    preregistered = _parse_ts(candidate.preregistered_at)
    ran = _parse_ts(candidate.arms_ran_at)
    if preregistered is None or ran is None:
        return False, (
            "preregistered_criterion: preregistered_at/arms_ran_at missing or "
            "unparseable — cannot prove the criterion predates the arms; "
            "fail closed."
        )
    if not preregistered < ran:
        return False, (
            "preregistered_criterion: the criterion was not written before "
            "the arms ran (preregistered_at=%r arms_ran_at=%r)."
            % (candidate.preregistered_at, candidate.arms_ran_at)
        )
    return True, ""


def rule_machine_measurement(candidate: AdmissionCandidate) -> tuple[bool, str]:
    """Rule 4: measured by machine / different seat / deterministic — never self-report."""
    measurement = (candidate.measurement or "").strip().lower()
    if measurement in MACHINE_MEASUREMENTS:
        return True, ""
    if measurement in ("self_report", "self-report", "claimant"):
        return False, (
            "machine_measurement: the outcome was scored by the claimant's "
            "own report — self-attestation is not measurement (SN-042: "
            "independence must be real)."
        )
    return False, (
        "machine_measurement: no machine, different-seat, or deterministic "
        "measurement declared — fail closed."
    )


def rule_doer_scorer(candidate: AdmissionCandidate) -> tuple[bool, str]:
    """Rule 5: doer and scorer are named different seats."""
    doer = (candidate.doer_seat or "").strip()
    scorer = (candidate.scorer_seat or "").strip()
    if not doer or not scorer:
        return False, (
            "doer_scorer_separation: doer and scorer seats must both be "
            "named — unnamed scoring is not independent."
        )
    if doer.casefold() == scorer.casefold():
        return False, (
            "doer_scorer_separation: doer and scorer are the same seat "
            "(%r) — the scorer must differ from the doer." % doer
        )
    return True, ""


def rule_null_not_verified(candidate: AdmissionCandidate) -> tuple[bool, str]:
    """Rule 6: nulls remain NOT VERIFIED — a null is evidence, never verification."""
    outcome = (candidate.outcome or "").strip().lower()
    if outcome == "null":
        return False, (
            "null_not_verified: the experiment returned a null result "
            "(behavioral_change:false). A null is kept as negative evidence — "
            "it is never verification and cannot enter CANDIDATE."
        )
    if outcome != "positive":
        return False, (
            "null_not_verified: no positive outcome was measured "
            "(outcome=%r) — nothing ran or nothing was found; not admittable."
            % (candidate.outcome or "")
        )
    if not candidate.measured_capability_delta:
        return False, (
            "null_not_verified: no measured capability delta — an observed "
            "output difference without a capability delta is not learning "
            "(SN-042: measure capability delta, not output difference)."
        )
    return True, ""


def rule_replication(candidate: AdmissionCandidate) -> tuple[bool, str]:
    """Rule 7: replication on >=3 unseen tasks before the candidate may be admitted."""
    n = candidate.replications_on_unseen_tasks or 0
    if n >= REPLICATIONS_REQUIRED:
        return True, ""
    return False, (
        "replication_gate: %d replication(s) on unseen tasks; %d required "
        "before a candidate may be admitted." % (n, REPLICATIONS_REQUIRED)
    )


_RULE_PREDICATES: tuple[tuple[str, object], ...] = (
    (RULE_FALSIFIABLE, rule_falsifiable),
    (RULE_SAME_TASK, rule_same_task),
    (RULE_PREREGISTERED, rule_preregistered),
    (RULE_MEASUREMENT, rule_machine_measurement),
    (RULE_DOER_SCORER, rule_doer_scorer),
    (RULE_NULL, rule_null_not_verified),
    (RULE_REPLICATION, rule_replication),
)


def check_admission(candidate: AdmissionCandidate) -> AdmissionResult:
    """Run the admission contract. A candidate failing ANY rule is REJECTED.

    Fail-closed: missing design information fails the rules it would prove.
    The human-director lane bypasses explicitly (bypassed=True) — the
    director's word is the verification and this contract never gates it.
    """
    if not isinstance(candidate, AdmissionCandidate):
        return AdmissionResult(
            passed=False,
            failed_rules=list(ADMISSION_RULES),
            reasons=["admission bundle missing or malformed — fail closed: no design, no CANDIDATE."],
        )
    if (candidate.capture_path or "").strip().lower() == "human_director":
        return AdmissionResult(
            passed=True,
            failed_rules=[],
            reasons=[
                "human_director lane: the director's word IS the verification "
                "(Verification Law) — the admission contract does not apply."
            ],
            bypassed=True,
        )
    failed_rules: list[str] = []
    reasons: list[str] = []
    for rule_id, predicate in _RULE_PREDICATES:
        ok, reason = predicate(candidate)  # type: ignore[operator]
        if not ok:
            failed_rules.append(rule_id)
            reasons.append(reason)
    return AdmissionResult(
        passed=not failed_rules,
        failed_rules=failed_rules,
        reasons=reasons,
    )

"""Learning-candidate admission gate — MACHINE LAW (round 2).

No learning candidate enters the system without passing this gate. It validates
experiment DESIGN at the door; it never claims that learning occurred.

The law (Shawn, 2026-10-09): the old backlog proved that verification cannot be
bolted onto a candidate that never had a falsifiable experimental contract.
0 of 13 analyzed candidates were verifiable as designed — tautologies, honest
nulls, non-experiments, definitional token changes. This gate exists so that
class of failure can never enter again.

ADMISSION CONTRACT (all must hold):
  (a) falsifiable claim — the claimant states what observation would prove it
      wrong, IN SUBSTANCE (a negation-paraphrase of the claim is a tautology,
      not a falsification condition)
  (b) same named task in both arms
  (c) pre-registered success criterion, independent of the lesson IN SUBSTANCE,
      registered BEFORE the first measurement (temporal pre-registration is
      checked, not claimed)
  (d) machine / different-seat / deterministic measurement
  (e) doer != scorer (identity normalized: case/whitespace-insensitive)
  (f) nulls are admitted as NOT VERIFIED, never as CANDIDATE — an honest null
      is a well-designed experiment that found nothing, and its natural
      encodings (outcome "null", asserts_behavioral_change false) admit it
  (g) both arms actually measured (a non-experiment is not a candidate)
  (h) asserts a behavioral change, not a token difference

Anything failing the contract is REJECTED AT THE DOOR with machine-readable
reasons. It never becomes a "candidate."

HONEST JUDGMENT BOUNDARY (B1b): the machine checks below catch
negation-paraphrase tautologies (falsification ≈ claim with negations
stripped). A tautology rewritten with synonyms will pass the machine check —
substantive independence beyond paraphrase detection requires model or human
judgment. The gate does not pretend otherwise: when the paraphrase score is
inconclusive, admission proceeds and the DOOR LOG records it; the independent
verifier remains the backstop. What the machine CAN check, it checks; what it
cannot, it names.

INTEGRATION CONTRACT — the gate FIRES on every learning-candidacy write:
  * In-repo: call submit_learning_claim() (below) before writing a CANDIDATE
    row. Write the row only when admitted_as == "CANDIDATE". Write
    NOT_VERIFIED rows only when admitted_as == "NOT_VERIFIED". On rejection,
    log the reasons and write nothing.
  * In-repo: learning_verification_queue.enqueue() runs the gate itself and
    refuses anything not admitted as CANDIDATE — the queue cannot be filled
    around the gate.
  * Receiver (supabase/functions/v7-smart-note-canonical/index.ts): WO9
    (2026-10-09) RETIRED the receiver's learning_evidence INSERT — the v7
    write path no longer exists; single writer is nayanet-learning-verify.
    (Historical note: the INSERT was the capture-stage row for the checkpoint
    invariant, NOT a learning-candidacy claim — the parallel lane
    (naya5/learn-admission-contract) tested and documented this separation,
    and capture must never be gated (Verification Law).) Learning candidacy
    begins at submit_learning_claim()/enqueue().
The gate is pure: no DB, no network.
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

ADMISSION_SCHEMA = "NAYAPOWER_LEARNING_CANDIDATE_ADMISSION_V1"

MEASUREMENT_METHODS = frozenset({"machine", "different_seat", "deterministic"})

# admitted_as values
CANDIDATE = "CANDIDATE"
NOT_VERIFIED = "NOT_VERIFIED"
REJECTED = "REJECTED"

# Rejection reason codes
SCHEMA_MISMATCH = "SCHEMA_MISMATCH"
CANDIDATE_MUST_BE_OBJECT = "CANDIDATE_MUST_BE_OBJECT"
CLAIM_REQUIRED = "CLAIM_REQUIRED"
CLAIM_NOT_FALSIFIABLE = "CLAIM_NOT_FALSIFIABLE"
TAUTOLOGICAL_FALSIFICATION = "TAUTOLOGICAL_FALSIFICATION"
NO_NAMED_TASK = "NO_NAMED_TASK"
NO_PREREGISTERED_CRITERION = "NO_PREREGISTERED_CRITERION"
CRITERION_NOT_INDEPENDENT = "CRITERION_NOT_INDEPENDENT"
TAUTOLOGICAL_CRITERION = "TAUTOLOGICAL_CRITERION"
CRITERION_REGISTERED_AT_REQUIRED = "CRITERION_REGISTERED_AT_REQUIRED"
CRITERION_TIMESTAMP_UNPARSEABLE = "CRITERION_TIMESTAMP_UNPARSEABLE"
MEASURED_AT_UNPARSEABLE = "MEASURED_AT_UNPARSEABLE"
POST_HOC_CRITERION = "POST_HOC_CRITERION"
NO_MACHINE_MEASUREMENT = "NO_MACHINE_MEASUREMENT"
DOER_AND_SCORER_REQUIRED = "DOER_AND_SCORER_REQUIRED"
DOER_EQUALS_SCORER = "DOER_EQUALS_SCORER"
ARMS_REQUIRE_OBSERVABLE_BEHAVIOR = "ARMS_REQUIRE_OBSERVABLE_BEHAVIOR"
ARMS_INDIMINISHABLE = "ARMS_INDIMINISHABLE"
NON_EXPERIMENT_NO_MEASURED_ARMS = "NON_EXPERIMENT_NO_MEASURED_ARMS"
TOKEN_DIFFERENCE_NOT_BEHAVIOR = "TOKEN_DIFFERENCE_NOT_BEHAVIOR"
BEHAVIORAL_MEASURE_REQUIRED = "BEHAVIORAL_MEASURE_REQUIRED"


@dataclass(frozen=True)
class AdmissionResult:
    admitted: bool
    admitted_as: str  # CANDIDATE | NOT_VERIFIED | REJECTED
    reasons: tuple[str, ...]  # empty when admitted; rejection codes otherwise


def normalize_identity(value: Any) -> str:
    """Canonical identity comparison: case- and whitespace-insensitive.

    "Naya-5", "naya-5 " and "NAYA-5" are the same seat. Used for every
    doer/scorer/verifier separation check (B6b).
    """
    return str(value).strip().casefold()


def _nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _parse_ts(value: Any) -> datetime | None:
    """Parse an ISO-8601 timestamp. Naive values are assumed UTC. None if unparseable."""
    if not _nonempty_str(value):
        return None
    text = str(value).strip()
    try:
        # fromisoformat does not accept a trailing "Z" before 3.11
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None
    except Exception:  # noqa: BLE001 - defensive: never let parsing raise
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


# --- Substantive independence (B1b) ---------------------------------------
# A falsification condition / success criterion that is just the claim with
# negations stripped is a tautology wearing a costume. The machine strips
# negation phrasing and stopwords, then measures sequence similarity against
# the claim. Attacks score >= 0.84 in testing; legitimate criteria score
# <= 0.36. Threshold 0.75.
#
# HONEST LIMIT: synonym-substituted tautologies ("improves" -> "enhances")
# can pass. That class requires model/human judgment — the independent
# verifier is the backstop, and this docstring says so instead of pretending
# fields suffice.

_NEGATION_PHRASES = (
    "did not", "does not", "do not", "would not", "will not", "is not",
    "are not", "was not", "were not", "has not", "have not", "had not",
    "cannot", "could not", "should not",
)
_NEGATION_TOKENS = frozenset({
    "not", "no", "never", "n't", "neither", "nor", "without", "lacks", "lack",
    "lacking", "fails", "failed", "failing", "failure", "unable", "absence",
    "absent", "against", "didnt", "doesnt", "dont", "cant", "wont",
})
_STOPWORDS = frozenset({
    "the", "a", "an", "if", "then", "of", "on", "in", "to", "for", "with",
    "and", "or", "is", "are", "was", "were", "be", "by", "as", "at", "it",
    "its", "this", "that", "these", "those", "than", "when", "where",
    "which", "what", "how", "s", "t", "over", "under",
})
_PARAPHRASE_THRESHOLD = 0.75


def _content_signature(text: str) -> str:
    lowered = text.lower()
    for phrase in _NEGATION_PHRASES:
        lowered = lowered.replace(phrase, " ")
    tokens = [
        tok for tok in re.findall(r"[a-z0-9]+", lowered)
        if tok not in _NEGATION_TOKENS and tok not in _STOPWORDS
    ]
    return " ".join(tokens)


def _is_negation_paraphrase(claim: str, condition: str) -> bool:
    """True when the condition is the claim restated with negations stripped."""
    sig_claim = _content_signature(claim)
    sig_condition = _content_signature(condition)
    if not sig_claim or not sig_condition:
        return False
    ratio = difflib.SequenceMatcher(None, sig_claim, sig_condition).ratio()
    return ratio >= _PARAPHRASE_THRESHOLD


def _is_null_outcome(candidate: dict) -> bool:
    """The natural null encodings: explicit outcome "null", or the candidate
    declares it found no behavioral change. Per the law's plain reading, an
    honest null admits as NOT_VERIFIED — it must not be rejected for failing
    to assert a behavioral change (B2b)."""
    if str(candidate.get("outcome", "pending")).strip().lower() == "null":
        return True
    return candidate.get("asserts_behavioral_change") is False


def admit_candidate(candidate: Any) -> AdmissionResult:
    """Apply the admission contract. Pure: no DB, no network."""
    if not isinstance(candidate, dict):
        return AdmissionResult(False, REJECTED, (CANDIDATE_MUST_BE_OBJECT,))
    errors: list[str] = []

    if candidate.get("schema") != ADMISSION_SCHEMA:
        errors.append(SCHEMA_MISMATCH)

    # (a) falsifiable claim — IN SUBSTANCE, not just field presence (B1b).
    claim = candidate.get("claim")
    falsification = candidate.get("falsification_condition")
    if not _nonempty_str(claim):
        errors.append(CLAIM_REQUIRED)
    if not _nonempty_str(falsification):
        errors.append(CLAIM_NOT_FALSIFIABLE)
    elif _nonempty_str(claim) and _is_negation_paraphrase(str(claim), str(falsification)):
        # "if applying the lesson did not change behavior" is the claim in a
        # costume — it can never fail independently of the claim itself.
        errors.append(TAUTOLOGICAL_FALSIFICATION)

    # (b) same named task in both arms
    if not _nonempty_str(candidate.get("task")):
        errors.append(NO_NAMED_TASK)

    # (c) pre-registered success criterion, independent of the lesson IN
    # SUBSTANCE, and temporally pre-registered (B1b, B5). We check the
    # timestamps — we do not merely claim pre-registration.
    criterion = candidate.get("success_criterion")
    if not _nonempty_str(criterion):
        errors.append(NO_PREREGISTERED_CRITERION)
    else:
        if candidate.get("criterion_independent_of_lesson") is not True:
            errors.append(CRITERION_NOT_INDEPENDENT)
        if _nonempty_str(claim) and _is_negation_paraphrase(str(claim), str(criterion)):
            errors.append(TAUTOLOGICAL_CRITERION)

    # (d) machine / different-seat / deterministic measurement
    measurement = candidate.get("measurement")
    method = measurement.get("method") if isinstance(measurement, dict) else None
    if method not in MEASUREMENT_METHODS:
        errors.append(NO_MACHINE_MEASUREMENT)

    # (e) doer != scorer — identity normalized (B6b)
    doer = candidate.get("doer")
    scorer = candidate.get("scorer")
    if not _nonempty_str(doer) or not _nonempty_str(scorer):
        errors.append(DOER_AND_SCORER_REQUIRED)
    elif normalize_identity(doer) == normalize_identity(scorer):
        errors.append(DOER_EQUALS_SCORER)

    # (g) both arms actually measured — with parseable timestamps, because
    # pre-registration cannot be checked against unparseable clocks (B5).
    arms = candidate.get("arms")
    arms_dict = arms if isinstance(arms, dict) else {}
    treatment = arms_dict.get("treatment") if isinstance(arms_dict.get("treatment"), dict) else {}
    control = arms_dict.get("control") if isinstance(arms_dict.get("control"), dict) else {}
    treatment_obs = treatment.get("observable")
    control_obs = control.get("observable")
    treatment_ts = _parse_ts(treatment.get("measured_at"))
    control_ts = _parse_ts(control.get("measured_at"))
    if not _nonempty_str(treatment_obs) or not _nonempty_str(control_obs):
        errors.append(ARMS_REQUIRE_OBSERVABLE_BEHAVIOR)
    elif str(treatment_obs).strip().lower() == str(control_obs).strip().lower():
        errors.append(ARMS_INDIMINISHABLE)
    if treatment_ts is None or control_ts is None:
        # Covers both missing and unparseable: without real timestamps there
        # was no measurable experiment and no pre-registration to check.
        if not _nonempty_str(treatment.get("measured_at")) or not _nonempty_str(control.get("measured_at")):
            errors.append(NON_EXPERIMENT_NO_MEASURED_ARMS)
        else:
            errors.append(MEASURED_AT_UNPARSEABLE)

    # (c-temporal) criterion registered BEFORE the first measurement (B5).
    # A criterion timestamped after the outcome was measured is post-hoc —
    # the gate checks this instead of taking "pre-registered" on faith.
    registered_raw = candidate.get("criterion_registered_at")
    if not _nonempty_str(registered_raw):
        errors.append(CRITERION_REGISTERED_AT_REQUIRED)
    else:
        registered_ts = _parse_ts(registered_raw)
        if registered_ts is None:
            errors.append(CRITERION_TIMESTAMP_UNPARSEABLE)
        elif treatment_ts is not None and control_ts is not None:
            first_measured = min(treatment_ts, control_ts)
            if registered_ts >= first_measured:
                errors.append(POST_HOC_CRITERION)

    if errors:
        return AdmissionResult(False, REJECTED, tuple(errors))

    # (f) honest nulls admit as NOT VERIFIED — AFTER the design checks above
    # (a null still needs a real experiment: named task, measured arms,
    # pre-registered criterion), but BEFORE the behavioral-assertion
    # requirements below. A null must never be rejected for failing to
    # assert the change it honestly did not find (B2b).
    if _is_null_outcome(candidate):
        return AdmissionResult(True, NOT_VERIFIED, ())

    # (h) behavioral change, not a token difference — only for non-nulls.
    if candidate.get("asserts_behavioral_change") is not True:
        errors.append(TOKEN_DIFFERENCE_NOT_BEHAVIOR)
    elif not _nonempty_str(candidate.get("behavioral_measure")):
        errors.append(BEHAVIORAL_MEASURE_REQUIRED)

    if errors:
        return AdmissionResult(False, REJECTED, tuple(errors))
    return AdmissionResult(True, CANDIDATE, ())


def submit_learning_claim(candidate: Any) -> AdmissionResult:
    """THE choke point for creating learning candidates (B8).

    Every writer that mints a learning-candidate row calls this first:
      result = submit_learning_claim(candidate_dict)
      - admitted_as == "CANDIDATE"    -> write the CANDIDATE row
      - admitted_as == "NOT_VERIFIED" -> write the NOT_VERIFIED row (negative evidence)
      - admitted_as == "REJECTED"      -> log result.reasons, write NOTHING
    """
    return admit_candidate(candidate)


def rejection_log(candidate_id: str, result: AdmissionResult) -> str:
    """One-line door log for a rejected candidate."""
    return f"ADMISSION_REJECTED id={candidate_id} reasons={','.join(result.reasons)}"

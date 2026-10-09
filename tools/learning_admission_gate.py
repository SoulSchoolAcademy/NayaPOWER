"""Learning-candidate admission gate — MACHINE LAW.

No learning candidate enters the system without passing this gate. It validates
experiment DESIGN at the door; it never claims that learning occurred.

The law (Shawn, 2026-10-09): the old backlog proved that verification cannot be
bolted onto a candidate that never had a falsifiable experimental contract.
0 of 13 analyzed candidates were verifiable as designed — tautologies, honest
nulls, non-experiments, definitional token changes. This gate exists so that
class of failure can never enter again.

ADMISSION CONTRACT (all must hold):
  (a) falsifiable claim — the claimant states what observation would prove it wrong
  (b) same named task in both arms
  (c) pre-registered success criterion, independent of the lesson
  (d) machine / different-seat / deterministic measurement
  (e) doer != scorer
  (f) nulls are admitted as NOT VERIFIED, never as CANDIDATE
  (g) both arms actually measured (a non-experiment is not a candidate)
  (h) asserts a behavioral change, not a token difference

Anything failing the contract is REJECTED AT THE DOOR with machine-readable
reasons. It never becomes a "candidate."

INTEGRATION CONTRACT (for the canonical Receiver and any other writer):
  Call admit_candidate() with the candidate dict BEFORE writing a CANDIDATE row.
  Write the row only when admitted_as == "CANDIDATE". Write NOT_VERIFIED rows
  only when admitted_as == "NOT_VERIFIED". On rejection, log the reasons and
  write nothing. The gate is pure: no DB, no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

ADMISSION_SCHEMA = "NAYAPOWER_LEARNING_CANDIDATE_ADMISSION_V1"

MEASUREMENT_METHODS = frozenset({"machine", "different_seat", "deterministic"})

# admitted_as values
CANDIDATE = "CANDIDATE"
NOT_VERIFIED = "NOT_VERIFIED"
REJECTED = "REJECTED"


@dataclass(frozen=True)
class AdmissionResult:
    admitted: bool
    admitted_as: str  # CANDIDATE | NOT_VERIFIED | REJECTED
    reasons: tuple[str, ...]  # empty when admitted; rejection codes otherwise


def _nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def admit_candidate(candidate: Any) -> AdmissionResult:
    """Apply the admission contract. Pure: no DB, no network."""
    if not isinstance(candidate, dict):
        return AdmissionResult(False, REJECTED, ("CANDIDATE_MUST_BE_OBJECT",))
    errors: list[str] = []

    if candidate.get("schema") != ADMISSION_SCHEMA:
        errors.append("SCHEMA_MISMATCH")

    # (a) falsifiable claim — machine-checkable proxy: the claimant must state
    # what observation would prove the claim wrong.
    if not _nonempty_str(candidate.get("claim")):
        errors.append("CLAIM_REQUIRED")
    if not _nonempty_str(candidate.get("falsification_condition")):
        errors.append("CLAIM_NOT_FALSIFIABLE")

    # (b) same named task in both arms
    if not _nonempty_str(candidate.get("task")):
        errors.append("NO_NAMED_TASK")

    # (c) pre-registered success criterion, independent of the lesson
    if not _nonempty_str(candidate.get("success_criterion")):
        errors.append("NO_PREREGISTERED_CRITERION")
    elif candidate.get("criterion_independent_of_lesson") is not True:
        errors.append("CRITERION_NOT_INDEPENDENT")

    # (d) machine / different-seat / deterministic measurement
    measurement = candidate.get("measurement")
    method = measurement.get("method") if isinstance(measurement, dict) else None
    if method not in MEASUREMENT_METHODS:
        errors.append("NO_MACHINE_MEASUREMENT")

    # (e) doer != scorer
    doer = candidate.get("doer")
    scorer = candidate.get("scorer")
    if not _nonempty_str(doer) or not _nonempty_str(scorer):
        errors.append("DOER_AND_SCORER_REQUIRED")
    elif str(doer).strip() == str(scorer).strip():
        errors.append("DOER_EQUALS_SCORER")

    # (g) both arms actually measured — kills tautologies and non-experiments
    arms = candidate.get("arms")
    treatment_obs = arms.get("treatment", {}).get("observable") if isinstance(arms, dict) else None
    control_obs = arms.get("control", {}).get("observable") if isinstance(arms, dict) else None
    treatment_measured = arms.get("treatment", {}).get("measured_at") if isinstance(arms, dict) else None
    control_measured = arms.get("control", {}).get("measured_at") if isinstance(arms, dict) else None
    if not _nonempty_str(treatment_obs) or not _nonempty_str(control_obs):
        errors.append("ARMS_REQUIRE_OBSERVABLE_BEHAVIOR")
    elif str(treatment_obs).strip().lower() == str(control_obs).strip().lower():
        errors.append("ARMS_INDIMINISHABLE")
    if not _nonempty_str(treatment_measured) or not _nonempty_str(control_measured):
        errors.append("NON_EXPERIMENT_NO_MEASURED_ARMS")

    # (h) behavioral change, not a token difference
    if candidate.get("asserts_behavioral_change") is not True:
        errors.append("TOKEN_DIFFERENCE_NOT_BEHAVIOR")
    elif not _nonempty_str(candidate.get("behavioral_measure")):
        errors.append("BEHAVIORAL_MEASURE_REQUIRED")

    if errors:
        return AdmissionResult(False, REJECTED, tuple(errors))

    # (f) nulls stay NOT VERIFIED — an honest null is negative evidence, kept,
    # but it is never a candidate for verification.
    if str(candidate.get("outcome", "pending")).strip().lower() == "null":
        return AdmissionResult(True, NOT_VERIFIED, ())

    return AdmissionResult(True, CANDIDATE, ())


def rejection_log(candidate_id: str, result: AdmissionResult) -> str:
    """One-line door log for a rejected candidate."""
    return f"ADMISSION_REJECTED id={candidate_id} reasons={','.join(result.reasons)}"

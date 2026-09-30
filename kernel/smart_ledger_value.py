"""Typed V2.1 value receipts for the existing ``nayanet_smart_ledger`` runtime.

This module is the deterministic, database-free half of the SmartLedger value
seam. The physical ledger (``public.nayanet_smart_ledger``) and its writer
(``nayanet_record_ledger_event``) are unchanged; typed V2.1 receipts travel in
the existing ``value`` JSONB column. The SQL migration mirrors the validation
rules here so the database rejects malformed receipts even if a caller
bypasses this module.

Boundaries (do not move silently):
  Truth before score. Law before optimization. Authority before action.
  Value before activity. Evidence before reward. Human worth outside the
  equation. Reality corrects the math.

Key rules:
  * Historical ``NayaNET_V1_STARTING_MODEL`` rows (``assessed: false``,
    ``base_points`` 5/10) are preserved byte-identical and classify as
    UNASSESSED. They are never rewritten or reinterpreted.
  * Recognition points are minted ONLY from VERIFIED_PASS contribution
    value. Raw engagement is recorded with zero points.
  * Negative contribution value is evidence for reliability/conduct
    evaluation; it never subtracts recognition points.
  * Reputation/points never create authority; these receipts carry no
    authority claim.
"""

from __future__ import annotations

import hashlib
import json
from typing import Mapping, Sequence

from kernel.value_calculus import (
    ENGINE_VERSION as CALCULUS_ENGINE_VERSION,
    contribution_points,
    contribution_value_score,
    independent_recompute,
)

ENGINE = "DECISION-VALUE-CALCULUS-V2.1"
ENGINE_VERSION = CALCULUS_ENGINE_VERSION  # "2.1"; single source of truth
RECEIPT_SCHEMA = "nayanet.value_receipt/v1"

RECEIPT_TYPES = ("ALIGNMENT_DECISION", "CONTRIBUTION_VALUE")
VERIFICATION_STATES = (
    "UNVERIFIED",
    "PASS_PENDING_WINDOW",
    "VERIFIED_PASS",
    "FAIL",
    "ESCALATE",
)
ASSESSMENTS = ("UNASSESSED", "ASSESSED", "VERIFIED_VALUE")
PRIVACY_CLASSES = ("PRIVATE", "SHARED", "COLLECTIVE", "PUBLIC")

LEGACY_ENGINE = "NayaNET_V1_STARTING_MODEL"

_CVS_FORMULA = "sign(verified_delta)*9*(quality*relevance*verification*impact*novelty)^(1/5)"


class ReceiptError(ValueError):
    """Raised when a value receipt is malformed. Message carries the reason."""


def _require(cond: bool, reason: str) -> None:
    if not cond:
        raise ReceiptError(f"VALUE_RECEIPT_INVALID: {reason}")


def validate_value_receipt(receipt: Mapping) -> Mapping:
    """Validate a typed V2.1 value receipt; return it unchanged if valid.

    Mirrors ``nayanet_value_receipt_validate`` in the SQL migration so the
    database enforces the same contract.
    """
    _require(isinstance(receipt, Mapping), "receipt must be a JSON object")
    rtype = receipt.get("receipt_type")
    _require(rtype in RECEIPT_TYPES, f"receipt_type must be one of {RECEIPT_TYPES}")
    _require(receipt.get("engine") == ENGINE, f"engine must be {ENGINE}")
    _require(receipt.get("engine_version") == ENGINE_VERSION,
              f"engine_version must be {ENGINE_VERSION}")
    vstate = receipt.get("verification_state")
    _require(vstate in VERIFICATION_STATES,
              f"verification_state must be one of {VERIFICATION_STATES}")

    inputs = receipt.get("inputs")
    _require(isinstance(inputs, Mapping) and len(inputs) > 0,
              "inputs must be a non-empty object")
    _require(isinstance(receipt.get("evidence"), list), "evidence must be an array")
    _require(isinstance(receipt.get("value_calculation"), Mapping)
              and len(receipt["value_calculation"]) > 0,
              "value_calculation must be a non-empty object")
    _require(isinstance(receipt.get("points_derivation"), Mapping),
              "points_derivation must be an object")

    prov = receipt.get("provenance")
    _require(isinstance(prov, Mapping), "provenance must be an object")
    for key in ("owner_id", "source_table", "source_id"):
        _require(prov.get(key), f"provenance.{key} is required")

    pclass = receipt.get("privacy_classification", "PRIVATE")
    _require(pclass in PRIVACY_CLASSES,
              f"privacy_classification must be one of {PRIVACY_CLASSES}")

    points = receipt["points_derivation"].get("points_awarded", 0)
    _require(isinstance(points, (int, float)) and points >= 0,
              "points_derivation.points_awarded must be a non-negative number")
    # Evidence before reward: no points until value is verified.
    if vstate != "VERIFIED_PASS":
        _require(points == 0,
                  f"points_awarded must be 0 while verification_state={vstate} "
                  "(evidence before reward)")

    if rtype == "ALIGNMENT_DECISION":
        embedded = receipt.get("decision_receipt")
        _require(isinstance(embedded, Mapping),
                  "ALIGNMENT_DECISION requires an embedded decision_receipt")
        _require(embedded.get("receipt_type") == "ALIGNMENT_DECISION",
                  "embedded decision_receipt must be a V2.1 ALIGNMENT_DECISION receipt")
    else:  # CONTRIBUTION_VALUE
        _require(inputs.get("action_class"), "inputs.action_class is required")
        _require(inputs.get("actor_id"), "inputs.actor_id is required")
        vc = receipt["value_calculation"]
        cvs = vc.get("cvs")
        _require(isinstance(cvs, (int, float)) and -9.0 <= cvs <= 9.0,
                  "value_calculation.cvs must be a number in [-9, 9]")
        _require(isinstance(vc.get("factors"), Mapping) and len(vc["factors"]) > 0,
                  "value_calculation.factors must be a non-empty object")
    return receipt


def build_alignment_decision_receipt(
    *,
    decision_receipt: Mapping,
    owner_id: str,
    source_table: str,
    source_id: str,
    recorded_by: str,
    recorded_at: str,
    evidence_refs: Sequence[str] | None = None,
    privacy_classification: str = "PRIVATE",
) -> dict:
    """Wrap a canonical V2.1 ALIGNMENT_DECISION receipt in the ledger envelope.

    The embedded decision receipt is kept byte-identical so its strict-JSON
    schema validation still applies. Decision receipts award no recognition
    points; they record alignment value, not recognition.
    """
    _require(isinstance(decision_receipt, Mapping)
              and decision_receipt.get("receipt_type") == "ALIGNMENT_DECISION",
              "decision_receipt must be a V2.1 ALIGNMENT_DECISION receipt")
    evaluation = decision_receipt.get("evaluation", {})
    receipt = {
        "receipt_type": "ALIGNMENT_DECISION",
        "receipt_schema": RECEIPT_SCHEMA,
        "engine": ENGINE,
        "engine_version": ENGINE_VERSION,
        "assessment": "ASSESSED",
        "verification_state": decision_receipt.get("verification", "UNVERIFIED"),
        "privacy_classification": privacy_classification,
        "inputs": {
            "decision_id": decision_receipt.get("decision_id"),
            "objective": decision_receipt.get("objective"),
            "baseline_id": decision_receipt.get("baseline_id"),
            "stakeholders": decision_receipt.get("stakeholders", []),
            "horizon": decision_receipt.get("horizon"),
            "authority_basis": decision_receipt.get("authority_basis"),
            "candidate_ids": [r.get("candidate_id")
                              for r in evaluation.get("rows", [])],
        },
        "evidence": list(evidence_refs or decision_receipt.get("evidence_refs", [])),
        "value_calculation": {
            "delta_v_predicted": decision_receipt.get("delta_v_predicted"),
            "delta_v_actual": decision_receipt.get("delta_v_actual"),
            "d_verified": decision_receipt.get("d_verified"),
            "calibration_error": decision_receipt.get("calibration_error"),
            "decision": evaluation.get("decision"),
            "selected": evaluation.get("selected"),
            "relative_margin": evaluation.get("relative_margin"),
        },
        "points_derivation": {
            "points_awarded": 0,
            "basis": "decision receipts record alignment value; they mint no "
                     "recognition points",
        },
        "provenance": {
            "owner_id": owner_id,
            "source_table": source_table,
            "source_id": source_id,
            "recorded_by": recorded_by,
            "recorded_at": recorded_at,
            "ledger": "public.nayanet_smart_ledger",
            "writer": "nayanet_record_value_receipt",
        },
        "decision_receipt": dict(decision_receipt),
    }
    return validate_value_receipt(receipt)


def build_contribution_value_receipt(
    *,
    actor_id: str,
    owner_id: str,
    source_table: str,
    source_id: str,
    action_class: str,
    quality: float,
    relevance: float,
    verification: float,
    impact: float,
    novelty: float,
    verified_delta: float,
    points_per_unit: float,
    repeat_count: int = 1,
    verification_state: str = "UNVERIFIED",
    evidence: Sequence | None = None,
    recorded_by: str | None = None,
    recorded_at: str,
    scoring_profile: str = "contribution-profile/v1",
    privacy_classification: str = "PRIVATE",
) -> dict:
    """Build a typed CONTRIBUTION_VALUE receipt.

    Diminishing returns: ``repeat_decay = 1 / repeat_count`` so repetitive
    activity cannot farm points. Evidence before reward: ``points_awarded``
    is zero unless ``verification_state == "VERIFIED_PASS"``.
    """
    _require(repeat_count >= 1, "repeat_count must be >= 1")
    _require(verification_state in VERIFICATION_STATES,
              f"verification_state must be one of {VERIFICATION_STATES}")
    factors = {
        "quality": quality,
        "relevance": relevance,
        "verification": verification,
        "impact": impact,
        "novelty": novelty,
    }
    cvs = contribution_value_score(
        quality=quality, relevance=relevance, verification=verification,
        impact=impact, novelty=novelty, verified_delta=verified_delta,
    )
    repeat_decay = 1.0 / repeat_count
    if verification_state == "VERIFIED_PASS":
        points_awarded = contribution_points(cvs, points_per_unit, repeat_decay)
    else:
        points_awarded = 0.0
    receipt = {
        "receipt_type": "CONTRIBUTION_VALUE",
        "receipt_schema": RECEIPT_SCHEMA,
        "engine": ENGINE,
        "engine_version": ENGINE_VERSION,
        "assessment": "ASSESSED",
        "verification_state": verification_state,
        "privacy_classification": privacy_classification,
        "inputs": {
            "actor_id": actor_id,
            "action_class": action_class,
            **factors,
            "verified_delta": verified_delta,
            "repeat_count": repeat_count,
            "scoring_profile": scoring_profile,
        },
        "evidence": list(evidence or []),
        "value_calculation": {
            "cvs": cvs,
            "factors": factors,
            "verified_delta": verified_delta,
            "formula": _CVS_FORMULA,
            "note": "negative CVS is evidence for reliability/conduct "
                    "evaluation; it never subtracts recognition points",
        },
        "points_derivation": {
            "points_per_unit": points_per_unit,
            "repeat_count": repeat_count,
            "repeat_decay": repeat_decay,
            "points_awarded": points_awarded,
            "basis": "positive recognition from verified value only; raw "
                     "activity is recorded separately with zero points",
        },
        "provenance": {
            "owner_id": owner_id,
            "source_table": source_table,
            "source_id": source_id,
            "actor_id": actor_id,
            "recorded_by": recorded_by or actor_id,
            "recorded_at": recorded_at,
            "ledger": "public.nayanet_smart_ledger",
            "writer": "nayanet_record_value_receipt",
            "scoring_profile": scoring_profile,
        },
    }
    return validate_value_receipt(receipt)


def is_legacy_starting_model(ledger_value: Mapping) -> bool:
    """True for historical NayaNET_V1_STARTING_MODEL rows.

    These rows (``assessed: false``, ``base_points`` 5/10) are historical
    provenance and must be preserved exactly, never rewritten.
    """
    if not isinstance(ledger_value, Mapping):
        return False
    return (
        ledger_value.get("value_engine") == LEGACY_ENGINE
        or ledger_value.get("assessed") is False
    )


def classify_value_assessment(ledger_value) -> str:
    """Classify a ledger ``value`` payload: UNASSESSED / ASSESSED / VERIFIED_VALUE.

    Mirrors the ``nayanet_ledger_value_assessment`` SQL view. Legacy starting
    model rows classify as UNASSESSED without being modified.
    """
    if not isinstance(ledger_value, Mapping):
        return "UNASSESSED"
    if is_legacy_starting_model(ledger_value):
        return "UNASSESSED"
    try:
        validate_value_receipt(ledger_value)
    except ReceiptError:
        return "UNASSESSED"
    if ledger_value.get("verification_state") == "VERIFIED_PASS":
        return "VERIFIED_VALUE"
    return "ASSESSED"


def receipt_canonical_hash(receipt: Mapping) -> str:
    """Deterministic sha256 over canonical JSON (sorted keys, compact)."""
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def recompute_contribution_from_receipt(receipt: Mapping) -> dict:
    """Independently recompute a CONTRIBUTION_VALUE receipt from its inputs.

    Parses the receipt fresh (no builder involved) and re-derives the score
    and points from the recorded inputs, then compares. This is the
    INDEPENDENT REREAD -> SAME CALCULATION link of the proof chain.
    """
    validate_value_receipt(receipt)
    _require(receipt["receipt_type"] == "CONTRIBUTION_VALUE",
              "recompute_contribution_from_receipt needs a CONTRIBUTION_VALUE receipt")
    inputs = dict(receipt["inputs"])  # fresh parse of the stored inputs
    stated_cvs = receipt["value_calculation"]["cvs"]
    stated_points = receipt["points_derivation"]["points_awarded"]
    stated_decay = receipt["points_derivation"]["repeat_decay"]

    recomputed_cvs = contribution_value_score(
        quality=float(inputs["quality"]), relevance=float(inputs["relevance"]),
        verification=float(inputs["verification"]), impact=float(inputs["impact"]),
        novelty=float(inputs["novelty"]),
        verified_delta=float(inputs["verified_delta"]),
    )
    recomputed_decay = 1.0 / int(inputs["repeat_count"])
    if receipt["verification_state"] == "VERIFIED_PASS":
        recomputed_points = contribution_points(
            recomputed_cvs,
            float(receipt["points_derivation"]["points_per_unit"]),
            recomputed_decay,
        )
    else:
        recomputed_points = 0.0

    cvs_ok = abs(recomputed_cvs - stated_cvs) < 1e-9
    points_ok = abs(recomputed_points - stated_points) < 1e-9
    decay_ok = abs(recomputed_decay - stated_decay) < 1e-12
    return {
        "cvs_matches": cvs_ok,
        "points_match": points_ok,
        "repeat_decay_matches": decay_ok,
        "recomputed_cvs": recomputed_cvs,
        "recomputed_points": recomputed_points,
        "receipt_hash": receipt_canonical_hash(receipt),
        "ok": cvs_ok and points_ok and decay_ok,
    }


def recompute_decision_from_receipt(receipt: Mapping, candidates, profile,
                                    risk_policy=None) -> dict:
    """Independently recompute an ALIGNMENT_DECISION receipt's evaluation."""
    validate_value_receipt(receipt)
    _require(receipt["receipt_type"] == "ALIGNMENT_DECISION",
              "recompute_decision_from_receipt needs an ALIGNMENT_DECISION receipt")
    if risk_policy is None:
        result = independent_recompute(receipt["decision_receipt"], candidates, profile)
    else:
        result = independent_recompute(receipt["decision_receipt"], candidates,
                                       profile, risk_policy)
    result["receipt_hash"] = receipt_canonical_hash(receipt)
    result["ok"] = bool(result["matches_decision"] and result["matches_selected"])
    return result

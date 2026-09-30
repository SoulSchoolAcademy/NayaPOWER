"""SmartLedger V2.1 typed value-receipt seam.

Routes ALIGNMENT_DECISION and CONTRIBUTION_VALUE receipts through the EXISTING
public.nayanet_smart_ledger via its `value` jsonb column. No new table, no
parallel ledger, no second points store.

Truth state: CANDIDATE runtime seam for Issue #1182 (left open for
production/runtime proof) and Issue #1184. Not production-applied.

Constitutional invariants (enforced here and in SQL):
  ACTIVITY != VALUE. ENGAGEMENT != VERIFICATION. REPUTATION != AUTHORITY.
  EVIDENCE before REWARD. Human worth outside the equation.
  Historical NayaNET_V1_STARTING_MODEL rows are preserved exactly and are
  NEVER reinterpreted, rescored, or upgraded by this seam.

Assessment states:
  UNASSESSED     - legacy V1 rows ({"assessed": false, "base_points": 5|10}).
  ASSESSED       - V2.1 evaluated; verification pending.
  VERIFIED_VALUE - outcome observed and verified; delta_v_actual recorded.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Sequence

from kernel.value_calculus import (
    ENGINE_VERSION,
    Candidate,
    QualityProfile,
    RiskPolicy,
    build_decision_receipt,
    contribution_points,
    contribution_value_score,
    evaluate_candidates,
    independent_recompute,
)

V1_ENGINE = "NayaNET_V1_STARTING_MODEL"
V2_ENGINE = ENGINE_VERSION  # "DECISION-VALUE-CALCULUS-V2.1"
SCHEMA_VERSION = "2.1"

RECEIPT_TYPES = ("ALIGNMENT_DECISION", "CONTRIBUTION_VALUE")
ASSESSMENTS = ("ASSESSED", "VERIFIED_VALUE")

# Ten-Star progression: candidate thresholds + names (Issue #1184).
# No historical set was recovered from the Brain (searched 2026-09-30);
# these are fresh hypotheses, versioned, calibratable from evidence.
TEN_STAR_TIERS = (
    (1, "Seed", 0),
    (2, "Emerging", 500),
    (3, "Developing", 2_000),
    (4, "Advancing", 6_000),
    (5, "Mastering", 12_000),
    (6, "Guide", 20_000),
    (7, "Mentor", 30_000),
    (8, "Steward", 42_000),
    (9, "Luminary", 57_000),
    (10, "Primal Master", 75_000),
)


class EnvelopeError(ValueError):
    """Raised when a value-receipt envelope is malformed. Mirrors the SQL
    VALUE_RECEIPT_* exceptions in 20261001031000_smartledger_v2_1_value_receipts.sql."""


def _require_finite(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise EnvelopeError(f"non-numeric {name}")
    if not math.isfinite(float(value)):
        raise EnvelopeError(f"non-finite {name}")
    return float(value)


def validate_envelope(value: Mapping[str, Any]) -> None:
    """Validate a V2.1 receipt envelope. Raises EnvelopeError if malformed.
    Mirrors public.nayanet_record_value_receipt."""
    if not isinstance(value, dict):
        raise EnvelopeError("envelope must be an object")
    receipt_type = value.get("receipt_type")
    if receipt_type not in RECEIPT_TYPES:
        raise EnvelopeError(f"unknown receipt_type: {receipt_type!r}")
    if value.get("value_engine") != V2_ENGINE:
        raise EnvelopeError(f"unknown value_engine: {value.get('value_engine')!r}")
    if value.get("assessment") not in ASSESSMENTS:
        raise EnvelopeError(f"bad assessment: {value.get('assessment')!r}")
    if receipt_type == "ALIGNMENT_DECISION":
        receipt = value.get("receipt")
        if not isinstance(receipt, dict) or receipt.get("receipt_type") != "ALIGNMENT_DECISION":
            raise EnvelopeError("ALIGNMENT_DECISION envelope missing receipt")
    else:
        for key in ("inputs", "value_calculation", "points_derivation",
                    "verification_state", "provenance"):
            if key not in value:
                raise EnvelopeError(f"CONTRIBUTION_VALUE envelope missing {key}")
        _require_finite(value["value_calculation"].get("cvs"), "cvs")
        _require_finite(value["points_derivation"].get("points"), "points")
    # Authority invariant: a receipt must never carry an authority grant.
    if "authority_grant" in value or "grants_authority" in value:
        raise EnvelopeError("receipt must not carry authority")


def classify(value: Any) -> str:
    """Classify any ledger `value` payload. V1 legacy rows are UNASSESSED and
    are never reinterpreted."""
    if not isinstance(value, dict):
        return "UNASSESSED"
    if value.get("value_engine") == V1_ENGINE:
        return "UNASSESSED"
    if value.get("value_engine") != V2_ENGINE:
        return "UNASSESSED"
    assessment = value.get("assessment")
    return assessment if assessment in ASSESSMENTS else "UNASSESSED"


def build_alignment_value(
    *,
    receipt: Mapping[str, Any],
    assessment: str,
    provenance: Mapping[str, Any],
) -> dict:
    """Wrap a build_decision_receipt() output into the ledger `value` envelope."""
    if assessment not in ASSESSMENTS:
        raise EnvelopeError(f"bad assessment: {assessment!r}")
    envelope = {
        "receipt_type": "ALIGNMENT_DECISION",
        "value_engine": V2_ENGINE,
        "engine_version": V2_ENGINE,
        "schema_version": SCHEMA_VERSION,
        "assessment": assessment,
        "receipt": dict(receipt),
        "provenance": dict(provenance),
    }
    validate_envelope(envelope)
    return envelope


def build_contribution_value(
    *,
    contributor_id: str,
    action_class: str,
    quality: float,
    relevance: float,
    verification: float,
    impact: float,
    novelty: float,
    verified_delta: float,
    points_per_unit: float,
    repeat_decay: float = 1.0,
    verification_state: str = "UNVERIFIED",
    evidence_refs: Sequence[str] = (),
    provenance: Mapping[str, Any] = None,
    assessment: str = "ASSESSED",
) -> dict:
    """Build a CONTRIBUTION_VALUE envelope from V2.1 contribution math.

    EVIDENCE before REWARD: verification == 0 (or verified_delta == 0) forces
    CVS to 0 and points to 0, whatever the action class. Raw engagement never
    equals verified value. Negative CVS yields zero points (evidence for
    reliability/conduct evaluation, never automatic punishment).
    """
    cvs = contribution_value_score(
        quality=quality, relevance=relevance, verification=verification,
        impact=impact, novelty=novelty, verified_delta=verified_delta,
    )
    points = contribution_points(cvs, points_per_unit, repeat_decay)
    if verification_state == "VERIFIED" and verification > 0 and verified_delta != 0:
        assessment = "VERIFIED_VALUE"
    envelope = {
        "receipt_type": "CONTRIBUTION_VALUE",
        "value_engine": V2_ENGINE,
        "engine_version": V2_ENGINE,
        "schema_version": SCHEMA_VERSION,
        "assessment": assessment,
        "contributor_id": contributor_id,
        "action_class": action_class,
        "inputs": {
            "quality": quality, "relevance": relevance, "verification": verification,
            "impact": impact, "novelty": novelty, "verified_delta": verified_delta,
        },
        "value_calculation": {"cvs": cvs, "formula": "CVS_v2.1"},
        "points_derivation": {
            "points_per_unit": points_per_unit,
            "repeat_decay": repeat_decay,
            "points": points,
            "profile_version": "ten-star-action-profile-v1-hypothesis",
        },
        "verification_state": verification_state,
        "evidence_refs": list(evidence_refs),
        "provenance": dict(provenance or {}),
    }
    validate_envelope(envelope)
    return envelope


def reread_and_recompute(
    envelope: Mapping[str, Any],
    candidates: Sequence[Candidate] = (),
    profile: Optional[QualityProfile] = None,
    risk_policy: Optional[RiskPolicy] = None,
) -> dict:
    """Independent reconstruction: given ONLY the stored envelope (plus the
    candidate set for decisions, refetched by the verifier), recompute and
    compare. Returns {"verdict": "MATCH"|"MISMATCH", ...}."""
    validate_envelope(envelope)
    receipt_type = envelope["receipt_type"]
    if receipt_type == "ALIGNMENT_DECISION":
        if profile is None:
            raise EnvelopeError("decision recompute requires the quality profile")
        result = independent_recompute(
            envelope["receipt"], candidates, profile, risk_policy or RiskPolicy()
        )
        match = bool(result.get("matches_decision") and result.get("matches_selected"))
        return {"verdict": "MATCH" if match else "MISMATCH",
                "detail": result}
    inputs = envelope["inputs"]
    expected_cvs = contribution_value_score(
        quality=inputs["quality"], relevance=inputs["relevance"],
        verification=inputs["verification"], impact=inputs["impact"],
        novelty=inputs["novelty"], verified_delta=inputs["verified_delta"],
    )
    stored_cvs = envelope["value_calculation"]["cvs"]
    pd = envelope["points_derivation"]
    expected_points = contribution_points(
        expected_cvs, pd["points_per_unit"], pd["repeat_decay"])
    stored_points = pd["points"]
    match = (abs(expected_cvs - stored_cvs) < 1e-9
             and abs(expected_points - stored_points) < 1e-9)
    return {"verdict": "MATCH" if match else "MISMATCH",
            "expected_cvs": expected_cvs, "stored_cvs": stored_cvs,
            "expected_points": expected_points, "stored_points": stored_points}


def tier_for_points(points: float) -> dict:
    """Project a Ten-Star tier from verified points. Derived on every call;
    nothing is stored. Names/thresholds are candidates (Issue #1184)."""
    stars, name, _ = TEN_STAR_TIERS[0]
    for s, n, threshold in TEN_STAR_TIERS:
        if points >= threshold:
            stars, name = s, n
    return {"stars": stars, "name": name, "points": points,
            "tier_set": "ten-star-v1-hypothesis"}


def derive_owner_projection(rows: Sequence[Mapping[str, Any]], owner_id: str) -> dict:
    """Project score/level for one owner SOLELY from their V2.1 receipt
    evidence. Owner-scoped (RLS model): other owners' rows are ignored.
    Returns no authority fields, ever."""
    verified_points = 0.0
    pending_points = 0.0
    decisions = 0
    contributions = 0
    for row in rows:
        if row.get("owner_id") != owner_id:
            continue  # cross-owner isolation
        value = row.get("value") or {}
        if value.get("value_engine") != V2_ENGINE:
            continue  # legacy V1 rows never enter the projection
        rt = value.get("receipt_type")
        if rt == "ALIGNMENT_DECISION":
            decisions += 1
        elif rt == "CONTRIBUTION_VALUE":
            contributions += 1
            pts = float(value["points_derivation"]["points"])
            if value.get("assessment") == "VERIFIED_VALUE":
                verified_points += pts
            else:
                pending_points += pts
    tier = tier_for_points(verified_points)
    return {
        "owner_id": owner_id,
        "verified_points": verified_points,
        "assessed_pending_points": pending_points,
        "decision_receipts": decisions,
        "contribution_receipts": contributions,
        "tier": tier,
        "derived_from": "smartledger_v2.1_receipts",
    }


@dataclass
class MemoryLedgerHarness:
    """Deterministic in-memory model of nayanet_record_ledger_event semantics:
    idempotent on (owner_id, source_table, source_id); hash-chained per owner;
    owner-scoped reads (RLS model). Used for the proof chain without a live DB."""

    _rows: dict = field(default_factory=dict)
    _last_hash: dict = field(default_factory=dict)

    def _chain_hash(self, owner_id: str, event_type: str, source_table: str,
                    source_id: str, previous: str, value: Any) -> str:
        import json as _json
        canonical = "|".join([
            owner_id, event_type, source_table, source_id, previous or "",
            _json.dumps(value, sort_keys=True, allow_nan=False),
        ])
        return hashlib.sha256(canonical.encode()).hexdigest()

    def record_value_receipt(
        self, *, owner_id: str, actor_id: Optional[str], event_type: str,
        source_table: str, source_id: str, value: Mapping[str, Any],
        verification: Mapping[str, Any] = None,
        privacy_classification: str = "PRIVATE",
        status: str = "RECORDED",
    ) -> tuple[dict, bool]:
        """Validate the envelope (SQL-validator model), then record idempotently.
        Returns (row, created). Replay of the same (owner, source_table,
        source_id) returns the EXISTING row with created=False."""
        validate_envelope(value)
        key = (owner_id, source_table, source_id)
        if key in self._rows:
            return self._rows[key], False
        previous = self._last_hash.get(owner_id)
        event_hash = self._chain_hash(owner_id, event_type, source_table,
                                      source_id, previous, value)
        row = {
            "ledger_event_id": f"evt-{len(self._rows) + 1:04d}",
            "owner_id": owner_id,
            "actor_id": actor_id,
            "event_type": event_type,
            "source_table": source_table,
            "source_id": source_id,
            "previous_chain_hash": previous,
            "event_hash": event_hash,
            "privacy_classification": privacy_classification,
            "status": status,
            "verification": dict(verification or {}),
            "value": dict(value),
        }
        self._rows[key] = row
        self._last_hash[owner_id] = event_hash
        return row, True

    def record_legacy(self, **kwargs) -> tuple[dict, bool]:
        """Record a historical V1-shaped row verbatim (no envelope validation)."""
        key = (kwargs["owner_id"], kwargs["source_table"], kwargs["source_id"])
        if key in self._rows:
            return self._rows[key], False
        row = {"ledger_event_id": f"evt-{len(self._rows) + 1:04d}", **kwargs}
        self._rows[key] = row
        return row, True

    def rows_for(self, owner_id: str) -> list[dict]:
        return [r for r in self._rows.values() if r.get("owner_id") == owner_id]

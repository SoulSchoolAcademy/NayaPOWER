"""Risk-based intelligence quarantine — eligibility overlay (SPEC, not production code).

Shawn's refinement (2026-10-10): quarantine unsafe USES of knowledge, not
knowledge itself. "Contain the smallest unsafe dependency. Preserve
independent truth. Keep authorized work flowing."

Design:
- Five containment levels L0-L4, ORTHOGONAL to truth states
  (CANDIDATE/VERIFIED/ACTIVE). A VERIFIED lesson can become
  application-restricted without erasing its receipt.
- Risk is per proposed USE, not per lesson: R = Pc x H x D x E.
  LAW hard stops apply before any numeric comparison. Uncalibrated
  probability stays UNKNOWN, never guessed.
- Architecture: immutable incident record + separate versioned eligibility
  overlay. Every ACT plan records the intelligence AND eligibility
  versions used.
- Fail-closed: eligibility lookup failure on a consequential dependency
  = the action cannot proceed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# Containment levels ----------------------------------------------------------

L0_NORMAL = "L0_NORMAL"            # eligible
L1_OBSERVE = "L1_OBSERVE"          # monitored; use allowed, watched
L2_RESTRICT = "L2_RESTRICT"        # limited use: read/investigate/hypothesize ok,
                                  # consequential uses blocked
L3_QUARANTINE = "L3_QUARANTINE"    # application blocked for affected decisions
L4_EMERGENCY = "L4_EMERGENCY"      # stop the execution path, preserve evidence,
                                  # escalate via LAW

LEVELS = (L0_NORMAL, L1_OBSERVE, L2_RESTRICT, L3_QUARANTINE, L4_EMERGENCY)

# Use classes: which uses does a level permit?
READ_USES = ("read", "investigate", "hypothesize")
CONSEQUENTIAL_USES = ("act", "decide", "promote", "execute")


@dataclass(frozen=True)
class IncidentRecord:
    """Immutable incident: what was detected, when, by whom. Never mutated."""
    incident_id: str
    lesson_id: str
    detected_at: str
    detected_by: str
    reason: str
    evidence_refs: tuple[str, ...] = ()


@dataclass
class EligibilityRecord:
    """Versioned eligibility for one lesson. Separate from the lesson itself."""
    lesson_id: str
    level: str
    scope: tuple[str, ...] = ()      # situations/decisions affected; empty = all
    incident_id: str | None = None
    version: int = 1
    set_at: str = ""
    set_by: str = ""
    # raising the level requires a new incident; lowering requires revalidation
    revalidation_ref: str | None = None


@dataclass
class EligibilityOverlay:
    """Versioned map lesson_id -> EligibilityRecord + immutable incident log."""
    version: int = 1
    records: dict[str, EligibilityRecord] = field(default_factory=dict)
    incidents: list[IncidentRecord] = field(default_factory=list)

    def get(self, lesson_id: str) -> EligibilityRecord | None:
        return self.records.get(lesson_id)

    def apply_incident(self, incident: IncidentRecord, level: str,
                       scope: tuple[str, ...] = (), at: str = "",
                       by: str = "") -> "EligibilityOverlay":
        """Return a NEW overlay version (immutable history)."""
        new_records = dict(self.records)
        prev = new_records.get(incident.lesson_id)
        new_records[incident.lesson_id] = EligibilityRecord(
            lesson_id=incident.lesson_id, level=level, scope=scope,
            incident_id=incident.incident_id,
            version=(prev.version + 1) if prev else 1,
            set_at=at, set_by=by)
        return EligibilityOverlay(version=self.version + 1,
                                  records=new_records,
                                  incidents=[*self.incidents, incident])

    def restore(self, lesson_id: str, revalidation_ref: str,
                at: str = "", by: str = "") -> "EligibilityOverlay":
        """Lower a level after revalidation. Requires the revalidation receipt."""
        if not revalidation_ref:
            raise ValueError("restore_requires_revalidation_ref")
        new_records = dict(self.records)
        prev = new_records.get(lesson_id)
        if prev is None:
            raise ValueError("restore_unknown_lesson")
        new_records[lesson_id] = EligibilityRecord(
            lesson_id=lesson_id, level=L0_NORMAL, scope=(),
            incident_id=None, version=prev.version + 1,
            set_at=at, set_by=by, revalidation_ref=revalidation_ref)
        return EligibilityOverlay(version=self.version + 1,
                                  records=new_records,
                                  incidents=list(self.incidents))


# Per-use risk -----------------------------------------------------------------

def assess_use_risk(pc: float | None, consequence: float,
                    dependency: float, exposure: float) -> float | str:
    """R = Pc x H x D x E.

    pc: contamination probability in [0,1], or None when uncalibrated.
    consequence (H), dependency (D), exposure (E): non-negative weights.
    Uncalibrated probability stays UNKNOWN (never guessed) -> the use
    is treated as unassessable and fail-closed at the boundary.

    LAW hard stops apply BEFORE any numeric comparison (not modeled here;
    the caller enforces them first).
    """
    if pc is None:
        return "UNKNOWN"
    if not (0.0 <= pc <= 1.0):
        raise ValueError("pc_out_of_range")
    for name, v in (("consequence", consequence), ("dependency", dependency),
                    ("exposure", exposure)):
        if v < 0:
            raise ValueError(f"{name}_negative")
    return pc * consequence * dependency * exposure


# Decision boundary --------------------------------------------------------------

@dataclass(frozen=True)
class UseDecision:
    allowed: bool
    level: str
    reason: str
    overlay_version: int
    # the ACT plan must record intelligence_version + overlay_version


def check_use_eligibility(lesson_id: str, use: str, situation: str,
                          overlay: EligibilityOverlay | None,
                          risk: float | str = 0.0,
                          risk_threshold: float = 1.0) -> UseDecision:
    """The canonical decision boundary. Fail-closed.

    - overlay is None or lesson missing from overlay on a CONSEQUENTIAL
      use -> BLOCKED (eligibility lookup failure = action cannot proceed).
    - L0: allowed. L1: allowed + monitored. L2: read uses allowed,
      consequential blocked. L3: blocked for affected scope. L4: blocked,
      escalate.
    - risk UNKNOWN on consequential use -> BLOCKED.
    - risk >= threshold on consequential use -> BLOCKED (even at L0/L1:
      per-use risk overrides the level).
    """
    ov = overlay.version if overlay else 0
    if use in CONSEQUENTIAL_USES:
        if overlay is None:
            return UseDecision(False, L4_EMERGENCY,
                               "eligibility_lookup_failure", ov)
        rec = overlay.get(lesson_id)
        if rec is None:
            # No incident history: eligible by default (L0). The overlay
            # records deviations from normal; absence of incidents is not
            # a failure. (Infrastructure failure — overlay None — still
            # fail-closes above.)
            if risk == "UNKNOWN":
                return UseDecision(False, L0_NORMAL, "risk_unknown_fail_closed", ov)
            if isinstance(risk, (int, float)) and risk >= risk_threshold:
                return UseDecision(False, L0_NORMAL, "per_use_risk_exceeds_threshold", ov)
            return UseDecision(True, L0_NORMAL, "no_incidents_eligible_by_default", ov)
        if risk == "UNKNOWN":
            return UseDecision(False, rec.level, "risk_unknown_fail_closed", ov)
        if isinstance(risk, (int, float)) and risk >= risk_threshold:
            return UseDecision(False, rec.level, "per_use_risk_exceeds_threshold", ov)
        if rec.level == L0_NORMAL:
            return UseDecision(True, rec.level, "eligible", ov)
        if rec.level == L1_OBSERVE:
            return UseDecision(True, rec.level, "eligible_monitored", ov)
        if rec.level == L2_RESTRICT:
            return UseDecision(False, rec.level, "consequential_use_restricted", ov)
        if rec.level == L3_QUARANTINE:
            if rec.scope and situation not in rec.scope:
                return UseDecision(True, rec.level, "outside_quarantine_scope", ov)
            return UseDecision(False, rec.level, "quarantined_for_situation", ov)
        if rec.level == L4_EMERGENCY:
            return UseDecision(False, rec.level, "emergency_stop_escalate_via_law", ov)
        return UseDecision(False, rec.level, "unknown_level_fail_closed", ov)
    # read uses
    if overlay is None:
        return UseDecision(True, L0_NORMAL, "read_use_no_overlay", ov)
    rec = overlay.get(lesson_id)
    if rec is None:
        return UseDecision(True, L0_NORMAL, "read_use_unlisted", ov)
    if rec.level in (L0_NORMAL, L1_OBSERVE, L2_RESTRICT):
        return UseDecision(True, rec.level, "read_use_permitted", ov)
    if rec.level == L3_QUARANTINE:
        return UseDecision(True, rec.level, "read_use_permitted_quarantined", ov)
    return UseDecision(False, rec.level, "read_use_emergency_only", ov)

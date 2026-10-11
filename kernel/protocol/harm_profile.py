"""harm_profile.py — Law 11 structured harm profiles (T-05).

Per Naya 1's "Law of One — Conflicting Harms" and "Do-No-Harm Law: Intelligent
Risk Under Uncertainty" (2026-10-11):

  "No person is expendable. No serious harm disappears inside an average.
   No uncertain harm becomes zero."

The landed Law 11 enforcement (typed_action.py) represents harm as scalar
booleans (rights_safe / safety_safe / privacy_safe). This module adds the
missing structure: a harm profile H_g(a) preserved PER AFFECTED GROUP, with
the five harm dimensions qualified separately:

  severity | reversibility | timing | measurability | distribution

Rules this module enforces mechanically:
  1. Dimensions are ORDINALS, never numbers. No arithmetic is permitted on
     them — there is no "average severity", no weighted score, no optimistic
     collapse. Aggregation is worst-of, never mean.
  2. Severity and reversibility are independent qualifiers. A major-but-
     reversible harm is not the same decision as a minor-but-irreversible
     one; neither axis implies the other.
  3. Unknown is not safe. Any unqualified dimension in any group fails
     closed to NEEDS_EVIDENCE. (The six-state finding classification —
     TRUE_ZERO vs UNKNOWN vs UNMEASURED etc. — is T-06's module; here
     unknowns simply block admission.)
  4. One catastrophic group blocks the action no matter how many groups are
     unharmed. Concentrated serious harm is never averaged away.
  5. The full per-group assessment is preserved on every judgment, so any
     caller can audit which group, which dimension, which value decided.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Dimension value sets. Ordinals — ordering is meaningful, arithmetic is not.
# ---------------------------------------------------------------------------

SEVERITY_NEGLIGIBLE = "negligible"
SEVERITY_MINOR = "minor"
SEVERITY_MODERATE = "moderate"
SEVERITY_MAJOR = "major"
SEVERITY_CATASTROPHIC = "catastrophic"
SEVERITY_UNKNOWN = "unknown"
SEVERITIES = (
    SEVERITY_NEGLIGIBLE,
    SEVERITY_MINOR,
    SEVERITY_MODERATE,
    SEVERITY_MAJOR,
    SEVERITY_CATASTROPHIC,
    SEVERITY_UNKNOWN,
)

REV_FULLY = "fully_reversible"
REV_CONDITIONAL = "conditionally_reversible"
REV_IRREVERSIBLE = "irreversible"
REV_UNKNOWN = "unknown"
REVERSIBILITIES = (REV_FULLY, REV_CONDITIONAL, REV_IRREVERSIBLE, REV_UNKNOWN)

TIME_IMMEDIATE = "immediate"
TIME_NEAR_TERM = "near_term"
TIME_DELAYED = "delayed"
TIME_UNKNOWN = "unknown"
TIMINGS = (TIME_IMMEDIATE, TIME_NEAR_TERM, TIME_DELAYED, TIME_UNKNOWN)

MEAS_MEASURED = "measured"
MEAS_ESTIMATED = "estimated"
MEAS_UNMEASURABLE = "unmeasurable"
MEAS_UNKNOWN = "unknown"
MEASURABILITIES = (MEAS_MEASURED, MEAS_ESTIMATED, MEAS_UNMEASURABLE, MEAS_UNKNOWN)

DIST_SINGLE = "single_person"
DIST_SMALL_GROUP = "small_group"
DIST_BROAD = "broad_population"
DIST_UNIVERSAL = "universal"
DIST_UNKNOWN = "unknown"
DISTRIBUTIONS = (DIST_SINGLE, DIST_SMALL_GROUP, DIST_BROAD, DIST_UNIVERSAL, DIST_UNKNOWN)

# Ordinal rank for worst-of comparisons only. Rank is NOT a score: it is
# never summed, averaged, or weighted. UNKNOWN ranks highest so that
# worst-of comparison surfaces uncertainty instead of hiding it.
_SEVERITY_RANK = {
    SEVERITY_NEGLIGIBLE: 0,
    SEVERITY_MINOR: 1,
    SEVERITY_MODERATE: 2,
    SEVERITY_MAJOR: 3,
    SEVERITY_CATASTROPHIC: 4,
    SEVERITY_UNKNOWN: 5,
}
_REV_RANK = {REV_FULLY: 0, REV_CONDITIONAL: 1, REV_IRREVERSIBLE: 2, REV_UNKNOWN: 3}
_TIME_RANK = {TIME_IMMEDIATE: 0, TIME_NEAR_TERM: 1, TIME_DELAYED: 2, TIME_UNKNOWN: 3}
_MEAS_RANK = {MEAS_MEASURED: 0, MEAS_ESTIMATED: 1, MEAS_UNMEASURABLE: 2, MEAS_UNKNOWN: 3}
_DIST_RANK = {DIST_SINGLE: 0, DIST_SMALL_GROUP: 1, DIST_BROAD: 2, DIST_UNIVERSAL: 3, DIST_UNKNOWN: 4}


# ---------------------------------------------------------------------------
# GroupHarm — one affected group's five dimensions.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GroupHarm:
    """The harm assessment for ONE affected group.

    Every dimension defaults to unknown: an assessor must actively qualify
    each dimension, and anything unqualified fails closed downstream.
    group_id names WHO could be harmed (a person, role, population, or the
    collective) — it is preserved through every judgment, never aggregated.
    """
    group_id: str
    severity: str = SEVERITY_UNKNOWN
    reversibility: str = REV_UNKNOWN
    timing: str = TIME_UNKNOWN
    measurability: str = MEAS_UNKNOWN
    distribution: str = DIST_UNKNOWN
    evidence_refs: tuple[str, ...] = ()
    note: str = ""

    def __post_init__(self) -> None:
        if not self.group_id or not self.group_id.strip():
            raise ValueError("GroupHarm.group_id must be a non-empty identifier")
        for name, value, allowed in (
            ("severity", self.severity, SEVERITIES),
            ("reversibility", self.reversibility, REVERSIBILITIES),
            ("timing", self.timing, TIMINGS),
            ("measurability", self.measurability, MEASURABILITIES),
            ("distribution", self.distribution, DISTRIBUTIONS),
        ):
            if value not in allowed:
                raise ValueError(
                    f"GroupHarm.{name}={value!r} is not a canonical value; "
                    f"must be one of {allowed}"
                )

    def has_unknown(self) -> bool:
        return (
            self.severity == SEVERITY_UNKNOWN
            or self.reversibility == REV_UNKNOWN
            or self.timing == TIME_UNKNOWN
            or self.measurability == MEAS_UNKNOWN
            or self.distribution == DIST_UNKNOWN
        )

    def unknown_dimensions(self) -> tuple[str, ...]:
        out = []
        if self.severity == SEVERITY_UNKNOWN:
            out.append("severity")
        if self.reversibility == REV_UNKNOWN:
            out.append("reversibility")
        if self.timing == TIME_UNKNOWN:
            out.append("timing")
        if self.measurability == MEAS_UNKNOWN:
            out.append("measurability")
        if self.distribution == DIST_UNKNOWN:
            out.append("distribution")
        return tuple(out)


# ---------------------------------------------------------------------------
# HarmProfile — the full per-group assessment for one action.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class HarmProfile:
    """Structured harm profile H(a) = { H_g(a) for each affected group }.

    Immutable. The groups tuple is the profile — judgments below preserve
    it in full so the per-group record is never lost to aggregation.
    """
    groups: tuple[GroupHarm, ...]
    assessed_by: str = ""
    assessed_at: str = ""

    def __post_init__(self) -> None:
        if not self.groups:
            raise ValueError("HarmProfile requires at least one GroupHarm")
        ids = [g.group_id for g in self.groups]
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        if dupes:
            raise ValueError(f"HarmProfile has duplicate group_ids: {dupes}")

    def group(self, group_id: str) -> GroupHarm:
        for g in self.groups:
            if g.group_id == group_id:
                return g
        raise KeyError(f"unknown group_id: {group_id!r}")


# ---------------------------------------------------------------------------
# HarmJudgment — worst-of aggregation, never a score.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class HarmJudgment:
    """Outcome of judging a HarmProfile.

    blocks: at least one group faces blocking harm (catastrophic, or major
        + irreversible). One blocking group is enough — the count of
        unharmed groups never offsets it.
    needs_evidence: at least one dimension is unknown in at least one group.
        Unknown is not safe; the gate must demand evidence.
    delayed_observation: at least one group faces delayed harm. Does not
        force a verdict here — it flags that T-07's observation-window
        machinery must be engaged before execution.
    worst_*: worst observed ordinal per dimension (UNKNOWN sorts worst so
        uncertainty is surfaced, not hidden).
    blocking_group_ids: group_ids that triggered blocking harm, as structured
        data — never parsed out of reason strings (group_ids may contain
        ":" and "=").
    evidence_group_ids: group_ids with at least one unknown dimension, as
        structured data.
    groups: the full per-group assessment, preserved for audit.
    """
    blocks: bool
    needs_evidence: bool
    delayed_observation: bool
    worst_severity: str
    worst_reversibility: str
    worst_timing: str
    worst_measurability: str
    worst_distribution: str
    block_reasons: tuple[str, ...] = ()
    evidence_reasons: tuple[str, ...] = ()
    blocking_group_ids: tuple[str, ...] = ()
    evidence_group_ids: tuple[str, ...] = ()
    groups: tuple[GroupHarm, ...] = ()


def _worst(values: tuple[str, ...], rank: dict[str, int]) -> str:
    return max(values, key=lambda v: rank[v])


def judge(profile: HarmProfile) -> HarmJudgment:
    """Judge a harm profile. Worst-of per dimension; booleans, never a score.

    Blocking rule (no compression, no averaging):
      - any group with severity catastrophic -> blocks
      - any group with severity major AND reversibility irreversible -> blocks
    Evidence rule (fail closed):
      - any unknown dimension in any group -> needs_evidence
    """
    block_reasons: list[str] = []
    evidence_reasons: list[str] = []
    blocking_ids: list[str] = []
    evidence_ids: list[str] = []
    delayed = False

    for g in profile.groups:
        if g.severity == SEVERITY_CATASTROPHIC:
            # No person is expendable: one catastrophic group blocks, however
            # many other groups are unharmed. Reversibility does not redeem
            # catastrophe at plan time.
            block_reasons.append(
                f"BLOCK:group={g.group_id}:severity=catastrophic"
            )
            blocking_ids.append(g.group_id)
        elif g.severity == SEVERITY_MAJOR and g.reversibility == REV_IRREVERSIBLE:
            block_reasons.append(
                f"BLOCK:group={g.group_id}:severity=major:reversibility=irreversible"
            )
            blocking_ids.append(g.group_id)
        unknowns = g.unknown_dimensions()
        if unknowns:
            evidence_ids.append(g.group_id)
        for dim in unknowns:
            evidence_reasons.append(f"UNKNOWN:group={g.group_id}:dimension={dim}")
        if g.timing == TIME_DELAYED:
            delayed = True

    return HarmJudgment(
        blocks=bool(block_reasons),
        needs_evidence=bool(evidence_reasons),
        delayed_observation=delayed,
        worst_severity=_worst(tuple(g.severity for g in profile.groups), _SEVERITY_RANK),
        worst_reversibility=_worst(tuple(g.reversibility for g in profile.groups), _REV_RANK),
        worst_timing=_worst(tuple(g.timing for g in profile.groups), _TIME_RANK),
        worst_measurability=_worst(tuple(g.measurability for g in profile.groups), _MEAS_RANK),
        worst_distribution=_worst(tuple(g.distribution for g in profile.groups), _DIST_RANK),
        block_reasons=tuple(block_reasons),
        evidence_reasons=tuple(evidence_reasons),
        blocking_group_ids=tuple(sorted(set(blocking_ids))),
        evidence_group_ids=tuple(sorted(set(evidence_ids))),
        groups=profile.groups,
    )


def profile_digest(profile: HarmProfile) -> str:
    """Stable sha256 over the canonical serialization of the profile.

    Deterministic under group reordering (groups are sorted by group_id).
    Intended so Law 12 proof receipts can bind a harm profile as a
    dependency digest without depending on this module's internals.
    """
    canonical = {
        "groups": [
            {
                "group_id": g.group_id,
                "severity": g.severity,
                "reversibility": g.reversibility,
                "timing": g.timing,
                "measurability": g.measurability,
                "distribution": g.distribution,
                "evidence_refs": sorted(g.evidence_refs),
                "note": g.note,
            }
            for g in sorted(profile.groups, key=lambda g: g.group_id)
        ],
        "assessed_by": profile.assessed_by,
        "assessed_at": profile.assessed_at,
    }
    return hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

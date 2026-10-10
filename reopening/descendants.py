"""Descendant impact tracing for interpretation changes.

When a resolved interpretation changes, only MATERIALLY affected
descendants lose application eligibility. The classification:

    HISTORICAL_CITE   — cites the old interpretation for context/history.
                        Preserved. History is not rewritten.
    MATERIAL_DEPENDENT — the old interpretation is its sole evidence or
                         permission basis. Eligibility reassessed;
                         restricted pending review.

A descendant with genuine independent support is recalculated via that
support — never mechanically condemned because an ancestor changed.
"""

from __future__ import annotations

from dataclasses import dataclass, field


HISTORICAL_CITE = "HISTORICAL_CITE"
MATERIAL_DEPENDENT = "MATERIAL_DEPENDENT"
INDEPENDENTLY_SUPPORTED = "INDEPENDENTLY_SUPPORTED"


@dataclass(frozen=True)
class DependencyEdge:
    """One dependency of a descendant on an interpretation."""
    descendant_id: str
    interpretation_id: str
    relation: str      # REQUIRES | DERIVED_FROM | SUPPORTS | CITES ...
    is_sole_basis: bool  # True when nothing else supports this use


@dataclass
class DescendantImpact:
    descendant_id: str
    classification: str  # HISTORICAL_CITE | MATERIAL_DEPENDENT | INDEPENDENTLY_SUPPORTED
    action: str          # PRESERVE | REASSESS | RESTRICT_PENDING_REVIEW


def trace_impact(descendant_id: str,
                 edges: list[DependencyEdge],
                 changed_interpretation_id: str,
                 has_independent_support: bool) -> DescendantImpact:
    """Classify one descendant after an interpretation change.

    Rules, in order:
    1. Independent support exists -> INDEPENDENTLY_SUPPORTED / REASSESS
       (recalculate via own evidence; never mechanically condemned).
    2. No edge to the changed interpretation -> HISTORICAL_CITE / PRESERVE.
    3. Edge exists and is the sole basis -> MATERIAL_DEPENDENT /
       RESTRICT_PENDING_REVIEW.
    4. Edge exists but not sole basis -> HISTORICAL_CITE / PRESERVE
       (context preserved; other support carries the use).
    """
    relevant = [e for e in edges
                if e.descendant_id == descendant_id
                and e.interpretation_id == changed_interpretation_id]
    if has_independent_support:
        return DescendantImpact(descendant_id, INDEPENDENTLY_SUPPORTED,
                                "REASSESS")
    if not relevant:
        return DescendantImpact(descendant_id, HISTORICAL_CITE, "PRESERVE")
    if any(e.is_sole_basis for e in relevant):
        return DescendantImpact(descendant_id, MATERIAL_DEPENDENT,
                                "RESTRICT_PENDING_REVIEW")
    return DescendantImpact(descendant_id, HISTORICAL_CITE, "PRESERVE")

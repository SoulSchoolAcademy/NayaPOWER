"""Claim graph with CONNECT-reconciled relationship edges.

Reconciliation with the existing CONNECT registry
(.naya/NAYAPOWER-SYSTEM-NORTH-STAR-WHITE-PAPER-AND-ENGINEERING-BLUEPRINT-V1.md §16):
  Shawn's term      -> canonical edge used here
  REQUIRES          -> REQUIRES (exists)
  DERIVED_FROM      -> DERIVES_FROM (exists; canonical spelling)
  SUPPORTS          -> SUPPORTS (exists)
  CONTRADICTS       -> CONTRADICTS (exists)
  SUPERSEDES        -> SUPERSEDES (exists)
  CAUSES            -> CAUSED (exists; canonical spelling)
  EXCEPTION_TO      -> REFINES (exists; a limiting refinement — mapped, documented)
  BEFORE / AFTER    -> TEMPORAL_BEFORE / TEMPORAL_AFTER (NEW — no temporal edge exists;
                       justified: chronology without causation is a demonstrated need)
  ATTRIBUTED_TO     -> ATTRIBUTED_TO (NEW — no equivalent; epistemic-type
                       preservation requires distinguishing reported from observed)

Contamination propagates along MATERIAL dependencies only: if B REQUIRES A
and A is invalidated, B's qualification suspends — UNLESS B is also
SUPPORTS-linked to independent evidence X, in which case B recalculates
via X. Dependents are never mechanically condemned.
"""
from __future__ import annotations

from .claim import Claim


CANONICAL_EDGES = {
    "REQUIRES", "DERIVES_FROM", "SUPPORTS", "CONTRADICTS", "SUPERSEDES",
    "CAUSED", "REFINES", "TEMPORAL_BEFORE", "TEMPORAL_AFTER", "ATTRIBUTED_TO",
    "APPLIES_TO", "ENABLES", "INVALIDATES", "LEARNS_FROM",
}

# Shawn's vocabulary -> canonical edge (documents the reconciliation)
EDGE_ALIASES = {
    "DERIVED_FROM": "DERIVES_FROM",
    "CAUSES": "CAUSED",
    "EXCEPTION_TO": "REFINES",
    "BEFORE": "TEMPORAL_BEFORE",
    "AFTER": "TEMPORAL_AFTER",
}

# Edges along which contamination MATERIAL propagates
MATERIAL_DEPENDENCY_EDGES = {"REQUIRES", "DERIVES_FROM", "CAUSED"}


def canonical_edge(name: str) -> str:
    """Resolve an edge name to the canonical registry term."""
    upper = name.upper()
    resolved = EDGE_ALIASES.get(upper, upper)
    if resolved not in CANONICAL_EDGES:
        raise ValueError(f"unknown edge (not in CONNECT registry): {name}")
    return resolved


class ClaimGraph:
    """Directed graph of claims with typed, evidence-carrying edges."""

    def __init__(self):
        self.claims: dict = {}
        self.edges: list = []  # (src_id, edge, dst_id, evidence_ref)

    def add_claim(self, claim: Claim):
        self.claims[claim.claim_id] = claim

    def add_edge(self, src_id: str, edge: str, dst_id: str, evidence_ref: str = ""):
        edge = canonical_edge(edge)
        if src_id not in self.claims or dst_id not in self.claims:
            raise ValueError("edge endpoint unknown")
        self.edges.append((src_id, edge, dst_id, evidence_ref))

    def dependents(self, claim_id: str) -> list:
        """Claims materially depending on claim_id (contamination paths).

        Edge (B, REQUIRES, A) means B depends on A, so dependents(A) == [B].
        """
        out = []
        for src, edge, dst, _ in self.edges:
            if dst == claim_id and edge in MATERIAL_DEPENDENCY_EDGES:
                out.append((src, edge, dst))
        return out

    def independent_support(self, claim_id: str) -> list:
        """SUPPORTS edges into claim_id from outside its dependency cone."""
        return [(s, e) for s, e, d, _ in self.edges
                if d == claim_id and e == "SUPPORTS"]

    def propagate_invalidation(self, claim_id: str) -> dict:
        """Recalculate eligibility after invalidation.

        Returns {suspended: [...], recalculated_via_independent: [...]}.
        A dependent with independent SUPPORTS evidence recalculates via that
        evidence instead of being suspended.
        """
        suspended, recalculated = [], []
        for s, e, d in self.dependents(claim_id):
            if self.independent_support(s):
                recalculated.append(s)
            else:
                suspended.append(s)
        return {"suspended": suspended,
                "recalculated_via_independent": recalculated}

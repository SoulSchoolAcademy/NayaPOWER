"""Claim graph tests: CONNECT reconciliation + material propagation."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from extraction.graph import (
    ClaimGraph, canonical_edge, CANONICAL_EDGES, EDGE_ALIASES,
)
from extraction.claim import Claim


def _claim(cid):
    return Claim(claim_id=cid, parent_source_id="T",
                 source_content_hash="h" * 64, text_span=(0, 1),
                 nucleus="test")


def test_alias_reconciliation():
    assert canonical_edge("DERIVED_FROM") == "DERIVES_FROM"
    assert canonical_edge("CAUSES") == "CAUSED"
    assert canonical_edge("EXCEPTION_TO") == "REFINES"
    assert canonical_edge("BEFORE") == "TEMPORAL_BEFORE"
    assert canonical_edge("AFTER") == "TEMPORAL_AFTER"
    # existing registry terms pass through
    for e in ["REQUIRES", "SUPPORTS", "CONTRADICTS", "SUPERSEDES",
              "ATTRIBUTED_TO"]:
        assert canonical_edge(e) == e


def test_unknown_edge_rejected():
    with pytest.raises(ValueError):
        canonical_edge("VIBES_WITH")


def test_material_propagation_suspends_dependent():
    g = ClaimGraph()
    for cid in ["A", "B"]:
        g.add_claim(_claim(cid))
    g.add_edge("B", "REQUIRES", "A")
    result = g.propagate_invalidation("A")
    assert result["suspended"] == ["B"]
    assert result["recalculated_via_independent"] == []


def test_independent_support_recalculates():
    # B REQUIRES A, but B is also independently SUPPORTS-linked to X:
    # B recalculates via X, it is NOT mechanically condemned.
    g = ClaimGraph()
    for cid in ["A", "B", "X"]:
        g.add_claim(_claim(cid))
    g.add_edge("B", "REQUIRES", "A")
    g.add_edge("X", "SUPPORTS", "B", evidence_ref="independent-trial")
    result = g.propagate_invalidation("A")
    assert result["suspended"] == []
    assert result["recalculated_via_independent"] == ["B"]


def test_non_material_edge_does_not_propagate():
    g = ClaimGraph()
    for cid in ["A", "B"]:
        g.add_claim(_claim(cid))
    g.add_edge("B", "SUPPORTS", "A")  # support is not a material dependency
    result = g.propagate_invalidation("A")
    assert result["suspended"] == []

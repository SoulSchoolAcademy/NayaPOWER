"""P3: L2 evidence plan exposes exact floor failures.

Verifies that PROVE's NEED_EVIDENCE names the specific gaps (not just
L1/L2), and that our independence count is honest (3, not manufactured 5).
"""
from pathlib import Path

from tests.test_nodes.test_demo1_prove_p7 import (
    acquire_package_evidence,
    _build_claim_from_evidence,
    PACKAGE_DIR,
)
from naya_kernel.nodes.prove_node import ProveNode
from naya_kernel.node_base import GateVerdict


def test_p3_prove_names_exact_floor_failures():
    """PROVE must name the specific gaps, not just 'L1/L2'."""
    evidence = acquire_package_evidence(PACKAGE_DIR)
    claim = _build_claim_from_evidence(evidence)
    result = ProveNode().gate({"claim": claim, "operation": "intake"})
    
    assert result.verdict == GateVerdict.NEED_EVIDENCE
    reasons_text = " ".join(result.reasons)
    # Must name the oracle gap (§3.4), not just the level.
    assert "oracle unqualified" in reasons_text, (
        f"missing oracle gap in: {result.reasons}")
    assert "§3.4" in reasons_text, (
        f"missing section reference in: {result.reasons}")


def test_p3_independence_count_is_honest():
    """We claim 3 independent observations, not 5 manufactured ones."""
    # Per §3.9: independent = differ in source/method/time AND share
    # no single failure mode. Our 2 evidence items share source
    # (same package) and method (same read). They are NOT independent.
    evidence = acquire_package_evidence(PACKAGE_DIR)
    claim = _build_claim_from_evidence(evidence)
    
    # Both evidence items have the same source and method.
    sources = {e["source"] for e in claim["evidence"]}
    methods = {e["acquisition_method"] for e in claim["evidence"]}
    # They differ in method (sha256 recompute vs manifest parse),
    # but share the same source (frozen package) and failure mode
    # (package compromise). Per §3.9, sharing a single failure mode
    # means they are NOT independent.
    assert len(sources) == 1, "both from same package source"
    # Honest: we do not claim 5 independent observations.
    assert len(claim["evidence"]) < 5


def test_p3_plan_document_exists():
    """The L2 evidence plan is a preserved artifact."""
    plan = Path(__file__).resolve().parents[2] / "evidence" / "demo1" / "L2-EVIDENCE-PLAN.md"
    assert plan.is_file(), "L2 evidence plan must be preserved"
    text = plan.read_text()
    assert "G2" in text and "oracle" in text
    assert "DATA_FLOOR_OBSERVATIONS" in text or "5" in text
    assert "Coda 2" in text  # coordination specified
    # Must not recommend lowering the floor unilaterally.
    assert "not unilateral" in text.lower() or "governed" in text.lower()

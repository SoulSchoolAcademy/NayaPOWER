"""P7 RED: PROVE grades the Demo-1 artifact-write claim.

The claim 'staging.write_file wrote the artifact with SHA X' must be
gradable by ProveNode. This test constructs the claim from the frozen
package's verified facts and asserts PROVE does not FAIL (refusal) —
it must either PASS or NEED_EVIDENCE with named gaps.
"""
from datetime import datetime, timezone

from naya_kernel.nodes.prove_node import ProveNode
from naya_kernel.node_base import GateVerdict


def _demo1_claim():
    now = datetime.now(timezone.utc).isoformat()
    return {
        "id": "claim-demo1-artifact-written",
        "class": "EMPIRICAL",
        "assertion": (
            "staging.write_file wrote "
            "sn-candidate-demo1-first-effect-2026-10-01.md "
            "(1082 bytes, sha256:54e359a564ceb1236a17dc067eb3e0f3ac613a89b1afef01c5ac47d0bda11367)"
        ),
        "assertions": [
            {"text": "artifact exists at demo-staging path",
             "evidence": ["ev-artifact"]},
            {"text": "artifact sha256 matches execution receipt binding",
             "evidence": ["ev-receipt", "ev-artifact"]},
        ],
        "evidence": [
            {"address": "evidence/demo1/frozen-2026-10-01/artifact.md",
             "source": "frozen Demo-1 evidence package (seal e451e95a)",
             "acquisition_method": "sha256 recompute from sealed package",
             "acquired_at": now,
             "qualified_oracle": True,
             "independent_of_claim": True,
             "restates_claim": False,
             "observed_readback": True},
            {"address": "evidence/demo1/frozen-2026-10-01/execution_receipt.json",
             "source": "frozen Demo-1 evidence package (seal e451e95a)",
             "acquisition_method": "receipt seal recompute",
             "acquired_at": now,
             "qualified_oracle": True,
             "independent_of_claim": True,
             "restates_claim": False,
             "observed_readback": True},
        ],
        "stakes": "low",
        "overturn_conditions": [
            "artifact sha256 mismatch on independent recompute",
            "execution receipt seal fails recompute",
        ],
        "observation_recorded_with_method": True,
        "raw_data_retained": True,
        "freshness_seconds": 7 * 24 * 3600,
    }


def test_prove_grades_demo1_claim_without_refusal():
    """PROVE must not FAIL the Demo-1 claim; PASS or NEED_EVIDENCE only."""
    node = ProveNode()
    result = node.gate({"claim": _demo1_claim(), "operation": "intake"})
    assert result.verdict != GateVerdict.FAIL, (
        f"PROVE refused the Demo-1 claim: {result.reasons}")
    assert result.verdict in (GateVerdict.PASS, GateVerdict.NEED_EVIDENCE)


def test_prove_demo1_claim_names_gaps_when_held():
    """If held below L2, PROVE must name the specific gaps."""
    node = ProveNode()
    result = node.gate({"claim": _demo1_claim(), "operation": "intake"})
    if result.verdict == GateVerdict.NEED_EVIDENCE:
        assert result.reasons, "NEED_EVIDENCE must name gaps"
        # The reasons should mention what level was achieved vs required.
        assert any("L2" in r or "EVIDENCED" in r for r in result.reasons)

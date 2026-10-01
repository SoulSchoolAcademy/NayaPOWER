"""RED-1 — the shared V2.1 calculator must decide, not local proxies.

Lane-verified finding (#554 comments 5933756362, 5933738728):
EVOLVE's scoring path computes `score = value - risk` locally
(naya_kernel/nodes/evolve_node.py::_score_candidate) and binds the ratified
config hash. Binding the hash does not prove the shared executable calculator
(kernel/value_calculus.py) performed the decision.

This test FAILS on 42eb0e0c (red). It must PASS after the wiring fix (green):
the node's public propose->evaluate path must invoke the shared calculator.

FROZEN SHA: 42eb0e0c34bafa851d6d5bc124d5f23612240443
"""

import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import kernel.value_calculus as shared_calc
from naya_kernel.nodes.evolve_node import EvolveNode


def test_shared_calculator_decides_evolve_scoring():
    node = EvolveNode()
    result = node.propose({
        "objective": "RED-1 probe: prove the shared calculator decides",
        "change_class": "PARAMETER",
        "proposed_change": "wire _score_candidate to kernel/value_calculus",
        "expected_value": 7.5,
        "blast_radius": "LOCAL",
        "reversibility": 0.8,
        "rollback_plan": {
            "mechanism": "revert the wiring commit",
            "authority": "Naya 4 integration owner",
            "evidence": "red test turns green on the branch",
            "verification": "independent recomputation of the receipt score",
        },
        "authority_requirement": "NONE",
        "future_behavior": "evolve scores come from the shared calculator",
    })
    assert result["decision"] == "PROPOSED", f"setup failed: {result}"
    evolution_id = result["evolution_id"]

    calls = []
    real_evaluate = shared_calc.evaluate_candidates

    def spy(*args, **kwargs):
        calls.append((args, kwargs))
        return real_evaluate(*args, **kwargs)

    with patch.object(shared_calc, "evaluate_candidates", spy):
        outcome = node.evaluate(evolution_id)

    assert outcome.get("decision") not in ("REFUSED", "STALE_PROPOSAL"), (
        f"setup failed: evaluate returned {outcome}"
    )
    assert calls, (
        "RED: the EVOLVE node's propose->evaluate path did not invoke the "
        "shared V2.1 calculator (kernel/value_calculus.evaluate_candidates). "
        "The score was computed locally; binding deciding_config_hash and "
        "calculusConfigHash does not prove the shared calculator decided. "
        "Fix: wire the scoring path to the shared calculator, or explicitly "
        "fence the local computation as PROVISIONAL with lift conditions."
    )

"""Kernel.decide() skeleton — SCAFFOLD (CANDIDATE — NOT RATIFIED — NOT MERGED).

GAP-A closure point. GAP-A: Kernel.decide() currently exercises SELF+LAW only
and disclaims the other seven; the nine-node manifest + gate script were
missing. This skeleton is the structural target: decide() iterates ALL nine
nodes' gates in pipeline order and returns a decision receipt. It is NOT
implemented — every node gate raises NotImplementedError until built.
"""

from __future__ import annotations

from typing import Any, Dict, List

from naya_kernel.node_base import GateResult, GateVerdict
from naya_kernel.nodes import (
    act_node,
    connect_node,
    evolve_node,
    know_node,
    law_node,
    learn_node,
    prove_node,
    self_node,
    verify_node,
)

# Pipeline order per the node specs. NOTE: LEARN's spec declares itself the
# "ninth pipeline responsibility" and EVOLVE "the last", leaving the eighth
# pipeline slot unassigned — an open question for the overnight review.
GATE_ORDER = [
    ("SELF", self_node.SelfNode),
    ("LAW", law_node.LawNode),
    ("ACT", act_node.ActNode),
    ("KNOW", know_node.KnowNode),
    ("PROVE", prove_node.ProveNode),
    ("CONNECT", connect_node.ConnectNode),
    ("VERIFY", verify_node.VerifyNode),
    ("LEARN", learn_node.LearnNode),
    ("EVOLVE", evolve_node.EvolveNode),
]


class Kernel:
    """Nine-node kernel. SCAFFOLD — decide() is not implemented."""

    def __init__(self) -> None:
        self.nodes = {name: cls() for name, cls in GATE_ORDER}

    def decide(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run every node's gate in order; return a decision receipt.

        SCAFFOLD: raises NotImplementedError until all nine node gates are
        implemented against their ratified specs. When implemented, the first
        non-PASS gate short-circuits the pipeline and the receipt records
        exactly which node stopped it and why.
        """
        raise NotImplementedError(
            "Kernel.decide is a SCAFFOLD stub (GAP-A closure target). "
            "Implement after the nine node specs are ratified."
        )

    def gate_all(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """SCAFFOLD: evaluate every gate without short-circuit (future use)."""
        raise NotImplementedError("Kernel.gate_all is a SCAFFOLD stub.")

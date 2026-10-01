"""Smoke test: Kernel skeleton (SCAFFOLD, CANDIDATE)."""
import pytest

from naya_kernel.kernel import GATE_ORDER, Kernel
from naya_kernel.node_base import NodeBase


def test_gate_order_covers_all_nine_nodes():
    names = [name for name, _ in GATE_ORDER]
    assert names == ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT",
                     "VERIFY", "LEARN", "EVOLVE"]


def test_kernel_instantiates_all_nine_nodes():
    kernel = Kernel()
    assert len(kernel.nodes) == 9
    assert all(isinstance(n, NodeBase) for n in kernel.nodes.values())


def test_decide_is_scaffold_stub():
    kernel = Kernel()
    with pytest.raises(NotImplementedError):
        kernel.decide({})
    with pytest.raises(NotImplementedError):
        kernel.gate_all({})

"""Smoke test: connect_node exposes the node interface (stub, CANDIDATE)."""
import pytest

from naya_kernel.node_base import NodeBase
from naya_kernel.nodes import connect_node


def test_module_exposes_node_class():
    assert issubclass(connect_node.ConnectNode, NodeBase)


def test_stub_methods_raise_not_implemented():
    node = connect_node.ConnectNode()
    with pytest.raises(NotImplementedError):
        node.manifest_entry()
    with pytest.raises(NotImplementedError):
        node.gate({})
    with pytest.raises(NotImplementedError):
        node.persisted_transitions()
    with pytest.raises(NotImplementedError):
        node.evidence_hooks()
    with pytest.raises(NotImplementedError):
        node.authority_checks()
    with pytest.raises(NotImplementedError):
        node.cold_reconstruct([])

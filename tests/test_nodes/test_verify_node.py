"""Smoke test: verify_node exposes the node interface (stub, CANDIDATE)."""
import pytest

from naya_kernel.node_base import NodeBase
from naya_kernel.nodes import verify_node


def test_module_exposes_node_class():
    assert issubclass(verify_node.VerifyNode, NodeBase)


def test_stub_methods_raise_not_implemented():
    node = verify_node.VerifyNode()
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

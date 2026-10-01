"""NAYA-KERNEL-CONNECT — STUB (CANDIDATE — NOT RATIFIED — NOT MERGED).

Contractual responsibility, quoted from CONNECT-NODE-SPEC-CANDIDATE.md §0:

CONNECT decides what may be connected to what, under whose consent, and what
context becomes relevant because of it — for knowledge inside one mind and for
minds reaching each other across NayaNET, under one boundary law. It owns the
connection boundary: the rules of what crosses and what never does.

This module is a scaffold only. Every method raises NotImplementedError until
the node is implemented against its ratified spec.
"""

from __future__ import annotations

from naya_kernel.node_base import NodeBase


class ConnectNode(NodeBase):
    """NAYA-KERNEL-CONNECT stub. See module docstring for the contractual responsibility."""

    def manifest_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "ConnectNode.manifest_entry is a SCAFFOLD stub. Implement per "
            "CONNECT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-CONNECT) after ratification."
        )

    def gate(self, *args, **kwargs):
        raise NotImplementedError(
            "ConnectNode.gate is a SCAFFOLD stub. Implement per "
            "CONNECT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-CONNECT) after ratification."
        )

    def persisted_transitions(self, *args, **kwargs):
        raise NotImplementedError(
            "ConnectNode.persisted_transitions is a SCAFFOLD stub. Implement per "
            "CONNECT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-CONNECT) after ratification."
        )

    def evidence_hooks(self, *args, **kwargs):
        raise NotImplementedError(
            "ConnectNode.evidence_hooks is a SCAFFOLD stub. Implement per "
            "CONNECT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-CONNECT) after ratification."
        )

    def authority_checks(self, *args, **kwargs):
        raise NotImplementedError(
            "ConnectNode.authority_checks is a SCAFFOLD stub. Implement per "
            "CONNECT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-CONNECT) after ratification."
        )

    def cold_reconstruct(self, *args, **kwargs):
        raise NotImplementedError(
            "ConnectNode.cold_reconstruct is a SCAFFOLD stub. Implement per "
            "CONNECT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-CONNECT) after ratification."
        )

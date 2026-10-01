"""NAYA-KERNEL-KNOW — STUB (CANDIDATE — NOT RATIFIED — NOT MERGED).

Contractual responsibility, quoted from KNOW-NODE-SPEC-CANDIDATE.md §0:

KNOW is the memory organ: it decides what durable information exists, what is
current, what applies, what is supported, and what is relevant — and it proves
every one of those claims with provenance. ... KNOW is the only node
permitted to persist knowledge into the intelligent graph.

This module is a scaffold only. Every method raises NotImplementedError until
the node is implemented against its ratified spec.
"""

from __future__ import annotations

from naya_kernel.node_base import NodeBase


class KnowNode(NodeBase):
    """NAYA-KERNEL-KNOW stub. See module docstring for the contractual responsibility."""

    def manifest_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "KnowNode.manifest_entry is a SCAFFOLD stub. Implement per "
            "KNOW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-KNOW) after ratification."
        )

    def gate(self, *args, **kwargs):
        raise NotImplementedError(
            "KnowNode.gate is a SCAFFOLD stub. Implement per "
            "KNOW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-KNOW) after ratification."
        )

    def persisted_transitions(self, *args, **kwargs):
        raise NotImplementedError(
            "KnowNode.persisted_transitions is a SCAFFOLD stub. Implement per "
            "KNOW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-KNOW) after ratification."
        )

    def evidence_hooks(self, *args, **kwargs):
        raise NotImplementedError(
            "KnowNode.evidence_hooks is a SCAFFOLD stub. Implement per "
            "KNOW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-KNOW) after ratification."
        )

    def authority_checks(self, *args, **kwargs):
        raise NotImplementedError(
            "KnowNode.authority_checks is a SCAFFOLD stub. Implement per "
            "KNOW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-KNOW) after ratification."
        )

    def cold_reconstruct(self, *args, **kwargs):
        raise NotImplementedError(
            "KnowNode.cold_reconstruct is a SCAFFOLD stub. Implement per "
            "KNOW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-KNOW) after ratification."
        )

"""NAYA-KERNEL-ACT — STUB (CANDIDATE — NOT RATIFIED — NOT MERGED).

Contractual responsibility, quoted from ACT-NODE-SPEC-CANDIDATE.md §0:

ACT is the only node that produces effects in the world. LAW decides; ACT does.
Every authorized decision becomes real through exactly one disciplined path:
claim the execution under an idempotency key, invoke only registered tools
within the granted authority envelope, observe the effects, and emit a receipt
that a cold successor can trust.

This module is a scaffold only. Every method raises NotImplementedError until
the node is implemented against its ratified spec.
"""

from __future__ import annotations

from naya_kernel.node_base import NodeBase


class ActNode(NodeBase):
    """NAYA-KERNEL-ACT stub. See module docstring for the contractual responsibility."""

    def manifest_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "ActNode.manifest_entry is a SCAFFOLD stub. Implement per "
            "ACT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-ACT) after ratification."
        )

    def gate(self, *args, **kwargs):
        raise NotImplementedError(
            "ActNode.gate is a SCAFFOLD stub. Implement per "
            "ACT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-ACT) after ratification."
        )

    def persisted_transitions(self, *args, **kwargs):
        raise NotImplementedError(
            "ActNode.persisted_transitions is a SCAFFOLD stub. Implement per "
            "ACT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-ACT) after ratification."
        )

    def evidence_hooks(self, *args, **kwargs):
        raise NotImplementedError(
            "ActNode.evidence_hooks is a SCAFFOLD stub. Implement per "
            "ACT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-ACT) after ratification."
        )

    def authority_checks(self, *args, **kwargs):
        raise NotImplementedError(
            "ActNode.authority_checks is a SCAFFOLD stub. Implement per "
            "ACT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-ACT) after ratification."
        )

    def cold_reconstruct(self, *args, **kwargs):
        raise NotImplementedError(
            "ActNode.cold_reconstruct is a SCAFFOLD stub. Implement per "
            "ACT-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-ACT) after ratification."
        )

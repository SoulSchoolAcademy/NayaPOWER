"""NAYA-KERNEL-EVOLVE — STUB (CANDIDATE — NOT RATIFIED — NOT MERGED).

Contractual responsibility, quoted from EVOLVE-NODE-SPEC-CANDIDATE.md §0:

EVOLVE is the last semantic responsibility before the cycle returns to SELF.
It answers one question: What should the next generation of this system be —
and can it prove the change is an improvement before it becomes one?

This module is a scaffold only. Every method raises NotImplementedError until
the node is implemented against its ratified spec.
"""

from __future__ import annotations

from naya_kernel.node_base import NodeBase


class EvolveNode(NodeBase):
    """NAYA-KERNEL-EVOLVE stub. See module docstring for the contractual responsibility."""

    def manifest_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "EvolveNode.manifest_entry is a SCAFFOLD stub. Implement per "
            "EVOLVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-EVOLVE) after ratification."
        )

    def gate(self, *args, **kwargs):
        raise NotImplementedError(
            "EvolveNode.gate is a SCAFFOLD stub. Implement per "
            "EVOLVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-EVOLVE) after ratification."
        )

    def persisted_transitions(self, *args, **kwargs):
        raise NotImplementedError(
            "EvolveNode.persisted_transitions is a SCAFFOLD stub. Implement per "
            "EVOLVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-EVOLVE) after ratification."
        )

    def evidence_hooks(self, *args, **kwargs):
        raise NotImplementedError(
            "EvolveNode.evidence_hooks is a SCAFFOLD stub. Implement per "
            "EVOLVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-EVOLVE) after ratification."
        )

    def authority_checks(self, *args, **kwargs):
        raise NotImplementedError(
            "EvolveNode.authority_checks is a SCAFFOLD stub. Implement per "
            "EVOLVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-EVOLVE) after ratification."
        )

    def cold_reconstruct(self, *args, **kwargs):
        raise NotImplementedError(
            "EvolveNode.cold_reconstruct is a SCAFFOLD stub. Implement per "
            "EVOLVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-EVOLVE) after ratification."
        )

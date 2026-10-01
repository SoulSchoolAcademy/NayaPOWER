"""NAYA-KERNEL-PROVE — STUB (CANDIDATE — NOT RATIFIED — NOT MERGED).

Contractual responsibility, quoted from PROVE-NODE-SPEC-CANDIDATE.md §0:

PROVE is the organism checking its own work before anything it believes is
allowed to leave it. ... UNKNOWN, BLOCKED, and IMPLEMENTED never count as
VERIFIED; only evidence does, and PROVE is the node that enforces the
difference mechanically.

This module is a scaffold only. Every method raises NotImplementedError until
the node is implemented against its ratified spec.
"""

from __future__ import annotations

from naya_kernel.node_base import NodeBase


class ProveNode(NodeBase):
    """NAYA-KERNEL-PROVE stub. See module docstring for the contractual responsibility."""

    def manifest_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "ProveNode.manifest_entry is a SCAFFOLD stub. Implement per "
            "PROVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-PROVE) after ratification."
        )

    def gate(self, *args, **kwargs):
        raise NotImplementedError(
            "ProveNode.gate is a SCAFFOLD stub. Implement per "
            "PROVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-PROVE) after ratification."
        )

    def persisted_transitions(self, *args, **kwargs):
        raise NotImplementedError(
            "ProveNode.persisted_transitions is a SCAFFOLD stub. Implement per "
            "PROVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-PROVE) after ratification."
        )

    def evidence_hooks(self, *args, **kwargs):
        raise NotImplementedError(
            "ProveNode.evidence_hooks is a SCAFFOLD stub. Implement per "
            "PROVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-PROVE) after ratification."
        )

    def authority_checks(self, *args, **kwargs):
        raise NotImplementedError(
            "ProveNode.authority_checks is a SCAFFOLD stub. Implement per "
            "PROVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-PROVE) after ratification."
        )

    def cold_reconstruct(self, *args, **kwargs):
        raise NotImplementedError(
            "ProveNode.cold_reconstruct is a SCAFFOLD stub. Implement per "
            "PROVE-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-PROVE) after ratification."
        )

"""NAYA-KERNEL-VERIFY — STUB (CANDIDATE — NOT RATIFIED — NOT MERGED).

Contractual responsibility, quoted from VERIFY-NODE-SPEC-CANDIDATE.md §0:

VERIFY is the organism's immune system: the independent seat that re-derives,
attacks, and closes. ... Nothing is learned from, evolved from, or compounded
on that VERIFY has not closed.

This module is a scaffold only. Every method raises NotImplementedError until
the node is implemented against its ratified spec.
"""

from __future__ import annotations

from naya_kernel.node_base import NodeBase


class VerifyNode(NodeBase):
    """NAYA-KERNEL-VERIFY stub. See module docstring for the contractual responsibility."""

    def manifest_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "VerifyNode.manifest_entry is a SCAFFOLD stub. Implement per "
            "VERIFY-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-VERIFY) after ratification."
        )

    def gate(self, *args, **kwargs):
        raise NotImplementedError(
            "VerifyNode.gate is a SCAFFOLD stub. Implement per "
            "VERIFY-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-VERIFY) after ratification."
        )

    def persisted_transitions(self, *args, **kwargs):
        raise NotImplementedError(
            "VerifyNode.persisted_transitions is a SCAFFOLD stub. Implement per "
            "VERIFY-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-VERIFY) after ratification."
        )

    def evidence_hooks(self, *args, **kwargs):
        raise NotImplementedError(
            "VerifyNode.evidence_hooks is a SCAFFOLD stub. Implement per "
            "VERIFY-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-VERIFY) after ratification."
        )

    def authority_checks(self, *args, **kwargs):
        raise NotImplementedError(
            "VerifyNode.authority_checks is a SCAFFOLD stub. Implement per "
            "VERIFY-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-VERIFY) after ratification."
        )

    def cold_reconstruct(self, *args, **kwargs):
        raise NotImplementedError(
            "VerifyNode.cold_reconstruct is a SCAFFOLD stub. Implement per "
            "VERIFY-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-VERIFY) after ratification."
        )

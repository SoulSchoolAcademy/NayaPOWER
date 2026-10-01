"""NAYA-KERNEL-LEARN — STUB (CANDIDATE — NOT RATIFIED — NOT MERGED).

Contractual responsibility, quoted from LEARN-NODE-SPEC-CANDIDATE.md §0:

LEARN decides what should change because of a verified outcome, under what
applicability conditions — and proves the change by measuring future behavior
difference attributable to the retained intelligence. ... LEARN is the only node
permitted to propose persistent changes to future behavior, and every proposal
is scored with the Decision Value Calculus V2.1 before it is allowed to persist.

This module is a scaffold only. Every method raises NotImplementedError until
the node is implemented against its ratified spec.
"""

from __future__ import annotations

from naya_kernel.node_base import NodeBase


class LearnNode(NodeBase):
    """NAYA-KERNEL-LEARN stub. See module docstring for the contractual responsibility."""

    def manifest_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "LearnNode.manifest_entry is a SCAFFOLD stub. Implement per "
            "LEARN-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LEARN) after ratification."
        )

    def gate(self, *args, **kwargs):
        raise NotImplementedError(
            "LearnNode.gate is a SCAFFOLD stub. Implement per "
            "LEARN-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LEARN) after ratification."
        )

    def persisted_transitions(self, *args, **kwargs):
        raise NotImplementedError(
            "LearnNode.persisted_transitions is a SCAFFOLD stub. Implement per "
            "LEARN-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LEARN) after ratification."
        )

    def evidence_hooks(self, *args, **kwargs):
        raise NotImplementedError(
            "LearnNode.evidence_hooks is a SCAFFOLD stub. Implement per "
            "LEARN-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LEARN) after ratification."
        )

    def authority_checks(self, *args, **kwargs):
        raise NotImplementedError(
            "LearnNode.authority_checks is a SCAFFOLD stub. Implement per "
            "LEARN-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LEARN) after ratification."
        )

    def cold_reconstruct(self, *args, **kwargs):
        raise NotImplementedError(
            "LearnNode.cold_reconstruct is a SCAFFOLD stub. Implement per "
            "LEARN-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LEARN) after ratification."
        )

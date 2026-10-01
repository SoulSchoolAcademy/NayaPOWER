"""NAYA-KERNEL-SELF — STUB (CANDIDATE — NOT RATIFIED — NOT MERGED).

Contractual responsibility, quoted from SELF-NODE-SPEC-CANDIDATE.md §0:

SELF answers three questions before anything else is allowed to happen: who is
acting, under what identity and mission, and what durable state may safely
continue? ... Every pipeline cycle begins at SELF; nothing downstream (LAW, ACT,
and the rest) may execute until SELF reaches READY.

This module is a scaffold only. Every method raises NotImplementedError until
the node is implemented against its ratified spec.
"""

from __future__ import annotations

from naya_kernel.node_base import NodeBase


class SelfNode(NodeBase):
    """NAYA-KERNEL-SELF stub. See module docstring for the contractual responsibility."""

    def manifest_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "SelfNode.manifest_entry is a SCAFFOLD stub. Implement per "
            "SELF-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-SELF) after ratification."
        )

    def gate(self, *args, **kwargs):
        raise NotImplementedError(
            "SelfNode.gate is a SCAFFOLD stub. Implement per "
            "SELF-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-SELF) after ratification."
        )

    def persisted_transitions(self, *args, **kwargs):
        raise NotImplementedError(
            "SelfNode.persisted_transitions is a SCAFFOLD stub. Implement per "
            "SELF-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-SELF) after ratification."
        )

    def evidence_hooks(self, *args, **kwargs):
        raise NotImplementedError(
            "SelfNode.evidence_hooks is a SCAFFOLD stub. Implement per "
            "SELF-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-SELF) after ratification."
        )

    def authority_checks(self, *args, **kwargs):
        raise NotImplementedError(
            "SelfNode.authority_checks is a SCAFFOLD stub. Implement per "
            "SELF-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-SELF) after ratification."
        )

    def cold_reconstruct(self, *args, **kwargs):
        raise NotImplementedError(
            "SelfNode.cold_reconstruct is a SCAFFOLD stub. Implement per "
            "SELF-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-SELF) after ratification."
        )

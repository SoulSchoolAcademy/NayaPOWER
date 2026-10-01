"""NAYA-KERNEL-LAW — STUB (CANDIDATE — NOT RATIFIED — NOT MERGED).

Contractual responsibility, quoted from LAW-NODE-SPEC-CANDIDATE.md §0:

LAW is the organism's conscience made mechanical. Every proposed action must
pass through LAW before it can be executed, scored, learned from, or evolved.
LAW holds no authority of its own; it validates authority claims against the
Constitution, applies the four-valued gate structure with hard stops that no
principal can override, and refuses known-wrong instructions even when they
come from the Human Director himself.

This module is a scaffold only. Every method raises NotImplementedError until
the node is implemented against its ratified spec.
"""

from __future__ import annotations

from naya_kernel.node_base import NodeBase


class LawNode(NodeBase):
    """NAYA-KERNEL-LAW stub. See module docstring for the contractual responsibility."""

    def manifest_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "LawNode.manifest_entry is a SCAFFOLD stub. Implement per "
            "LAW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LAW) after ratification."
        )

    def gate(self, *args, **kwargs):
        raise NotImplementedError(
            "LawNode.gate is a SCAFFOLD stub. Implement per "
            "LAW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LAW) after ratification."
        )

    def persisted_transitions(self, *args, **kwargs):
        raise NotImplementedError(
            "LawNode.persisted_transitions is a SCAFFOLD stub. Implement per "
            "LAW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LAW) after ratification."
        )

    def evidence_hooks(self, *args, **kwargs):
        raise NotImplementedError(
            "LawNode.evidence_hooks is a SCAFFOLD stub. Implement per "
            "LAW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LAW) after ratification."
        )

    def authority_checks(self, *args, **kwargs):
        raise NotImplementedError(
            "LawNode.authority_checks is a SCAFFOLD stub. Implement per "
            "LAW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LAW) after ratification."
        )

    def cold_reconstruct(self, *args, **kwargs):
        raise NotImplementedError(
            "LawNode.cold_reconstruct is a SCAFFOLD stub. Implement per "
            "LAW-NODE-SPEC-CANDIDATE.md (NAYA-KERNEL-LAW) after ratification."
        )

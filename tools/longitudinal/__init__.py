"""C5 longitudinal proof — distillation-quality instruments.

Each module measures one compounding component (see
BRAIN/00-ACTIVATION/C5-DISTILLATION-QUALITY-DESIGN-V1.md):

- cold_retrieval_drill (C5.3): cold retrieval precision on contributed knowledge
- recurrence_scan      (C5.4): behavioral-change evidence via failure-class scan
- chain_record         (C5.5): lesson→outcome chain recording + verification
- enforcement_audit    (C5.6): mechanical enforcement rate for new laws
- contribution_review  (C5.7): contribution signal integrity (anti-gaming)

(C5.1 note_integration_rate and C5.2 citation_graph live on the same package
path once their PR merges; union the __all__ lists at that merge.)

Privacy-architectural rule for every instrument here: inputs are
deliberately-contributed artifacts only (notes manifests, promotion receipts,
repo paths). There is no input channel for private communications; these tools
cannot consume DMs, private messages, or unshared drafts by construction.
"""

__all__ = [
    "cold_retrieval_drill",
    "recurrence_scan",
    "chain_record",
    "enforcement_audit",
    "contribution_review",
]

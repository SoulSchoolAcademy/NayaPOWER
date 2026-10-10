"""C5 longitudinal proof — distillation-quality instruments.

Each module measures one compounding component (see
BRAIN/00-ACTIVATION/C5-DISTILLATION-QUALITY-DESIGN-V1.md):

- note_integration_rate (C5.1): Smart Note -> doctrine integration rate
- citation_graph        (C5.2): cross-seat citation / reuse graph

Privacy-architectural rule for every instrument here: inputs are
deliberately-contributed artifacts only (notes manifests, promotion receipts,
repo paths). There is no input channel for private communications; these tools
cannot consume DMs, private messages, or unshared drafts by construction.
"""

__all__ = ["note_integration_rate", "citation_graph"]

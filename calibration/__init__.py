"""Risk-calibrated interpretation reopening.

Extends the reopening spec (four objects, five states, ten triggers) with
the calibration layer: three-gate thresholds, cost-based decisions,
four-layer architecture, hierarchical risk model, offline study protocol.

Governing principle: when evidence is scarce, uncertainty increases
caution — not invented confidence.
"""

from . import gates, cost, architecture, hierarchical, study

__all__ = ["gates", "cost", "architecture", "hierarchical", "study"]

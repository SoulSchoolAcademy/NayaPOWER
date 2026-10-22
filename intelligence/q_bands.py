"""Canonical Q -> band labeler (display-layer contract).

The value-calculus spec defines score bands only in prose
(NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md):

    - 9.5-10.0 DELIGHT
    - 9.0-<9.5 ACCEPT
    - 7.0-<9.0 BELOW STANDARD
    - <7.0 REJECT / REWORK

The kernel (kernel/value_calculus.py) implements scoring only; the one
"BELOW_STANDARD" string there is a different domain's status tuple
(next-best-action gating: ("BELOW_STANDARD", "QUALITY_FLOOR")) and is
NOT this band. This module is the single canonical mapping so every
consumer renders the same label for the same scalar Q.

Display-layer only: it never alters scoring, gating, or autonomy caps.
"""

from __future__ import annotations

import math
from typing import Union

Number = Union[int, float]

# Canonical band table, verbatim from the spec. Each row: (name, lo, hi).
# Interval semantics: lo <= Q <= hi, EXCEPT the upper bound is exclusive
# wherever the spec writes "<x" (ACCEPT, BELOW_STANDARD, REJECT_REWORK).
BANDS: tuple[tuple[str, float, float, bool], ...] = (
    # (name, lo, hi, hi_inclusive)
    ("DELIGHT", 9.5, 10.0, True),        # 9.5-10.0 DELIGHT
    ("ACCEPT", 9.0, 9.5, False),         # 9.0-<9.5 ACCEPT
    ("BELOW_STANDARD", 7.0, 9.0, False),  # 7.0-<9.0 BELOW STANDARD
    ("REJECT_REWORK", 0.0, 7.0, False),  # <7.0 REJECT / REWORK
)

SPEC_PATH = "NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md"


def label_band(q: Number) -> str:
    """Return the canonical band name for scalar quality score Q.

    Boundary pins (from the spec): 9.5 -> DELIGHT, 9.0 -> ACCEPT,
    7.0 -> BELOW_STANDARD, 10.0 -> DELIGHT.

    Domain: finite numbers in [0, 10]. Anything else raises ValueError
    rather than silently mislabeling: a 10.7 is not DELIGHT, and NaN
    has no band. Booleans are rejected (they are not scores).
    """
    if isinstance(q, bool) or not isinstance(q, (int, float)):
        raise ValueError(f"Q must be a number, got {type(q).__name__}")
    if not math.isfinite(q):
        raise ValueError(f"Q must be finite, got {q!r}")
    if not 0.0 <= q <= 10.0:
        raise ValueError(f"Q must be in [0, 10], got {q!r}")

    for name, lo, hi, hi_inclusive in BANDS:
        if q >= lo and (q < hi or (hi_inclusive and q == hi)):
            return name
    raise AssertionError(f"unreachable: Q={q!r} matched no band")  # pragma: no cover


def band_table() -> list[dict[str, object]]:
    """Return the canonical band table for consumers to render from.

    Shape: [{"name": str, "lo": float, "hi": float, "hi_inclusive": bool,
             "spec": str}], ordered DELIGHT -> REJECT_REWORK.
    """
    return [
        {"name": name, "lo": lo, "hi": hi, "hi_inclusive": hi_inclusive,
         "spec": SPEC_PATH}
        for name, lo, hi, hi_inclusive in BANDS
    ]

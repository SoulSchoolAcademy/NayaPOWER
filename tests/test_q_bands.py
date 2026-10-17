"""Tests for the canonical Q -> band labeler (intelligence/q_bands.py).

Boundary pins are verbatim from the spec
(NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md):
  9.5-10.0 DELIGHT / 9.0-<9.5 ACCEPT / 7.0-<9.0 BELOW STANDARD / <7.0 REJECT/REWORK
"""

import math

import pytest

from intelligence.q_bands import BANDS, SPEC_PATH, band_table, label_band


def test_boundary_pins():
    assert label_band(9.5) == "DELIGHT"
    assert label_band(10.0) == "DELIGHT"
    assert label_band(9.0) == "ACCEPT"
    assert label_band(7.0) == "BELOW_STANDARD"
    assert label_band(0.0) == "REJECT_REWORK"
    assert label_band(6.999999) == "REJECT_REWORK"


def test_just_below_boundaries():
    # float noise just under a boundary must NOT round up into the higher band
    assert label_band(9.499999999999998) == "ACCEPT"
    assert label_band(8.999999999999998) == "BELOW_STANDARD"
    assert label_band(6.999999999999998) == "REJECT_REWORK"


def test_interior_values():
    assert label_band(9.75) == "DELIGHT"
    assert label_band(9.2) == "ACCEPT"
    assert label_band(8.0) == "BELOW_STANDARD"
    assert label_band(3.5) == "REJECT_REWORK"


def test_int_inputs():
    assert label_band(9) == "ACCEPT"
    assert label_band(10) == "DELIGHT"


def test_out_of_domain_raises():
    for bad in (-0.1, 10.0000001, 11.0, math.nan, math.inf, -math.inf,
                "9.5", None, True):
        with pytest.raises(ValueError):
            label_band(bad)


def test_band_table_shape():
    t = band_table()
    assert [r["name"] for r in t] == [b[0] for b in BANDS]
    assert all(r["spec"] == SPEC_PATH for r in t)
    # boundaries cover [0,10] contiguously with no gaps
    # boundaries cover [0,10] contiguously with no gaps (order-independent)
    bounds = sorted((r["lo"], r["hi"]) for r in t)
    assert bounds[0][0] == 0.0 and bounds[-1][1] == 10.0
    for ( _, hi), (lo, _) in zip(bounds, bounds[1:]):
        assert hi == lo

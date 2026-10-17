"""Retrieval floor discrimination gate — RED-FIRST (Naya Narzan, 2026-10-13).

A relevance floor is admissible only when the labeled positive and negative
query classes SEPARATE (min positive top-1 > max negative top-1 + margin).
Measured 2026-10-13 at tip 582e5e5f: they overlap (best false positive
23.95 > weakest true positive 18.80), so NO floor value can currently admit
true positives while refusing false positives. This test is RED until the
applicability/relevance discrimination fix lands. It must NOT be "fixed" by
editing the battery's labels or the margin — only by a discrimination change
that genuinely separates the classes.
"""
import runpy
import sys
from pathlib import Path

import pytest

BATTERY = Path(__file__).resolve().parent.parent / "tools" / "retrieval_calibration_battery.py"


def _run_battery():
    """Run the battery in-process; returns (exit_code, stdout_text)."""
    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    saved = sys.argv
    sys.argv = ["retrieval_calibration_battery.py"]
    try:
        with redirect_stdout(buf):
            try:
                runpy.run_path(str(BATTERY), run_name="__main__")
                code = 0
            except SystemExit as e:
                code = int(e.code or 0)
    finally:
        sys.argv = saved
    return code, buf.getvalue()


def test_relevance_floor_discrimination():
    code, out = _run_battery()
    assert code == 0, (
        "RETRIEVAL FLOOR DISCRIMINATION RED:\n" + out
        + "\nThe relevance floor cannot separate true positives from false "
        "positives. Fix discrimination (applicability/relevance scoring), "
        "not the floor value or this test."
    )

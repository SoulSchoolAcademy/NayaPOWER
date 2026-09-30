"""Tests for the EVOLVE cold-start probe."""

import importlib.util
import re
from pathlib import Path

import pytest

PROBE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "cold-start-probe.py"


def load_probe():
    spec = importlib.util.spec_from_file_location("cold_start_probe", PROBE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_required_facts_list_is_nonempty():
    probe = load_probe()
    assert len(probe.REQUIRED_FACTS) >= 8, "probe must check a meaningful fact set"


def test_probe_patterns_catch_gutted_continuity():
    """A successor with empty continuity files must fail the probe."""
    probe = load_probe()
    gutted = "# empty torch\n"
    missing = [
        name
        for name, pattern, _ in probe.REQUIRED_FACTS
        if not re.search(pattern, gutted, re.IGNORECASE | re.DOTALL)
    ]
    assert len(missing) == len(probe.REQUIRED_FACTS), (
        f"probe must fail on empty continuity files; only {len(missing)}/"
        f"{len(probe.REQUIRED_FACTS)} flagged"
    )


def test_probe_passes_on_real_continuity_files():
    """Against the live workspace files the probe must pass (or the test
    environment lacks the files — in which case the test reports why)."""
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, str(PROBE_PATH)], capture_output=True, text=True
    )
    assert result.returncode == 0, (
        f"cold-start probe failed on live continuity files:\n{result.stdout}\n{result.stderr}"
    )
    assert "COLD-START PROBE PASS" in result.stdout

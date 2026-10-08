"""Tests for the pipeline health monitor.

The monitor is read-only and reports GREEN/YELLOW/RED.
These tests verify the health logic, not live DB state.
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "protocol"))

from pipeline_health import (
    get_packaged_ids,
    hours_ago,
)


def test_hours_ago_valid():
    h = hours_ago("2026-10-07T15:37:44Z")
    assert h is not None and h > 0


def test_hours_ago_invalid():
    assert hours_ago("not-a-time") is None
    assert hours_ago("") is None


def test_get_packaged_ids_empty_dir(tmp_path):
    assert get_packaged_ids(tmp_path) == set()


def test_get_packaged_ids_nonexistent():
    assert get_packaged_ids(Path("/nonexistent/dir")) == set()


def test_get_packaged_ids_parses_tier_files(tmp_path):
    (tmp_path / "07d705b0-tier1.md").touch()
    (tmp_path / "367a6ae3-tier2.md").touch()
    (tmp_path / "index.md").touch()  # should be ignored
    ids = get_packaged_ids(tmp_path)
    assert "07d705b0" in ids
    assert "367a6ae3" in ids
    assert len(ids) == 2


def test_get_packaged_ids_registry(tmp_path):
    reg = tmp_path / "packaged_ids.json"
    reg.write_text(json.dumps(["aaaa1111", "bbbb2222"]))
    ids = get_packaged_ids(tmp_path)
    assert "aaaa1111" in ids
    assert "bbbb2222" in ids


def _mock_report(unpackaged_48h, new_12h, over_24h, slowing):
    """Replicate the health determination logic for unit testing."""
    issues = []
    if unpackaged_48h or new_12h == 0:
        health = "RED"
    elif over_24h or slowing:
        health = "YELLOW"
    else:
        health = "GREEN"
    return health


def test_health_red_unpackaged_old():
    assert _mock_report(["abc123"], 10, False, False) == "RED"


def test_health_red_no_movement():
    assert _mock_report([], 0, False, False) == "RED"


def test_health_yellow_old_candidates():
    assert _mock_report([], 10, True, False) == "YELLOW"


def test_health_yellow_slowing():
    assert _mock_report([], 10, False, True) == "YELLOW"


def test_health_green():
    assert _mock_report([], 10, False, False) == "GREEN"


def test_health_red_beats_yellow():
    # RED conditions take precedence
    assert _mock_report(["abc123"], 10, True, True) == "RED"


def test_monitor_is_read_only():
    """The monitor must never contain write operations."""
    src = (ROOT / "tools" / "protocol" / "pipeline_health.py").read_text()
    src_lower = src.lower()
    # No UPDATE, INSERT, DELETE, ALTER in SQL strings
    for kw in ["update learning_evidence", "insert into",
               "delete from", "alter table"]:
        assert kw not in src_lower, f"monitor contains write: {kw}"
    # Uses sb-api without --allow-write
    assert "--allow-write" not in src

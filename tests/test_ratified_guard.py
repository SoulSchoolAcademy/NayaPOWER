"""Tests for tools/ratified_guard.py (SN-0408 enforcement).

The critical property: a diff that deletes a ratified object without a
retirement record MUST fail. Everything else must pass.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from ratified_guard import (  # noqa: E402
    build_manifest,
    check_diff,
    is_ratified_capture,
    is_ratified_markdown,
)

V2_RATIFIED = {
    "schema": "naya.smart-note-capture.v2",
    "capture_id": "SMART-NOTE-20261005-sn9999-test",
    "smart_note_id": "SN-9999",
    "source": {"ratification": {"by": "Shawn Vibert", "at": "2026-10-05"}},
    "lifecycle_state": "ACTIVE",
}

V2_UNRATIFIED = {
    "schema": "naya.smart-note-capture.v2",
    "capture_id": "SMART-NOTE-20261005-sn9998-test",
    "smart_note_id": "SN-9998",
    "source": {},
    "lifecycle_state": "ACTIVE",
}

V1_RATIFIED = {"schema": "naya.smart-note-capture.v1", "truth_state": "RATIFIED"}


@pytest.fixture()
def tree(tmp_path: Path) -> Path:
    cap = tmp_path / ".naya" / "capture"
    cap.mkdir(parents=True)
    (cap / "ratified-v2.json").write_text(json.dumps(V2_RATIFIED))
    (cap / "plain-v2.json").write_text(json.dumps(V2_UNRATIFIED))
    (cap / "ratified-v1.json").write_text(json.dumps(V1_RATIFIED))
    (cap / "broken.json").write_text("{not json")
    brain = tmp_path / "BRAIN" / "01-GOVERNANCE"
    brain.mkdir(parents=True)
    (brain / "law.md").write_text("# Law\n- **Truth state:** RATIFIED\n")
    (brain / "draft.md").write_text("# Draft\n- **Truth state:** CANDIDATE\n")
    return tmp_path


def test_manifest_finds_ratified_captures(tree: Path):
    manifest = build_manifest(tree)
    assert ".naya/capture/ratified-v2.json" in manifest
    assert ".naya/capture/ratified-v1.json" in manifest
    assert "BRAIN/01-GOVERNANCE/law.md" in manifest


def test_manifest_ignores_unratified_and_broken(tree: Path):
    manifest = build_manifest(tree)
    assert ".naya/capture/plain-v2.json" not in manifest
    assert ".naya/capture/broken.json" not in manifest
    assert "BRAIN/01-GOVERNANCE/draft.md" not in manifest


def test_no_deletions_passes(tree: Path):
    manifest = build_manifest(tree)
    assert check_diff(manifest, [], []) == []


def test_delete_ratified_fails(tree: Path):
    """THE critical property: deleting a ratified object without a
    retirement record must fail."""
    manifest = build_manifest(tree)
    violations = check_diff(manifest, [".naya/capture/ratified-v2.json"], [])
    assert len(violations) == 1
    assert "ratified-v2.json" in violations[0]


def test_delete_unratified_passes(tree: Path):
    manifest = build_manifest(tree)
    assert check_diff(manifest, [".naya/capture/plain-v2.json"], []) == []


def test_delete_ratified_with_retirement_record_passes(tree: Path):
    manifest = build_manifest(tree)
    violations = check_diff(
        manifest,
        [".naya/capture/ratified-v2.json"],
        ["RATIFIED-RETIREMENT-SN-9999.md"],
    )
    assert violations == []


def test_is_ratified_capture_variants():
    assert is_ratified_capture(V2_RATIFIED)
    assert is_ratified_capture(V1_RATIFIED)
    assert is_ratified_capture({"truth_state": "IMMUTABLE"})
    assert not is_ratified_capture(V2_UNRATIFIED)
    assert not is_ratified_capture({})
    assert not is_ratified_capture(None)


def test_is_ratified_markdown():
    assert is_ratified_markdown("- **Truth state:** RATIFIED")
    assert not is_ratified_markdown("- **Truth state:** CANDIDATE")

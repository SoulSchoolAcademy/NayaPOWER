"""Fail-closed static GT-039 client compatibility evidence.

No test here authorizes a deployment. A successful test run only proves that
the dangerous mismatch is *detected*, not that visitor mail works.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import preflight_gt039_mail_clients as preflight  # noqa: E402


def test_pending_revoke_breaks_committed_visitor_mail_client_contract() -> None:
    result = preflight.evaluate()
    assert result["verdict"] == "BLOCKED_MAIL_CLIENT_COMPAT"
    assert result["no_release_approval"] is True
    assert result["booking_reminder_rest_insert_found"] is True
    paths = {p["path"] for p in result["affected_browser_sources"]}
    assert paths == set(preflight.CLIENT_FILES)
    assert all(p["features"]["requires_returned_thread_id"]
               for p in result["affected_browser_sources"])


def fixture_tree(tmp_path: Path) -> Path:
    for name in (*preflight.CLIENT_FILES, preflight.BOOKING_FILE, preflight.MIGRATION):
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / name, target)
    return tmp_path


def test_removing_revoke_does_not_clear_gate(tmp_path: Path) -> None:
    tree = fixture_tree(tmp_path)
    sql = tree / preflight.MIGRATION
    source = sql.read_text(encoding="utf-8")
    assert preflight.REVOKE.search(source)
    sql.write_text(preflight.REVOKE.sub("-- deliberately removed", source), encoding="utf-8")
    with pytest.raises(preflight.PreflightError, match="SECURITY_REVOKE_CONTRACT_MISSING"):
        preflight.evaluate(tree)


def test_missing_client_source_fails_closed(tmp_path: Path) -> None:
    tree = fixture_tree(tmp_path)
    (tree / preflight.CLIENT_FILES[0]).unlink()
    with pytest.raises(preflight.PreflightError, match="REQUIRED_SOURCE_UNAVAILABLE"):
        preflight.evaluate(tree)


def test_no_detected_direct_visitors_is_still_not_pass(tmp_path: Path) -> None:
    tree = fixture_tree(tmp_path)
    for name in preflight.CLIENT_FILES:
        file = tree / name
        file.write_text("/* replaced with authenticated server side intent */\n",
                        encoding="utf-8")
    result = preflight.evaluate(tree)
    assert result["verdict"] == "UNKNOWN_RUNTIME_COMPATIBILITY"
    assert result["booking_reminder_requires_independent_functional_proof"] is True
    assert result["no_release_approval"] is True


def test_missing_all_client_paths_fails_closed(tmp_path: Path) -> None:
    tree = fixture_tree(tmp_path)
    for name in (*preflight.CLIENT_FILES, preflight.BOOKING_FILE):
        file = tree / name
        file.write_text("/* no verified mail client */\n", encoding="utf-8")
    with pytest.raises(preflight.PreflightError, match="CLIENT_PATHS_NOT_FOUND"):
        preflight.evaluate(tree)

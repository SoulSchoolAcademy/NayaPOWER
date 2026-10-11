"""Tests that the executable boot/cycle entry point fails closed."""
import json

import pytest

from tools.protocol import cold_start_gate as gate


def _stub_static_checks(monkeypatch):
    monkeypatch.setattr(gate, "check_manifest_valid", lambda _m: (True, "ok"))
    monkeypatch.setattr(gate, "check_tip_resolvable", lambda: (True, "main reachable"))
    monkeypatch.setattr(gate, "check_law_ids_unique", lambda _m: (True, "unique"))
    monkeypatch.setattr(gate, "check_conflict_hierarchy_complete", lambda _m: (True, "complete"))
    monkeypatch.setattr(gate, "check_truth_states_distinct", lambda _m: (True, "distinct"))
    monkeypatch.setattr(gate, "check_never_do_nonempty", lambda _m: (True, "complete"))
    monkeypatch.setattr(gate, "resolve_current_main_sha", lambda: "a" * 40)


def test_activate_fails_closed_without_read_and_signin_receipts(monkeypatch):
    _stub_static_checks(monkeypatch)
    result = gate.run_gate(agent_id="naya-test", mode="activate")
    assert not result["pass"]
    failed = {item["name"] for item in result["failures"]}
    assert "read_comprehension_receipt" in failed
    assert "live_feed_sign_in" in failed


def test_close_fails_closed_without_same_cycle_receipts(monkeypatch):
    _stub_static_checks(monkeypatch)
    result = gate.run_gate(agent_id="naya-test", mode="close")
    assert not result["pass"]
    assert any(
        item["name"] == "cycle_sign_out" and not item["pass"]
        for item in result["failures"]
    )


def test_comment_fetch_rejects_body_mismatch(monkeypatch):
    class FakeResponse:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self):
            return json.dumps({
                "html_url": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1867#issuecomment-99",
                "body": "different body",
                "issue_url": "https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER/issues/1867",
            }).encode("utf-8")

    monkeypatch.setattr(gate.urllib.request, "urlopen", lambda *_a, **_k: FakeResponse())
    record = {
        "feed_issue": 1867,
        "comment_id": "99",
        "comment_url": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1867#issuecomment-99",
        "comment_body": "expected body",
    }
    with pytest.raises(ValueError, match="differs from the actual"):
        gate.fetch_actual_github_comment(record, "test-token")

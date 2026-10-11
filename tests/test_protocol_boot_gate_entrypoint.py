"""Acceptance tests for the executable protocol activation and cycle-close gate."""
import hashlib
import json

import pytest

from tools.protocol import cold_start_gate as gate


def _stub_integrity(monkeypatch):
    monkeypatch.setattr(gate, "load_manifest", lambda: {"laws": [], "protected_gates": [1, 2, 3, 4, 5], "truth_states": [], "operating_loop": [], "never_do": ["x"] * 10, "law_conflict_hierarchy": ["protected_gates"], "cold_start_required": ["x"]})
    monkeypatch.setattr(gate, "check_manifest_valid", lambda _m: (True, "valid"))
    monkeypatch.setattr(gate, "check_tip_resolvable", lambda: (True, "main reachable"))
    monkeypatch.setattr(gate, "check_law_ids_unique", lambda _m: (True, "unique"))
    monkeypatch.setattr(gate, "check_conflict_hierarchy_complete", lambda _m: (True, "complete"))
    monkeypatch.setattr(gate, "check_truth_states_distinct", lambda _m: (True, "distinct"))
    monkeypatch.setattr(gate, "check_never_do_nonempty", lambda _m: (True, "complete"))
    monkeypatch.setattr(gate, "resolve_current_main_sha", lambda: "a" * 40)


def test_activation_fails_closed_without_comprehension_and_signin(monkeypatch):
    _stub_integrity(monkeypatch)
    result = gate.run_gate(agent_id="naya-test", mode="activate")
    assert result["pass"] is False
    failed = {item["name"] for item in result["failures"]}
    assert "read_comprehension_receipt" in failed
    assert "live_feed_sign_in" in failed


def test_cycle_close_fails_closed_without_signin_signout_and_token(monkeypatch):
    _stub_integrity(monkeypatch)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    result = gate.run_gate(agent_id="naya-test", mode="close")
    assert result["pass"] is False
    assert any(item["name"] == "cycle_sign_out" for item in result["failures"])


def test_actual_comment_fetch_rejects_body_mismatch(monkeypatch):
    body = "<!-- NAYA-WORK-CYCLE-RECEIPT:START -->{}<!-- NAYA-WORK-CYCLE-RECEIPT:END -->"

    class FakeResponse:
        def __enter__(self):
            return self
        def __exit__(self, *_args):
            return False
        def read(self):
            return json.dumps({
                "html_url": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1867#issuecomment-123",
                "issue_url": "https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER/issues/1867",
                "body": body,
            }).encode("utf-8")

    monkeypatch.setattr(gate.urllib.request, "urlopen", lambda *_a, **_k: FakeResponse())
    wrong = {
        "feed_issue": 1867,
        "comment_id": "123",
        "comment_body": "different body",
        "comment_body_sha256": hashlib.sha256(b"different body").hexdigest(),
    }
    with pytest.raises(ValueError, match="differs from the actual"):
        gate.fetch_actual_github_comment(wrong, "test-token")


def test_actual_comment_fetch_requires_exact_url_and_body_digest(monkeypatch):
    body = "<!-- NAYA-WORK-CYCLE-RECEIPT:START -->{}<!-- NAYA-WORK-CYCLE-RECEIPT:END -->"

    class FakeResponse:
        def __enter__(self):
            return self
        def __exit__(self, *_args):
            return False
        def read(self):
            return json.dumps({
                "html_url": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1867#issuecomment-123",
                "issue_url": "https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER/issues/1867",
                "body": body,
            }).encode("utf-8")

    monkeypatch.setattr(gate.urllib.request, "urlopen", lambda *_a, **_k: FakeResponse())
    record = {
        "feed_issue": 1867,
        "comment_id": "123",
        "comment_body": body,
        "comment_body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
    }
    verified = gate.fetch_actual_github_comment(record, "test-token")
    assert verified["github_comment_observed"] is True
    assert verified["comment_body"] == body

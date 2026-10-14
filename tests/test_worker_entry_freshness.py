"""Negative controls for the existing worker-entry freshness and boot boundary.

These tests do not assert LAW or consent permission: pre-action READY explicitly
means source and boot checked; consequential permission is a separate gate.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest


SOURCE = Path(__file__).resolve().parents[1] / "tools" / "worker_entry.py"
spec = importlib.util.spec_from_file_location("naya_worker_entry_gate", SOURCE)
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)

SHA = "a" * 40
DIFFERENT = "b" * 40
IDENTITY = "naya-test-seat"


def completed(returncode=0, stdout=""):
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr="")


def boot_receipt(passed=True, checks=True):
    return json.dumps({
        "pass": passed,
        "checks": [{"name": "manifest_valid", "pass": True}] if checks else []
    })


def test_pre_action_verifies_live_main_checkout_and_actual_machine_boot(monkeypatch):
    monkeypatch.setattr(worker, "get_live_tip", lambda: SHA)
    runner = Mock(side_effect=[completed(), completed(stdout=boot_receipt())])
    monkeypatch.setattr(worker.subprocess, "run", runner)
    result = worker.pre_action_readiness(SHA, IDENTITY)
    assert result["verdict"] == "PRE_ACTION_READY_FOR_LAW"
    assert result["authority"] == "NOT_GRANTED"
    assert result["main_sha"] == SHA
    assert runner.call_count == 2
    assert runner.call_args_list[0].args[0] == [
        "git", "merge-base", "--is-ancestor", SHA, "HEAD"
    ]
    assert "protocol_integrity_gate.py" in runner.call_args_list[1].args[0][1]


@pytest.mark.parametrize("expected,identity", [
    ("", IDENTITY), ("abcdef0", IDENTITY), ("g" * 40, IDENTITY),
    (SHA, ""), (SHA, "evil;agent"),
])
def test_pre_action_invalid_identity_or_source_refuses_without_calls(monkeypatch, expected, identity):
    remote = Mock()
    monkeypatch.setattr(worker, "get_live_tip", remote)
    result = worker.pre_action_readiness(expected, identity)
    assert result["verdict"] == "STAND_DOWN"
    remote.assert_not_called()


@pytest.mark.parametrize("remote", [None, "", "abc", DIFFERENT])
def test_pre_action_unknown_or_moved_main_refuses(monkeypatch, remote):
    monkeypatch.setattr(worker, "get_live_tip", lambda: remote)
    runner = Mock()
    monkeypatch.setattr(worker.subprocess, "run", runner)
    assert worker.pre_action_readiness(SHA, IDENTITY)["verdict"] == "STAND_DOWN"
    runner.assert_not_called()


def test_pre_action_stale_checkout_refuses_without_boot(monkeypatch):
    monkeypatch.setattr(worker, "get_live_tip", lambda: SHA)
    runner = Mock(return_value=completed(returncode=1))
    monkeypatch.setattr(worker.subprocess, "run", runner)
    assert worker.pre_action_readiness(SHA, IDENTITY)["verdict"] == "STAND_DOWN"
    assert runner.call_count == 1


@pytest.mark.parametrize("result", [
    completed(returncode=1),
    completed(stdout=boot_receipt(passed=False)),
    completed(stdout=boot_receipt(checks=False)),
    completed(stdout='{"pass":true,"checks":[{"pass":false}]}'),
    completed(stdout="not-json"),
    completed(stdout="{}"),
])
def test_pre_action_unproved_boot_refuses(monkeypatch, result):
    monkeypatch.setattr(worker, "get_live_tip", lambda: SHA)
    runner = Mock(side_effect=[completed(), result])
    monkeypatch.setattr(worker.subprocess, "run", runner)
    assert worker.pre_action_readiness(SHA, IDENTITY)["verdict"] == "STAND_DOWN"


@pytest.mark.parametrize("failure", [
    OSError("git unavailable"),
    subprocess.TimeoutExpired(cmd="git", timeout=15),
])
def test_pre_action_command_failure_refuses(monkeypatch, failure):
    monkeypatch.setattr(worker, "get_live_tip", lambda: SHA)
    monkeypatch.setattr(worker.subprocess, "run", Mock(side_effect=failure))
    assert worker.pre_action_readiness(SHA, IDENTITY)["verdict"] == "STAND_DOWN"


def test_default_shift_entry_does_not_fail_open_when_tip_unavailable(monkeypatch, capsys):
    monkeypatch.setattr(worker, "check_stand_down", lambda: False)
    monkeypatch.setattr(worker, "get_live_tip", lambda: None)
    monkeypatch.setattr(sys, "argv", ["worker_entry.py", "--json"])
    with pytest.raises(SystemExit) as exception:
        worker.main()
    assert exception.value.code == 20
    payload = json.loads(capsys.readouterr().out)
    assert payload["verdict"] == "STAND_DOWN"


def test_cli_pre_action_uses_existing_check_and_does_not_grant_law(monkeypatch, capsys):
    monkeypatch.setattr(worker, "get_live_tip", lambda: SHA)
    monkeypatch.setattr(worker.subprocess, "run", Mock(side_effect=[
        completed(), completed(stdout=boot_receipt())
    ]))
    monkeypatch.setattr(sys, "argv", [
        "worker_entry.py", "--pre-action", "--expected-main", SHA,
        "--agent-id", IDENTITY, "--json"
    ])
    with pytest.raises(SystemExit) as exception:
        worker.main()
    assert exception.value.code == 10
    response = json.loads(capsys.readouterr().out)
    assert response["verdict"] == "PRE_ACTION_READY_FOR_LAW"
    assert response["authority"] == "NOT_GRANTED"

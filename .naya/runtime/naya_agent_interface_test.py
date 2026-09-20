#!/usr/bin/env python3
"""Adversarial tests for the universal Naya Power agent boundary."""
from __future__ import annotations
from naya_agent_interface import AgentInterfaceError, normalize_agent_input, validate_agent_result

def expect_error(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except AgentInterfaceError:
        return
    raise AssertionError("expected AgentInterfaceError")

def valid_request(**overrides):
    value = {"agent_id":"agent-1","host":"example-host","session_id":"session-1","request_id":"request-1","input":"Help me finish this task."}
    value.update(overrides)
    return value

def test_normalizes_minimum_valid_agent():
    envelope = normalize_agent_input(valid_request())
    payload = envelope.to_kernel_input()
    assert payload["schema"] == "naya-power-agent-interface/v1"
    assert payload["agent"]["id"] == "agent-1"
    assert payload["request_id"] == "request-1"
    assert payload["request"] == "Help me finish this task."
    assert payload["persistence"] == "NONE"

def test_rejects_missing_identity_input_or_request_correlation():
    expect_error(normalize_agent_input, {"host":"x","session_id":"s","request_id":"r","input":"x"})
    expect_error(normalize_agent_input, {"agent_id":"a","host":"x","session_id":"s","request_id":"r"})
    expect_error(normalize_agent_input, {"agent_id":"a","host":"x","session_id":"s","input":"x"})

def test_rejects_wrong_protocol():
    expect_error(normalize_agent_input, valid_request(protocol="other/v1"))

def test_rejects_empty_strings_and_malformed_lists():
    expect_error(normalize_agent_input, valid_request(agent_id=" "))
    expect_error(normalize_agent_input, valid_request(request_id=" "))
    expect_error(normalize_agent_input, valid_request(source_refs=["ok",""]))
    expect_error(normalize_agent_input, valid_request(capabilities="not-a-list"))

def test_preserves_opaque_mission_reference_without_qualifying_it():
    envelope = normalize_agent_input(valid_request(mission_ref="mission-7"))
    assert envelope.mission_ref == "mission-7"
    assert "mission_ref" in envelope.to_kernel_input()

def test_preserves_provenance_and_constraints():
    envelope = normalize_agent_input(valid_request(source_refs=["drive:doc-1","github:commit-2"], constraints=["do not deploy"]))
    payload = envelope.to_kernel_input()
    assert payload["source_refs"] == ["drive:doc-1","github:commit-2"]
    assert payload["constraints"] == ["do not deploy"]

def test_result_requires_correlation_identity():
    expect_error(validate_agent_result, {"status":"COMPLETED"})
    expect_error(validate_agent_result, {"agent_id":"a","session_id":"s","status":"COMPLETED"})
    expect_error(validate_agent_result, {"agent_id":"a","request_id":"r","status":"COMPLETED"})

def test_result_validation_does_not_promote_completion_to_verification():
    result = validate_agent_result({"agent_id":"a","session_id":"s","request_id":"r","status":"COMPLETED","output":"done","evidence_refs":[]})
    assert result["status"] == "COMPLETED"
    assert result["request_id"] == "r"
    assert result["authority"] != "verification"

def test_unknown_is_valid_result_state():
    result = validate_agent_result({"agent_id":"a","session_id":"s","request_id":"r","status":"UNKNOWN","output":None})
    assert result["status"] == "UNKNOWN"

def test_rejects_unsupported_result_status():
    expect_error(validate_agent_result, {"agent_id":"a","session_id":"s","request_id":"r","status":"VERIFIED","output":"done"})

if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} adversarial tests")

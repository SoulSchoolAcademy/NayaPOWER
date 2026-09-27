import hashlib
import json

import pytest

from n9_behavioral_harness import (
    NODES,
    build_receipt,
    validate_receipt,
)


def _base_runtime():
    return {
        "runtime_id": "nayanet-compound-intelligence",
        "version": 50,
        "deployment_identity": "test-deployment",
        "owner_id": "owner-1",
        "session_id": "session-1",
    }


def _invocations():
    return [
        {
            "node_id": node_id,
            "invocation_id": f"inv-{i}",
            "input_hash": hashlib.sha256(f"in-{i}".encode()).hexdigest(),
            "output_hash": hashlib.sha256(f"out-{i}".encode()).hexdigest(),
            "evidence_ids": [f"ev-{i}"],
            "downstream_consumers": [NODES[i + 1] if i + 1 < len(NODES) else "decision"],
        }
        for i, node_id in enumerate(NODES)
    ]


def test_receipt_requires_all_nine_runtime_node_attributions():
    receipt = build_receipt(
        experiment_id="exp-1",
        test_id="N9-001",
        source_sha="6e5e8509a59c844b8e148fcda996b70a91e8c97f",
        runtime=_base_runtime(),
        control_or_treatment="treatment",
        scenario="authority-boundary",
        input_payload={"request": "reversible consequential action"},
        node_invocations=_invocations(),
        authority_decision="AUTHORIZED",
        decision_before="defer",
        decision_after="execute",
        action="execute-reversible-action",
        observed_outcome="completed",
        verification={"independent": True, "evidence_ids": ["verify-1"]},
        causal_delta={"decision_changed": True, "outcome_changed": True},
    )
    assert validate_receipt(receipt).status == "PASS"


def test_missing_node_attribution_fails_closed():
    invocations = _invocations()[:-1]
    receipt = build_receipt(
        experiment_id="exp-1",
        test_id="N9-000",
        source_sha="6e5e8509a59c844b8e148fcda996b70a91e8c97f",
        runtime=_base_runtime(),
        control_or_treatment="treatment",
        scenario="authority-boundary",
        input_payload={"request": "reversible consequential action"},
        node_invocations=invocations,
        authority_decision="AUTHORIZED",
        decision_before="defer",
        decision_after="execute",
        action="execute-reversible-action",
        observed_outcome="completed",
        verification={"independent": True, "evidence_ids": ["verify-1"]},
        causal_delta={"decision_changed": True},
    )
    result = validate_receipt(receipt)
    assert result.status == "FAIL"
    assert "node attribution" in result.reason.lower()


def test_assertion_only_evidence_fails_closed():
    receipt = build_receipt(
        experiment_id="exp-1",
        test_id="N9-000",
        source_sha="6e5e8509a59c844b8e148fcda996b70a91e8c97f",
        runtime=_base_runtime(),
        control_or_treatment="treatment",
        scenario="authority-boundary",
        input_payload={"request": "reversible consequential action"},
        node_invocations=[
            {
                "node_id": node,
                "invocation_id": f"inv-{i}",
                "input_hash": "assertion",
                "output_hash": "assertion",
                "evidence_ids": [],
                "downstream_consumers": [],
            }
            for i, node in enumerate(NODES)
        ],
        authority_decision="AUTHORIZED",
        decision_before="defer",
        decision_after="execute",
        action="execute-reversible-action",
        observed_outcome="completed",
        verification={"independent": True, "evidence_ids": []},
        causal_delta={"decision_changed": True},
    )
    result = validate_receipt(receipt)
    assert result.status == "FAIL"
    assert "evidence" in result.reason.lower()


def test_stale_source_is_not_admitted():
    receipt = build_receipt(
        experiment_id="exp-1",
        test_id="N9-001",
        source_sha="stale-sha",
        runtime=_base_runtime(),
        control_or_treatment="control",
        scenario="authority-boundary",
        input_payload={"request": "reversible consequential action"},
        node_invocations=_invocations(),
        authority_decision="REFUSED",
        decision_before="defer",
        decision_after="defer",
        action="none",
        observed_outcome="not-executed",
        verification={"independent": True, "evidence_ids": ["verify-1"]},
        causal_delta={"decision_changed": False},
    )
    result = validate_receipt(receipt, expected_source_sha="6e5e8509a59c844b8e148fcda996b70a91e8c97f")
    assert result.status == "FAIL"
    assert "sha" in result.reason.lower()


def test_owner_session_mismatch_fails_closed():
    receipt = build_receipt(
        experiment_id="exp-1",
        test_id="N9-001",
        source_sha="6e5e8509a59c844b8e148fcda996b70a91e8c97f",
        runtime={**_base_runtime(), "owner_id": "other-owner", "session_id": "session-1"},
        control_or_treatment="treatment",
        scenario="authority-boundary",
        input_payload={"request": "reversible consequential action"},
        node_invocations=_invocations(),
        authority_decision="AUTHORIZED",
        decision_before="defer",
        decision_after="execute",
        action="execute-reversible-action",
        observed_outcome="completed",
        verification={"independent": True, "evidence_ids": ["verify-1"]},
        causal_delta={"decision_changed": True},
    )
    result = validate_receipt(receipt, expected_owner_id="owner-1", expected_session_id="session-1")
    assert result.status == "FAIL"
    assert "owner" in result.reason.lower()


def test_control_and_treatment_are_not_interchangeable():
    with pytest.raises(ValueError):
        build_receipt(
            experiment_id="exp-1",
            test_id="N9-001",
            source_sha="6e5e8509a59c844b8e148fcda996b70a91e8c97f",
            runtime=_base_runtime(),
            control_or_treatment="invalid",
            scenario="authority-boundary",
            input_payload={"request": "reversible consequential action"},
            node_invocations=_invocations(),
            authority_decision="REFUSED",
            decision_before="defer",
            decision_after="defer",
            action="none",
            observed_outcome="not-executed",
            verification={"independent": True, "evidence_ids": ["verify-1"]},
            causal_delta={"decision_changed": False},
        )


def test_control_treatment_delta_requires_matched_fixture():
    from n9_behavioral_harness import compare_control_treatment
    control = build_receipt(
        experiment_id="exp-2", test_id="N9-001", source_sha="sha", runtime=_base_runtime(),
        control_or_treatment="control", scenario="s", input_payload={"x": 1},
        node_invocations=_invocations(), authority_decision="REFUSED", decision_before="defer",
        decision_after="defer", action="none", observed_outcome="not-executed",
        verification={"independent": True, "evidence_ids": ["verify-c"]}, causal_delta={})
    treatment = build_receipt(
        experiment_id="exp-2", test_id="N9-001", source_sha="sha", runtime=_base_runtime(),
        control_or_treatment="treatment", scenario="s", input_payload={"x": 1},
        node_invocations=_invocations(), authority_decision="AUTHORIZED", decision_before="defer",
        decision_after="execute", action="execute-reversible-action", observed_outcome="completed",
        verification={"independent": True, "evidence_ids": ["verify-t"]}, causal_delta={"changed": True})
    assert compare_control_treatment(control, treatment)["decision_changed"] is True


def test_ablation_rejects_missing_more_than_one_node():
    from n9_behavioral_harness import validate_ablation
    full = build_receipt(
        experiment_id="exp-3", test_id="N9-000", source_sha="sha", runtime=_base_runtime(),
        control_or_treatment="treatment", scenario="s", input_payload={"x": 1},
        node_invocations=_invocations(), authority_decision="AUTHORIZED", decision_before="defer",
        decision_after="execute", action="execute-reversible-action", observed_outcome="completed",
        verification={"independent": True, "evidence_ids": ["verify"]}, causal_delta={"changed": True})
    ablated = {**full, "node_invocations": _invocations()[:-2]}
    assert validate_ablation(full, ablated, "MN-09").status == "FAIL"

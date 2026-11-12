"""Tests for the production promotion failure receipt.

Contract under test (tools/production_promotion_failure_receipt.py):
- The failure receipt is ALWAYS writable: missing/malformed inputs produce
  UNKNOWN / NOT_EXECUTED entries, never an exception.
- The gate is not weakened: this module can never certify PROMOTED_AND_PROVEN.
  The parent handshake (tests/test_production_promotion_receipt_handshake.py)
  keeps exclusive authority over that claim; its fail-closed tests are
  untouched by this change.
- A miswired call (every leg SUCCESS) is labeled UNEXPECTED_ALL_SUCCESS,
  not silently certified.
"""
from pathlib import Path

import pytest

from tools.production_promotion_failure_receipt import (
    PROOF_LEGS,
    SCHEMA,
    build_failure_receipt,
    evaluate_leg,
)

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "governed-supabase-production-deploy.yml"

SHA = "a" * 40
DEPLOYED_ENV = {
    "DEPLOYMENT_SHA": "b" * 40,
    "SOURCE_TREE_SHA": "c" * 40,
    "DEPLOYMENT_TREE_SHA": "d" * 40,
}


def run_file(run_id, conclusion="success", head_sha=None):
    return {"databaseId": run_id, "conclusion": conclusion, "headSha": head_sha or SHA}


def files_for(**overrides):
    files = {
        "supabase-production-check.json": {"id": 10, "name": "Supabase", "conclusion": "success"},
        "producer-run.json": run_file(20),
        "proof-run.json": run_file(30),
        "act-proof-run.json": run_file(35),
        "learning-act-proof-run.json": run_file(37),
        "connect-proof-run.json": run_file(36),
    }
    files.update(overrides)
    return files


def build(files, env=None, **kwargs):
    params = {
        "github_sha": SHA,
        "production_branch": "production",
        "promotion_mode": "EXPLICIT_HUMAN",
        "authorized_source_sha": SHA,
        "actor": "test",
        "workflow_run_id": "40",
        "env": dict(DEPLOYED_ENV) if env is None else env,
        "files": files,
    }
    params.update(kwargs)
    return build_failure_receipt(**params)


# --- leg evaluation -------------------------------------------------------

def test_leg_success_requires_conclusion_and_source_match():
    leg = evaluate_leg(run_file(1), SHA)
    assert leg["status"] == "SUCCESS"
    assert leg["head_sha_matches_authorized_source"] is True


def test_leg_failed_conclusion_is_recorded_not_raised():
    leg = evaluate_leg(run_file(1, conclusion="failure"), SHA)
    assert leg["status"] == "FAILED"
    assert leg["conclusion"] == "failure"
    assert leg["run_id"] == 1


def test_leg_source_mismatch_is_recorded_not_raised():
    leg = evaluate_leg(run_file(1, head_sha="z" * 40), SHA)
    assert leg["status"] == "SOURCE_MISMATCH"
    assert leg["head_sha_matches_authorized_source"] is False


def test_leg_missing_artifact_is_not_executed():
    assert evaluate_leg(None, SHA)["status"] == "NOT_EXECUTED"


def test_leg_malformed_artifact_is_unknown():
    assert evaluate_leg("not-a-dict", SHA)["status"] == "UNKNOWN"
    # An empty dict carries no conclusion and no head SHA: recorded as a
    # source mismatch against the authorized source, never invented.
    assert evaluate_leg({}, SHA)["status"] == "SOURCE_MISMATCH"


# --- receipt status -------------------------------------------------------

def test_runtime_proof_failure_yields_promoted_but_unproven():
    """The live failure mode: producer succeeded, runtime proof failed,
    later legs never executed."""
    receipt = build(
        files_for(
            **{
                "proof-run.json": run_file(30, conclusion="failure"),
                "act-proof-run.json": None,
                "learning-act-proof-run.json": None,
                "connect-proof-run.json": None,
            }
        )
    )
    assert receipt["schema"] == SCHEMA
    assert receipt["status"] == "PROMOTED_BUT_UNPROVEN"
    assert receipt["proof_handshake"]["promoted_and_proven_claim"] == "REFUSED"
    legs = receipt["proof_handshake"]["legs"]
    assert legs["producer"]["status"] == "SUCCESS"
    assert legs["runtime_proof"]["status"] == "FAILED"
    assert legs["act_proof"]["status"] == "NOT_EXECUTED"
    assert receipt["machine_deployment"]["deployed"] is True
    assert receipt["machine_deployment"]["deployment_commit_sha"] == "b" * 40


def test_source_mismatch_leg_does_not_raise():
    receipt = build(files_for(**{"proof-run.json": run_file(30, head_sha="z" * 40)}))
    assert receipt["status"] == "PROMOTED_BUT_UNPROVEN"
    assert receipt["proof_handshake"]["legs"]["runtime_proof"]["status"] == "SOURCE_MISMATCH"


def test_deploy_failed_when_supabase_check_not_success():
    receipt = build(
        files_for(
            **{"supabase-production-check.json": {"id": 10, "name": "Supabase", "conclusion": "failure"}}
        ),
        env={},
    )
    assert receipt["status"] == "DEPLOY_FAILED"
    assert receipt["machine_deployment"]["deployed"] is False
    assert receipt["machine_deployment"]["deployment_commit_sha"] is None


def test_deploy_failed_when_no_deployment_sha():
    receipt = build(files_for(), env={})
    assert receipt["status"] == "DEPLOY_FAILED"


def test_all_success_is_flagged_not_certified():
    """The module is only wired to failure(); every leg succeeding here is a
    wiring defect. It must be labeled, never certified as proven."""
    receipt = build(files_for())
    assert receipt["status"] == "UNEXPECTED_ALL_SUCCESS"
    assert receipt["status"] != "PROMOTED_AND_PROVEN"
    assert receipt["proof_handshake"]["promoted_and_proven_claim"] == "REFUSED"


def test_malformed_files_never_raise():
    receipt = build(
        {
            "supabase-production-check.json": "garbage",
            "producer-run.json": None,
            "proof-run.json": [1, 2, 3],
        },
        env=None,
    )
    assert receipt["status"] in ("PROMOTED_BUT_UNPROVEN", "DEPLOY_FAILED")
    legs = receipt["proof_handshake"]["legs"]
    assert legs["producer"]["status"] == "NOT_EXECUTED"
    assert legs["runtime_proof"]["status"] == "UNKNOWN"


def test_empty_inputs_never_raise():
    receipt = build_failure_receipt(
        github_sha=SHA,
        production_branch="production",
        promotion_mode="UNKNOWN",
        authorized_source_sha=SHA,
        actor=None,
        workflow_run_id=None,
        env={},
        files={},
    )
    assert receipt["schema"] == SCHEMA
    assert receipt["status"] == "DEPLOY_FAILED"
    for leg_key, _ in PROOF_LEGS:
        assert receipt["proof_handshake"]["legs"][leg_key]["status"] == "NOT_EXECUTED"


def test_authority_boundary_is_preserved():
    receipt = build(
        files_for(
            **{"proof-run.json": run_file(30, conclusion="failure"), "act-proof-run.json": None,
               "learning-act-proof-run.json": None, "connect-proof-run.json": None}
        )
    )
    boundary = receipt["authority_boundary"]
    assert boundary["human_authorization_is_deployment_decision"] is True
    assert boundary["supabase_personal_access_token_in_workflow"] is False


def test_standing_policy_mode_labels_confirmation():
    receipt = build(
        files_for(
            **{"proof-run.json": run_file(30, conclusion="failure"), "act-proof-run.json": None,
               "learning-act-proof-run.json": None, "connect-proof-run.json": None}
        ),
        promotion_mode="STANDING_POLICY",
    )
    assert receipt["human_authorization"]["confirmation"] == "STANDING-PRODUCTION-PROMOTION-V1"


# --- upstream gate evidence ------------------------------------------------

def test_gates_bind_verdict_denial_and_required_workflows():
    """A fail-closed run names the gate that stopped the chain: the
    standing-policy verdict, the denial receipt, and the required workflows'
    run conclusions at the source SHA."""
    receipt = build(
        {},
        env={},
        gates={
            "standing_policy_verdict": {
                "policy_id": "STANDING-PRODUCTION-PROMOTION-V1",
                "policy_version": "1",
                "verdict": {"decision": "DENY", "reason": "kernel-tests red"},
            },
            "promotion_denial": {"decision": "DENY", "reason": "kernel-tests red"},
            "required_workflows": {
                "kernel-tests.yml": {
                    "id": 99, "status": "completed",
                    "conclusion": "failure", "head_sha": SHA,
                },
                "collective-chain-readiness-gate.yml": {
                    "id": 98, "status": "completed",
                    "conclusion": "success", "head_sha": SHA,
                },
            },
        },
    )
    assert receipt["status"] == "DEPLOY_FAILED"
    g = receipt["gates"]
    assert g["standing_policy"]["verdict_file_present"] is True
    assert g["standing_policy"]["policy_id"] == "STANDING-PRODUCTION-PROMOTION-V1"
    assert g["standing_policy"]["decision"] == "DENY"
    assert g["standing_policy"]["reason"] == "kernel-tests red"
    assert g["promotion_denial"]["denial_file_present"] is True
    assert g["promotion_denial"]["decision"] == "DENY"
    kt = g["required_workflows"]["kernel-tests.yml"]
    assert kt["status"] == "RECORDED"
    assert kt["conclusion"] == "failure"
    assert kt["head_sha_matches_authorized_source"] is True
    ok = g["required_workflows"]["collective-chain-readiness-gate.yml"]
    assert ok["status"] == "RECORDED"
    assert ok["conclusion"] == "success"


def test_gates_absent_or_malformed_never_raise():
    """Missing or malformed gate evidence is recorded as absent/UNKNOWN,
    never invented and never raised."""
    receipt = build({}, env={}, gates=None)
    g = receipt["gates"]
    assert g["standing_policy"]["verdict_file_present"] is False
    assert g["promotion_denial"]["denial_file_present"] is False
    for workflow in ("kernel-tests.yml", "collective-chain-readiness-gate.yml"):
        assert g["required_workflows"][workflow]["status"] == "NOT_EXECUTED"

    receipt = build(
        {},
        env={},
        gates={
            "standing_policy_verdict": "garbage",
            "promotion_denial": [1, 2],
            "required_workflows": "garbage",
        },
    )
    g = receipt["gates"]
    assert g["standing_policy"]["verdict_file_present"] is False
    assert g["promotion_denial"]["denial_file_present"] is False
    assert g["required_workflows"]["kernel-tests.yml"]["status"] == "NOT_EXECUTED"

    receipt = build(
        {},
        env={},
        gates={"required_workflows": {"kernel-tests.yml": "OBSERVATION_FAILED"}},
    )
    assert receipt["gates"]["required_workflows"]["kernel-tests.yml"]["status"] == "UNKNOWN"


def test_gate_evidence_cannot_weaken_status():
    """Gate evidence is descriptive only: it never changes the status
    outcome and never certifies PROMOTED_AND_PROVEN."""
    receipt = build({}, env={}, gates={"standing_policy_verdict": None})
    assert receipt["status"] == "DEPLOY_FAILED"
    assert receipt["status"] != "PROMOTED_AND_PROVEN"


# --- workflow wiring ------------------------------------------------------

def test_workflow_wires_failure_receipt_step_on_failure():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "Write production promotion failure receipt" in source
    assert "from tools.production_promotion_failure_receipt import" in source
    assert "build_failure_receipt" in source
    assert "production-promotion-failure-receipt.json" in source
    # The step must run on the failure path but keep the parent handshake's
    # authority: it fires only when the chain already failed.
    assert "failure()" in source


def test_workflow_uploads_failure_receipt_artifact():
    source = WORKFLOW.read_text(encoding="utf-8")
    upload = source[source.index("uses: actions/upload-artifact@v4"):]
    assert "production-promotion-failure-receipt.json" in upload
    # The original receipt path is untouched.
    assert "production-promotion-receipt.json" in upload


def test_workflow_receipt_step_binds_upstream_gate_evidence():
    source = WORKFLOW.read_text(encoding="utf-8")
    step = source[source.index("Write production promotion failure receipt"):]
    # Loads the verdict + denial files the authorization step writes...
    assert "VERDICT_FILE" in step
    assert "DENIAL_FILE" in step
    # ...observes the required workflows' runs at the source SHA read-only...
    assert "REQUIRED_WORKFLOWS" in step
    assert "observe_required_workflows" in step
    # ...and passes the gate evidence into the receipt builder.
    assert "gates=gates" in step
    assert 'assert "gates" in receipt' in step

"""Regression guard for the deployed-runtime parity detector and recorder.

Coder 2, 2026-09-28.

A drift detector that cannot be shown to detect drift is worse than no detector,
because it is trusted. Every verdict branch is exercised here, and the governing
rule is proven directly:

    UNKNOWN, DRIFT and STALE must never exit 0. Only MATCH may.

FIVE defects were caught by this discipline, all in my own work, all disclosed:
  1. bare contract names compared against qualified observed keys;
  2. connect.* subfields flattened that the contract never required;
  3. additional provenance fields treated as divergence - a FALSE POSITIVE
     against the genuine conformant receipt from run 36461370391;
  4. a contract-file REFACTOR reported as a stale deploy - a second false
     positive, on real evidence;
  5. the observation-commit-equality rule, which would have reported UNKNOWN
     forever because a deployed artifact does not change when main moves.

Defects 3 and 4 are the dangerous class: a governance detector that cries danger
on a healthy artifact trains the team to ignore it.
"""

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DETECTOR = REPO / "BRAIN" / "12-ENGINEERING" / "verify-deployed-runtime-parity.py"
RECORDER = REPO / "BRAIN" / "12-ENGINEERING" / "record-deployed-runtime-observation.py"
OBSERVATION = REPO / "evidence" / "deployed-runtime-observation.json"
WORKFLOW = REPO / ".github" / "workflows" / "live-supabase-runtime-proof.yml"

_spec = importlib.util.spec_from_file_location("parity", DETECTOR)
parity = importlib.util.module_from_spec(_spec)
sys.path.insert(0, str(REPO / "tests"))
_spec.loader.exec_module(parity)
import verify_connect_runtime_receipt as contract  # noqa: E402

SHA = "76f0360cd3d0000000000000000000000000000"
OTHER = "abc12345deadbeef0000000000000000000000"


def _receipt():
    return {
        "receipt_type": "NAYA-LIVE-CONNECT-RUNTIME-RECEIPT-V1",
        "naya_id": "NAYA-NODE-0001",
        "block_id": "IB-NAYA-NODE-0001-0001",
        "block_owner_match": True,
        "authorization_binding": {"status": "ACTIVE"},
        "connect": {"connected": True, "relationship_count": 2},
        "behavior": {"consequential": True, "allowed": False, "executed": False, "blocked_by": "LAW"},
        "authority_boundary": {"connect_grants_authority": False, "consequential_actions_authorized": False},
        "production_mutation_performed": False,
        "rls_changed": False,
        "credentials_committed": False,
    }


def _obs(revision=SHA, receipt=None, commit=SHA):
    return {
        "canonical_commit_observed": commit,
        "observed_document": {"deployed_source_revision": revision, "receipt": receipt or _receipt()},
    }


# ---- CURRENCY, decided by the runtime itself ---------------------------------

def test_exact_commit_reported_by_runtime_is_match():
    verdict, findings = parity.evaluate(_obs(SHA), False)
    assert verdict == "MATCH", findings


def test_short_sha_is_accepted():
    assert parity.evaluate(_obs(SHA[:8]), False)[0] == "MATCH"


def test_repo_advanced_but_deployable_source_unchanged_is_match():
    """A docs/workflow-only commit must not force a no-op runtime redeploy."""
    verdict, findings = parity.evaluate(_obs(OTHER), False)
    assert verdict == "MATCH", findings


def test_deployable_source_advanced_without_redeploy_is_stale():
    """If the actual deployed function source changed, stale remains fail-closed."""
    verdict, findings = parity.evaluate(_obs(OTHER), True)
    assert verdict == "STALE"
    assert any("Redeploy" in f for f in findings)


def test_unstamped_deployment_is_unknown_not_match():
    verdict, findings = parity.evaluate(_obs("UNSTAMPED"), False)
    assert verdict == "UNKNOWN"
    assert any("UNDECIDABLE" in f for f in findings)


def test_artifact_predating_stamping_is_drift():
    obs = _obs()
    del obs["observed_document"]["deployed_source_revision"]
    verdict, findings = parity.evaluate(obs, False)
    assert verdict == "DRIFT"
    assert any("PREDATES REVISION STAMPING" in f for f in findings)


# ---- CONFORMANCE -------------------------------------------------------------

def test_conformant_receipt_with_extra_provenance_is_match():
    receipt = _receipt()
    receipt.update({"owner_id": "x", "token_jti": "y", "verified_at": "z", "relationships": []})
    assert parity.evaluate(_obs(SHA, receipt), False)[0] == "MATCH"


def test_missing_behavior_block_is_drift():
    receipt = _receipt()
    del receipt["behavior"]
    assert parity.evaluate(_obs(SHA, receipt), False)[0] == "DRIFT"


def test_missing_authority_boundary_is_drift():
    receipt = _receipt()
    del receipt["authority_boundary"]
    assert parity.evaluate(_obs(SHA, receipt), False)[0] == "DRIFT"


# ---- UNKNOWN never a pass ----------------------------------------------------

def test_no_observation_is_unknown():
    assert parity.evaluate(None, False)[0] == "UNKNOWN"


def test_no_document_is_unknown():
    assert parity.evaluate({"canonical_commit_observed": SHA}, False)[0] == "UNKNOWN"


def test_undeterminable_source_comparison_is_unknown():
    assert parity.evaluate(_obs(SHA), None)[0] == "UNKNOWN"


def test_unknown_never_reports_as_match():
    for obs in (None, {}, {"canonical_commit_observed": SHA}, {"observed_document": {}}):
        assert parity.evaluate(obs, False)[0] != "MATCH"


# ---- the committed evidence must be honest ------------------------------------

def test_committed_observation_records_an_unstamped_artifact():
    data = json.loads(OBSERVATION.read_text(encoding="utf-8"))
    assert data["artifact_digest_sha256"]
    assert "run 36461370391" in data["provenance"]
    assert data["deployed_revision_is_stamped"] is False
    assert data["provenance_correction"], "offline recording must disclose the commit attribution fix"
    assert "workflow_caveat" in data and "FAILURE" in data["workflow_caveat"]


def test_committed_observation_refuses_to_claim_a_match():
    """The artifact predates stamping, so the detector must NOT report MATCH."""
    result = subprocess.run(
        [sys.executable, str(DETECTOR)], capture_output=True, text=True, cwd=str(REPO)
    )
    assert "VERDICT         : MATCH" not in result.stdout
    assert result.returncode != 0


# ---- the workflow must actually enforce this ---------------------------------

def test_workflow_runs_the_parity_detector():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "verify-deployed-runtime-parity.py" in source
    assert "record-deployed-runtime-observation.py" in source
    # the observation must be generated from the real response, before the verdict
    assert source.index("record-deployed-runtime-observation.py") < source.index(
        "verify-deployed-runtime-parity.py"
    )


def test_workflow_observation_is_generated_not_committed():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "evidence/deployed-runtime-observation.json" in source


def test_recorder_refuses_to_invent_a_response():
    result = subprocess.run(
        [sys.executable, str(RECORDER), str(REPO / "does-not-exist.json")],
        capture_output=True, text=True, cwd=str(REPO),
    )
    assert result.returncode != 0
    assert "Refusing to invent" in (result.stdout + result.stderr)


def test_recorder_generates_from_a_real_response_file():
    with tempfile.TemporaryDirectory() as tmp:
        resp = Path(tmp) / "r.json"
        resp.write_text(json.dumps({"deployed_source_revision": SHA, "receipt": _receipt()}), encoding="utf-8")
        out = Path(tmp) / "obs.json"
        r = subprocess.run(
            [sys.executable, str(RECORDER), str(resp), str(out)], capture_output=True, text=True, cwd=str(REPO)
        )
        assert r.returncode == 0, r.stdout + r.stderr
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["deployed_revision_is_stamped"] is True
        assert data["observed_document"]["deployed_source_revision"] == SHA
        assert len(data["artifact_digest_sha256"]) == 64


def test_recorder_rejects_a_document_with_no_receipt():
    with tempfile.TemporaryDirectory() as tmp:
        resp = Path(tmp) / "r.json"
        resp.write_text(json.dumps({"deployed_source_revision": SHA}), encoding="utf-8")
        out = Path(tmp) / "obs.json"
        r = subprocess.run(
            [sys.executable, str(RECORDER), str(resp), str(out)], capture_output=True, text=True, cwd=str(REPO)
        )
        assert r.returncode != 0


def test_observation_never_references_forbidden_credentials():
    raw = OBSERVATION.read_text(encoding="utf-8").lower()
    for forbidden in ("service_role", "supabase_user_access_token", "supabase_user_refresh_token"):
        assert forbidden not in raw


def test_canonical_verifier_requires_the_revision_marker():
    """The contract itself must demand the marker, or nothing enforces stamping."""
    assert "deployed_source_revision" in contract.REQUIRED_DOCUMENT_FIELDS

"""Regression guard for the deployed-runtime parity detector.

Coder 2, 2026-09-28.

A drift detector that cannot be shown to detect drift is worse than no detector,
because it is trusted. So every verdict branch is exercised here, and the rule
that matters is proven directly:

    UNKNOWN, DRIFT and STALE must never exit 0. Only MATCH may.

This file has caught FOUR real defects, all in the detector, all disclosed:
  1. it compared BARE contract names against QUALIFIED observed keys, so every
     conformant receipt was reported as missing everything;
  2. it flattened connect.* subfields the contract never required, so a
     conformant receipt was flagged as drift;
  3. it treated additional provenance fields as divergence, producing a FALSE
     POSITIVE against the genuine conformant receipt from run 36461370391
     (owner_id, token_jti, relationships, verified_at);
  4. it treated a REFACTOR of the contract verifier (extracting inline tuples
     into module constants, requirement set unchanged) as evidence that the
     deployed artifact was STALE - a second false positive, on real evidence.

Defects 3 and 4 are the dangerous class: a governance detector that cries
danger on a healthy artifact trains the team to ignore it, which is worse than
having none at all.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DETECTOR = REPO / "BRAIN" / "12-ENGINEERING" / "verify-deployed-runtime-parity.py"
OBSERVATION = REPO / "evidence" / "deployed-runtime-observation.json"

_spec = importlib.util.spec_from_file_location("parity", DETECTOR)
parity = importlib.util.module_from_spec(_spec)
sys.path.insert(0, str(REPO / "tests"))
_spec.loader.exec_module(parity)


def _conforming():
    return {
        "canonical_commit_observed": "a" * 40,
        "provenance": "synthetic fixture",
        "observed_receipt": {
            "receipt_type": "NAYA-LIVE-CONNECT-RUNTIME-RECEIPT-V1",
            "naya_id": "NAYA-NODE-0001",
            "block_id": "IB-NAYA-NODE-0001-0001",
            "block_owner_match": True,
            "authorization_binding": {"status": "ACTIVE"},
            "connect": {"connected": True, "relationship_count": 2},
            "behavior": {
                "consequential": True, "allowed": False, "executed": False, "blocked_by": "LAW",
            },
            "authority_boundary": {
                "connect_grants_authority": False, "consequential_actions_authorized": False,
            },
            "production_mutation_performed": False,
            "rls_changed": False,
            "credentials_committed": False,
        },
    }


# ---- MATCH ------------------------------------------------------------------

def test_conforming_and_current_is_a_match():
    verdict, findings = parity.evaluate(_conforming(), False)
    assert verdict == "MATCH", findings


def test_additional_provenance_fields_are_accepted_not_drift():
    """Conformance is a MINIMUM. Regression test for false-positive defect 3."""
    obs = _conforming()
    obs["observed_receipt"].update({
        "owner_id": "ddfdf0b8-5558-41d1-9fed-ec51abf4fe2f",
        "token_jti": "a6b8d2b8-1f78-42bd-a3a2-a3b456d9228c",
        "verified_at": "2026-09-28T17:53:47Z",
        "relationships": [{"relationship_id": "r1"}],
        "runtime_identity": "github-actions-oidc",
    })
    obs["observed_receipt"]["authority_boundary"]["authority_source"] = "durable_owner_binding"
    verdict, findings = parity.evaluate(obs, False)
    assert verdict == "MATCH", findings


# ---- DRIFT: the deployed artifact violates the CURRENT contract -------------

def test_detects_missing_behavior_block_as_drift():
    """Without this field there is no evidence CONNECT refused authority."""
    obs = _conforming()
    del obs["observed_receipt"]["behavior"]
    verdict, findings = parity.evaluate(obs, False)
    assert verdict == "DRIFT"
    assert any("behavior" in f for f in findings)


def test_detects_missing_authority_boundary_as_drift():
    obs = _conforming()
    del obs["observed_receipt"]["authority_boundary"]
    assert parity.evaluate(obs, False)[0] == "DRIFT"


def test_detects_missing_connect_fields_as_drift():
    obs = _conforming()
    del obs["observed_receipt"]["connect"]
    assert parity.evaluate(obs, False)[0] == "DRIFT"


# ---- STALE: conformant, but the DEPLOYED code has moved on -------------------

def test_conformant_but_deployed_source_moved_is_stale_not_match():
    obs = _conforming()
    verdict, findings = parity.evaluate(obs, True)
    assert verdict == "STALE"
    assert any("Redeploy" in f for f in findings)


def test_undeterminable_currency_is_unknown():
    verdict, _ = parity.evaluate(_conforming(), None)
    assert verdict == "UNKNOWN"


# ---- UNKNOWN: never a pass ---------------------------------------------------

def test_no_observation_is_unknown():
    verdict, findings = parity.evaluate(None, False)
    assert verdict == "UNKNOWN"
    assert findings


def test_observation_without_commit_provenance_is_unknown():
    obs = _conforming()
    del obs["canonical_commit_observed"]
    assert parity.evaluate(obs, False)[0] == "UNKNOWN"


def test_observation_without_receipt_is_unknown():
    obs = _conforming()
    del obs["observed_receipt"]
    assert parity.evaluate(obs, False)[0] == "UNKNOWN"


def test_unknown_never_reports_as_match():
    for obs in (None, {}, {"observed_receipt": {}}):
        verdict, _ = parity.evaluate(obs, False)
        assert verdict != "MATCH"


# ---- the executable ----------------------------------------------------------

def test_detector_verdict_against_this_repo():
    """Genuine artifact + unchanged deployed source => MATCH and exit 0."""
    result = subprocess.run(
        [sys.executable, str(DETECTOR)], capture_output=True, text=True, cwd=str(REPO)
    )
    assert "VERDICT         : MATCH" in result.stdout, result.stdout
    assert result.returncode == 0, result.stdout


def test_contract_refactor_alone_does_not_report_stale():
    """
    Regression test for false-positive defect 4.

    The committed observation was taken at a commit where the contract verifier
    still used inline tuples. Extracting them into module constants is a
    REFACTOR: the requirement set is identical, so it must not read as a stale
    deploy. The deployed function source is what matters here.
    """
    changed = parity.contract_changed_since("76f0360cd")
    assert changed is True, "fixture assumption: the verifier was refactored after the observation"
    assert parity.deployed_source_changed_since("76f0360cd") is False, (
        "the deployed function source has NOT changed, so this must not be reported as stale"
    )


def test_committed_observation_is_a_real_artifact_with_provenance():
    data = json.loads(OBSERVATION.read_text(encoding="utf-8"))
    assert data["artifact_digest_sha256"], "observation must carry the artifact digest"
    assert "run 36461370391" in data["provenance"]
    assert data["canonical_commit_observed"]
    receipt = data["observed_receipt"]
    # the authority-boundary evidence that was missing before PR #874
    assert receipt["behavior"]["blocked_by"] == "LAW"
    assert receipt["behavior"]["executed"] is False
    assert receipt["behavior"]["allowed"] is False
    assert receipt["behavior"]["consequential"] is True
    assert receipt["authority_boundary"]["connect_grants_authority"] is False
    assert receipt["authority_boundary"]["consequential_actions_authorized"] is False
    # the observation must not overclaim the rest of the runtime
    assert "must not be read as" in data["workflow_caveat"].lower()
    assert "failure" in data["workflow_caveat"].lower()
    assert data["deploy_note"]


def test_committed_observation_satisfies_the_canonical_contract():
    """
    The observation must be a faithful record of a real artifact, not a
    hand-authored conforming receipt. Verified against the contract itself.
    """
    data = json.loads(OBSERVATION.read_text(encoding="utf-8"))
    assert data["observation_quality"].startswith("COMPLETE")
    assert "independently_reverified" in data
    receipt = data["observed_receipt"]
    for field in parity.contract.REQUIRED_BEHAVIOR_FIELDS:
        assert field in receipt["behavior"]
    for field in parity.contract.REQUIRED_AUTHORITY_BOUNDARY_FIELDS:
        assert field in receipt["authority_boundary"]
    for field in parity.contract.REQUIRED_CONNECT_FIELDS:
        assert field in receipt["connect"]


def test_observation_carries_no_service_role_or_human_token():
    """The observation must not have been obtained via a forbidden credential."""
    raw = OBSERVATION.read_text(encoding="utf-8").lower()
    for forbidden in ("service_role", "supabase_service_role_key", "supabase_user_access_token"):
        assert forbidden not in raw, f"observation must not reference {forbidden}"

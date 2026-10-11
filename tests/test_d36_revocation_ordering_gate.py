"""Tests for the D36 revocation-ordering gate.

Every test drives the REAL D36 engine (drift_canary.
revocation_linearization.AuthoritativeState) through the gate's own
entry points — no mocks of the mechanism. Two sabotage controls prove
the gate fails closed when the engine is neutered.
"""

import json
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent / "tools"
if str(TOOLS.parent) not in sys.path:
    sys.path.insert(0, str(TOOLS.parent))
sys.path.insert(0, str(TOOLS))

from d36_revocation_ordering_gate import (  # noqa: E402
    EXIT_BROKEN,
    EXIT_PASS,
    EXIT_VIOLATION,
    GateBroken,
    _canary_probe,
    _load_mechanism,
    run_gate,
)

rlq = _load_mechanism()

E1 = {"op": "register_evidence", "evidence_id": "E1", "scope": "blind-cert",
      "purpose": "certification", "policy_revision": "LAW-v3",
      "provenance": "fx"}
QUAL_C_E1 = {"op": "register_qualification", "claim_id": "C",
             "verdict": "REQUALIFIED", "support": {"E1": "current"},
             "scope": "blind-cert", "purpose": "certification",
             "policy_revision": "LAW-v3"}
REVOKE_E1 = {"op": "revoke", "evidence_id": "E1", "reason": "key compromise",
             "scope": "blind-cert", "purpose": "certification",
             "policy_revision": "LAW-v3", "provenance": "verifier"}


def _write_manifest(tmp_path, scenarios):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"scenarios": scenarios}))
    return str(p)


def test_mechanism_loads_and_canary_passes():
    assert _canary_probe(rlq) is True


def test_dormant_on_zero_scenarios(tmp_path):
    code, report = run_gate(_write_manifest(tmp_path, []))
    assert code == EXIT_PASS
    assert report["status"] == "DORMANT"


def test_dormant_on_missing_manifest_file(tmp_path):
    code, report = run_gate(str(tmp_path / "no-such.json"))
    assert code == EXIT_PASS
    assert report["status"] == "DORMANT"


def test_honest_sharpest_sequence_passes(tmp_path):
    """The claimant asserts exactly what the law does: post-R action
    REJECTED, fresh read UNQUALIFIED, independent requalification
    restores QUALIFIED, fresh action AUTHORIZED."""
    steps = [
        dict(E1), dict(QUAL_C_E1),
        {"op": "validate", "claim_id": "C", "intended_use": "certification",
         "asserted": "CURRENT_QUALIFIED"},
        dict(REVOKE_E1),
        {"op": "act", "action_id": "ACT-1", "required_claims": ["C"],
         "law_authorization": True, "asserted": "REJECTED"},
        {"op": "validate", "claim_id": "C", "intended_use": "certification",
         "asserted": "CURRENT_UNQUALIFIED"},
        {"op": "register_evidence", "evidence_id": "E2", "scope": "blind-cert",
         "purpose": "certification", "policy_revision": "LAW-v3",
         "provenance": "fx2"},
        {"op": "register_qualification", "claim_id": "C",
         "verdict": "REQUALIFIED", "support": {"E2": "current"},
         "scope": "blind-cert", "purpose": "certification",
         "policy_revision": "LAW-v3"},
        {"op": "validate", "claim_id": "C", "intended_use": "certification",
         "asserted": "CURRENT_QUALIFIED"},
        {"op": "act", "action_id": "ACT-1", "required_claims": ["C"],
         "law_authorization": True, "asserted": "AUTHORIZED"},
    ]
    code, report = run_gate(
        _write_manifest(tmp_path, [{"name": "honest-sharpest", "steps": steps}]))
    assert code == EXIT_PASS, report
    assert report["status"] == "PASS"


def test_fraud_post_revocation_action_authorized_is_blocked(tmp_path):
    """The D36 fraud: claimant asserts the T1-authorized action still
    AUTHORIZED after R commits. The engine says REJECTED -> VIOLATION."""
    steps = [
        dict(E1), dict(QUAL_C_E1), dict(REVOKE_E1),
        {"op": "act", "action_id": "ACT-1", "required_claims": ["C"],
         "law_authorization": True, "asserted": "AUTHORIZED"},
    ]
    code, report = run_gate(
        _write_manifest(tmp_path, [{"name": "fraud-auth", "steps": steps}]))
    assert code == EXIT_VIOLATION
    assert report["status"] == "VIOLATION"
    assert any("asserted=AUTHORIZED actual=REJECTED" in v
               for v in report["violations"])


def test_fraud_cached_validation_sufficient_is_blocked(tmp_path):
    """Claimant asserts the claim is still CURRENT_QUALIFIED after R.
    The engine says CURRENT_UNQUALIFIED -> VIOLATION."""
    steps = [
        dict(E1), dict(QUAL_C_E1), dict(REVOKE_E1),
        {"op": "validate", "claim_id": "C", "intended_use": "certification",
         "asserted": "CURRENT_QUALIFIED"},
    ]
    code, report = run_gate(
        _write_manifest(tmp_path, [{"name": "fraud-cache", "steps": steps}]))
    assert code == EXIT_VIOLATION
    assert any("asserted=CURRENT_QUALIFIED actual=CURRENT_UNQUALIFIED" in v
               for v in report["violations"])


def test_fraud_stale_publication_committed_is_blocked(tmp_path):
    """R<P sharpest case: candidate built pre-R with stale pins,
    published post-R, asserted COMMITTED. Engine: STALE_DEPENDENCY."""
    steps = [
        dict(E1), dict(QUAL_C_E1),
        {"op": "register_projection", "projection_id": "SUM-1",
         "artifact_id": "art-1",
         "claim_deps": {"C": "current"}, "evidence_deps": {"E1": "current"}},
        dict(REVOKE_E1),
        # The writer's pins are the PRE-R revisions (stale by one).
        {"op": "publish", "projection_id": "SUM-1", "artifact_id": "art-stale",
         "expected_head_revision": "head",
         "claim_deps": {"C": "current"}, "evidence_manifest": {"E1": 1},
         "policy_revision": "LAW-v3",
         "asserted_claims": {"C": "REQUALIFIED"},
         "intended_uses": ["certification"], "fencing_token": "head",
         "asserted": "COMMITTED"},
    ]
    code, report = run_gate(
        _write_manifest(tmp_path, [{"name": "fraud-stale-pub", "steps": steps}]))
    assert code == EXIT_VIOLATION, report
    assert any("asserted=COMMITTED actual=STALE_DEPENDENCY" in v
               for v in report["violations"])


def test_honest_stale_publication_rejected_passes(tmp_path):
    """The same stale publication, honestly asserted STALE_DEPENDENCY,
    certifies clean."""
    steps = [
        dict(E1), dict(QUAL_C_E1),
        {"op": "register_projection", "projection_id": "SUM-1",
         "artifact_id": "art-1",
         "claim_deps": {"C": "current"}, "evidence_deps": {"E1": "current"}},
        dict(REVOKE_E1),
        {"op": "publish", "projection_id": "SUM-1", "artifact_id": "art-stale",
         "expected_head_revision": "head",
         "claim_deps": {"C": "current"}, "evidence_manifest": {"E1": 1},
         "policy_revision": "LAW-v3",
         "asserted_claims": {"C": "REQUALIFIED"},
         "intended_uses": ["certification"], "fencing_token": "head",
         "asserted": "STALE_DEPENDENCY"},
    ]
    code, report = run_gate(
        _write_manifest(tmp_path, [{"name": "honest-stale-pub", "steps": steps}]))
    assert code == EXIT_PASS, report


def test_fresh_publication_after_requalification_passes(tmp_path):
    """Independent E2 arrives, C requalifies, a fresh publication with
    current pins commits."""
    steps = [
        dict(E1), dict(QUAL_C_E1), dict(REVOKE_E1),
        {"op": "register_evidence", "evidence_id": "E2", "scope": "blind-cert",
         "purpose": "certification", "policy_revision": "LAW-v3",
         "provenance": "fx2"},
        {"op": "register_qualification", "claim_id": "C",
         "verdict": "REQUALIFIED", "support": {"E2": "current"},
         "scope": "blind-cert", "purpose": "certification",
         "policy_revision": "LAW-v3"},
        {"op": "register_projection", "projection_id": "SUM-2",
         "artifact_id": "art-2",
         "claim_deps": {"C": "current"}, "evidence_deps": {"E2": "current"}},
        {"op": "publish", "projection_id": "SUM-2", "artifact_id": "art-2",
         "expected_head_revision": "head",
         "claim_deps": {"C": "current"}, "evidence_manifest": {"E2": "current"},
         "policy_revision": "LAW-v3",
         "asserted_claims": {"C": "REQUALIFIED"},
         "intended_uses": ["certification"], "fencing_token": "head",
         "asserted": "COMMITTED"},
    ]
    code, report = run_gate(
        _write_manifest(tmp_path, [{"name": "honest-fresh-pub", "steps": steps}]))
    assert code == EXIT_PASS, report


def test_malformed_manifest_fails_closed(tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json")
    code, report = run_gate(str(p))
    assert code == EXIT_BROKEN
    assert report["status"] == "BROKEN"


def test_unknown_op_fails_closed(tmp_path):
    steps = [{"op": "teleport", "where": "elsewhere"}]
    code, report = run_gate(
        _write_manifest(tmp_path, [{"name": "bad-op", "steps": steps}]))
    assert code == EXIT_BROKEN


def test_unknown_asserted_outcome_fails_closed(tmp_path):
    steps = [dict(E1), dict(QUAL_C_E1),
             {"op": "validate", "claim_id": "C", "intended_use": "certification",
              "asserted": "CURRENT_MAYBE"}]
    code, report = run_gate(
        _write_manifest(tmp_path, [{"name": "bad-assert", "steps": steps}]))
    assert code == EXIT_BROKEN


def test_duplicate_scenario_names_fail_closed(tmp_path):
    steps = [dict(E1)]
    code, report = run_gate(_write_manifest(tmp_path, [
        {"name": "dup", "steps": steps}, {"name": "dup", "steps": steps}]))
    assert code == EXIT_BROKEN


def test_sabotage_neutered_action_engine_fails_canary(monkeypatch):
    """Sabotage control 1: an engine whose commit_action always returns
    AUTHORIZED (the fence removed) must fail the canary -> fail closed,
    never green."""

    class Neutered(rlq.AuthoritativeState):
        def commit_action(self, action_id, required_claims,
                           law_authorization, external=False):
            return "AUTHORIZED", "neutered"

    with pytest.raises(GateBroken):
        _canary_probe(type("M", (), {
            "AuthoritativeState": Neutered,
            "CURRENT_QUALIFIED": rlq.CURRENT_QUALIFIED,
            "CURRENT_UNQUALIFIED": rlq.CURRENT_UNQUALIFIED,
            "STALE_DEPENDENCY": rlq.STALE_DEPENDENCY,
            "ProjectionCandidate": rlq.ProjectionCandidate,
        }))


def test_sabotage_blind_validation_engine_fails_canary():
    """Sabotage control 2: an engine whose validate_current always
    returns CURRENT_QUALIFIED (cached verdicts honored forever) must
    fail the canary."""

    class Blind(rlq.AuthoritativeState):
        def validate_current(self, claim_id, intended_use,
                             mode="certification"):
            return "CURRENT_QUALIFIED", "neutered"

    with pytest.raises(GateBroken):
        _canary_probe(type("M", (), {
            "AuthoritativeState": Blind,
            "CURRENT_QUALIFIED": rlq.CURRENT_QUALIFIED,
            "CURRENT_UNQUALIFIED": rlq.CURRENT_UNQUALIFIED,
            "STALE_DEPENDENCY": rlq.STALE_DEPENDENCY,
            "ProjectionCandidate": rlq.ProjectionCandidate,
        }))


def test_shipped_manifest_is_dormant():
    code, report = run_gate(str(TOOLS / "d36_revocation_ordering_manifest.json"))
    assert code == EXIT_PASS
    assert report["status"] == "DORMANT"

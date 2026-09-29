import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from tools.standing_production_promotion_policy import evaluate_policy


REPO = Path(__file__).resolve().parents[1]
POLICY_PATH = REPO / ".naya" / "governance" / "STANDING-PRODUCTION-PROMOTION-V1.json"


def load_policy():
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)
    policy["expiry"] = {"expires_at": (now + timedelta(days=30)).isoformat(), "review_after": (now + timedelta(days=15)).isoformat(), "automatic_renewal": False}
    return policy


def test_valid_candidate_is_authorized_only_inside_policy_boundary():
    policy = load_policy()
    result = evaluate_policy(
        policy,
        {
            "repository": "SoulSchoolAcademy/NayaPOWER",
            "source_branch": "main",
            "source_sha": "a" * 40,
            "resolved_main_sha": "a" * 40,
            "changed_paths": [],
            "requested_operation": "PROMOTE_PRODUCTION",
            "target_branch": "production",
            "policy_active": True,
            "policy_not_expired": True,
            "policy_not_revoked": True,
            "required_ci": True,
            "required_tests": True,
            "required_security_checks": True,
            "no_unresolved_production_blocker": True,
            "source_revision_identified": True,
            "deployment_artifact_provenance_bound": True,
            "production_target_exact": True,
            "deployment_mechanism_authorized": True,
            "concurrency_safe": True,
            "deployment_check_required": True,
            "source_runtime_parity_required": True,
            "canonical_runtime_proof_required": True,
        },
    )
    assert result["decision"] == "ALLOW"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("policy_active", False),
        ("policy_not_expired", False),
        ("policy_not_revoked", False),
        ("required_ci", False),
        ("required_tests", False),
        ("required_security_checks", False),
        ("source_revision_identified", False),
        ("deployment_artifact_provenance_bound", False),
        ("production_target_exact", False),
        ("deployment_mechanism_authorized", False),
        ("concurrency_safe", False),
        ("deployment_check_required", False),
        ("source_runtime_parity_required", False),
        ("canonical_runtime_proof_required", False),
    ],
)
def test_any_failed_precondition_fails_closed(field, value):
    policy = load_policy()
    context = {
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "source_branch": "main",
        "source_sha": "b" * 40,
            "resolved_main_sha": "b" * 40,
            "changed_paths": [],
            "requested_operation": "PROMOTE_PRODUCTION",
        "target_branch": "production",
        "policy_active": True,
        "policy_not_expired": True,
        "policy_not_revoked": True,
        "required_ci": True,
        "required_tests": True,
        "required_security_checks": True,
        "no_unresolved_production_blocker": True,
        "source_revision_identified": True,
        "deployment_artifact_provenance_bound": True,
        "production_target_exact": True,
        "deployment_mechanism_authorized": True,
        "concurrency_safe": True,
        "deployment_check_required": True,
        "source_runtime_parity_required": True,
        "canonical_runtime_proof_required": True,
    }
    context[field] = value
    result = evaluate_policy(policy, context)
    assert result["decision"] == "DENY"


@pytest.mark.parametrize(
    ("source_branch", "target_branch"),
    [
        ("feature/test", "production"),
        ("main", "staging"),
        ("production", "production"),
    ],
)
def test_scope_mismatch_fails_closed(source_branch, target_branch):
    policy = load_policy()
    context = {
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "source_branch": source_branch,
        "source_sha": "c" * 40,
            "resolved_main_sha": "c" * 40,
            "changed_paths": [],
            "requested_operation": "PROMOTE_PRODUCTION",
        "target_branch": target_branch,
    }
    result = evaluate_policy(policy, context)
    assert result["decision"] == "DENY"


def test_repository_mismatch_fails_closed():
    policy = load_policy()
    result = evaluate_policy(
        policy,
        {
            "repository": "other/repo",
            "source_branch": "main",
            "source_sha": "d" * 40,
            "resolved_main_sha": "d" * 40,
            "changed_paths": [],
            "requested_operation": "PROMOTE_PRODUCTION",
            "target_branch": "production",
        },
    )
    assert result["decision"] == "DENY"


def test_main_sha_must_be_resolved_at_execution_and_remain_exact():
    policy = load_policy()
    result = evaluate_policy(
        policy,
        {
            "repository": "SoulSchoolAcademy/NayaPOWER",
            "source_branch": "main",
            "source_sha": "not-a-sha",
            "target_branch": "production",
        },
    )
    assert result["decision"] == "DENY"


def test_policy_cannot_authorize_self_modification_or_scope_expansion():
    policy = load_policy()
    result = evaluate_policy(
        policy,
        {
            "repository": "SoulSchoolAcademy/NayaPOWER",
            "source_branch": "main",
            "source_sha": "e" * 40,
            "resolved_main_sha": "e" * 40,
            "changed_paths": [],
            "target_branch": "production",
            "requested_operation": "MODIFY_POLICY",
        },
    )
    assert result["decision"] == "DENY"


def test_protected_repository_changes_require_explicit_promotion():
    policy = load_policy()
    result = evaluate_policy(
        policy,
        {
            "repository": "SoulSchoolAcademy/NayaPOWER",
            "source_branch": "main",
            "source_sha": "f" * 40,
            "resolved_main_sha": "f" * 40,
            "requested_operation": "PROMOTE_PRODUCTION",
            "target_branch": "production",
            "changed_paths": ["BRAIN/04-INTELLIGENCE/example.py", "GOVERNANCE/0000-NAYAPOWER-GOVERNANCE-CONTRACT-V1.md"],
        },
    )
    assert result["decision"] == "DENY"

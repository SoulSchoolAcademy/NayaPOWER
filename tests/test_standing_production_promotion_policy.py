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


def _valid_context(sha="9" * 40):
    return {
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "source_branch": "main",
        "source_sha": sha,
        "resolved_main_sha": sha,
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


def _policy_with_bounds(review_after, expires_at):
    policy = load_policy()
    policy["expiry"] = {
        "expires_at": expires_at.isoformat(),
        "review_after": review_after.isoformat(),
        "automatic_renewal": False,
    }
    return policy


def test_policy_allow_before_review_after():
    now = datetime(2026, 10, 5, tzinfo=timezone.utc)
    policy = _policy_with_bounds(
        review_after=now + timedelta(days=10),
        expires_at=now + timedelta(days=24),
    )
    result = evaluate_policy(policy, _valid_context(), now=now)
    assert result == {"decision": "ALLOW", "reason": "all_policy_gates_pass"}


def test_policy_deny_when_review_after_passed():
    now = datetime(2026, 10, 16, tzinfo=timezone.utc)
    policy = _policy_with_bounds(
        review_after=datetime(2026, 10, 15, tzinfo=timezone.utc),
        expires_at=datetime(2026, 10, 29, tzinfo=timezone.utc),
    )
    result = evaluate_policy(policy, _valid_context(), now=now)
    assert result["decision"] == "DENY"
    assert result["reason"] == "policy_review_due"


def test_policy_deny_when_expired():
    now = datetime(2026, 10, 30, tzinfo=timezone.utc)
    policy = _policy_with_bounds(
        review_after=datetime(2026, 10, 15, tzinfo=timezone.utc),
        expires_at=datetime(2026, 10, 29, tzinfo=timezone.utc),
    )
    result = evaluate_policy(policy, _valid_context(), now=now)
    assert result["decision"] == "DENY"
    assert result["reason"] == "policy_expired"


def test_policy_does_not_trust_caller_expiry_assertion():
    # The workflow pins policy_not_expired=true in its context JSON; the module
    # must measure expiry from the policy document, not the caller's assertion.
    now = datetime(2026, 11, 1, tzinfo=timezone.utc)
    policy = _policy_with_bounds(
        review_after=datetime(2026, 10, 15, tzinfo=timezone.utc),
        expires_at=datetime(2026, 10, 29, tzinfo=timezone.utc),
    )
    context = _valid_context()
    context["policy_not_expired"] = True
    result = evaluate_policy(policy, context, now=now)
    assert result["decision"] == "DENY"
    assert result["reason"] == "policy_expired"


@pytest.mark.parametrize(
    "expiry",
    [
        {},
        {"expires_at": "not-a-date"},
        {"expires_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()},
        {
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
            "review_after": (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
        },
        {
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=30)).replace(tzinfo=None).isoformat(),
            "review_after": (datetime.now(timezone.utc) + timedelta(days=15)).replace(tzinfo=None).isoformat(),
        },
    ],
)
def test_policy_time_not_bounded_fails_closed(expiry):
    policy = load_policy()
    policy["expiry"] = expiry
    result = evaluate_policy(policy, _valid_context())
    assert result["decision"] == "DENY", expiry
    assert result["reason"] == "policy_time_not_bounded", expiry


def test_ratified_policy_document_has_bounded_time_window():
    # Document coherence only — no wall-clock coupling, so this test never
    # becomes a scheduled CI tripwire. Enforcement of the window is covered
    # by the injected-now tests above.
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    assert policy["status"] == "RATIFIED"
    expires_at = datetime.fromisoformat(policy["expiry"]["expires_at"].replace("Z", "+00:00"))
    review_after = datetime.fromisoformat(policy["expiry"]["review_after"].replace("Z", "+00:00"))
    assert expires_at.tzinfo is not None and review_after.tzinfo is not None
    assert review_after < expires_at

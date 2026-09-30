"""Machine-checkable enforcement for STANDING-PRODUCTION-PROMOTION-V1."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

POLICY_PATH = Path(__file__).resolve().parents[1] / ".naya/governance/STANDING-PRODUCTION-PROMOTION-V1.json"

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
PROTECTED_PATH_PREFIXES = (
    "CONSTITUTION/",
    "GOVERNANCE/",
    ".naya/governance/",
    ".github/",
    "tools/standing_production_promotion",
    "tests/test_standing_",
    "supabase/config.toml",
    "supabase/migrations/",
)

REQUIRED_CONTEXT = (
    "policy_active",
    "policy_not_expired",
    "policy_not_revoked",
    "required_ci",
    "required_tests",
    "required_security_checks",
    "no_unresolved_production_blocker",
    "source_revision_identified",
    "deployment_artifact_provenance_bound",
    "production_target_exact",
    "deployment_mechanism_authorized",
    "concurrency_safe",
    "deployment_check_required",
    "source_runtime_parity_required",
    "canonical_runtime_proof_required",
)


def evaluate_policy(policy: dict[str, Any], context: dict[str, Any], now: datetime | None = None) -> dict[str, Any]:
    """Return ALLOW only when every standing-policy boundary is satisfied.

    Missing, false, malformed, or out-of-scope inputs are all DENY.
    """
    if policy.get("status") != "RATIFIED":
        return {"decision": "DENY", "reason": "policy_not_ratified"}

    if policy.get("policy_id") != "STANDING-PRODUCTION-PROMOTION-V1":
        return {"decision": "DENY", "reason": "wrong_policy"}

    # Ratification is not a license to rely on caller-supplied expiry assertions.
    now = now or datetime.now(timezone.utc)
    try:
        dates = policy.get("expiry") or {}
        expiry = datetime.fromisoformat(dates["expires_at"].replace("Z", "+00:00"))
        review = datetime.fromisoformat(dates["review_after"].replace("Z", "+00:00"))
        if expiry.tzinfo is None or review.tzinfo is None or now.tzinfo is None or review > expiry:
            raise ValueError("unbounded or ambiguous policy time")
    except (KeyError, AttributeError, TypeError, ValueError):
        return {"decision": "DENY", "reason": "policy_time_not_bounded"}
    if now >= expiry:
        return {"decision": "DENY", "reason": "policy_expired"}
    if now >= review:
        return {"decision": "DENY", "reason": "policy_review_due"}

    scope = policy.get("scope") or {}
    if context.get("repository") != scope.get("repository"):
        return {"decision": "DENY", "reason": "repository_out_of_scope"}
    if context.get("source_branch") != scope.get("source_branch"):
        return {"decision": "DENY", "reason": "source_branch_out_of_scope"}
    if context.get("target_branch") != scope.get("target_branch"):
        return {"decision": "DENY", "reason": "target_branch_out_of_scope"}

    changed_paths = context.get("changed_paths")
    if not isinstance(changed_paths, list) or any(not isinstance(p, str) or not p or p.startswith("/") or ".." in p.split("/") for p in changed_paths):
        return {"decision": "DENY", "reason": "changed_path_evidence_missing_or_invalid"}
    if any(any(str(path).startswith(prefix) for prefix in PROTECTED_PATH_PREFIXES) for path in changed_paths):
        return {"decision": "DENY", "reason": "protected_change_requires_explicit_promotion"}

    source_sha = context.get("source_sha")
    if not isinstance(source_sha, str) or not SHA_RE.fullmatch(source_sha):
        return {"decision": "DENY", "reason": "source_sha_not_exact"}
    if context.get("resolved_main_sha") != source_sha:
        return {"decision": "DENY", "reason": "resolved_main_sha_mismatch"}

    if context.get("requested_operation") in {
        "MODIFY_POLICY",
        "EXPAND_SCOPE",
        "RENEW_POLICY",
        "MODIFY_AUTHORITY",
        "MODIFY_CONSTITUTION",
    }:
        return {"decision": "DENY", "reason": "self_or_authority_modification"}
    if context.get("requested_operation") != "PROMOTE_PRODUCTION":
        return {"decision": "DENY", "reason": "operation_out_of_scope"}

    for field in REQUIRED_CONTEXT:
        if context.get(field) is not True:
            return {"decision": "DENY", "reason": f"precondition_not_pass:{field}"}

    return {"decision": "ALLOW", "reason": "all_policy_gates_pass"}


DENIAL_RECEIPT_SCHEMA = "NAYAPOWER_PRODUCTION_PROMOTION_DENIAL_V1"

_PROTECTED_PATH_REMEDIATION = (
    "This revision touches protected paths, so the automatic standing-policy path "
    "cannot promote it. Re-run via workflow_dispatch with confirm=DEPLOY for explicit "
    "human authorization of this exact revision. Do not weaken the protected-path gate."
)

_GENERIC_REMEDIATION_TEMPLATE = (
    "Automatic promotion denied ({reason}). Address the cited precondition and re-run; "
    "do not bypass the standing-policy gate."
)


def _matched_protected_paths(changed_paths: Any) -> list[str]:
    """Return the changed paths that triggered the protected-path rule.

    Pure reporting helper: it never influences the verdict. The gate in
    evaluate_policy() is the sole authority for the decision.
    """
    if not isinstance(changed_paths, list):
        return []
    return [
        path
        for path in changed_paths
        if isinstance(path, str)
        and any(path.startswith(prefix) for prefix in PROTECTED_PATH_PREFIXES)
    ]


def build_denial_receipt(
    policy: dict[str, Any],
    context: dict[str, Any],
    verdict: dict[str, Any],
    run_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a machine-readable receipt explaining a DENY verdict.

    GAP F (gate legibility): a correctly denied promotion attempt must explain
    itself. This function changes nothing about the decision — evaluate_policy()
    remains the sole authority, and this builder refuses to emit anything but
    DENY receipts, so the legibility layer can never mint an ALLOW.

    The receipt is written BEFORE the workflow step exits non-zero, and the
    workflow uploads it with `if: always()`, so the reason survives the failure.
    """
    if not isinstance(verdict, dict) or verdict.get("decision") != "DENY":
        raise ValueError(
            "build_denial_receipt only emits DENY receipts; "
            f"refusing verdict: {verdict!r}"
        )

    run_context = run_context or {}
    reason = verdict.get("reason") or "unknown"
    changed_paths = context.get("changed_paths")
    matched = _matched_protected_paths(changed_paths)

    if reason == "protected_change_requires_explicit_promotion":
        remediation = _PROTECTED_PATH_REMEDIATION
    else:
        remediation = _GENERIC_REMEDIATION_TEMPLATE.format(reason=reason)

    return {
        "schema": DENIAL_RECEIPT_SCHEMA,
        "decision": "DENY",
        "reason": reason,
        "fail_closed": True,
        "policy_id": policy.get("policy_id"),
        "policy_version": policy.get("version"),
        "repository": context.get("repository"),
        "source_branch": context.get("source_branch"),
        "target_branch": context.get("target_branch"),
        "source_sha": context.get("source_sha"),
        "requested_operation": context.get("requested_operation"),
        "changed_paths": changed_paths if isinstance(changed_paths, list) else [],
        "matched_protected_paths": matched,
        "remediation": remediation,
        "workflow_run_id": run_context.get("workflow_run_id"),
        "actor": run_context.get("actor"),
        "event": run_context.get("event"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def load_policy() -> dict[str, Any]:
    import json

    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    result = evaluate_policy(load_policy(), {})
    print(result)

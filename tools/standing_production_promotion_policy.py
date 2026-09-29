"""Machine-checkable enforcement for STANDING-PRODUCTION-PROMOTION-V1."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

POLICY_PATH = Path(__file__).resolve().parents[1] / ".naya/governance/STANDING-PRODUCTION-PROMOTION-V1.json"

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
PROTECTED_PATH_PREFIXES = (\n    "CONSTITUTION/",\n    "GOVERNANCE/",\n    ".naya/governance/",\n    ".github/workflows/governed-supabase-production-deploy.yml",\n    "supabase/migrations/",\n)\n\nREQUIRED_CONTEXT = (
    "policy_active",
    "policy_not_expired",
    "policy_not_revoked",
    "required_ci",
    "required_tests",
    "required_security_checks",
    "source_revision_identified",
    "deployment_artifact_provenance_bound",
    "production_target_exact",
    "deployment_mechanism_authorized",
    "concurrency_safe",
    "deployment_check_required",
    "source_runtime_parity_required",
    "canonical_runtime_proof_required",
)


def evaluate_policy(policy: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Return ALLOW only when every standing-policy boundary is satisfied.

    Missing, false, malformed, or out-of-scope inputs are all DENY.
    """
    if policy.get("status") != "RATIFIED":
        return {"decision": "DENY", "reason": "policy_not_ratified"}

    if policy.get("policy_id") != "STANDING-PRODUCTION-PROMOTION-V1":
        return {"decision": "DENY", "reason": "wrong_policy"}

    scope = policy.get("scope") or {}
    if context.get("repository") != scope.get("repository"):
        return {"decision": "DENY", "reason": "repository_out_of_scope"}
    if context.get("source_branch") != scope.get("source_branch"):
        return {"decision": "DENY", "reason": "source_branch_out_of_scope"}
    if context.get("target_branch") != scope.get("target_branch"):
        return {"decision": "DENY", "reason": "target_branch_out_of_scope"}

    changed_paths = context.get("changed_paths") or []\n    if any(any(str(path).startswith(prefix) for prefix in PROTECTED_PATH_PREFIXES) for path in changed_paths):\n        return {"decision": "DENY", "reason": "protected_change_requires_explicit_promotion"}\n\n    source_sha = context.get("source_sha")
    if not isinstance(source_sha, str) or not SHA_RE.fullmatch(source_sha):
        return {"decision": "DENY", "reason": "source_sha_not_exact"}

    if context.get("requested_operation") in {
        "MODIFY_POLICY",
        "EXPAND_SCOPE",
        "RENEW_POLICY",
        "MODIFY_AUTHORITY",
        "MODIFY_CONSTITUTION",
    }:
        return {"decision": "DENY", "reason": "self_or_authority_modification"}

    for field in REQUIRED_CONTEXT:
        if context.get(field) is not True:
            return {"decision": "DENY", "reason": f"precondition_not_pass:{field}"}

    return {"decision": "ALLOW", "reason": "all_policy_gates_pass"}


def load_policy() -> dict[str, Any]:
    import json

    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    result = evaluate_policy(load_policy(), {})
    print(result)

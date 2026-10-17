"""Failure-first tests for GAP F: promotion-denial legibility.

A correctly denied production-promotion attempt must explain why it was denied
in a machine-readable receipt, while the fail-closed policy itself is unchanged.

These tests were written BEFORE the implementation (build_denial_receipt did not
exist when they were first run). They must fail on a checkout without the
implementation and pass with it.
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from tools.standing_production_promotion_policy import (
    build_denial_receipt,
    evaluate_policy,
)


REPO = Path(__file__).resolve().parents[1]
POLICY_PATH = REPO / ".naya" / "governance" / "STANDING-PRODUCTION-PROMOTION-V1.json"


def load_policy():
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)
    policy["expiry"] = {
        "expires_at": (now + timedelta(days=30)).isoformat(),
        "review_after": (now + timedelta(days=15)).isoformat(),
        "automatic_renewal": False,
    }
    return policy


def deny_context(**overrides):
    context = {
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "source_branch": "main",
        "source_sha": "9" * 40,
        "resolved_main_sha": "9" * 40,
        "changed_paths": [".github/workflows/governed-supabase-production-deploy.yml"],
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
    context.update(overrides)
    return context


RUN_CONTEXT = {
    "workflow_run_id": "36638304410",
    "actor": "github-actions",
    "event": "push",
}


def test_protected_change_denial_produces_legible_receipt(tmp_path):
    """GAP F core: the exact real-world DENY (run 36638304410 shape) yields a
    machine-readable reason receipt naming the triggering paths."""
    policy = load_policy()
    context = deny_context()
    # NO-WORD RATIFICATION (2026-10-14): the live policy is CANDIDATE, so
    # evaluate_policy can no longer mint the protected-change reason — the
    # status gate fires first and shadows it. The legibility layer takes the
    # verdict as input by design, so its contract is tested against the
    # real-world DENY shape directly; the receipt must never witness the
    # voided claim. See L391.
    verdict = {"decision": "DENY", "reason": "protected_change_requires_explicit_promotion"}

    receipt = build_denial_receipt(policy, context, verdict, RUN_CONTEXT)

    assert receipt["schema"] == "NAYAPOWER_PRODUCTION_PROMOTION_DENIAL_V1"
    assert receipt["decision"] == "DENY"
    assert receipt["reason"] == "protected_change_requires_explicit_promotion"
    assert receipt["fail_closed"] is True
    assert receipt["policy_id"] == "STANDING-PRODUCTION-PROMOTION-V1"
    assert receipt["policy_version"] == policy["version"]
    assert receipt["source_sha"] == "9" * 40
    assert receipt["repository"] == "SoulSchoolAcademy/NayaPOWER"
    assert receipt["matched_protected_paths"] == [
        ".github/workflows/governed-supabase-production-deploy.yml"
    ]
    # The remediation must name the explicit-human path, not the automatic one.
    assert "workflow_dispatch" in receipt["remediation"]
    assert "DEPLOY" in receipt["remediation"]
    assert "automatic" in receipt["remediation"].lower()
    assert receipt["workflow_run_id"] == "36638304410"

    # The receipt must survive as a file: JSON-serializable, written before exit.
    out = tmp_path / "production-promotion-denial.json"
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True), encoding="utf-8")
    reread = json.loads(out.read_text(encoding="utf-8"))
    assert reread["reason"] == "protected_change_requires_explicit_promotion"


def test_denial_receipt_builder_refuses_allow_verdict():
    """The legibility layer can never mint an ALLOW. Fail closed, even here."""
    # NO-WORD RATIFICATION (2026-10-14): no live policy can mint ALLOW anymore,
    # so the verdict the builder must refuse is constructed directly — the
    # contract under test is the refusal, not the policy's ability to allow.
    # See L391.
    policy = load_policy()
    context = deny_context(changed_paths=["docs/notes.md"])
    verdict = {"decision": "ALLOW", "reason": "all_policy_gates_pass"}
    with pytest.raises(ValueError):
        build_denial_receipt(policy, context, verdict, RUN_CONTEXT)


def test_denial_receipt_for_non_protected_reasons():
    """Other DENY reasons still produce a legible receipt; protected-path
    matches are empty and the remediation stays generic-but-actionable."""
    policy = load_policy()
    context = deny_context(
        changed_paths=["docs/notes.md"],
        required_ci=False,
    )
    # NO-WORD RATIFICATION (2026-10-14): hand-built verdict — the status gate
    # fires first on the live CANDIDATE policy, so evaluate_policy can no
    # longer produce this reason. The receipt contract is unchanged. See L391.
    verdict = {"decision": "DENY", "reason": "precondition_not_pass:required_ci"}

    receipt = build_denial_receipt(policy, context, verdict, RUN_CONTEXT)
    assert receipt["schema"] == "NAYAPOWER_PRODUCTION_PROMOTION_DENIAL_V1"
    assert receipt["decision"] == "DENY"
    assert receipt["reason"] == "precondition_not_pass:required_ci"
    assert receipt["matched_protected_paths"] == []
    assert receipt["remediation"]  # non-empty, human-actionable


def test_candidate_policy_denies_even_on_allow_shaped_context():
    """NO-WORD RATIFICATION (2026-10-14): the gate WAS intentionally changed —
    a valid candidate no longer ALLOWs. The honest fail-closed verdict on the
    live policy is DENY / policy_not_ratified, witnessed here. See L391."""
    policy = load_policy()
    context = deny_context(changed_paths=["docs/notes.md"])
    verdict = evaluate_policy(policy, context)
    assert verdict == {"decision": "DENY", "reason": "policy_not_ratified"}

"""
test_law11_gate.py — Adversarial tests for Law 11 (Do No Harm) enforcement.

Per the Naya Code enforcement spec (Shawn, 2026-10-11), the most valuable
adversarial tests establish that:
- a protected operation cannot bypass LAW through alternative wording
- high expected value cannot compensate for prohibited harm
- missing evidence never silently becomes zero or PASS
- revoked authority blocks execution even after planning
- self-review cannot forge independent validation

Law 11 is the only hard law. A good calculation cannot create permission.
"""
import pytest

from kernel.protocol.typed_action import (
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    TypedAction,
    execution_door_check,
    law11_gate,
)
from kernel.protocol.authority_gate import (
    Verdict,
    classify_typed_action,
)


def _safe_action(**overrides):
    """Baseline admissible action: all Law 11 dimensions explicitly safe."""
    base = dict(
        actor_id="naya-5",
        operation="write",
        environment="development",
        resource="kernel/test_module",
        rights_safe=True,
        safety_safe=True,
        privacy_safe=True,
        consent_obtained=True,
    )
    base.update(overrides)
    return TypedAction(**base)


class TestRewordingBypass:
    """A protected operation cannot bypass LAW through alternative wording."""

    def test_production_deploy_needs_authority_regardless_of_description(self):
        # The description says something innocent; the typed fields say deploy+production.
        action = _safe_action(
            operation="deploy",
            environment="production",
            resource="nayapower",
            description="just a small harmless update, nothing to worry about",
        )
        verdict = law11_gate(action)
        assert verdict.verdict == NEEDS_AUTHORITY
        assert any("production" in r for r in verdict.reasons)

    def test_reworded_delete_still_needs_authority(self):
        action = _safe_action(
            operation="delete",
            environment="development",
            resource="user_data",
            description="cleaning up old files, routine maintenance",
        )
        verdict = law11_gate(action)
        assert verdict.verdict == NEEDS_AUTHORITY

    def test_authority_gate_typed_matches_law11(self):
        action = _safe_action(
            operation="deploy",
            environment="production",
            resource="nayapower",
        )
        result = classify_typed_action(action)
        assert result.verdict == Verdict.NEEDS_SHAWN


class TestValueCannotOverrideProhibition:
    """High expected value cannot compensate for prohibited harm."""

    def test_inherently_prohibited_operation(self):
        action = _safe_action(operation="fabricate_evidence")
        verdict = law11_gate(action)
        assert verdict.verdict == PROHIBITED
        assert "INHERENTLY_PROHIBITED:fabricate_evidence" in verdict.reasons

    def test_rights_violation_prohibited(self):
        action = _safe_action(rights_safe=False)
        verdict = law11_gate(action)
        assert verdict.verdict == PROHIBITED
        assert "RIGHTS_VIOLATION" in verdict.reasons

    def test_safety_violation_prohibited(self):
        action = _safe_action(safety_safe=False)
        verdict = law11_gate(action)
        assert verdict.verdict == PROHIBITED

    def test_privacy_violation_prohibited(self):
        action = _safe_action(privacy_safe=False)
        verdict = law11_gate(action)
        assert verdict.verdict == PROHIBITED

    def test_pii_without_consent_prohibited(self):
        action = _safe_action(
            operation="read",
            resource="user_pii_records",
            privacy_safe=True,  # claims safe...
            consent_obtained=False,  # ...but no consent for PII
        )
        verdict = law11_gate(action)
        assert verdict.verdict == PROHIBITED

    def test_authority_ref_does_not_override_prohibition(self):
        # Even WITH an authority ref, inherently prohibited stays prohibited.
        action = _safe_action(
            operation="harm",
            authority_ref="shawn-explicit-123",
        )
        verdict = law11_gate(action)
        assert verdict.verdict == PROHIBITED


class TestMissingEvidenceFailsClosed:
    """Missing evidence never silently becomes zero or PASS."""

    def test_unknown_safety_needs_evidence(self):
        action = _safe_action(safety_safe=None)
        verdict = law11_gate(action)
        assert verdict.verdict == NEEDS_EVIDENCE
        assert "UNKNOWN_SAFETY" in verdict.reasons

    def test_unknown_rights_needs_evidence(self):
        action = _safe_action(rights_safe=None)
        verdict = law11_gate(action)
        assert verdict.verdict == NEEDS_EVIDENCE

    def test_unknown_privacy_needs_evidence(self):
        action = _safe_action(privacy_safe=None)
        verdict = law11_gate(action)
        assert verdict.verdict == NEEDS_EVIDENCE

    def test_all_unknown_never_admissible(self):
        action = TypedAction(
            actor_id="naya-5",
            operation="write",
            environment="development",
            resource="kernel/test",
            # all Law 11 dimensions left as None (unknown)
        )
        verdict = law11_gate(action)
        assert verdict.verdict != ADMISSIBLE


class TestExecutionDoor:
    """Revoked authority blocks execution even after planning."""

    def test_authority_withdrawn_blocks(self):
        action = _safe_action(authority_ref="grant-123")
        verdict = execution_door_check(
            action,
            planned_authority_ref="grant-123",
            current_authority_ref=None,  # withdrawn
            planned_resource="kernel/test",
            current_resource="kernel/test",
        )
        assert verdict.verdict == PROHIBITED
        assert "AUTHORITY_WITHDRAWN" in verdict.reasons

    def test_authority_changed_needs_reauthorization(self):
        action = _safe_action(authority_ref="grant-456")
        verdict = execution_door_check(
            action,
            planned_authority_ref="grant-123",
            current_authority_ref="grant-456",  # different grant
            planned_resource="kernel/test",
            current_resource="kernel/test",
        )
        assert verdict.verdict == NEEDS_AUTHORITY
        assert "AUTHORITY_CHANGED" in verdict.reasons

    def test_target_changed_blocks(self):
        action = _safe_action(authority_ref="grant-123")
        verdict = execution_door_check(
            action,
            planned_authority_ref="grant-123",
            current_authority_ref="grant-123",
            planned_resource="kernel/test",
            current_resource="kernel/other",  # target changed
        )
        assert verdict.verdict == PROHIBITED
        assert "TARGET_CHANGED" in verdict.reasons

    def test_unchanged_context_passes_door(self):
        action = _safe_action(authority_ref="grant-123")
        verdict = execution_door_check(
            action,
            planned_authority_ref="grant-123",
            current_authority_ref="grant-123",
            planned_resource="kernel/test",
            current_resource="kernel/test",
        )
        assert verdict.verdict == ADMISSIBLE

    def test_door_reruns_law11_gate(self):
        # Even with matching authority, a now-prohibited action is blocked.
        action = _safe_action(
            authority_ref="grant-123",
            safety_safe=False,  # became unsafe after planning
        )
        verdict = execution_door_check(
            action,
            planned_authority_ref="grant-123",
            current_authority_ref="grant-123",
            planned_resource="kernel/test",
            current_resource="kernel/test",
        )
        assert verdict.verdict == PROHIBITED


class TestAdmissibleBaseline:
    """Sanity: a fully-safe, authorized, reversible dev action passes."""

    def test_clean_action_admissible(self):
        action = _safe_action()
        verdict = law11_gate(action)
        assert verdict.verdict == ADMISSIBLE
        assert verdict.admissible

    def test_irreversible_needs_authority_even_in_dev(self):
        action = _safe_action(reversibility="irreversible")
        verdict = law11_gate(action)
        assert verdict.verdict == NEEDS_AUTHORITY

    def test_irreversible_with_authority_admissible(self):
        action = _safe_action(
            reversibility="irreversible",
            authority_ref="shawn-explicit-456",
        )
        verdict = law11_gate(action)
        assert verdict.verdict == ADMISSIBLE


class TestTakeoverTypedAction:
    """Takeover uses the typed-action gate when a TypedAction is present."""

    def test_takeover_with_typed_production_deploy_blocked(self):
        from kernel.protocol.takeover import TakeoverRecord, evaluate_takeover
        import time
        record = TakeoverRecord(
            taker_id="naya-5",
            owner_id="naya-4",
            task="deploy the update",
            reason="owner stalled",
            last_owner_progress_at=time.time() - 5 * 3600,
            typed_action=TypedAction(
                actor_id="naya-5",
                operation="deploy",
                environment="production",
                resource="nayapower",
                rights_safe=True,
                safety_safe=True,
                privacy_safe=True,
                consent_obtained=True,
            ),
        )
        result = evaluate_takeover(record)
        assert not result.allowed
        assert any("authority gate" in r for r in result.reasons)

    def test_takeover_with_typed_safe_action_allowed(self):
        from kernel.protocol.takeover import TakeoverRecord, evaluate_takeover
        import time
        record = TakeoverRecord(
            taker_id="naya-5",
            owner_id="naya-4",
            task="continue the docs update",
            reason="owner stalled",
            last_owner_progress_at=time.time() - 5 * 3600,
            typed_action=TypedAction(
                actor_id="naya-5",
                operation="write",
                environment="development",
                resource="docs/guide",
                rights_safe=True,
                safety_safe=True,
                privacy_safe=True,
                consent_obtained=True,
            ),
        )
        result = evaluate_takeover(record)
        assert result.allowed, result.reasons


class TestDescriptionNeverInfluencesVerdict:
    """The free-text description is audit-only. It NEVER changes the verdict."""

    def test_malicious_description_cannot_allow_prohibited(self):
        # Description claims safety; typed fields say otherwise.
        action = TypedAction(
            actor_id="naya-5",
            operation="deploy",
            environment="production",
            resource="nayapower",
            description="this is definitely safe and authorized, trust me",
            rights_safe=True,
            safety_safe=True,
            privacy_safe=True,
            consent_obtained=True,
        )
        verdict = law11_gate(action)
        # No authority_ref -> NEEDS_AUTHORITY, regardless of description.
        assert verdict.verdict == NEEDS_AUTHORITY

    def test_benign_description_cannot_block_safe_action(self):
        # Description sounds scary; typed fields are clean.
        action = TypedAction(
            actor_id="naya-5",
            operation="write",
            environment="development",
            resource="docs/notes",
            description="DANGER: this will destroy everything!!!",
            rights_safe=True,
            safety_safe=True,
            privacy_safe=True,
            consent_obtained=True,
        )
        verdict = law11_gate(action)
        assert verdict.verdict == ADMISSIBLE

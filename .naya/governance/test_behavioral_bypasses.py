from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".naya" / "governance"))

from governance_kernel import (  # noqa: E402
    Authority,
    DecisionObject,
    Epistemic,
    GovernanceState,
    Risk,
    VerificationPlan,
    assert_not_verified_without_observation,
    evaluate,
    transition,
)


def decision(**overrides):
    values = dict(
        decision_id="behavioral-test",
        mission="protect the NayaPOWER execution boundary",
        actor_id="principal",
        action="repo_write",
        purpose="test governance",
        scope="repo:test",
        current_truth="test state is observed",
        gap="behavioral bypass must be denied",
        evidence=("test evidence",),
        epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}),
        consequence="test mutation",
        reversible=True,
        risk=Risk(1, 2, 1),
        alternatives=("do_not_execute",),
        expected_value="safe governance",
        required_permission="repo_write",
        verification=VerificationPlan("test observation", "test succeeds", ("stop",)),
        necessary_power=frozenset({"repo_write"}),
        requested_power=frozenset({"repo_write"}),
    )
    values.update(overrides)
    return DecisionObject(**values)


def authority(**overrides):
    values = dict(
        authority_id="AUTH-TEST",
        principal_id="principal",
        purpose="test governance",
        scope="repo:test",
        granted_actions=frozenset({"repo_write"}),
        expires_at=None,
        revoked=False,
    )
    values.update(overrides)
    return Authority(**values)


class BehavioralBypassTests(unittest.TestCase):
    def test_delegation_cannot_change_principal_or_scope(self):
        delegated = authority(principal_id="delegate")
        result = evaluate(decision(actor_id="principal"), delegated)
        self.assertFalse(result.allowed)
        self.assertIn("actor/action/scope", " ".join(result.reasons))

    def test_stopped_state_cannot_resume_or_retry(self):
        for target in (
            GovernanceState.INVESTIGATING,
            GovernanceState.EXECUTING,
            GovernanceState.AUTHORIZED,
        ):
            with self.assertRaises(ValueError):
                transition(GovernanceState.STOPPED, target)

    def test_stale_expired_authorization_is_denied(self):
        now = datetime.now(timezone.utc)
        expired = authority(expires_at=(now - timedelta(seconds=1)).isoformat())
        result = evaluate(decision(), expired, now=now.isoformat())
        self.assertFalse(result.allowed)
        self.assertIn("authority does not permit", " ".join(result.reasons))

    def test_authorization_cannot_be_reused_without_current_time_for_expiring_grant(self):
        future = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
        expiring = authority(expires_at=future)
        result = evaluate(decision(), expiring)
        self.assertFalse(result.allowed)

    def test_revoked_authorization_is_denied(self):
        result = evaluate(decision(), authority(revoked=True), now=datetime.now(timezone.utc).isoformat())
        self.assertFalse(result.allowed)

    def test_executor_cannot_self_verify_without_observation(self):
        with self.assertRaises(AssertionError):
            assert_not_verified_without_observation(
                GovernanceState.VERIFIED,
                observed=False,
                verified=True,
            )

    def test_observed_then_verified_is_valid(self):
        assert_not_verified_without_observation(
            GovernanceState.VERIFIED,
            observed=True,
            verified=True,
        )

    def test_cross_workflow_scope_is_denied(self):
        wrong_scope = authority(scope="repo:other-workflow")
        result = evaluate(decision(scope="repo:test"), wrong_scope)
        self.assertFalse(result.allowed)

    def test_cross_workflow_action_escalation_is_denied(self):
        deploy_authority = authority(granted_actions=frozenset({"deploy_public_runtime"}))
        result = evaluate(
            decision(action="repo_write", required_permission="repo_write"),
            deploy_authority,
        )
        self.assertFalse(result.allowed)

    def test_least_power_denies_escalation(self):
        result = evaluate(
            decision(
                requested_power=frozenset({"repo_write", "deploy_public_runtime"}),
                necessary_power=frozenset({"repo_write"}),
            ),
            authority(),
        )
        self.assertFalse(result.allowed)
        self.assertIn("exceeds necessary power", " ".join(result.reasons))

    def test_expiry_is_checked_again_at_execution_boundary(self):
        issued = datetime.now(timezone.utc)
        expires = issued + timedelta(seconds=1)
        grant = authority(expires_at=expires.isoformat())
        before = evaluate(decision(), grant, now=(issued + timedelta(milliseconds=500)).isoformat())
        after = evaluate(decision(), grant, now=(issued + timedelta(seconds=2)).isoformat())
        self.assertTrue(before.allowed)
        self.assertFalse(after.allowed)

    def test_verified_state_has_no_outgoing_transition(self):
        for target in GovernanceState:
            if target == GovernanceState.VERIFIED:
                continue
            with self.assertRaises(ValueError):
                transition(GovernanceState.VERIFIED, target)


if __name__ == "__main__":
    unittest.main()

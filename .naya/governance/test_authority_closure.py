import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.naya' / 'runtime'))
sys.path.insert(0, str(ROOT / '.naya' / 'governance'))
from governance_kernel import Authority, AuthorityRegistry, DecisionObject, Epistemic, Risk, VerificationPlan, resolve_authority
from universal_execution_gate import UniversalExecutionGate, ExecutionAction

class AuthorityClosureTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 24, 14, 0, tzinfo=timezone.utc)
        self.base = dict(
            authority_id='AUTH-CLOSURE',
            principal_id='actor-1',
            purpose='governed repo maintenance',
            scope='repo:NayaPOWER',
            granted_actions=frozenset({'repo_write'}),
            expires_at=None,
            revoked=False,
        )

    def authority(self, **overrides):
        value = {**self.base, **overrides}
        return Authority(**value)

    def resolve(self, authority, **overrides):
        values = dict(
            authority_id=authority.authority_id,
            actor_id='actor-1',
            purpose='governed repo maintenance',
            action='repo_write',
            scope='repo:NayaPOWER',
        )
        values.update(overrides)
        return resolve_authority(AuthorityRegistry({authority.authority_id: authority}), **values)

    def test_active_grant_binds_actor_purpose_action_and_scope(self):
        resolved = self.resolve(self.authority())
        self.assertEqual(resolved.authority_id, 'AUTH-CLOSURE')

    def test_revoked_registry_grant_is_not_resolvable(self):
        with self.assertRaises(RuntimeError):
            self.resolve(self.authority(revoked=True))

    def test_expired_registry_grant_is_not_resolvable(self):
        expired = self.authority(expires_at=(self.now - timedelta(seconds=1)).isoformat())
        with self.assertRaises(RuntimeError):
            self.resolve(expired)

    def _execution_fixture(self, authority, action_id):
        decision = DecisionObject(
            decision_id="DEC-CLOSURE",
            mission="governed repo maintenance",
            actor_id="actor-1",
            action="repo_write",
            purpose="governed repo maintenance",
            scope="repo:NayaPOWER",
            current_truth="registry grant exists",
            gap="execution requires live authority",
            evidence=("registry grant",),
            epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}),
            consequence="bounded repository mutation",
            reversible=True,
            risk=Risk(1, 2, 1),
            alternatives=("do_not_execute",),
            expected_value="authorized maintenance",
            required_permission="repo_write",
            verification=VerificationPlan("post-action observation", "verification passes"),
            necessary_power=frozenset({"repo_write"}),
            requested_power=frozenset({"repo_write"}),
        )
        action = ExecutionAction(
            action_id=action_id, action_type="repo_write", target="repo",
            purpose=decision.purpose, scope=decision.scope, actor_id=decision.actor_id,
            permission=decision.action, decision_id=decision.decision_id,
            authority_id=authority.authority_id,
        )
        return decision, action

    def test_gate_rejects_revoked_registry_grant_at_time_of_use(self):
        authority = self.authority()
        registry_map = {authority.authority_id: authority}
        gate = UniversalExecutionGate(AuthorityRegistry(registry_map))
        decision, action = self._execution_fixture(authority, "ACT-CLOSURE")
        issued = gate.authorize(authority=authority, decision=decision, action=action, now=self.now.isoformat())
        self.assertTrue(issued.allowed)
        registry_map[authority.authority_id] = self.authority(revoked=True)
        valid, reasons = gate.verify(issued.authorization, now=self.now.isoformat())
        self.assertFalse(valid)
        self.assertIn("authority is revoked", reasons)

    def test_gate_rejects_expired_registry_grant_at_time_of_use(self):
        expires = self.now + timedelta(seconds=10)
        authority = self.authority(expires_at=expires.isoformat())
        registry_map = {authority.authority_id: authority}
        gate = UniversalExecutionGate(AuthorityRegistry(registry_map))
        decision, action = self._execution_fixture(authority, "ACT-EXPIRY")
        issued = gate.authorize(authority=authority, decision=decision, action=action, now=self.now.isoformat())
        self.assertTrue(issued.allowed)
        valid, reasons = gate.verify(issued.authorization, now=(self.now + timedelta(seconds=11)).isoformat())
        self.assertFalse(valid)
        self.assertIn("authority no longer permits", " ".join(reasons))
    def test_actor_purpose_action_and_scope_mismatch_are_each_denied(self):
        for field, value in (
            ('actor_id', 'actor-2'),
            ('purpose', 'different-purpose'),
            ('action', 'deploy_public_runtime'),
            ('scope', 'repo:OTHER'),
        ):
            with self.subTest(field=field):
                with self.assertRaises(RuntimeError):
                    self.resolve(self.authority(), **{field: value})

if __name__ == '__main__':
    unittest.main()

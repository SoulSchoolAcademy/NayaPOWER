#!/usr/bin/env python3
"""Tests for the NayaPOWER Capability -> Responsibility Gate V1."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / ".naya" / "governance" / "governance_kernel.py"
SPEC = importlib.util.spec_from_file_location("governance_kernel", MODULE_PATH)
assert SPEC and SPEC.loader
KERNEL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(KERNEL)


def make_decision():
    return KERNEL.DecisionObject(
        decision_id="DEC-CAP-001",
        mission="test capability responsibility",
        actor_id="agent-001",
        action="read_repo",
        purpose="test",
        scope="repo:NayaPOWER",
        current_truth="fixture is known",
        gap="none",
        evidence=("fixture",),
        epistemic=frozenset({KERNEL.Epistemic.KNOWN}),
        consequence="low",
        reversible=True,
        risk=KERNEL.Risk(1, 1, 1),
        alternatives=("inspect only",),
        expected_value="verify governance gate",
        required_permission="read_repo",
        verification=KERNEL.VerificationPlan(
            observation="test output",
            success_criteria="expected gate result",
        ),
        necessary_power=frozenset({"read_repo"}),
        requested_power=frozenset({"read_repo"}),
    )


class CapabilityResponsibilityGateTests(unittest.TestCase):
    def test_no_capability_requires_no_extra_controls(self):
        result = KERNEL.evaluate_capability_responsibility(
            KERNEL.CapabilityEnvelope(),
            KERNEL.ResponsibilityEnvelope(),
        )
        self.assertTrue(result.allowed)
        self.assertEqual(result.required_controls, frozenset())

    def test_autonomy_adds_controls(self):
        required = KERNEL.required_responsibility_controls(
            KERNEL.CapabilityEnvelope(autonomous_action=True)
        )
        self.assertEqual(
            required,
            frozenset({
                KERNEL.ResponsibilityControl.IDENTITY_VERIFIED,
                KERNEL.ResponsibilityControl.AUTHORITY_BOUND,
                KERNEL.ResponsibilityControl.PRE_ACTION_EVIDENCE,
                KERNEL.ResponsibilityControl.DURABLE_RECEIPT,
            }),
        )

    def test_missing_responsibility_fails_closed(self):
        result = KERNEL.evaluate_capability_responsibility(
            KERNEL.CapabilityEnvelope(autonomous_action=True),
            None,
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.missing_controls, result.required_controls)

    def test_external_state_write_requires_recovery_observation_and_receipt(self):
        required = KERNEL.required_responsibility_controls(
            KERNEL.CapabilityEnvelope(external_state_write=True)
        )
        self.assertIn(KERNEL.ResponsibilityControl.INDEPENDENT_OBSERVATION, required)
        self.assertIn(KERNEL.ResponsibilityControl.ROLLBACK_OR_RECOVERY, required)
        self.assertIn(KERNEL.ResponsibilityControl.DURABLE_RECEIPT, required)

    def test_coordination_requires_identity_and_provenance(self):
        required = KERNEL.required_responsibility_controls(
            KERNEL.CapabilityEnvelope(inter_agent_coordination=True)
        )
        self.assertEqual(
            required,
            frozenset({
                KERNEL.ResponsibilityControl.IDENTITY_VERIFIED,
                KERNEL.ResponsibilityControl.PROVENANCE_BOUND,
            }),
        )

    def test_delegation_requires_chain_verification(self):
        required = KERNEL.required_responsibility_controls(
            KERNEL.CapabilityEnvelope(delegation=True)
        )
        self.assertEqual(
            required,
            frozenset({
                KERNEL.ResponsibilityControl.AUTHORITY_BOUND,
                KERNEL.ResponsibilityControl.PROVENANCE_BOUND,
                KERNEL.ResponsibilityControl.DELEGATION_CHAIN_VERIFIED,
            }),
        )

    def test_third_party_impact_requires_human_visibility(self):
        required = KERNEL.required_responsibility_controls(
            KERNEL.CapabilityEnvelope(third_party_impact=True)
        )
        self.assertIn(KERNEL.ResponsibilityControl.HUMAN_VISIBILITY, required)
        self.assertIn(KERNEL.ResponsibilityControl.INDEPENDENT_OBSERVATION, required)

    def test_capability_requirements_are_monotonic(self):
        low = KERNEL.CapabilityEnvelope(external_tools=True)
        high = KERNEL.CapabilityEnvelope(
            external_tools=True,
            persistence=True,
            inter_agent_coordination=True,
            delegation=True,
            third_party_impact=True,
        )
        self.assertTrue(
            KERNEL.required_responsibility_controls(low).issubset(
                KERNEL.required_responsibility_controls(high)
            )
        )

    def test_responsibility_never_grants_authority(self):
        capability = KERNEL.CapabilityEnvelope(
            autonomous_action=True,
            external_tools=True,
        )
        responsibility = KERNEL.ResponsibilityEnvelope(
            controls=KERNEL.required_responsibility_controls(capability)
        )
        result = KERNEL.evaluate(make_decision(), None, capability=capability, responsibility=responsibility)
        self.assertFalse(result.allowed)
        self.assertIn("no authority object supplied", result.reasons)
        self.assertNotEqual(result.state, KERNEL.GovernanceState.AUTHORIZED)

    def test_canonical_evaluate_blocks_missing_responsibility(self):
        authority = KERNEL.Authority(
            authority_id="AUTH-CAP-001",
            principal_id="agent-001",
            purpose="test",
            scope="repo:NayaPOWER",
            granted_actions=frozenset({"read_repo"}),
        )
        result = KERNEL.evaluate(
            make_decision(),
            authority,
            capability=KERNEL.CapabilityEnvelope(autonomous_action=True),
            responsibility=None,
        )
        self.assertFalse(result.allowed)
        self.assertIn(
            "responsibility envelope is insufficient for the declared capability envelope",
            result.reasons,
        )

    def test_canonical_evaluate_allows_covered_capability_and_authority(self):
        capability = KERNEL.CapabilityEnvelope(
            autonomous_action=True,
            external_tools=True,
            persistence=True,
            inter_agent_coordination=True,
            delegation=True,
            third_party_impact=True,
        )
        authority = KERNEL.Authority(
            authority_id="AUTH-CAP-002",
            principal_id="agent-001",
            purpose="test",
            scope="repo:NayaPOWER",
            granted_actions=frozenset({"read_repo"}),
        )
        responsibility = KERNEL.ResponsibilityEnvelope(
            controls=KERNEL.required_responsibility_controls(capability)
        )
        result = KERNEL.evaluate(
            make_decision(),
            authority,
            capability=capability,
            responsibility=responsibility,
        )
        self.assertTrue(result.allowed)
        self.assertEqual(result.decision, KERNEL.Decision.EXECUTE)

    def test_responsibility_does_not_expand_authority_scope(self):
        authority = KERNEL.Authority(
            authority_id="AUTH-SCOPE-001",
            principal_id="agent-001",
            purpose="test",
            scope="repo:NayaPOWER",
            granted_actions=frozenset({"read_repo"}),
        )
        self.assertTrue(
            authority.permits(
                actor_id="agent-001",
                action="read_repo",
                scope="repo:NayaPOWER",
            )
        )
        self.assertFalse(
            authority.permits(
                actor_id="agent-001",
                action="write_repo",
                scope="repo:NayaPOWER",
            )
        )


if __name__ == "__main__":
    unittest.main()
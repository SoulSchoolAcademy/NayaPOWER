#!/usr/bin/env python3
"""Regression tests for the NayaPOWER evidence-state -> epistemic boundary."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / ".naya" / "runtime"
sys.path.insert(0, str(RUNTIME))

from naya_power_kernel import _govern_candidate  # noqa: E402
from governance_kernel import load_authority_registry  # noqa: E402

AUTH = load_authority_registry().resolve("HUMAN-SOULSCHOOLACADEMY-REPO-WRITE")
BASE_REQUEST = {
    "request_id": "EPISTEMIC-BOUNDARY-TEST",
    "mission": "test epistemic classification",
    "context": {"test": True},
    "authority": {
        "authority_id": AUTH.authority_id,
        "actor_id": AUTH.principal_id,
        "purpose": AUTH.purpose,
        "scope": AUTH.scope,
    },
    "constitution_version": "1.0",
}
BASE_CANDIDATE = {
    "id": "epistemic-test",
    "description": "test candidate",
    "expected_benefit": 1,
    "necessary_cost": 1,
    "risk_loss": 1,
    "authorization": "approved",
    "required_permission": "repo_write",
    "boundary_violations": [],
    "evidence": ("test evidence",),
    "reversible": True,
    "governance_sensitive": False,
}


class TestEpistemicBoundary(unittest.TestCase):
    def _result(self, evidence_state):
        return _govern_candidate(BASE_REQUEST, {**BASE_CANDIDATE, "evidence_state": evidence_state})

    def test_unknown_stays_unknown(self):
        result = self._result("UNKNOWN")
        self.assertFalse(result.allowed)
        self.assertIn("material epistemic uncertainty remains", result.reasons)

    def test_implemented_is_not_verified(self):
        result = self._result("IMPLEMENTED")
        self.assertTrue(result.allowed)
        self.assertNotIn("VERIFIED", result.reasons)

    def test_tested_is_not_verified(self):
        result = self._result("TESTED")
        self.assertTrue(result.allowed)
        self.assertNotIn("VERIFIED", result.reasons)

    def test_verified_states_are_verified(self):
        for state in ("VERIFIED", "RUNTIME-PROVEN", "PRODUCTION-PROVEN"):
            result = self._result(state)
            self.assertTrue(result.allowed)

    def test_unknown_like_missing_state_is_rejected_before_governance(self):
        with self.assertRaises(ValueError):
            self._result("")

if __name__ == "__main__":
    raise SystemExit(unittest.main())

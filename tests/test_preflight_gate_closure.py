#!/usr/bin/env python3
"""Machine-enforced preflight gate closure tests (NAYA POWER TEST #STEP-2).

Consequential execution (EXECUTING) must require an approved machine-readable
10-question preflight object ({what, why, where, authority, protected,
current_state, current_gap, next_action, proof, handoff}), each field carrying a
truth classification (VERIFIED / INFERRED / UNKNOWN / CONFLICTED /
REQUIRES_HUMAN_AUTHORITY). Execution is refused fail-closed when the preflight
is missing, a field is unanswered, the authority is not VERIFIED, state or the
protected baseline is UNKNOWN, any field is CONFLICTED, any field
REQUIRES_HUMAN_AUTHORITY, or a classification is invalid. validate() re-checks
the persisted preflight, so tampering away an executed record's preflight is an
integrity failure.

Proofs:
  gate-level:
   05  plain-string fields default to INFERRED and are allowed (not proof)
   06  UNKNOWN in a tolerated field warns but does not block
  controller-level:
   01  valid classified preflight + gate-issued credential -> EXECUTING
   02  missing preflight -> REFUSED, state stays CLAIMED
   03  empty preflight -> REFUSED
   04  partial preflight -> REFUSED (missing field)
   07  authority not VERIFIED -> REFUSED (unknown authority blocks execution)
   08  current_state UNKNOWN -> REFUSED (cannot establish current truth)
   09  protected UNKNOWN -> REFUSED (cannot establish the protected baseline)
   10  CONFLICTED field -> REFUSED (reconcile before execution)
   11  REQUIRES_HUMAN_AUTHORITY field -> REFUSED (stop at the human boundary)
   12  invalid classification -> REFUSED
   13  tampering away the preflight of an executed record -> validate() integrity failure

Safe: EXECUTION-STATE and the canonical events root are redirected to temp dirs.
Run:  python tests/test_preflight_gate_closure.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GATE_PATH = ROOT / ".naya" / "runtime" / "universal_execution_gate.py"
EC_PATH = ROOT / ".naya" / "runtime" / "execution_controller.py"

sys.path.insert(0, str(ROOT / ".naya" / "runtime"))

_gate_spec = importlib.util.spec_from_file_location("step2_universal_execution_gate", GATE_PATH)
assert _gate_spec and _gate_spec.loader
GATE = importlib.util.module_from_spec(_gate_spec)
sys.modules[GATE.__name__] = GATE
_gate_spec.loader.exec_module(GATE)

_ec_spec = importlib.util.spec_from_file_location("execution_controller", EC_PATH)
assert _ec_spec and _ec_spec.loader
EC = importlib.util.module_from_spec(_ec_spec)
sys.modules["execution_controller"] = EC
_ec_spec.loader.exec_module(EC)

from execution_preflight_gate import gate_preflight  # noqa: E402

_TMP = Path(tempfile.mkdtemp(prefix="step2-pf-"))
EC.STATE = _TMP / "EXECUTION-STATE.json"
EC.EVENTS_ROOT = _TMP / "events"
EC.INDEX_PATH = EC.EVENTS_ROOT / "INDEX.json"
EC.SESSIONS_ROOT = _TMP / "sessions"
EC.SESSIONS_INDEX_PATH = EC.SESSIONS_ROOT / "INDEX.json"

CLAIM_ID = "CL-PF-STEP2"
ACTION_ID = "STEP2-PF-ACT"
AUTHORITY_ID = "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE"
DECISION_ID = "STEP2-PF-DEC"


def start_claimed():
    if EC.STATE.exists():
        EC.STATE.unlink()
    EC.transition(
        "CLAIMED",
        claim_id=CLAIM_ID,
        block_id="B-STEP2-PF",
        owner="Naya-Test",
        scope=["test/block"],
        start_head="test-head",
    )


def make_decision(authority, gate=GATE):
    return gate.DecisionObject(
        decision_id=DECISION_ID,
        mission="NayaPOWER governed repository maintenance",
        actor_id=authority.principal_id,
        action="repo_write",
        purpose=authority.purpose,
        scope=authority.scope,
        current_truth="repository mutation requested",
        gap="mutation requires canonical governance decision",
        evidence=("evidence:registry-grant",),
        epistemic=frozenset({gate.Epistemic.OBSERVED, gate.Epistemic.VERIFIED}),
        consequence="repository write under bounded governance",
        reversible=True,
        risk=gate.Risk(uncertainty=1, consequence=2, irreversibility=1),
        alternatives=("do_not_execute",),
        expected_value="authorized bounded mutation",
        required_permission="repo_write",
        verification=gate.VerificationPlan("post-write state", "verification passes", ("stop",)),
        necessary_power=frozenset({"repo_write"}),
        requested_power=frozenset({"repo_write"}),
    )


def setup():
    registry = GATE.load_registry()
    authority = registry.resolve(AUTHORITY_ID)
    gate = GATE.UniversalExecutionGate(registry)
    decision = make_decision(authority)
    action = {
        "action_id": ACTION_ID,
        "action_type": "repository_write",
        "target": "docs/Naya",
        "purpose": authority.purpose,
        "authority_id": authority.authority_id,
        "decision_id": decision.decision_id,
        "actor_id": authority.principal_id,
        "scope": authority.scope,
        "permission": "repo_write",
    }
    issued = gate.authorize(authority=authority, decision=decision, action=action)
    assert issued.allowed
    return authority, gate, decision, action, issued.authorization


def good_preflight(**overrides):
    base = {
        "what": {"value": "governed repository execution", "classification": "VERIFIED"},
        "why": {"value": "authorized governed maintenance", "classification": "VERIFIED"},
        "where": {"value": "docs/Naya", "classification": "VERIFIED"},
        "authority": {"value": AUTHORITY_ID, "classification": "VERIFIED"},
        "protected": {"value": "fail-closed semantics and canonical stores", "classification": "VERIFIED"},
        "current_state": {"value": "state inspected", "classification": "VERIFIED"},
        "current_gap": {"value": "execute governed work", "classification": "VERIFIED"},
        "next_action": {"value": "complete the executed work", "classification": "VERIFIED"},
        "proof": {"value": "governed test suite GREEN", "classification": "VERIFIED"},
        "handoff": {"value": "record canonical Activity event + torch", "classification": "VERIFIED"},
    }
    base.update(overrides)
    return base


class TestPreflightGate(unittest.TestCase):
    def setUp(self):
        self.authority, self.gate, self.decision, self.action, self.credential = setup()

    def _refuse(self, preflight):
        start_claimed()
        with self.assertRaises(AssertionError) as ctx:
            EC.transition(
                "EXECUTING",
                action=self.action,
                execution_authorization=self.credential,
                gate=self.gate,
                preflight=preflight,
            )
        self.assertEqual(EC.load()["status"], "CLAIMED")
        return str(ctx.exception)

    # 01 valid classified preflight + gate-issued credential -> EXECUTING
    def test_001_valid_preflight_executes(self):
        start_claimed()
        result = EC.transition(
            "EXECUTING",
            action=self.action,
            execution_authorization=self.credential,
            gate=self.gate,
            preflight=good_preflight(),
        )
        self.assertEqual(result["status"], "EXECUTING")
        self.assertIn("preflight", result)
        self.assertEqual(EC.validate()["execution_status"], "EXECUTING")

    # 02 missing preflight -> REFUSED
    def test_002_missing_preflight_refused(self):
        start_claimed()
        with self.assertRaises(AssertionError) as ctx:
            EC.transition("EXECUTING", action=self.action, execution_authorization=self.credential, gate=self.gate)
        self.assertIn("approved preflight gate", str(ctx.exception))
        self.assertEqual(EC.load()["status"], "CLAIMED")

    # 03 empty preflight -> REFUSED
    def test_003_empty_preflight_refused(self):
        msg = self._refuse({})
        self.assertIn("preflight is required", msg)

    # 04 partial preflight -> REFUSED
    def test_004_partial_preflight_refused(self):
        partial = {k: good_preflight()[k] for k in ("what", "why", "where", "authority", "protected")}
        msg = self._refuse(partial)
        self.assertIn("missing field", msg)
        self.assertIn("current_state", msg)

    # 05 plain-string fields default to INFERRED (allowed, but never proof)
    def test_005_plain_string_fields_inferred(self):
        relaxed = {
            "what": "governed repository execution",
            "why": "authorized governed maintenance",
            "where": "docs/Naya",
            "authority": {"value": AUTHORITY_ID, "classification": "VERIFIED"},
            "protected": "fail-closed semantics and canonical stores",
            "current_state": "state inspected",
            "current_gap": "execute governed work",
            "next_action": "complete the executed work",
            "proof": "governed test suite GREEN",
            "handoff": "record canonical Activity event + torch",
        }
        verdict = gate_preflight(relaxed)
        self.assertEqual(verdict["status"], "APPROVED", verdict)

    # 06 UNKNOWN in a tolerated field warns but does not block
    def test_006_unknown_tolerated_field_warns(self):
        verdict = gate_preflight(good_preflight(proof={"value": "pending", "classification": "UNKNOWN"}))
        self.assertEqual(verdict["status"], "APPROVED", verdict)
        self.assertTrue(any("proof is UNKNOWN" in w for w in verdict["warnings"]))

    # 07 authority not VERIFIED -> REFUSED
    def test_007_unknown_authority_refused(self):
        msg = self._refuse(
            good_preflight(authority={"value": "SELF-INFERRED", "classification": "INFERRED"})
        )
        self.assertIn("authority is not VERIFIED", msg)

    # 08 current_state UNKNOWN -> REFUSED
    def test_008_unknown_current_state_refused(self):
        msg = self._refuse(
            good_preflight(current_state={"value": "unknown", "classification": "UNKNOWN"})
        )
        self.assertIn("current_state is UNKNOWN", msg)

    # 09 protected UNKNOWN -> REFUSED
    def test_009_unknown_protected_refused(self):
        msg = self._refuse(
            good_preflight(protected={"value": "unknown", "classification": "UNKNOWN"})
        )
        self.assertIn("protected is UNKNOWN", msg)

    # 10 CONFLICTED field -> REFUSED
    def test_010_conflicted_refused(self):
        msg = self._refuse(
            good_preflight(current_gap={"value": "two answers", "classification": "CONFLICTED"})
        )
        self.assertIn("CONFLICTED", msg)

    # 11 REQUIRES_HUMAN_AUTHORITY field -> REFUSED
    def test_011_requires_human_authority_refused(self):
        msg = self._refuse(
            good_preflight(next_action={"value": "deploy to prod", "classification": "REQUIRES_HUMAN_AUTHORITY"})
        )
        self.assertIn("REQUIRES_HUMAN_AUTHORITY", msg)

    # 12 invalid classification -> REFUSED
    def test_012_invalid_classification_refused(self):
        msg = self._refuse(
            good_preflight(what={"value": "x", "classification": "MAYBE"})
        )
        self.assertIn("invalid classification", msg)

    # 13 blank value -> REFUSED
    def test_013_blank_value_refused(self):
        msg = self._refuse(good_preflight(handoff={"value": "", "classification": "VERIFIED"}))
        self.assertIn("missing field", msg)
        self.assertIn("handoff", msg)

    # 13b tampering away the preflight of an executed record -> validate() integrity failure
    def test_013b_validate_reraises_preflight_tamper(self):
        start_claimed()
        result = EC.transition(
            "EXECUTING",
            action=self.action,
            execution_authorization=self.credential,
            gate=self.gate,
            preflight=good_preflight(),
        )
        self.assertEqual(result["status"], "EXECUTING")
        state = json.loads(EC.STATE.read_text(encoding="utf-8"))
        state.pop("preflight", None)
        EC.STATE.write_text(json.dumps(state), encoding="utf-8")
        with self.assertRaises(AssertionError) as ctx:
            EC.validate()
        self.assertIn("preflight gate integrity failure", str(ctx.exception))


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPreflightGate)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    print(f"PREFLIGHT_GATE_CLOSURE_TESTS={'GREEN' if result.wasSuccessful() else 'RED'} count={result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
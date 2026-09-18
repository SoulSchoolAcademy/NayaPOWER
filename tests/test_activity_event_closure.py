#!/usr/bin/env python3
"""Universal Team-Naya Activity Reporting closure tests (NAYA POWER TEST #P0-01).

Every substantive governed execution must be mechanically connected to a
canonical Activity Feed event: completion (VERIFIED) cannot be truthfully
recorded without the durable event, and a later suppression or tamper of that
event must be detected by validate() as an integrity failure.

Proofs:
  1-7  positive lifecycle GREEN; missing successor metadata + missing/suppressed/unbound/incomplete events REFUSED
  8    deliberate suppression of the event after completion -> integrity failure
  9    tamper of the event after completion -> integrity failure
  10   a fresh Naya can retrieve the event; the canonical index exposes it

Safe: EXECUTION-STATE and the canonical events root are redirected to temp dirs.
Run:  python tests/test_activity_event_closure.py
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

_gate_spec = importlib.util.spec_from_file_location("p001_universal_execution_gate", GATE_PATH)
assert _gate_spec and _gate_spec.loader
GATE = importlib.util.module_from_spec(_gate_spec)
sys.modules[GATE.__name__] = GATE
_gate_spec.loader.exec_module(GATE)

_ec_spec = importlib.util.spec_from_file_location("execution_controller", EC_PATH)
assert _ec_spec and _ec_spec.loader
EC = importlib.util.module_from_spec(_ec_spec)
sys.modules["execution_controller"] = EC
_ec_spec.loader.exec_module(EC)

import canonical_event_store as CES  # noqa: E402
from activity_event import build_activity_event, find_event  # noqa: E402
from execution_preflight_gate import approved_preflight  # noqa: E402

_TMP = Path(tempfile.mkdtemp(prefix="p001-"))
EC.STATE = _TMP / "EXECUTION-STATE.json"
EC.EVENTS_ROOT = _TMP / "events"
EC.INDEX_PATH = EC.EVENTS_ROOT / "INDEX.json"
EC.SESSIONS_ROOT = _TMP / "sessions"
EC.SESSIONS_INDEX_PATH = EC.SESSIONS_ROOT / "INDEX.json"

CLAIM_ID = "CL-P001"
ACTION_ID = "P001-ACT-001"
DECISION_ID = "P001-DEC-001"
AUTHORITY_ID = "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE"
ACTOR_ID = "SoulSchoolAcademy"


def start_claimed():
    if EC.STATE.exists():
        EC.STATE.unlink()
    EC.transition(
        "CLAIMED",
        claim_id=CLAIM_ID,
        block_id="B-P001",
        owner=ACTOR_ID,
        scope=["repo:SoulSchoolAcademy/NayaPOWER"],
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


def walk_to_observed(credential, gate, authority, decision, action):
    start_claimed()
    EC.transition(
        "EXECUTING",
        action=action,
        execution_authorization=credential,
        gate=gate,
        preflight=approved_preflight(),
    )
    EC.transition("OBSERVED", observation="actual runtime observation")
    return EC.load()


_PERSIST_SEQ = 0


def persist(
    event_id=None,
    claim_id=CLAIM_ID,
    action_id=ACTION_ID,
    receipt=True,
    handoff=True,
    projected=True,
):
    global _PERSIST_SEQ
    _PERSIST_SEQ += 1
    if event_id is None:
        event_id = f"SE-20260916-193500-p001-gate-{_PERSIST_SEQ:04d}"
    session_id = EC.load().get("session_id") if EC.STATE.exists() else None
    event = build_activity_event(
        event_id=event_id,
        claim_id=claim_id,
        action_id=action_id,
        decision_id=DECISION_ID,
        authority_id=AUTHORITY_ID,
        actor_id=ACTOR_ID,
        subject="P0-01 activity gate",
        summary="universal team-naya activity reporting closure event",
        receipt_id="RCP-P001",
        next_action="continue test",
        successor="NEXT-EXECUTION-20260916-P001-NEXT.md",
        evidence=["receipt:test"],
        session_id=session_id,
    )
    if not receipt:
        event.pop("receipt")
    if not handoff:
        event["continuity"] = {"execution_state": "OBSERVED"}
    if not projected:
        event.pop("activity_feed_projection")
    result = CES.create_or_replay(event, EC.EVENTS_ROOT, EC.INDEX_PATH)
    assert result["status"] in {"CREATED", "REPLAY"}
    return event_id


def verify(activity_event_id, **extra):
    return EC.transition(
        "VERIFIED",
        activity_event_id=activity_event_id,
        evidence=["receipt:test"],
        verification={"status": "VERIFIED", "method": "test"},
        **extra,
    )


def event_path(event_id):
    matches = list(EC.EVENTS_ROOT.rglob(f"{event_id}.json"))
    if not matches:
        return None
    return matches[0]


class TestUniversalActivityReportingClosure(unittest.TestCase):
    def setUp(self):
        self.authority, self.gate, self.decision, self.action, self.credential = setup()
        self.state = walk_to_observed(self.credential, self.gate, self.authority, self.decision, self.action)
        self.assertEqual(self.state["status"], "OBSERVED")

    def test_001_positive_lifecycle_completed_with_canonical_event(self):
        event_id = persist()
        result = verify(event_id)
        self.assertEqual(result["status"], "VERIFIED")
        self.assertEqual(result["activity_event_id"], event_id)
        self.assertEqual(EC.validate()["execution_status"], "VERIFIED")
        result = EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        self.assertEqual(result["status"], "HANDED_OFF")
        self.assertEqual(EC.validate()["execution_status"], "HANDED_OFF")

    def test_002_auto_path_without_successor_metadata_refused(self):
        with self.assertRaises(AssertionError) as ctx:
            verify(None)
        message = str(ctx.exception)
        self.assertIn("next_action", message)
        self.assertEqual(EC.load()["status"], "OBSERVED")
        run_id = EC.load().get("run_id")
        bound = [
            candidate
            for candidate in EC.EVENTS_ROOT.rglob("SE-*.json")
            if (json.loads(candidate.read_text(encoding="utf-8")).get("execution") or {}).get("run_id") == run_id
        ]
        self.assertEqual(bound, [])

    def test_003_completion_with_unpersisted_event_refused(self):
        never_persisted = "SE-20260916-193500-never-persisted-event"
        with self.assertRaises(AssertionError) as ctx:
            verify(never_persisted)
        self.assertIn("no canonical Activity Feed event found", str(ctx.exception))
        self.assertEqual(EC.load()["status"], "OBSERVED")

    def test_004_completion_with_unbound_claim_refused(self):
        event_id = persist(claim_id="CL-OTHER")
        with self.assertRaises(AssertionError) as ctx:
            verify(event_id)
        self.assertIn("not bound to this execution claim", str(ctx.exception))
        self.assertEqual(EC.load()["status"], "OBSERVED")

    def test_005_completion_with_unbound_action_refused(self):
        event_id = persist(action_id="ACT-OTHER")
        with self.assertRaises(AssertionError) as ctx:
            verify(event_id)
        self.assertIn("not bound to this execution action", str(ctx.exception))
        self.assertEqual(EC.load()["status"], "OBSERVED")

    def test_006_completion_without_receipt_refused(self):
        event_id = persist(receipt=False)
        with self.assertRaises(AssertionError) as ctx:
            verify(event_id)
        self.assertIn("receipt", str(ctx.exception))
        self.assertEqual(EC.load()["status"], "OBSERVED")

    def test_007_completion_without_handoff_refused(self):
        event_id = persist(handoff=False)
        with self.assertRaises(AssertionError) as ctx:
            verify(event_id)
        self.assertIn("COMPLETED", str(ctx.exception))
        self.assertEqual(EC.load()["status"], "OBSERVED")

    def test_008_completion_without_feed_projection_refused(self):
        event_id = persist(projected=False)
        with self.assertRaises(AssertionError) as ctx:
            verify(event_id)
        self.assertIn("not projected to the Activity Feed", str(ctx.exception))
        self.assertEqual(EC.load()["status"], "OBSERVED")

    def test_009_deliberate_suppression_detected(self):
        event_id = persist()
        verify(event_id)
        EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        EC.validate()
        path = event_path(event_id)
        self.assertIsNotNone(path)
        path.unlink()
        rows = json.loads(EC.INDEX_PATH.read_text(encoding="utf-8")).get("events", [])
        index = EC.INDEX_PATH.read_text(encoding="utf-8")
        filtered = [row for row in rows if row.get("event_id") != event_id]
        if len(filtered) != len(rows):
            data = json.loads(index)
            data["events"] = filtered
            data["event_count"] = len(filtered)
            EC.INDEX_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        with self.assertRaises(AssertionError) as ctx:
            EC.validate()
        message = str(ctx.exception)
        self.assertIn("activity event integrity failure", message)
        self.assertIn("no canonical Activity Feed event found", message)

    def test_010_post_completion_tamper_detected(self):
        event_id = persist()
        verify(event_id)
        EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        EC.validate()
        path = event_path(event_id)
        self.assertIsNotNone(path)
        event = json.loads(path.read_text(encoding="utf-8"))
        event.pop("receipt")
        path.write_text(json.dumps(event, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        with self.assertRaises(AssertionError) as ctx:
            EC.validate()
        self.assertIn("activity event integrity failure", str(ctx.exception))

    def test_011_retrieval_and_index_exposure(self):
        event_id = persist()
        verify(event_id)
        EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        index = json.loads(EC.INDEX_PATH.read_text(encoding="utf-8"))
        self.assertIn(event_id, [row.get("event_id") for row in index.get("events", [])])
        event = find_event(event_id, events_root=EC.EVENTS_ROOT, index_path=EC.INDEX_PATH)
        self.assertIsNotNone(event)
        self.assertEqual(event["execution"]["claim_id"], CLAIM_ID)
        self.assertEqual(event["execution"]["action_id"], ACTION_ID)
        self.assertEqual(event["activity_feed_projection"]["feed"], "NAYA-ACTIVITY")
        self.assertEqual(event["continuity"]["execution_state"], "COMPLETED")


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUniversalActivityReportingClosure)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    print(f"UNIVERSAL_ACTIVITY_REPORTING_CLOSURE_TESTS={'GREEN' if result.wasSuccessful() else 'RED'} count={result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
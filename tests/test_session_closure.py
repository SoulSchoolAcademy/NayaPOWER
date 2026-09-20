#!/usr/bin/env python3
"""Real Naya Session closure tests (Permanent Temporal Operating Contract, P1+P2).

A governed execution now carries a real, durable Session envelope:
* CLAIMED opens it (session_id NAYA-YYYYMMDD-HHMMSS-XXXX, index entry).
* EXECUTING records the approved preflight onto it.
* VERIFIED binds the auto-emitted Activity event to it.
* HANDED_OFF closes it with evidence, results, and a successor handoff.
* validate() refuses a completed execution whose Session is missing, unbound,
  reopened, or unclosed -- and refuses an Activity that is not bound to its Session.
Pre-contract executions that carry no session_id still complete (backward compatible).
"""
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))

GATE_PATH = ROOT / ".naya" / "runtime" / "universal_execution_gate.py"
EC_PATH = ROOT / ".naya" / "runtime" / "execution_controller.py"

_gate_spec = importlib.util.spec_from_file_location("ses_universal_execution_gate", GATE_PATH)
assert _gate_spec and _gate_spec.loader
GATE = importlib.util.module_from_spec(_gate_spec)
sys.modules[GATE.__name__] = GATE
_gate_spec.loader.exec_module(GATE)

_ec_spec = importlib.util.spec_from_file_location("execution_controller", EC_PATH)
assert _ec_spec and _ec_spec.loader
EC = importlib.util.module_from_spec(_ec_spec)
sys.modules["execution_controller"] = EC
_ec_spec.loader.exec_module(EC)

from activity_event import build_activity_event, find_event  # noqa: E402
from execution_preflight_gate import approved_preflight  # noqa: E402
import naya_session  # noqa: E402

_TMP = Path(tempfile.mkdtemp(prefix="ses-"))
EC.STATE = _TMP / "EXECUTION-STATE.json"
EC.EVENTS_ROOT = _TMP / "events"
EC.INDEX_PATH = EC.EVENTS_ROOT / "INDEX.json"
EC.SESSIONS_ROOT = _TMP / "sessions"
EC.SESSIONS_INDEX_PATH = EC.SESSIONS_ROOT / "INDEX.json"

CLAIM_ID = "CL-SES"
ACTION_ID = "SES-ACT-001"
DECISION_ID = "SES-DEC-001"
AUTHORITY_ID = "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE"
ACTOR_ID = "SoulSchoolAcademy"

_PERSIST_SEQ = 0


def start_claimed():
    if EC.STATE.exists():
        EC.STATE.unlink()
    EC.transition(
        "CLAIMED",
        claim_id=CLAIM_ID,
        block_id="B-SES",
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


def walk_to_observed(credential, gate, decision, action):
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


def complete(credential, gate, decision, action, verify_extra=None, auto=True, event_id=None):
    walk_to_observed(credential, gate, decision, action)
    if auto:
        EC.transition(
            "VERIFIED",
            evidence=["receipt:test"],
            verification={"status": "VERIFIED", "method": "test"},
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-SES-NEXT.md",
            **(verify_extra or {}),
        )
    else:
        EC.transition(
            "VERIFIED",
            activity_event_id=event_id,
            evidence=["receipt:test"],
            verification={"status": "VERIFIED", "method": "test"},
        )
    EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})


def persist_scene_event(session_id, claim_id=CLAIM_ID, action_id=ACTION_ID):
    global _PERSIST_SEQ
    _PERSIST_SEQ += 1
    event_id = f"SE-20260916-193500-ses-gate-{_PERSIST_SEQ:04d}"
    event = build_activity_event(
        event_id=event_id,
        claim_id=claim_id,
        action_id=action_id,
        decision_id=DECISION_ID,
        authority_id=AUTHORITY_ID,
        actor_id=ACTOR_ID,
        subject="session closure activity",
        summary="session-bound canonical activity",
        receipt_id="RCP-SES",
        next_action="continue test",
        successor="NEXT-EXECUTION-20260916-SES-NEXT.md",
        evidence=["receipt:test"],
        session_id=session_id,
    )
    import canonical_event_store as CES

    result = CES.create_or_replay(event, EC.EVENTS_ROOT, EC.INDEX_PATH)
    assert result["status"] in {"CREATED", "REPLAY"}
    return event_id


def session_path(session_id):
    return EC.SESSIONS_ROOT / f"{session_id}.json"


def state_session_id():
    return EC.load().get("session_id")


def read_session(session_id):
    return json.loads(session_path(session_id).read_text(encoding="utf-8"))


def write_session(session):
    session_path(session["session_id"]).write_text(
        json.dumps(session, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


class TestSessionClosure(unittest.TestCase):
    def setUp(self):
        self.authority, self.gate, self.decision, self.action, self.credential = setup()

    # 1. CLAIMED opens a real, durable Session envelope.
    def test_001_claim_opens_real_session(self):
        start_claimed()
        session_id = state_session_id()
        self.assertIsNotNone(session_id)
        self.assertRegex(session_id, r"^NAYA-[0-9]{8}-[0-9]{6}-[0-9A-F]{4}$")
        session = read_session(session_id)
        self.assertEqual(session["status"], "OPEN")
        self.assertEqual(session["actor"]["actor_id"], ACTOR_ID)
        self.assertEqual(session["execution"]["claim_id"], CLAIM_ID)
        self.assertEqual(session["execution"]["run_id"], EC.load()["run_id"])
        self.assertEqual(session["project"]["head_before"], "test-head")
        parsed = datetime.fromisoformat(session["entered_at"].replace("Z", "+00:00"))
        self.assertIsNotNone(parsed)
        index = json.loads(EC.SESSIONS_INDEX_PATH.read_text(encoding="utf-8"))
        self.assertEqual(index["session_count"], 1)
        self.assertEqual(index["sessions"][0]["session_id"], session_id)
        self.assertEqual(index["sessions"][0]["status"], "OPEN")

    # 2. EXECUTING records the approved preflight on the Session.
    def test_002_executing_records_preflight_on_session(self):
        _, gate, decision, action, credential = setup()
        walk_to_observed(credential, gate, decision, action)
        session = read_session(state_session_id())
        self.assertEqual(session["preflight_verdict"], "APPROVED")
        self.assertIsNotNone(session["preflight"])
        self.assertEqual(session["execution"]["action_id"], ACTION_ID)

    # 3. VERIFIED auto-emits an Activity bound to that Session.
    def test_003_verified_binds_activity_to_session(self):
        _, gate, decision, action, credential = setup()
        walk_to_observed(credential, gate, decision, action)
        session_id = state_session_id()
        EC.transition(
            "VERIFIED",
            evidence=["receipt:test"],
            verification={"status": "VERIFIED", "method": "test"},
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-SES-NEXT.md",
        )
        event_id = EC.load()["activity_event_id"]
        event = find_event(event_id, events_root=EC.EVENTS_ROOT, index_path=EC.INDEX_PATH)
        self.assertIsNotNone(event)
        self.assertEqual(event["execution"]["session_id"], session_id)
        session = read_session(session_id)
        bound_ids = [item["activity_event_id"] for item in session["actions"]]
        self.assertIn(event_id, bound_ids)

    # 4. HANDED_OFF closes the Session completely and validate() is GREEN.
    def test_004_handed_off_closes_session(self):
        _, gate, decision, action, credential = setup()
        complete(credential, gate, decision, action)
        session_id = state_session_id()
        session = read_session(session_id)
        self.assertEqual(session["status"], "COMPLETED")
        self.assertIsNotNone(session["exited_at"])
        self.assertIsNotNone(session["project"]["head_after"])
        self.assertEqual(session["evidence"], ["receipt:test"])
        self.assertEqual(session["next_action"], "continue test")
        self.assertEqual(session["successor"], "NEXT-EXECUTION-20260916-SES-NEXT.md")
        self.assertEqual(session["handoff"]["successor"], "NEXT-EXECUTION-20260916-SES-NEXT.md")
        self.assertEqual(EC.validate()["execution_status"], "HANDED_OFF")

    # 5. Suppressing the Session record is an integrity failure.
    def test_005_session_suppression_detected(self):
        _, gate, decision, action, credential = setup()
        complete(credential, gate, decision, action)
        EC.validate()
        session_id = state_session_id()
        path = session_path(session_id)
        self.assertTrue(path.exists())
        path.unlink()
        with self.assertRaises(AssertionError) as ctx:
            EC.validate()
        self.assertIn("session integrity failure", str(ctx.exception))
        self.assertIn("no real Session record", str(ctx.exception))

    # 6. Rewriting the Session to another execution is an integrity failure.
    def test_006_session_unbound_run_refused(self):
        _, gate, decision, action, credential = setup()
        complete(credential, gate, decision, action)
        session = read_session(state_session_id())
        session["execution"]["run_id"] = "RUN-UNRELATED"
        write_session(session)
        with self.assertRaises(AssertionError) as ctx:
            EC.validate()
        self.assertIn("session integrity failure", str(ctx.exception))
        self.assertIn("not bound to this execution run", str(ctx.exception))

    # 7. Reopening a closed Session is an integrity failure.
    def test_007_reopened_session_refused(self):
        _, gate, decision, action, credential = setup()
        complete(credential, gate, decision, action)
        session = read_session(state_session_id())
        session["status"] = "OPEN"
        session["exited_at"] = None
        write_session(session)
        with self.assertRaises(AssertionError) as ctx:
            EC.validate()
        self.assertIn("no COMPLETED Session record", str(ctx.exception))

    # 8. An Activity that is not bound to its Session is refused at VERIFIED.
    def test_008_activity_without_session_bound_refused(self):
        _, gate, decision, action, credential = setup()
        walk_to_observed(credential, gate, decision, action)
        unbound_id = persist_scene_event(None)
        with self.assertRaises(AssertionError) as ctx:
            EC.transition(
                "VERIFIED",
                activity_event_id=unbound_id,
                evidence=["receipt:test"],
                verification={"status": "VERIFIED", "method": "test"},
            )
        self.assertIn("not bound to this execution session", str(ctx.exception))
        self.assertEqual(EC.load()["status"], "OBSERVED")

    # 9. Pre-contract executions with no Session still complete (legacy-compatible).
    def test_009_sessionless_execution_still_completes(self):
        if EC.STATE.exists():
            EC.STATE.unlink()
        EC.STATE.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "status": "CLAIMED",
                    "claim_id": "CL-LEGACY",
                    "block_id": "B-LEGACY",
                    "owner": "anyone",
                    "scope": ["legacy"],
                    "start_head": "test-head",
                    "history": [],
                }
            ),
            encoding="utf-8",
        )
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
        self.assertTrue(issued.allowed)
        EC.transition(
            "EXECUTING",
            action=action,
            execution_authorization=issued.authorization,
            gate=gate,
            preflight=approved_preflight(),
        )
        EC.transition("OBSERVED", observation="actual runtime observation")
        legacy_event = persist_scene_event(None, claim_id="CL-LEGACY")
        EC.transition(
            "VERIFIED",
            activity_event_id=legacy_event,
            evidence=["receipt:test"],
            verification={"status": "VERIFIED", "method": "test"},
        )
        self.assertIsNone(EC.load().get("session_id"))
        EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        self.assertEqual(EC.validate()["execution_status"], "HANDED_OFF")

    # 10. Mutable-session operations refuse once closed (no double close).
    def test_010_closed_session_rejects_further_mutation(self):
        _, gate, decision, action, credential = setup()
        complete(credential, gate, decision, action)
        session_id = state_session_id()
        with self.assertRaises(AssertionError) as ctx:
            naya_session.close_session(
                session_id,
                evidence=["receipt:test"],
                next_action="again",
                successor="NEXT.md",
                sessions_root=EC.SESSIONS_ROOT,
                index_path=EC.SESSIONS_INDEX_PATH,
            )
        self.assertIn("not OPEN", str(ctx.exception))
        with self.assertRaises(AssertionError) as ctx:
            naya_session.bind_activity(
                session_id,
                "SE-20260916-193500-late-activity",
                sessions_root=EC.SESSIONS_ROOT,
            )
        self.assertIn("not OPEN", str(ctx.exception))


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSessionClosure)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    print(f"SESSION_CLOSURE_TESTS={'GREEN' if result.wasSuccessful() else 'RED'} count={result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
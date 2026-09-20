#!/usr/bin/env python3
"""P0-01 automatic Activity-event emission closure tests (NAYA POWER TEST #P0-01A).

The VERIFIED boundary must create the canonical Activity event itself -- the
runtime, not the calling Naya, produces the durable receipt that completion
depends on.

Proofs:
  A  POSITIVE automatic emission at the boundary (event exists BECAUSE execution
     happened; bound, durable, receipted, feed-projected; only then VERIFIED).
  A2 boundary cannot complete without successor metadata; nothing is emitted.
  B  persistence failure / CONFLICT => FAIL-CLOSED: VERIFIED refused, execution
     stays OBSERVED, no completion claim.
  C  idempotency: a retry/resume of the SAME run reuses its one event
     (REPLAY_EVENT); a NEW run of the same claim/action gets its own event and
     never reuses the stale previous-run record.
  D  tamper after acceptance: deletion, receipt removal, and run re-binding are
     all detected by validate() (integrity preserved, no regression).

Safe: EXECUTION-STATE and canonical events root redirected to temp dirs.
Run:   python tests/test_activity_event_auto_emission.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]

GATE_PATH = ROOT / ".naya" / "runtime" / "universal_execution_gate.py"
EC_PATH = ROOT / ".naya" / "runtime" / "execution_controller.py"

sys.path.insert(0, str(ROOT / ".naya" / "runtime"))

_gate_spec = importlib.util.spec_from_file_location("p001a_universal_execution_gate", GATE_PATH)
assert _gate_spec and _gate_spec.loader
GATE = importlib.util.module_from_spec(_gate_spec)
sys.modules[GATE.__name__] = GATE
_gate_spec.loader.exec_module(GATE)

_ec_spec = importlib.util.spec_from_file_location("execution_controller", EC_PATH)
assert _ec_spec and _ec_spec.loader
EC = importlib.util.module_from_spec(_ec_spec)
sys.modules["execution_controller"] = EC
_ec_spec.loader.exec_module(EC)

import activity_event as AE  # noqa: E402
from execution_preflight_gate import approved_preflight  # noqa: E402

_TMP = Path(tempfile.mkdtemp(prefix="p001a-"))
EC.STATE = _TMP / "EXECUTION-STATE.json"
EC.EVENTS_ROOT = _TMP / "events"
EC.INDEX_PATH = EC.EVENTS_ROOT / "INDEX.json"
EC.SESSIONS_ROOT = _TMP / "sessions"
EC.SESSIONS_INDEX_PATH = EC.SESSIONS_ROOT / "INDEX.json"

CLAIM_ID = "CL-AUTO"
ACTION_ID = "AUTO-ACT-001"
DECISION_ID = "AUTO-DEC-001"
AUTHORITY_ID = "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE"
ACTOR_ID = "SoulSchoolAcademy"

EMISSION_ARGS = {
    "claim_id": CLAIM_ID,
    "action_id": ACTION_ID,
    "decision_id": DECISION_ID,
    "authority_id": AUTHORITY_ID,
    "actor_id": ACTOR_ID,
    "subject": "P0-01 automatic emission",
    "summary": "auto-emission closure event",
    "receipt_id": f"RCP-{CLAIM_ID}",
    "next_action": "continue test",
    "successor": "NEXT-EXECUTION-20260916-P001A-NEXT.md",
    "evidence": ["receipt:test"],
}


def start_claimed():
    if EC.STATE.exists():
        EC.STATE.unlink()
    EC.transition(
        "CLAIMED",
        claim_id=CLAIM_ID,
        block_id="B-P001A",
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


def auto_verify(**extra):
    return EC.transition(
        "VERIFIED",
        evidence=["receipt:test"],
        verification={"status": "VERIFIED", "method": "test"},
        **extra,
    )


def bound_events(run_id):
    events = []
    for candidate in EC.EVENTS_ROOT.rglob("SE-*.json"):
        body = json.loads(candidate.read_text(encoding="utf-8"))
        execution = body.get("execution") or {}
        if (
            execution.get("claim_id") == CLAIM_ID
            and execution.get("action_id") == ACTION_ID
            and execution.get("run_id") == run_id
        ):
            events.append(body)
    return events


def event_path(event_id):
    matches = list(EC.EVENTS_ROOT.rglob(f"{event_id}.json"))
    return matches[0] if matches else None


class TestAutomaticActivityEmission(unittest.TestCase):
    def setUp(self):
        self.authority, self.gate, self.decision, self.action, self.credential = setup()
        self.state = walk_to_observed(self.credential, self.gate, self.authority, self.decision, self.action)
        self.run_id = self.state["run_id"]
        self.assertEqual(self.state["status"], "OBSERVED")

    def test_a_positive_automatic_emission_at_boundary(self):
        result = auto_verify(
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-P001A-NEXT.md",
        )
        self.assertEqual(result["status"], "VERIFIED")
        self.assertTrue(result.get("activity_event_id"))
        self.assertEqual(result.get("activity_event_emitted"), "CREATED")
        self.assertEqual(result["run_id"], self.run_id)
        events = bound_events(self.run_id)
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event["event_id"], result["activity_event_id"])
        execution = event["execution"]
        self.assertEqual(execution["claim_id"], CLAIM_ID)
        self.assertEqual(execution["action_id"], ACTION_ID)
        self.assertEqual(execution["run_id"], self.run_id)
        self.assertEqual(event["receipt"]["receipt_id"], f"RCP-{CLAIM_ID}")
        self.assertEqual(event["receipt"]["event_id"], event["event_id"])
        self.assertEqual(event["continuity"]["execution_state"], "COMPLETED")
        self.assertTrue(event["continuity"]["handoff"]["next_action"])
        self.assertTrue(event["continuity"]["handoff"]["successor"])
        self.assertEqual(event["activity_feed_projection"]["feed"], "NAYA-ACTIVITY")
        measurement = event.get("compounding_measurement") or {}
        self.assertEqual(measurement.get("schema"), "naya-power-compounding-measurement/v1")
        self.assertEqual(measurement.get("status"), "VERIFIED_CAPTURED")
        self.assertEqual(measurement.get("activity_event_id"), event["event_id"])
        self.assertEqual(measurement.get("verified_state_change", {}).get("verification_status"), "VERIFIED")
        self.assertFalse(measurement.get("promotion", {}).get("compounded"))
        index = json.loads(EC.INDEX_PATH.read_text(encoding="utf-8"))
        self.assertIn(event["event_id"], [row.get("event_id") for row in index.get("events", [])])
        EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        self.assertEqual(EC.validate()["execution_status"], "HANDED_OFF")

    def test_a2_boundary_requires_successor_metadata(self):
        with self.assertRaises(AssertionError) as ctx:
            auto_verify()
        self.assertIn("next_action", str(ctx.exception))
        self.assertEqual(EC.load()["status"], "OBSERVED")
        self.assertEqual(bound_events(self.run_id), [])

    def test_b_persistence_failure_fails_closed(self):
        with mock.patch.object(AE, "persist_activity_event", side_effect=RuntimeError("simulated disk failure")):
            with self.assertRaises(AssertionError) as ctx:
                auto_verify(
                    next_action="continue test",
                    successor="NEXT-EXECUTION-20260916-P001A-NEXT.md",
                )
        self.assertIn("could not auto-persist the canonical Activity Feed event", str(ctx.exception))
        self.assertIn("NO EVENT = INCOMPLETE EXECUTION RECORD", str(ctx.exception))
        self.assertEqual(EC.load()["status"], "OBSERVED")
        self.assertEqual(bound_events(self.run_id), [])

    def test_b_persistence_conflict_fails_closed(self):
        conflict = {"status": "CONFLICT", "event_id": "SE-x", "path": "x", "idempotency_key": "k", "fingerprint": "f"}
        with mock.patch.object(AE, "persist_activity_event", return_value=conflict):
            with self.assertRaises(AssertionError) as ctx:
                auto_verify(
                    next_action="continue test",
                    successor="NEXT-EXECUTION-20260916-P001A-NEXT.md",
                )
        self.assertIn("conflicting existing canonical Activity event", str(ctx.exception))
        self.assertEqual(EC.load()["status"], "OBSERVED")

    def test_c_idempotent_reuse_single_event(self):
        result = auto_verify(
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-P001A-NEXT.md",
        )
        replay = AE.ensure_activity_event(
            events_root=EC.EVENTS_ROOT,
            index_path=EC.INDEX_PATH,
            run_id=self.run_id,
            **EMISSION_ARGS,
        )
        self.assertEqual(replay["status"], "REPLAY_EVENT")
        self.assertEqual(replay["event_id"], result["activity_event_id"])
        self.assertEqual(len(bound_events(self.run_id)), 1)

    def test_c_crash_resume_no_duplicate(self):
        pre_emitted = AE.ensure_activity_event(
            events_root=EC.EVENTS_ROOT,
            index_path=EC.INDEX_PATH,
            run_id=self.run_id,
            session_id=EC.load().get("session_id"),
            **EMISSION_ARGS,
        )
        self.assertEqual(pre_emitted["status"], "CREATED")
        result = auto_verify(
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-P001A-NEXT.md",
        )
        self.assertEqual(result.get("activity_event_emitted"), "REPLAY_EVENT")
        self.assertEqual(result["activity_event_id"], pre_emitted["event_id"])
        self.assertEqual(len(bound_events(self.run_id)), 1)

    def test_c_stale_previous_run_never_reused(self):
        result_run1 = auto_verify(
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-P001A-NEXT.md",
        )
        EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        run1_id = self.run_id
        run1_event_id = result_run1["activity_event_id"]
        self.authority, self.gate, self.decision, self.action, self.credential = setup()
        self.state = walk_to_observed(self.credential, self.gate, self.authority, self.decision, self.action)
        self.assertNotEqual(self.state["run_id"], run1_id)
        result_run2 = auto_verify(
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-P001A-NEXT.md",
        )
        self.assertEqual(result_run2.get("activity_event_emitted"), "CREATED")
        self.assertNotEqual(result_run2["activity_event_id"], run1_event_id)
        self.assertEqual(len(bound_events(run1_id)), 1)
        self.assertEqual(len(bound_events(self.state["run_id"])), 1)
        self.assertEqual(event_path(run1_event_id).exists(), True)

    def test_d_tamper_receipt_detected(self):
        auto_verify(
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-P001A-NEXT.md",
        )
        EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        EC.validate()
        event_id = EC.load()["activity_event_id"]
        path = event_path(event_id)
        event = json.loads(path.read_text(encoding="utf-8"))
        event.pop("receipt")
        path.write_text(json.dumps(event, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        with self.assertRaises(AssertionError) as ctx:
            EC.validate()
        self.assertIn("activity event integrity failure", str(ctx.exception))

    def test_d_delete_after_acceptance_detected(self):
        auto_verify(
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-P001A-NEXT.md",
        )
        EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        EC.validate()
        event_id = EC.load()["activity_event_id"]
        path = event_path(event_id)
        path.unlink()
        rows = json.loads(EC.INDEX_PATH.read_text(encoding="utf-8")).get("events", [])
        filtered = [row for row in rows if row.get("event_id") != event_id]
        index = json.loads(EC.INDEX_PATH.read_text(encoding="utf-8"))
        index["events"] = filtered
        index["event_count"] = len(filtered)
        EC.INDEX_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        with self.assertRaises(AssertionError) as ctx:
            EC.validate()
        message = str(ctx.exception)
        self.assertIn("activity event integrity failure", message)
        self.assertIn("no canonical Activity Feed event found", message)

    def test_d_run_rebinding_detected(self):
        auto_verify(
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-P001A-NEXT.md",
        )
        EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        EC.validate()
        event_id = EC.load()["activity_event_id"]
        path = event_path(event_id)
        event = json.loads(path.read_text(encoding="utf-8"))
        event["execution"]["run_id"] = "RUN-SOMEOTHER-000000000000"
        path.write_text(json.dumps(event, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        with self.assertRaises(AssertionError) as ctx:
            EC.validate()
        self.assertIn("not bound to this execution run", str(ctx.exception))


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAutomaticActivityEmission)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    print(f"ACTIVITY_AUTO_EMISSION_CLOSURE_TESTS={'GREEN' if result.wasSuccessful() else 'RED'} count={result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
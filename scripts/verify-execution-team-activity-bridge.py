#!/usr/bin/env python3
"""End-to-end proof: real execution-controller lifecycle -> Team Naya Activity."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".naya" / "runtime"
sys.path.insert(0, str(RUNTIME))

import execution_controller as ec  # noqa: E402
from execution_preflight_gate import approved_preflight  # noqa: E402
from universal_execution_gate import DecisionObject, Epistemic, Risk, UniversalExecutionGate, VerificationPlan, load_registry  # noqa: E402


def main() -> int:
    original = ec.STATE.read_text(encoding="utf-8") if ec.STATE.exists() else None
    tmp = Path(tempfile.mkdtemp(prefix="naya-execution-team-bridge-"))
    saved = (ec.EVENTS_ROOT, ec.INDEX_PATH, ec.SESSIONS_ROOT, ec.SESSIONS_INDEX_PATH)
    import execution_activity_writer as activity_writer
    saved_activity_root = activity_writer.ACTIVITY_ROOT
    events_root = tmp / "events"
    ec.EVENTS_ROOT = events_root
    ec.INDEX_PATH = events_root / "INDEX.json"
    ec.SESSIONS_ROOT = tmp / "sessions"
    ec.SESSIONS_INDEX_PATH = ec.SESSIONS_ROOT / "INDEX.json"
    activity_writer.ACTIVITY_ROOT = tmp / "activity"
    try:
        if ec.STATE.exists():
            ec.STATE.unlink()

        claim_id = "CL-TEAM-BRIDGE-001"
        run_id = "RUN-TEAM-BRIDGE-001"
        ec.transition("CLAIMED", claim_id=claim_id, run_id=run_id, block_id="B-TEAM-BRIDGE", owner="Naya-Team-Bridge-Test", scope=["team/activity/bridge"], start_head="test-head", restored_context="Team Naya communication proof is already GREEN.")

        registry = load_registry()
        authority = registry.resolve("HUMAN-SOULSCHOOLACADEMY-REPO-WRITE")
        gate = UniversalExecutionGate(registry)
        decision = DecisionObject(decision_id="DEC-TEAM-BRIDGE-001", mission="Prove governed execution automatically reaches Team Naya Activity.", actor_id=authority.principal_id, action="repo_write", purpose=authority.purpose, scope=authority.scope, current_truth="execution lifecycle is governed and canonical Activity already exists", gap="Team communication must receive the real execution completion automatically", evidence=("evidence:execution-controller", "evidence:team-activity-facade"), epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}), consequence="bounded repository test execution", reversible=True, risk=Risk(uncertainty=1, consequence=1, irreversibility=1), alternatives=("do_not_execute",), expected_value="verified execution-to-team communication", required_permission="repo_write", verification=VerificationPlan("Team Naya Activity event", "NAYA_VERIFIED event exists and binds to execution", ("stop",)), necessary_power=frozenset({"repo_write"}), requested_power=frozenset({"repo_write"}))
        action = {"action_id": "ACT-TEAM-BRIDGE-001", "action_type": "repository_write", "target": "team/activity/bridge-test", "purpose": authority.purpose, "authority_id": authority.authority_id, "decision_id": decision.decision_id, "actor_id": decision.actor_id, "scope": decision.scope, "permission": decision.action}
        issued = gate.authorize(authority=authority, decision=decision, action=action)
        assert issued.allowed

        ec.transition("EXECUTING", action=action, execution_authorization=issued.authorization, gate=gate, preflight=approved_preflight())
        ec.transition("OBSERVED", observation="real execution-controller transition reached OBSERVED")
        next_action = "Next Naya retrieves the verified execution from Team Naya Activity and continues."
        successor = "NEXT-NAYA-EXECUTION-FROM-TEAM-ACTIVITY"
        ec.transition("VERIFIED", evidence=["receipt:team-bridge-e2e", "test:execution-controller"], verification={"status": "VERIFIED", "method": "execution-to-team-activity-e2e"}, next_action=next_action, successor=successor)

        state = ec.load()
        assert state["status"] == "VERIFIED"
        assert state.get("activity_event_id")

        team_events = []
        for candidate in events_root.rglob("SE-*.json"):
            body = json.loads(candidate.read_text(encoding="utf-8"))
            if body.get("event_type") == "team-communication":
                team_events.append(body)

        verified = [event for event in team_events if (event.get("team") or {}).get("intent") == "NAYA_VERIFIED"]
        assert verified, "NO TEAM ACTIVITY EVENT: execution did not reach the Team Naya facade"
        bridge = verified[-1]
        assert state["activity_event_id"] in bridge.get("evidence_ids", [])
        assert bridge["team"]["recipients"] == ["TEAM-NAYA"]
        assert bridge["continuity"]["next_action"] == next_action
        assert bridge["continuity"]["successor"] == successor

        # Hard-handoff proof: remove the human-readable durable day projection.
        # The canonical event still exists, but HANDED_OFF must refuse to close.
        daily = activity_writer.find_daily_activity(state["activity_event_id"])
        assert daily is not None
        daily.unlink()
        try:
            ec.transition("HANDED_OFF", next_action=next_action, handoff={"current_state": "VERIFIED"})
        except AssertionError as exc:
            assert "NO DAILY RECORD = NO HANDOFF" in str(exc)
        else:
            raise AssertionError("HANDED_OFF accepted missing durable Team Naya day Activity")
        activity_writer.write_execution_activity(
            event=__import__("activity_event").find_event(state["activity_event_id"], events_root=events_root, index_path=ec.INDEX_PATH),
            execution={**action, "claim_id": claim_id, "run_id": run_id, "session_id": state["session_id"], "governance_state": "AUTHORIZED", "authorization_verified": True},
            next_action=next_action,
            successor=successor,
            evidence=["receipt:team-bridge-e2e", "test:hard-handoff"],
        )
        ec.transition("HANDED_OFF", next_action=next_action, handoff={"current_state": "VERIFIED"})
        assert ec.load()["status"] == "HANDED_OFF"

        before = len(team_events)
        from activity_event import ensure_activity_event
        replay = ensure_activity_event(claim_id=claim_id, action_id=action["action_id"], decision_id=action["decision_id"], authority_id=action["authority_id"], actor_id=action["actor_id"], subject="VERIFIED completion — replay", summary="replay must reuse the canonical execution Activity event", receipt_id=f"RCP-{claim_id}", next_action=next_action, successor=successor, evidence=["receipt:team-bridge-e2e"], run_id=run_id, session_id=state.get("session_id"), events_root=events_root, index_path=ec.INDEX_PATH)
        assert replay["status"] == "REPLAY_EVENT"
        after = [json.loads(candidate.read_text(encoding="utf-8")) for candidate in events_root.rglob("SE-*.json") if json.loads(candidate.read_text(encoding="utf-8")).get("event_type") == "team-communication"]
        assert len(after) == before, "REPLAY created duplicate Team Naya Activity communication"

        print("EXECUTION_CONTROLLER=PASS")
        print("EXECUTION_TO_TEAM_ACTIVITY=PASS")
        print("TEAM_ACTIVITY_EVIDENCE_BINDING=PASS")
        print("TEAM_ACTIVITY_HANDOFF=PASS")
        print("TEAM_ACTIVITY_IDEMPOTENCY=PASS")
        print("HARD_HANDOFF_ACTIVITY_GATE=PASS")
        print(f"EXECUTION_ACTIVITY_EVENT_ID={state['activity_event_id']}")
        print(f"TEAM_NAYA_EVENT_ID={bridge['event_id']}")
        print(f"TEAM_NAYA_SUCCESSOR={bridge['continuity']['successor']}")
        return 0
    finally:
        ec.EVENTS_ROOT, ec.INDEX_PATH, ec.SESSIONS_ROOT, ec.SESSIONS_INDEX_PATH = saved
        activity_writer.ACTIVITY_ROOT = saved_activity_root
        shutil.rmtree(tmp, ignore_errors=True)
        if original is None:
            if ec.STATE.exists():
                ec.STATE.unlink()
        else:
            ec.STATE.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())

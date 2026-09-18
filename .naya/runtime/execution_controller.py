#!/usr/bin/env python3
"""Fail-closed execution state machine for Naya Power consequential actions."""
from __future__ import annotations

import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".naya" / "runtime" / "EXECUTION-STATE.json"
EVENTS_ROOT = ROOT / ".naya" / "memory" / "events"
INDEX_PATH = EVENTS_ROOT / "INDEX.json"
SESSIONS_ROOT = ROOT / ".naya" / "memory" / "sessions"
SESSIONS_INDEX_PATH = SESSIONS_ROOT / "INDEX.json"
VALID_STATES = {"READY", "CLAIMED", "EXECUTING", "OBSERVED", "VERIFIED", "HANDED_OFF"}
TRANSITIONS = {
    "READY": {"CLAIMED"},
    "CLAIMED": {"EXECUTING"},
    "EXECUTING": {"OBSERVED"},
    "OBSERVED": {"VERIFIED"},
    "VERIFIED": {"HANDED_OFF"},
    "HANDED_OFF": set(),
}


def fail(message: str) -> None:
    raise AssertionError(message)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load() -> dict[str, Any]:
    if not STATE.exists():
        return {"schema_version": 1, "status": "READY", "history": []}
    data = json.loads(STATE.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("status") not in VALID_STATES:
        fail("execution state is invalid")
    return data


def save(data: dict[str, Any]) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def require_fields(data: dict[str, Any], fields: tuple[str, ...]) -> None:
    missing = [field for field in fields if data.get(field) in (None, "", [], {})]
    if missing:
        fail("missing required execution fields: " + ", ".join(missing))


def _find_activity_event(event_id: str, events_root=None, index_path=None) -> dict[str, Any] | None:
    root = Path(events_root) if events_root else EVENTS_ROOT
    index = Path(index_path) if index_path else INDEX_PATH
    if index.exists():
        rows: list[dict[str, Any]] = []
        try:
            rows = json.loads(index.read_text(encoding="utf-8")).get("events", [])
        except (json.JSONDecodeError, AttributeError, OSError):
            rows = []
        for row in rows:
            if row.get("event_id") == event_id:
                candidate = root / str(row.get("path", ""))
                if candidate.exists():
                    try:
                        return json.loads(candidate.read_text(encoding="utf-8"))
                    except (json.JSONDecodeError, OSError):
                        return None
    for candidate in root.rglob(f"{event_id}.json"):
        try:
            return json.loads(candidate.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
    return None


def _verify_activity_event(event_id, claim_id, action_id, run_id=None, session_id=None, events_root=None, index_path=None) -> tuple[bool, list[str]]:
    if not event_id:
        return False, ["no canonical Activity Feed event_id was supplied"]
    event = _find_activity_event(event_id, events_root=events_root, index_path=index_path)
    if event is None:
        return False, [f"no canonical Activity Feed event found for {event_id!r}"]
    problems: list[str] = []
    if event.get("event_id") != event_id:
        problems.append("canonical event id does not match the supplied event_id")
    execution = event.get("execution")
    if not isinstance(execution, dict):
        problems.append("canonical event has no execution binding")
    else:
        if claim_id and execution.get("claim_id") != claim_id:
            problems.append("canonical event is not bound to this execution claim")
        if action_id and execution.get("action_id") != action_id:
            problems.append("canonical event is not bound to this execution action")
        if run_id and execution.get("run_id") and execution.get("run_id") != run_id:
            problems.append("canonical event is not bound to this execution run")
        if session_id and execution.get("session_id") != session_id:
            problems.append("canonical event is not bound to this execution session")
    receipt = event.get("receipt")
    if not isinstance(receipt, dict):
        problems.append("canonical event is missing the required durable receipt block")
    else:
        if not receipt.get("receipt_id") or not receipt.get("schema"):
            problems.append("canonical event receipt is incomplete")
        if receipt.get("event_id") != event_id:
            problems.append("canonical event receipt is not bound to the same event")
    continuity = event.get("continuity")
    if not isinstance(continuity, dict) or continuity.get("execution_state") != "COMPLETED":
        problems.append("canonical event does not mark this execution COMPLETED")
    else:
        handoff = continuity.get("handoff")
        if not isinstance(handoff, dict) or not handoff.get("next_action") or not handoff.get("successor"):
            problems.append("canonical event is missing the required successor handoff")
    projection = event.get("activity_feed_projection")
    if not isinstance(projection, dict) or not projection.get("feed") or not projection.get("event_id"):
        problems.append("canonical event is not projected to the Activity Feed")
    return (not problems), problems


def transition(target: str, **fields: Any) -> dict[str, Any]:
    # Transient boundary inputs: never persisted, never treated as authority
    # outside the credential check below.
    gate = fields.pop("gate", None)
    credential = fields.pop("execution_authorization", None)

    if target == "EXECUTING":
        # The Universal Execution Gate is the ONLY authorization source. The
        # controller does not accept caller-supplied authorization strings,
        # model/agent approval, claims, or receipts; a gate-issued
        # ExecutionAuthorization bound to THIS action is mandatory and
        # re-validated against the registry at time of use.
        if credential is None:
            fail("execution boundary refused: EXECUTING requires a gate-issued ExecutionAuthorization")
        if gate is None:
            from universal_execution_gate import UniversalExecutionGate

            gate = UniversalExecutionGate.from_canonical()
        valid, reasons = gate.verify(credential)
        if not valid:
            fail("execution boundary refused: " + "; ".join(reasons))
        action = fields.get("action")
        if not isinstance(action, dict):
            fail("execution boundary refused: EXECUTING requires an action binding")
        if action.get("action_id") != credential.action_id:
            fail("action_id does not match execution authorization")
        if action.get("authority_id") != credential.authority_id:
            fail("authority_id does not match execution authorization")
        if action.get("decision_id") != credential.decision_id:
            fail("decision_id does not match execution authorization")
        if action.get("actor_id") != credential.actor_id:
            fail("actor_id does not match execution authorization")
        if action.get("scope") != credential.scope:
            fail("scope does not match execution authorization")
        if action.get("permission") != credential.permission:
            fail("permission does not match execution authorization")
        if credential.governance_state != "AUTHORIZED":
            fail("execution authorization governance_state is not AUTHORIZED")
        # Machine-enforced preflight gate (STEP 2): consequential execution
        # requires an approved 10-question preflight object with classified
        # authority/state/protected boundaries. Missing, unknown-authority,
        # conflicted, human-authority, and invalid baselines are refused.
        from execution_preflight_gate import gate_preflight

        preflight_verdict = gate_preflight(fields.get("preflight"))
        if preflight_verdict["status"] != "APPROVED":
            fail(
                "execution boundary refused: EXECUTING requires an approved preflight gate: "
                + "; ".join(preflight_verdict["reasons"])
            )

    data = load()
    current = data["status"]
    if target not in TRANSITIONS[current]:
        fail(f"invalid execution transition: {current} -> {target}")
    if target == "CLAIMED":
        require_fields(fields, ("claim_id", "block_id", "owner", "scope", "start_head"))
        if not fields.get("run_id"):
            fields["run_id"] = "RUN-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        # Real Naya Session records (Priority 1): an execution claim opens a
        # Session envelope immediately and durably. Activities produced by this
        # execution are bound to that Session, and HANDED_OFF closes it.
        from naya_session import open_session

        try:
            opened = open_session(
                claim_id=fields["claim_id"],
                run_id=fields["run_id"],
                owner=fields["owner"],
                scope=fields.get("scope"),
                start_head=fields["start_head"],
                block_id=fields.get("block_id"),
                restored_context=fields.get("restored_context"),
                sessions_root=SESSIONS_ROOT,
                index_path=SESSIONS_INDEX_PATH,
            )
        except Exception as exc:
            fail("execution boundary refused: CLAIMED requires a real Session record: " + str(exc))
        fields["session_id"] = opened["session_id"]
        fields["session_started_at"] = opened["session"].get("entered_at")
    elif target == "EXECUTING":
        require_fields(data, ("claim_id", "block_id", "owner", "scope", "start_head"))
    elif target == "OBSERVED":
        require_fields(fields, ("observation",))
    elif target == "VERIFIED":
        require_fields(fields, ("evidence", "verification"))
        action_ctx = data.get("action") or {}
        claim_id = data.get("claim_id")
        action_id = action_ctx.get("action_id")
        run_id = data.get("run_id")
        supplied = fields.get("activity_event_id")
        if not supplied:
            # Automatic canonical Activity-event emission at the completion
            # boundary (P0-01): the runtime -- not the calling Naya -- produces
            # the durable Activity receipt that VERIFIED acceptance depends on.
            from activity_event import ensure_activity_event

            require_fields(fields, ("next_action", "successor"))
            emitted_evidence = fields.get("evidence")
            if not isinstance(emitted_evidence, list):
                emitted_evidence = [str(emitted_evidence)]
            try:
                emitted = ensure_activity_event(
                    claim_id=claim_id,
                    action_id=action_id,
                    decision_id=action_ctx.get("decision_id"),
                    authority_id=action_ctx.get("authority_id"),
                    actor_id=action_ctx.get("actor_id"),
                    subject=f"VERIFIED completion — {action_id or claim_id}",
                    summary=f"governed execution {claim_id} completed VERIFIED with a durable Activity receipt auto-emitted at the execution boundary",
                    receipt_id=f"RCP-{claim_id}",
                    next_action=fields.get("next_action"),
                    successor=fields.get("successor"),
                    evidence=emitted_evidence,
                    run_id=run_id,
                    session_id=data.get("session_id"),
                    events_root=EVENTS_ROOT,
                    index_path=INDEX_PATH,
                )
            except Exception as exc:
                fail(
                    "execution boundary refused: VERIFIED could not auto-persist the canonical "
                    "Activity Feed event (NO EVENT = INCOMPLETE EXECUTION RECORD): " + str(exc)
                )
            supplied = emitted["event_id"]
            fields["activity_event_id"] = supplied
            fields["activity_event_emitted"] = emitted.get("status")
        ok, activity_problems = _verify_activity_event(supplied, claim_id, action_id, run_id, data.get("session_id"))
        if not ok:
            fail(
                "execution boundary refused: VERIFIED requires a canonical Activity Feed event "
                "(NO EVENT = INCOMPLETE EXECUTION RECORD): " + "; ".join(activity_problems)
            )
        if data.get("session_id"):
            from naya_session import bind_activity

            try:
                bind_activity(
                    data["session_id"],
                    supplied,
                    action_id or None,
                    sessions_root=SESSIONS_ROOT,
                )
            except Exception as exc:
                fail("execution boundary refused: VERIFIED could not bind the Activity to its Session: " + str(exc))
    elif target == "HANDED_OFF":
        require_fields(fields, ("next_action", "handoff"))
    event = {"at": now(), "from": current, "to": target, **fields}
    data.update(fields)
    if target == "EXECUTING" and data.get("session_id"):
        from naya_session import record_preflight

        try:
            record_preflight(
                data["session_id"],
                fields.get("preflight"),
                "APPROVED",
                action_id=(data.get("action") or {}).get("action_id"),
                sessions_root=SESSIONS_ROOT,
            )
        except Exception as exc:
            fail("execution boundary refused: EXECUTING could not record the preflight on its Session: " + str(exc))
    elif target == "HANDED_OFF" and data.get("session_id"):
        from naya_session import close_session

        successor = fields.get("successor") or data.get("successor")
        if not successor:
            completed = _find_activity_event(data.get("activity_event_id"), EVENTS_ROOT, INDEX_PATH)
            handoff = (completed.get("continuity") or {}).get("handoff") or {}
            successor = handoff.get("successor")
        try:
            closed = close_session(
                data["session_id"],
                evidence=data.get("evidence") or (fields.get("evidence") or []),
                results=[{"handoff": fields.get("handoff")}],
                next_action=fields["next_action"],
                successor=successor,
                sessions_root=SESSIONS_ROOT,
                index_path=SESSIONS_INDEX_PATH,
            )
        except Exception as exc:
            fail("execution boundary refused: HANDED_OFF could not close the Session record: " + str(exc))
        else:
            fields["session_closed_at"] = closed["session"].get("exited_at")
            event["session_closed_at"] = fields["session_closed_at"]
    data["status"] = target
    data.setdefault("history", []).append(event)
    save(data)
    return data


def validate(data: dict[str, Any] | None = None) -> dict[str, Any]:
    data = data or load()
    status = data.get("status")
    if status not in VALID_STATES:
        fail("invalid execution status")
    if status in {"CLAIMED", "EXECUTING", "OBSERVED", "VERIFIED", "HANDED_OFF"}:
        require_fields(data, ("claim_id", "block_id", "owner", "scope", "start_head"))
    if status in {"OBSERVED", "VERIFIED", "HANDED_OFF"}:
        require_fields(data, ("observation",))
    if status in {"VERIFIED", "HANDED_OFF"}:
        require_fields(data, ("evidence", "verification", "activity_event_id"))
        action_ctx = data.get("action") or {}
        ok, activity_problems = _verify_activity_event(
            data.get("activity_event_id"), data.get("claim_id"), action_ctx.get("action_id"), data.get("run_id"), data.get("session_id")
        )
        if not ok:
            fail(
                "activity event integrity failure — completed execution has no durable "
                "canonical Activity Feed event (suppression suspected): " + "; ".join(activity_problems)
            )
        if data.get("session_id"):
            from naya_session import load_session, session_integrity

            session = load_session(data["session_id"], sessions_root=SESSIONS_ROOT)
            if session is None:
                fail(
                    "session integrity failure — executed record has no real Session "
                    "record (suppression suspected)"
                )
            ok, session_problems = session_integrity(
                session,
                expected_claim_id=data.get("claim_id"),
                expected_run_id=data.get("run_id"),
                need_closed=(status == "HANDED_OFF"),
            )
            if not ok:
                fail(
                    "session integrity failure — Session record does not fully bind this execution: "
                    + "; ".join(session_problems)
                )
    if status == "HANDED_OFF":
        require_fields(data, ("next_action", "handoff"))
    if not isinstance(data.get("history"), list):
        fail("execution history must be a list")
    if status in {"EXECUTING", "OBSERVED", "VERIFIED", "HANDED_OFF"}:
        # EXECUTING (and everything after it) may only be reached through a real
        # transition event; a file tamper that flips status without the gate has
        # no such event and is rejected even though the file parses.
        if not any(event.get("to") == "EXECUTING" for event in data.get("history", [])):
            fail("execution state has no EXECUTING transition event")
    if status in {"EXECUTING", "OBSERVED", "VERIFIED", "HANDED_OFF"}:
        # The preflight that permitted execution must still be present and
        # approved; a tamper that drops or invalidates the preflight of an
        # executed record is a preflight gate integrity failure.
        from execution_preflight_gate import gate_preflight

        preflight_verdict = gate_preflight(data.get("preflight"), context="an executed record")
        if preflight_verdict["status"] != "APPROVED":
            fail(
                "preflight gate integrity failure — executed record has no approved preflight: "
                + "; ".join(preflight_verdict["reasons"])
            )
    return {"status": "GREEN", "execution_status": status, "history_count": len(data["history"])}


def self_test() -> int:
    from universal_execution_gate import (
        DecisionObject,
        Epistemic,
        Risk,
        UniversalExecutionGate,
        VerificationPlan,
        load_registry,
    )

    global EVENTS_ROOT, INDEX_PATH, SESSIONS_ROOT, SESSIONS_INDEX_PATH
    original = STATE.read_text(encoding="utf-8") if STATE.exists() else None
    events_tmp = Path(tempfile.mkdtemp(prefix="ec-selftest-events-"))
    saved_events_root, saved_index_path = EVENTS_ROOT, INDEX_PATH
    saved_sessions_root, saved_sessions_index_path = SESSIONS_ROOT, SESSIONS_INDEX_PATH
    EVENTS_ROOT = events_tmp / "events"
    INDEX_PATH = EVENTS_ROOT / "INDEX.json"
    SESSIONS_ROOT = events_tmp / "sessions"
    SESSIONS_INDEX_PATH = SESSIONS_ROOT / "INDEX.json"
    try:
        if STATE.exists(): STATE.unlink()
        transition("CLAIMED", claim_id="CL-TEST", block_id="B-TEST", owner="Naya-Test", scope=["test/block"], start_head="test-head")
        claimed_state = load()
        assert claimed_state.get("session_id")
        assert SESSIONS_INDEX_PATH.exists()

        # EXECUTING now requires a gate-issued credential bound to this action.
        registry = load_registry()
        authority = registry.resolve("HUMAN-SOULSCHOOLACADEMY-REPO-WRITE")
        gate = UniversalExecutionGate(registry)
        decision = DecisionObject(
            decision_id="EC-SELFTEST-DEC",
            mission="NayaPOWER governed repository maintenance",
            actor_id=authority.principal_id,
            action="repo_write",
            purpose=authority.purpose,
            scope=authority.scope,
            current_truth="repository mutation requested",
            gap="mutation requires canonical governance decision",
            evidence=("evidence:registry-grant",),
            epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}),
            consequence="repository write under bounded governance",
            reversible=True,
            risk=Risk(uncertainty=1, consequence=2, irreversibility=1),
            alternatives=("do_not_execute",),
            expected_value="authorized bounded mutation",
            required_permission="repo_write",
            verification=VerificationPlan("post-write state", "verification passes", ("stop",)),
            necessary_power=frozenset({"repo_write"}),
            requested_power=frozenset({"repo_write"}),
        )
        bound = {
            "action_id": "ACT-EC-SELFTEST-001",
            "action_type": "repository_write",
            "target": "docs/Naya",
            "purpose": authority.purpose,
            "authority_id": authority.authority_id,
            "decision_id": decision.decision_id,
            "actor_id": decision.actor_id,
            "scope": decision.scope,
            "permission": decision.action,
        }
        issued = gate.authorize(authority=authority, decision=decision, action=bound)
        assert issued.allowed
        from execution_preflight_gate import approved_preflight

        transition(
            "EXECUTING",
            action=bound,
            execution_authorization=issued.authorization,
            gate=gate,
            preflight=approved_preflight(),
        )
        transition("OBSERVED", observation="actual runtime observation")
        transition(
            "VERIFIED",
            evidence=["receipt:test"],
            verification={"status": "VERIFIED", "method": "test"},
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-EC-SELFTEST-NEXT.md",
        )
        auto_state = load()
        assert auto_state.get("activity_event_id")
        from activity_event import ensure_activity_event

        re_emit = ensure_activity_event(
            claim_id="CL-TEST",
            action_id=bound["action_id"],
            decision_id=bound["decision_id"],
            authority_id=bound["authority_id"],
            actor_id=bound["actor_id"],
            subject="EC self-test activity gate",
            summary="fail-closed execution self-test completion record",
            receipt_id="RCP-EC-SELFTEST",
            next_action="continue test",
            successor="NEXT-EXECUTION-20260916-EC-SELFTEST-NEXT.md",
            evidence=["receipt:test"],
            run_id=auto_state.get("run_id"),
            events_root=EVENTS_ROOT,
            index_path=INDEX_PATH,
        )
        assert re_emit["status"] == "REPLAY_EVENT"
        assert re_emit["event_id"] == auto_state["activity_event_id"]
        bound_count = 0
        for candidate in EVENTS_ROOT.rglob("SE-*.json"):
            body = json.loads(candidate.read_text(encoding="utf-8"))
            execution = body.get("execution") or {}
            if (
                execution.get("claim_id") == "CL-TEST"
                and execution.get("action_id") == bound["action_id"]
                and execution.get("run_id") == auto_state.get("run_id")
            ):
                bound_count += 1
        assert bound_count == 1
        transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        from naya_session import load_session

        closed_session = load_session(claimed_state["session_id"], sessions_root=SESSIONS_ROOT)
        assert closed_session is not None
        assert closed_session.get("status") == "COMPLETED"
        assert closed_session.get("exited_at")
        assert closed_session.get("next_action") == "continue test"
        result = validate()
        assert result["execution_status"] == "HANDED_OFF"
        try:
            transition("READY")
        except AssertionError:
            pass
        else:
            raise AssertionError("terminal state accepted an invalid transition")
        try:
            # A gate-issued credential without an approved preflight must be
            # refused by the machine-enforced preflight gate.
            transition(
                "EXECUTING",
                action=bound,
                execution_authorization=issued.authorization,
                gate=gate,
            )
        except AssertionError:
            pass
        else:
            raise AssertionError("execution reached EXECUTING without an approved preflight gate")
        print(
            "PASS — fail-closed execution state machine GREEN (EXECUTING is gate-bound; "
            "preflight gate enforced; VERIFIED auto-emits the canonical Activity event; "
            "CLAIMED opens a real Session; HANDED_OFF closes it)"
        )
        return 0
    finally:
        EVENTS_ROOT, INDEX_PATH = saved_events_root, saved_index_path
        SESSIONS_ROOT, SESSIONS_INDEX_PATH = saved_sessions_root, saved_sessions_index_path
        import shutil

        shutil.rmtree(str(events_tmp), ignore_errors=True)
        if original is None:
            if STATE.exists(): STATE.unlink()
        else:
            STATE.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["self-test", "validate"])
    args = parser.parse_args()
    try:
        if args.command == "self-test": raise SystemExit(self_test())
        print(json.dumps(validate(), indent=2))
    except (AssertionError, json.JSONDecodeError) as exc:
        print(f"EXECUTION=RED\nFIRST_DIVERGENCE={exc}")
        raise SystemExit(1)

#!/usr/bin/env python3
"""End-to-end proof: governed execution -> Activity -> Intelligence -> Promotion."""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".naya" / "runtime"
sys.path.insert(0, str(RUNTIME))

import execution_controller as ec
from execution_preflight_gate import approved_preflight
from universal_execution_gate import DecisionObject, Epistemic, Risk, UniversalExecutionGate, VerificationPlan, load_registry


def _write_ci_execution_capture(*, observed_output: str, result: str, commit_sha: str, run_id: str, action: str) -> None:
    github_run_id = os.environ.get("GITHUB_RUN_ID")
    if not github_run_id:
        return
    capture_path = Path(os.environ.get("NAYA_EXECUTION_CAPTURE_PATH", ROOT / "execution-capture.json"))
    capture = {"schema": "naya-power-execution-capture/v1", "execution_state": "COMPLETED", "execution_id": f"github-actions:{github_run_id}", "github_run_id": github_run_id, "github_job": os.environ.get("GITHUB_JOB", ""), "action": action, "observed_output": observed_output, "result": result, "commit_sha": commit_sha, "source": "github-actions"}
    capture_path.parent.mkdir(parents=True, exist_ok=True)
    capture_path.write_text(json.dumps(capture, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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
        decision = DecisionObject(decision_id="DEC-TEAM-BRIDGE-001", mission="Prove governed execution reaches durable reusable intelligence.", actor_id=authority.principal_id, action="repo_write", purpose=authority.purpose, scope=authority.scope, current_truth="execution lifecycle is governed and canonical Activity already exists", gap="verified learning must cross into the existing Intelligence promotion machinery", evidence=("evidence:execution-controller", "evidence:team-activity-facade"), epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}), consequence="bounded repository test execution", reversible=True, risk=Risk(uncertainty=1, consequence=1, irreversibility=1), alternatives=("do_not_execute",), expected_value="verified execution-to-intelligence promotion", required_permission="repo_write", verification=VerificationPlan("Intelligence promotion artifact", "existing Promotion Engine writes an artifact bound to this Activity event", ("stop",)), necessary_power=frozenset({"repo_write"}), requested_power=frozenset({"repo_write"}))
        action = {"action_id": "ACT-TEAM-BRIDGE-001", "action_type": "repository_write", "target": "team/activity/bridge-test", "purpose": authority.purpose, "authority_id": authority.authority_id, "decision_id": decision.decision_id, "actor_id": decision.actor_id, "scope": decision.scope, "permission": decision.action}
        issued = gate.authorize(authority=authority, decision=decision, action=action)
        assert issued.allowed

        ec.transition("EXECUTING", action=action, execution_authorization=issued.authorization, gate=gate, preflight=approved_preflight())
        ec.transition("OBSERVED", observation="real execution-controller transition reached OBSERVED")
        next_action = "Next Naya retrieves the verified execution from the promoted intelligence artifact and continues."
        successor = "NEXT-NAYA-EXECUTION-FROM-PROMOTED-INTELLIGENCE"
        learning = {
            "title": "Explicit learning crosses the Activity-to-Intelligence boundary",
            "what_happened": "A governed execution completed VERIFIED and emitted a canonical Activity Event.",
            "intended_outcome": "An explicit learning lesson is converted into the existing Intelligence Event contract and processed by the existing Promotion Engine.",
            "actual_outcome": "The explicit lesson was bound to the verified Activity provenance and became eligible for existing promotion.",
            "lesson": "Verified execution becomes reusable intelligence only when an explicit non-empty lesson is supplied; the Activity record alone must never invent the lesson.",
            "value": "Preserves provenance while preventing operational success from being mistaken for learned intelligence.",
            "recommendation": "Require explicit learning semantics before Activity-to-Intelligence promotion.",
            "next_action": next_action,
            "successor_instruction": successor,
            "root_cause": "The prior Activity boundary contained verified operational facts but no canonical learning semantics.",
        }
        ec.transition("VERIFIED", evidence=["receipt:team-bridge-intelligence-e2e", "test:execution-controller"], verification={"status": "VERIFIED", "method": "execution-to-intelligence-e2e"}, next_action=next_action, successor=successor, new_learning=learning)

        state = ec.load()
        assert state["status"] == "VERIFIED"
        activity_id = state.get("activity_event_id")
        assert activity_id

        from activity_event import find_event
        activity_event = find_event(activity_id, events_root=events_root, index_path=ec.INDEX_PATH)
        assert activity_event is not None, "FIRST_DIVERGENCE=canonical Activity Event cannot be independently recovered"
        assert activity_event["event_type"] == "activity"
        assert activity_event["verification"]["status"] == "VERIFIED"
        assert activity_event["continuity"]["execution_state"] == "COMPLETED"
        assert activity_event["evidence_ids"]

        intelligence_id = f"INT-{activity_id}"
        intelligence_path = ROOT / "MASTER-NOTES" / "INTELLIGENCE-EVENTS" / f"{intelligence_id}.json"
        assert intelligence_path.exists(), "FIRST_DIVERGENCE=Activity -> Intelligence Event missing"
        intelligence_event = json.loads(intelligence_path.read_text(encoding="utf-8"))
        assert intelligence_event["event_id"] == intelligence_id
        assert intelligence_event["lesson"] == learning["lesson"]
        assert f"activity_event:{activity_id}" in intelligence_event["source"]
        assert intelligence_event["evidence"] == activity_event["evidence_ids"]
        assert intelligence_event["evidence_state"] == "VERIFIED"

        import promote_intelligence as promotion_engine
        promotion_root = tmp / "promotion"
        promotion_event_dir = promotion_root / "INTELLIGENCE-EVENTS"
        promotion_receipt_dir = promotion_root / "INTELLIGENCE-PROMOTIONS"
        promotion_naya_dir = promotion_root / "NAYA-NOTES"
        promotion_shawn_dir = promotion_root / "SHAWN-NOTES"
        promotion_feed_dir = promotion_root / "INTELLIGENCE-FEED"
        promotion_hub = promotion_root / "PRIMARY-INTELLIGENCE-HUB.md"
        promotion_event_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(intelligence_path, promotion_event_dir / intelligence_path.name)
        promotion_engine.EVENT_DIR = promotion_event_dir
        promotion_engine.RECEIPT_DIR = promotion_receipt_dir
        promotion_engine.NAYA_DIR = promotion_naya_dir
        promotion_engine.SHAWN_DIR = promotion_shawn_dir
        promotion_engine.FEED_DIR = promotion_feed_dir
        promotion_engine.HUB_PATH = promotion_hub
        assert promotion_engine.main() == 0, "FIRST_DIVERGENCE=existing Promotion Engine rejected the isolated Intelligence Event"

        receipt_path = promotion_receipt_dir / "LATEST-PROMOTION-RECEIPT.json"
        assert receipt_path.exists(), "FIRST_DIVERGENCE=Promotion Engine receipt missing"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        rows = [row for row in receipt.get("receipts", []) if row.get("event_id") == intelligence_id]
        assert rows, "FIRST_DIVERGENCE=Promotion Engine did not process the new Intelligence Event"
        row = rows[-1]
        assert row["promotion_status"] == "PROMOTED_WRITTEN", f"FIRST_DIVERGENCE=unexpected promotion status {row['promotion_status']!r}"
        promoted = row.get("promoted_artifacts", [])
        assert any(f"{intelligence_id}.md" in item for item in promoted), "FIRST_DIVERGENCE=Promotion Engine produced no bound intelligence artifact"

        feed_path = promotion_feed_dir / f"{intelligence_id}.md"
        note_path = promotion_naya_dir / f"{intelligence_id}.md"
        assert feed_path.exists(), "FIRST_DIVERGENCE=Intelligence Feed artifact missing"
        assert note_path.exists(), "FIRST_DIVERGENCE=Naya Note artifact missing"

        output_lines = ["EXECUTION_CONTROLLER=PASS", "ACTIVITY_EVENT=PASS", "EXPLICIT_LEARNING_LESSON=PASS", "INTELLIGENCE_EVENT=PASS", "PROMOTION_ENGINE=PASS", "PROMOTED_ARTIFACT=PASS", f"EXECUTION_ACTIVITY_EVENT_ID={activity_id}", f"INTELLIGENCE_EVENT_ID={intelligence_id}", f"PROMOTION_STATUS={row['promotion_status']}", f"PROMOTED_ARTIFACTS={json.dumps(promoted)}"]
        output = "\n".join(output_lines)
        _write_ci_execution_capture(observed_output=output, result="PASS", commit_sha=os.environ.get("GITHUB_SHA", ""), run_id=run_id, action="Run governed execution through Activity to Intelligence promotion proof")
        print(output)
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

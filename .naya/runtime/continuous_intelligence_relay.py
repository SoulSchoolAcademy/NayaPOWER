#!/usr/bin/env python3
"""
Continuous Intelligence Relay
Automates Activity → Learning → Playback → Baton updates around canonical events
without creating a second store.

One canonical event creates:
- Durable operational record (execution receipt + activity event)
- Reusable learning when material (learning evidence + learner state)
- Playback state (lineage chain)
- One successor baton (BATON.json)

Architecture:
EXECUTION RECEIPT → (trigger) → INTELLIGENCE NOTIFICATION → (consumer) →
  ACTIVITY EVENT + LEARNING CANDIDATE (if new) + PLAYBACK UPDATE + BATON REBUILD
"""

from __future__ import annotations
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[2]
PI = ROOT / ".naya" / "project-intelligence"
CONTROL_PLANE = ROOT / ".naya" / "control-plane"
STATE = CONTROL_PLANE / "STATE.json"
BLOCKS = CONTROL_PLANE / "BLOCKS.json"
MAP = CONTROL_PLANE / "MAP.json"
PROOF = CONTROL_PLANE / "PROOF.json"
BATON = CONTROL_PLANE / "BATON.json"
ACTIVITY_BOARD = ROOT / "NAYA" / "ACTIVITY" / "2026" / "09" / "00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md"


def run(cmd: list[str], cwd: Path = ROOT) -> str:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def git_head() -> str:
    return run(["git", "rev-parse", "HEAD"])


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_current_state() -> dict:
    """Read current control plane state"""
    return {
        "state": load_json(STATE),
        "blocks": load_json(BLOCKS),
        "map": load_json(MAP),
        "proof": load_json(PROOF),
        "baton": load_json(BATON),
    }


def update_activity_board(event: dict, learning: Optional[dict] = None) -> None:
    """Update the activity board with latest event and learning"""
    head = git_head()
    now = datetime.now(timezone.utc).isoformat()
    
    entry = f"""## {now} — {event.get('event_type', 'ACTIVITY')}

**Event ID:** {event.get('event_id', 'unknown')}
**Action:** {event.get('action', 'unknown')}
**Status:** {event.get('status', 'unknown')}
**Source HEAD:** {head}
**Receipt:** {event.get('receipt_id', 'none')}

"""
    if learning:
        entry += f"""**Learning:** {learning.get('claim', 'none')} → {learning.get('status', 'unknown')}
**Evidence:** {learning.get('evidence_id', 'none')}

"""
    entry += "---\n"
    
    # Prepend to activity board
    existing = ACTIVITY_BOARD.read_text(encoding="utf-8") if ACTIVITY_BOARD.exists() else ""
    ACTIVITY_BOARD.write_text(entry + existing, encoding="utf-8")


def extract_learning_from_event(event: dict) -> Optional[dict]:
    """Determine if an execution event produces new learning"""
    # Check if event has learning-relevant metadata
    metadata = event.get("metadata", {})
    observed = event.get("observed_result", "")
    
    # Heuristics for learning-worthy events
    learning_indicators = [
        "learning" in observed.lower(),
        "verified" in observed.lower(),
        "improved" in observed.lower(),
        "discovered" in observed.lower(),
        "confirmed" in observed.lower(),
    ]
    
    if any(learning_indicators):
        return {
            "claim": observed[:200],
            "source_event_id": event.get("event_id"),
            "source_receipt_id": event.get("receipt_id"),
            "level": "E1_UNDERSTANDS",
            "provenance": "RUNTIME_OBSERVATION",
            "status": "CANDIDATE",
            "verification_method": "AUTOMATIC_EXTRACTION",
        }
    return None


def create_learning_candidate(learning: dict) -> str:
    """Create learning evidence record via Supabase RPC (placeholder for actual integration)"""
    # In production, this would call nayanet-compound-intelligence → learningCandidate
    # For now, record locally
    evidence_id = f"learning-{learning['source_event_id']}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    learning["evidence_id"] = evidence_id
    learning["created_at"] = datetime.now(timezone.utc).isoformat()
    
    # Save to project-intelligence
    learning_path = PI / f"{evidence_id}.json"
    save_json(learning_path, learning)
    
    return evidence_id


def update_playback_lineage(event: dict) -> None:
    """Update playback lineage with new event"""
    # In production, this would update the canonical playback chain
    # For now, record the lineage entry
    lineage_entry = {
        "event_id": event.get("event_id"),
        "event_type": event.get("event_type"),
        "source_receipt_id": event.get("receipt_id"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": event.get("action"),
        "status": event.get("status"),
        "next_action": event.get("next_action"),
    }
    
    lineage_path = CONTROL_PLANE / "PLAYBACK_LINEAGE.json"
    existing = load_json(lineage_path) if lineage_path.exists() else {"lineage": []}
    existing["lineage"].append(lineage_entry)
    existing["latest_event_id"] = event.get("event_id")
    existing["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_json(lineage_path, existing)


def rebuild_baton(event: dict, learning: Optional[dict] = None) -> None:
    """Rebuild the successor baton with current state"""
    cp = get_current_state()
    head = git_head()
    
    # Update BATON.json with latest event and learning
    baton = cp["baton"]
    if "source_snapshot" not in baton:
        baton["source_snapshot"] = {}
    baton["source_snapshot"]["live_head"] = head
    baton["generated_at"] = datetime.now(timezone.utc).isoformat()
    
    # Update evidence with latest event
    if "evidence" not in baton:
        baton["evidence"] = []
    
    baton["evidence"].append({
        "kind": "activity_event",
        "event_id": event.get("event_id"),
        "receipt_id": event.get("receipt_id"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": event.get("action"),
        "status": event.get("status"),
    })
    
    if learning:
        baton["evidence"].append({
            "kind": "learning_candidate",
            "evidence_id": learning.get("evidence_id"),
            "claim": learning.get("claim"),
            "status": learning.get("status"),
        })
    
    # Update next action if event provides one
    if event.get("next_action"):
        baton["next_action"]["action"] = event["next_action"]
        baton["next_action"]["reason"] = f"Derived from event {event.get('event_id')}"
    
    save_json(BATON, baton)


def relay_from_execution_receipt(receipt: dict) -> dict:
    """
    Main relay function: given an execution receipt, propagate intelligence
    through Activity → Learning → Playback → Baton
    """
    # Build canonical event from receipt
    event = {
        "event_id": f"execution-receipt:{receipt.get('id', 'unknown')}",
        "event_type": "EXECUTION_COMPLETED",
        "action": receipt.get("action", "unknown"),
        "status": receipt.get("status", "unknown"),
        "receipt_id": receipt.get("id"),
        "revision": receipt.get("revision"),
        "observed_result": receipt.get("observed_result", ""),
        "expected_result": receipt.get("expected_result", ""),
        "evidence": receipt.get("evidence", {}),
        "learning": receipt.get("learning", []),
        "authority_grant_id": receipt.get("authority_grant_id"),
        "authority_source_event_id": receipt.get("authority_source_event_id"),
        "created_at": receipt.get("created_at"),
        "next_action": None,  # Will be derived from control plane
    }
    
    # Get current next action from control plane
    state = load_json(STATE)
    sna = state.get("single_next_action")
    if isinstance(sna, dict):
        event["next_action"] = sna.get("action")
    else:
        event["next_action"] = sna
    
    # 1. Activity: Event already exists (execution receipt trigger creates notification)
    # 2. Learning: Extract if material
    learning = extract_learning_from_event(event)
    if learning:
        evidence_id = create_learning_candidate(learning)
        learning["evidence_id"] = evidence_id
    
    # 3. Playback: Update lineage
    update_playback_lineage(event)
    
    # 4. Baton: Rebuild successor context
    rebuild_baton(event, learning)
    
    # 5. Activity Board: Update human-readable board
    update_activity_board(event, learning)
    
    return {
        "event": event,
        "learning": learning,
        "relayed_at": datetime.now(timezone.utc).isoformat(),
        "status": "RELAYED"
    }


def main() -> int:
    """Test the relay with a mock execution receipt"""
    mock_receipt = {
        "id": "test-receipt-001",
        "revision": 1,
        "action": "test_intelligence_commit",
        "expected_result": "Learning captured as Intelligent Block",
        "observed_result": "Verified learning improved policy from 0 to 1 on held-out case",
        "status": "SUCCESS",
        "evidence": {"event_id": "test-event-001"},
        "learning": [{"type": "policy_improvement", "before": 0, "after": 1}],
        "authority_grant_id": "test-grant-001",
        "authority_source_event_id": "test-source-001",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    
    result = relay_from_execution_receipt(mock_receipt)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
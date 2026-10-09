"""KNOW-side receiver for the ACT -> KNOW execution handoff arc.

ingest_execution() records an execution handoff as a knowledge edge: it
appends one JSON object per line to the edge log at
.naya/memory/execution-edges.jsonl (edge = handoff + ingested_at + edge_id).

Fail-closed receiver: handoffs missing execution_id or action_taken are
REFUSED, never recorded.
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EDGES_PATH = ROOT / ".naya" / "memory" / "execution-edges.jsonl"

EDGE_TYPE_EXECUTION = "EXECUTION"


def _edges_path(registry_path=None) -> Path:
    if registry_path is not None:
        return Path(registry_path)
    env = os.environ.get("NAYA_EXECUTION_EDGES")
    if env:
        return Path(env)
    return DEFAULT_EDGES_PATH


def _atomic_append_jsonl(path: Path, record: dict) -> None:
    """Append one JSON line atomically (read all + temp + rename).

    The edge log is small; a read-all/append/rewrite keeps the file always
    well-formed (no torn lines) even if the process dies mid-write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    lines.append(json.dumps(record, ensure_ascii=False))
    tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def ingest_execution(handoff: dict, registry_path=None) -> dict:
    """Record an execution handoff as a knowledge edge.

    Returns {"status": "RECORDED", "edge_id": ...} on success, or
    {"status": "REFUSED", "reason": ...} when the handoff fails the
    fail-closed validation (missing execution_id / action_taken).
    """
    if not isinstance(handoff, dict):
        return {"status": "REFUSED", "reason": "handoff must be a dict (fail closed)"}
    execution_id = str(handoff.get("execution_id") or "").strip()
    action_taken = str(handoff.get("action_taken") or "").strip()
    if not execution_id:
        return {"status": "REFUSED",
                "reason": "missing execution_id (fail closed)"}
    if not action_taken:
        return {"status": "REFUSED",
                "reason": "missing action_taken (fail closed)"}
    edge = {
        "edge_id": uuid.uuid4().hex,
        "type": EDGE_TYPE_EXECUTION,
        "handoff": handoff,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        _atomic_append_jsonl(_edges_path(registry_path), edge)
    except OSError as exc:
        return {"status": "REFUSED",
                "reason": f"edge log write failed: {exc} (fail closed)"}
    return {"status": "RECORDED", "edge_id": edge["edge_id"]}

"""PROVE lifecycle step: verify an execution's outcome against its prediction.

Reads the execution edge from .naya/memory/execution-edges.jsonl and compares
what the plan predicted (predicted_outcome) with what execution observed
(outcome_observed):

  - both present and exactly equal -> MATCH
  - both present and different     -> MISMATCH (with flag OUTCOME_DEVIATION)
  - either missing                 -> INSUFFICIENT_DATA

The verdict is written back to the edge log as a new edge of type "PROOF"
linking to the execution_id — the proof is itself recorded knowledge, never
a silent in-memory verdict.
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EDGES_PATH = ROOT / ".naya" / "memory" / "execution-edges.jsonl"

MATCH = "MATCH"
MISMATCH = "MISMATCH"
INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
OUTCOME_DEVIATION = "OUTCOME_DEVIATION"

EDGE_TYPE_PROOF = "PROOF"


def _edges_path(edges_path=None) -> Path:
    if edges_path is not None:
        return Path(edges_path)
    env = os.environ.get("NAYA_EXECUTION_EDGES")
    if env:
        return Path(env)
    return DEFAULT_EDGES_PATH


def _read_edges(path: Path) -> list:
    if not path.exists():
        return []
    edges = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            edges.append(json.loads(line))
        except ValueError:
            continue
    return edges


def _append_edge(path: Path, edge: dict) -> None:
    """Append one JSON line atomically (read all + temp + rename)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    lines.append(json.dumps(edge, ensure_ascii=False))
    tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def prove_execution(execution_id: str, edges_path=None) -> dict:
    """Verify an execution's outcome against its prediction.

    Returns {"execution_id": ..., "verdict": "MATCH"|"MISMATCH"|
    "INSUFFICIENT_DATA", "predicted": ..., "observed": ..., "proven_at": ...}.
    A MISMATCH verdict includes "flag": "OUTCOME_DEVIATION" (not silent).
    The verdict is persisted as a PROOF edge; persistence status is reported
    as proof_persisted / proof_edge_id (or proof_error on failure).
    """
    path = _edges_path(edges_path)
    execution_edge = None
    for edge in _read_edges(path):
        if edge.get("type") == EDGE_TYPE_PROOF:
            continue
        handoff = edge.get("handoff") or {}
        if handoff.get("execution_id") == execution_id:
            execution_edge = edge  # last recorded execution edge wins
    handoff = (execution_edge or {}).get("handoff") or {}
    predicted = handoff.get("predicted_outcome")
    observed = handoff.get("outcome_observed")
    proven_at = datetime.now(timezone.utc).isoformat()

    result = {
        "execution_id": execution_id,
        "predicted": predicted,
        "observed": observed,
        "proven_at": proven_at,
    }
    if predicted and observed:
        if str(predicted) == str(observed):
            result["verdict"] = MATCH
        else:
            result["verdict"] = MISMATCH
            result["flag"] = OUTCOME_DEVIATION
    else:
        result["verdict"] = INSUFFICIENT_DATA

    proof_edge = {
        "edge_id": uuid.uuid4().hex,
        "type": EDGE_TYPE_PROOF,
        "execution_id": execution_id,
        "verdict": result["verdict"],
        "predicted": predicted,
        "observed": observed,
        "proven_at": proven_at,
    }
    if result.get("flag"):
        proof_edge["flag"] = result["flag"]
    try:
        _append_edge(path, proof_edge)
    except OSError as exc:
        result["proof_persisted"] = False
        result["proof_error"] = str(exc)
    else:
        result["proof_persisted"] = True
        result["proof_edge_id"] = proof_edge["edge_id"]
    return result

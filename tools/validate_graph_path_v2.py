#!/usr/bin/env python3
"""Multi-hop graph path quality gate (Graph Relationship Contract V2).

Composes the single-edge selector gate from validate_graph_selector_v2.py over
bounded multi-hop traversals. A path is only as good as its weakest hop:
every hop must pass the full edge-level gate, or the path is not selected.

Path laws (fail-closed):
  1. Per-hop gate: each hop is evaluated with its own target_id against the
     same task (owner_id, task_class, now). A hop that fails the edge gate
     cannot carry a path. No hop, no path.
  2. Hop budget: at most max_hops edges. If the target is reachable only with
     more hops than the budget allows -> PATH_HOP_BUDGET_EXCEEDED.
  3. No cycles: a path never revisits a node. If no valid path exists and the
     search pruned a revisit -> PATH_CYCLE_DETECTED.
  4. Unresolved contradiction: a CONTRADICTS hop is traversal-blocked. If the
     only routes to the target run through an unresolved contradiction ->
     PATH_UNRESOLVED_CONFLICT (mirrors the V2 reconciliation oracle).
  5. Shortest first: among valid paths, the shortest (fewest hops) wins.
     A longer admissible route never shadows a shorter one.

Reason precedence on failure:
  PATH_FOUND > PATH_HOP_BUDGET_EXCEEDED > PATH_CYCLE_DETECTED >
  PATH_UNRESOLVED_CONFLICT > NO_VALID_PATH

Authority boundary: a selected path is a *retrieval* result, not an
authorization. Per the V2 authority contract, relationship_exists => authorized
and retrieved => authorized are forbidden inferences. This tool grants nothing.
"""

import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
_SELECTOR_PATH = Path(__file__).resolve().parent / "validate_graph_selector_v2.py"
FIXTURE = ROOT / "BRAIN/04-INTELLIGENCE/GRAPH/0006-GRAPH-PATH-V2-ACCEPTANCE.json"

_spec = importlib.util.spec_from_file_location(
    "graph_selector_v2", _SELECTOR_PATH
)
_selector = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_selector)
evaluate = _selector.evaluate

CONTRADICTS_TYPES = {"CONTRADICTS"}


def _hop_task(edge: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    hop = dict(task)
    hop["target_id"] = edge.get("target_id")
    return hop


def find_path(
    edges: list[dict[str, Any]],
    start_node: str,
    target_node: str,
    task: dict[str, Any],
    allowed_types: list[str],
    max_hops: int,
) -> tuple[bool, str, list[str], dict[str, Any]]:
    """Select a quality-gated path from start_node to target_node.

    Returns (selected, reason, path_relationship_ids, detail).
    """
    detail: dict[str, Any] = {"hop_rejections": [], "cycle_pruned": False}

    admissible: list[dict[str, Any]] = []
    conflict_seen = False
    for edge in edges:
        selected, reason = evaluate(edge, _hop_task(edge, task), allowed_types)
        if not selected:
            detail["hop_rejections"].append(
                {"relationship_id": edge.get("relationship_id"), "reason": reason}
            )
            continue
        if edge.get("relationship_type") in CONTRADICTS_TYPES:
            conflict_seen = True
            continue
        admissible.append(edge)

    adjacency: dict[str, list[dict[str, Any]]] = {}
    for edge in admissible:
        adjacency.setdefault(str(edge.get("source_id")), []).append(edge)

    def search(depth_limit: int | None) -> tuple[list[dict[str, Any]] | None, bool]:
        """BFS shortest-first, cycle-guarded. Returns (found_path, cycle_pruned)."""
        from collections import deque

        if start_node == target_node:
            return [], False
        queue: deque[tuple[str, list[dict[str, Any]]]] = deque()
        queue.append((start_node, []))
        cycle_pruned = False
        while queue:
            node, path = queue.popleft()
            if depth_limit is not None and len(path) >= depth_limit:
                continue
            path_nodes = {start_node} | {str(e.get("target_id")) for e in path}
            for edge in adjacency.get(node, []):
                nxt = str(edge.get("target_id"))
                if nxt in path_nodes:
                    cycle_pruned = True
                    continue
                new_path = path + [edge]
                if nxt == target_node:
                    return new_path, cycle_pruned
                queue.append((nxt, new_path))
        return None, cycle_pruned

    bounded_path, bounded_cycle = search(max_hops)
    if bounded_path is not None:
        return (
            True,
            "PATH_FOUND",
            [str(e.get("relationship_id")) for e in bounded_path],
            detail,
        )

    unbounded_path, unbounded_cycle = search(None)
    if unbounded_path is not None:
        # Target reachable with admissible edges, but only beyond the hop budget.
        return False, "PATH_HOP_BUDGET_EXCEEDED", [], detail

    detail["cycle_pruned"] = bounded_cycle or unbounded_cycle
    if detail["cycle_pruned"]:
        return False, "PATH_CYCLE_DETECTED", [], detail
    if conflict_seen:
        return False, "PATH_UNRESOLVED_CONFLICT", [], detail
    return False, "NO_VALID_PATH", [], detail


def main() -> int:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    task = data["task"]
    allowed = data["allowed_relationship_types"]
    max_hops = data["max_hops"]
    failures = []
    for case in data["cases"]:
        selected, reason, path, _detail = find_path(
            case["edges"],
            case["start_node"],
            case["target_node"],
            task,
            allowed,
            case.get("max_hops", max_hops),
        )
        if selected != case["expect_selected"]:
            failures.append(
                {
                    "case": case["name"],
                    "expected_selected": case["expect_selected"],
                    "actual_selected": selected,
                    "reason": reason,
                    "path": path,
                }
            )
        expected_reason = case.get("expect_reason")
        if expected_reason and reason != expected_reason:
            failures.append(
                {
                    "case": case["name"],
                    "expected_reason": expected_reason,
                    "actual_reason": reason,
                }
            )
        expected_path = case.get("expect_path")
        if expected_path is not None and path != expected_path:
            failures.append(
                {
                    "case": case["name"],
                    "expected_path": expected_path,
                    "actual_path": path,
                }
            )
    print(
        json.dumps(
            {
                "schema": "naya.graph.path.v2.acceptance-report",
                "failures": failures,
                "passed": not failures,
            },
            indent=2,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

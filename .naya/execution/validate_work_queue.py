#!/usr/bin/env python3
"""Fail-closed validator and selector bridge for the ONE Master Work Queue.

The queue is durable operational work input. It is subordinate to the
constitution, control plane, and governance kernel, and it feeds the canonical
`.naya/runtime/priority_decision.py` selector. This module never executes work,
never grants authority, and never defines a competing state machine.

Commands:
  validate   structural + semantic validation of the canonical queue (GREEN/RED)
  select     validate, then return exactly ONE highest-value executable task,
             or STOP_CLEANLY when no legitimate work remains
  self-test  adversarial RED/GREEN proof that malformed queues fail closed
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
QUEUE_PATH = ROOT / ".naya" / "execution" / "WORK-QUEUE.json"
SCHEMA_PATH = ROOT / ".naya" / "execution" / "MASTER-WORK-QUEUE-V1.schema.json"
RUNTIME_DIR = ROOT / ".naya" / "runtime"
for _path in (RUNTIME_DIR, ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from priority_decision import PriorityError, WorkItem, choose_priority  # noqa: E402

SCHEMA_ID = "naya/master-work-queue/v1"
STATUSES = {"PROPOSED", "READY", "IN_PROGRESS", "COMPLETE", "BLOCKED", "DEFERRED", "FAILED", "CANCELLED"}
TERMINAL_SUCCESS = {"COMPLETE"}
CANDIDATE_STATUSES = {"READY", "IN_PROGRESS"}
SELECTOR_FACTORS = ("mission_alignment", "expected_value", "urgency", "dependency_impact", "reversibility", "risk")
REQUIRED_TASK_FIELDS = (
    "task_id", "mission", "objective", "current_state", "why_it_matters", "dependencies",
    "authority", "constraints", "protected_boundaries", "acceptance_criteria",
    "test_requirements", "evidence_requirements", "quality_scorecard", "minimum_score",
    "target_score", "risk", "rollback_repair", "next_action", "successor_action",
    "autonomy_level", "status", "selector",
)
LIST_FIELDS = (
    "dependencies", "constraints", "protected_boundaries", "acceptance_criteria",
    "test_requirements", "evidence_requirements",
)


def load(path: Path = QUEUE_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_is_text(item) for item in value)


def _is_score(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _detect_cycle(graph: dict[str, list[str]]) -> list[str]:
    state: dict[str, int] = {}
    cycle: list[str] = []

    def visit(node: str, stack: list[str]) -> bool:
        if state.get(node) == 1:
            cycle.extend(stack[stack.index(node):] + [node])
            return True
        if state.get(node) == 2:
            return False
        state[node] = 1
        for dep in graph.get(node, []):
            if visit(dep, stack + [node]):
                return True
        state[node] = 2
        return False

    for node in graph:
        if state.get(node) is None and visit(node, []):
            return cycle
    return []


def validate(queue: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(queue, dict):
        return ["queue must be an object"]
    if queue.get("$schema") != SCHEMA_ID:
        errors.append(f"queue: invalid $schema (expected {SCHEMA_ID})")
    if queue.get("status") != "CANONICAL":
        errors.append("queue: status must be CANONICAL")

    authority = queue.get("authority")
    if not isinstance(authority, dict):
        errors.append("queue: authority object is required")
    else:
        if not _is_nonempty_list(authority.get("subordinate_to")):
            errors.append("queue.authority: subordinate_to must be a non-empty list")
        if not _is_text(authority.get("selector")):
            errors.append("queue.authority: selector is required")
        if not _is_text(authority.get("record_layer")):
            errors.append("queue.authority: record_layer is required")

    policy = queue.get("quality_policy")
    if not isinstance(policy, dict):
        errors.append("queue: quality_policy object is required")
    else:
        minimum = policy.get("minimum_score")
        target = policy.get("target_score")
        objective = policy.get("objective_score")
        if not _is_score(minimum) or minimum < 9.0:
            errors.append("queue.quality_policy: minimum_score must be >= 9.0")
        if not _is_score(target) or (_is_score(minimum) and target < minimum):
            errors.append("queue.quality_policy: target_score must be >= minimum_score")
        if not _is_score(objective) or (_is_score(target) and objective < target):
            errors.append("queue.quality_policy: objective_score must be >= target_score")
        if not _is_text(policy.get("regression_law")):
            errors.append("queue.quality_policy: regression_law is required")

    tasks = queue.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        errors.append("queue: tasks must be a non-empty list")
        return errors

    seen: set[str] = set()
    graph: dict[str, list[str]] = {}
    status_by_id: dict[str, str] = {}
    index: dict[str, dict[str, Any]] = {}
    for position, task in enumerate(tasks):
        label = f"task[{position}]"
        if not isinstance(task, dict):
            errors.append(f"{label}: must be an object")
            continue
        task_id = task.get("task_id")
        if not _is_text(task_id) or not task_id.startswith("TASK-"):
            errors.append(f"{label}: invalid task_id")
            continue
        label = task_id
        if task_id in seen:
            errors.append(f"{label}: duplicate task_id")
        seen.add(task_id)
        index[task_id] = task

        for field in REQUIRED_TASK_FIELDS:
            if field not in task:
                errors.append(f"{label}: missing required field {field}")
        if not _is_text(task.get("mission")):
            errors.append(f"{label}: mission is required")
        for field in ("objective", "current_state", "why_it_matters", "rollback_repair", "next_action", "successor_action"):
            if not _is_text(task.get(field)):
                errors.append(f"{label}: {field} is required")
        for field in LIST_FIELDS:
            value = task.get(field)
            if field == "dependencies":
                if not isinstance(value, list) or not all(_is_text(item) and item.startswith("TASK-") for item in value):
                    errors.append(f"{label}: dependencies must be a list of TASK- ids")
                else:
                    graph[task_id] = list(value)
            elif not _is_nonempty_list(value):
                errors.append(f"{label}: {field} must be a non-empty list of strings")

        task_authority = task.get("authority")
        if not isinstance(task_authority, dict) or not _is_text(task_authority.get("source")) or not _is_nonempty_list(task_authority.get("scope")):
            errors.append(f"{label}: authority requires a source and a non-empty scope list")

        scorecard = task.get("quality_scorecard")
        if not isinstance(scorecard, dict) or not _is_nonempty_list(scorecard.get("dimensions")):
            errors.append(f"{label}: quality_scorecard.dimensions must be a non-empty list")

        minimum = task.get("minimum_score")
        target = task.get("target_score")
        if not _is_score(minimum) or minimum < 9.0:
            errors.append(f"{label}: minimum_score must be >= 9.0")
        if not _is_score(target) or (_is_score(minimum) and target < minimum):
            errors.append(f"{label}: target_score must be >= minimum_score")

        risk = task.get("risk")
        if not _is_text(risk) or not (len(risk) == 2 and risk[0] == "R" and risk[1] in "012345" and risk[1].isdigit()):
            errors.append(f"{label}: risk must be R0..R5")

        level = task.get("autonomy_level")
        if not isinstance(level, int) or isinstance(level, bool) or not 1 <= level <= 8:
            errors.append(f"{label}: autonomy_level must be an integer 1..8")

        status = task.get("status")
        if status not in STATUSES:
            errors.append(f"{label}: invalid status")
        status_by_id[task_id] = status if isinstance(status, str) else ""

        selector = task.get("selector")
        blocked_flag = isinstance(selector, dict) and selector.get("blocked") is True
        if not isinstance(selector, dict):
            errors.append(f"{label}: selector object is required")
        else:
            for factor in SELECTOR_FACTORS:
                value = selector.get(factor)
                if not _is_score(value) or not 0 <= value <= 1:
                    errors.append(f"{label}: selector.{factor} must be between 0 and 1")
            for flag in ("executable", "blocked"):
                if not isinstance(selector.get(flag), bool):
                    errors.append(f"{label}: selector.{flag} must be a boolean")
            if blocked_flag and status != "BLOCKED":
                errors.append(f"{label}: selector.blocked=true requires status=BLOCKED")
            if selector.get("executable") is False and selector.get("blocked") is not True:
                errors.append(f"{label}: non-executable task must be blocked")
        if (status == "BLOCKED" or blocked_flag) and not _is_text(task.get("blocked_reason")):
            errors.append(f"{label}: blocked task requires blocked_reason")

    for task_id, deps in graph.items():
        for dep in deps:
            if dep not in seen:
                errors.append(f"{task_id}: dependency {dep} does not exist")
            elif dep == task_id:
                errors.append(f"{task_id}: task cannot depend on itself")
    for task_id in graph:
        if status_by_id.get(task_id) in CANDIDATE_STATUSES:
            unmet = [dep for dep in graph[task_id] if status_by_id.get(dep) not in TERMINAL_SUCCESS]
            if unmet:
                errors.append(f"{task_id}: candidate status requires completed dependencies: {', '.join(unmet)}")

    cycle = _detect_cycle(graph)
    if cycle:
        errors.append("dependency cycle detected: " + " -> ".join(cycle))
    return errors


def candidates(queue: dict[str, Any]) -> list[dict[str, Any]]:
    tasks = queue["tasks"]
    status_by_id = {task["task_id"]: task["status"] for task in tasks}
    ready: list[dict[str, Any]] = []
    for task in tasks:
        if task["status"] not in CANDIDATE_STATUSES:
            continue
        selector = task["selector"]
        if not selector["executable"] or selector["blocked"]:
            continue
        if any(status_by_id.get(dep) not in TERMINAL_SUCCESS for dep in task["dependencies"]):
            continue
        ready.append(task)
    return ready


def _work_item(task: dict[str, Any]) -> WorkItem:
    selector = task["selector"]
    return WorkItem(
        work_id=task["task_id"],
        title=task["objective"],
        next_action=task["next_action"],
        acceptance_criteria="; ".join(task["acceptance_criteria"]),
        mission_alignment=selector["mission_alignment"],
        expected_value=selector["expected_value"],
        urgency=selector["urgency"],
        dependency_impact=selector["dependency_impact"],
        reversibility=selector["reversibility"],
        risk=selector["risk"],
        executable=selector["executable"],
        blocked=selector["blocked"],
    )


def select(queue: dict[str, Any]) -> dict[str, Any]:
    ready = candidates(queue)
    if not ready:
        return {
            "status": "STOP_CLEANLY",
            "reason": "no legitimate executable unblocked work remains",
            "candidate_count": 0,
        }
    mission = next((task["mission"] for task in queue["tasks"] if _is_text(task.get("mission"))), "")
    try:
        decision = choose_priority(mission, [_work_item(task) for task in ready])
    except PriorityError as exc:
        return {"status": "STOP_CLEANLY", "reason": str(exc), "candidate_count": len(ready)}
    winner = next(task for task in ready if task["task_id"] == decision.work_id)
    return {
        "status": "SELECTED",
        "task_id": decision.work_id,
        "priority": decision.priority,
        "score": round(decision.score, 6),
        "why": decision.why,
        "next_action": decision.next_action,
        "acceptance_criteria": decision.acceptance_criteria,
        "successor_action": winner["successor_action"],
        "autonomy_level": winner["autonomy_level"],
        "risk": winner["risk"],
        "candidate_count": len(ready),
    }


def _mutate(queue: dict[str, Any], path: str, value: Any) -> dict[str, Any]:
    clone = json.loads(json.dumps(queue))
    parts = path.split(".")
    node: Any = clone
    for part in parts[:-1]:
        node = node[int(part)] if part.isdigit() else node[part]
    last = parts[-1]
    if last.isdigit():
        node[int(last)] = value
    else:
        node[last] = value
    return clone


def self_test() -> int:
    base = load()
    assert not validate(base), "canonical queue must validate"
    selection = select(base)
    assert selection["status"] == "SELECTED", "canonical queue must select exactly one task"

    def tid(name: str) -> int:
        return next(position for position, task in enumerate(base["tasks"]) if task["task_id"] == name)

    m1 = tid("TASK-NAYA-M1-MASTER-WORK-QUEUE")
    m2 = tid("TASK-NAYA-M2-EXECUTION-SUPERVISOR")
    m3 = tid("TASK-NAYA-M3-ACTIVITY-AUTOWRITE")

    checks = [
        ("duplicate task_id", _mutate(base, f"tasks.{m2}.task_id", base["tasks"][m1]["task_id"]), "duplicate task_id"),
        ("minimum below floor", _mutate(base, f"tasks.{m1}.minimum_score", 8.9), "minimum_score must be >= 9.0"),
        ("missing required field", _mutate(base, f"tasks.{m1}", {k: v for k, v in base["tasks"][m1].items() if k != "successor_action"}), "missing required field successor_action"),
        ("selector out of range", _mutate(base, f"tasks.{m1}.selector.risk", 1.5), "selector.risk must be between 0 and 1"),
        ("blocked without reason", _mutate(base, f"tasks.{m3}.status", "BLOCKED"), "blocked task requires blocked_reason"),
        ("blocked flag/status mismatch", _mutate(base, f"tasks.{m3}.selector.blocked", True), "requires status=BLOCKED"),
        ("unknown dependency", _mutate(base, f"tasks.{m2}.dependencies", ["TASK-DOES-NOT-EXIST"]), "does not exist"),
        ("candidate with unmet dependency", _mutate(base, f"tasks.{m3}.status", "READY"), "requires completed dependencies"),
        ("invalid quality policy", _mutate(base, "quality_policy.minimum_score", 8.0), "minimum_score must be >= 9.0"),
        ("invalid schema id", _mutate(base, "$schema", "naya/other/v1"), "invalid $schema"),
    ]
    failures = 0
    for name, mutated, expected in checks:
        errors = validate(mutated)
        matched = any(expected in error for error in errors)
        print(f"{'PASS' if matched else 'FAIL'}: {name} -> {'RED' if errors else 'GREEN'}")
        if not matched:
            failures += 1
            print(f"  expected substring: {expected}")
            print(f"  actual errors: {errors}")

    cycle = json.loads(json.dumps(base))
    cycle["tasks"][m1]["dependencies"] = ["TASK-NAYA-M2-EXECUTION-SUPERVISOR"]
    cycle_errors = validate(cycle)
    cycle_ok = any("cycle" in error for error in cycle_errors)
    print(f"{'PASS' if cycle_ok else 'FAIL'}: dependency cycle detected -> {'RED' if cycle_errors else 'GREEN'}")
    if not cycle_ok:
        failures += 1
        print(f"  actual errors: {cycle_errors}")

    print(f"SELECTED {selection['task_id']} (score {selection['score']})")
    if failures:
        print(f"FAIL - {failures} self-test assertion(s) failed")
        return 1
    print("PASS - Master Work Queue validation, fail-closed behavior, and selection are GREEN")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Master Work Queue validator and selector")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("select")
    sub.add_parser("self-test")
    args = parser.parse_args()
    try:
        queue = load()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"WORK_QUEUE=RED\nFIRST_DIVERGENCE={exc}")
        return 1
    if args.command == "self-test":
        return self_test()
    errors = validate(queue)
    if args.command == "validate":
        if errors:
            print("WORK_QUEUE=RED")
            for error in errors:
                print(f"- {error}")
            return 1
        print(f"WORK_QUEUE=GREEN ({len(queue['tasks'])} tasks)")
        return 0
    if errors:
        print("WORK_QUEUE=RED — fix validation before selecting")
        for error in errors:
            print(f"- {error}")
        return 1
    print(json.dumps(select(queue), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "pathgate", ROOT / "tools" / "validate_graph_path_v2.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
FIXTURE = json.loads(
    (ROOT / "BRAIN/04-INTELLIGENCE/GRAPH/0006-GRAPH-PATH-V2-ACCEPTANCE.json").read_text()
)
TASK = FIXTURE["task"]
TYPES = FIXTURE["allowed_relationship_types"]
MAX_HOPS = FIXTURE["max_hops"]


def case(name):
    return next(x for x in FIXTURE["cases"] if x["name"] == name)


def run(name, task=None, max_hops=MAX_HOPS):
    c = case(name)
    return mod.find_path(
        copy.deepcopy(c["edges"]),
        c["start_node"],
        c["target_node"],
        copy.deepcopy(task or TASK),
        TYPES,
        c.get("max_hops", max_hops),
    )


def test_all_predeclared_path_cases_match():
    for c in FIXTURE["cases"]:
        selected, reason, path, _detail = run(c["name"])
        assert selected is c["expect_selected"], c["name"]
        if "expect_reason" in c:
            assert reason == c["expect_reason"], c["name"]
        if "expect_path" in c:
            assert path == c["expect_path"], c["name"]


def test_valid_two_hop_path_selected():
    selected, reason, path, _ = run("valid_two_hop_path")
    assert (selected, reason, path) == (True, "PATH_FOUND", ["R-A", "R-B"])


def test_mid_hop_expiry_breaks_path():
    """Adversarial: the middle hop (not an endpoint) is expired -> whole path rejected."""
    c = copy.deepcopy(case("valid_two_hop_path"))
    c["edges"][0]["valid_until"] = "2026-09-30T01:00:00Z"  # first hop expired
    selected, reason, _path, detail = mod.find_path(
        c["edges"], c["start_node"], c["target_node"], copy.deepcopy(TASK), TYPES, MAX_HOPS
    )
    assert (selected, reason) == (False, "NO_VALID_PATH")
    assert detail["hop_rejections"] == [
        {"relationship_id": "R-A", "reason": "TEMPORALLY_INVALID"}
    ]


def test_budget_is_fail_closed():
    selected, reason, _p, _d = run("hop_budget_exceeded")
    assert (selected, reason) == (False, "PATH_HOP_BUDGET_EXCEEDED")
    # Same chain with a 4-hop budget: budget, not quality, was the blocker.
    selected, reason, path, _d = run("hop_budget_exceeded", max_hops=4)
    assert (selected, reason, path) == (True, "PATH_FOUND", ["R-1", "R-2", "R-3", "R-4"])


def test_cycle_is_fail_closed():
    selected, reason, _p, detail = run("cycle_rejected")
    assert (selected, reason) == (False, "PATH_CYCLE_DETECTED")
    assert detail["cycle_pruned"] is True


def test_contradiction_surfaces_conflict():
    selected, reason, _p, _d = run("contradiction_midpath_surfaces_conflict")
    assert (selected, reason) == (False, "PATH_UNRESOLVED_CONFLICT")


def test_shortest_path_wins():
    selected, reason, path, _d = run("shortest_path_preferred")
    assert (selected, reason, path) == (True, "PATH_FOUND", ["R-S1"])


def test_cross_owner_hop_rejected():
    selected, reason, _p, detail = run("cross_owner_hop_rejected")
    assert (selected, reason) == (False, "NO_VALID_PATH")
    assert detail["hop_rejections"] == [
        {"relationship_id": "R-Y2", "reason": "OWNER_MISMATCH"}
    ]


def test_disconnected_target_has_no_path():
    selected, reason, _p, detail = run("valid_two_hop_path")
    assert selected is True
    # Same valid edges, but the target is not connected to anything.
    c = case("valid_two_hop_path")
    selected, reason, _p, detail = mod.find_path(
        copy.deepcopy(c["edges"]), "N-1", "N-9", copy.deepcopy(TASK), TYPES, MAX_HOPS
    )
    assert (selected, reason) == (False, "NO_VALID_PATH")
    assert detail["hop_rejections"] == []


def test_start_equals_target_is_trivial_path():
    c = case("valid_two_hop_path")
    selected, reason, path, _d = mod.find_path(
        copy.deepcopy(c["edges"]), "N-1", "N-1", copy.deepcopy(TASK), TYPES, MAX_HOPS
    )
    assert (selected, reason, path) == (True, "PATH_FOUND", [])

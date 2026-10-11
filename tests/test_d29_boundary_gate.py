"""Tests for the D29 boundary-claims gate.

Real-mechanism tests run against the actual drift_canary/d29_boundary.py
(the stacked tree carries it via the #2184 base branch). Sabotage tests
inject fake mechanisms through the gate's sys.modules test seam and prove
the gate fails closed (exit 2) instead of passing on a neutered module.
"""

import json
import os
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from types import ModuleType, SimpleNamespace

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.d29_boundary_gate import judge  # noqa: E402

TREE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_NAME = "drift_canary.d29_boundary"
EMPTY_MANIFEST = os.path.join(TREE_ROOT, "tools", "d29_boundary_manifest.json")

VERDICTS = (
    "ENVIRONMENT_BLOCKER", "SCHEDULER_STARVATION",
    "SCHEDULER_SERVICE_FAILURE", "WORKER_NONPROGRESS",
    "BOUNDARY_UNDETERMINED", "COMPLETED",
)
CONTROLLERS = ("ENVIRONMENT", "SCHEDULER", "WORKER", "UNDETERMINED")


@contextmanager
def seeded_fake(mod):
    saved = sys.modules.get(MODULE_NAME)
    sys.modules[MODULE_NAME] = mod
    try:
        yield
    finally:
        if saved is None:
            sys.modules.pop(MODULE_NAME, None)
        else:
            sys.modules[MODULE_NAME] = saved


def make_fake(table=None, ledger_ok=True, with_api=True):
    """Build a fake d29_boundary module.

    table maps (case, rounds) -> (verdict, controller); anything absent
    returns BOUNDARY_UNDETERMINED/UNDETERMINED (the blind default).
    """
    table = table or {}
    mod = ModuleType(MODULE_NAME)
    mod.VERDICTS = VERDICTS
    mod.CONTROLLERS = CONTROLLERS
    mod.CASES = ("A", "B", "C")

    @dataclass(frozen=True)
    class ComponentReport:
        component: str
        label: str
        seq: int = 0

    mod.ComponentReport = ComponentReport

    def run_case(case, rounds=6, false_blame=()):
        verdict, controller = table.get(
            (case, rounds), ("BOUNDARY_UNDETERMINED", "UNDETERMINED"))
        return SimpleNamespace(
            case=case, verdict=verdict,
            record=SimpleNamespace(controller=controller),
            detail="fake verdict " + verdict)

    def verify_against_ledger(result):
        if ledger_ok:
            return True, "fake ledger consistent"
        return False, "injected ledger contradiction"

    def classify_boundary(*args, **kwargs):
        return ("BOUNDARY_UNDETERMINED", "UNDETERMINED", "fake")

    if with_api:
        mod.run_case = run_case
    mod.verify_against_ledger = verify_against_ledger
    mod.classify_boundary = classify_boundary
    return mod


def write_manifest(tmp_path, claims):
    path = str(tmp_path / "manifest.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"claims": claims}, fh)
    return path


def claim(cid, case, rounds, verdict, controller, false_blame=None):
    c = {"id": cid, "case": case, "rounds": rounds,
         "claimed_verdict": verdict, "claimed_controller": controller,
         "note": "test claim"}
    if false_blame is not None:
        c["false_blame"] = false_blame
    return c


# --- real mechanism: the honest paths -------------------------------------

def test_dormant_empty_manifest_real_mechanism():
    code, report = judge(TREE_ROOT, EMPTY_MANIFEST)
    assert code == 0
    assert report["verdict"] == "DORMANT"
    assert report["canary"] == "ok"


def test_honest_claim_passes_real_mechanism(tmp_path):
    mp = write_manifest(tmp_path, [
        claim("honest-c", "C", 6, "WORKER_NONPROGRESS", "WORKER")])
    code, report = judge(TREE_ROOT, mp)
    assert code == 0, report
    assert report["verdict"] == "PASS"
    assert report["claims_checked"] == 1


def test_honest_claim_case_b_passes_real_mechanism(tmp_path):
    mp = write_manifest(tmp_path, [
        claim("honest-b", "B", 6, "SCHEDULER_STARVATION", "SCHEDULER")])
    code, report = judge(TREE_ROOT, mp)
    assert code == 0, report
    assert report["verdict"] == "PASS"


def test_fraud_claim_blocked_real_mechanism(tmp_path):
    mp = write_manifest(tmp_path, [
        claim("fraud-a", "A", 6, "SCHEDULER_STARVATION", "SCHEDULER")])
    code, report = judge(TREE_ROOT, mp)
    assert code == 1, report
    assert report["verdict"] == "VIOLATION"
    assert len(report["violations"]) == 1
    v = report["violations"][0]
    assert v["mechanism"] == "ENVIRONMENT_BLOCKER/ENVIRONMENT"


def test_false_blame_does_not_move_verdict(tmp_path):
    mp = write_manifest(tmp_path, [
        claim("fraud-labels", "A", 6, "SCHEDULER_STARVATION", "SCHEDULER",
              false_blame=[
                  {"component": "SCHEDULER",
                   "label": "DATABASE_UNAVAILABLE", "seq": 1},
                  {"component": "WORKER",
                   "label": "WORKER_TIMEOUT", "seq": 2}])])
    code, report = judge(TREE_ROOT, mp)
    assert code == 1, report
    assert report["violations"][0]["mechanism"] == \
        "ENVIRONMENT_BLOCKER/ENVIRONMENT"


def test_controller_mismatch_is_violation(tmp_path):
    mp = write_manifest(tmp_path, [
        claim("ctrl-mismatch", "C", 6, "WORKER_NONPROGRESS", "ENVIRONMENT")])
    code, report = judge(TREE_ROOT, mp)
    assert code == 1, report
    assert report["verdict"] == "VIOLATION"


# --- sabotage: the gate must fail closed, never pass ----------------------

def test_blind_engine_caught_by_canary():
    with seeded_fake(make_fake()):
        code, report = judge(TREE_ROOT, EMPTY_MANIFEST)
    assert code == 2, report
    assert report["canary"] == "FAILED"
    assert report["claims_checked"] == 0


def test_masquerade_engine_caught_by_canary(tmp_path):
    # Returns exactly what the manifest claims for the claimed scenario,
    # but is blind on the canary's non-manifest (B, 7) parameterization.
    table = {("A", 6): ("SCHEDULER_STARVATION", "SCHEDULER")}
    mp = write_manifest(tmp_path, [
        claim("masked", "A", 6, "SCHEDULER_STARVATION", "SCHEDULER")])
    with seeded_fake(make_fake(table=table)):
        code, report = judge(TREE_ROOT, mp)
    assert code == 2, report
    assert report["canary"] == "FAILED"
    assert report["claims_checked"] == 0


def test_missing_mechanism_fails_closed():
    code, report = judge(TREE_ROOT, EMPTY_MANIFEST,
                         mechanism_rel="drift_canary/no_such_module.py")
    assert code == 2, report
    assert any("not found" in n for n in report["notes"])


def test_changed_api_surface_fails_closed():
    with seeded_fake(make_fake(with_api=False)):
        code, report = judge(TREE_ROOT, EMPTY_MANIFEST)
    assert code == 2, report
    assert any("run_case" in n for n in report["notes"])


def test_broken_ledger_crosscheck_fails_closed(tmp_path):
    mp = write_manifest(tmp_path, [
        claim("honest-c", "C", 6, "WORKER_NONPROGRESS", "WORKER")])
    table = {("A", 6): ("ENVIRONMENT_BLOCKER", "ENVIRONMENT"),
             ("B", 7): ("SCHEDULER_STARVATION", "SCHEDULER"),
             ("C", 6): ("WORKER_NONPROGRESS", "WORKER")}
    with seeded_fake(make_fake(table=table, ledger_ok=False)):
        code, report = judge(TREE_ROOT, mp)
    assert code == 2, report


def test_corrupt_manifest_fails_closed(tmp_path):
    bad = str(tmp_path / "bad.json")
    with open(bad, "w", encoding="utf-8") as fh:
        fh.write("{not json")
    code, report = judge(TREE_ROOT, bad)
    assert code == 2, report
    assert report["canary"] == "ok"  # canary ran first, then manifest broke


def test_malformed_claim_unknown_case_fails_closed(tmp_path):
    mp = write_manifest(tmp_path, [
        claim("bad-case", "Z", 6, "WORKER_NONPROGRESS", "WORKER")])
    code, report = judge(TREE_ROOT, mp)
    assert code == 2, report

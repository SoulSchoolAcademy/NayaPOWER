"""Behavioral tests for the machine-enforced VERIFIED verdict gate.

These tests prove the seam the gate closes: an honest VERIFIED verdict must
be a computation against Pair C's 5-point bar (pair-c-scorer-verdict-20261009.md),
not a judgment. Every test feeds the REAL gate (tools/verified_verdict_gate)
and asserts the rule that fires.

Fail-closed behaviors under test:
  - VERIFIED happy path: 3 distinct unseen tasks, treatment parses AND
    control does not on every task, independent blind scorer -> VERIFIED
  - R1: empty claim / missing falsifiable / un-pre-registered -> NOT_VERIFIED
  - R2: no machine check -> NOT_VERIFIED (self-report-only cannot verify)
  - R3: machine check explodes on one artifact -> NOT_VERIFIED (unmeasured)
  - R4: scorer is also a doer -> NOT_VERIFIED (independence)
  - R4b: no scorer named -> NOT_VERIFIED
  - R5: null on one task (treatment fails to parse) -> NOT_VERIFIED,
    null recorded as a task row, never as support
  - R5b: control parses too (no delta) -> NOT_VERIFIED
  - R6: duplicate task arm pairing (two treatments, no control) -> NOT_VERIFIED
  - R6b: seen task reused (memorization) -> NOT_VERIFIED
  - R7: only 2 tasks (demonstration, not proof) -> NOT_VERIFIED
  - malformed request / malformed arm -> NOT_VERIFIED, never an exception
  - receipt digest: recomputes; tampered receipt fails verification
  - rule trace: every rule named with pass/fail and a detail string
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from verified_verdict_gate import (  # noqa: E402
    SCHEMA,
    Arm,
    VerdictRequest,
    provenance_block_check,
    verdict,
    verify_receipt,
)

SCORER = "scorer-seat-9"
DOER = "doer-seat-7"

CLAIM = "Preserving provenance before applying retained intelligence raises " \
        "the share of machine-parseable provenance blocks in capture artifacts."
FALSIFIABLE = "Treatment artifacts parse LESS often than control artifacts."
FAMILY = "capture-intelligence-record"
CRITERION = "artifact contains a machine-parseable provenance block " \
            "(source, timestamp, authority), checked by script"
PREREG = "2026-10-09T20:00:00Z"


def _prov_artifact(source="cap-001"):
    return json.dumps({
        "record": "intelligence note",
        "provenance": {
            "source": source,
            "timestamp": "2026-10-09T20:01:00Z",
            "authority": "capture-seat",
        },
    })


def _no_prov_artifact():
    return json.dumps({"record": "intelligence note"})  # no provenance block


def _arms(tasks, doer=DOER, treat_ok=True, control_ok=False):
    """Build paired arms for the named tasks. treat_ok=False makes the
    treatment artifact unparsable (a null); control_ok=True makes the
    control parse (no delta)."""
    arms = []
    for t in tasks:
        arms.append(Arm(task_name=t, lesson_provided=False,
                        artifact=_prov_artifact(t) if control_ok else _no_prov_artifact(),
                        doer_id=doer))
        arms.append(Arm(task_name=t, lesson_provided=True,
                        artifact=_prov_artifact(t) if treat_ok else _no_prov_artifact(),
                        doer_id=doer))
    return arms


def _request(arms, **kw):
    base = dict(claim=CLAIM, falsifiable=FALSIFIABLE, task_family=FAMILY,
                success_criterion=CRITERION, machine_check=provenance_block_check,
                arms=arms, scorer_id=SCORER, blind=True,
                preregistered_at=PREREG, seen_tasks=frozenset())
    base.update(kw)
    return VerdictRequest(**base)


def _rules(receipt):
    return {r["rule"]: r for r in receipt["rule_trace"]}


# ---------------------------------------------------------------------------
# VERIFIED happy path
# ---------------------------------------------------------------------------

def test_verified_happy_path():
    r = verdict(_request(_arms(["task-alpha", "task-beta", "task-gamma"])))
    assert r["schema"] == SCHEMA
    assert r["verdict"] == "VERIFIED"
    rules = _rules(r)
    assert all(rules[rid]["passed"] for rid in ("R1", "R2", "R3", "R4",
                                                "R5", "R6", "R7", "R8"))
    assert len(r["task_rows"]) == 3
    assert all(row["delta"] for row in r["task_rows"])
    assert r["scorer_id"] == SCORER
    assert verify_receipt(r), "receipt digest must recompute"


# ---------------------------------------------------------------------------
# R1: the contract must be complete and pre-registered
# ---------------------------------------------------------------------------

def test_r1_empty_claim_fails_closed():
    r = verdict(_request(_arms(["t1", "t2", "t3"]), claim=""))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R1"]["passed"]


def test_r1_missing_falsifiable_fails_closed():
    r = verdict(_request(_arms(["t1", "t2", "t3"]), falsifiable="  "))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R1"]["passed"]


def test_r1_unpreregistered_fails_closed():
    r = verdict(_request(_arms(["t1", "t2", "t3"]), preregistered_at=""))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R1"]["passed"]


def test_none_request_never_raises():
    r = verdict(None)
    assert r["verdict"] == "NOT_VERIFIED"


# ---------------------------------------------------------------------------
# R2: no machine check, no VERIFIED (self-report ritual fails)
# ---------------------------------------------------------------------------

def test_r2_no_machine_check_fails_closed():
    r = verdict(_request(_arms(["t1", "t2", "t3"]), machine_check=None))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R2"]["passed"]


# ---------------------------------------------------------------------------
# R3: the check must measure every arm
# ---------------------------------------------------------------------------

def test_r3_check_exploding_on_one_artifact_fails_closed():
    def boom(artifact):
        if "gamma" in artifact:
            raise RuntimeError("parser blew up")
        return provenance_block_check(artifact)

    arms = _arms(["task-alpha", "task-beta", "task-gamma"])
    r = verdict(_request(arms, machine_check=boom))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R3"]["passed"]


# ---------------------------------------------------------------------------
# R4: doer != scorer
# ---------------------------------------------------------------------------

def test_r4_scorer_also_doer_fails_closed():
    r = verdict(_request(_arms(["t1", "t2", "t3"]), scorer_id=DOER))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R4"]["passed"]


def test_r4_no_scorer_named_fails_closed():
    r = verdict(_request(_arms(["t1", "t2", "t3"]), scorer_id=""))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R4"]["passed"]


# ---------------------------------------------------------------------------
# R5: the delta or it did not happen; nulls recorded, never support
# ---------------------------------------------------------------------------

def test_r5_null_on_one_task_is_not_verified_but_recorded():
    arms = _arms(["task-alpha", "task-beta"]) + _arms(["task-null"], treat_ok=False)
    r = verdict(_request(arms))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R5"]["passed"]
    rows = {row["task"]: row for row in r["task_rows"]}
    assert rows["task-null"]["delta"] is False
    assert rows["task-null"]["treatment_parses"] is False
    # the null is a recorded row, not support: verdict stays NOT_VERIFIED
    assert len(r["task_rows"]) == 3


def test_r5b_control_parses_too_means_no_delta():
    r = verdict(_request(_arms(["t1", "t2", "t3"], control_ok=True)))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R5"]["passed"]


# ---------------------------------------------------------------------------
# R6: distinct, unseen tasks; exactly one control + one treatment each
# ---------------------------------------------------------------------------

def test_r6_two_treatments_no_control_fails_closed():
    arms = [
        Arm(task_name="t1", lesson_provided=False,
            artifact=_no_prov_artifact(), doer_id=DOER),
        Arm(task_name="t1", lesson_provided=True,
            artifact=_prov_artifact("t1"), doer_id=DOER),
        Arm(task_name="t1", lesson_provided=True,  # second treatment, no control slot
            artifact=_prov_artifact("t1"), doer_id=DOER),
        Arm(task_name="t2", lesson_provided=False,
            artifact=_no_prov_artifact(), doer_id=DOER),
        Arm(task_name="t2", lesson_provided=True,
            artifact=_prov_artifact("t2"), doer_id=DOER),
        Arm(task_name="t3", lesson_provided=False,
            artifact=_no_prov_artifact(), doer_id=DOER),
        Arm(task_name="t3", lesson_provided=True,
            artifact=_prov_artifact("t3"), doer_id=DOER),
    ]
    r = verdict(_request(arms))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R6"]["passed"]


def test_r6b_seen_task_reuse_is_memorization_not_learning():
    arms = _arms(["task-alpha", "task-beta", "task-gamma"])
    r = verdict(_request(arms, seen_tasks=frozenset({"task-beta"})))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R6"]["passed"]


# ---------------------------------------------------------------------------
# R7: replication >= 3 (a demonstration is not proof)
# ---------------------------------------------------------------------------

def test_r7_two_tasks_is_insufficient_replication():
    r = verdict(_request(_arms(["task-alpha", "task-beta"])))
    assert r["verdict"] == "NOT_VERIFIED"
    assert not _rules(r)["R7"]["passed"]


# ---------------------------------------------------------------------------
# Malformed input is unproven, never an exception
# ---------------------------------------------------------------------------

def test_malformed_arm_never_raises():
    arms = _arms(["t1", "t2", "t3"])
    arms[0] = Arm(task_name="", lesson_provided=True,
                  artifact=_prov_artifact(), doer_id=DOER)
    r = verdict(_request(arms))
    assert r["verdict"] == "NOT_VERIFIED"


# ---------------------------------------------------------------------------
# Receipt integrity: digest recomputes; tampering fails
# ---------------------------------------------------------------------------

def test_receipt_tamper_evident():
    r = verdict(_request(_arms(["t1", "t2", "t3"])))
    assert verify_receipt(r)
    tampered = dict(r)
    tampered_rows = [dict(row) for row in r["task_rows"]]
    tampered_rows[0]["delta"] = not tampered_rows[0]["delta"]  # flip one delta
    tampered["task_rows"] = tampered_rows
    assert not verify_receipt(tampered)


def test_rule_trace_names_every_rule_with_detail():
    r = verdict(_request(_arms(["t1", "t2", "t3"])))
    seen = {row["rule"] for row in r["rule_trace"]}
    for rid in ("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"):
        assert rid in seen, "rule %s missing from trace" % rid
    for row in r["rule_trace"]:
        assert isinstance(row["passed"], bool)
        assert isinstance(row["detail"], str) and row["detail"].strip()


def test_provenance_check_is_a_real_measurement_not_prose():
    # prose about provenance is not a provenance block
    assert provenance_block_check("the agent preserved provenance") is False
    assert provenance_block_check(_no_prov_artifact()) is False
    assert provenance_block_check(_prov_artifact("x")) is True
    assert provenance_block_check(b"\xff\xfe not json") is False

"""Tests for tools/production_readiness_checklist.py — the production readiness instrument.

Network-dependent checks (C1 fetch, C2, C3) are NOT unit-tested here; they are
exercised by the live run itself. These tests cover the pure logic: dispatch
contract, standing policy, migration hygiene, workflow references, receipt path,
and report scoring.
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import production_readiness_checklist as prc  # noqa: E402

GOOD_DISPATCH = """
on:
  workflow_dispatch:
    inputs:
      confirm:
        description: "Type DEPLOY to authorize"
        required: true
        type: string
      source_sha:
        description: "Exact 40-hex main SHA"
        required: true
        type: string
jobs:
  promote:
    steps:
      - run: |
          test "${{ inputs.confirm }}" = "DEPLOY"
          authorized_sha="${{ inputs.source_sha }}"
          if [ "${#authorized_sha}" -ne 40 ]; then exit 1; fi
          case "$authorized_sha" in *[!0-9a-f]*|"") exit 1;; esac
          if [ "$authorized_sha" != "$GITHUB_SHA" ]; then exit 1; fi
          # main moved check
          echo "FAIL CLOSED: main moved to $resolved_main"
      - uses: actions/upload-artifact@v4
        with:
          name: production-promotion-receipt
      - run: echo NAYAPOWER_PRODUCTION_PROMOTION_RECEIPT_V1
"""


# ---- C5 dispatch contract ----------------------------------------------------

def test_dispatch_contract_pass():
    r = prc.check_dispatch_contract(text=GOOD_DISPATCH)
    assert r["check"] == "C5"
    assert r["verdict"] == "PASS", r


def test_dispatch_contract_fail_on_missing_confirm():
    bad = GOOD_DISPATCH.replace("confirm:", "confirmation_input:")
    r = prc.check_dispatch_contract(text=bad)
    assert r["verdict"] == "FAIL"
    assert any("confirm" in m for m in r["evidence"]["missing"])


def test_dispatch_contract_fail_on_missing_sha_binding():
    bad = GOOD_DISPATCH.replace('"$authorized_sha" != "$GITHUB_SHA"', '"$x" != "$y"')
    r = prc.check_dispatch_contract(text=bad)
    assert r["verdict"] == "FAIL"


def test_dispatch_contract_live_workflow_passes():
    r = prc.check_dispatch_contract()  # reads the real repo file
    assert r["verdict"] == "PASS", r


# ---- C4 standing policy ------------------------------------------------------

def test_standing_policy_pass(tmp_path):
    p = tmp_path / "policy.json"
    p.write_text(json.dumps({"policy_id": "STANDING-PRODUCTION-PROMOTION-V1",
                             "status": "RATIFIED", "scope": {}}))
    r = prc.check_standing_policy(policy_path=p)
    assert r["verdict"] == "PASS", r


def test_standing_policy_fail_not_ratified(tmp_path):
    p = tmp_path / "policy.json"
    p.write_text(json.dumps({"policy_id": "STANDING-PRODUCTION-PROMOTION-V1",
                             "status": "DRAFT"}))
    r = prc.check_standing_policy(policy_path=p)
    assert r["verdict"] == "FAIL"


def test_standing_policy_fail_missing(tmp_path):
    r = prc.check_standing_policy(policy_path=tmp_path / "nope.json")
    assert r["verdict"] == "FAIL"


def test_standing_policy_live_repo_passes():
    r = prc.check_standing_policy()  # reads the real repo file
    assert r["verdict"] == "PASS", r


# ---- C6 migration hygiene ----------------------------------------------------

def _mig_dir(tmp_path, names):
    d = tmp_path / "migrations"
    d.mkdir()
    for n in names:
        (d / n).write_text("-- sql\n")
    return d


def test_migration_hygiene_clean(tmp_path):
    d = _mig_dir(tmp_path, ["20261001000000_a.sql", "20261002000000_b.sql"])
    ledger = tmp_path / "ledger.json"
    ledger.write_text(json.dumps({"pending": []}))
    r = prc.check_migration_hygiene(migrations_dir=d, ledger_path=ledger)
    assert r["verdict"] == "PASS", r
    assert r["evidence"]["migration_count"] == 2


def test_migration_hygiene_duplicate_timestamp(tmp_path):
    d = _mig_dir(tmp_path, ["20261001000000_a.sql", "20261001000000_b.sql"])
    r = prc.check_migration_hygiene(migrations_dir=d, ledger_path=tmp_path / "missing.json")
    assert r["verdict"] == "FAIL"
    assert any("duplicate" in p for p in r["evidence"]["problems"])


def test_migration_hygiene_bad_name(tmp_path):
    d = _mig_dir(tmp_path, ["not-a-migration.sql"])
    r = prc.check_migration_hygiene(migrations_dir=d, ledger_path=tmp_path / "missing.json")
    assert r["verdict"] == "FAIL"
    assert any("non-conforming" in p for p in r["evidence"]["problems"])


def test_migration_hygiene_missing_ledger_file(tmp_path):
    d = _mig_dir(tmp_path, ["20261001000000_a.sql"])
    ledger = tmp_path / "ledger.json"
    ledger.write_text(json.dumps({"pending": [{"path": "supabase/migrations/gone.sql",
                                               "version": "20261001000000"}]}))
    r = prc.check_migration_hygiene(migrations_dir=d, ledger_path=ledger)
    assert r["verdict"] == "FAIL"
    assert any("missing" in p for p in r["evidence"]["problems"])


def test_migration_hygiene_live_repo_passes():
    r = prc.check_migration_hygiene()  # reads the real repo tree
    assert r["verdict"] == "PASS", r
    assert r["evidence"]["migration_count"] >= 100


# ---- C7 / C8 ---------------------------------------------------------------

def test_proof_workflows_exist_pass(tmp_path):
    (tmp_path / "a.yml").write_text("x")
    (tmp_path / "b.yml").write_text("x")
    r = prc.check_proof_workflows_exist(text="uses: ./a.yml\nrun: b.yml", workflows_dir=tmp_path)
    assert r["verdict"] == "PASS", r


def test_proof_workflows_exist_fail(tmp_path):
    r = prc.check_proof_workflows_exist(text="uses: ./ghost.yml", workflows_dir=tmp_path)
    assert r["verdict"] == "FAIL"
    assert "ghost.yml" in r["evidence"]["missing"]


def test_proof_workflows_live_repo_passes():
    r = prc.check_proof_workflows_exist()
    assert r["verdict"] == "PASS", r


def test_receipt_path_pass():
    r = prc.check_receipt_path(text=GOOD_DISPATCH)
    assert r["verdict"] == "PASS", r


def test_receipt_path_warn():
    r = prc.check_receipt_path(text="no receipt here")
    assert r["verdict"] == "WARN"


def test_receipt_path_live_repo_passes():
    r = prc.check_receipt_path()
    assert r["verdict"] == "PASS", r


# ---- scoring -----------------------------------------------------------------

def _mk(verdict):
    return {"check": "CX", "verdict": verdict, "summary": "", "evidence": {}}


def test_score_ready():
    v, code = prc.score([_mk("PASS"), _mk("PASS")])
    assert (v, code) == ("READY", 0)


def test_score_warn_ok():
    v, code = prc.score([_mk("PASS"), _mk("WARN")])
    assert (v, code) == ("READY_WITH_WARNINGS", 0)


def test_score_unknown_ok():
    v, code = prc.score([_mk("PASS"), _mk("UNKNOWN")])
    assert (v, code) == ("READY_WITH_UNKNOWN", 0)


def test_score_fail():
    v, code = prc.score([_mk("PASS"), _mk("FAIL")])
    assert (v, code) == ("NOT_READY", 1)


def test_check_result_rejects_bad_verdict():
    with pytest.raises(AssertionError):
        prc.check_result("CX", "MAYBE", "nope")

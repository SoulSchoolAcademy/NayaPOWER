"""Tests for tools/production_readiness_checklist.py — the production readiness instrument.

Network-dependent checks (C1 fetch, C3) are NOT unit-tested here; they are
exercised by the live run itself. C2's git-protocol fallback IS unit-tested
below via faked gh_get/git (no real network). These tests cover the pure
logic: dispatch contract, standing policy, migration hygiene, workflow
references, receipt path, production-stamp fallback, and report scoring.
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


# ---- C3 required-CI attribution ------------------------------------------------

def test_required_ci_constant_matches_workflow_text():
    text = (Path(__file__).resolve().parents[1]
            / ".github/workflows/governed-supabase-production-deploy.yml").read_text()
    for wf in prc.REQUIRED_CI_WORKFLOWS:
        assert f'"{wf}"' in text, wf


def test_required_ci_status_shape(monkeypatch):
    def fake_gh(path):
        return {"workflow_runs": [
            {"id": 1, "head_sha": "a" * 40, "head_branch": "main",
             "event": "push", "status": "completed", "conclusion": "failure",
             "run_attempt": 1}]}
    monkeypatch.setattr(prc, "gh_get", fake_gh)
    out = prc.required_ci_status("a" * 40)
    assert set(out) == set(prc.REQUIRED_CI_WORKFLOWS)
    assert out["kernel-tests.yml"]["conclusion"] == "failure"


def test_required_ci_status_no_sha():
    assert prc.required_ci_status(None) == {}


def test_required_ci_status_includes_failed_jobs(monkeypatch):
    def fake_gh(path):
        if "/actions/runs/" in path:  # jobs endpoint for the failing kernel run
            return {"jobs": [{"name": "test", "conclusion": "failure",
                              "steps": [{"name": "Run python -m pytest -q",
                                         "conclusion": "failure"}]}]}
        if "kernel-tests.yml" in path:
            return {"workflow_runs": [
                {"id": 200, "head_sha": "b" * 40, "head_branch": "main",
                 "event": "push", "status": "completed", "conclusion": "failure",
                 "run_attempt": 1}]}
        return {"workflow_runs": [
            {"id": 201, "head_sha": "b" * 40, "head_branch": "main",
             "event": "push", "status": "completed", "conclusion": "success",
             "run_attempt": 1}]}
    monkeypatch.setattr(prc, "gh_get", fake_gh)
    out = prc.required_ci_status("b" * 40)
    assert out["kernel-tests.yml"]["failed_jobs"] == ["test"], out
    assert out["collective-chain-readiness-gate.yml"]["failed_jobs"] is None


def test_required_ci_status_failed_jobs_none_when_jobs_api_down(monkeypatch):
    def fake_gh(path):
        if "/actions/runs/" in path:
            return None
        return {"workflow_runs": [
            {"id": 200, "head_sha": "b" * 40, "head_branch": "main",
             "event": "push", "status": "completed", "conclusion": "failure",
             "run_attempt": 1}]}
    monkeypatch.setattr(prc, "gh_get", fake_gh)
    out = prc.required_ci_status("b" * 40)
    assert out["kernel-tests.yml"]["failed_jobs"] is None


# ---- C3 fail-closed classification ------------------------------------------------

def _ci(red=(), unknown=()):
    out = {}
    for wf in prc.REQUIRED_CI_WORKFLOWS:
        if wf in red:
            out[wf] = {"status": "completed", "conclusion": "failure",
                       "run_id": 1, "failed_jobs": ["test"]}
        elif wf in unknown:
            out[wf] = {"status": "unknown", "conclusion": None,
                       "reason": "no_api", "failed_jobs": None}
        else:
            out[wf] = {"status": "completed", "conclusion": "success",
                       "run_id": 2, "failed_jobs": None}
    return out


def _failures(n, steps):
    return [{"run_id": i, "failing_steps": list(steps)} for i in range(n)]


def _race_failures(n):
    return [{"run_id": 900 + i,
             "failing_steps": ["Resolve standing authorization mode"],
             "head_sha_full": "a" * 40}
            for i in range(n)]


def _patch_ancestor(monkeypatch, value):
    monkeypatch.setattr(prc, "_is_strict_ancestor_of_tip", lambda sha: value)


def test_classify_superseded_tip_race_pure(monkeypatch):
    _patch_ancestor(monkeypatch, True)
    r = prc.classify_promotion_failures(_race_failures(2), _ci(red=("kernel-tests.yml",)))
    assert r["classification"] == "SUPERSEDED_TIP_RACE", r
    assert r["superseded_tip_race"]["count"] == 2
    assert "failure receipt" in r["detail"]


def test_classify_fail_closed_with_race_mixed(monkeypatch):
    _patch_ancestor(monkeypatch, True)
    failures = (_failures(2, ["Enforce ratified standing policy before automatic promotion"])
                + _race_failures(1))
    r = prc.classify_promotion_failures(failures, _ci(red=("kernel-tests.yml",)))
    assert r["classification"] == "FAIL_CLOSED_BY_DESIGN", r
    assert r["policy_step_trips"] == 2
    assert r["superseded_tip_race"]["count"] == 1
    assert "superseded-tip race" in r["detail"]


def test_classify_race_not_claimed_when_not_ancestor(monkeypatch):
    _patch_ancestor(monkeypatch, False)
    r = prc.classify_promotion_failures(_race_failures(1), _ci(red=("kernel-tests.yml",)))
    assert r["classification"] == "NEEDS_INVESTIGATION", r
    assert r["superseded_tip_race"]["count"] == 0


def test_classify_race_not_claimed_when_ancestor_unknown(monkeypatch):
    _patch_ancestor(monkeypatch, None)
    r = prc.classify_promotion_failures(_race_failures(1), _ci(red=("kernel-tests.yml",)))
    assert r["classification"] == "NEEDS_INVESTIGATION", r


def test_classify_race_ignored_without_full_sha(monkeypatch):
    # A failure dict without head_sha_full can never be race-attributed:
    # the instrument records what it could actually read, never guesses.
    r = prc.classify_promotion_failures(
        _failures(1, ["Resolve standing authorization mode"]),
        _ci(red=("kernel-tests.yml",)))
    assert r["classification"] == "NEEDS_INVESTIGATION", r
    assert r["superseded_tip_race"]["count"] == 0


def test_is_strict_ancestor_of_tip_rejects_shallow(monkeypatch):
    monkeypatch.setattr(prc, "git", lambda args: "true" if args[:2] == ["rev-parse", "--is-shallow-repository"] else "x" * 40)
    assert prc._is_strict_ancestor_of_tip("a" * 40) is None


def test_is_strict_ancestor_of_tip_rejects_bad_sha():
    assert prc._is_strict_ancestor_of_tip("not-a-sha") is None
    assert prc._is_strict_ancestor_of_tip("") is None


def test_classify_fail_closed_by_design():
    r = prc.classify_promotion_failures(
        _failures(3, ["Enforce ratified standing policy before automatic promotion"]),
        _ci(red=("kernel-tests.yml",)))
    assert r["classification"] == "FAIL_CLOSED_BY_DESIGN", r
    assert r["policy_step_trips"] == 3
    assert "kernel-tests.yml" in r["detail"]


def test_classify_needs_investigation_when_step_unexplained():
    r = prc.classify_promotion_failures(
        _failures(2, ["Some other step broke"]),
        _ci(red=("kernel-tests.yml",)))
    assert r["classification"] == "NEEDS_INVESTIGATION", r


def test_classify_needs_investigation_when_ci_green():
    r = prc.classify_promotion_failures(
        _failures(1, ["Enforce ratified standing policy before automatic promotion"]),
        _ci())
    assert r["classification"] == "NEEDS_INVESTIGATION", r


def test_classify_unknown_when_ci_unreadable():
    r = prc.classify_promotion_failures(
        _failures(1, ["Enforce ratified standing policy before automatic promotion"]),
        _ci(unknown=("kernel-tests.yml", "collective-chain-readiness-gate.yml")))
    assert r["classification"] == "UNKNOWN", r


def test_check_workflow_health_carries_classification(monkeypatch):
    head = "c" * 40

    def fake_gh(path):
        if "governed-supabase-production-deploy.yml/runs" in path:
            return {"workflow_runs": [
                {"id": 100, "event": "push", "head_sha": head,
                 "conclusion": "failure", "created_at": "2026-10-08T15:27:40Z"}]}
        if "/actions/runs/100/jobs" in path:
            return {"jobs": [{"name": "promote", "conclusion": "failure",
                              "steps": [{"name": "Enforce ratified standing policy "
                                                 "before automatic promotion",
                                         "conclusion": "failure"}]}]}
        if "/actions/runs/200/jobs" in path:
            return {"jobs": [{"name": "test", "conclusion": "failure",
                              "steps": [{"name": "Run python -m pytest -q",
                                         "conclusion": "failure"}]}]}
        if "kernel-tests.yml" in path:
            return {"workflow_runs": [
                {"id": 200, "head_sha": head, "head_branch": "main",
                 "event": "push", "status": "completed", "conclusion": "failure",
                 "run_attempt": 1}]}
        return {"workflow_runs": [
            {"id": 201, "head_sha": head, "head_branch": "main",
             "event": "push", "status": "completed", "conclusion": "success",
             "run_attempt": 1}]}

    monkeypatch.setattr(prc, "gh_get", fake_gh)
    r = prc.check_workflow_health(recent=1)
    assert r["check"] == "C3"
    assert r["verdict"] == "FAIL", r
    cls = r["evidence"]["promotion_failure_classification"]
    assert cls["classification"] == "FAIL_CLOSED_BY_DESIGN", cls
    assert "FAIL_CLOSED_BY_DESIGN" in r["summary"]
    assert r["evidence"]["required_ci_at_latest_tip"]["kernel-tests.yml"]["failed_jobs"] == ["test"]


# ---- C9 branch hygiene ---------------------------------------------------------

def _prs(n, start=1800, age_days=1):
    from datetime import datetime, timedelta, timezone
    base = datetime.now(timezone.utc) - timedelta(days=age_days)
    return [{"number": start + i,
             "created_at": (base - timedelta(hours=i)).isoformat()} for i in range(n)]


def _gh_for(open_prs, dirty=(), merged=()):
    def fake_gh(path):
        if "state=open" in path:
            return open_prs
        if "state=closed" in path:
            return [{"number": 900 + i, "merged_at": m} for i, m in enumerate(merged)]
        num = int(path.rsplit("/", 1)[-1])
        return {"mergeable_state": "dirty" if num in dirty else "clean"}
    return fake_gh


def _recent_iso(hours_ago):
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc) - timedelta(hours=hours_ago)).isoformat()


def test_branch_hygiene_clean(monkeypatch):
    monkeypatch.setattr(prc, "gh_get",
                        _gh_for(_prs(10), merged=[_recent_iso(2)] * 30))
    r = prc.check_branch_hygiene()
    assert r["check"] == "C9"
    assert r["verdict"] == "PASS", r


def test_branch_hygiene_warn_on_dirty(monkeypatch):
    prs = _prs(5)
    monkeypatch.setattr(prc, "gh_get",
                        _gh_for(prs, dirty={prs[0]["number"]},
                                merged=[_recent_iso(2)] * 30))
    r = prc.check_branch_hygiene()
    assert r["verdict"] == "WARN", r
    assert prs[0]["number"] in r["evidence"]["dirty_prs"]


def test_branch_hygiene_warn_on_ancient(monkeypatch):
    monkeypatch.setattr(prc, "gh_get",
                        _gh_for(_prs(5, age_days=20), merged=[_recent_iso(2)] * 30))
    r = prc.check_branch_hygiene()
    assert r["verdict"] == "WARN", r
    assert r["evidence"]["ancient_prs_over_14d"]


def test_branch_hygiene_warn_on_pileup(monkeypatch):
    # 100 open vs 10 merged/day: pile > 3x velocity -> WARN, never FAIL.
    monkeypatch.setattr(prc, "gh_get",
                        _gh_for(_prs(100), merged=[_recent_iso(2)] * 10))
    r = prc.check_branch_hygiene()
    assert r["verdict"] == "WARN", r


def test_branch_hygiene_never_fails(monkeypatch):
    monkeypatch.setattr(prc, "gh_get",
                        _gh_for(_prs(200, age_days=60), dirty={1800},
                                merged=[]))
    r = prc.check_branch_hygiene()
    assert r["verdict"] in ("PASS", "WARN", "UNKNOWN"), r


def test_branch_hygiene_unknown_when_no_api(monkeypatch):
    monkeypatch.setattr(prc, "gh_get", lambda path: None)
    assert prc.check_branch_hygiene()["verdict"] == "UNKNOWN"


# ---- main() --json -------------------------------------------------------------

def test_main_json_flag_emits_pure_json(monkeypatch, capsys):
    report = {"schema": prc.SCHEMA, "verdict": "READY",
              "checks": [], "summary": {"PASS": 0, "WARN": 0, "FAIL": 0, "UNKNOWN": 0}}
    monkeypatch.setattr(prc, "run", lambda: (report, 0))
    code = prc.main(["--json"])
    out = capsys.readouterr().out
    assert code == 0
    assert json.loads(out)["verdict"] == "READY"  # pure JSON, no trailing text


# ---- C2 production stamp (REST-first, git-protocol fallback) -------------------

_STAMP_MSG = ("deploy: stamp Naya runtime source "
              "00f50bb32c1c7fadfbe5cd03d0319646ab9dc0e9")
_PROD_SHA = "acf57082f5c4ece46ac27ba04919073dbe02e396"
_TIP_SHA = "7281ede6b07869f64e576d4d6432628c4750d5de"
_STAMPED_SRC = "00f50bb32c1c7fadfbe5cd03d0319646ab9dc0e9"


def _git_ok(monkeypatch, stamp_msg=_STAMP_MSG):
    responses = {
        ("ls-remote", "origin", "refs/heads/production"):
            f"{_PROD_SHA}\trefs/heads/production",
        ("fetch", "origin", "production", "--quiet"): "",
        ("rev-parse", "origin/production"): _PROD_SHA,
        ("log", "-1", "--format=%B", _PROD_SHA): stamp_msg,
        ("rev-parse", "--is-shallow-repository"): "true",
    }
    monkeypatch.setattr(prc, "gh_get", lambda path: None)
    monkeypatch.setattr(prc, "git", lambda args: responses.get(tuple(args)))


def test_production_stamp_prefers_rest_api(monkeypatch):
    monkeypatch.setattr(prc, "gh_get", lambda path: {
        "commit": {"sha": _PROD_SHA,
                   "commit": {"message": _STAMP_MSG.replace(_STAMPED_SRC, _TIP_SHA)}}})
    r = prc.check_production_stamp(_TIP_SHA)
    assert r["check"] == "C2"
    assert r["verdict"] == "PASS", r
    assert r["evidence"]["source"] == "rest-api"


def test_production_stamp_git_fallback_warn_on_drift(monkeypatch):
    _git_ok(monkeypatch)  # API down; stamp names an older source SHA
    r = prc.check_production_stamp(_TIP_SHA)
    assert r["verdict"] == "WARN", r
    assert r["evidence"]["source"] == "git-protocol-fallback"
    assert r["evidence"]["stamped_source_sha"] == _STAMPED_SRC
    assert r["evidence"]["production_tip"] == _PROD_SHA
    assert r["evidence"]["shallow_clone"] is True  # no ancestry claimed


def test_production_stamp_git_fallback_pass_when_current(monkeypatch):
    _git_ok(monkeypatch,
            stamp_msg=f"deploy: stamp Naya runtime source {_TIP_SHA}")
    r = prc.check_production_stamp(_TIP_SHA)
    assert r["verdict"] == "PASS", r
    assert r["evidence"]["source"] == "git-protocol-fallback"


def test_production_stamp_git_fallback_warn_when_not_a_stamp(monkeypatch):
    _git_ok(monkeypatch, stamp_msg="routine merge, no stamp here")
    r = prc.check_production_stamp(_TIP_SHA)
    assert r["verdict"] == "WARN", r
    assert r["evidence"]["stamped_source_sha"] is None


def test_production_stamp_unknown_when_both_paths_fail(monkeypatch):
    monkeypatch.setattr(prc, "gh_get", lambda path: None)
    monkeypatch.setattr(prc, "git", lambda args: None)
    r = prc.check_production_stamp(_TIP_SHA)
    assert r["verdict"] == "UNKNOWN", r
    assert r["evidence"]["reason"] == "no_api_no_git"


def test_production_stamp_unknown_without_tip():
    r = prc.check_production_stamp(None)
    assert r["verdict"] == "UNKNOWN"

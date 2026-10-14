"""Tests for the readiness instrument's API economy: --local-only + call counter.

Every REST call spends from a monthly budget. These tests prove the instrument
can never silently blow the budget again (the 2026-10-14 09:50Z run spent
~28-29 calls): --local-only makes zero calls, and --max-api-calls caps the
run, with skipped API checks reporting UNKNOWN explicitly.

Hermetic: no test here touches the network. gh_get is monkeypatched or the
local-only path is taken before any call is made.
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import production_readiness_checklist as prc  # noqa: E402


# Budget-state reset lives in tests/conftest.py (autouse, whole suite).


def test_local_only_skips_api_checks_with_zero_calls():
    prc._LOCAL_ONLY = True
    for check in (prc.check_production_stamp("0" * 40),
                  prc.check_workflow_health(),
                  prc.check_branch_hygiene()):
        assert check["verdict"] == "UNKNOWN", check
        assert check["evidence"]["reason"] == "local_only", check
        assert "--local-only" in check["summary"], check
    assert prc._api_call_count == 0


def test_local_only_wins_over_a_working_credential(monkeypatch):
    # Even when gh_get would succeed, --local-only must not call it.
    monkeypatch.setattr(prc, "gh_get", lambda path: (_ for _ in ()).throw(
        AssertionError("gh_get must not be called in local-only mode")))
    prc._LOCAL_ONLY = True
    with pytest.raises(prc._ApiSkipped):
        prc._api_get("/repos/x")
    assert prc._api_call_count == 0


def test_api_budget_cap_reports_unknown_instead_of_spending():
    prc._MAX_API_CALLS = 0
    check = prc.check_production_stamp("0" * 40)
    assert check["verdict"] == "UNKNOWN", check
    assert check["evidence"]["reason"] == "api_budget_exhausted", check
    assert "0/0" in check["summary"], check
    assert prc._api_call_count == 0


def test_api_get_counts_every_call_and_then_raises(monkeypatch):
    seen = []
    monkeypatch.setattr(prc, "gh_get", lambda path: seen.append(path) or {"ok": True})
    prc._MAX_API_CALLS = 2
    prc._api_get("/x/1")
    prc._api_get("/x/2")
    assert prc._api_call_count == 2
    assert seen == ["/x/1", "/x/2"]
    with pytest.raises(prc._ApiSkipped) as exc:
        prc._api_get("/x/3")
    assert "budget exhausted" in exc.value.reason
    assert prc._api_call_count == 2  # the refused call is not counted


def test_budget_exhaustion_mid_check_yields_unknown(monkeypatch):
    # C9 pages PRs then scans per-PR detail: with budget 2 the page fetch
    # succeeds, the first detail fetch trips the cap, and C9 must report
    # UNKNOWN (budget) rather than erroring or spending silently.
    def fake_gh(path):
        if "pulls?state=open" in path:
            return [{"number": 1, "created_at": "2026-10-01T00:00:00Z"}]
        return {"mergeable_state": "clean"}

    monkeypatch.setattr(prc, "gh_get", fake_gh)
    prc._MAX_API_CALLS = 2
    check = prc.check_branch_hygiene()
    assert check["verdict"] == "UNKNOWN", check
    assert check["evidence"]["reason"] == "api_budget_exhausted", check
    assert prc._api_call_count == 2


def test_main_local_only_json_reports_zero_api_calls(capsys):
    code = prc.main(["--local-only", "--json"])
    report = json.loads(capsys.readouterr().out)
    assert report["api_calls"] == 0
    assert report["local_only"] is True
    by_id = {c["check"]: c for c in report["checks"]}
    for cid in ("C2", "C3", "C9"):
        assert by_id[cid]["verdict"] == "UNKNOWN", by_id[cid]
        assert by_id[cid]["evidence"]["reason"] == "local_only"
    # Local checks still ran (PASS/WARN/FAIL allowed); only the API verdicts
    # are asserted here. C1 may FAIL in a network-less test env — not our claim.
    assert code in (0, 1)


def test_main_max_api_calls_flag_caps_the_run(capsys, monkeypatch):
    stamp = "deploy: stamp Naya runtime source " + "0" * 40
    monkeypatch.setattr(
        prc, "gh_get",
        lambda path: {"commit": {"sha": "a" * 40, "commit": {"message": stamp}}})
    code = prc.main(["--max-api-calls", "1", "--json"])
    report = json.loads(capsys.readouterr().out)
    assert report["api_calls"] == 1  # C2 consumed the single budgeted call
    by_id = {c["check"]: c for c in report["checks"]}
    assert by_id["C3"]["verdict"] == "UNKNOWN"
    assert by_id["C3"]["evidence"]["reason"] == "api_budget_exhausted"
    assert by_id["C9"]["verdict"] == "UNKNOWN"
    assert code in (0, 1)


def test_main_max_api_calls_rejects_non_integer(capsys):
    code = prc.main(["--max-api-calls", "many"])
    assert code == 2
    assert json.loads(capsys.readouterr().out)["verdict"] == "INSTRUMENT_ERROR"

"""Adversarial battery for tools/generate_organ_health_matrix.py.

Proves the generator's fail-closed invariants under hostile or degraded
evidence, per build item health-matrix-tests:

  A. missing evidence -> UNKNOWN, never PASS (no evidence of success is not
     success);
  B. failing required CI caps rungs — and only the required checks cap;
     non-success conclusions that are not failures are UNKNOWN, not a
     manufactured "capped" claim;
  C. stale stamped SHA refuses in live mode without --allow-stale;
  D. no manufactured tenths — rungs are discrete, evidence statuses come
     from the fixed enum, no numeric scores anywhere;
  E. refusal battery — canonical-file drift/absence, malformed SHA, an
     undeterminable stamp;
  F. UNIT coverage rules — exact token matching (no substring hits), the
     operator coverage escape hatch, ref truncation.

Companion: tests/test_organ_health_matrix_generator.py (8 smoke tests).

Two generator behaviors hardened by this battery (fixed on this branch):
  - a required unit check that is present but neither success nor a failure
    conclusion (e.g. "skipped") previously marked UNIT CAPPED_BY_CI,
    manufacturing a cap that did not exist; now UNKNOWN, consistent with the
    INTEGRATION branch and spec "missing evidence -> UNKNOWN";
  - live mode fetched check-runs at the API default page size (30); now
    per_page=100 so evidence cannot be silently truncated off the first page.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import generate_organ_health_matrix as gen  # noqa: E402

ORGANS = ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]
RUNGS = ["STRUCTURAL", "CONTRACT", "UNIT", "INTEGRATION",
         "BEHAVIORAL", "OUTCOME", "PRODUCTION", "SUCCESSOR"]
STATUSES = ["PROVEN", "UNKNOWN", "UNKNOWN_NOT_DISPATCHED",
            "UNKNOWN_NOT_QUALIFIED", "CAPPED_BY_CI"]
SHA = "507d34213333a38708912d343537985e619938ac"
OTHER_SHA = "0" * 40

REGISTRY = ROOT / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json"
CONTRACT = ROOT / "BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json"
SCHEMA = ROOT / "BRAIN/03-KERNEL/SCHEMA/ORGAN-HEALTH-MATRIX-SCHEMA.json"

GREEN = [
    {"name": "kernel-tests", "conclusion": "success", "id": 1},
    {"name": "chain-readiness-gate", "conclusion": "success", "id": 2},
    {"name": "current-truth-resolver", "conclusion": "success", "id": 3},
]


@pytest.fixture()
def repo_root(tmp_path):
    dest = tmp_path / "repo" / "BRAIN" / "03-KERNEL"
    (dest / "SCHEMA").mkdir(parents=True)
    shutil.copy(REGISTRY, dest / REGISTRY.name)
    shutil.copy(CONTRACT, dest / CONTRACT.name)
    shutil.copy(SCHEMA, dest / "SCHEMA" / SCHEMA.name)
    return tmp_path / "repo"


def _fixture(path, payload):
    Path(path).write_text(json.dumps(payload), encoding="utf-8")


def _run(repo_root, tmp_path, checks=None, runs=None, paths=None,
         unit_coverage=None, acceptance=None, prod_receipt=None,
         cont_receipt=None, sha=SHA, extra_args=()):
    checks = GREEN if checks is None else checks
    _fixture(tmp_path / "checks.json", {"check_runs": checks})
    _fixture(tmp_path / "runs.json", {"workflow_runs": runs or []})
    _fixture(tmp_path / "tree.json", {"paths": paths or []})
    if unit_coverage is not None:
        _fixture(tmp_path / "unit.json", unit_coverage)
    if acceptance is not None:
        _fixture(tmp_path / "acc.json", acceptance)
    if prod_receipt is not None:
        _fixture(tmp_path / "prod.json", prod_receipt)
    if cont_receipt is not None:
        _fixture(tmp_path / "cont.json", cont_receipt)
    out = tmp_path / "matrix.json"
    argv = ["--repo", str(repo_root), "--sha", sha,
            "--out", str(out), "--evaluator", "adversarial-test",
            "--check-runs", str(tmp_path / "checks.json"),
            "--workflow-runs", str(tmp_path / "runs.json"),
            "--tree-paths", str(tmp_path / "tree.json")]
    if unit_coverage is not None:
        argv += ["--unit-coverage", str(tmp_path / "unit.json")]
    if acceptance is not None:
        argv += ["--acceptance-records", str(tmp_path / "acc.json")]
    if prod_receipt is not None:
        argv += ["--production-receipt", str(tmp_path / "prod.json")]
    if cont_receipt is not None:
        argv += ["--continuity-receipt", str(tmp_path / "cont.json")]
    argv += list(extra_args)
    rc = gen.main(argv)
    assert rc == 0, f"generator refused unexpectedly (rc={rc})"
    return json.loads(out.read_text(encoding="utf-8"))


def _rung(matrix, organ, rung):
    o = next(x for x in matrix["organs"] if x["organ"] == organ)
    return next(e for e in o["rung_evidence"] if e["rung"] == rung)


def _organ(matrix, organ):
    return next(x for x in matrix["organs"] if x["organ"] == organ)


# ---------------------------------------------------------------------------
# A. missing evidence -> UNKNOWN, never PASS
# ---------------------------------------------------------------------------

def test_zero_evidence_every_organ_stuck_at_contract(repo_root, tmp_path):
    m = _run(repo_root, tmp_path, checks=[], runs=[], paths=[])
    assert m["ci_state_at_stamp"] == {
        "kernel-tests": "absent",
        "chain-readiness-gate": "absent",
        "current-truth-resolver": "absent",
    }
    assert m["gate_coverage"] == []
    for o in m["organs"]:
        assert o["current_rung"] == "CONTRACT", o["organ"]
        ev = {e["rung"]: e["status"] for e in o["rung_evidence"]}
        assert ev["STRUCTURAL"] == "PROVEN" and ev["CONTRACT"] == "PROVEN"
        assert ev["UNIT"] == "UNKNOWN", o["organ"]
        assert ev["INTEGRATION"] == "UNKNOWN", o["organ"]
        assert ev["BEHAVIORAL"] == "UNKNOWN", o["organ"]
        assert ev["OUTCOME"] == "UNKNOWN", o["organ"]
        assert ev["PRODUCTION"] == "UNKNOWN_NOT_DISPATCHED", o["organ"]
        assert ev["SUCCESSOR"] == "UNKNOWN_NOT_QUALIFIED", o["organ"]
        assert o["missing_rung"] == "UNIT"
        assert "kernel-tests" in o["next_proof"]


def test_green_ci_but_no_organ_tests_anywhere_unit_unknown_all(repo_root, tmp_path):
    m = _run(repo_root, tmp_path, paths=["tests/test_something_else.py"])
    for o in m["organs"]:
        assert _rung(m, o["organ"], "UNIT")["status"] == "UNKNOWN", o["organ"]


def test_verification_without_acceptance_records_is_unknown(repo_root, tmp_path):
    checks = GREEN + [{"name": "independent-verification", "conclusion": "success", "id": 7}]
    m = _run(repo_root, tmp_path, checks=checks)
    for o in m["organs"]:
        assert _rung(m, o["organ"], "OUTCOME")["status"] == "UNKNOWN", o["organ"]


def test_acceptance_records_without_verification_check_is_unknown(repo_root, tmp_path):
    m = _run(repo_root, tmp_path,
             acceptance={"KNOW": ["verify:acceptance/know-001"]})
    assert _rung(m, "KNOW", "OUTCOME")["status"] == "UNKNOWN"


def test_live_proof_run_on_wrong_sha_not_behavioral(repo_root, tmp_path):
    runs = [{"name": "live-know-proof", "conclusion": "success", "id": 5,
             "head_sha": OTHER_SHA, "head_branch": "main"}]
    m = _run(repo_root, tmp_path, runs=runs)
    assert _rung(m, "KNOW", "BEHAVIORAL")["status"] == "UNKNOWN"


def test_live_proof_run_off_main_not_behavioral(repo_root, tmp_path):
    runs = [{"name": "live-know-proof", "conclusion": "success", "id": 5,
             "head_sha": SHA, "head_branch": "feature/x"}]
    m = _run(repo_root, tmp_path, runs=runs)
    assert _rung(m, "KNOW", "BEHAVIORAL")["status"] == "UNKNOWN"


def test_live_proof_run_failed_not_behavioral(repo_root, tmp_path):
    runs = [{"name": "live-know-proof", "conclusion": "failure", "id": 5,
             "head_sha": SHA, "head_branch": "main"}]
    m = _run(repo_root, tmp_path, runs=runs)
    assert _rung(m, "KNOW", "BEHAVIORAL")["status"] == "UNKNOWN"


def test_proof_name_missing_live_token_matches_no_organ(repo_root, tmp_path):
    runs = [{"name": "know-proof-run", "conclusion": "success", "id": 5,
             "head_sha": SHA, "head_branch": "main"}]
    m = _run(repo_root, tmp_path, runs=runs)
    for o in m["organs"]:
        assert _rung(m, o["organ"], "BEHAVIORAL")["status"] == "UNKNOWN", o["organ"]


def test_proof_name_missing_organ_token_matches_no_organ(repo_root, tmp_path):
    runs = [{"name": "live-proof-run", "conclusion": "success", "id": 5,
             "head_sha": SHA, "head_branch": "main"}]
    m = _run(repo_root, tmp_path, runs=runs)
    for o in m["organs"]:
        assert _rung(m, o["organ"], "BEHAVIORAL")["status"] == "UNKNOWN", o["organ"]


def test_first_exact_check_match_wins(repo_root, tmp_path):
    # List order decides: document the contract explicitly.
    fail_first = ([{"name": "kernel-tests", "conclusion": "failure", "id": 9},
                   {"name": "kernel-tests", "conclusion": "success", "id": 10}]
                  + GREEN[1:])
    m = _run(repo_root, tmp_path, checks=fail_first)
    for o in m["organs"]:
        assert o["current_rung"] == "CONTRACT", o["organ"]
    success_first = ([{"name": "kernel-tests", "conclusion": "success", "id": 10},
                      {"name": "kernel-tests", "conclusion": "failure", "id": 9}]
                     + GREEN[1:])
    m = _run(repo_root, tmp_path, checks=success_first)
    for o in m["organs"]:
        # No cap; but no organ-scoped tests in the fixture tree either, so
        # UNIT is the first gap and the claim stops at CONTRACT (prefix rule).
        assert o["current_rung"] == "CONTRACT", o["organ"]
        assert o["missing_rung"] == "UNIT", o["organ"]


# ---------------------------------------------------------------------------
# B. failing required CI caps rungs — and only required checks cap
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("conclusion", ["cancelled", "timed_out", "action_required"])
def test_bad_conclusions_on_truth_check_cap_everything(repo_root, tmp_path, conclusion):
    checks = [GREEN[0], GREEN[1],
              {"name": "current-truth-resolver", "conclusion": conclusion, "id": 8}]
    m = _run(repo_root, tmp_path, checks=checks)
    for o in m["organs"]:
        assert o["current_rung"] == "CONTRACT", o["organ"]
        above = [e for e in o["rung_evidence"] if e["rung"] not in ("STRUCTURAL", "CONTRACT")]
        assert all(e["status"] == "CAPPED_BY_CI" for e in above), o["organ"]
        refs = _rung(m, o["organ"], "UNIT")["refs"]
        assert any("current-truth-resolver" in r and conclusion in r for r in refs)


def test_non_required_check_failure_does_not_cap(repo_root, tmp_path):
    # Cloudflare Workers Builds fails on main today (pre-existing, frontend):
    # it must never drag the nine organs down with it.
    checks = GREEN + [{"name": "Cloudflare Workers Builds", "conclusion": "failure", "id": 42}]
    m = _run(repo_root, tmp_path, checks=checks,
             paths=["tests/test_know_retrieval.py"])
    know = _organ(m, "KNOW")
    assert know["current_rung"] == "INTEGRATION"
    assert _rung(m, "KNOW", "UNIT")["status"] == "PROVEN"
    assert _rung(m, "KNOW", "INTEGRATION")["status"] == "PROVEN"


def test_skipped_unit_check_is_unknown_not_a_manufactured_cap(repo_root, tmp_path):
    checks = ([{"name": "kernel-tests", "conclusion": "skipped", "id": 11}]
              + GREEN[1:])
    m = _run(repo_root, tmp_path, checks=checks)
    for o in m["organs"]:
        # No cap in force; a skipped check is missing evidence of success,
        # not a failure. INTEGRATION's branch already answered UNKNOWN here.
        assert _rung(m, o["organ"], "UNIT")["status"] == "UNKNOWN", o["organ"]
        assert _rung(m, o["organ"], "INTEGRATION")["status"] == "PROVEN", o["organ"]
        # ...but the claim is a prefix, so the UNIT gap stops it at CONTRACT.
        assert o["current_rung"] == "CONTRACT", o["organ"]
        assert o["missing_rung"] == "UNIT", o["organ"]


def test_pending_integration_check_is_unknown(repo_root, tmp_path):
    checks = [GREEN[0],
              {"name": "chain-readiness-gate", "conclusion": "in_progress", "id": 12},
              GREEN[2]]
    m = _run(repo_root, tmp_path, checks=checks)
    for o in m["organs"]:
        assert _rung(m, o["organ"], "INTEGRATION")["status"] == "UNKNOWN", o["organ"]


def test_ci_cap_overrides_a_valid_production_receipt(repo_root, tmp_path):
    checks = ([{"name": "kernel-tests", "conclusion": "failure", "id": 9}]
              + GREEN[1:])
    m = _run(repo_root, tmp_path, checks=checks,
             prod_receipt={"promotion_run_id": 777, "dispatched_by": "shawn",
                           "migration_receipts": ["m1", "m2"]})
    for o in m["organs"]:
        assert _rung(m, o["organ"], "PRODUCTION")["status"] == "CAPPED_BY_CI", o["organ"]


def test_alias_must_be_exact_not_substring(repo_root, tmp_path):
    # "kernel-tests-nightly-extra" normalizes to "kerneltestsnightlyextra":
    # not an exact alias -> the unit check is absent -> UNKNOWN, never PASS.
    checks = ([{"name": "kernel-tests-nightly-extra", "conclusion": "success", "id": 13}]
              + GREEN[1:])
    m = _run(repo_root, tmp_path, checks=checks)
    assert m["ci_state_at_stamp"]["kernel-tests"] == "absent"
    for o in m["organs"]:
        assert _rung(m, o["organ"], "UNIT")["status"] == "UNKNOWN", o["organ"]


def test_plural_test_name_does_not_match_test_alias(repo_root, tmp_path):
    checks = ([{"name": "tests", "conclusion": "success", "id": 14}] + GREEN[1:])
    m = _run(repo_root, tmp_path, checks=checks)
    assert m["ci_state_at_stamp"]["kernel-tests"] == "absent"


def test_alias_match_records_actual_check_name_and_id(repo_root, tmp_path):
    # Auditability: the matched ACTUAL name+id land in refs and gate_coverage.
    checks = [GREEN[0],
              {"name": "chain-gate", "conclusion": "success", "id": 22},
              GREEN[2]]
    m = _run(repo_root, tmp_path, checks=checks)
    assert m["ci_state_at_stamp"]["chain-gate"] == "success"
    # One coverage record per organ evaluated (identical content).
    assert len(m["gate_coverage"]) == 9
    for g in m["gate_coverage"]:
        assert g == {"gate": "chain-gate", "check_run_id": 22, "covers": ORGANS}
    refs = _rung(m, "KNOW", "INTEGRATION")["refs"]
    assert any("22:chain-gate=success" in r for r in refs)


# ---------------------------------------------------------------------------
# C. stale stamped SHA refuses in live mode
# ---------------------------------------------------------------------------

def _live_out(repo_root, tmp_path):
    return tmp_path / "live-matrix.json"


def test_live_stale_stamp_refuses(repo_root, tmp_path, capsys, monkeypatch):
    def fake(gh_api, method, path):
        if "git/refs/heads/main" in path:
            return {"object": {"sha": OTHER_SHA}}
        raise AssertionError(f"must not fetch evidence on stale stamp: {path}")

    monkeypatch.setattr(gen, "_run_gh", fake)
    rc = gen.main(["--repo", str(repo_root), "--sha", SHA,
                   "--out", str(_live_out(repo_root, tmp_path)),
                   "--live", "--gh-api", "/nonexistent-gh-api"])
    assert rc == 2
    assert "stale stamp" in capsys.readouterr().err


def test_live_stale_stamp_allowed_marks_matrix(repo_root, tmp_path, monkeypatch):
    seen = []

    def fake(gh_api, method, path):
        seen.append(path)
        if "git/refs/heads/main" in path:
            return {"object": {"sha": OTHER_SHA}}
        if "check-runs" in path:
            return {"check_runs": GREEN}
        if "actions/runs" in path:
            return {"workflow_runs": []}
        if "git/trees" in path:
            return {"tree": []}
        raise AssertionError(path)

    monkeypatch.setattr(gen, "_run_gh", fake)
    out = _live_out(repo_root, tmp_path)
    rc = gen.main(["--repo", str(repo_root), "--sha", SHA, "--out", str(out),
                   "--live", "--gh-api", "/nonexistent-gh-api", "--allow-stale"])
    assert rc == 0
    m = json.loads(out.read_text(encoding="utf-8"))
    assert m["stale_stamp"] is True
    # Evidence must not be silently truncated off the first page.
    assert any("per_page=100" in p and "check-runs" in p for p in seen), seen


def test_live_fresh_stamp_marks_not_stale(repo_root, tmp_path, monkeypatch):
    def fake(gh_api, method, path):
        if "git/refs/heads/main" in path:
            return {"object": {"sha": SHA}}
        if "check-runs" in path:
            return {"check_runs": GREEN}
        if "actions/runs" in path:
            return {"workflow_runs": []}
        if "git/trees" in path:
            return {"tree": []}
        raise AssertionError(path)

    monkeypatch.setattr(gen, "_run_gh", fake)
    out = _live_out(repo_root, tmp_path)
    rc = gen.main(["--repo", str(repo_root), "--sha", SHA, "--out", str(out),
                   "--live", "--gh-api", "/nonexistent-gh-api"])
    assert rc == 0
    assert json.loads(out.read_text(encoding="utf-8"))["stale_stamp"] is False


def test_live_fetch_failure_refuses(repo_root, tmp_path, monkeypatch):
    def boom(gh_api, method, path):
        raise gen.Refused("simulated transport failure")

    monkeypatch.setattr(gen, "_run_gh", boom)
    rc = gen.main(["--repo", str(repo_root), "--sha", SHA,
                   "--out", str(_live_out(repo_root, tmp_path)),
                   "--live", "--gh-api", "/nonexistent-gh-api"])
    assert rc == 2


def test_real_gh_fetch_failure_is_a_refusal():
    # The real _run_gh turns a dead helper into Refused, never an exception leak.
    with pytest.raises(gen.Refused):
        gen._run_gh("/nonexistent-gh-api-binary", "GET", "/x")


# ---------------------------------------------------------------------------
# D. no manufactured tenths — rungs are discrete, statuses from the enum
# ---------------------------------------------------------------------------

def test_no_numeric_scores_anywhere(repo_root, tmp_path):
    m = _run(repo_root, tmp_path)
    raw = json.dumps(m)
    assert "score" not in raw.lower()
    assert "tenths" not in raw.lower()
    assert "rating" not in raw.lower()

    def walk(v):
        if isinstance(v, float):
            raise AssertionError(f"float score leaked into matrix: {v!r}")
        if isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)

    walk(m["organs"])


def test_rungs_and_statuses_come_from_fixed_enums(repo_root, tmp_path):
    m = _run(repo_root, tmp_path)
    for o in m["organs"]:
        assert o["current_rung"] in (["UNKNOWN"] + RUNGS)
        assert o["missing_rung"] in (["UNIT", "INTEGRATION", "BEHAVIORAL",
                                      "OUTCOME", "PRODUCTION", "SUCCESSOR", None])
        assert [e["rung"] for e in o["rung_evidence"]] == RUNGS
        for e in o["rung_evidence"]:
            assert e["status"] in STATUSES, (o["organ"], e["rung"], e["status"])
            assert isinstance(e["refs"], list)
        # missing_rung and next_proof are null together, always.
        assert (o["missing_rung"] is None) == (o["next_proof"] is None)


def test_full_receipt_path_reaches_successor_honestly(repo_root, tmp_path):
    runs = [{"name": "live-know-proof", "conclusion": "success", "id": 5,
             "head_sha": SHA, "head_branch": "main"}]
    checks = GREEN + [{"name": "independent-verification", "conclusion": "success", "id": 7}]
    m = _run(repo_root, tmp_path, checks=checks, runs=runs,
             paths=["tests/test_know_retrieval.py"],
             acceptance={"KNOW": ["verify:acceptance/know-001"]},
             prod_receipt={"promotion_run_id": 777, "dispatched_by": "shawn",
                           "migration_receipts": ["m1", "m2"]},
             cont_receipt={"qualification_run_id": 888, "chartered_by": "shawn"})
    know = _organ(m, "KNOW")
    assert know["current_rung"] == "SUCCESSOR"
    assert know["missing_rung"] is None
    assert know["next_proof"] is None
    assert all(e["status"] == "PROVEN" for e in know["rung_evidence"])
    # The other organs stay honest about their own holes: LAW has genuine
    # production/continuity receipts (evidence recorded PROVEN) but no UNIT
    # proof, so the prefix rule caps its CLAIM at CONTRACT with UNIT missing
    # — the receipts are not erased, just unclaimable until the gap closes.
    law = _organ(m, "LAW")
    assert law["current_rung"] == "CONTRACT"
    assert law["missing_rung"] == "UNIT"
    assert "kernel-tests" in law["next_proof"]
    assert _rung(m, "LAW", "PRODUCTION")["status"] == "PROVEN"
    assert _rung(m, "LAW", "SUCCESSOR")["status"] == "PROVEN"


def test_partial_production_receipt_stays_undispatched(repo_root, tmp_path):
    # A receipt missing migration_receipts is not a dispatch.
    m = _run(repo_root, tmp_path,
             prod_receipt={"promotion_run_id": 777, "dispatched_by": "shawn"})
    for o in m["organs"]:
        assert _rung(m, o["organ"], "PRODUCTION")["status"] == "UNKNOWN_NOT_DISPATCHED"


def test_blockers_name_the_missing_proof(repo_root, tmp_path):
    # Missing UNIT with an absent check: next_proof names the check; with a
    # green check but no organ tests, blockers name the evidence hole.
    m = _run(repo_root, tmp_path, checks=[], runs=[], paths=[])
    know = _organ(m, "KNOW")
    assert know["missing_rung"] == "UNIT"
    assert "kernel-tests" in know["next_proof"]

    m = _run(repo_root, tmp_path, paths=["tests/test_know_retrieval.py"])
    know = _organ(m, "KNOW")
    assert know["missing_rung"] == "BEHAVIORAL"
    assert any("live-know-proof" in b for b in know["blockers"])


# ---------------------------------------------------------------------------
# E. refusal battery
# ---------------------------------------------------------------------------

def _refuse(repo_root, tmp_path, mutate=None, argv_extra=(), sha=SHA):
    if mutate:
        mutate(repo_root)
    out = tmp_path / "m.json"
    rc = gen.main(["--repo", str(repo_root), "--sha", sha, "--out", str(out),
                   "--evaluator", "adversarial-test"] + list(argv_extra))
    assert rc == 2
    assert not out.exists()


def test_refuses_when_registry_file_absent(repo_root, tmp_path):
    def mutate(r):
        (r / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json").unlink()
    _refuse(repo_root, tmp_path, mutate)


def test_refuses_when_contract_file_absent(repo_root, tmp_path):
    def mutate(r):
        (r / "BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json").unlink()
    _refuse(repo_root, tmp_path, mutate)


def test_refuses_when_schema_file_absent(repo_root, tmp_path):
    def mutate(r):
        (r / "BRAIN/03-KERNEL/SCHEMA/ORGAN-HEALTH-MATRIX-SCHEMA.json").unlink()
    _refuse(repo_root, tmp_path, mutate)


def test_refuses_when_registry_order_differs(repo_root, tmp_path):
    def mutate(r):
        p = r / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json"
        reg = json.loads(p.read_text())
        reg["node_order"] = list(reversed(reg["node_order"]))  # same set, wrong order
        p.write_text(json.dumps(reg))
    _refuse(repo_root, tmp_path, mutate)


def test_refuses_when_node_missing_from_contract(repo_root, tmp_path):
    def mutate(r):
        p = r / "BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json"
        con = json.loads(p.read_text())
        del con["nodes"]["EVOLVE"]  # STRUCTURAL unprovable
        p.write_text(json.dumps(con))
    _refuse(repo_root, tmp_path, mutate)


def test_refuses_when_proof_ladder_renamed(repo_root, tmp_path):
    def mutate(r):
        p = r / "BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json"
        con = json.loads(p.read_text())
        con["nodes"]["KNOW"]["proof_ladder"] = [x.lower() for x in RUNGS]
        p.write_text(json.dumps(con))
    _refuse(repo_root, tmp_path, mutate)


def test_refuses_when_envelope_fields_empty(repo_root, tmp_path):
    def mutate(r):
        p = r / "BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json"
        con = json.loads(p.read_text())
        con["universal_envelope"]["required_fields"] = []
        p.write_text(json.dumps(con))
    _refuse(repo_root, tmp_path, mutate)


@pytest.mark.parametrize("bad", ["507d3421",            # 8 hex — short SHA
                                 "z" * 40,              # non-hex
                                 "507d34213333a38708912d343537985e619938a!",  # 40th char bad
                                 "507d34213333a38708912d343537985e619938ac00"])  # 42 hex
def test_refuses_on_malformed_sha(repo_root, tmp_path, bad):
    _refuse(repo_root, tmp_path, sha=bad)


def test_uppercase_sha_is_normalized(repo_root, tmp_path):
    m = _run(repo_root, tmp_path, sha=SHA.upper())
    assert m["stamped_sha"] == SHA


def test_refuses_when_stamp_undeterminable(repo_root, tmp_path):
    # No --sha and the repo is not a git checkout: no stamp may be invented.
    out = tmp_path / "m.json"
    rc = gen.main(["--repo", str(repo_root), "--out", str(out)])
    assert rc == 2
    assert not out.exists()


# ---------------------------------------------------------------------------
# F. UNIT coverage rules — exact tokens, escape hatch, ref truncation
# ---------------------------------------------------------------------------

def test_operator_coverage_escape_hatch(repo_root, tmp_path):
    m = _run(repo_root, tmp_path, paths=[],
             unit_coverage={"LAW": True, "KNOW": False})
    assert _rung(m, "LAW", "UNIT")["status"] == "PROVEN"
    assert any("operator:unit-coverage.json" in r for r in _rung(m, "LAW", "UNIT")["refs"])
    assert _rung(m, "KNOW", "UNIT")["status"] == "UNKNOWN"


def test_substring_organ_token_does_not_cover(repo_root, tmp_path):
    # "myself" contains "self" but is not the token "self".
    m = _run(repo_root, tmp_path, paths=["myself/tests/x.py"])
    assert _rung(m, "SELF", "UNIT")["status"] == "UNKNOWN"


def test_organ_token_without_test_token_does_not_cover(repo_root, tmp_path):
    m = _run(repo_root, tmp_path, paths=["BRAIN/KNOW/domain.md", "src/know/runtime.py"])
    assert _rung(m, "KNOW", "UNIT")["status"] == "UNKNOWN"


def test_case_insensitive_paths_cover(repo_root, tmp_path):
    m = _run(repo_root, tmp_path, paths=["TESTS/TEST_KNOW_X.PY"])
    assert _rung(m, "KNOW", "UNIT")["status"] == "PROVEN"


def test_refs_truncate_at_ten_with_overflow_marker(repo_root, tmp_path):
    paths = [f"tests/test_know_{i:02d}.py" for i in range(12)]
    m = _run(repo_root, tmp_path, paths=paths)
    refs = _rung(m, "KNOW", "UNIT")["refs"]
    assert _rung(m, "KNOW", "UNIT")["status"] == "PROVEN"
    assert "repo:+2-more-organ-test-paths" in refs
    repo_refs = [r for r in refs if r.startswith("repo:tests/")]
    assert len(repo_refs) == 10

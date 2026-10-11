"""Tests for the directive status honesty gate (wire lane).

Proves the gate blocks every hand-edit bypass of the status tool's ladder
rules, and proves the ENFORCED-gate persistence repair it ships with.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import directive_status_honesty as hon


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def entry(did, status, evidence_pr=None, gate=None):
    e = {
        "id": did,
        "title": f"Directive {did}",
        "source_issue": 2175,
        "source_comment": "6100000000",
        "owner": "naya2",
        "status": status,
        "evidence_pr": evidence_pr,
        "wave": 6,
    }
    if gate is not None:
        e["gate"] = gate
    return e


@pytest.fixture()
def repo(tmp_path):
    (tmp_path / "BRAIN").mkdir()
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / ".github" / "workflows" / "real-gate.yml").write_text(
        "# a real gate\n", encoding="utf-8"
    )
    return tmp_path


def honest_head(repo):
    return [
        entry("D1", "NOT_STARTED"),
        entry("D2", "BUILDING", evidence_pr=100),
        entry("D3", "BUILT_AS_CODE", evidence_pr=101),
        entry(
            "D4", "ENFORCED", evidence_pr=102,
            gate=".github/workflows/real-gate.yml",
        ),
    ]


# ---------------------------------------------------------------------------
# H1-H3: rung invariants on the head register
# ---------------------------------------------------------------------------

def test_clean_register_passes(repo):
    assert hon.check_registers(None, honest_head(repo), repo) == []


def test_not_started_with_evidence_refused(repo):
    head = [entry("D1", "NOT_STARTED", evidence_pr=100)]
    vs = hon.check_registers(None, head, repo)
    assert len(vs) == 1 and "H1" in vs[0] and "D1" in vs[0]


def test_built_as_code_without_evidence_refused(repo):
    head = [entry("D3", "BUILT_AS_CODE")]
    vs = hon.check_registers(None, head, repo)
    assert len(vs) == 1 and "H2" in vs[0] and "D3" in vs[0]


def test_built_as_code_with_zero_evidence_pr_refused(repo):
    head = [entry("D3", "BUILT_AS_CODE", evidence_pr=0)]
    vs = hon.check_registers(None, head, repo)
    assert len(vs) == 1 and "H2" in vs[0]


def test_enforced_without_gate_refused(repo):
    head = [entry("D4", "ENFORCED", evidence_pr=102)]
    vs = hon.check_registers(None, head, repo)
    assert len(vs) == 1 and "H3" in vs[0] and "D4" in vs[0]


def test_enforced_with_phantom_gate_path_refused(repo):
    head = [
        entry("D4", "ENFORCED", evidence_pr=102,
              gate=".github/workflows/does-not-exist.yml")
    ]
    vs = hon.check_registers(None, head, repo)
    assert len(vs) == 1 and "H3" in vs[0] and "does-not-exist" in vs[0]


def test_enforced_with_named_non_path_gate_allowed(repo):
    # A named (non-path) gate is accepted as a name — reviewers judge reality.
    head = [entry("D4", "ENFORCED", evidence_pr=102, gate="branch protection rule")]
    assert hon.check_registers(None, head, repo) == []


# ---------------------------------------------------------------------------
# H4: ladder movement base -> head
# ---------------------------------------------------------------------------

def test_honest_promotion_one_rung_passes(repo):
    base = [entry("D2", "BUILDING", evidence_pr=100)]
    head = [entry("D2", "BUILT_AS_CODE", evidence_pr=101)]
    assert hon.check_registers(base, head, repo) == []


def test_skip_rung_refused(repo):
    base = [entry("D1", "NOT_STARTED")]
    head = [entry("D1", "BUILT_AS_CODE", evidence_pr=101)]
    vs = hon.check_registers(base, head, repo)
    assert len(vs) == 1 and "H4" in vs[0] and "D1" in vs[0]


def test_skip_to_enforced_refused_even_with_evidence_and_gate(repo):
    # The movement is the crime — evidence + gate do not excuse the skip.
    base = [entry("D1", "NOT_STARTED")]
    head = [entry("D1", "ENFORCED", evidence_pr=101,
                  gate=".github/workflows/real-gate.yml")]
    vs = hon.check_registers(base, head, repo)
    assert any("H4" in v for v in vs)


def test_demotion_any_distance_allowed(repo):
    base = [entry("D4", "ENFORCED", evidence_pr=102,
                  gate=".github/workflows/real-gate.yml")]
    head = [entry("D4", "NOT_STARTED")]  # evidence cleared, honest news
    assert hon.check_registers(base, head, repo) == []


def test_removed_entry_refused(repo):
    base = [entry("D1", "NOT_STARTED"), entry("D2", "BUILDING", evidence_pr=100)]
    head = [entry("D1", "NOT_STARTED")]
    vs = hon.check_registers(base, head, repo)
    assert len(vs) == 1 and "H4" in vs[0] and "D2" in vs[0]


def test_new_entry_judged_by_invariants_only(repo):
    base = [entry("D1", "NOT_STARTED")]
    head = [entry("D1", "NOT_STARTED"),
            entry("D9", "BUILT_AS_CODE", evidence_pr=200)]
    assert hon.check_registers(base, head, repo) == []


# ---------------------------------------------------------------------------
# Repair regression: ENFORCED promotion persists the validated gate
# ---------------------------------------------------------------------------

def _write_register(path, entries):
    path.write_text(json.dumps(entries, indent=2, ensure_ascii=True),
                    encoding="utf-8")


def test_gate_persisted_on_enforced_promotion(repo):
    """Wire-lane repair: the CLI validated --gate but dropped it from the
    entry. The register must record which live mechanism enforces the rung."""
    import directive_register as reg
    import directive_status as ds

    register = repo / "BRAIN" / "01-GOVERNANCE" / "directive-register.json"
    register.parent.mkdir(parents=True, exist_ok=True)
    _write_register(register, [entry("D32", "BUILT_AS_CODE", evidence_pr=2213)])
    gate_rel = ".github/workflows/real-gate.yml"

    argv = ["--register", str(register), "promote", "D32", "--to", "ENFORCED",
            "--evidence-pr", "2224", "--gate", gate_rel]
    code = ds.main(argv)
    assert code == 0
    persisted = reg.get_directive(reg.load_register(register), "D32")
    assert persisted["status"] == "ENFORCED"
    assert persisted["evidence_pr"] == 2224
    assert persisted.get("gate") == gate_rel, (
        "the validated gate must be written to the entry, not just the receipt"
    )
    # And the honesty gate accepts the CLI-produced state end to end.
    assert hon.check_registers(None, reg.load_register(register), repo) == []


# ---------------------------------------------------------------------------
# CLI end to end over a real git repo
# ---------------------------------------------------------------------------

def _git(repo, *args, env=None):
    base_env = dict(os.environ)
    base_env.update({
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
    })
    if env:
        base_env.update(env)
    proc = subprocess.run(["git", *args], cwd=repo, capture_output=True,
                          text=True, env=base_env)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip()


def _commit_register(gitrepo, entries):
    rel = hon.REGISTER_REL
    target = gitrepo / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    _write_register(target, entries)
    (gitrepo / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (gitrepo / ".github" / "workflows" / "real-gate.yml").write_text("# g\n")
    (gitrepo / "BRAIN").mkdir(exist_ok=True)
    _git(gitrepo, "add", "-A")
    _git(gitrepo, "commit", "-m", "register")
    return _git(gitrepo, "rev-parse", "HEAD")


@pytest.fixture()
def gitrepo(tmp_path):
    d = tmp_path / "gr"
    d.mkdir()
    _git(d, "init", "-q")
    return d


def _run_cli(gitrepo, base_ref, head_ref):
    proc = subprocess.run(
        [sys.executable, str(Path(hon.__file__)),
         "--base-ref", base_ref, "--head-ref", head_ref,
         "--repo", str(gitrepo)],
        capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def test_cli_blocks_skip_rung_end_to_end(gitrepo):
    v1 = _commit_register(gitrepo, [entry("D1", "NOT_STARTED")])
    v2 = _commit_register(gitrepo, [entry("D1", "BUILT_AS_CODE", evidence_pr=9)])
    code, out = _run_cli(gitrepo, v1, v2)
    assert code == 1, out
    assert "H4" in out and "D1" in out


def test_cli_passes_honest_one_rung_end_to_end(gitrepo):
    v1 = _commit_register(gitrepo, [entry("D1", "NOT_STARTED")])
    v2 = _commit_register(gitrepo, [entry("D1", "BUILDING", evidence_pr=9)])
    code, out = _run_cli(gitrepo, v1, v2)
    assert code == 0, out
    assert "STATUS-HONESTY OK" in out


def test_cli_fail_closed_on_corrupt_head(gitrepo):
    v1 = _commit_register(gitrepo, [entry("D1", "NOT_STARTED")])
    target = gitrepo / hon.REGISTER_REL
    target.write_text("{not json", encoding="utf-8")
    _git(gitrepo, "add", "-A")
    _git(gitrepo, "commit", "-m", "corrupt")
    v2 = _git(gitrepo, "rev-parse", "HEAD")
    code, out = _run_cli(gitrepo, v1, v2)
    assert code == 2, out
    assert "FAIL-CLOSED" in out


def test_cli_new_register_runs_invariants_only(gitrepo):
    _git(gitrepo, "commit", "--allow-empty", "-m", "empty")
    v1 = _git(gitrepo, "rev-parse", "HEAD")
    v2 = _commit_register(
        gitrepo,
        [entry("D1", "ENFORCED", evidence_pr=9,
               gate=".github/workflows/real-gate.yml")],
    )
    code, out = _run_cli(gitrepo, v1, v2)
    assert code == 0, out
    assert "movement check skipped" in out

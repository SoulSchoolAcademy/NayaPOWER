"""Proof for the Law-of-One rung-2 advisory reporter
(.github/workflows/law-of-one-report.yml).

The reporter is the change under test; the judge (tools/check_law_of_one.py)
was already proven at rung-1 with 12/12 tests and its 0/1/2 exit contract is
taken from its docstring. These tests extract the EXACT `run:` script bytes
from the shipped workflow and execute them in sandbox fixture trees, proving
the reporter's contract:

  - exit 1 (UNOWNED — honest baseline) -> reporter exit 0, summary BASELINE
  - exit 0 (all owned)               -> reporter exit 0, summary PASS
  - exit 2 (judge failed closed)     -> reporter exit 0, summary ERROR
  - check script absent (rung-1 not on main) -> reporter exit 0, PENDING
  - workflow YAML parses; advisory-never-fails is documented; actions pinned.

A reporter that failed closed would hold up the merge queue on a CANDIDATE
law's honest baseline — that is why every case must prove exit 0.
"""
import os
import stat
import subprocess
from pathlib import Path

import pytest
import yaml

WORKFLOW = (
    Path(__file__).resolve().parent.parent
    / ".github"
    / "workflows"
    / "law-of-one-report.yml"
)


def _load_workflow():
    return yaml.safe_load(WORKFLOW.read_text())


def _report_script():
    wf = _load_workflow()
    for job in wf["jobs"].values():
        for step in job["steps"]:
            if "Law-of-One enforcement report" in step.get("name", ""):
                return step["run"]
    raise AssertionError("advisory report step not found in workflow")


def _stub_judge(root, exit_code, stdout_text):
    """A judge that honors the 0/1/2 contract with canned output."""
    tool = root / "tools" / "check_law_of_one.py"
    tool.parent.mkdir(parents=True, exist_ok=True)
    tool.write_text(
        "#!/usr/bin/env python3\n"
        "import sys\n"
        f'print({stdout_text!r})\n'
        f"sys.exit({exit_code})\n"
    )
    tool.chmod(tool.stat().st_mode | stat.S_IEXEC)


def _run_reporter(root):
    script = _report_script()
    summary = root / "step-summary.md"
    summary.write_text("")
    proc = subprocess.run(
        ["bash", "-c", script],
        cwd=root,
        env={**os.environ, "GITHUB_STEP_SUMMARY": str(summary)},
        capture_output=True,
        text=True,
        timeout=60,
    )
    return proc.returncode, summary.read_text(), proc.stderr


def test_workflow_yaml_structure():
    wf = _load_workflow()
    assert wf["permissions"] == {"contents": "read"}, "minimal permissions only"
    triggers = wf[True]  # `on:` parses to boolean True in YAML 1.1
    assert "pull_request_target" in triggers, "judge must run base code"
    assert "push" in triggers, "continuous detection on main"
    script = _report_script()
    assert "exit 0" in script
    assert "GITHUB_STEP_SUMMARY" in script
    raw = WORKFLOW.read_text()
    assert "never blocks a merge" in raw, "advisory contract documented"
    assert "11d5960a326750d5838078e36cf38b85af677262" in raw, "checkout pinned"
    assert "a26af69be951a213d495a4c3e4e4022e16d87065" in raw, "setup-python pinned"


def test_unowned_baseline_reports_honest_without_blocking(tmp_path):
    _stub_judge(tmp_path, 1, "FAIL: 5/5 operational rules without live mechanical owner")
    code, summary, _ = _run_reporter(tmp_path)
    assert code == 0, "reporter never fails the workflow"
    assert "BASELINE" in summary
    assert "5/5" in summary


def test_all_owned_reports_pass_without_blocking(tmp_path):
    _stub_judge(tmp_path, 0, "PASS: all 5 operational rules have a live mechanical owner")
    code, summary, _ = _run_reporter(tmp_path)
    assert code == 0
    assert "PASS — every operational rule has a live mechanical owner." in summary


def test_judge_error_reports_error_without_blocking(tmp_path):
    _stub_judge(tmp_path, 2, "ERROR: registry unparseable")
    code, summary, _ = _run_reporter(tmp_path)
    assert code == 0
    assert "ERROR — the registry check failed closed" in summary


def test_rung1_absent_reports_pending_not_silent(tmp_path):
    code, summary, _ = _run_reporter(tmp_path)
    assert code == 0
    assert "PENDING" in summary
    assert "not on main yet" in summary

"""Fail-closed regression tests for the consensus gate's head-SHA lookup.

Zeta's wave-45 forensics (job 115177642875: installation-token rate-limited
after 5 attempts) raised the fail-OPEN fear class: a blind head-SHA lookup
producing a confident-looking `head_sha` into $GITHUB_OUTPUT.

Live verification (2026-10-13, tip 1324b263) found the shipped script already
exits 1 on lookup failure — no hardcoded fallback exists in the workflow or in
its git history. These tests PIN that property behaviorally (P-017): they
extract the ACTUAL "Get PR info" run script from the live workflow file and
execute it with a stubbed `gh`, proving:

  1. failed lookup (5 exhausted attempts) -> non-zero exit, NO head_sha line
     in $GITHUB_OUTPUT (never a fabricated SHA)
  2. malformed/forged lookup output (non-40-hex) -> non-zero exit, NO head_sha
     line (the P-008 fail-closed binding)
  3. valid 40-hex lookup -> head_sha echoed exactly (happy path unchanged)

The test substitutes the GitHub `${{ }}` template expressions with test
values and strips the wall-clock `sleep` backoff lines (irrelevant to the
fail-closed property); everything else is the verbatim shipped script.
"""
import os
import re
import stat
import subprocess
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "merge-consensus-gate.yml"

VALID_SHA = "a" * 40
FORGED_SHA = "deadbeef"  # plausible-looking but not a full git SHA


def _extract_step_script():
    """Extract the verbatim run script of the 'Get PR info' step."""
    lines = WORKFLOW.read_text().splitlines()
    in_step = False
    capturing = False
    script = []
    indent = None
    for line in lines:
        if re.match(r"\s*- name: Get PR info\s*$", line):
            in_step = True
            continue
        if in_step and re.match(r"\s*run: \|\s*$", line):
            capturing = True
            indent = len(line) - len(line.lstrip())
            continue
        if capturing:
            if line.strip() == "" or (len(line) - len(line.lstrip())) > indent:
                script.append(line[indent + 2:] if len(line) > indent + 2 else "")
                continue
            break
    body = "\n".join(script)
    assert "for attempt in 1 2 3 4 5" in body, "step script not found in live workflow"
    # Substitute GitHub template expressions; strip wall-clock sleeps.
    body = body.replace("${{ github.event_name }}", "issue_comment")
    body = body.replace("${{ github.event.issue.number }}", "2512")
    body = body.replace("${{ github.repository }}", "SoulSchoolAcademy/NayaPOWER")
    body = re.sub(r"^\s*sleep .*$\n?", "", body, flags=re.M)
    return body


STEP_SCRIPT = _extract_step_script()


def _run_step(gh_stub_body):
    """Run the live step script with a stubbed gh; return (rc, github_output)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        stub_dir = tmpdir / "bin"
        stub_dir.mkdir()
        stub = stub_dir / "gh"
        stub.write_text("#!/bin/sh\n" + gh_stub_body + "\n")
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        script = tmpdir / "step.sh"
        script.write_text("#!/bin/sh\n" + STEP_SCRIPT + "\n")
        script.chmod(script.stat().st_mode | stat.S_IEXEC)
        output_file = tmpdir / "github_output"
        output_file.write_text("")
        env = dict(os.environ)
        env["PATH"] = str(stub_dir) + os.pathsep + env.get("PATH", "")
        env["GITHUB_OUTPUT"] = str(output_file)
        proc = subprocess.run(
            [str(script)], env=env, capture_output=True, text=True, timeout=120
        )
        return proc.returncode, output_file.read_text()


def _head_sha_lines(output):
    return [l for l in output.splitlines() if l.startswith("head_sha=")]


def test_failed_lookup_exits_nonzero_with_no_head_sha():
    """5 exhausted API attempts -> fail closed: exit != 0, NO head_sha output."""
    rc, output = _run_step("echo 'rate limit stub' >&2; exit 1")
    assert rc != 0, "failed lookup must fail the step"
    assert _head_sha_lines(output) == [], (
        "failed lookup must not emit any head_sha into $GITHUB_OUTPUT"
    )


def test_forged_malformed_sha_is_rejected():
    """A lookup returning a non-40-hex value is REJECTED, not echoed."""
    rc, output = _run_step(f"echo '{FORGED_SHA}'; exit 0")
    assert rc != 0, "malformed lookup output must fail the step"
    assert _head_sha_lines(output) == [], (
        "malformed SHA must never be echoed as a confident-looking head_sha"
    )


def test_empty_lookup_output_is_rejected():
    """A lookup returning empty output is rejected (no head_sha line)."""
    rc, output = _run_step("echo ''; exit 0")
    assert rc != 0, "empty lookup output must fail the step"
    assert _head_sha_lines(output) == []


def test_valid_sha_still_echoed():
    """Happy path: a valid 40-hex lookup result is echoed exactly once."""
    rc, output = _run_step(f"echo '{VALID_SHA}'; exit 0")
    assert rc == 0, "valid lookup must succeed"
    assert _head_sha_lines(output) == [f"head_sha={VALID_SHA}"]

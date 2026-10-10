"""Tests for tools/check_scorecard_receipt.py.

The Scorecard Law's first mechanical rung: detect whether a PR body carries
the five-step receipt (enumerate / score / gate / decide / receipt).

Conventions: stdlib only (pytest or plain asserts); the tool module is loaded
by path so tests run from the repo root without installation.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools" / "check_scorecard_receipt.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("check_scorecard_receipt", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FULL_RECEIPT_BODY = """\
## What
Something changed.

## Scorecard receipt (Scorecard Law, five steps)
1. **Enumerate:** (a) do X, (b) do Y, (c) do nothing.
2. **Score:** (b) wins — reversible, high value; (a) is toil; (c) compounds debt.
3. **Gate:** reversible ✓ · no production/credentials/destructive change ✓.
4. **Decide:** (b). Strongest alternative: (a). Falsifier: metric drops.
5. **Receipt:** this PR body + feed sign in/out. No receipt, no merge.

## Evidence
Tests green.
"""

NO_RECEIPT_BODY = """\
## What
Something changed.

## Evidence
Tests green. Trust me.
"""

PARTIAL_RECEIPT_BODY = """\
## Scorecard Receipt
1. Enumerate: (a) do X, (b) do Y.
2. Score: (b) wins.
3. Gate: reversible.

(Two of the five steps were never written.)
"""


def test_full_receipt_present():
    mod = load_tool()
    r = mod.verdict_for(FULL_RECEIPT_BODY)
    assert r["verdict"] == "PRESENT", r
    assert r["steps_missing"] == []
    assert len(r["steps_found"]) == 5


def test_no_receipt_missing():
    mod = load_tool()
    r = mod.verdict_for(NO_RECEIPT_BODY)
    assert r["verdict"] == "MISSING", r
    assert r["steps_found"] == []


def test_partial_receipt():
    mod = load_tool()
    r = mod.verdict_for(PARTIAL_RECEIPT_BODY)
    assert r["verdict"] == "PARTIAL", r
    assert set(r["steps_missing"]) == {"decide", "receipt"}


def test_empty_body_is_missing_not_present():
    # Fail-closed: UNKNOWN != PASS.
    mod = load_tool()
    r = mod.verdict_for("")
    assert r["verdict"] == "MISSING", r


def test_score_does_not_match_scorecard():
    # The word-boundary guard: a section that only says "scorecard" must not
    # count as the "score" step.
    mod = load_tool()
    body = "## Scorecard\n\nThis scorecard section mentions nothing else.\n"
    r = mod.verdict_for(body)
    assert r["verdict"] in ("PARTIAL", "MISSING"), r
    assert "score" in r["steps_missing"], r


def test_section_bounded_by_next_header():
    # Steps mentioned AFTER the next header must not leak into the receipt.
    mod = load_tool()
    body = ("## Scorecard receipt\n\n1. Enumerate: options.\n\n"
            "## Appendix\n\nWe score and gate and decide and receipt things here.\n")
    r = mod.verdict_for(body)
    assert r["verdict"] == "PARTIAL", r
    assert set(r["steps_missing"]) == {"score", "gate", "decide", "receipt"}


def test_header_without_steps_is_missing():
    # A "scorecard" header with zero of the five steps is MISSING, not PARTIAL.
    mod = load_tool()
    body = ("## Scorecard receipt — SCORECARD-LAW-V1\n\n"
            "We did the work carefully and it is good.\n")
    r = mod.verdict_for(body)
    assert r["verdict"] == "MISSING", r


def test_cli_exit_codes():
    # 0 = PRESENT, 1 = PARTIAL/MISSING, via real subprocess (fail-closed wiring).
    p = subprocess.run([sys.executable, str(TOOL), "--body", FULL_RECEIPT_BODY],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
    assert "PRESENT" in p.stdout

    p = subprocess.run([sys.executable, str(TOOL), "--body", NO_RECEIPT_BODY],
                       capture_output=True, text=True)
    assert p.returncode == 1, p.stdout + p.stderr
    assert "MISSING" in p.stdout

    p = subprocess.run([sys.executable, str(TOOL), "--body", PARTIAL_RECEIPT_BODY],
                       capture_output=True, text=True)
    assert p.returncode == 1, p.stdout + p.stderr
    assert "PARTIAL" in p.stdout


def test_cli_json_and_summary_modes():
    p = subprocess.run([sys.executable, str(TOOL), "--body", FULL_RECEIPT_BODY,
                        "--json"], capture_output=True, text=True)
    assert p.returncode == 0
    import json
    data = json.loads(p.stdout)
    assert data["verdict"] == "PRESENT"

    p = subprocess.run([sys.executable, str(TOOL), "--body", NO_RECEIPT_BODY,
                        "--summary", "--pr", "1234"], capture_output=True, text=True)
    assert p.returncode == 1
    assert "PR #1234" in p.stdout
    assert "MISSING" in p.stdout

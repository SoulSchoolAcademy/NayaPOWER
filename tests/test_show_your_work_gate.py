"""Tests for tools/check_show_your_work.py.

The show-your-work gate blocks any merge missing a valid three-pass
self-validation receipt. These tests prove:
  - Positive: a complete, honest receipt passes.
  - Negative: missing/incomplete/mislabeled receipts are blocked.
"""
import os
import subprocess
import sys

GATE = os.path.join(os.path.dirname(__file__), "..", "tools",
                    "check_show_your_work.py")
HEAD_SHA = "a" * 40  # fake but valid-format SHA for tests


def run_gate(pr_body, head_sha=HEAD_SHA):
    env = dict(os.environ, PR_BODY=pr_body, HEAD_SHA=head_sha)
    result = subprocess.run([sys.executable, GATE], capture_output=True,
                            text=True, env=env)
    return result.returncode, result.stdout + result.stderr


VALID_RECEIPT = f"""## Summary
Fixed the thing.

## Show-Your-Work Receipt
**Branch:** `naya4/my-feature`
**Head SHA:** `{HEAD_SHA}`

### Pass 1 (self-validation) — Score: 7/10
**Holes found:**
- The error message was unclear.
- No test for the empty-input case.
**Repairs made:**
- Rewrote the error message in plain words.
- Added test_empty_input.

### Pass 2 (self-validation) — Score: 9/10
**Remaining holes:**
- The docstring was missing a parameter.
**Repairs made:**
- Added the missing parameter to the docstring.

### Pass 3 (self-validation) — Score: 10/10
**Result:** All holes closed. Tests pass. Ready to merge.
**Exact head certified:** `{HEAD_SHA}`
"""


def test_valid_receipt_passes():
    code, out = run_gate(VALID_RECEIPT)
    assert code == 0, f"valid receipt should pass:\n{out}"
    assert "GATE PASSED" in out


def test_missing_receipt_section_blocked():
    code, out = run_gate("## Summary\nJust a regular PR body.\n")
    assert code == 1, "missing receipt section should block"
    assert "no `## Show-Your-Work Receipt` section" in out


def test_missing_pass_2_blocked():
    body = VALID_RECEIPT.replace("### Pass 2 (self-validation)", "### Skipped")
    code, out = run_gate(body)
    assert code == 1, "missing Pass 2 should block"
    assert "Pass 2" in out


def test_mislabeled_pass_blocked():
    # Three self-passes must never be called "independent verification".
    body = VALID_RECEIPT.replace(
        "### Pass 1 (self-validation)", "### Pass 1 (independent verification)")
    code, out = run_gate(body)
    assert code == 1, "mislabeled pass should block"
    assert "self-validation" in out


def test_missing_score_blocked():
    body = VALID_RECEIPT.replace("Score: 7/10", "Score: TBD")
    code, out = run_gate(body)
    assert code == 1, "missing score should block"
    assert "Pass 1" in out


def test_missing_holes_blocked():
    body = VALID_RECEIPT.replace("**Holes found:**", "**Stuff:**")
    code, out = run_gate(body)
    assert code == 1, "missing holes list should block"
    assert "Pass 1" in out


def test_sha_mismatch_blocked():
    other_sha = "b" * 40
    code, out = run_gate(VALID_RECEIPT, head_sha=other_sha)
    assert code == 1, "SHA mismatch should block"
    assert "exact head" in out.lower()


def test_pass3_missing_certification_blocked():
    body = VALID_RECEIPT.replace("**Exact head certified:**", "**Head:**")
    code, out = run_gate(body)
    assert code == 1, "Pass 3 missing certification should block"
    assert "Pass 3" in out


def test_perfect_first_pass_allowed_with_explicit_statement():
    # A 10/10 first pass is fine IF it says so explicitly.
    body = VALID_RECEIPT.replace(
        "**Holes found:**\n- The error message was unclear.\n- No test for the empty-input case.",
        "**Holes found:** None — the work was clean on first review.")
    code, out = run_gate(body)
    assert code == 0, f"explicit no-holes should pass:\n{out}"

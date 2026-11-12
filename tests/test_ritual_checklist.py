"""Tests for tools/ritual_checklist.py — the Ritual Bounce Mechanism (Gate 6 of 7).

The tool is a REVIEWER AID, not a hard gate: it reports FOUND / MISSING / N/A
per ritual check with evidence, and never auto-rejects (exit 0 always).

Cases: a positive control (fully ritual-compliant product), the adversarial
cases named in the assignment (9.5 claim with no holes, technical-only update,
design with no justification), plus per-ritual targeted and N/A cases.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "ritual_checklist.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))
import ritual_checklist as rc


def check_map(results):
    out = {}
    for rr in results:
        for c in rr.checks:
            out[c.check_id] = c.status
    return out


POSITIVE = """\
## THE TECHNICAL

I ran the calculator on the three candidate actions. Scoring dimensions were:
Dimension 1 — objective alignment: 9.5/10
Dimension 2 — evidence strength: 9.0/10
Dimension 3 — collective impact (Law of One): 9.5/10

Self-score: 9.2/10. Holes found: (1) the mobile viewport meta was missing on
one page, (2) one Smart Note lacked a source receipt. Fills: added the viewport
meta to the shared chassis and re-ran bake; attached the missing receipt and
re-indexed. I saw the page render on my screen — the glow borders lit correctly
and the layout held at 390px width.

Law of One test stated before acting: "Am I doing the most intelligent thing
available?" Yes — this is the most intelligent move for the collective.
The human better off: Shawn spends zero attention on routine review.
On the close call (ship now vs wait for Naya 4's lane), shipping serves the
human better because it unblocks the demo.

Learning claim: I learned the battery venv must include reportlab before the
full suite runs. Behavioral proof: novel problem — ran the suite on a cold
worktree I had never built before; scored blind — Naya 4 scored my fix 9.0
without knowing it was mine.

Shawn, you did this — the dispatch script pointed at the old MAXIS app, which
is not aligned with our protocol. I'm making it right: rewrote it to target
nayanet.live.

Design: this serves one living intelligence — every surface is one brain with
many doors. The purple glow on buttons is justified because it signals the
primary action in low light; the animation is justified because it communicates
state change, not decoration. What improved: contrast on mobile. What was
preserved: the approved black-root chassis.

## LITERALLY WHAT I'M SAYING

I checked my work three ways, found two gaps, fixed both, and the page looks
right on a phone screen. You don't need to touch anything.
"""


def test_positive_control_all_rituals_pass():
    statuses = check_map(rc.run_all(POSITIVE))
    for cid, status in statuses.items():
        assert status == "FOUND", f"{cid} -> {status}"


def test_tool_never_auto_rejects(tmp_path):
    # Even a fully non-compliant product must exit 0 (human decides).
    bad = tmp_path / "bad.md"
    bad.write_text("hello world, nothing here")
    out = subprocess.run(
        [sys.executable, str(TOOL), "--file", str(bad)],
        capture_output=True, text=True, timeout=30,
    )
    assert out.returncode == 0, out.stderr
    assert "NOT a gate" in out.stdout or "reviewer aid" in out.stdout


# ---------------------------------------------------------------- adversarial

def test_adversarial_score_without_holes_is_flagged():
    """Product claims 9.5 but lists no holes -> execution.holes MISSING."""
    text = ("Self-score: 9.5/10. The work is complete and excellent. "
            "I fixed all the tests and re-ran the battery. I saw the page render.")
    statuses = check_map(rc.run_all(text))
    assert statuses["execution.self_score"] == "FOUND"
    assert statuses["execution.holes"] == "MISSING", statuses


def test_adversarial_technical_only_update_is_flagged():
    """Update with only the technical section -> two-part MISSING."""
    text = ("## THE TECHNICAL\n\nI merged the branch and re-ran the battery.\n\n"
            "Nothing else to add.")
    statuses = check_map(rc.run_all(text))
    assert statuses["communication.two_part"] == "MISSING", statuses


def test_adversarial_design_without_justification_is_flagged():
    """Design describing effects with no justification -> design.effect_justified MISSING."""
    text = ("Design: I added a purple glow border, a fade-in animation, and a "
            "deep gradient to the header. It looks amazing. What improved: the "
            "header. What was preserved: the footer. This serves one living "
            "intelligence.")
    statuses = check_map(rc.run_all(text))
    assert statuses["design.one_living_intelligence"] == "FOUND"
    assert statuses["design.effect_justified"] == "MISSING", statuses
    assert statuses["design.improved_vs_preserved"] == "FOUND"


def test_adversarial_learning_claim_without_behavioral_proof_is_flagged():
    """'I learned X, I saved it' with no novel/blind/scored -> MISSING."""
    text = ("Learning claim: I learned that the brain index needs a regen after "
            "governance commits. I saved it as a Smart Note for future runs.")
    statuses = check_map(rc.run_all(text))
    assert statuses["learning.behavioral_proof"] == "MISSING", statuses


def test_adversarial_first_paragraph_with_pr_number_is_flagged():
    text = ("## THE TECHNICAL\n\nPer PR #2091 the branch was merged and verified.\n\n"
            "## LITERALLY WHAT I'M SAYING\n\nAll good.")
    statuses = check_map(rc.run_all(text))
    assert statuses["communication.first_paragraph_clean"] == "MISSING", statuses


def test_adversarial_authority_without_plain_statement_is_flagged():
    """Correcting Shawn's error without stating the misalignment -> MISSING."""
    text = ("I noticed Shawn's dispatch script had a bug and patched it to point "
            "at the right domain. Deployed the fix.")
    statuses = check_map(rc.run_all(text))
    assert statuses["authority.misalignment_stated"] == "MISSING", statuses


def test_adversarial_constitution_without_law_of_one_is_flagged():
    text = ("Significant action taken: I rewrote the activation gate. "
            "The human is better off because setup is faster.")
    statuses = check_map(rc.run_all(text))
    assert statuses["constitution.law_of_one"] == "MISSING", statuses
    assert statuses["constitution.human_value"] == "FOUND"


# ---------------------------------------------------------------- positive targeted

def test_decision_calculator_statement_detected():
    statuses = check_map(rc.run_all("I ran the calculator. Dimensions: speed 8/10, quality 9/10."))
    assert statuses["decision.calculator"] == "FOUND"
    assert statuses["decision.dimensions"] == "FOUND"


def test_first_paragraph_clean_passes():
    text = ("## THE TECHNICAL\n\nThe battery is green and the tip is verified.\n\n"
            "Details on PR #2091 below.\n\n"
            "## LITERALLY WHAT I'M SAYING\n\nEverything checks out.")
    statuses = check_map(rc.run_all(text))
    assert statuses["communication.two_part"] == "FOUND"
    assert statuses["communication.first_paragraph_clean"] == "FOUND"


# ---------------------------------------------------------------- N/A honesty

def test_non_applicable_rituals_report_na_not_missing():
    """A plain code summary claims no learning, no Shawn correction, no design,
    no update — those rituals must report N/A, never MISSING."""
    text = "Refactored the helper into two functions. Unit tests pass 12/12."
    statuses = check_map(rc.run_all(text))
    assert statuses["communication.two_part"] == "N/A"
    assert statuses["learning.behavioral_proof"] == "N/A"
    assert statuses["authority.misalignment_stated"] == "N/A"
    assert statuses["design.one_living_intelligence"] == "N/A"
    # but execution self-score is genuinely missing -> MISSING, not N/A
    assert statuses["execution.self_score"] == "MISSING"


# ---------------------------------------------------------------- CLI shape

def test_cli_json_shape(tmp_path):
    f = tmp_path / "p.md"
    f.write_text(POSITIVE)
    out = subprocess.run(
        [sys.executable, str(TOOL), "--file", str(f), "--json"],
        capture_output=True, text=True, timeout=30,
    )
    assert out.returncode == 0, out.stderr
    data = json.loads(out.stdout)
    assert data["auto_reject"] is False
    keys = [r["key"] for r in data["rituals"]]
    assert keys == ["DECISION", "COMMUNICATION", "EXECUTION", "LEARNING",
                    "AUTHORITY", "CONSTITUTION", "DESIGN"]
    assert all(r["verdict"] == "PASS" for r in data["rituals"])
    assert all(set(c) == {"id", "description", "status", "evidence"}
               for r in data["rituals"] for c in r["checks"])


def test_cli_text_checklist_renders(tmp_path):
    f = tmp_path / "p.md"
    f.write_text("Self-score: 9.5/10.")
    out = subprocess.run(
        [sys.executable, str(TOOL), "--file", str(f)],
        capture_output=True, text=True, timeout=30,
    )
    assert out.returncode == 0, out.stderr
    assert "RITUAL CHECKLIST" in out.stdout
    assert "summary:" in out.stdout
    assert "[-]" in out.stdout  # at least one flag on this thin product

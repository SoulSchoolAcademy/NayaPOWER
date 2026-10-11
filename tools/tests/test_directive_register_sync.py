"""Tests for the directive-register wire: loader + sync scanner.

These are REAL asserts with negative controls. The wire is proven only if:
  1. a phantom directive reference (D70) FAILS the scan with a witness,
  2. a sabotaged register FAILS CLOSED (exit 2), never silently passes,
  3. a clean governance doc PASSES.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

from directive_register import (  # noqa: E402
    DirectiveRegisterError,
    UnknownDirectiveError,
    get_directive,
    load_register,
)
from directive_register_sync import run as sync_run, scan_file  # noqa: E402

REAL_REGISTER = (
    Path(__file__).resolve().parent.parent.parent
    / "BRAIN" / "01-GOVERNANCE" / "directive-register.json"
)

MINI_REGISTER = [
    {"id": "D8", "title": "Calibration Drift Detection", "source_issue": 1354,
     "source_comment": "6100512641", "owner": "naya5", "status": "NOT_STARTED",
     "evidence_pr": None, "wave": 6},
    {"id": "D32", "title": "Evidence-Bounded Uncertainty Propagation",
     "source_issue": 2175, "source_comment": "6101361594", "owner": "naya2",
     "status": "BUILT_AS_CODE", "evidence_pr": 2224, "wave": 6},
]


@pytest.fixture()
def mini_repo(tmp_path):
    reg = tmp_path / "register.json"
    reg.write_text(json.dumps(MINI_REGISTER), encoding="utf-8")
    doc = tmp_path / "doc.md"
    return tmp_path, reg, doc


# ---------- loader: fail-closed ----------

def test_loader_loads_real_register():
    directives = load_register(REAL_REGISTER)
    assert len(directives) == 58
    entry = get_directive(directives, "D32")
    assert entry["title"] == "Evidence-Bounded Uncertainty Propagation"
    assert entry["owner"] == "naya2"


def test_loader_missing_file_fails_closed(tmp_path):
    with pytest.raises(DirectiveRegisterError):
        load_register(tmp_path / "nope.json")


def test_loader_invalid_json_fails_closed(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(DirectiveRegisterError):
        load_register(bad)


def test_loader_wrong_shape_fails_closed(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"D8": {}}), encoding="utf-8")
    with pytest.raises(DirectiveRegisterError):
        load_register(bad)


def test_loader_duplicate_ids_fail_closed(tmp_path):
    dup = tmp_path / "dup.json"
    dup.write_text(json.dumps(MINI_REGISTER + [MINI_REGISTER[0]]), encoding="utf-8")
    with pytest.raises(DirectiveRegisterError, match="[Dd]uplicate"):
        load_register(dup)


def test_loader_missing_keys_fail_closed(tmp_path):
    short = tmp_path / "short.json"
    entry = dict(MINI_REGISTER[0])
    del entry["owner"]
    short.write_text(json.dumps([entry]), encoding="utf-8")
    with pytest.raises(DirectiveRegisterError, match="[Mm]issing keys"):
        load_register(short)


def test_unknown_directive_never_synthesized():
    directives = load_register(REAL_REGISTER)
    with pytest.raises(UnknownDirectiveError):
        get_directive(directives, "D70")
    with pytest.raises(UnknownDirectiveError):
        get_directive(directives, "D999")


# ---------- scanner ----------

def test_clean_doc_passes(mini_repo):
    _, reg, doc = mini_repo
    doc.write_text("# Note\n\nPer D32, uncertainty must stay evidence-bounded.\n", encoding="utf-8")
    directives = load_register(reg)
    violations, _ = scan_file(doc, directives)
    assert violations == []


def test_phantom_directive_reference_fails_with_witness(mini_repo):
    """NEGATIVE CONTROL: D70 is not registered -> must be a violation naming D70."""
    _, reg, doc = mini_repo
    doc.write_text("# Note\n\nPer D70, we proceed.\n", encoding="utf-8")
    directives = load_register(reg)
    violations, _ = scan_file(doc, directives)
    assert len(violations) == 1
    assert "D70" in violations[0]
    assert str(doc) in violations[0]  # witness names the file


def test_d1_d7_are_out_of_scope_not_violations(mini_repo):
    _, reg, doc = mini_repo
    doc.write_text("# Note\n\nD6 governs reopening; D32 governs uncertainty.\n", encoding="utf-8")
    directives = load_register(reg)
    violations, notes = scan_file(doc, directives)
    assert violations == []
    assert any("D6" in n for n in notes)


def test_multiple_violations_all_reported(mini_repo):
    _, reg, doc = mini_repo
    doc.write_text("D70 here.\nAnd D999 there.\nD32 is fine.\n", encoding="utf-8")
    directives = load_register(reg)
    violations, _ = scan_file(doc, directives)
    assert len(violations) == 2
    assert any("D70" in v for v in violations)
    assert any("D999" in v for v in violations)


def test_sabotaged_register_fails_closed_never_passes(tmp_path, capsys):
    """NEGATIVE CONTROL: corrupt register -> exit 2, never exit 0."""
    bad = tmp_path / "register.json"
    bad.write_text("CORRUPT{{{", encoding="utf-8")
    doc = tmp_path / "doc.md"
    doc.write_text("Per D32, all good.\n", encoding="utf-8")
    rc = sync_run(tmp_path, [doc], bad)
    assert rc == 2
    assert "FAIL-CLOSED" in capsys.readouterr().err


def test_run_exit_codes_end_to_end(tmp_path, capsys):
    reg = tmp_path / "register.json"
    reg.write_text(json.dumps(MINI_REGISTER), encoding="utf-8")
    clean = tmp_path / "clean.md"
    clean.write_text("Per D32.\n", encoding="utf-8")
    dirty = tmp_path / "dirty.md"
    dirty.write_text("Per D70.\n", encoding="utf-8")

    assert sync_run(tmp_path, [clean], reg) == 0
    capsys.readouterr()
    assert sync_run(tmp_path, [dirty], reg) == 1
    out = capsys.readouterr().out
    assert "D70" in out


def test_cli_against_real_register_and_real_governance_docs():
    """LIVE-FIRE (read-only): the real register against real BRAIN/01-GOVERNANCE docs
    that reference directives. Whatever it finds is reported honestly."""
    gov = REAL_REGISTER.parent
    docs = [p for p in gov.rglob("*.md") if p.name != "directive-register.json"]
    assert docs, "expected governance docs to scan"
    directives = load_register(REAL_REGISTER)
    all_violations = []
    for doc in docs:
        violations, _ = scan_file(doc, directives)
        all_violations.extend(violations)
    # Honest report: print what was found so the run log shows it.
    print(f"\nlive-fire: scanned={len(docs)} violations={len(all_violations)}")
    for v in all_violations[:20]:
        print("  " + v)
    # The gate must be green on the current tree: any violation here is a
    # REAL stale reference the wire run must fix or explicitly disposition.
    assert all_violations == [], (
        f"{len(all_violations)} stale directive reference(s) in BRAIN/01-GOVERNANCE/"
    )

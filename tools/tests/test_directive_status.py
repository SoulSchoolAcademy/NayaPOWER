"""Tests for the directive status-promotion mechanism (tools/directive_status.py).

These are REAL asserts with negative controls. The mechanism is proven only if:
  1. a one-rung promotion with evidence SUCCEEDS and leaves all other entries
     byte-identical (the diff is confined to the promoted entry's status/evidence),
  2. a rung-skipping promotion is REFUSED with the file untouched,
  3. promotion to ENFORCED without a live gate is REFUSED,
  4. a phantom gate path is REFUSED,
  5. unknown/malformed directive ids FAIL CLOSED (nothing written),
  6. demotion without a reason is REFUSED,
  7. every refusal leaves the register file byte-identical.

The fixture is a copy of the REAL register (58 directives) — the tests run
against the true shape, not a toy.
"""

import difflib
import io
import json
import shutil
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

import directive_register as reg  # noqa: E402
import directive_status as ds  # noqa: E402

REAL_REGISTER = (
    Path(__file__).resolve().parent.parent.parent
    / "BRAIN"
    / "01-GOVERNANCE"
    / "directive-register.json"
)

REAL_GATE = ".github/workflows/directive-register-sync.yml"


@pytest.fixture()
def register_copy(tmp_path):
    """A private copy of the real register. Tests must never touch the real one."""
    assert REAL_REGISTER.is_file(), "real register missing — fixture cannot run"
    dest = tmp_path / "directive-register.json"
    shutil.copy2(REAL_REGISTER, dest)
    return dest


def read_bytes(p: Path) -> bytes:
    return p.read_bytes()


def changed_lines(before: bytes, after: bytes) -> list[str]:
    return [
        ln
        for ln in difflib.unified_diff(
            before.decode("utf-8").splitlines(), after.decode("utf-8").splitlines()
        )
        if (ln.startswith("+") or ln.startswith("-")) and not ln.startswith(("+++", "---"))
    ]


def entry(directives, did):
    return reg.get_directive(directives, did)


# ---------------------------------------------------------------- ladder


def test_ladder_order_is_fixed():
    assert ds.LADDER == ("NOT_STARTED", "BUILDING", "BUILT_AS_CODE", "ENFORCED")
    assert ds.next_rung("NOT_STARTED") == "BUILDING"
    assert ds.next_rung("BUILT_AS_CODE") == "ENFORCED"
    assert ds.next_rung("ENFORCED") is None


# ---------------------------------------------------------------- promote: happy path


def test_promote_one_rung_with_evidence(register_copy):
    directives = reg.load_register(register_copy)
    before = entry(directives, "D8")
    assert before["status"] == "NOT_STARTED"

    ds.promote_entry(before, "BUILDING", evidence_pr=2228)
    ds.save_register(register_copy, directives)

    reloaded = reg.load_register(register_copy)
    assert len(reloaded) == 58
    d8 = entry(reloaded, "D8")
    assert d8["status"] == "BUILDING"
    assert d8["evidence_pr"] == 2228
    # every other entry semantically identical
    for e in reloaded:
        if e["id"] != "D8":
            orig = entry(reg.load_register(REAL_REGISTER), e["id"])
            assert e == orig


def test_promote_diff_confined_to_status_and_evidence(register_copy):
    before_bytes = read_bytes(register_copy)
    directives = reg.load_register(register_copy)
    ds.promote_entry(entry(directives, "D8"), "BUILDING", evidence_pr=2228)
    ds.save_register(register_copy, directives)
    after_bytes = read_bytes(register_copy)

    lines = changed_lines(before_bytes, after_bytes)
    assert lines, "a promotion must change the file"
    for ln in lines:
        assert '"status"' in ln or '"evidence_pr"' in ln, f"unexpected diff line: {ln}"


def test_promote_to_enforced_with_real_gate(register_copy):
    directives = reg.load_register(register_copy)
    d32 = entry(directives, "D32")
    assert d32["status"] == "BUILT_AS_CODE"
    ds.promote_entry(d32, "ENFORCED", evidence_pr=2224, gate=REAL_GATE)
    ds.save_register(register_copy, directives)
    assert entry(reg.load_register(register_copy), "D32")["status"] == "ENFORCED"


# ---------------------------------------------------------------- promote: refusals (negative controls)


def test_promote_skipping_rung_refused_and_file_untouched(register_copy):
    before_bytes = read_bytes(register_copy)
    directives = reg.load_register(register_copy)
    with pytest.raises(ds.StatusError, match="BUILDING"):
        ds.promote_entry(entry(directives, "D8"), "BUILT_AS_CODE", evidence_pr=2228)
    assert read_bytes(register_copy) == before_bytes


def test_promote_to_enforced_without_gate_refused(register_copy):
    before_bytes = read_bytes(register_copy)
    directives = reg.load_register(register_copy)
    with pytest.raises(ds.StatusError, match="--gate"):
        ds.promote_entry(entry(directives, "D32"), "ENFORCED", evidence_pr=2224)
    assert read_bytes(register_copy) == before_bytes


@pytest.fixture()
def fake_repo(tmp_path):
    """A minimal repo-shaped dir: BRAIN/ + register copy, so gate paths resolve."""
    gov = tmp_path / "BRAIN" / "01-GOVERNANCE"
    gov.mkdir(parents=True)
    dest = gov / "directive-register.json"
    shutil.copy2(REAL_REGISTER, dest)
    return tmp_path, dest


def test_promote_to_enforced_with_phantom_gate_path_refused(fake_repo):
    _, register_copy = fake_repo
    before_bytes = read_bytes(register_copy)
    repo = reg.repo_root(register_copy.resolve())
    # unit level: the path check itself refuses phantom paths
    with pytest.raises(ds.StatusError, match="does not exist"):
        ds.validate_gate(".github/workflows/does-not-exist.yml", repo)
    # CLI level: a phantom gate path refuses with exit 1 and writes nothing
    code, _ = run_cli(["--register", str(register_copy),
                       "promote", "D32", "--to", "ENFORCED",
                       "--evidence-pr", "2224",
                       "--gate", ".github/workflows/does-not-exist.yml"])
    assert code == 1
    assert read_bytes(register_copy) == before_bytes


def test_cli_promote_to_enforced_with_existing_gate(fake_repo):
    repo_root, register_copy = fake_repo
    gate_rel = ".github/workflows/directive-register-sync.yml"
    gate_path = repo_root / gate_rel
    gate_path.parent.mkdir(parents=True)
    gate_path.write_text("# fake gate\n", encoding="utf-8")
    code, out = run_cli(["--register", str(register_copy),
                         "promote", "D32", "--to", "ENFORCED",
                         "--evidence-pr", "2224", "--gate", gate_rel])
    assert code == 0
    receipt = json.loads(out)
    assert receipt["to"] == "ENFORCED"
    assert receipt["gate"] == gate_rel
    assert entry(reg.load_register(register_copy), "D32")["status"] == "ENFORCED"


def test_promote_unknown_directive_fail_closed(register_copy):
    before_bytes = read_bytes(register_copy)
    directives = reg.load_register(register_copy)
    with pytest.raises(reg.UnknownDirectiveError):
        reg.get_directive(directives, "D999")
    assert read_bytes(register_copy) == before_bytes


def test_promote_malformed_id_fail_closed():
    with pytest.raises(reg.DirectiveRegisterError, match="Malformed"):
        reg.directive_number("X1")


def test_promote_bad_evidence_pr_refused(register_copy):
    before_bytes = read_bytes(register_copy)
    directives = reg.load_register(register_copy)
    for bad in (0, -3):
        with pytest.raises(ds.StatusError, match="positive PR number"):
            ds.promote_entry(entry(directives, "D8"), "BUILDING", evidence_pr=bad)
    assert read_bytes(register_copy) == before_bytes


def test_promote_unknown_target_status_refused(register_copy):
    before_bytes = read_bytes(register_copy)
    directives = reg.load_register(register_copy)
    with pytest.raises(ds.StatusError, match="Unknown target status"):
        ds.promote_entry(entry(directives, "D8"), "DONE", evidence_pr=2228)
    assert read_bytes(register_copy) == before_bytes


def test_promote_from_enforced_refused(register_copy):
    directives = reg.load_register(register_copy)
    d32 = entry(directives, "D32")
    ds.promote_entry(d32, "ENFORCED", evidence_pr=2224, gate=REAL_GATE)
    with pytest.raises(ds.StatusError, match="already ENFORCED"):
        ds.promote_entry(d32, "ENFORCED", evidence_pr=2224, gate=REAL_GATE)


def test_gate_path_escaping_repo_refused(fake_repo):
    repo, _ = fake_repo
    with pytest.raises(ds.StatusError, match="escapes the repo"):
        ds.validate_gate("../../etc/passwd", repo)


# ---------------------------------------------------------------- demote


def test_demote_requires_reason(register_copy):
    before_bytes = read_bytes(register_copy)
    directives = reg.load_register(register_copy)
    with pytest.raises(ds.StatusError, match="--reason"):
        ds.demote_entry(entry(directives, "D32"), "BUILDING", reason="  ")
    assert read_bytes(register_copy) == before_bytes


def test_demote_multi_rung_ok_and_clears_evidence_at_not_started(register_copy):
    directives = reg.load_register(register_copy)
    d32 = entry(directives, "D32")
    assert d32["evidence_pr"] == 2213
    ds.demote_entry(d32, "NOT_STARTED", reason="code reverted in #2300")
    ds.save_register(register_copy, directives)
    d32b = entry(reg.load_register(register_copy), "D32")
    assert d32b["status"] == "NOT_STARTED"
    assert d32b["evidence_pr"] is None  # stale evidence must not survive


def test_demote_keeps_evidence_while_code_remains(register_copy):
    directives = reg.load_register(register_copy)
    d32 = entry(directives, "D32")
    ds.promote_entry(d32, "ENFORCED", evidence_pr=2224, gate=REAL_GATE)
    ds.demote_entry(d32, "BUILT_AS_CODE", reason="gate workflow deleted in #2300")
    ds.save_register(register_copy, directives)
    d32b = entry(reg.load_register(register_copy), "D32")
    assert d32b["status"] == "BUILT_AS_CODE"
    assert d32b["evidence_pr"] == 2224  # the code (and its PR) still exists


def test_demote_upward_or_same_refused(register_copy):
    before_bytes = read_bytes(register_copy)
    directives = reg.load_register(register_copy)
    with pytest.raises(ds.StatusError, match="DOWN the ladder"):
        ds.demote_entry(entry(directives, "D8"), "BUILDING", reason="oops")
    with pytest.raises(ds.StatusError, match="DOWN the ladder"):
        ds.demote_entry(entry(directives, "D8"), "NOT_STARTED", reason="oops")
    assert read_bytes(register_copy) == before_bytes


# ---------------------------------------------------------------- fail-closed register handling


def test_corrupt_register_fail_closed(tmp_path):
    bad = tmp_path / "directive-register.json"
    bad.write_text("{ not json", encoding="utf-8")
    before = bad.read_bytes()
    with pytest.raises(reg.DirectiveRegisterError):
        reg.load_register(bad)
    assert bad.read_bytes() == before


def test_missing_register_fail_closed(tmp_path):
    with pytest.raises(reg.DirectiveRegisterError, match="not found"):
        reg.load_register(tmp_path / "nope.json")


# ---------------------------------------------------------------- CLI end to end


def run_cli(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = ds.main(argv)
    return code, buf.getvalue()


def test_cli_promote_receipt(register_copy):
    code, out = run_cli(["--register", str(register_copy),
                         "promote", "D8", "--to", "BUILDING",
                         "--evidence-pr", "2228", "--note", "lane signed in"])
    assert code == 0
    receipt = json.loads(out)
    assert receipt["action"] == "promote"
    assert receipt["directive_id"] == "D8"
    assert receipt["from"] == "NOT_STARTED"
    assert receipt["to"] == "BUILDING"
    assert receipt["evidence_pr"] == 2228
    assert receipt["at"].endswith("Z")
    assert entry(reg.load_register(register_copy), "D8")["status"] == "BUILDING"


def test_cli_promote_refused_exit_1_and_file_untouched(register_copy):
    before_bytes = read_bytes(register_copy)
    code, _ = run_cli(["--register", str(register_copy),
                       "promote", "D8", "--to", "BUILT_AS_CODE",
                       "--evidence-pr", "2228"])
    assert code == 1
    assert read_bytes(register_copy) == before_bytes


def test_cli_unknown_directive_exit_2(register_copy):
    code, _ = run_cli(["--register", str(register_copy),
                       "promote", "D999", "--to", "BUILDING",
                       "--evidence-pr", "2228"])
    assert code == 2


def test_cli_show(register_copy):
    code, out = run_cli(["--register", str(register_copy), "show", "D26"])
    assert code == 0
    shown = json.loads(out)
    assert shown["id"] == "D26"
    assert shown["status"] == "NOT_STARTED"


def test_cli_demote_receipt(register_copy):
    code, out = run_cli(["--register", str(register_copy),
                         "demote", "D32", "--to", "BUILDING",
                         "--reason", "re-audit requested"])
    assert code == 0
    receipt = json.loads(out)
    assert receipt["action"] == "demote"
    assert receipt["from"] == "BUILT_AS_CODE"
    assert receipt["to"] == "BUILDING"
    assert receipt["reason"] == "re-audit requested"


def test_cli_as_subprocess_against_real_repo_shape(tmp_path):
    """The CLI works from a cold subprocess on a real-shaped register copy."""
    dest = tmp_path / "directive-register.json"
    shutil.copy2(REAL_REGISTER, dest)
    proc = subprocess.run(
        [sys.executable, str(TOOLS / "directive_status.py"),
         "--register", str(dest),
         "promote", "D26", "--to", "BUILDING", "--evidence-pr", "2228"],
        capture_output=True, text=True, cwd=str(TOOLS.parent),
    )
    assert proc.returncode == 0, proc.stderr
    receipt = json.loads(proc.stdout)
    assert receipt["to"] == "BUILDING"
    assert entry(reg.load_register(dest), "D26")["evidence_pr"] == 2228

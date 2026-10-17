"""Battery for tools/check_ratified_claims.py.

Positive + negative + fail-closed controls. The instrument under test is
check(diff_text) / main(); assertions are on verdicts and exit codes, never on
prose.

Run: python3 -m pytest tests/test_check_ratified_claims.py -q
"""

import importlib.util
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_ratified_claims.py"

spec = importlib.util.spec_from_file_location("check_ratified_claims", TOOL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def diff_for(path: str, lines: list[str], old_path: str | None = None) -> str:
    old = old_path or path
    head = f"diff --git a/{old} b/{path}\n--- a/{old}\n+++ b/{path}\n@@ -1,1 +1,{len(lines)} @@\n"
    return head + "".join("+" + ln + "\n" for ln in lines)


def run_main(args: list[str]) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = mod.main(args)
    return code, buf.getvalue()


def run_check(diff: str) -> dict:
    return mod.check(diff)


# --- Positive controls: recorded claims PASS --------------------------------

def test_claim_with_marker_and_issue_ref_passes():
    d = diff_for("CONSTITUTION/0004-X.md", [
        "# Amendment X",
        "RATIFICATION-RECORD: Shawn Vibert (Human Director), #1354 comment 6056195765, 2026-10-08",
        "This amendment is RATIFIED.",
    ])
    r = run_check(d)
    assert r["pass"] is True and r["violations"] == []


def test_claim_with_marker_and_date_only_passes():
    d = diff_for("docs/law.md", [
        "RATIFICATION-RECORD: Shawn Vibert, verbal ratification 2026-10-05",
        "The Scorecard Law is RATIFIED as of that date.",
    ])
    r = run_check(d)
    assert r["pass"] is True


def test_lowercase_marker_passes():
    d = diff_for("docs/x.md", [
        "ratification-record: #1718 comment 1, 2026-10-08",
        "x was ratified.",
    ])
    assert run_check(d)["pass"] is True


def test_ratification_noun_with_record_passes():
    d = diff_for("docs/x.md", [
        "RATIFICATION-RECORD: Human Director, #9999, 2026-10-08",
        "This records the ratification of the protocol.",
    ])
    assert run_check(d)["pass"] is True


def test_no_claims_passes():
    d = diff_for("tools/other.py", ["# just code", "x = 1"])
    r = run_check(d)
    assert r["pass"] is True and r["files_scanned"] == 1


def test_empty_diff_passes():
    r = run_check("")
    assert r["pass"] is True and r["files_scanned"] == 0


# --- Negative controls: unrecorded claims FAIL --------------------------------

def test_bare_ratified_claim_fails():
    d = diff_for("docs/law.md", ["# Law", "This law is RATIFIED."])
    r = run_check(d)
    assert r["pass"] is False
    assert len(r["violations"]) == 1
    assert r["violations"][0]["path"] == "docs/law.md"


def test_ratification_claim_fails():
    d = diff_for("docs/law.md", ["We claim ratification of this protocol."])
    assert run_check(d)["pass"] is False


def test_marker_without_citation_fails():
    d = diff_for("docs/law.md", [
        "RATIFICATION-RECORD: someday, maybe",
        "This is RATIFIED.",
    ])
    r = run_check(d)
    assert r["pass"] is False
    assert "citation" in r["violations"][0]["reason"]


def test_context_and_removed_lines_ignored():
    d = ("diff --git a/docs/law.md b/docs/law.md\n--- a/docs/law.md\n+++ b/docs/law.md\n"
         "@@ -1,2 +1,2 @@\n context: this was RATIFIED long ago\n-old line RATIFIED\n+new line, no claim here\n")
    assert run_check(d)["pass"] is True


def test_multi_file_mixed_verdicts():
    good = diff_for("a.md", ["RATIFICATION-RECORD: #1234, 2026-10-08", "RATIFIED."])
    bad = diff_for("b.md", ["RATIFIED by me."])
    r = run_check(good + bad)
    assert r["pass"] is False
    assert [v["path"] for v in r["violations"]] == ["b.md"]


# --- Self-exemption: the machinery may speak of ratified claims ---------------

def test_tool_source_exempt_from_self_flag():
    tool_text = TOOL.read_text(encoding="utf-8").splitlines()
    d = diff_for("tools/check_ratified_claims.py", tool_text)
    assert run_check(d)["pass"] is True


# --- Fail-closed: UNKNOWN != PASS ---------------------------------------------

def test_unreadable_diff_input_fails_closed(tmp_path):
    missing = tmp_path / "no-such.diff"
    code, out = run_main(["--diff", f"@{missing}"])
    assert code == 1
    assert "FAIL" in out


def test_malformed_diff_still_parses_without_false_pass():
    # Garbage input must not produce a vacuous PASS on phantom content.
    # A stray '+++ ' header opens an (empty) file entry — no added lines,
    # so no claims can exist there; the verdict is honestly PASS.
    r = run_check("not a diff at all\n+++ nowhere\n")
    assert r["pass"] is True and r["violations"] == []
    # And a real claim smuggled outside diff framing is not an added line:
    r2 = run_check("RATIFIED by decree\n")
    assert r2["pass"] is True and r2["violations"] == []


def test_exit_code_contract_json_fail(tmp_path):
    p = tmp_path / "bad.diff"
    p.write_text(diff_for("x.md", ["it is RATIFIED"]), encoding="utf-8")
    code, out = run_main(["--diff", f"@{p}", "--json"])
    assert code == 1
    body = json.loads(out)
    assert body["pass"] is False
    assert body["violations"][0]["path"] == "x.md"


def test_exit_zero_on_pass_file(tmp_path):
    p = tmp_path / "ok.diff"
    p.write_text(diff_for("x.md", ["hello"]), encoding="utf-8")
    code, out = run_main(["--diff", f"@{p}", "--json"])
    assert code == 0
    assert json.loads(out)["pass"] is True


def test_exit_one_on_violation_file(tmp_path):
    p = tmp_path / "bad.diff"
    p.write_text(diff_for("x.md", ["it is RATIFIED"]), encoding="utf-8")
    code, out = run_main(["--diff", f"@{p}"])
    assert code == 1
    assert "FAIL" in out


def test_stdin_path(tmp_path):
    import subprocess
    p = tmp_path / "ok.diff"
    p.write_text(diff_for("x.md", ["hello"]), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(TOOL), "--diff", "-"],
        stdin=open(p, "rb"), capture_output=True, text=True,
    )
    assert proc.returncode == 0 and "PASS" in proc.stdout

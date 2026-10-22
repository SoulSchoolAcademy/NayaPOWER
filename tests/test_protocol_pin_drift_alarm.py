"""
Tests for the protocol pin-drift alarm (tools/protocol_pin.py).

The alarm is the watchdog form of the protocol pin: silent while
PROTOCOL.md matches its pinned fingerprints, loud — with both hashes
named — the moment the document moves without a deliberate re-pin.
Born of a real incident: on 2026-10-21 PR #2802 landed legitimate
protocol repairs with no re-pin and the boot gate refused cold boots
for a day before a seat noticed.

Positive AND negative controls, per the house pattern: the alarm must
fire on planted drift and must stay silent on matching bytes. The
clean controls here are real — pins are set to the crafted tree's own
fingerprints via monkeypatch (unit) or via a pin-patched copy of the
tool (CLI), the same way a ratified re-pin sets them in production.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from tools import protocol_pin as pp

REPO_ROOT = Path(__file__).resolve().parent.parent

PROTOCOL_TEXT = """# NAYA PROTOCOL

Ratified and amended by Shawn Vibert, 2026-10-20.

**0. DECLARE — WHO I AM.** Speak who you are.

**1. WAKE.** Establish identity from canonical sources.
"""


def _scratch_repo(tmp_path, text=PROTOCOL_TEXT):
    root = tmp_path / "repo"
    root.mkdir()
    (root / "PROTOCOL.md").write_text(text, encoding="utf-8")
    return root


def _pin_to_tree(monkeypatch, root):
    """Point the module pins at the scratch tree's own bytes — the
    test-time equivalent of a ratified re-pin."""
    fp = pp.protocol_fingerprints(str(root))
    monkeypatch.setattr(pp, "PROTOCOL_FILE_PIN", fp["sha256"])
    monkeypatch.setattr(pp, "STEP0_PIN", fp["step0_sha256"])
    return fp


# ---------------------------------------------------------------------------
# pin_drift_status — the data form
# ---------------------------------------------------------------------------

def test_no_drift_when_bytes_match_pins(tmp_path, monkeypatch):
    root = _scratch_repo(tmp_path)
    _pin_to_tree(monkeypatch, root)
    status = pp.pin_drift_status(str(root))
    assert status["readable"] is True
    assert status["drifted"] is False
    assert status["file"]["match"] is True
    assert status["step0"]["match"] is True
    assert pp.drift_alarm_line(status) == ""


def test_planted_drift_fires_with_both_hashes(tmp_path, monkeypatch):
    root = _scratch_repo(tmp_path)
    fp = _pin_to_tree(monkeypatch, root)
    with open(root / "PROTOCOL.md", "a", encoding="utf-8") as f:
        f.write("\nOne silent byte of drift.\n")
    status = pp.pin_drift_status(str(root))
    assert status["readable"] is True
    assert status["drifted"] is True
    assert status["file"]["match"] is False
    assert status["file"]["pinned"] == fp["sha256"]
    assert status["file"]["current"] != fp["sha256"]
    line = pp.drift_alarm_line(status)
    assert line.startswith("PIN-DRIFT-ALARM:")
    assert status["file"]["current"] in line
    assert fp["sha256"] in line
    assert "re-pin" in line


def test_step0_only_drift_is_named_separately(tmp_path, monkeypatch):
    root = _scratch_repo(tmp_path)
    _pin_to_tree(monkeypatch, root)
    text = (root / "PROTOCOL.md").read_text(encoding="utf-8")
    drifted = text.replace("Speak who you are.",
                           "Speak who you are, quietly edited.")
    (root / "PROTOCOL.md").write_text(drifted, encoding="utf-8")
    status = pp.pin_drift_status(str(root))
    assert status["drifted"] is True
    assert status["step0"]["match"] is False
    assert "Step 0 declaration sha256" in status["detail"]


def test_unreadable_protocol_fails_closed(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()  # no PROTOCOL.md at all
    status = pp.pin_drift_status(str(root))
    assert status["readable"] is False
    assert status["drifted"] is None
    assert "fail closed" in status["detail"]
    assert pp.drift_alarm_line(status) == ""


# ---------------------------------------------------------------------------
# check_drift_alarm — the gate-pattern wrapper
# ---------------------------------------------------------------------------

def test_wrapper_passes_on_matching_bytes(tmp_path, monkeypatch):
    root = _scratch_repo(tmp_path)
    _pin_to_tree(monkeypatch, root)
    verdict = pp.check_drift_alarm({"repo_root": str(root)})
    assert verdict["pass"] is True
    assert verdict["details"]["law"] == "PROTOCOL-PIN-DRIFT"


def test_wrapper_fails_on_drift_and_on_bad_record(tmp_path, monkeypatch):
    root = _scratch_repo(tmp_path)
    _pin_to_tree(monkeypatch, root)
    with open(root / "PROTOCOL.md", "a", encoding="utf-8") as f:
        f.write("drift\n")
    verdict = pp.check_drift_alarm({"repo_root": str(root)})
    assert verdict["pass"] is False
    assert verdict["reasons"][0].startswith("PIN-DRIFT-ALARM:")
    bad = pp.check_drift_alarm("not-a-dict")
    assert bad["pass"] is False
    assert bad["reasons"] == ["record is not a JSON object"]


# ---------------------------------------------------------------------------
# CLI — run a pin-patched copy of the tool against a scratch repo,
# exactly as a ratified re-pin would leave it in production.
# ---------------------------------------------------------------------------

def _cli_scratch(tmp_path, text=PROTOCOL_TEXT):
    root = _scratch_repo(tmp_path, text)
    tools_dir = root / "tools"
    tools_dir.mkdir()
    tool_copy = tools_dir / "protocol_pin.py"
    shutil.copy(REPO_ROOT / "tools" / "protocol_pin.py", tool_copy)
    fp = pp.protocol_fingerprints(str(root))
    src = tool_copy.read_text(encoding="utf-8")
    src, n1 = re.subn(r'PROTOCOL_FILE_PIN = \\\n\s*"[0-9a-f]{64}"',
                      'PROTOCOL_FILE_PIN = \\\n    "%s"' % fp["sha256"],
                      src)
    src, n2 = re.subn(r'STEP0_PIN = \\\n\s*"[0-9a-f]{64}"',
                      'STEP0_PIN = \\\n    "%s"' % fp["step0_sha256"],
                      src)
    assert n1 == 1 and n2 == 1, "pin constants not found in tool copy"
    tool_copy.write_text(src, encoding="utf-8")
    return root, tool_copy, fp


def _run_cli(tool_copy, root, *extra):
    return subprocess.run(
        [sys.executable, str(tool_copy), "--drift-alarm",
         "--repo-root", str(root), *extra],
        capture_output=True, text=True, timeout=60)


def test_cli_silent_on_clean_tree(tmp_path):
    root, tool_copy, _fp = _cli_scratch(tmp_path)
    run = _run_cli(tool_copy, root)
    assert run.returncode == 0
    assert run.stdout == ""  # silent means silent
    run_json = _run_cli(tool_copy, root, "--json")
    assert run_json.returncode == 0
    assert json.loads(run_json.stdout)["alarm"] is False


def test_cli_fires_on_planted_drift(tmp_path):
    root, tool_copy, fp = _cli_scratch(tmp_path)
    with open(root / "PROTOCOL.md", "a", encoding="utf-8") as f:
        f.write("\nPlanted drift for the alarm proof.\n")
    run = _run_cli(tool_copy, root)
    assert run.returncode == 1
    assert run.stdout.startswith("PIN-DRIFT-ALARM:")
    assert fp["sha256"] in run.stdout  # the pinned hash is named
    run_json = _run_cli(tool_copy, root, "--json")
    assert run_json.returncode == 1
    payload = json.loads(run_json.stdout)
    assert payload["alarm"] is True
    assert payload["status"]["drifted"] is True


def test_cli_unreadable_tree_exits_2(tmp_path):
    root, tool_copy, _fp = _cli_scratch(tmp_path)
    (root / "PROTOCOL.md").unlink()
    run = _run_cli(tool_copy, root)
    assert run.returncode == 2
    assert run.stdout == ""

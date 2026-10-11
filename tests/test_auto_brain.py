"""Tests for SN-AUTO-BRAIN's mechanical gate (tools/protocol/checks/auto_brain.py).

The gate verifies the auto-brain surface: every law in
kernel/protocol/protocol_manifest.json binds to a real, executable check;
boot-gate modules reference manifests that exist; the boot gate runs green.

Red -> green: each failure mode is planted in a scratch tree (or a scratch
manifest) and must FAIL naming the law, the file, and the fix. The healthy
tree must PASS.
"""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "tools" / "protocol" / "checks" / "auto_brain.py"
MANIFEST = ROOT / "kernel" / "protocol" / "protocol_manifest.json"


def _load_check():
    """Load the check module from its file path (the suite's established
    pattern — a bare `import auto_brain` trips the CI-dependency guard)."""
    spec = importlib.util.spec_from_file_location("auto_brain", str(CHECK))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


auto_brain = _load_check()


@pytest.fixture
def manifest():
    return json.loads(MANIFEST.read_text())


def test_check_module_exists_and_registered(manifest):
    """The manifest must register SN-AUTO-BRAIN with a real check file."""
    law = next(l for l in manifest["laws"] if l["id"] == "SN-AUTO-BRAIN")
    assert law["check"] == "tools/protocol/checks/auto_brain.py"
    assert (ROOT / law["check"]).is_file()


def test_check_passes_on_healthy_tree():
    """Full gate on the real checkout: PASS (proves green, not just red)."""
    result = auto_brain.check({"repo_root": str(ROOT)})
    assert result["pass"] is True, result["reasons"]
    assert result["details"]["laws_total"] == 18


def test_dead_check_binding_fails_naming_law_and_file(tmp_path, manifest):
    """A law whose check points at a missing file FAILS, naming both."""
    manifest["laws"][0]["check"] = "tools/protocol/checks/does_not_exist.py"
    reasons, _ = auto_brain._check_bindings(ROOT, manifest["laws"])
    assert reasons, "dead binding must fail"
    text = " ".join(reasons)
    assert manifest["laws"][0]["id"] in text
    assert "does_not_exist.py" in text
    assert "protocol_manifest.json" in text  # the fix names the file to edit


def test_dead_machine_check_binding_fails(tmp_path, manifest):
    law = next(l for l in manifest["laws"] if l["id"] == "SN-NO-EGO")
    law["machine_check"] = "kernel/protocol/checks/gone.py"
    reasons, _ = auto_brain._check_bindings(ROOT, manifest["laws"])
    assert reasons
    assert "SN-NO-EGO" in " ".join(reasons)
    assert "gone.py" in " ".join(reasons)


def test_null_check_with_honest_human_label_passes(manifest):
    """SN-0500 (Think Before You Act) is honestly human — not fake-mechanized."""
    law = next(l for l in manifest["laws"] if l["id"] == "SN-0500")
    assert law["check"] is None
    reasons, _ = auto_brain._check_bindings(ROOT, [law])
    assert reasons == [], f"honest human label must pass: {reasons}"


def test_null_check_with_path_like_label_fails(manifest):
    """A null check whose 'label' looks like a module path is a phantom reference."""
    law = {"id": "SN-FAKE", "name": "Fake", "check": None,
           "enforcement": "some/phantom_module.py"}
    reasons, _ = auto_brain._check_bindings(ROOT, [law])
    assert reasons
    assert "SN-FAKE" in " ".join(reasons)


def test_null_check_with_no_label_fails():
    law = {"id": "SN-FAKE2", "name": "Fake2", "check": None}
    reasons, _ = auto_brain._check_bindings(ROOT, [law])
    assert reasons
    assert "SN-FAKE2" in " ".join(reasons)


def test_malformed_binding_fails_in_plain_words():
    """A binding that is not a string fails closed with words, not a traceback."""
    law = {"id": "SN-FAKE3", "name": "Fake3", "check": 123}
    reasons, details = auto_brain._check_bindings(ROOT, [law])
    assert reasons
    assert "SN-FAKE3" in " ".join(reasons)
    assert details["bindings"]["SN-FAKE3"] == "MALFORMED"


def test_non_dict_law_entry_fails_in_plain_words():
    reasons, _ = auto_brain._check_bindings(ROOT, ["not-a-law"])
    assert reasons
    assert "not an object" in " ".join(reasons)


def test_broken_boot_gate_manifest_reference_fails(tmp_path):
    """A *_gate.py whose MANIFEST_PATH points nowhere FAILS (the dead-duplicate class)."""
    (tmp_path / "tools" / "protocol").mkdir(parents=True)
    (tmp_path / "tools" / "protocol" / "broken_gate.py").write_text(
        "from pathlib import Path\n"
        "ROOT = Path(__file__).resolve().parents[2]\n"
        "MANIFEST_PATH = ROOT / 'nope' / 'missing.json'\n"
    )
    reasons, _ = auto_brain._check_boot_gate_manifests(tmp_path, [])
    assert reasons
    text = " ".join(reasons)
    assert "broken_gate.py" in text
    assert "missing.json" in text


def test_gate_module_missing_main_fails_pattern(tmp_path):
    """A check binding that is not a real gate (no main()) FAILS the pattern."""
    mod = tmp_path / "half_gate.py"
    mod.write_text("def check(record):\n    return {'pass': True, 'reasons': [], 'details': {}}\n")
    laws = [{"id": "SN-X", "name": "X", "check": "half_gate.py"}]
    reasons, _ = auto_brain._check_gates_executable(tmp_path, laws)
    assert reasons
    assert "main()" in " ".join(reasons)


def test_fail_open_check_module_fails(tmp_path):
    """A check whose CLI exits 0 on a malformed record is fail-open: FAIL."""
    mod = tmp_path / "failopen_gate.py"
    mod.write_text(
        "def check(record):\n"
        "    return {'pass': True, 'reasons': [], 'details': {}}\n"
        "def main():\n"
        "    print('PASS')\n"
        "    return 0\n"
        "if __name__ == '__main__':\n"
        "    raise SystemExit(main())\n"
    )
    laws = [{"id": "SN-Y", "name": "Y", "check": "failopen_gate.py"}]
    reasons, _ = auto_brain._check_gates_executable(tmp_path, laws)
    assert reasons
    assert "fail-open" in " ".join(reasons)


def test_machine_check_needs_entry_point(tmp_path):
    """A machine_check module with no validation entry point FAILS."""
    mod = tmp_path / "empty_mc.py"
    mod.write_text("VALUE = 42\n")
    laws = [{"id": "SN-Z", "name": "Z", "machine_check": "empty_mc.py"}]
    reasons, _ = auto_brain._check_machine_checks(tmp_path, laws)
    assert reasons
    assert "SN-Z" in " ".join(reasons)


def test_boot_gate_green_on_real_tree():
    """The canonical boot gate runs green end-to-end for a probe agent."""
    reasons, details = auto_brain._check_boot_gate_green(ROOT)
    assert reasons == [], f"boot gate must be green: {reasons}"
    assert "green" in details.get("boot_gate", "")


def test_cli_passes_on_healthy_tree():
    proc = subprocess.run(
        [sys.executable, str(CHECK), "--record", "{}"],
        capture_output=True, text=True, timeout=300, cwd=ROOT,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS" in proc.stdout


def test_cli_fails_closed_on_garbage_record():
    proc = subprocess.run(
        [sys.executable, str(CHECK), "--record", "###not-json###"],
        capture_output=True, text=True, timeout=60, cwd=ROOT,
    )
    assert proc.returncode == 1
    assert "FAIL" in proc.stdout


def test_cli_fails_closed_on_non_checkout(tmp_path):
    proc = subprocess.run(
        [sys.executable, str(CHECK), "--record",
         json.dumps({"repo_root": str(tmp_path)})],
        capture_output=True, text=True, timeout=60, cwd=ROOT,
    )
    assert proc.returncode == 1
    assert "not a NayaPOWER checkout" in proc.stdout

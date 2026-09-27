import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json"
VALIDATOR = ROOT / "scripts/verify-nine-master-nodes.py"

def run_validator(path):
    # Use the interpreter running the tests, never a bare "python3".
    # On Windows hosts "python3" resolves to the Microsoft Store app-execution
    # alias stub and exits 9009, which made this gate report a manifest defect
    # that did not exist. The kernel gate must not be host-dependent.
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        text=True,
        capture_output=True,
    )

class NineMasterNodeKernelTests(unittest.TestCase):
    def test_manifest_passes(self):
        result = run_validator(MANIFEST)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_duplicate_node_fails(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        data["nodes"].append(data["nodes"][0])
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad.json"
            bad.write_text(json.dumps(data), encoding="utf-8")
            result = run_validator(bad)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exactly 9", result.stderr)

    def test_missing_contract_owner_fails(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        data["contract_primary_ownership"].pop("26")
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad.json"
            bad.write_text(json.dumps(data), encoding="utf-8")
            result = run_validator(bad)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("00-26", result.stderr)

    def test_safety_invariants_are_mandatory(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        text = " ".join(data["global_invariants"]["must_not"]).lower()
        self.assertIn("self-authorize", text)
        self.assertIn("self-ratify", text)
        self.assertIn("competing canonical intelligence store", text)


    def test_validator_is_invocable_on_this_host(self):
        """Regression: a missing interpreter must not masquerade as a bad kernel.

        Exit 9009 (command not found) means the GATE is broken, not the kernel.
        Without this test the Windows "python3" Store-alias stub silently turned
        a passing kernel into 3 apparent failures.
        """
        result = run_validator(MANIFEST)
        self.assertNotEqual(
            result.returncode, 9009,
            "validator could not be launched (9009 = interpreter not found); "
            "the gate is broken, which is not the same as an invalid kernel",
        )
        self.assertTrue(
            os.path.exists(VALIDATOR), f"validator missing at {VALIDATOR}"
        )
        self.assertTrue(sys.executable, "no interpreter for this test run")

    def test_valid_kernel_and_invalid_kernel_are_distinguishable(self):
        """A real conformance failure must not look like a broken gate."""
        good = run_validator(MANIFEST)
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        data["nodes"] = data["nodes"][:8]
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad.json"
            bad.write_text(json.dumps(data), encoding="utf-8")
            invalid = run_validator(bad)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertNotEqual(invalid.returncode, 0)
        # The invalid case must fail on kernel content, with an explanation.
        self.assertIn("exactly 9", invalid.stderr)
        self.assertNotEqual(invalid.returncode, 9009)

    def test_runtime_loader_is_bound_to_the_canonical_nine(self):
        source = (ROOT / "supabase/functions/nayanet-compound-intelligence/index.ts").read_text(encoding="utf-8")
        for node_id in [f"IB-{n:06d}" for n in range(1233, 1242)]:
            self.assertIn(node_id, source)
        self.assertIn("loadMasterNodeKernel", source)
        self.assertIn('"kernel_boot"', source)
        self.assertIn('"KERNEL_ACTIVE_STRUCTURAL"', source)
        self.assertIn('"MASTER_NODE_KERNEL_INCOMPLETE:"', source)
        self.assertIn('"MASTER_NODE_KERNEL_INVALID:"', source)

if __name__ == "__main__":
    unittest.main()

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json"
VALIDATOR = ROOT / "scripts/verify-nine-master-nodes.py"

def run_validator(path):
    return subprocess.run(
        ["python3", str(VALIDATOR), str(path)],
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


    def test_runtime_loader_is_bound_to_the_canonical_nine(self):
        source = (ROOT / "supabase/functions/nayanet-compound-intelligence/index.ts").read_text(encoding="utf-8")
        for node_id in [f"IB-{n:06d}" for n in range(1233, 1242)]:
            self.assertIn(node_id, source)
        self.assertIn("loadMasterNodeKernel", source)
        self.assertIn('"kernel_boot"', source)
        self.assertIn('"KERNEL_ACTIVE_STRUCTURAL"', source)
        self.assertIn('"MASTER_NODE_KERNEL_INCOMPLETE:"', source)
        self.assertIn('"MASTER_NODE_KERNEL_INVALID:"', source)
        self.assertIn('const MASTER_NODE_ACCESS_SCOPE = "SYSTEM_AUTHENTICATED";', source)
        self.assertIn('admin.from("nayanet_intelligent_blocks")', source)
        self.assertIn('.eq("owner_scope", MASTER_NODE_ACCESS_SCOPE)', source)
        self.assertIn('node.content?.classification !== "system_intelligence"', source)
        loader_start = source.index("async function loadMasterNodeKernel")
        loader_end = source.index("async function restore", loader_start)
        loader = source[loader_start:loader_end]
        self.assertNotIn('.eq("owner_id", userId)', loader)
        self.assertIn('"access_scope"', json.dumps(json.loads(MANIFEST.read_text(encoding="utf-8"))))
        self.assertIn('from "../../../n9_kernel_decision.mjs"', source)
        self.assertIn('evaluateNineNodeKernel', source)
        self.assertIn('case "kernel_decide"', source)
        self.assertIn('masterKernel.nodes', source)

if __name__ == "__main__":
    unittest.main()

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

# Load the sibling assemble.py by explicit path under a unique module name.
# A bare `from assemble import assemble` resolves through sys.modules, which
# full-suite collection has already populated with the unrelated assembler at
# HUB/design-system/tools/smart-builder/assemble.py (imported first by
# functions/tests/test_composable_templates.py) — that collision interrupted
# pytest collection repo-wide. The explicit path load is immune to it.
_ASSEMBLE_SPEC = importlib.util.spec_from_file_location(
    "smart_builder_assemble", Path(__file__).resolve().parent / "assemble.py"
)
_ASSEMBLE_MODULE = importlib.util.module_from_spec(_ASSEMBLE_SPEC)
sys.modules["smart_builder_assemble"] = _ASSEMBLE_MODULE
_ASSEMBLE_SPEC.loader.exec_module(_ASSEMBLE_MODULE)
assemble = _ASSEMBLE_MODULE.assemble


class AssemblerTests(unittest.TestCase):
    def setup_fixture(self, root: Path):
        library = root / "library"
        (library / "smart-blocks").mkdir(parents=True)
        (library / "smart-blocks/manifest.json").write_text(json.dumps({
            "blocks": [{
                "id": "button", "html_file": "smart-blocks/button.html",
                "needs": ["smart-blocks/tokens.css"], "js_needed": False
            }]
        }), encoding="utf-8")
        (library / "smart-blocks/REGISTRY.md").write_text("# registry", encoding="utf-8")
        (library / "smart-blocks/button.html").write_text('<button class="sample">Go</button>', encoding="utf-8")
        (library / "smart-blocks/tokens.css").write_text("body{color:white}", encoding="utf-8")
        (library / "smart-blocks/icons.svg").write_text('<svg aria-hidden="true"><defs></defs></svg>', encoding="utf-8")
        contract = root / "contract.json"
        contract.write_text(json.dumps({
            "schema_version": "naya-smart-builder-page-contract-v1",
            "contract_id": "test",
            "title": "Test page",
            "description": "Test",
            "source_registry": "smart-blocks/manifest.json",
            "source_ref": "fixture",
            "sections": [{"id": "actions", "title": "Actions", "block_ids": ["button"]}]
        }), encoding="utf-8")
        return library, contract

    def test_assembles_resolved_block_and_records_hashes(self):
        with tempfile.TemporaryDirectory() as d:
            library, contract = self.setup_fixture(Path(d))
            html, receipt = assemble(contract, library)
            self.assertIn('data-block-id="button"', html)
            self.assertIn('<button class="sample">Go</button>', html)
            self.assertEqual(receipt["status"], "ASSEMBLED_NOT_VISUALLY_VERIFIED")
            self.assertTrue(receipt["verification"]["all_declared_dependencies_exist"])
            self.assertEqual(len(receipt["selected_block_ids"]), 1)
            self.assertEqual(len(receipt["output_sha256"]), 64)

    def test_unknown_block_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            library, contract = self.setup_fixture(Path(d))
            value = json.loads(contract.read_text(encoding="utf-8"))
            value["sections"][0]["block_ids"] = ["missing-block"]
            contract.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unresolved block id"):
                assemble(contract, library)

    def test_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            library, contract = self.setup_fixture(Path(d))
            value = json.loads(contract.read_text(encoding="utf-8"))
            value["sections"][0]["block_ids"] = ["button"]
            contract.write_text(json.dumps(value), encoding="utf-8")
            manifest = json.loads((library / "smart-blocks/manifest.json").read_text(encoding="utf-8"))
            manifest["blocks"][0]["needs"] = ["../../outside.css"]
            (library / "smart-blocks/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "escapes library root"):
                assemble(contract, library)


if __name__ == "__main__":
    unittest.main()

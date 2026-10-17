import json
import unittest
from materialize_template import materialize


class TemplateMaterializerTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads(open("../../HUB/contracts/smart-builder-template-catalog-v1.json", encoding="utf-8").read())
        self.manifest = json.loads(open("../../.library-source/smart-blocks/manifest.json", encoding="utf-8").read())

    def test_twelve_templates_exist_and_all_ids_resolve(self):
        self.assertEqual(len(self.catalog["templates"]), 12)
        ids = {b["id"] for b in self.manifest["blocks"]}
        for template in self.catalog["templates"]:
            for section in template["sections"]:
                for block_id in section["block_ids"]:
                    self.assertIn(block_id, ids, f"{template['id']} -> {block_id}")

    def test_materializes_contract_with_module_states(self):
        contract = materialize(self.catalog, self.manifest, "my-personal-world", mode="preview")
        self.assertEqual(contract["schema_version"], "naya-smart-builder-page-contract-v1")
        self.assertEqual(contract["template_id"], "my-personal-world")
        self.assertTrue(contract["modules"])
        self.assertTrue(any(m["status"] == "not_wired" for m in contract["modules"]))

    def test_publish_fails_closed_for_unwired_default_modules(self):
        with self.assertRaisesRegex(ValueError, "publish requires verified modules"):
            materialize(self.catalog, self.manifest, "my-personal-world", mode="publish")

    def test_unknown_template_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Unknown or duplicate template id"):
            materialize(self.catalog, self.manifest, "made-up-template")


if __name__ == "__main__":
    unittest.main()

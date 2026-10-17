import json
import tempfile
import unittest
from pathlib import Path

from build_library_inventory import build_inventory, gallery_html


class LibraryInventoryTests(unittest.TestCase):
    def fixture(self, root: Path):
        main = root / "repo"
        canonical = root / "canonical"
        (main / "BRAIN/10-INTERFACES/DESIGN-BLOCKS").mkdir(parents=True)
        (canonical / "smart-blocks").mkdir(parents=True)
        (main / "HUB").mkdir()
        (main / "BRAIN/10-INTERFACES/DESIGN-BLOCKS/naya-design-catalog.json").write_text(
            json.dumps({"total_blocks": 1, "blocks": [{
                "id": "button", "name": "Button", "category": "buttons",
                "job": "Primary action", "when_to_use": "Act",
                "selectors": [".btn"], "files": {"specimen": "specimen.html"}
            }]}), encoding="utf-8")
        (canonical / "smart-blocks/manifest.json").write_text(
            json.dumps({"blocks": [{
                "id": "smart-tabs", "name": "Smart Tabs", "category": "navigation",
                "html_file": "smart-blocks/tabs.html", "css_file": "smart-blocks/tabs.css",
                "needs": ["smart-blocks/tokens.css"], "tier": "canonical"
            }]}), encoding="utf-8")
        (canonical / "smart-blocks/REGISTRY.md").write_text("# Registry\n", encoding="utf-8")
        gallery = main / "HUB/SMART-BUILDER-LIBRARY.html"
        gallery.write_text(
            '<div class="num">91</div><div class="num">58</div><div class="num">149</div>'
            '<div class="num">31</div><select id="category" aria-label="Filter">'
            '<option value="">All categories</option></select>'
            '<script>const items=[]; const q=document.getElementById(\\'q\\')</script>',
            encoding="utf-8")
        return main, canonical, gallery

    def test_source_counts_remain_separate_and_composite_ids_are_unique(self):
        with tempfile.TemporaryDirectory() as d:
            main, canonical, _ = self.fixture(Path(d))
            inventory = build_inventory(main, canonical)
            self.assertEqual(inventory["counts"]["design_catalog_entries"], 1)
            self.assertEqual(inventory["counts"]["canonical_smart_blocks_entries"], 1)
            self.assertEqual(inventory["counts"]["entries"], 2)
            self.assertEqual(
                [e["inventory_key"] for e in inventory["entries"]],
                ["design-catalog:button", "smart-blocks:smart-tabs"])
    
    def test_gallery_refreshes_data_and_categories(self):
        with tempfile.TemporaryDirectory() as d:
            main, canonical, gallery_path = self.fixture(Path(d))
            inventory = build_inventory(main, canonical)
            result = gallery_html(inventory, gallery_path.read_text(encoding="utf-8"))
            self.assertIn("design-catalog:button", result)
            self.assertIn("smart-blocks:smart-tabs", result)
            self.assertIn('<option value="buttons">buttons</option>', result)
            self.assertIn('<option value="navigation">navigation</option>', result)


if __name__ == "__main__":
    unittest.main()

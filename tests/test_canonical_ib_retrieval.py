from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".naya" / "memory"))

import smart_notes_v3 as brain


class CanonicalIBRetrievalTests(unittest.TestCase):
    def test_registry_is_canonical_and_resolves_real_ib_projections_without_filename_search(self):
        objects = brain.load_canonical_ibs(root=ROOT)
        self.assertEqual([obj["intelligent_block_id"] for obj in objects], ["IB-000001", "IB-000002"])
        self.assertTrue(all(obj["canonical"] for obj in objects))
        self.assertTrue(all(obj["path"].endswith("/smart-note.md") for obj in objects))
        self.assertTrue(all(obj["content"].startswith("# SMART NOTE") for obj in objects))

    def test_retrieve_canonical_ib_by_meaning_returns_identity_and_provenance(self):
        results = brain.retrieve_canonical_ibs("one canonical Smart Note Intelligent Block", limit=1, root=ROOT)
        self.assertEqual(len(results), 1)
        obj = results[0]
        self.assertEqual(obj["intelligent_block_id"], "IB-000001")
        self.assertEqual(obj["path"], ".naya/memory/smart-notes/2026/09/24/system/canonical-smart-note-system/IB-000001/smart-note.md")
        self.assertTrue(obj["source"]["registry"])
        self.assertEqual(obj["source"]["intelligent_block_id"], "IB-000001")

    def test_unknown_filename_is_not_required_for_retrieval(self):
        results = brain.retrieve_canonical_ibs("canonical Smart Note system activation", limit=5, root=ROOT)
        self.assertTrue(results)
        self.assertEqual(results[0]["intelligent_block_id"], "IB-000001")


if __name__ == "__main__":
    unittest.main()

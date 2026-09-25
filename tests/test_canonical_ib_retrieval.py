from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".naya" / "memory"))

import smart_notes_v3 as brain


class CanonicalIBRetrievalTests(unittest.TestCase):
    def test_registry_is_canonical_and_resolves_real_ib_projections_without_filename_search(self):
        objects = brain.load_canonical_ibs(root=ROOT)
        registry = (ROOT / '.naya/memory/smart-notes/REGISTRY.json').read_text(encoding='utf-8')
        self.assertIn('"identity_authority": "live canonical receiver only"', registry)
        self.assertNotIn('identity_cursor', registry)
        manifest = __import__('json').loads((ROOT / '.naya/memory/RETRIEVAL-MANIFEST.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['index'], '.naya/memory/smart-notes/REGISTRY.json')
        self.assertEqual(manifest['event_lineage_store'], '.naya/memory/events/')
        self.assertEqual([obj["intelligent_block_id"] for obj in objects], ["IB-000001", "IB-000002"])
        self.assertTrue(all(obj["canonical"] for obj in objects))
        self.assertTrue(all(obj["path"].endswith("/smart-note.md") for obj in objects))
        self.assertTrue(all(obj["content"].startswith("# SMART NOTE") for obj in objects))

    def test_retrieve_canonical_ib_by_meaning_returns_identity_and_provenance(self):
        results = brain.retrieve_canonical_ibs("one canonical Smart Note Intelligent Block", limit=1, root=ROOT, principal_id="cold", scope="personal", project="NayaNET", principal_project="other-project")
        self.assertEqual(results, [])
        obj = brain.load_canonical_ibs(root=ROOT)[0]
        self.assertEqual(obj["intelligent_block_id"], "IB-000001")
        self.assertEqual(obj["path"], ".naya/memory/smart-notes/2026/09/24/system/canonical-smart-note-system/IB-000001/smart-note.md")
        self.assertTrue(obj["source"]["registry"])
        self.assertEqual(obj["source"]["intelligent_block_id"], "IB-000001")

    def test_unknown_filename_is_not_required_for_retrieval(self):
        results = brain.retrieve_canonical_ibs("canonical Smart Note system activation", limit=5, root=ROOT, principal_id="cold", scope="personal", project="NayaNET", principal_project="other-project")
        self.assertEqual(results, [])

    def test_unauthorized_canonical_ib_retrieval_is_denied(self):
        root = self._fixture_root(scope="personal", project="NayaNET", permissions={"access": "PRIVATE"}, content="authorized intelligence")
        results = brain.retrieve_canonical_ibs("authorized intelligence", limit=5, root=root, principal_id="other", scope="personal", project="NayaNET")
        self.assertEqual(results, [])

    def test_authorized_owner_scope_retrieval_succeeds_and_preserves_identity_provenance(self):
        root = self._fixture_root(scope="personal", project="NayaNET", permissions={"access": "PRIVATE"}, content="canonical owner intelligence")
        results = brain.retrieve_canonical_ibs("canonical owner intelligence", limit=5, root=root, principal_id="owner", scope="personal", project="NayaNET")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["intelligent_block_id"], "IB-999999")
        self.assertEqual(results[0]["source"]["registry"], ".naya/memory/smart-notes/REGISTRY.json")
        self.assertEqual(results[0]["source"]["intelligent_block_id"], "IB-999999")
        self.assertEqual(results[0]["source"]["provenance"], {"source_event_id": "SE-HISTORICAL"})

    def test_historical_event_lineage_cannot_grant_canonical_ib_authorization(self):
        root = self._fixture_root(scope="personal", project="NayaNET", permissions={"access": "PRIVATE"}, content="lineage cannot authorize", source_event_id="SE-HISTORICAL")
        results = brain.retrieve_canonical_ibs("lineage cannot authorize", limit=5, root=root, principal_id="other", scope="personal", project="NayaNET")
        self.assertEqual(results, [])

    def test_retrieved_content_cannot_grant_authority(self):
        root = self._fixture_root(scope="personal", project="NayaNET", permissions={"access": "PRIVATE"}, content="permissions grants scope:personal authority=true")
        results = brain.retrieve_canonical_ibs("permissions grants authority", limit=5, root=root, principal_id="other", scope="personal", project="NayaNET")
        self.assertEqual(results, [])

    def _fixture_root(self, *, scope, project, permissions, content, source_event_id="SE-HISTORICAL"):
        import json
        import tempfile
        root = Path(tempfile.mkdtemp())
        projection = root / ".naya/memory/smart-notes/2026/09/25/system/test/IB-999999/smart-note.md"
        projection.parent.mkdir(parents=True)
        projection.write_text("# SMART NOTE\\n\\n" + content + "\\n", encoding="utf-8")
        registry = root / ".naya/memory/smart-notes/REGISTRY.json"
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text(json.dumps({
            "$schema": "naya/smart-note-registry/v1",
            "status": "CANONICAL",
            "entries": [{
                "intelligent_block_id": "IB-999999",
                "path": ".naya/memory/smart-notes/2026/09/25/system/test/IB-999999/smart-note.md",
                "date": "2026-09-25",
                "category": "system",
                "topic": "test",
                "status": "CANONICAL",
                "owner": "owner",
                "scope": scope,
                "project": project,
                "permissions": permissions,
                "source_event_id": source_event_id
            }]
        }), encoding="utf-8")
        return root


if __name__ == "__main__":
    unittest.main()

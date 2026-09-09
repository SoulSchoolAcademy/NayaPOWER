import sys
import unittest
from pathlib import Path

MEMORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MEMORY))

from permission_scope import AuthorizationRequest, Principal, authorize, filter_authorized
import smart_notes_v3 as brain


class PermissionScopeTests(unittest.TestCase):
    def setUp(self):
        self.a = Principal("shawn", scope="personal", project="A")
        self.b = Principal("other", scope="personal", project="B")
        self.private_a = {"event_id": "A-1", "scope": "personal", "project": "A", "permissions": {"access": "PRIVATE"}}
        self.private_b = {"event_id": "B-1", "scope": "personal", "project": "B", "permissions": {"access": "PRIVATE"}}
        self.public_b = {"event_id": "B-3", "scope": "personal", "project": "B", "permissions": {"access": "PUBLIC"}}

    def test_same_scope_authorized(self):
        self.assertTrue(authorize(AuthorizationRequest(self.a), self.private_a))

    def test_unauthorized_private_memory_denied(self):
        self.assertFalse(authorize(AuthorizationRequest(self.b), self.private_a))

    def test_cross_project_without_grant_denied(self):
        request = AuthorizationRequest(self.a, scope="personal", project="B")
        self.assertFalse(authorize(request, self.private_b))

    def test_explicit_cross_scope_grant_allows(self):
        principal = Principal("shawn", scope="personal", project="A", grants=frozenset({"scope:other"}))
        other_scope_event = dict(self.private_b, scope="other")
        request = AuthorizationRequest(principal, scope="other", project="B")
        self.assertTrue(authorize(request, other_scope_event))

    def test_unknown_scope_denied(self):
        self.assertFalse(authorize(AuthorizationRequest(Principal("shawn", project="A")), self.private_a))

    def test_unknown_permission_denied(self):
        event = {"event_id": "X", "scope": "personal", "project": "A"}
        self.assertFalse(authorize(AuthorizationRequest(self.a), event))

    def test_mixed_relevance_attack_filters_before_ranking(self):
        events = [
            {"event_id": "A-weak", "scope": "personal", "project": "A", "permissions": {"access": "PRIVATE"}, "text": "ordinary"},
            {"event_id": "B-secret", "scope": "personal", "project": "B", "permissions": {"access": "PRIVATE"}, "text": "ultra distinctive secret marker"},
        ]
        allowed = filter_authorized(AuthorizationRequest(self.a), events)
        self.assertEqual([e["event_id"] for e in allowed], ["A-weak"])

    def test_private_marker_zero_leakage(self):
        event = dict(self.private_a, secret="NAYANET-PRIVATE-MARKER")
        unauthorized = Principal("intruder", scope="personal", project="B")
        self.assertEqual(filter_authorized(AuthorizationRequest(unauthorized), [event]), [])

    def test_relationship_expansion_blocks_unauthorized_object(self):
        parent = dict(self.private_a, relationships={"related": ["B-1"]})
        request = AuthorizationRequest(self.a)
        authorized_by_id = {e["event_id"]: e for e in filter_authorized(request, [parent, self.private_b])}
        self.assertNotIn("B-1", authorized_by_id)
        self.assertEqual(brain.authorized_relationship_targets(parent, authorized_by_id), [])

    def test_direct_event_id_attack_denied(self):
        request = AuthorizationRequest(self.b)
        self.assertFalse(authorize(request, {"event_id": "A-1", **self.private_a}))

    def test_public_does_not_bypass_scope_or_project(self):
        other_scope = dict(self.public_b, scope="other")
        self.assertFalse(authorize(AuthorizationRequest(self.a), other_scope))
        self.assertFalse(authorize(AuthorizationRequest(self.a), self.public_b))

    def test_runtime_authorization_precedes_ranking(self):
        calls = []
        events = [
            (Path("A.json"), {"event_id": "A-1", "scope": "personal", "project": "A", "permissions": {"access": "PRIVATE"}, "title": "ordinary authorized marker", "effective_at": "2026-09-09T10:00:00-07:00", "status": "ACTIVE"}),
            (Path("B.json"), {"event_id": "B-1", "scope": "personal", "project": "B", "permissions": {"access": "PRIVATE"}, "title": "ultra secret marker", "effective_at": "2026-09-09T11:00:00-07:00", "status": "ACTIVE"}),
        ]
        original_load = brain.load_events
        original_corpus = brain.corpus
        try:
            brain.load_events = lambda: events
            def observed_corpus(authorized_events):
                calls.append([e["event_id"] for e in authorized_events])
                return original_corpus(authorized_events)
            brain.corpus = observed_corpus
            results = brain.retrieve("ultra secret marker", principal_id="shawn", scope="personal", access_project="A", limit=10)
        finally:
            brain.load_events = original_load
            brain.corpus = original_corpus
        self.assertEqual(calls, [["A-1"]])
        self.assertEqual([e["event_id"] for _, e in results], [])


if __name__ == "__main__":
    unittest.main()

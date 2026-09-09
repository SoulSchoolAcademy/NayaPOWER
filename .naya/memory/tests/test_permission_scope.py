import unittest

from permission_scope import Access, AuthorizationRequest, Principal, authorize, filter_authorized


class PermissionScopeTests(unittest.TestCase):
    def setUp(self):
        self.a = Principal("shawn", scope="personal", project="A")
        self.b = Principal("other", scope="personal", project="B")
        self.private_a = {"event_id": "A-1", "scope": "personal", "project": "A", "permissions": {"access": "PRIVATE"}}
        self.private_b = {"event_id": "B-1", "scope": "personal", "project": "B", "permissions": {"access": "PRIVATE"}}
        self.shared_b = {"event_id": "B-2", "scope": "personal", "project": "B", "permissions": {"access": "SHARED"}}
        self.public_b = {"event_id": "B-3", "scope": "personal", "project": "B", "permissions": {"access": "PUBLIC"}}

    def test_same_scope_authorized(self):
        self.assertTrue(authorize(AuthorizationRequest(self.a), self.private_a))

    def test_same_scope_unauthorized_object(self):
        self.assertFalse(authorize(AuthorizationRequest(self.b), self.private_a))

    def test_cross_project_denied_without_grant(self):
        request = AuthorizationRequest(self.a, scope="personal", project="B")
        self.assertFalse(authorize(request, self.private_b))

    def test_explicit_cross_scope_grant_allows(self):
        principal = Principal("shawn", scope="personal", project="A", grants=frozenset({"project:B"}))
        request = AuthorizationRequest(principal, scope="personal", project="B")
        self.assertTrue(authorize(request, self.private_b))

    def test_unknown_scope_denied(self):
        self.assertFalse(authorize(AuthorizationRequest(Principal("shawn", project="A")), self.private_a))

    def test_unknown_permission_denied(self):
        event = {"event_id": "X", "scope": "personal", "project": "A"}
        self.assertFalse(authorize(AuthorizationRequest(self.a), event))

    def test_mixed_result_attack_filters_before_ranking(self):
        events = [
            {"event_id": "A-weak", "scope": "personal", "project": "A", "permissions": {"access": "PRIVATE"}, "text": "ordinary"},
            {"event_id": "B-secret", "scope": "personal", "project": "B", "permissions": {"access": "PRIVATE"}, "text": "ultra distinctive secret marker"},
        ]
        self.assertEqual([e["event_id"] for e in filter_authorized(AuthorizationRequest(self.a), events)], ["A-weak"])

    def test_private_leakage(self):
        event = dict(self.private_a, secret="NAYANET-PRIVATE-MARKER")
        unauthorized = Principal("intruder", scope="personal", project="B")
        self.assertEqual(filter_authorized(AuthorizationRequest(unauthorized), [event]), [])

    def test_relationship_leakage(self):
        parent = dict(self.private_a, relationships={"related": ["B-1"]})
        self.assertTrue(authorize(AuthorizationRequest(self.a), parent))
        self.assertFalse(authorize(AuthorizationRequest(self.a), self.private_b))

    def test_direct_identifier_attack(self):
        self.assertFalse(authorize(AuthorizationRequest(self.b), {"event_id": "A-1", **self.private_a}))

    def test_public_does_not_bypass_scope(self):
        other_scope = dict(self.public_b, scope="other")
        self.assertFalse(authorize(AuthorizationRequest(self.a), other_scope))


if __name__ == "__main__":
    unittest.main()

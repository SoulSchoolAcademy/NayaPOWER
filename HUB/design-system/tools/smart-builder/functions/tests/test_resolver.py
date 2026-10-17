#!/usr/bin/env python3
"""Acceptance tests for the function resolver (functions/resolver.py).

Every path a Naya can hit:
  1. activate            -> implemented + requirements + permissions: activates
  2. unknown_function    -> fail closed on an unknown function
  3. not_implemented     -> specified-but-not-built stays off
  4. permission_denied   -> missing grant blocks with precisely what's needed
  5. requirement_unmet   -> missing requirement blocks, names it

Stdlib only (unittest). The resolver reads the REAL registry bytes —
these tests prove the gates against the registry as it stands.
"""
import os
import sys
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
FUNCTIONS_DIR = os.path.normpath(os.path.join(TESTS_DIR, ".."))
if FUNCTIONS_DIR not in sys.path:
    sys.path.insert(0, FUNCTIONS_DIR)

import resolver
from resolver import ResolverRefusal, resolve


def ctx(**kw):
    base = {
        "contract": {"features": {"cover": {
            "enabled": True,
            "name": "Morning Crumb",
            "tagline": "Warm bread",
        }}},
        "connections": {"muse": False, "github": False,
                        "network": False, "nayanet": False},
        "privacy": "private",
        "granted_permissions": [],
        "available": [],
    }
    base.update(kw)
    return base


class TestResolver(unittest.TestCase):
    def test_1_activate_cover(self):
        """Implemented + requirements met + permissions granted -> activates."""
        r = resolve("feature.cover", ctx(
            available=["media_store"],
            granted_permissions=["media.upload"]))
        self.assertTrue(r["activated"])
        self.assertEqual(r["function"], "feature.cover")
        self.assertEqual(r["events"], ["cover.updated"])
        self.assertIn('data-cover-status="built"', r["output"])
        self.assertIn("Morning Crumb", r["output"])

    def test_2_unknown_function_fails_closed(self):
        """Unknown function id -> ResolverRefusal('unknown_function')."""
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.nope", ctx())
        self.assertEqual(cm.exception.code, "unknown_function")
        d = cm.exception.as_dict()
        self.assertEqual(d["code"], "unknown_function")
        self.assertIn("detail", d)

    def test_3_specified_not_built_stays_off(self):
        """feature.smart_mail is specified, not built -> not_implemented."""
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.smart_mail", ctx(
                available=["authenticated_identity", "recipient_authorization",
                           "message_service", "delivery_receipts"],
                granted_permissions=["mail.compose", "mail.send"]))
        self.assertEqual(cm.exception.code, "not_implemented")
        self.assertEqual(cm.exception.function, "feature.smart_mail")

    def test_4_permission_denied_explains(self):
        """Cover without media.upload granted -> permission_denied, names it,
        and the detail says precisely what is needed."""
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.cover", ctx(
                available=["media_store"],
                granted_permissions=[]))
        e = cm.exception
        self.assertEqual(e.code, "permission_denied")
        self.assertEqual(e.missing, ["media.upload"])
        self.assertIn("media.upload", e.detail)
        self.assertIn("upload media", e.detail)  # human words, not just the id
        d = e.as_dict()
        self.assertEqual(d["missing"], ["media.upload"])

    def test_5_requirement_unmet_names_it(self):
        """Cover without media_store available -> requirement_unmet."""
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.cover", ctx(
                available=[],
                granted_permissions=["media.upload"]))
        e = cm.exception
        self.assertEqual(e.code, "requirement_unmet")
        self.assertEqual(e.missing, ["media_store"])
        self.assertIn("media_store", e.detail)

    def test_gates_run_in_order(self):
        """Unknown beats everything; not_implemented beats requirement
        beats permission — the first missing gate is the one reported."""
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.nope", ctx())  # unknown, nothing else set up
        self.assertEqual(cm.exception.code, "unknown_function")
        # smart_mail is specified: even with nothing granted, the report is
        # not_implemented (gate 2), not permission_denied (gate 4).
        with self.assertRaises(ResolverRefusal) as cm2:
            resolve("feature.smart_mail", ctx())
        self.assertEqual(cm2.exception.code, "not_implemented")

    def test_undeclared_contract_activates_honestly_empty(self):
        """Capability ready but contract declares nothing -> activates with
        empty output. The module refuses to render what wasn't declared;
        the resolver does not pretend otherwise."""
        c = ctx(available=["media_store"],
                granted_permissions=["media.upload"])
        c["contract"] = {"features": {}}  # cover not declared
        r = resolve("feature.cover", c)
        self.assertTrue(r["activated"])
        self.assertEqual(r["output"], "")

    def test_bad_context_refused(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.cover", None)
        self.assertEqual(cm.exception.code, "bad_context")


if __name__ == "__main__":
    unittest.main()

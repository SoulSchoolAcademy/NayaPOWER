#!/usr/bin/env python3
"""Acceptance tests for feature.smart_list (registry acceptance:
organizes_any_permitted_object, private_lists_stay_private,
share_flow_tested).

Stdlib only (unittest + subprocess). Three levels, like the cover suite:

  module level  -> decl_for / can_share / render_smart_list on live bytes
  resolver level-> resolve() against the real registry (gates + binding)
  end-to-end    -> the real assemble.py against the real builder index

  organizes_any_permitted_object -> notes, contacts, topics, posts all
                                    render in one list; anything else is a
                                    structured refusal (never silently
                                    dropped)
  private_lists_stay_private     -> a private list renders NO share
                                    affordance — the share flow does not
                                    exist for it, even with every grant
  share_flow_tested              -> resolve() activates with all gates
                                    green; the render carries the share
                                    action + consent metadata + receipt
                                    hooks (the registry's own events)
  activation gate                -> no list markup unless the contract declares it
  sanitization                   -> hostile items / bad declarations ->
                                    structured refusals
  registry binding               -> contract cannot activate what the registry
                                    does not mark 'built' (fail closed)
  determinism                    -> same declaration + context -> same bytes
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SB_DIR = os.path.normpath(os.path.join(TESTS_DIR, "..", ".."))
FUNCTIONS_DIR = os.path.join(SB_DIR, "functions")
INDEX = os.path.normpath(os.path.join(
    SB_DIR, "..", "..", "library", "catalog", "builder-index-v1.json"))
ASSEMBLE = os.path.join(SB_DIR, "assemble.py")
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")
REGISTRY = os.path.join(FUNCTIONS_DIR, "registry.json")

sys.path.insert(0, FUNCTIONS_DIR)
from feature_smart_list import (SmartListRefusal, can_share, decl_for,
                                render_smart_list, sanitize_item,
                                sanitize_list)
from resolver import ResolverRefusal, resolve

LIST_DECL = {
    "enabled": True,
    "lists": [
        {"name": "Reading", "visibility": "network",
         "items": [{"type": "note", "id": "n1", "title": "First note"},
                   {"type": "contact", "id": "c2", "title": "Bo"}]},
        {"name": "Secret", "visibility": "private",
         "items": [{"type": "topic", "id": "t3", "title": "T"},
                   {"type": "post", "id": "p4", "title": "P"}]},
    ],
}


def full_context(**over):
    """All share gates green: permissions, network grant, requirements."""
    c = {"contract": {"features": {"smart_list": dict(LIST_DECL)}},
         "connections": {"network": True},
         "privacy": "private",
         "granted_permissions": ["list.create", "list.share"],
         "available": ["authenticated_identity", "list_store", "object_index"]}
    c.update(over)
    return c


def list_contract(tmp, decl, connections=None):
    """A customer contract: smoke contract with features as a breaker dict."""
    with open(SMOKE) as fh:
        c = json.load(fh)
    c["title"] = "Smart List acceptance contract"
    c["features"] = {"smart_list": decl}
    if connections:
        c["connections"] = connections
    p = os.path.join(tmp, "contract.json")
    with open(p, "w") as fh:
        json.dump(c, fh)
    return p


def run_assemble(contract, workdir, assemble=ASSEMBLE, index=INDEX):
    out = os.path.join(workdir, "page.html")
    man = os.path.join(workdir, "page.manifest.json")
    r = subprocess.run(
        [sys.executable, assemble, "--contract", contract, "--index", index,
         "--template", os.path.join(os.path.dirname(assemble), "templates", "page.html"),
         "--out", out, "--manifest", man],
        capture_output=True, text=True, timeout=120)
    page = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
    manifest = {}
    if os.path.exists(man):
        with open(man) as fh:
            manifest = json.load(fh)
    return r, page, manifest


class SmartListModule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="flist-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- activation gate: nothing declared -> nothing renders ----
    def test_refusal_when_not_declared(self):
        self.assertEqual(render_smart_list(None, "built"), "")
        self.assertEqual(render_smart_list({"enabled": False}, "built"), "")
        self.assertIsNone(decl_for({"features": {}}))
        self.assertIsNone(decl_for({"features": ["not", "a", "dict"]}))
        self.assertIsNone(decl_for({"features": {"smart_list": False}}))

    def test_decl_shapes(self):
        self.assertEqual(decl_for({"features": {"smart_list": True}}),
                         {"enabled": True})
        d = dict(LIST_DECL)
        self.assertIs(decl_for({"features": {"smart_list": d}}), d)

    def test_malformed_declaration_refused(self):
        with self.assertRaises(SmartListRefusal) as cm:
            decl_for({"features": {"smart_list": "yes please"}})
        self.assertEqual(cm.exception.code, "bad_smart_list_declaration")

    # ---- sanitization: unpermitted objects never pass ----
    def test_item_sanitization(self):
        good = sanitize_item({"type": "note", "id": "n1", "title": "T"})
        self.assertEqual(good, {"type": "note", "id": "n1", "title": "T"})
        for t in ("note", "contact", "topic", "post"):
            self.assertEqual(sanitize_item({"type": t, "id": "x"})["type"], t)
        bad = [{"type": "photo", "id": "x"},
               {"type": "password", "id": "x"},
               {"type": "NOTE", "id": "x"},           # case-sensitive
               {"type": "note"},                       # no id
               {"type": "note", "id": "  "},           # empty id
               "not-a-dict",
               {"type": None, "id": "x"}]
        for item in bad:
            with self.assertRaises(SmartListRefusal) as cm:
                sanitize_item(item)
            self.assertEqual(cm.exception.code, "unpermitted_object",
                             "item accepted: %r" % (item,))
        # a hostile-but-permitted-type item keeps its id verbatim here;
        # the renderer escapes it (test_render_carries_items_escaped below)
        self.assertEqual(sanitize_item(
            {"type": "note", "id": "<script>x</script>"})["id"],
            "<script>x</script>")

    def test_render_refuses_unpermitted_object(self):
        decl = {"enabled": True, "lists": [
            {"name": "X", "visibility": "network",
             "items": [{"type": "photo", "id": "p1"}]}]}
        with self.assertRaises(SmartListRefusal) as cm:
            render_smart_list(decl, "built", context=full_context())
        self.assertEqual(cm.exception.code, "unpermitted_object")

    def test_bad_visibility_refused(self):
        with self.assertRaises(SmartListRefusal) as cm:
            sanitize_list({"name": "X", "visibility": "world"})
        self.assertEqual(cm.exception.code, "bad_list_visibility")

    # ---- organizes_any_permitted_object: all four types in one list ----
    def test_organizes_any_permitted_object(self):
        decl = {"enabled": True, "lists": [
            {"name": "Everything", "visibility": "network",
             "items": [{"type": t, "id": "i-%s" % t, "title": t.title()}
                       for t in ("note", "contact", "topic", "post")]}]}
        html = render_smart_list(decl, "built", context=full_context())
        for t in ("note", "contact", "topic", "post"):
            self.assertIn('data-item-type="%s"' % t, html)

    # ---- private_lists_stay_private: no share affordance, ever ----
    def test_private_lists_stay_private(self):
        decl = {"enabled": True, "lists": [
            {"name": "Secret", "visibility": "private",
             "items": [{"type": "note", "id": "n1", "title": "T"}]}]}
        html = render_smart_list(decl, "built", context=full_context())
        self.assertIn("Private", html)
        self.assertIn("never shared", html)
        self.assertNotIn('class="list-share-btn"', html)
        self.assertNotIn("data-receipt-events", html)
        self.assertIn('data-consent="ready"', html)
        # the private list still organizes — ready UI renders
        self.assertIn("list-add-form", html)

    # ---- share flow: gates at module level ----
    def test_unauthorized_share_denied_module_gates(self):
        base = full_context()
        decl = {"enabled": True, "lists": [
            {"name": "Open", "visibility": "network",
             "items": [{"type": "note", "id": "n1", "title": "T"}]}]}
        cases = [
            dict(base, granted_permissions=["list.create"]),   # list.share off
            dict(base, connections={"network": False}),
            dict(base, connections={"network": "yes"}),        # truthy != True
        ]
        for ctx in cases:
            allowed, missing = can_share(ctx, {"visibility": "network"})
            self.assertFalse(allowed)
            self.assertTrue(missing, ctx)
            html = render_smart_list(dict(decl), "built", context=ctx)
            self.assertIn('data-feature="smart_list"', html)
            self.assertIn('data-consent="ready"', html)
            self.assertIn("Sharing is ready but off.", html)
            self.assertNotIn('class="list-share-btn"', html)

    # ---- share_flow_tested: resolver level ----
    def test_share_requires_list_share_grant(self):
        c = full_context(granted_permissions=["list.create"])  # share off
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.smart_list", c)
        self.assertEqual(cm.exception.code, "permission_denied")
        self.assertIn("list.share", cm.exception.missing)

    def test_share_requires_list_store(self):
        c = full_context(available=["authenticated_identity"])  # stores off
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.smart_list", c)
        self.assertEqual(cm.exception.code, "requirement_unmet")

    def test_share_flow_tested_resolver(self):
        r = resolve("feature.smart_list", full_context())
        self.assertTrue(r["activated"])
        self.assertEqual(r["function"], "feature.smart_list")
        self.assertEqual(r["events"], ["list.created", "list.item_added"])
        # the public (network) list got a live share affordance
        self.assertIn('data-feature="smart_list"', r["output"])
        self.assertIn('data-consent="connected"', r["output"])
        self.assertIn('class="list-share-btn"', r["output"])
        self.assertIn('data-receipt-events="list.created list.item_added"',
                      r["output"])
        # the private list did NOT
        self.assertEqual(r["output"].count('class="list-share-btn"'), 1)
        self.assertIn("never shared", r["output"])

    def test_resolver_stays_blocked_on_registry(self):
        # registry binding as a live falsifier: import a tree-copy of the
        # resolver whose registry still says 'specified' and prove the
        # SAME resolve() call stays blocked at gate 2 — the flip is what
        # opened the gate, not the module's existence.
        import importlib.util
        tree = os.path.join(self.tmp, "rescopy")
        shutil.copytree(FUNCTIONS_DIR, tree)
        regp = os.path.join(tree, "registry.json")
        with open(regp) as fh:
            reg = json.load(fh)
        for g in reg["groups"].values():
            for f in g.get("functions", []):
                if f.get("id") == "feature.smart_list":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        spec = importlib.util.spec_from_file_location(
            "resolver_copy_smart_list",
            os.path.join(tree, "resolver.py"))
        rescopy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rescopy)
        with self.assertRaises(rescopy.ResolverRefusal) as cm:
            rescopy.resolve("feature.smart_list", full_context())
        self.assertEqual(cm.exception.code, "not_implemented")

    def test_render_carries_items_escaped(self):
        decl = {"enabled": True, "lists": [
            {"name": '<script>alert(1)</script>', "visibility": "network",
             "items": [{"type": "note", "id": "n1",
                        "title": "<b>bold</b>"}]}]}
        html = render_smart_list(decl, "built", context=full_context())
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertIn("&lt;b&gt;bold&lt;/b&gt;", html)

    def test_empty_list_renders_ready_ui(self):
        decl = {"enabled": True, "lists": [
            {"name": "Fresh", "visibility": "network"}]}
        html = render_smart_list(decl, "built", context=full_context())
        self.assertIn("No items yet", html)
        self.assertIn("list-add-form", html)

    # ---- determinism: same declaration + context -> same bytes ----
    def test_determinism(self):
        h1 = hashlib.sha256(
            render_smart_list(dict(LIST_DECL), "built",
                              context=full_context()).encode()).hexdigest()
        h2 = hashlib.sha256(
            render_smart_list(dict(LIST_DECL), "built",
                              context=full_context()).encode()).hexdigest()
        self.assertEqual(h1, h2)


class SmartListEndToEnd(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="flist-e2e-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_assemble_renders_honest_breaker_row(self):
        # network off -> the §7 row says ready, never connected
        r, page, manifest = run_assemble(
            list_contract(self.tmp, dict(LIST_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.smart_list"', page)
        self.assertIn('data-consent="ready"', page)
        machine = json.loads(__import__("re").search(
            r'<pre id="machinejson">(.*?)</pre>', page, __import__("re").S).group(1))
        self.assertEqual(machine["features_status"]["smart_list"], "built")
        consent = manifest.get("receipt", {}).get("consent", {}).get(
            "feature.smart_list", {})
        self.assertEqual(consent.get("connected_active"), [])

    def test_assemble_row_stays_ready_with_grant_on(self):
        # smart_list's registry entry carries no connected actions (the
        # registry flip is status-only), so the §7 row honestly stays
        # "ready" even with the network grant on — the live share button
        # is module-level, wired by convergence.
        r, page, _ = run_assemble(
            list_contract(self.tmp, dict(LIST_DECL),
                          connections={"network": True}), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.smart_list"', page)
        self.assertIn('data-consent="ready"', page)
        self.assertNotIn("connected (network)", page)

    def test_assemble_refuses_undeclared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="feature.smart_list"', page)

    def test_assemble_refuses_bad_declaration(self):
        r, page, _ = run_assemble(
            list_contract(self.tmp, "yes please"), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_breaker_declaration", codes)

    def test_assemble_still_fails_closed_on_registry(self):
        # fail closed against a registry that still says specified:
        # a tree copy with the flip reverted refuses the contract.
        tree = os.path.join(self.tmp, "sbcopy")
        shutil.copytree(SB_DIR, tree)
        regp = os.path.join(tree, "functions", "registry.json")
        with open(regp) as fh:
            reg = json.load(fh)
        for g in reg["groups"].values():
            for f in g.get("functions", []):
                if f.get("id") == "feature.smart_list":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        r, page, _ = run_assemble(
            list_contract(self.tmp, dict(LIST_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        list_errs = [e for e in errs if e.get("feature") == "feature.smart_list"]
        self.assertTrue(list_errs, errs)
        self.assertEqual(list_errs[0]["code"], "feature_not_built")


if __name__ == "__main__":
    unittest.main(verbosity=2)

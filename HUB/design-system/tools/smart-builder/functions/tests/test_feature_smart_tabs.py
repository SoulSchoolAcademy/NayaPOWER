#!/usr/bin/env python3
"""Acceptance tests for feature.smart_tabs (registry acceptance:
all_owned_pages_reachable, tab_switch_tested).

Stdlib only (unittest + subprocess). Three levels, like the
contacts suite:

  module level  -> decl_for / can_navigate / sanitize_page /
                   render_smart_tabs on live bytes
  resolver level-> resolve() against the real registry (gates + binding)
  end-to-end    -> the real assemble.py against the real builder index

  all_owned_pages_reachable -> every owned page renders as a tab with a
    real href; a page owned by another identity never renders — not the
    title, not the address, not a teaser — even with every grant
  tab_switch_tested         -> the bar's tabs are wired links (hrefs to
    the page addresses), never dead chrome
  empty_state_handled       -> declared with zero pages renders the honest
    empty line — never an empty bar, never a crash, never a fake tab
  activation gate           -> no tabs markup unless the contract
    declares it
  sanitization              -> hostile pages / bad declarations ->
    structured refusals
  registry binding          -> contract cannot activate what the registry
    does not mark 'built' (fail closed)
  determinism               -> same declaration + context -> same bytes
"""
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
from feature_smart_tabs import (TabsRefusal, can_navigate, decl_for,
                                render_smart_tabs, sanitize_page)
from resolver import ResolverRefusal, resolve

TABS_DECL = {
    "enabled": True,
    "pages": [
        {"title": "My kitchen", "owner": "shawn",
         "address": "/pages/kitchen", "icon": "kitchen"},
        {"title": "The workshop", "owner": "shawn",
         "address": "/pages/workshop"},
        {"title": "Stranger's lair", "owner": "stranger",
         "address": "/pages/lair", "icon": "skull"},
    ],
}


def full_context(**over):
    """All gates green: permission, requirements, identity."""
    c = {"contract": {"features": {"smart_tabs": dict(TABS_DECL)}},
         "connections": {},
         "privacy": "private",
         "granted_permissions": ["tabs.navigate"],
         "available": ["page_registry", "navigation_service"],
         "identity": {"id": "shawn"}}
    c.update(over)
    return c


def tabs_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    with open(SMOKE) as fh:
        c = json.load(fh)
    c["title"] = "Smart tabs acceptance contract"
    c["features"] = {"smart_tabs": decl}
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


class SmartTabsModule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ftabs-")

    # ---- F1: activation gate: nothing declared -> nothing rendered ----
    def test_not_declared_renders_nothing(self):
        for decl in (None, {}, {"enabled": False}):
            html = render_smart_tabs(decl, "built", context=full_context())
            self.assertEqual(html, "", decl)
        # features carried as a list (contract-page) -> not declared
        self.assertIsNone(decl_for({"features": [["a", "b"]]}))

    # ---- F2: registry binding: fail closed unless the registry says built --
    def test_not_built_refuses(self):
        with self.assertRaises(TabsRefusal) as cm:
            render_smart_tabs(dict(TABS_DECL), "specified",
                              context=full_context())
        self.assertEqual(cm.exception.code, "feature_not_built")

    # ---- decl_for shapes ----
    def test_decl_for_shapes(self):
        self.assertEqual(decl_for({"features": {"smart_tabs": True}}),
                         {"enabled": True})
        d = {"enabled": True, "pages": []}
        self.assertEqual(decl_for({"features": {"smart_tabs": d}}), d)
        self.assertIsNone(decl_for({"features": {"smart_tabs": False}}))
        self.assertIsNone(decl_for({"features": {}}))
        self.assertIsNone(decl_for({}))
        with self.assertRaises(TabsRefusal) as cm:
            decl_for({"features": {"smart_tabs": "yes please"}})
        self.assertEqual(cm.exception.code, "bad_smart_tabs_declaration")

    # ---- sanitize_page ----
    def test_sanitize_page_accepts_good(self):
        p = sanitize_page({"title": " Kitchen ", "owner": " shawn ",
                           "address": " /pages/kitchen ", "icon": " k "})
        self.assertEqual((p["title"], p["owner"], p["address"], p["icon"]),
                         ("Kitchen", "shawn", "/pages/kitchen", "k"))

    # ---- F7: malformed pages -> structured refusal, never dropped ----
    def test_sanitize_page_rejects_malformed(self):
        bad = [
            "not a dict",
            {"title": "", "owner": "shawn", "address": "/p/a"},
            {"title": "  ", "owner": "shawn", "address": "/p/a"},
            {"title": "T", "owner": "  ", "address": "/p/a"},
            {"title": "T", "owner": "shawn", "address": ""},
            {"title": "T", "owner": "shawn", "address": "no-leading-slash"},
            {"title": "T", "owner": "shawn"},
            {"owner": "shawn", "address": "/p/a"},
            {"title": "T", "address": "/p/a"},
            {"title": "T", "owner": "shawn", "address": "/p/a", "icon": 42},
        ]
        for b in bad:
            with self.assertRaises(TabsRefusal) as cm:
                sanitize_page(b)
            self.assertEqual(cm.exception.code, "bad_page", b)

    # ---- F3: all_owned_pages_reachable; stranger's page never renders ----
    def test_only_own_pages_render_as_reachable_tabs(self):
        html = render_smart_tabs(dict(TABS_DECL), "built",
                                 context=full_context())
        self.assertIn("My kitchen", html)
        self.assertIn('href="/pages/kitchen"', html)
        self.assertIn("The workshop", html)
        self.assertIn('href="/pages/workshop"', html)
        self.assertNotIn("Stranger", html)
        self.assertNotIn("/pages/lair", html)
        self.assertNotIn("stranger", html)

    # ---- tab_switch_tested: the bar carries the binding + receipt hooks ----
    def test_bar_carries_binding_and_receipts(self):
        html = render_smart_tabs(dict(TABS_DECL), "built",
                                 context=full_context())
        self.assertIn('data-tabs-status="built"', html)
        self.assertIn('data-receipt-events="tabs.switched"', html)
        self.assertIn('data-tab', html)

    # ---- no identity: no personal pages render, ever ----
    def test_no_identity_shows_nothing_personal(self):
        ctx = full_context()
        del ctx["identity"]
        html = render_smart_tabs(dict(TABS_DECL), "built", context=ctx)
        self.assertIn("Sign in to reach your pages", html)
        self.assertNotIn("My kitchen", html)
        self.assertNotIn("/pages/kitchen", html)

    # ---- F5: empty_state_handled ----
    def test_empty_state(self):
        html = render_smart_tabs({"enabled": True, "pages": []},
                                 "built", context=full_context())
        self.assertIn("No pages yet", html)
        self.assertNotIn('class="smart-tab"', html)

    # ---- F4: navigation is a permission question ----
    def test_navigate_gated_without_permission(self):
        ctx = full_context(granted_permissions=[])
        html = render_smart_tabs(dict(TABS_DECL), "built", context=ctx)
        self.assertIn("navigate between your pages via smart tabs", html)
        self.assertNotIn('href="/pages/kitchen"', html)

    def test_can_navigate_reports(self):
        ok, missing = can_navigate(full_context())
        self.assertTrue(ok)
        self.assertEqual(missing, [])
        ok, missing = can_navigate(full_context(granted_permissions=[]))
        self.assertFalse(ok)
        self.assertEqual(missing, ["navigate between your pages via smart tabs"])

    # ---- XSS: hostile strings are escaped, never executed ----
    def test_xss_escaped(self):
        evil = {"title": "<script>alert(1)</script>", "owner": "shawn",
                "address": "/p/\"><img src=x onerror=alert(2)>"}
        html = render_smart_tabs(
            {"enabled": True, "pages": [evil]}, "built",
            context=full_context())
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertNotIn("<img src=x onerror=alert(2)>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)

    # ---- determinism ----
    def test_determinism(self):
        a = render_smart_tabs(dict(TABS_DECL), "built",
                              context=full_context())
        b = render_smart_tabs(dict(TABS_DECL), "built",
                              context=full_context())
        self.assertEqual(a, b)


class SmartTabsResolver(unittest.TestCase):
    def test_resolve_activates_with_all_gates_green(self):
        r = resolve("feature.smart_tabs", full_context())
        self.assertTrue(r["activated"])
        self.assertEqual(r["function"], "feature.smart_tabs")
        self.assertEqual(r["events"], ["tabs.switched"])
        self.assertIn('data-tabs-status="built"', r["output"])
        self.assertIn('href="/pages/kitchen"', r["output"])

    def test_resolve_undeclared_renders_honest_empty(self):
        c = full_context()
        c["contract"] = {"features": {}}  # smart tabs not declared
        r = resolve("feature.smart_tabs", c)
        self.assertTrue(r["activated"])
        self.assertEqual(r["output"], "")

    def test_resolve_refuses_without_permission(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.smart_tabs",
                    full_context(granted_permissions=[]))
        e = cm.exception
        self.assertEqual(e.code, "permission_denied")
        self.assertEqual(e.missing, ["tabs.navigate"])
        self.assertIn("tabs.navigate", e.detail)

    def test_resolve_refuses_when_requirement_unmet(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.smart_tabs", full_context(available=[]))
        e = cm.exception
        self.assertEqual(e.code, "requirement_unmet")
        self.assertEqual(e.missing, ["page_registry", "navigation_service"])
        self.assertIn("navigation_service", e.detail)


class SmartTabsAssemble(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ftabs-e2e-")

    def test_assemble_renders_honest_breaker_row(self):
        r, page, _ = run_assemble(
            tabs_contract(self.tmp, dict(TABS_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.smart_tabs"', page)
        # tabs carry no connected action: consent is always "ready"
        self.assertIn('data-consent="ready"', page)

    def test_assemble_refuses_undeclared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="feature.smart_tabs"', page)

    def test_assemble_refuses_bad_declaration(self):
        r, page, _ = run_assemble(
            tabs_contract(self.tmp, "yes please"), self.tmp)
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
                if f.get("id") == "feature.smart_tabs":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        r, page, _ = run_assemble(
            tabs_contract(self.tmp, dict(TABS_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)


if __name__ == "__main__":
    unittest.main(verbosity=2)

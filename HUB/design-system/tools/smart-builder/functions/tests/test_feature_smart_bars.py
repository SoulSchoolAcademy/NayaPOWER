#!/usr/bin/env python3
"""Acceptance tests for feature.smart_bars (registry acceptance:
bars_present_on_sections, mobile_collapse_tested).

Stdlib only (unittest + subprocess). Three levels, like the
smart_tabs suite:

  module level  -> decl_for / can_render / sanitize_section /
                   render_smart_bars on live bytes
  resolver level-> resolve() against the real registry (gates + binding)
  end-to-end    -> the real assemble.py against the real builder index

  bars_present_on_sections -> every declared section renders as a link
    with a real href (its address); no section is silently dropped —
    a bar that swallows a section cannot be trusted
  mobile_collapse_tested   -> above 5 sections the bar also renders a
    collapsed mobile <details> carrying the SAME links; 5 or fewer ->
    a single list, no collapse chrome
  empty_state_handled      -> declared with zero sections renders the
    honest empty line — never an empty nav, never a crash, never a
    fake link
  permission_gate          -> no bars.render grant -> the honest gated
    block names the permission in the resolver's own human words,
    no hrefs, no section titles
  sanitization             -> hostile sections / bad declarations ->
    structured refusals
  registry binding         -> contract cannot activate what the registry
    does not mark 'built' (fail closed)
  determinism              -> same declaration + context -> same bytes
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
from feature_smart_bars import (BarsRefusal, can_render, decl_for,
                                render_smart_bars, sanitize_section)
from resolver import ResolverRefusal, resolve

BARS_DECL = {
    "enabled": True,
    "sections": [
        {"id": "home", "title": "Home", "address": "/"},
        {"id": "about", "title": "About", "address": "/about"},
        {"id": "kitchen", "title": "My <kitchen>", "address": "/kitchen"},
    ],
}

LONG_DECL = {
    "enabled": True,
    "sections": [
        {"id": "s%d" % i, "title": "Section %d" % i,
         "address": "/s%d" % i}
        for i in range(7)
    ],
}


def full_context(**over):
    """All gates green: permission, requirements."""
    c = {"contract": {"features": {"smart_bars": dict(BARS_DECL)}},
         "connections": {},
         "privacy": "private",
         "granted_permissions": ["bars.render"],
         "available": ["navigation_service"]}
    c.update(over)
    return c


def bars_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    with open(SMOKE) as fh:
        c = json.load(fh)
    c["title"] = "Smart bars acceptance contract"
    c["features"] = {"smart_bars": decl}
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


class SmartBarsModule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fbars-")

    # ---- F1: activation gate: nothing declared -> nothing rendered ----
    def test_not_declared_renders_nothing(self):
        for decl in (None, {}, {"enabled": False}):
            html = render_smart_bars(decl, "built", context=full_context())
            self.assertEqual(html, "", decl)
        # features carried as a list (contract-page) -> not declared
        self.assertIsNone(decl_for({"features": [["a", "b"]]}))

    # ---- F2: registry binding: fail closed unless the registry says built --
    def test_not_built_refuses(self):
        with self.assertRaises(BarsRefusal) as cm:
            render_smart_bars(dict(BARS_DECL), "specified",
                              context=full_context())
        self.assertEqual(cm.exception.code, "feature_not_built")

    # ---- F3: decl_for shapes ----
    def test_decl_for_shapes(self):
        self.assertEqual(decl_for({"features": {"smart_bars": True}}),
                         {"enabled": True})
        d = {"enabled": True, "sections": []}
        self.assertEqual(decl_for({"features": {"smart_bars": d}}), d)
        self.assertIsNone(decl_for({"features": {"smart_bars": False}}))
        self.assertIsNone(decl_for({"features": {}}))
        self.assertIsNone(decl_for({}))
        with self.assertRaises(BarsRefusal) as cm:
            decl_for({"features": {"smart_bars": "yes please"}})
        self.assertEqual(cm.exception.code, "bad_smart_bars_declaration")

    # ---- sanitize_section ----
    def test_sanitize_section_accepts_good(self):
        s = sanitize_section({"id": " about ", "title": " About ",
                              "address": " /about "})
        self.assertEqual((s["id"], s["title"], s["address"]),
                         ("about", "About", "/about"))

    # ---- F7: malformed sections -> structured refusal, never dropped ----
    def test_sanitize_section_rejects_malformed(self):
        bad = [
            "not a dict",
            {"id": "", "title": "T", "address": "/a"},
            {"id": "  ", "title": "T", "address": "/a"},
            {"id": "x", "title": "", "address": "/a"},
            {"id": "x", "title": "  ", "address": "/a"},
            {"id": "x", "title": "T", "address": ""},
            {"id": "x", "title": "T", "address": "no-leading-slash"},
            {"id": "x", "title": "T"},
            {"title": "T", "address": "/a"},
            {"id": "x", "address": "/a"},
        ]
        for b in bad:
            with self.assertRaises(BarsRefusal) as cm:
                sanitize_section(b)
            self.assertEqual(cm.exception.code, "bad_bar", b)

    # ---- F4: bars_present_on_sections: every section, a real href ----
    def test_all_sections_present_with_real_hrefs(self):
        html = render_smart_bars(dict(BARS_DECL), "built",
                                 context=full_context())
        for sec in BARS_DECL["sections"]:
            self.assertIn('href="%s"' % sec["address"], html)
        # title escaping: the "<kitchen>" title must not break out
        self.assertIn("My &lt;kitchen&gt;", html)
        self.assertNotIn("My <kitchen>", html)
        # every link carries the bar identity hooks
        self.assertEqual(html.count('class="smart-bar-link"'), 3)
        # binding marker + consent word
        self.assertIn('data-bars-status="built"', html)
        self.assertIn('data-consent="ready"', html)
        self.assertIn('data-receipt-events="bars.rendered"', html)

    # ---- F5: permission gate: no grant -> honest gated block ----
    def test_render_gated_without_permission(self):
        ctx = full_context(granted_permissions=[])
        html = render_smart_bars(dict(BARS_DECL), "built", context=ctx)
        # the resolver's own human words, byte-matched
        self.assertIn("render the smart navigation bars", html)
        # no working chrome: no hrefs at all
        self.assertNotIn("href=", html)
        self.assertNotIn('class="smart-bar-link"', html)
        # no section title leaks into a working link
        self.assertNotIn('data-section-title', html)

    # ---- F6: empty state: declared, zero sections -> honest line ----
    def test_empty_state(self):
        html = render_smart_bars({"enabled": True, "sections": []}, "built",
                                 context=full_context())
        self.assertIn("No sections yet", html)
        self.assertNotIn('class="smart-bar-link"', html)
        self.assertNotIn("<ul", html)

    # ---- F8: mobile collapse ----
    def test_mobile_collapse_present_above_threshold(self):
        html = render_smart_bars(dict(LONG_DECL), "built",
                                 context=full_context())
        self.assertIn('<details class="smart-bars-mobile">', html)
        # all 7 section links appear in BOTH the desktop list and the
        # collapsed mobile list -> collapse never hides a section
        self.assertEqual(html.count('class="smart-bar-link"'), 14)
        for sec in LONG_DECL["sections"]:
            self.assertIn('href="%s"' % sec["address"], html)

    def test_no_mobile_collapse_at_or_below_threshold(self):
        html = render_smart_bars(dict(BARS_DECL), "built",
                                 context=full_context())
        self.assertNotIn("smart-bars-mobile", html)
        self.assertEqual(html.count('class="smart-bar-link"'), 3)

    # ---- permission evaluation ----
    def test_can_render_evaluates_grant(self):
        ok, missing = can_render(full_context())
        self.assertTrue(ok)
        self.assertEqual(missing, [])
        ok, missing = can_render(full_context(granted_permissions=[]))
        self.assertFalse(ok)
        self.assertEqual(missing, ["render the smart navigation bars"])

    # ---- determinism ----
    def test_deterministic_bytes(self):
        a = render_smart_bars(dict(BARS_DECL), "built",
                              context=full_context())
        b = render_smart_bars(dict(BARS_DECL), "built",
                              context=full_context())
        self.assertEqual(a, b)


class SmartBarsResolver(unittest.TestCase):
    def test_resolve_activates_with_binding(self):
        r = resolve("feature.smart_bars", full_context())
        self.assertTrue(r["activated"])
        self.assertEqual(r["events"], ["bars.rendered"])
        self.assertIn('data-bars-status="built"', r["output"])
        # bars_present_on_sections at the resolver level
        for sec in BARS_DECL["sections"]:
            self.assertIn('href="%s"' % sec["address"], r["output"])

    def test_resolve_refuses_when_permission_missing(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.smart_bars",
                    full_context(granted_permissions=[]))
        e = cm.exception
        self.assertEqual(e.code, "permission_denied")
        self.assertEqual(e.missing, ["bars.render"])
        self.assertIn("render the smart navigation bars", e.detail)

    def test_resolve_refuses_when_requirement_unmet(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.smart_bars", full_context(available=[]))
        e = cm.exception
        self.assertEqual(e.code, "requirement_unmet")
        self.assertEqual(e.missing, ["navigation_service"])
        self.assertIn("navigation_service", e.detail)

    def test_resolve_propagates_bad_declaration_as_module_refusal(self):
        # the decl_for call sits outside the resolver's try — a bad
        # declaration propagates as the module's own refusal (the same
        # pattern holds for tabs' TabsRefusal). assemble.py guards the
        # contract surface with bad_breaker_declaration before resolve().
        c = full_context()
        c["contract"] = {"features": {"smart_bars": "yes please"}}
        with self.assertRaises(BarsRefusal) as cm:
            resolve("feature.smart_bars", c)
        self.assertEqual(cm.exception.code, "bad_smart_bars_declaration")


class SmartBarsAssemble(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fbars-e2e-")

    def test_assemble_renders_honest_breaker_row(self):
        r, page, _ = run_assemble(
            bars_contract(self.tmp, dict(BARS_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.smart_bars"', page)
        # bars carry no connected action: consent is always "ready"
        self.assertIn('data-consent="ready"', page)

    def test_assemble_refuses_undeclared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="feature.smart_bars"', page)

    def test_assemble_refuses_bad_declaration(self):
        r, page, _ = run_assemble(
            bars_contract(self.tmp, "yes please"), self.tmp)
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
                if f.get("id") == "feature.smart_bars":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        r, page, _ = run_assemble(
            bars_contract(self.tmp, dict(BARS_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)


if __name__ == "__main__":
    unittest.main(verbosity=2)

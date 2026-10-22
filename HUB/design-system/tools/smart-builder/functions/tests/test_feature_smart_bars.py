#!/usr/bin/env python3
"""Acceptance tests for feature.smart_bars (registry acceptance:
bars_present_on_sections, mobile_collapse_tested).

Stdlib only (unittest + subprocess). Each test runs the real
assemble.py end-to-end against the real builder index:

  day-one                 -> minimal contract -> useful render, ZERO errors
  three-state             -> explicit true: on; explicit false: off (no render,
                             no claim, no error — even with an unbuilt
                             registry); omitted: assembler policy
  bars_present_on_sections-> default bar links hit real template anchors
  mobile_collapse_tested  -> checkbox toggle + media query, no script at all
  privacy dial            -> audience-scoped links filter at all three dials
  consent line            -> ready (zero grants); sync=true without the
                             nayanet grant -> missing_grant refusal naming it;
                             with grant -> connected, mirrored in receipt
  sanitization            -> hostile hrefs -> structured refusal (exit 2)
  registry binding        -> contract cannot activate what the registry does
                             not mark 'built' (fail closed)
  determinism             -> same contract -> same bytes
  href audit (L-2026-10-17-002) -> builder-generated default links resolve in
                             the template; declared links are owner content
                             (verified safe/well-formed, like cover URLs)
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SB_DIR = os.path.normpath(os.path.join(TESTS_DIR, "..", ".."))
INDEX = os.path.normpath(os.path.join(
    SB_DIR, "..", "..", "library", "catalog", "builder-index-v1.json"))
ASSEMBLE = os.path.join(SB_DIR, "assemble.py")
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")
TEMPLATE = os.path.join(SB_DIR, "templates", "page.html")

MODULE_ID = "feature.smart_bars"

BARS_DECL = {
    "enabled": True,
    "brand": "Morning Crumb",
    "links": [
        {"label": "Menu", "href": "#features"},
        {"label": "Order ahead", "href": "https://order.morning-crumb.example/"},
    ],
}


def customer_contract(tmp, features, top_extra=None):
    """A customer contract: smoke contract with features as a breaker dict,
    plus optional top-level keys (privacy, connections)."""
    c = json.load(open(SMOKE))
    c["title"] = "Smart bars acceptance contract"
    c["features"] = features
    for k, v in (top_extra or {}).items():
        c[k] = v
    p = os.path.join(tmp, "contract.json")
    json.dump(c, open(p, "w"))
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


def sb_copy_with_status(tmp, module_id, status):
    """Copy the smart-builder tree once per tmpdir, flip one module status."""
    tree = os.path.join(tmp, "sbcopy")
    if not os.path.isdir(tree):
        shutil.copytree(SB_DIR, tree)
    regp = os.path.join(tree, "functions", "registry.json")
    reg = json.load(open(regp))
    for g in reg["groups"].values():
        for f in g.get("functions", []):
            if f.get("id") == module_id:
                f["status"] = status
    json.dump(reg, open(regp, "w"), indent=1)
    return os.path.join(tree, "assemble.py")


class FeatureSmartBarsAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fbars-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def built_assemble(self, status="built"):
        return sb_copy_with_status(self.tmp, MODULE_ID, status)

    def run_built(self, decl, top_extra=None, status="built"):
        contract = customer_contract(self.tmp, {"smart_bars": decl}, top_extra)
        return run_assemble(contract, self.tmp,
                            assemble=self.built_assemble(status))

    def bars_block(self, page):
        return page.split('data-feature="smart_bars"')[1].split("</nav>")[0]

    # ---- DAY-ONE: minimal contract -> useful render, ZERO errors ----
    def test_day_one_minimal_contract(self):
        r, page, manifest = self.run_built(True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("refused", r.stdout)
        self.assertIn('data-feature="smart_bars"', page)
        self.assertIn('data-smart-bars-status="built"', page)
        # the default bar: brand + real section links, never an empty nav
        block = self.bars_block(page)
        self.assertIn('href="#top"', block)
        self.assertIn('href="#features"', block)

    # ---- three-state: explicit true -> on ----
    def test_explicit_true_activation(self):
        r, page, manifest = self.run_built(dict(BARS_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_bars"', page)
        self.assertIn('data-smart-bars-status="built"', page)
        self.assertIn("Morning Crumb", page)
        self.assertIn('href="#features"', page)
        self.assertIn('href="https://order.morning-crumb.example/"', page)
        self.assertIn('data-mode="ready"', page)
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["smart_bars"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "bars.rendered"
                            and e.get("feature") == MODULE_ID for e in events))

    # ---- three-state: explicit false -> off (no render, no claim, no error) ----
    def test_explicit_false_suppression(self):
        for decl in (False, {"enabled": False},
                     {"enabled": False, "links": [
                         {"label": "X", "href": "javascript:alert(1)"}]}):
            r, page, manifest = self.run_built(decl)
            self.assertEqual(r.returncode, 0, "decl %r: %s" % (decl, r.stdout))
            self.assertNotIn('data-feature="smart_bars"', page)
            self.assertNotIn('<nav class="sb-bar"', page)
            events = manifest.get("receipt", {}).get("events", [])
            self.assertFalse(any(e.get("event") == "bars.rendered"
                                 for e in events))

    def test_explicit_false_ignores_registry(self):
        # off means off: not even the registry gate runs for an opted-out
        # breaker — no feature_not_built claim, no error.
        r, page, _ = self.run_built(False, status="specified")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_bars"', page)

    # ---- three-state: omitted -> assembler policy (bars: default-off) ----
    def test_omitted_follows_policy(self):
        contract = customer_contract(self.tmp, {})
        r, page, _ = run_assemble(contract, self.tmp,
                                  assemble=self.built_assemble())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_bars"', page)

    # ---- bars_present_on_sections: default bar links hit real anchors ----
    def test_default_bar_anchors_resolve_in_template(self):
        r, page, _ = self.run_built({"enabled": True})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.bars_block(page)
        template = open(TEMPLATE, encoding="utf-8").read()
        hrefs = re.findall(r'href="([^"]+)"', block)
        self.assertTrue(hrefs)
        for href in hrefs:
            self.assertTrue(href.startswith("#"), href)
            self.assertIn('id="%s"' % href[1:], template,
                          "builder-generated default bar links to #%s, "
                          "absent from the template" % href[1:])

    # ---- privacy dial: audience-scoped links filter at all three dials ----
    def test_audience_filtering_all_three_dials(self):
        decl = {"enabled": True, "brand": "B", "links": [
            {"label": "Home", "href": "#top"},
            {"label": "Members", "href": "#features", "audience": "network"},
            {"label": "World", "href": "https://example.com/", "audience": "public"},
        ]}
        expectations = {
            "private": (["Home"], ["Members", "World"]),
            "network": (["Home", "Members"], ["World"]),
            "public": (["Home", "Members", "World"], []),
        }
        for dial, (shown, hidden) in expectations.items():
            r, page, _ = self.run_built(
                dict(decl), top_extra={"privacy": dial})
            self.assertEqual(r.returncode, 0, "%s: %s" % (dial, r.stdout))
            block = self.bars_block(page)
            self.assertIn('data-privacy="%s"' % dial, page)
            for label in shown:
                self.assertIn(">%s<" % label, block, (dial, label))
            for label in hidden:
                self.assertNotIn(">%s<" % label, block, (dial, label))

    def test_invalid_audience_refused(self):
        decl = {"enabled": True, "links": [
            {"label": "X", "href": "#top", "audience": "everyone"}]}
        r, page, _ = self.run_built(decl)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_bar_link", codes)

    def test_bad_privacy_dial_refused(self):
        r, page, _ = self.run_built(
            True, top_extra={"privacy": "super-public"})
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_privacy", codes)
        self.assertNotIn('data-feature="smart_bars"', page)

    # ---- consent line: ready with zero grants; sync needs its grant ----
    def test_ready_with_zero_grants(self):
        r, page, manifest = self.run_built(dict(BARS_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-mode="ready"', page)
        self.assertNotIn('data-grant=', self.bars_block(page))
        readiness = manifest["receipt"]["readiness"]
        info = [r for r in readiness if r["feature"] == MODULE_ID][0]
        self.assertEqual(info["consent"], "ready")
        self.assertEqual(manifest["receipt"]["grants"],
                         {"muse": False, "github": False,
                          "network": False, "nayanet": False})

    def test_sync_without_grant_refused_naming_grant(self):
        decl = dict(BARS_DECL, sync=True)
        r, page, _ = self.run_built(decl)  # zero grants
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        grant_errs = [e for e in errs if e.get("code") == "missing_grant"]
        self.assertTrue(grant_errs, errs)
        self.assertIn("nayanet", grant_errs[0]["detail"])
        self.assertIn("contract.connections.nayanet", grant_errs[0]["detail"])
        self.assertNotIn('data-feature="smart_bars"', page)

    def test_sync_with_grant_connected(self):
        decl = dict(BARS_DECL, sync=True)
        r, page, manifest = self.run_built(
            decl, top_extra={"connections": {"nayanet": True}})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.bars_block(page)
        self.assertIn('data-mode="connected"', block)
        self.assertIn('data-grant="nayanet"', block)
        readiness = manifest["receipt"]["readiness"]
        info = [r for r in readiness if r["feature"] == MODULE_ID][0]
        self.assertEqual(info["mode"], "connected")
        self.assertEqual(info["consent"], "connected")
        self.assertTrue(manifest["receipt"]["grants"]["nayanet"])

    # ---- mobile_collapse_tested: pure CSS toggle, zero script ----
    def test_mobile_collapse_no_script(self):
        r, page, _ = self.run_built(dict(BARS_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.bars_block(page)
        self.assertIn('type="checkbox"', block)
        self.assertIn('id="sb-nav-toggle"', block)
        self.assertIn('for="sb-nav-toggle"', block)
        self.assertNotIn("<script", block)
        self.assertIn("@media(max-width:640px)", page)
        self.assertIn(".sb-nav-toggle:checked", page)

    # ---- gate: nothing renders for the contract-page shape ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_bars"', page)

    # ---- sanitization: hostile hrefs are structured refusals ----
    def test_href_sanitization_refusals(self):
        bad = [
            "javascript:alert(1)",
            "JaVaScRiPt:alert(1)",
            "vbscript:msgbox(1)",
            "data:text/html,<b>",
            "ftp://example.com/x",
            "//evil.example/x",
            "relative/path",
            "#no spaces",
            "#",
            "http:///no-host",
            "https://exa mple.com/",
            "java\tscript:alert(1)",
        ]
        for href in bad:
            decl = {"enabled": True, "brand": "B",
                    "links": [{"label": "X", "href": href}]}
            r, page, _ = self.run_built(decl)
            self.assertEqual(r.returncode, 2, "href accepted: %r" % href)
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            codes = [e["code"] for e in body["errors"]]
            self.assertIn("unsafe_bar_href", codes, href)
            self.assertNotIn('data-feature="smart_bars"', page)

    def test_bad_link_shapes_refused(self):
        for links, code in [
            ("nope", "bad_bar_link"),
            ([{"label": "", "href": "#x"}], "bad_bar_link"),
            ([{"label": "X"}], "unsafe_bar_href"),
            ([{"label": "X", "href": "#x"}] * 25, "too_many_links"),
            ([{"nope": 1}], "bad_bar_link"),
        ]:
            decl = {"enabled": True, "links": links}
            r, page, _ = self.run_built(decl)
            self.assertEqual(r.returncode, 2, links)
            codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
            self.assertIn(code, codes, links)

    # ---- malformed declaration: fail closed, not improvised ----
    def test_malformed_declaration_refused(self):
        r, page, _ = self.run_built("yes please")
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_smart_bars_declaration", codes)

    # ---- the general gate: an unbuilt breaker fails the contract closed ----
    def test_unbuilt_breaker_refused(self):
        # explicit true + registry 'specified' -> the contract claimed an
        # unbuilt capability -> structured refusal.
        r, page, _ = self.run_built(dict(BARS_DECL), status="specified")
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        bars_errs = [e for e in errs if e.get("feature") == MODULE_ID]
        self.assertTrue(bars_errs, errs)
        self.assertEqual(bars_errs[0]["code"], "feature_not_built")
        self.assertNotIn('data-feature="smart_bars"', page)

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = customer_contract(self.tmp, {"smart_bars": dict(BARS_DECL)})
        asm = self.built_assemble()
        _, page1, _ = run_assemble(contract, self.tmp, assemble=asm)
        d2 = tempfile.mkdtemp(prefix="fbars-b-")
        try:
            _, page2, _ = run_assemble(contract, d2, assemble=asm)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())

    # ---- L-2026-10-17-002: declared anchors are owner content ----
    def test_declared_anchors_render_verbatim_when_well_formed(self):
        # Declared anchors are the contract author's content (like cover
        # photo URLs): verified safe and well-formed at build time. The
        # builder-generated default bar is the part verified live against
        # the template (test_default_bar_anchors_resolve_in_template).
        r, page, _ = self.run_built(dict(BARS_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('href="#features"', self.bars_block(page))

    # ---- the module's CSS only uses real template tokens ----
    def test_module_css_vars_exist_in_template(self):
        template = open(TEMPLATE, encoding="utf-8").read()
        defined = set(re.findall(r"(--[\w-]+)\s*:",
                                 re.search(r":root\{(.*?)\}", template,
                                           re.S).group(1)))
        block = re.search(
            r"/\* ============ feature\.smart_bars.*?\*/(.*?)(?=/\* ============)",
            template, re.S).group(1)
        for var in set(re.findall(r"var\((--[\w-]+)\)", block)):
            self.assertIn(var, defined, "undefined CSS var %s" % var)

    # ---- rendered fragments are well-formed HTML ----
    def test_fragment_parses_clean(self):
        from html.parser import HTMLParser

        class P(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.stack = []
                self.errors = []

            def handle_starttag(self, tag, attrs):
                if tag not in ("input", "img", "br", "meta", "link", "hr"):
                    self.stack.append(tag)

            def handle_endtag(self, tag):
                if self.stack and self.stack[-1] == tag:
                    self.stack.pop()
                else:
                    self.errors.append((tag, list(self.stack)))

        sys.path.insert(0, os.path.join(SB_DIR, "functions"))
        try:
            from feature_smart_bars import render_smart_bars
        finally:
            sys.path.pop(0)
        frags = [
            render_smart_bars({"enabled": True}, "built")[0],
            render_smart_bars(
                {"enabled": True, "brand": "B",
                 "links": [{"label": "L", "href": "#x", "audience": "public"}],
                 "sync": True},
                "built",
                {"privacy": "public",
                 "connections": {"muse": False, "github": False,
                                 "network": True, "nayanet": True}})[0],
        ]
        for frag in frags:
            p = P()
            p.feed(frag)
            self.assertFalse(p.errors, p.errors)
            self.assertFalse(p.stack, p.stack)


if __name__ == "__main__":
    unittest.main(verbosity=2)

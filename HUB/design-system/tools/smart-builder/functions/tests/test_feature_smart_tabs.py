#!/usr/bin/env python3
"""Acceptance tests for feature.smart_tabs (registry acceptance:
all_owned_pages_reachable, tab_switch_tested).

Stdlib only (unittest + subprocess). Each test runs the real
assemble.py end-to-end against the real builder index:

  activation              -> contract-declared pages land as tab anchors
  explicit true/false     -> true renders; explicit false suppresses
                             (no render, no claim)
  omitted (dict-form)     -> assembler default-on policy (standards on)
  omitted (list-form)     -> off (the contract page keeps F1 semantics)
  day-one                 -> minimal declaration renders useful output,
                             zero errors, no setup
  connections             -> the module gates nothing on connections;
                             identical output with or without them
  privacy dial            -> data-privacy-scope stamped (default private);
                             unknown values refused
  gate                    -> no tabs markup unless the contract declares it
  sanitization            -> hostile tab URLs -> structured refusal (exit 2)
  malformed declarations  -> fail closed, never improvised
  fallback                -> enabled but no pages -> "This page" chrome
  registry binding        -> contract cannot activate what the registry does
                             not mark 'built' (fail closed)
  determinism             -> same contract -> same bytes

The wave-B modules ship with registry status 'specified'; activation
tests run against a temp tree where the module is flipped to 'built'
(the flip is the final step, never a test fixture).
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
INDEX = os.path.normpath(os.path.join(
    SB_DIR, "..", "..", "library", "catalog", "builder-index-v1.json"))
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")

TABS_DECL = {
    "enabled": True,
    "pages": [
        {"title": "Morning Crumb", "url": "https://morning-crumb.nayanet.live/"},
        {"title": "Bakes", "url": "https://morning-crumb.nayanet.live/bakes"},
        {"title": "About", "url": "https://morning-crumb.nayanet.live/about"},
    ],
    "active_url": "https://morning-crumb.nayanet.live/",
}


def tree_with_status(tmp, status):
    """A copy of the smart-builder tree with the three wave-B modules
    flipped to the given registry status (the post-flip production state
    is all three 'built')."""
    tree = os.path.join(tmp, "sbtree")
    if os.path.exists(tree):
        shutil.rmtree(tree)
    shutil.copytree(SB_DIR, tree)
    regp = os.path.join(tree, "functions", "registry.json")
    reg = json.load(open(regp))
    for g in reg["groups"].values():
        for f in g.get("functions", []):
            if f.get("id") in ("feature.smart_tabs",
                               "feature.intelligence_today",
                               "feature.contacts"):
                f["status"] = status
    json.dump(reg, open(regp, "w"), indent=1)
    return tree


def tabs_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    c = json.load(open(SMOKE))
    c["title"] = "Smart tabs acceptance contract"
    c["features"] = {"smart_tabs": decl}
    p = os.path.join(tmp, "contract.json")
    json.dump(c, open(p, "w"))
    return p


def full_contract(tmp, features, privacy=None, connections=None):
    """A customer contract with an explicit features dict plus optional
    top-level privacy/connections blocks."""
    c = json.load(open(SMOKE))
    c["title"] = "Smart tabs acceptance contract"
    c["features"] = features
    if privacy is not None:
        c["privacy"] = privacy
    if connections is not None:
        c["connections"] = connections
    p = os.path.join(tmp, "contract.json")
    json.dump(c, open(p, "w"))
    return p


def run_assemble(contract, workdir, assemble):
    out = os.path.join(workdir, "page.html")
    man = os.path.join(workdir, "page.manifest.json")
    r = subprocess.run(
        [sys.executable, assemble, "--contract", contract, "--index", INDEX,
         "--template", os.path.join(os.path.dirname(assemble), "templates", "page.html"),
         "--out", out, "--manifest", man],
        capture_output=True, text=True, timeout=120)
    page = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
    manifest = {}
    if os.path.exists(man):
        with open(man) as fh:
            manifest = json.load(fh)
    return r, page, manifest


class FeatureSmartTabsAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ftabs-")
        self.tree = tree_with_status(self.tmp, "built")
        self.assemble = os.path.join(self.tree, "assemble.py")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- all_owned_pages_reachable: every declared page lands as a tab ----
    def test_activation_via_contract(self):
        r, page, manifest = run_assemble(
            tabs_contract(self.tmp, dict(TABS_DECL)), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_tabs"', page)
        self.assertIn('data-smart_tabs-status="built"', page)
        # every declared URL is a real href (L-2026-10-17-002: verified, not
        # claimed) — and nothing else is
        hrefs = __import__("re").findall(
            r'<a[^>]*class="smart-tab[^"]*"[^>]*href="([^"]+)"', page)
        self.assertEqual(sorted(hrefs), sorted(
            p["url"] for p in TABS_DECL["pages"]))
        self.assertIn("Morning Crumb", page)
        self.assertIn("Bakes", page)
        # tab_switch_tested: the current tab is marked
        self.assertIn('aria-current="page"', page)
        self.assertIn('href="https://morning-crumb.nayanet.live/"', page)
        machine = json.loads(__import__("re").search(
            r'<pre id="machinejson">(.*?)</pre>', page, __import__("re").S).group(1))
        self.assertEqual(machine["features_status"]["smart_tabs"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "smart_tabs.updated"
                            and e.get("feature") == "feature.smart_tabs"
                            for e in events))

    # ---- gate: the page refuses to render tabs it was not given ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp, self.assemble)  # list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_tabs"', page)
        self.assertNotIn('<nav class="smart-tabs"', page)

    def test_refusal_when_declared_but_disabled(self):
        decl = dict(TABS_DECL, enabled=False)
        r, page, manifest = run_assemble(
            tabs_contract(self.tmp, decl), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_tabs"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "smart_tabs.updated"
                             for e in events))

    # ---- sanitization: hostile tab URLs are structured refusals ----
    def test_url_sanitization_refusals(self):
        bad = [
            "javascript:alert(1)",
            "JaVaScRiPt:alert(1)",
            "vbscript:msgbox(1)",
            "data:text/html;base64,PGI+",
            "ftp://example.com/x",
            "file:///etc/passwd",
            "//evil.example/x",
            "pages/relative",
            "http:///no-host",
            "https://exa mple.com/x",
        ]
        for url in bad:
            decl = {"enabled": True, "pages": [{"title": "Evil", "url": url}]}
            r, page, _ = run_assemble(
                tabs_contract(self.tmp, decl), self.tmp, self.assemble)
            self.assertEqual(r.returncode, 2, "url accepted: %r" % url)
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            codes = [e["code"] for e in body["errors"]]
            self.assertIn("unsafe_tabs_url", codes, url)
            self.assertNotIn('data-feature="smart_tabs"', page)

    def test_active_url_trailing_slash_insensitive(self):
        # the contract may name the active tab with or without a trailing
        # slash; both name the same tab
        decl = dict(TABS_DECL, active_url="https://morning-crumb.nayanet.live")
        r, page, _ = run_assemble(
            tabs_contract(self.tmp, decl), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        active = __import__("re").findall(
            r'<a[^>]*class="smart-tab is-current"[^>]*href="([^"]+)"', page)
        self.assertEqual(active, ["https://morning-crumb.nayanet.live/"])

    def test_active_url_sanitized(self):
        decl = dict(TABS_DECL, active_url="javascript:alert(1)")
        r, page, _ = run_assemble(
            tabs_contract(self.tmp, decl), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("unsafe_tabs_url", codes)

    def test_xss_in_titles_escaped(self):
        decl = {"enabled": True, "pages": [
            {"title": '<script>alert(1)</script>', "url": "https://example.com/a"},
            {"title": 'A "quoted" & <b>bold</b>', "url": "https://example.com/b"},
        ]}
        r, page, _ = run_assemble(
            tabs_contract(self.tmp, decl), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertIn("A &quot;quoted&quot; &amp; &lt;b&gt;bold&lt;/b&gt;", page)

    # ---- malformed declarations: fail closed, never improvised ----
    def test_malformed_declaration_refused(self):
        r, page, _ = run_assemble(
            tabs_contract(self.tmp, "yes please"), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_tabs_declaration", codes)
        self.assertNotIn('data-feature="smart_tabs"', page)

    def test_malformed_page_entries_refused(self):
        cases = [
            {"enabled": True, "pages": "not-a-list"},
            {"enabled": True, "pages": [{"url": "https://example.com/a"}]},  # no title
            {"enabled": True, "pages": [{"title": "", "url": "https://example.com/a"}]},
            {"enabled": True, "pages": [{"title": 42, "url": "https://example.com/a"}]},
            {"enabled": True,
             "pages": [{"title": "t%d" % i, "url": "https://example.com/%d" % i}
                       for i in range(25)]},  # over MAX_PAGES
        ]
        for decl in cases:
            r, page, _ = run_assemble(
                tabs_contract(self.tmp, decl), self.tmp, self.assemble)
            self.assertEqual(r.returncode, 2, decl)
            self.assertNotIn('data-feature="smart_tabs"', page)

    # ---- fallback: enabled but no pages -> "This page" chrome ----
    def test_fallback_when_pages_missing(self):
        for decl in ({"enabled": True},
                     {"enabled": True, "pages": []},
                     True):
            r, page, _ = run_assemble(
                tabs_contract(self.tmp, decl), self.tmp, self.assemble)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn('data-feature="smart_tabs"', page)
            self.assertIn("This page", page)
            # chrome with one current tab, never a link the contract did not
            # declare
            nav = page.split('data-feature="smart_tabs"')[1].split("</nav>")[0]
            self.assertNotIn("<a", nav)

    # ---- the general gate: an unbuilt breaker fails the contract closed ----
    def test_unbuilt_breaker_refused(self):
        tree = tree_with_status(self.tmp, "specified")
        asm = os.path.join(tree, "assemble.py")
        r, page, _ = run_assemble(
            tabs_contract(self.tmp, dict(TABS_DECL)), self.tmp, asm)
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        tabs_errs = [e for e in errs if e.get("feature") == "feature.smart_tabs"]
        self.assertTrue(tabs_errs, errs)
        self.assertIn("feature_not_built", [e["code"] for e in tabs_errs])
        self.assertNotIn('data-feature="smart_tabs"', page)

    # ---- three-state: explicit false suppresses, no render, no claim ----
    def test_explicit_false_scalar_suppression(self):
        r, page, manifest = run_assemble(
            full_contract(self.tmp, {"smart_tabs": False}), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_tabs"', page)
        self.assertNotIn('<nav class="smart-tabs"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "smart_tabs.updated"
                             for e in events))

    # ---- three-state: omitted (dict-form) -> assembler default-on policy ----
    def test_omitted_defaults_on_for_dict_form(self):
        r, page, manifest = run_assemble(
            full_contract(self.tmp, {}), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        # smart_tabs is a standard feature: on by default
        self.assertIn('data-feature="smart_tabs"', page)
        nav_tag = page.split('<nav class="smart-tabs"')[1].split(">")[0]
        self.assertIn('data-privacy-scope="private"', nav_tag)
        # contacts is not standard: stays off unless flipped
        self.assertNotIn('data-feature="contacts"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "smart_tabs.updated"
                            for e in events))

    def test_omitted_default_on_refused_when_unbuilt(self):
        # Coverage-gated policy (integrator ruling): the bundle's immediate
        # default-on was stripped. With unbuilt standard features the gate
        # is INACTIVE -> omitted = OFF (opt-in), no refusal. The sharpened
        # fail-closed refuses only EXPLICIT claims of unbuilt features
        # (impossible for default-on: gate active implies all built).
        tree = tree_with_status(self.tmp, "specified")
        asm = os.path.join(tree, "assemble.py")
        r, page, _ = run_assemble(
            full_contract(self.tmp, {}), self.tmp, asm)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_tabs"', page)

    # ---- day-one: the minimal declaration renders useful output, zero errors
    def test_day_one_minimal_contract(self):
        r, page, _ = run_assemble(
            full_contract(self.tmp, {"smart_tabs": True}), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("refused", r.stdout)
        self.assertIn('data-feature="smart_tabs"', page)
        self.assertIn("This page", page)  # useful chrome, no setup wizard

    # ---- connections: the module gates nothing on them ----
    def test_connections_do_not_gate(self):
        off = {"muse": False, "github": False, "network": False,
               "nayanet": False}
        r1, page1, _ = run_assemble(
            full_contract(self.tmp, {"smart_tabs": True},
                          connections=off), self.tmp, self.assemble)
        self.assertEqual(r1.returncode, 0, r1.stdout + r1.stderr)
        self.assertIn('data-feature="smart_tabs"', page1)
        d2 = tempfile.mkdtemp(prefix="ftabs-c-")
        try:
            r2, page2, _ = run_assemble(
                full_contract(d2, {"smart_tabs": True}), d2, self.assemble)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(r2.returncode, 0)
        # feature enabled renders the same UI with connections absent or
        # all-false: enabled ≠ connected, never a crash
        self.assertEqual(page1, page2)

    # ---- privacy dial: stamped, default private, unknown refused ----
    def test_privacy_dial_scopes(self):
        for scope in ("private", "network", "public"):
            r, page, _ = run_assemble(
                full_contract(self.tmp, {"smart_tabs": True},
                              privacy=scope), self.tmp, self.assemble)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            nav_tag = page.split('<nav class="smart-tabs"')[1].split(">")[0]
            self.assertIn('data-privacy-scope="%s"' % scope, nav_tag)

    def test_privacy_bad_value_refused(self):
        # privacy is validated once per build (resolve_contract_context):
        # page-level fail-closed refusal
        r, page, _ = run_assemble(
            full_contract(self.tmp, {"smart_tabs": True},
                          privacy="everyone"), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_privacy", codes)
        self.assertNotIn('data-feature="smart_tabs"', page)

    # ---- consent line: READY needs no grant; the receipt mirrors grants ----
    def test_ready_works_with_all_grants_false(self):
        off = {"muse": False, "github": False, "network": False,
               "nayanet": False}
        r, page, manifest = run_assemble(
            full_contract(self.tmp, {"smart_tabs": True}, connections=off),
            self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_tabs"', page)
        events = manifest.get("receipt", {}).get("events", [])
        tabs = [e for e in events if e.get("event") == "smart_tabs.updated"]
        self.assertTrue(tabs)
        self.assertEqual(tabs[0]["grants"], off)

    def test_capability_contract_carries_readiness_split(self):
        reg = json.load(open(os.path.join(
            self.tree, "functions", "registry.json")))
        entry = None
        for g in reg["groups"].values():
            for f in g.get("functions", []):
                if f.get("id") == "feature.smart_tabs":
                    entry = f
        self.assertIsNotNone(entry)
        # READY vs CONNECTED carried as top-level contract keys
        # (resolve_consent reads entry['ready'] / entry['connected'])
        ready = entry.get("ready", [])
        self.assertTrue(ready)
        # CONNECTED: none — nothing to consent to
        self.assertEqual(entry.get("connected"), [])

    def test_ui_copy_never_claims_connected(self):
        r, page, _ = run_assemble(
            full_contract(self.tmp, {"smart_tabs": True}), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        nav = page.split('data-feature="smart_tabs"')[1].split("</nav>")[0]
        self.assertNotIn("connected", nav.lower())

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = tabs_contract(self.tmp, dict(TABS_DECL))
        _, page1, _ = run_assemble(contract, self.tmp, self.assemble)
        d2 = tempfile.mkdtemp(prefix="ftabs-b-")
        try:
            _, page2, _ = run_assemble(contract, d2, self.assemble)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Acceptance tests for feature.smart_notes (registry acceptance:
note_from_context_composed, link_minted_deterministic, unsafe_content_sanitized,
capture_panel_fallback, link_not_claimed_live).

Stdlib only (unittest + subprocess). The work-tree registry carries the module
as 'specified' until the flip; each test therefore runs assemble from a
fixture copy of the smart-builder tree whose registry marks the module
'built' — except test_specified_registry_refuses, which proves the gate
refuses while specified. Every test runs the real assemble.py end-to-end
against the real builder index.
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
from html.parser import HTMLParser

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SB_DIR = os.path.normpath(os.path.join(TESTS_DIR, "..", ".."))
ASSEMBLE = os.path.join(SB_DIR, "assemble.py")
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")

SN_DECL = {
    "enabled": True,
    "link_base": "https://nayanet.live",
    "page_address": "nayanet.live/morning-crumb",
    "notes": [
        {"title": "Sourdough at 6am",
         "body": "The crumb sings.\nSecond line here.",
         "voice": "naya"},
        {"title": "Rye note",
         "body": "Dark and honest.",
         "voice": "grandma"},
    ],
}

FLIP_IDS = ("feature.smart_notes",)


def flip_registry(tree):
    regp = os.path.join(tree, "functions", "registry.json")
    reg = json.load(open(regp))
    for g in reg["groups"].values():
        for f in g.get("functions", []):
            if f.get("id") in FLIP_IDS:
                f["status"] = "built"
    json.dump(reg, open(regp, "w"), indent=2)


def sn_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    c = json.load(open(SMOKE))
    c["title"] = "Smart notes acceptance contract"
    c["features"] = {"smart_notes": decl}
    p = os.path.join(tmp, "contract.json")
    json.dump(c, open(p, "w"))
    return p


def run_assemble(contract, workdir, assemble=ASSEMBLE, sb_dir=SB_DIR):
    # the index always comes from the real tree: the fixture copy preserves
    # layout but not ancestry (F1 pattern).
    index = os.path.normpath(os.path.join(
        SB_DIR, "..", "..", "library", "catalog", "builder-index-v1.json"))
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


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.copy_targets = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if a.get("data-copy-target"):
            self.copy_targets.add(a["data-copy-target"])


class FeatureSmartNotesAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fsn-")
        # fixture tree: the module marked built (the real flip comes later)
        self.tree = os.path.join(self.tmp, "sbcopy")
        shutil.copytree(SB_DIR, self.tree)
        flip_registry(self.tree)
        self.assemble = os.path.join(self.tree, "assemble.py")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_decl(self, decl):
        return run_assemble(sn_contract(self.tmp, decl), self.tmp,
                            assemble=self.assemble, sb_dir=self.tree)

    # ---- note_from_context_composed: declared notes land in the page ----
    def test_activation_via_contract(self):
        r, page, manifest = self.run_decl(dict(SN_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_notes"', page)
        self.assertIn('data-smart-notes-status="built"', page)
        self.assertIn("Sourdough at 6am", page)
        self.assertIn("The crumb sings.", page)
        self.assertIn("Rye note", page)
        self.assertIn("grandma voice", page)
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["smart_notes"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        created = [e for e in events if e.get("event") == "smart_note.created"]
        minted = [e for e in events if e.get("event") == "smart_link.minted"]
        self.assertEqual(len(created), 2)
        self.assertEqual(len(minted), 2)
        for e in minted:
            self.assertTrue(e["link"].startswith("https://nayanet.live/sn/"))
            self.assertEqual(e["link_state"], "minted-unresolved")
            self.assertIn(e["link"], page)

    # ---- link_minted_deterministic: same inputs -> same note id + link ----
    def test_link_mint_deterministic(self):
        sys.path.insert(0, os.path.join(self.tree, "functions"))
        try:
            from feature_smart_notes import mint_note_id, mint_link
        finally:
            sys.path.pop(0)
        a = mint_note_id("nayanet.live/x", 0, "T", "B")
        b = mint_note_id("nayanet.live/x", 0, "T", "B")
        self.assertEqual(a, b)
        self.assertEqual(len(a), 12)
        self.assertNotEqual(a, mint_note_id("nayanet.live/x", 1, "T", "B"))
        self.assertEqual(mint_link("https://nayanet.live", a),
                         "https://nayanet.live/sn/" + a)

    # ---- gate: the page refuses to render notes it was not given ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp,
                                  assemble=self.assemble, sb_dir=self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_notes"', page)

    def test_refusal_when_declared_but_disabled(self):
        decl = dict(SN_DECL, enabled=False)
        r, page, manifest = self.run_decl(decl)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_notes"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "smart_note.created"
                             for e in events))

    # ---- unsafe_content_sanitized: hostile declarations are refusals ----
    def test_bad_voice_refused(self):
        decl = {"enabled": True, "notes": [
            {"title": "T", "body": "B", "voice": "robot"}]}
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_note_voice", codes)
        self.assertNotIn('data-feature="smart_notes"', page)

    def test_empty_body_refused(self):
        decl = {"enabled": True, "notes": [{"title": "T", "body": "   "}]}
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_note", codes)

    def test_unsafe_link_base_refused(self):
        for base in ("javascript:alert(1)", "ftp://example.com/x",
                     "//evil.example/x", "data:text/html,x"):
            decl = dict(SN_DECL, link_base=base)
            r, page, _ = self.run_decl(decl)
            self.assertEqual(r.returncode, 2, "base accepted: %r" % base)
            codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
            self.assertIn("unsafe_link_base", codes, base)
            self.assertNotIn('data-feature="smart_notes"', page)

    def test_html_injection_escaped(self):
        decl = {"enabled": True, "notes": [
            {"title": "<script>alert(1)</script>", "body": "B & <b>bold</b>"}]}
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertIn("B &amp; &lt;b&gt;bold&lt;/b&gt;", page)

    def test_malformed_declaration_refused(self):
        r, page, _ = self.run_decl("yes please")
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_smart_notes_declaration", codes)

    # ---- capture_panel_fallback: enabled with no notes -> panel, no cards ----
    def test_capture_panel_fallback(self):
        r, page, manifest = self.run_decl(True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_notes"', page)
        self.assertIn('id="sn-capture"', page)
        self.assertIn('id="sn-text"', page)
        self.assertIn('id="sn-save"', page)
        self.assertNotIn('class="sn-note"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "smart_note.created"
                             for e in events))

    # ---- DAY-ONE TEST (Shawn 21:34Z): minimal contract -> useful render, zero errors ----
    def test_day_one_minimal_contract(self):
        r, page, manifest = self.run_decl(True)  # the smallest possible declaration
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("refused", r.stdout)
        self.assertNotIn("Traceback", r.stderr)
        self.assertIn('data-feature="smart_notes"', page)
        self.assertIn("Smart Notes", page)  # useful: heading + capture form
        self.assertIn('id="sn-capture"', page)
        self.assertIn('id="sn-save"', page)

    # ---- link_not_claimed_live: minted links never claim to resolve ----
    def test_link_not_claimed_live(self):
        r, page, _ = self.run_decl(dict(SN_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-link-state="minted-unresolved"', page)
        self.assertIn("not connected", page)
        self.assertIn("connect the NayaNET bridge to enable link resolution", page)
        # no anchor pretends the link is live: links render as copyable chips
        self.assertNotIn('href="https://nayanet.live/sn/', page)

    # ---- every interactive control binds to DOM that exists (L-2026-10-17-004)
    def test_controls_bind_to_existing_dom(self):
        r, page, _ = self.run_decl(dict(SN_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        p = IdCollector()
        p.feed(page)
        self.assertTrue(p.copy_targets, "no copy buttons rendered")
        for t in p.copy_targets:
            self.assertIn(t, p.ids, "copy target missing from DOM: %r" % t)
        for need in ("sn-capture", "sn-text", "sn-voice", "sn-save", "sn-result"):
            self.assertIn(need, p.ids, "capture control missing: %s" % need)

    # ---- the general gate: specified (not built) refuses, fail closed ----
    def test_specified_registry_refuses(self):
        # the gate proof lives forever: a registry copy with this module
        # forced back to 'specified' must refuse the contract, fail closed.
        import copy as _copy
        tree = os.path.join(self.tmp, "sbspec")
        shutil.copytree(SB_DIR, tree)
        regp = os.path.join(tree, "functions", "registry.json")
        reg = json.load(open(regp))
        for g in reg["groups"].values():
            for fn in g.get("functions", []):
                if fn.get("id") == "feature.smart_notes":
                    fn["status"] = "specified"
        json.dump(reg, open(regp, "w"), indent=2)
        r, page, _ = run_assemble(sn_contract(self.tmp, dict(SN_DECL)), self.tmp,
                                  assemble=os.path.join(tree, "assemble.py"),
                                  sb_dir=tree)
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        mod_errs = [e for e in errs if e.get("feature") == "feature.smart_notes"]
        self.assertTrue(mod_errs, errs)
        self.assertEqual(mod_errs[0]["code"], "feature_not_built")
        self.assertNotIn('data-feature="smart_notes"', page)

    # ---- READY vs CONNECTED (Naya 3, 21:41Z): the missing grant is named ----
    def test_ready_connected_split_names_grant(self):
        r, page, manifest = self.run_decl(dict(SN_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        # ready-not-connected: the page says what to connect, never silent
        self.assertIn('data-grant-needed="bridge.smart_links.resolve"', page)
        events = manifest.get("receipt", {}).get("events", [])
        minted = [e for e in events if e.get("event") == "smart_link.minted"]
        self.assertTrue(minted)
        for e in minted:
            self.assertEqual(e["grant_needed"], "bridge.smart_links.resolve")
            self.assertEqual(e["connection"], "NayaNET bridge")
        # the capability contract itself carries the split
        reg = json.load(open(os.path.join(self.tree, "functions", "registry.json")))
        entry = [f for g in reg["groups"].values() for f in g.get("functions", [])
                 if f.get("id") == "feature.smart_notes"][0]
        self.assertTrue(entry["ready"])
        self.assertEqual(entry["connected"]["grant"], "bridge.smart_links.resolve")

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = sn_contract(self.tmp, dict(SN_DECL))
        _, page1, _ = run_assemble(contract, self.tmp,
                                    assemble=self.assemble, sb_dir=self.tree)
        d2 = tempfile.mkdtemp(prefix="fsn-b-")
        try:
            _, page2, _ = run_assemble(contract, d2,
                                        assemble=self.assemble, sb_dir=self.tree)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())


if __name__ == "__main__":
    unittest.main(verbosity=2)

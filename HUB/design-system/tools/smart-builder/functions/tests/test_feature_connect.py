#!/usr/bin/env python3
"""Acceptance tests for feature.connect (registry acceptance:
no_contact_without_consent, request_flow_tested, decline_respected).

Stdlib only (unittest + subprocess). Each test runs the real
assemble.py end-to-end against the real builder index:

  day-one                 -> minimal contract -> useful render, ZERO errors
  three-state             -> explicit true: on; explicit false: off (no render,
                             no claim, no error — even unbuilt); omitted:
                             assembler policy (connect: default-on)
  no_contact_without_consent -> channels without consent -> refusal (exit 2)
  request_flow_tested     -> form renders only wired + dial/grants allow;
                             posts to exactly the declared endpoint
  decline_respected       -> explicit false flips nothing on
  privacy dial            -> all three dials: channels always (consent-gated);
                             form private: suppressed, network: nayanet grant,
                             public: network grant
  consent line            -> ready with zero grants (channels work, requests
                             viewable by owner); connected-without-grant ->
                             missing_grant refusal naming the grant; with
                             grant -> connected, mirrored in receipt
  sanitization            -> hostile contact hrefs -> structured refusal
  registry binding        -> contract cannot activate what the registry does
                             not mark 'built' (fail closed)
  determinism             -> same contract -> same bytes
  href audit (L-2026-10-17-002) -> every rendered href is a working path

Build-time honesty: the registry's connect events (connect.requested /
.accepted / .declined) are visitor-lifecycle events — the build must NOT
fire them. The manifest receipt carries none.
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

MODULE_ID = "feature.connect"

CONNECT_DECL = {
    "enabled": True,
    "owner_name": "Morning Crumb",
    "consent": True,
    "channels": [
        {"kind": "email", "label": "Write to us",
         "href": "mailto:hello@morning-crumb.example"},
        {"kind": "phone", "label": "Call the bakery",
         "href": "tel:+15550123456"},
        {"kind": "link", "label": "Instagram",
         "href": "https://instagram.com/morningcrumb"},
    ],
    "form_action": "https://forms.morning-crumb.example/connect",
    "note": "We reply within a day.",
}


def customer_contract(tmp, features, top_extra=None):
    c = json.load(open(SMOKE))
    c["title"] = "Connect acceptance contract"
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


class FeatureConnectAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fconnect-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def built_assemble(self, status="built"):
        return sb_copy_with_status(self.tmp, MODULE_ID, status)

    def run_built(self, decl, top_extra=None, status="built"):
        contract = customer_contract(self.tmp, {"connect": decl}, top_extra)
        return run_assemble(contract, self.tmp,
                            assemble=self.built_assemble(status))

    def connect_block(self, page):
        return page.split('data-feature="connect"')[1].split("</section>")[0]

    # ---- DAY-ONE: minimal contract -> useful render, ZERO errors ----
    def test_day_one_minimal_contract(self):
        # bare true: no channels, no consent, no form -> the honest idle
        # shell. Nothing to gate, nothing staged, zero errors.
        r, page, manifest = self.run_built(True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("refused", r.stdout)
        self.assertIn('data-feature="connect"', page)
        self.assertIn('data-connect-status="built"', page)
        self.assertIn('data-mode="idle"', page)
        block = self.connect_block(page)
        self.assertNotIn("<form", block)
        self.assertNotIn("<a ", block)  # no contact paths without consent
        readiness = manifest["receipt"]["readiness"]
        info = [r for r in readiness if r["feature"] == MODULE_ID][0]
        self.assertEqual(info["mode"], "idle")
        self.assertEqual(info["consent"], "ready")

    # ---- three-state: explicit true -> on ----
    def test_explicit_true_full_private(self):
        # default dial is private: channels render (consent-gated, READY);
        # the inbound form is suppressed at private.
        r, page, manifest = self.run_built(dict(CONNECT_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="connect"', page)
        self.assertIn('data-connect-status="built"', page)
        self.assertIn('data-privacy="private"', page)
        self.assertIn('data-mode="ready"', page)
        self.assertIn("Connect with Morning Crumb", page)
        self.assertIn("mailto:hello@morning-crumb.example", page)
        self.assertIn("tel:+15550123456", page)
        self.assertIn("https://instagram.com/morningcrumb", page)
        block = self.connect_block(page)
        self.assertNotIn("<form", block)  # private: inbound suppressed
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["connect"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        for e in events:
            self.assertNotEqual(e.get("feature"), MODULE_ID,
                                "build fired a lifecycle event: %r" % e)
        readiness = manifest["receipt"]["readiness"]
        info = [r for r in readiness if r["feature"] == MODULE_ID][0]
        self.assertEqual(info["consent"], "ready")
        self.assertEqual(manifest["receipt"]["privacy"], "private")

    # ---- three-state: explicit false -> off (no render, no claim, no error) ----
    def test_explicit_false_suppression(self):
        for decl in (False, {"enabled": False},
                     {"enabled": False, "channels": [
                         {"kind": "email", "label": "E",
                          "href": "javascript:alert(1)"}]}):
            r, page, manifest = self.run_built(decl)
            self.assertEqual(r.returncode, 0, "decl %r: %s" % (decl, r.stdout))
            self.assertNotIn('data-feature="connect"', page)
            self.assertNotIn("mailto:", page)

    def test_explicit_false_ignores_registry(self):
        r, page, _ = self.run_built(False, status="specified")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="connect"', page)

    # ---- three-state: omitted -> assembler policy (connect: default-on) ----
    def test_omitted_policy_on_renders_idle(self):
        # Coverage gate ACTIVE (all 7 standard features built) -> omitted
        # = ON. Connect renders the honest idle shell (no contact paths
        # without consent).
        contract = customer_contract(self.tmp, {})
        r, page, manifest = run_assemble(contract, self.tmp,
                                         assemble=self.built_assemble())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="connect"', page)
        self.assertIn('data-mode="idle"', page)
    def test_omitted_policy_best_effort_when_unbuilt(self):
        # Policy defaults never fail a build the contract didn't claim:
        # omitted + registry 'specified' -> silently skipped, zero errors.
        contract = customer_contract(self.tmp, {})
        r, page, _ = run_assemble(contract, self.tmp,
                                  assemble=self.built_assemble("specified"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="connect"', page)

    # ---- no_contact_without_consent ----
    def test_refusal_without_consent(self):
        for decl in (dict(CONNECT_DECL, consent=False),
                     {k: v for k, v in CONNECT_DECL.items() if k != "consent"}):
            r, page, _ = self.run_built(decl)
            self.assertEqual(r.returncode, 2)
            codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
            self.assertIn("no_consent", codes)
            self.assertNotIn('data-feature="connect"', page)
            self.assertNotIn("mailto:", page)  # no contact path leaks through

    # ---- consent line: ready with zero grants ----
    def test_ready_with_zero_grants(self):
        decl = {k: v for k, v in CONNECT_DECL.items() if k != "form_action"}
        r, page, manifest = self.run_built(decl)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-mode="ready"', page)
        readiness = manifest["receipt"]["readiness"]
        info = [r for r in readiness if r["feature"] == MODULE_ID][0]
        self.assertEqual(info["consent"], "ready")
        self.assertFalse(any(manifest["receipt"]["grants"].values()))

    # ---- privacy dial x consent: the request form ----
    def test_form_network_dial_without_grant_refused(self):
        r, page, _ = self.run_built(
            dict(CONNECT_DECL),
            top_extra={"privacy": "network"})  # no grants
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        grant_errs = [e for e in errs if e.get("code") == "missing_grant"]
        self.assertTrue(grant_errs, errs)
        self.assertIn("nayanet", grant_errs[0]["detail"])
        self.assertIn("contract.connections.nayanet", grant_errs[0]["detail"])

    def test_form_network_dial_with_grant_connected(self):
        r, page, manifest = self.run_built(
            dict(CONNECT_DECL),
            top_extra={"privacy": "network",
                       "connections": {"nayanet": True}})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.connect_block(page)
        self.assertIn('action="https://forms.morning-crumb.example/connect"',
                      block)
        self.assertIn('data-mode="connected"', block)
        self.assertIn('data-grant="nayanet"', block)
        readiness = manifest["receipt"]["readiness"]
        info = [r for r in readiness if r["feature"] == MODULE_ID][0]
        self.assertEqual(info["mode"], "connected")
        self.assertEqual(info["consent"], "connected")
        self.assertTrue(manifest["receipt"]["grants"]["nayanet"])
        self.assertEqual(manifest["receipt"]["privacy"], "network")

    def test_form_public_dial_without_grant_refused(self):
        r, page, _ = self.run_built(
            dict(CONNECT_DECL),
            top_extra={"privacy": "public"})  # no grants
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        grant_errs = [e for e in errs if e.get("code") == "missing_grant"]
        self.assertTrue(grant_errs, errs)
        self.assertIn("contract.connections.network", grant_errs[0]["detail"])

    def test_form_public_dial_with_grant_connected(self):
        r, page, _ = self.run_built(
            dict(CONNECT_DECL),
            top_extra={"privacy": "public",
                       "connections": {"network": True}})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.connect_block(page)
        self.assertIn('data-mode="connected"', block)
        self.assertIn('data-grant="network"', block)

    def test_channels_only_no_form_needs_no_grant(self):
        # No form wired -> nothing connected claimed -> ready at every dial,
        # zero grants, zero errors.
        decl = {k: v for k, v in CONNECT_DECL.items() if k != "form_action"}
        for dial in ("private", "network", "public"):
            r, page, _ = self.run_built(decl, top_extra={"privacy": dial})
            self.assertEqual(r.returncode, 0, "%s: %s" % (dial, r.stdout))
            self.assertIn('data-mode="ready"', page)
            self.assertIn("mailto:hello@morning-crumb.example", page)

    # ---- request_flow_tested: the form exists only when wired ----
    def test_form_only_when_endpoint_wired(self):
        decl = {k: v for k, v in CONNECT_DECL.items() if k != "form_action"}
        r, page, _ = self.run_built(
            decl, top_extra={"privacy": "public",
                             "connections": {"network": True}})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.connect_block(page)
        self.assertNotIn("<form", block)  # no dead form
        self.assertIn("mailto:hello@morning-crumb.example", block)

    # ---- gate: nothing renders for the contract-page shape ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="connect"', page)
        self.assertNotIn('<section class="connect"', page)

    # ---- sanitization ----
    def test_contact_sanitization_refusals(self):
        bad_channels = [
            {"kind": "email", "label": "E", "href": "javascript:alert(1)"},
            {"kind": "email", "label": "E", "href": "mailto:not-an-address"},
            {"kind": "email", "label": "E", "href": "mailto:a@b"},
            {"kind": "phone", "label": "P", "href": "tel:javascript:alert(1)"},
            {"kind": "phone", "label": "P", "href": "https://example.com/call"},
            {"kind": "link", "label": "L", "href": "javascript:alert(1)"},
            {"kind": "link", "label": "L", "href": "//evil.example/"},
            {"kind": "link", "label": "L", "href": "relative/path"},
            {"kind": "chat", "label": "C", "href": "data:text/html,<b>"},
            {"kind": "chat", "label": "C", "href": "ftp://example.com/x"},
            {"kind": "smoke", "label": "S", "href": "https://example.com/"},
            {"kind": "email", "label": "", "href": "mailto:a@b.example"},
            {"kind": "email", "label": "E", "href": "mailto:a@b .example"},
        ]
        for ch in bad_channels:
            decl = dict(CONNECT_DECL, channels=[ch])
            r, page, _ = self.run_built(decl)
            self.assertEqual(r.returncode, 2, "channel accepted: %r" % ch)
            codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
            self.assertTrue({"unsafe_contact_url", "bad_channel"} & set(codes), ch)
            self.assertNotIn('data-feature="connect"', page)

    def test_hostile_form_action_refused(self):
        for action in ("http://forms.example.com/x", "javascript:alert(1)",
                       "//forms.example.com/x", ""):
            decl = dict(CONNECT_DECL, form_action=action)
            r, page, _ = self.run_built(decl)
            self.assertEqual(r.returncode, 2, "form_action accepted: %r" % action)
            codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
            self.assertIn("unsafe_contact_url", codes)

    # ---- malformed declaration: fail closed ----
    def test_malformed_declaration_refused(self):
        r, page, _ = self.run_built("yes please")
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_connect_declaration", codes)

    def test_bad_privacy_dial_refused(self):
        r, page, _ = self.run_built(True, top_extra={"privacy": "everyone"})
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_privacy", codes)

    # ---- the general gate: an unbuilt breaker fails the contract closed ----
    def test_unbuilt_breaker_refused(self):
        r, page, _ = self.run_built(dict(CONNECT_DECL), status="specified")
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        conn_errs = [e for e in errs if e.get("feature") == MODULE_ID]
        self.assertTrue(conn_errs, errs)
        self.assertEqual(conn_errs[0]["code"], "feature_not_built")
        self.assertNotIn('data-feature="connect"', page)

    # ---- determinism ----
    def test_determinism(self):
        contract = customer_contract(self.tmp, {"connect": dict(CONNECT_DECL)})
        asm = self.built_assemble()
        _, page1, _ = run_assemble(contract, self.tmp, assemble=asm)
        d2 = tempfile.mkdtemp(prefix="fconnect-b-")
        try:
            _, page2, _ = run_assemble(contract, d2, assemble=asm)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())

    # ---- L-2026-10-17-002: every rendered href is a working path ----
    def test_every_href_is_a_working_path(self):
        r, page, _ = self.run_built(dict(CONNECT_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.connect_block(page)
        hrefs = re.findall(r'href="([^"]+)"', block)
        self.assertTrue(hrefs)
        for href in hrefs:
            self.assertRegex(
                href,
                r"^(mailto:[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+"
                r"|tel:\+?[0-9().\- ]+"
                r"|https://\S+)$",
                "dead or unsafe contact path: %s" % href)
        actions = re.findall(r'<form[^>]*action="([^"]+)"', block)
        for a in actions:
            self.assertRegex(a, r"^https://\S+$",
                             "form posts somewhere unsafe: %s" % a)

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
            from feature_connect import render_connect
        finally:
            sys.path.pop(0)
        ctx_public = {"privacy": "public",
                      "connections": {"muse": False, "github": False,
                                      "network": True, "nayanet": False}}
        frags = [
            render_connect({"enabled": True}, "built")[0],
            render_connect(dict(CONNECT_DECL), "built", ctx_public)[0],
        ]
        for frag in frags:
            p = P()
            p.feed(frag)
            self.assertFalse(p.errors, p.errors)
            self.assertFalse(p.stack, p.stack)


if __name__ == "__main__":
    unittest.main(verbosity=2)

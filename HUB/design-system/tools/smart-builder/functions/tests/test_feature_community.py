#!/usr/bin/env python3
"""Acceptance tests for feature.community (registry acceptance:
comment_appears, abuse_path_exists, private_page_no_public_comments).

Stdlib only (unittest + subprocess). Each test runs the real
assemble.py end-to-end against the real builder index:

  day-one                 -> minimal contract -> useful render, ZERO errors
  three-state             -> explicit true: on; explicit false: off (no render,
                             no claim, no error — even unbuilt); omitted:
                             assembler policy (community: default-off)
  comment_appears         -> seed comments land in the page, escaped
  abuse_path_exists       -> report target required with a thread; missing ->
                             refusal
  private_page_no_public_comments -> private dial -> gated shell, always
  privacy dial x consent  -> network/public: grant -> connected; no grant +
                             no endpoint -> honest local state (never staged,
                             never a refusal); no grant + wired endpoint ->
                             missing_grant refusal naming the grant
  consent line            -> ready with zero grants; receipt mirrors
                             mode/consent/privacy/grants; copy never conflates
  sanitization            -> hostile URLs / XSS seeds -> refusal or escape
  registry binding        -> contract cannot activate what the registry does
                             not mark 'built' (fail closed)
  determinism             -> same contract -> same bytes
  href audit (L-2026-10-17-002) -> report + endpoint hrefs are real

Build-time honesty: the registry's community events
(community.comment.posted / .removed) are visitor-lifecycle events —
the build must NOT fire them. The manifest receipt carries none.
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

MODULE_ID = "feature.community"

COMMUNITY_DECL = {
    "enabled": True,
    "title": "The conversation",
    "service": "hub-community",
    "moderation": "owner-moderated",
    "seed_comments": [
        {"author": "Ana", "text": "First in line every morning.", "when": "today"},
        {"author": "Ben", "text": "The cardamom bun changed my life.", "when": "yesterday"},
    ],
    "comment_endpoint": "https://community.morning-crumb.example/post",
    "report_target": "mailto:moderation@morning-crumb.example",
}


def customer_contract(tmp, features, top_extra=None):
    c = json.load(open(SMOKE))
    c["title"] = "Community acceptance contract"
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


class FeatureCommunityAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fcommunity-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def built_assemble(self, status="built"):
        return sb_copy_with_status(self.tmp, MODULE_ID, status)

    def run_built(self, decl, top_extra=None, status="built"):
        contract = customer_contract(self.tmp, {"community": decl}, top_extra)
        return run_assemble(contract, self.tmp,
                            assemble=self.built_assemble(status))

    def community_block(self, page):
        return page.split('data-feature="community"')[1].split("</section>")[0]

    # ---- DAY-ONE: minimal contract -> useful render, ZERO errors ----
    def test_day_one_minimal_contract(self):
        # bare true, default dial (private) -> the gated shell: an honest,
        # useful render with zero errors and zero grants.
        r, page, manifest = self.run_built(True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("refused", r.stdout)
        self.assertIn('data-feature="community"', page)
        self.assertIn('data-community-status="built"', page)
        self.assertIn('data-mode="gated"', page)
        self.assertIn('data-privacy="private"', page)
        readiness = manifest["receipt"]["readiness"]
        info = [r for r in readiness if r["feature"] == MODULE_ID][0]
        self.assertEqual(info["mode"], "gated")
        self.assertEqual(info["consent"], "ready")

    # ---- three-state: explicit false -> off ----
    def test_explicit_false_suppression(self):
        for decl in (False, {"enabled": False}):
            r, page, _ = self.run_built(decl)
            self.assertEqual(r.returncode, 0, "decl %r: %s" % (decl, r.stdout))
            self.assertNotIn('data-feature="community"', page)

    def test_explicit_false_ignores_registry(self):
        r, page, _ = self.run_built(False, status="specified")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="community"', page)

    # ---- three-state: omitted -> assembler policy (community: default-off) ----
    def test_omitted_follows_policy(self):
        contract = customer_contract(self.tmp, {})
        r, page, _ = run_assemble(contract, self.tmp,
                                  assemble=self.built_assemble())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="community"', page)

    # ---- private_page_no_public_comments: the dial gates, always ----
    def test_private_dial_gated_all_three_ways(self):
        for decl in (dict(COMMUNITY_DECL), True,
                     {"enabled": True, "title": "T"}):
            r, page, _ = self.run_built(decl)  # default dial: private
            self.assertEqual(r.returncode, 0, "%r: %s" % (decl, r.stdout))
            self.assertIn('data-feature="community"', page)
            block = self.community_block(page)
            self.assertIn("community-gated", block)
            self.assertNotIn("First in line every morning.", block)
            self.assertNotIn("community-comment", block)
            self.assertNotIn("<form", block)

    # ---- comment_appears + connected (public dial, network grant) ----
    def test_public_dial_with_grant_connected(self):
        r, page, manifest = self.run_built(
            dict(COMMUNITY_DECL),
            top_extra={"privacy": "public",
                       "connections": {"network": True}})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="community"', page)
        self.assertIn('data-community-status="built"', page)
        self.assertIn('data-community-service="hub-community"', page)
        self.assertIn('data-mode="connected"', page)
        self.assertIn('data-grant="network"', page)
        self.assertIn('data-privacy="public"', page)
        block = self.community_block(page)
        self.assertIn("First in line every morning.", block)
        self.assertIn("The cardamom bun changed my life.", block)
        self.assertIn('action="https://community.morning-crumb.example/post"',
                      block)
        self.assertIn("mailto:moderation@morning-crumb.example", block)
        self.assertIn("owner-moderated", block)
        self.assertIn("Open to the world.", block)  # public, first-class
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["community"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        for e in events:
            self.assertNotEqual(e.get("feature"), MODULE_ID,
                                "build fired a lifecycle event: %r" % e)
        readiness = manifest["receipt"]["readiness"]
        info = [r for r in readiness if r["feature"] == MODULE_ID][0]
        self.assertEqual(info["mode"], "connected")
        self.assertEqual(info["consent"], "connected")
        self.assertTrue(manifest["receipt"]["grants"]["network"])
        self.assertEqual(manifest["receipt"]["privacy"], "public")

    # ---- dial x consent matrix: public dial + no grant -> honest local ----
    def test_public_dial_no_grant_stays_local(self):
        decl = {k: v for k, v in COMMUNITY_DECL.items()
                if k != "comment_endpoint"}  # nothing wired to publish
        r, page, manifest = self.run_built(
            decl, top_extra={"privacy": "public"})  # zero grants
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.community_block(page)
        self.assertIn('data-mode="local"', block)
        self.assertIn("First in line every morning.", block)  # local content shows
        self.assertNotIn("<form", block)  # no publish path: nothing staged
        self.assertIn("Not connected to the network", block)  # named, honest
        readiness = manifest["receipt"]["readiness"]
        info = [r for r in readiness if r["feature"] == MODULE_ID][0]
        self.assertEqual(info["mode"], "local")
        self.assertEqual(info["consent"], "ready")  # local is ready, not connected

    def test_network_dial_no_grant_stays_local(self):
        decl = {k: v for k, v in COMMUNITY_DECL.items()
                if k != "comment_endpoint"}
        r, page, _ = self.run_built(
            decl, top_extra={"privacy": "network"})  # zero grants
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.community_block(page)
        self.assertIn('data-mode="local"', block)
        self.assertIn("Not connected to NayaNET", block)

    # ---- connected-without-grant -> structured refusal naming the grant ----
    def test_endpoint_network_dial_without_grant_refused(self):
        r, page, _ = self.run_built(
            dict(COMMUNITY_DECL),
            top_extra={"privacy": "network"})  # endpoint wired, no grant
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        grant_errs = [e for e in errs if e.get("code") == "missing_grant"]
        self.assertTrue(grant_errs, errs)
        self.assertIn("nayanet", grant_errs[0]["detail"])
        self.assertIn("contract.connections.nayanet", grant_errs[0]["detail"])
        self.assertNotIn('data-feature="community"', page)

    def test_endpoint_public_dial_without_grant_refused(self):
        r, page, _ = self.run_built(
            dict(COMMUNITY_DECL),
            top_extra={"privacy": "public"})  # endpoint wired, no grant
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        grant_errs = [e for e in errs if e.get("code") == "missing_grant"]
        self.assertTrue(grant_errs, errs)
        self.assertIn("contract.connections.network", grant_errs[0]["detail"])

    def test_network_dial_with_grant_connected(self):
        r, page, manifest = self.run_built(
            dict(COMMUNITY_DECL),
            top_extra={"privacy": "network",
                       "connections": {"nayanet": True}})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.community_block(page)
        self.assertIn('data-mode="connected"', block)
        self.assertIn('data-grant="nayanet"', block)
        self.assertIn("Visible to your NayaNET network.", block)
        self.assertIn('action="https://community.morning-crumb.example/post"',
                      block)

    # ---- seed comments are plain text: XSS is escaped, never executed ----
    def test_seed_xss_escaped(self):
        decl = dict(COMMUNITY_DECL, seed_comments=[
            {"author": "<img src=x onerror=alert(1)>",
             "text": "<script>alert('xss')</script> nice buns",
             "when": "now"}])
        # drop the endpoint so no grant is needed; keep public dial
        del decl["comment_endpoint"]
        r, page, _ = self.run_built(
            decl, top_extra={"privacy": "public"})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.community_block(page)
        self.assertNotIn("<script>", block)
        self.assertNotIn("<img src=x", block)
        self.assertIn("&lt;script&gt;", block)
        self.assertIn("nice buns", block)

    # ---- abuse_path_exists ----
    def test_refusal_without_abuse_path(self):
        decl = {k: v for k, v in COMMUNITY_DECL.items()
                if k != "report_target"}
        del decl["comment_endpoint"]  # stay grant-free; thread still renders
        r, page, _ = self.run_built(
            decl, top_extra={"privacy": "public"})
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("no_abuse_path", codes)
        self.assertNotIn('data-feature="community"', page)

    # ---- service binding ----
    def test_refusal_without_service_binding(self):
        for drop in ("service", "moderation"):
            decl = {k: v for k, v in COMMUNITY_DECL.items() if k != drop}
            del decl["comment_endpoint"]
            r, page, _ = self.run_built(
                decl, top_extra={"privacy": "public"})
            self.assertEqual(r.returncode, 2, drop)
            codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
            self.assertIn("missing_service_binding", codes, drop)

    # ---- gate: nothing renders for the contract-page shape ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="community"', page)
        self.assertNotIn('<section class="community"', page)

    # ---- sanitization ----
    def test_url_sanitization_refusals(self):
        bad = [
            "javascript:alert(1)",
            "http://community.example.com/post",  # http, not https
            "//community.example.com/post",
            "ftp://community.example.com/post",
            "data:text/html,<b>",
            "java\tscript:alert(1)",
        ]
        for field in ("comment_endpoint", "report_target"):
            for url in bad:
                decl = dict(COMMUNITY_DECL, **{field: url})
                r, page, _ = self.run_built(
                    decl, top_extra={"privacy": "public",
                                     "connections": {"network": True}})
                self.assertEqual(r.returncode, 2,
                                 "%s accepted: %r" % (field, url))
                codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
                # validation runs before any grant/publish logic: hostile
                # input always fails closed as unsafe_community_url.
                self.assertIn("unsafe_community_url", codes, (field, url))
                self.assertNotIn('data-feature="community"', page)

    def test_https_report_target_allowed(self):
        decl = dict(COMMUNITY_DECL,
                    report_target="https://moderation.morning-crumb.example/report")
        del decl["comment_endpoint"]
        r, page, _ = self.run_built(
            decl, top_extra={"privacy": "public"})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("https://moderation.morning-crumb.example/report", page)

    # ---- malformed declaration: fail closed ----
    def test_malformed_declaration_refused(self):
        r, page, _ = self.run_built("yes please")
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_community_declaration", codes)

    def test_bad_privacy_dial_refused(self):
        r, page, _ = self.run_built(True, top_extra={"privacy": "everyone"})
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_privacy", codes)
        self.assertNotIn('data-feature="community"', page)

    # ---- the general gate: an unbuilt breaker fails the contract closed ----
    def test_unbuilt_breaker_refused(self):
        r, page, _ = self.run_built(dict(COMMUNITY_DECL), status="specified")
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        comm_errs = [e for e in errs if e.get("feature") == MODULE_ID]
        self.assertTrue(comm_errs, errs)
        self.assertEqual(comm_errs[0]["code"], "feature_not_built")
        self.assertNotIn('data-feature="community"', page)

    # ---- determinism ----
    def test_determinism(self):
        contract = customer_contract(self.tmp, {"community": dict(COMMUNITY_DECL)})
        asm = self.built_assemble()
        _, page1, _ = run_assemble(contract, self.tmp, assemble=asm)
        d2 = tempfile.mkdtemp(prefix="fcommunity-b-")
        try:
            _, page2, _ = run_assemble(contract, d2, assemble=asm)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())

    # ---- L-2026-10-17-002: every rendered href is a working path ----
    def test_every_href_is_a_working_path(self):
        r, page, _ = self.run_built(
            dict(COMMUNITY_DECL),
            top_extra={"privacy": "public",
                       "connections": {"network": True}})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        block = self.community_block(page)
        hrefs = re.findall(r'href="([^"]+)"', block)
        self.assertTrue(hrefs)
        for href in hrefs:
            self.assertRegex(
                href,
                r"^(mailto:[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+"
                r"|https://\S+)$",
                "dead or unsafe path: %s" % href)
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
            from feature_community import render_community
        finally:
            sys.path.pop(0)
        ctx_net = {"privacy": "network",
                   "connections": {"muse": False, "github": False,
                                   "network": False, "nayanet": True}}
        frags = [
            render_community({"enabled": True}, "built")[0],
            render_community(dict(COMMUNITY_DECL), "built", ctx_net)[0],
            render_community(
                {"enabled": True, "service": "s", "moderation": "m",
                 "seed_comments": [{"author": "A", "text": "hi"}],
                 "report_target": "mailto:m@e.example"},
                "built",
                {"privacy": "public",
                 "connections": {"muse": False, "github": False,
                                 "network": False, "nayanet": False}})[0],
        ]
        for frag in frags:
            p = P()
            p.feed(frag)
            self.assertFalse(p.errors, p.errors)
            self.assertFalse(p.stack, p.stack)


if __name__ == "__main__":
    unittest.main(verbosity=2)

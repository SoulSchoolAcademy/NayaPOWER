#!/usr/bin/env python3
"""Acceptance tests for feature.social_feed (registry acceptance:
post_appears_for_audience, private_post_not_leaked, failure_state_visible).

Stdlib only (unittest + subprocess). Each test runs the real
assemble.py end-to-end against the real builder index:

  activation gate       -> no feed markup unless the contract declares it
  activation            -> declared + built -> feed section with the
                           audience-visible posts
  privacy               -> non-public posts/audiences never leak onto the page
  sanitization          -> hostile post URLs -> structured refusal (exit 2)
  registry binding      -> contract cannot activate what the registry does
                           not mark 'built' (fail closed)
  determinism           -> same contract -> same bytes
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

FEED_DECL = {
    "enabled": True,
    "title": "Fresh from the oven",
    "audience": "public",
    "posts": [
        {"text": "Warm sourdough at 7am.",
         "url": "https://morning-crumb.example/posts/sourdough",
         "time": "2026-10-17",
         "audience": "public"},
        {"text": "New: cardamom buns.",
         "audience": "public"},
    ],
}


def feed_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    c = json.load(open(SMOKE))
    c["title"] = "Social feed acceptance contract"
    c["features"] = {"social_feed": decl}
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


def feed_section(page):
    m = re.search(r'<section class="breaker breaker-feed".*?</section>',
                  page, re.S)
    return m.group(0) if m else ""


class FeatureSocialFeedAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ffeed-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- activation: declared + built -> audience-visible posts render ----
    def test_activation_via_contract(self):
        decl = json.loads(json.dumps(FEED_DECL))  # deep copy
        r, page, manifest = run_assemble(feed_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="social_feed"', page)
        self.assertIn('data-social_feed-status="built"', page)
        sec = feed_section(page)
        self.assertTrue(sec, "feed section missing")
        self.assertIn("Fresh from the oven", sec)
        self.assertIn("Warm sourdough at 7am.", sec)
        self.assertIn("New: cardamom buns.", sec)
        self.assertIn('href="https://morning-crumb.example/posts/sourdough"',
                      sec)
        self.assertIn("2026-10-17", sec)
        self.assertEqual(sec.count("<article"), 2)
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["social_feed"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "social_feed.wired"
                            and e.get("feature") == "feature.social_feed"
                            for e in events), events)

    def test_bare_true_falls_back_private(self):
        r, page, _ = run_assemble(feed_contract(self.tmp, True), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = feed_section(page)
        # fail-closed default audience: honest members-only state, zero posts
        self.assertIn("This feed is private", sec)
        self.assertNotIn("<article", sec)

    # ---- gate: the page refuses to render a feed it was not given ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="social_feed"', page)
        self.assertNotIn("breaker-feed", page)

    def test_refusal_when_declared_but_disabled(self):
        decl = json.loads(json.dumps(FEED_DECL))
        decl["enabled"] = False
        r, page, manifest = run_assemble(feed_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="social_feed"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "social_feed.wired"
                             for e in events))

    # ---- three-state: explicit false suppresses silently (no render, no claim) ----
    def test_explicit_false_suppresses(self):
        r, page, manifest = run_assemble(
            feed_contract(self.tmp, False), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="social_feed"', page)
        self.assertNotIn("breaker-feed", page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "social_feed.wired"
                             for e in events))
        # suppression is silent: no structured error, exit 0 (not a refusal)
        self.assertNotIn('"status": "refused"', r.stdout)

    def test_omitted_flag_defaults_on_under_active_gate(self):
        # Coverage gate ACTIVE (all 7 standard features built) -> omitted
        # = ON (default-on live). The module renders with its fallbacks.
        c = json.load(open(SMOKE))
        c["features"] = {}
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="social_feed"', page)
    def test_private_post_not_leaked(self):
        decl = json.loads(json.dumps(FEED_DECL))
        decl["posts"].append({"text": "SECRET FAMILY RECIPE DO NOT SHARE",
                              "audience": "private"})
        decl["posts"].append({"text": "Members presale link",
                              "audience": "members"})
        r, page, _ = run_assemble(feed_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = feed_section(page)
        self.assertIn("Warm sourdough at 7am.", sec)
        self.assertNotIn("SECRET FAMILY RECIPE", page)
        self.assertNotIn("Members presale link", page)
        self.assertEqual(sec.count("<article"), 2)

    def test_nonpublic_audience_renders_no_posts(self):
        decl = json.loads(json.dumps(FEED_DECL))
        decl["audience"] = "members"
        r, page, _ = run_assemble(feed_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = feed_section(page)
        self.assertIn("This feed is members", sec)
        self.assertNotIn("<article", sec)
        self.assertNotIn("Warm sourdough", sec)

    def test_default_audience_is_private(self):
        decl = {"enabled": True, "title": "T",
                "posts": [{"text": "leak?", "audience": "public"}]}
        r, page, _ = run_assemble(feed_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("leak?", feed_section(page))

    # ---- privacy dial: fills omitted audience; unlabeled posts inherit it ----
    def test_privacy_dial_public_by_legitimate_choice(self):
        c = json.load(open(SMOKE))
        c["features"] = {"social_feed": {
            "enabled": True, "title": "Fresh",
            # audience omitted -> dial decides; post audience omitted too
            "posts": [{"text": "Hello, world"}]}}
        c["privacy"] = "public"
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = feed_section(page)
        # public is legitimate: the unlabeled post renders, no warnings
        self.assertIn("Hello, world", sec)
        self.assertIn("<article", sec)
        self.assertNotIn("violation", page.lower())

    def test_privacy_dial_network_maps_members(self):
        c = json.load(open(SMOKE))
        c["features"] = {"social_feed": {"enabled": True, "title": "Fresh",
                                         "posts": []}}
        c["privacy"] = "network"
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("This feed is members", feed_section(page))

    def test_explicit_audience_beats_dial(self):
        c = json.load(open(SMOKE))
        c["features"] = {"social_feed": {
            "enabled": True, "title": "Fresh", "audience": "private",
            "posts": [{"text": "stay hidden"}]}}
        c["privacy"] = "public"  # dial says public; explicit private wins
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = feed_section(page)
        self.assertIn("This feed is private", sec)
        self.assertNotIn("stay hidden", sec)

    def test_bad_privacy_dial_refused(self):
        c = json.load(open(SMOKE))
        c["features"] = {"social_feed": json.loads(json.dumps(FEED_DECL))}
        c["privacy"] = "everyone"
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_privacy_dial", codes)

    # ---- consent line: READY vs CONNECTED ----
    # snapshot posts are READY (zero grants); live updates are CONNECTED.
    def test_live_without_grant_refused(self):
        decl = json.loads(json.dumps(FEED_DECL))
        decl["live"] = True
        r, page, _ = run_assemble(feed_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 2)
        body = json.loads(r.stdout)
        self.assertEqual(body["status"], "refused")
        errs = [e for e in body["errors"] if e["code"] == "grant_required"]
        self.assertTrue(errs, body["errors"])
        self.assertIn("connections.network", errs[0]["detail"])
        self.assertIn("ready but not connected", errs[0]["detail"])
        self.assertNotIn('data-feature="social_feed"', page)

    def test_live_with_grant_and_url(self):
        c = json.load(open(SMOKE))
        c["features"] = {"social_feed": dict(
            json.loads(json.dumps(FEED_DECL)), live=True,
            feed_url="https://hub.nayanet.live/feed/morning-crumb")}
        c["connections"] = {"network": True}
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, manifest = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = feed_section(page)
        # snapshot still renders (ready) + the real live link (connected)
        self.assertIn("Warm sourdough at 7am.", sec)
        self.assertIn('href="https://hub.nayanet.live/feed/morning-crumb"',
                      sec)
        self.assertIn("Connected via the network", sec)
        events = manifest.get("receipt", {}).get("events", [])
        grant_events = [e for e in events
                        if e.get("event") == "social_feed.live.connected"]
        self.assertTrue(grant_events, events)
        self.assertEqual(grant_events[0]["grant"], "connections.network")

    def test_live_with_grant_no_url(self):
        c = json.load(open(SMOKE))
        decl = json.loads(json.dumps(FEED_DECL))
        decl["live"] = True
        c["features"] = {"social_feed": decl}
        c["connections"] = {"network": True}
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = feed_section(page)
        self.assertIn("no live feed URL is configured", sec)
        self.assertNotIn("View the live", sec)

    def test_unsafe_feed_url_refused(self):
        decl = json.loads(json.dumps(FEED_DECL))
        decl["live"] = True
        decl["feed_url"] = "javascript:alert(1)"
        c = json.load(open(SMOKE))
        c["features"] = {"social_feed": decl}
        c["connections"] = {"network": True}
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("unsafe_feed_url", codes)

    def test_ready_copy_never_says_connected(self):
        # The ready snapshot (no live requested) never claims "connected".
        decl = json.loads(json.dumps(FEED_DECL))
        r, page, _ = run_assemble(feed_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = feed_section(page)
        self.assertTrue(sec)
        self.assertNotIn("connected", sec.lower())

    # ---- empty feed -> honest empty state, never an empty pretense ----
    def test_empty_posts_honest_state(self):
        decl = {"enabled": True, "title": "Fresh", "audience": "public",
                "posts": []}
        r, page, _ = run_assemble(feed_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = feed_section(page)
        self.assertIn("Nothing posted yet", sec)
        self.assertNotIn("<article", sec)

    # ---- sanitization: hostile post URLs are structured refusals ----
    def test_unsafe_post_url_refused(self):
        bad = [
            "javascript:alert(1)",
            "data:text/html,<h1>x</h1>",
            "//evil.example/post",
            "posts/relative",
            "ftp://example.com/x",
        ]
        for url in bad:
            decl = json.loads(json.dumps(FEED_DECL))
            decl["posts"] = [{"text": "x", "url": url, "audience": "public"}]
            r, page, _ = run_assemble(feed_contract(self.tmp, decl), self.tmp)
            self.assertEqual(r.returncode, 2, "url accepted: %r" % url)
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            codes = [e["code"] for e in body["errors"]]
            self.assertIn("unsafe_post_url", codes, url)
            self.assertNotIn('data-feature="social_feed"', page)

    def test_post_text_too_long_refused(self):
        decl = json.loads(json.dumps(FEED_DECL))
        decl["posts"] = [{"text": "x" * 2001, "audience": "public"}]
        r, page, _ = run_assemble(feed_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("post_text_too_long", codes)

    def test_bad_audience_refused(self):
        decl = json.loads(json.dumps(FEED_DECL))
        decl["audience"] = "everyone"
        r, page, _ = run_assemble(feed_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_feed_audience", codes)

    def test_markup_in_post_is_escaped(self):
        decl = json.loads(json.dumps(FEED_DECL))
        decl["posts"] = [{"text": "<script>alert(1)</script>",
                          "audience": "public"}]
        r, page, _ = run_assemble(feed_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("<script>alert(1)</script>", feed_section(page))
        self.assertIn("&lt;script&gt;", feed_section(page))

    # ---- malformed declaration: fail closed, not improvised ----
    def test_malformed_declaration_refused(self):
        r, page, _ = run_assemble(
            feed_contract(self.tmp, "yes please"), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_social_feed_declaration", codes)

    # ---- registry binding: the contract cannot out-claim the registry ----
    def test_registry_binding_refusal(self):
        tree = os.path.join(self.tmp, "sbcopy")
        shutil.copytree(SB_DIR, tree)
        regp = os.path.join(tree, "functions", "registry.json")
        reg = json.load(open(regp))
        for g in reg["groups"].values():
            for f in g.get("functions", []):
                if f.get("id") == "feature.social_feed":
                    f["status"] = "specified"
        json.dump(reg, open(regp, "w"), indent=1)
        decl = json.loads(json.dumps(FEED_DECL))
        r, page, _ = run_assemble(
            feed_contract(self.tmp, decl), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)
        self.assertNotIn('data-feature="social_feed"', page)

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        decl = json.loads(json.dumps(FEED_DECL))
        contract = feed_contract(self.tmp, decl)
        _, page1, _ = run_assemble(contract, self.tmp)
        d2 = tempfile.mkdtemp(prefix="ffeed-b-")
        try:
            _, page2, _ = run_assemble(contract, d2)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        h1 = hashlib.sha256(page1.encode()).hexdigest()
        h2 = hashlib.sha256(page2.encode()).hexdigest()
        self.assertEqual(h1, h2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

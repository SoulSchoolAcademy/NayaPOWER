#!/usr/bin/env python3
"""Acceptance tests for feature.social_feed (registry acceptance:
post_appears_for_audience, private_post_not_leaked, failure_state_visible).

Stdlib only (unittest + subprocess). Three levels, like the space suite:

  module level  -> decl_for / can_publish / render_social_feed on live bytes
  resolver level-> resolve() against the real registry (gates + binding)
  end-to-end    -> the real assemble.py against the real builder index

  post_appears_for_audience -> declared posts render with their titles
                               and bodies, by visibility
  private_post_not_leaked   -> a private post renders NO publish
                               affordance — publishing is absent for it,
                               never gated, even with every grant
  failure_state_visible     -> a failed post renders the honest failure
                               line; nothing is swallowed silently
  activation gate           -> no feed markup unless the contract declares it
  sanitization              -> hostile posts / bad declarations ->
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
from feature_social_feed import (FeedRefusal, can_publish, decl_for,
                                 render_social_feed, sanitize_post)
from resolver import ResolverRefusal, resolve

FEED_DECL = {
    "enabled": True,
    "posts": [
        {"title": "Launch day", "body": "We opened the doors.",
         "visibility": "network"},
        {"title": "Quiet note", "body": "For my eyes only.",
         "visibility": "private"},
        {"title": "Draft thought", "body": "Still thinking.",
         "visibility": "network", "draft": True},
    ],
}


def full_context(**over):
    """All publish gates green: permissions, nayanet grant, requirements."""
    c = {"contract": {"features": {"social_feed": dict(FEED_DECL)}},
         "connections": {"nayanet": True},
         "privacy": "private",
         "granted_permissions": ["feed.publish"],
         "available": ["authenticated_identity", "feed_service",
                       "audience_rules"]}
    c.update(over)
    return c


def feed_contract(tmp, decl, connections=None):
    """A customer contract: smoke contract with features as a breaker dict."""
    with open(SMOKE) as fh:
        c = json.load(fh)
    c["title"] = "Social feed acceptance contract"
    c["features"] = {"social_feed": decl}
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


class SocialFeedModule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ffeed-")

    # ---- activation gate: nothing declared -> nothing rendered ----
    def test_not_declared_renders_nothing(self):
        for decl in (None, {}, {"enabled": False}):
            html = render_social_feed(decl, "built", context=full_context())
            self.assertEqual(html, "", decl)
        # features carried as a list (contract-page) -> not declared
        self.assertIsNone(decl_for({"features": [["a", "b"]]}))

    # ---- registry binding: fail closed unless the registry says built ----
    def test_not_built_refuses(self):
        with self.assertRaises(FeedRefusal) as cm:
            render_social_feed(dict(FEED_DECL), "specified",
                               context=full_context())
        self.assertEqual(cm.exception.code, "feature_not_built")

    # ---- decl_for shapes ----
    def test_decl_for_shapes(self):
        self.assertEqual(decl_for({"features": {"social_feed": True}}),
                         {"enabled": True})
        d = {"enabled": True, "posts": []}
        self.assertEqual(decl_for({"features": {"social_feed": d}}), d)
        self.assertIsNone(decl_for({"features": {"social_feed": False}}))
        self.assertIsNone(decl_for({"features": {}}))
        self.assertIsNone(decl_for({}))
        with self.assertRaises(FeedRefusal) as cm:
            decl_for({"features": {"social_feed": "yes please"}})
        self.assertEqual(cm.exception.code, "bad_social_feed_declaration")

    # ---- private posts stay private: absent, never gated ----
    def test_private_post_renders_no_publish_affordance_even_granted(self):
        decl = {"enabled": True, "posts": [
            {"title": "Secret", "body": "Eyes only.", "visibility": "private"}]}
        html = render_social_feed(decl, "built", context=full_context())
        self.assertIn('data-feature="social_feed"', html)
        self.assertIn("Secret", html)
        self.assertIn("Eyes only.", html)
        self.assertNotIn('class="feed-publish-btn"', html)
        self.assertNotIn('data-consent="connected"', html)
        self.assertIn("Private — only you see this", html)
        self.assertIn('data-consent="ready"', html)

    # ---- publish is the connected action: live only when authorized ----
    def test_publish_live_when_granted(self):
        decl = {"enabled": True, "posts": [
            {"title": "Hello network", "body": "Out loud.",
             "visibility": "network"}]}
        html = render_social_feed(decl, "built", context=full_context())
        self.assertIn('class="feed-publish-btn"', html)
        self.assertIn('data-consent="connected"', html)
        self.assertIn('data-publish-grant="nayanet"', html)
        self.assertIn("Publish to network", html)
        # receipt hooks carry the registry's own events
        self.assertIn('data-receipt-events=', html)
        self.assertIn("feed.post.published", html)
        self.assertIn("feed.post.failed", html)

    def test_gated_block_when_permission_missing(self):
        decl = {"enabled": True, "posts": [
            {"title": "Hello network", "body": "Out loud.",
             "visibility": "network"}]}
        ctx = full_context(granted_permissions=[])
        allowed, missing = can_publish(ctx)
        self.assertFalse(allowed)
        self.assertTrue(missing)
        html = render_social_feed(decl, "built", context=ctx)
        self.assertIn('data-consent="ready"', html)
        self.assertIn("Publishing is ready but off.", html)
        self.assertIn("your permission to publish posts", html)
        self.assertNotIn('class="feed-publish-btn"', html)

    def test_gated_block_when_nayanet_not_strictly_true(self):
        decl = {"enabled": True, "posts": [
            {"title": "Hello network", "body": "Out loud.",
             "visibility": "network"}]}
        for conn in ({"nayanet": False}, {"nayanet": "yes"}):  # truthy != True
            ctx = full_context(connections=conn)
            allowed, missing = can_publish(ctx)
            self.assertFalse(allowed, conn)
            html = render_social_feed(decl, "built", context=ctx)
            self.assertIn('data-consent="ready"', html, conn)
            self.assertIn("the NayaNET connection switched on for this page",
                          html, conn)
            self.assertNotIn('class="feed-publish-btn"', html, conn)

    # ---- acceptance: posts appear for their audience ----
    def test_posts_render_declared_content(self):
        html = render_social_feed(dict(FEED_DECL), "built",
                                  context=full_context())
        for title, body in (("Launch day", "We opened the doors."),
                            ("Quiet note", "For my eyes only."),
                            ("Draft thought", "Still thinking.")):
            self.assertIn(title, html)
            self.assertIn(body, html)
        self.assertIn('feed-visibility-network', html)
        self.assertIn('feed-visibility-private', html)

    # ---- acceptance: malformed posts are refused, never dropped ----
    def test_bad_posts_refused(self):
        bad = [
            {"body": "no title"},                       # missing title
            {"title": "   ", "body": "blank title"},    # blank title
            {"title": "no body"},                       # missing body
            {"title": "t", "body": "b", "visibility": "galactic"},
            {"title": "t", "body": "b", "draft": "maybe"},
            "just a string",
            42,
        ]
        for post in bad:
            with self.assertRaises(FeedRefusal, msg=repr(post)) as cm:
                sanitize_post(post)
            self.assertEqual(cm.exception.code, "bad_social_feed_post")

    # ---- sanitization: hostile content escaped ----
    def test_render_escapes_xss(self):
        decl = {"enabled": True, "posts": [
            {"title": '<script>alert(1)</script>', "body": '<b>bold</b>',
             "visibility": "network"}]}
        html = render_social_feed(decl, "built", context=full_context())
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertNotIn("<b>bold</b>", html)
        self.assertIn("&lt;script&gt;", html)

    # ---- READY: drafts live in the local drafts tray ----
    def test_draft_posts_render_local_tray(self):
        html = render_social_feed(dict(FEED_DECL), "built",
                                  context=full_context(
                                      granted_permissions=[],
                                      connections={}))
        self.assertIn('class="feed-drafts"', html)
        self.assertIn("Draft thought", html)
        self.assertNotIn('class="feed-publish-btn"', html)

    # ---- acceptance: failure state is visible, never swallowed ----
    def test_failure_state_visible(self):
        decl = {"enabled": True, "posts": [
            {"title": "Flop", "body": "Did not go out.",
             "visibility": "network", "failed": True}]}
        html = render_social_feed(decl, "built", context=full_context())
        self.assertIn("This post failed to publish", html)
        self.assertIn("Flop", html)

    # ---- determinism ----
    def test_determinism(self):
        a = render_social_feed(dict(FEED_DECL), "built",
                               context=full_context())
        b = render_social_feed(dict(FEED_DECL), "built",
                               context=full_context())
        self.assertEqual(a, b)


class SocialFeedResolver(unittest.TestCase):
    def test_resolve_activates_with_all_gates_green(self):
        r = resolve("feature.social_feed", full_context())
        self.assertTrue(r["activated"])
        self.assertEqual(r["function"], "feature.social_feed")
        self.assertEqual(r["events"], ["feed.post.published",
                                       "feed.post.failed"])
        self.assertIn('class="feed-publish-btn"', r["output"])
        self.assertIn('data-consent="connected"', r["output"])

    def test_resolve_undeclared_renders_honest_empty(self):
        c = full_context()
        c["contract"] = {"features": {}}  # social_feed not declared
        r = resolve("feature.social_feed", c)
        self.assertTrue(r["activated"])
        self.assertEqual(r["output"], "")

    def test_resolve_refuses_without_permission(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.social_feed", full_context(
                granted_permissions=[]))
        e = cm.exception
        self.assertEqual(e.code, "permission_denied")
        self.assertEqual(e.missing, ["feed.publish"])
        self.assertIn("feed.publish", e.detail)
        self.assertIn("publish posts", e.detail)  # human words, not just the id

    def test_resolve_refuses_when_requirement_unmet(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.social_feed", full_context(available=[]))
        e = cm.exception
        self.assertEqual(e.code, "requirement_unmet")
        self.assertEqual(e.missing, ["authenticated_identity", "feed_service",
                                     "audience_rules"])
        self.assertIn("feed_service", e.detail)


class SocialFeedAssemble(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ffeed-e2e-")

    def test_assemble_renders_honest_breaker_row(self):
        r, page, _ = run_assemble(
            feed_contract(self.tmp, dict(FEED_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.social_feed"', page)
        self.assertIn('data-consent="ready"', page)

    def test_assemble_row_goes_connected_with_grant_on(self):
        r, page, _ = run_assemble(
            feed_contract(self.tmp, dict(FEED_DECL),
                          connections={"nayanet": True}), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.social_feed"', page)
        self.assertIn('data-consent="connected"', page)
        self.assertIn("connected (nayanet)", page)

    def test_assemble_refuses_undeclared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="feature.social_feed"', page)

    def test_assemble_refuses_bad_declaration(self):
        r, page, _ = run_assemble(
            feed_contract(self.tmp, "yes please"), self.tmp)
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
                if f.get("id") == "feature.social_feed":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        r, page, _ = run_assemble(
            feed_contract(self.tmp, dict(FEED_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)


if __name__ == "__main__":
    unittest.main(verbosity=2)

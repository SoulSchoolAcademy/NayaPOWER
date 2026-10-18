#!/usr/bin/env python3
"""Acceptance tests for feature.community (registry acceptance:
comment_appears, abuse_path_exists, private_page_no_public_comments).

Stdlib only (unittest + subprocess). Three levels, like the
smart_bars suite:

  module level  -> decl_for / can_comment / sanitize_thread /
                   sanitize_post / render_community on live bytes
  resolver level-> resolve() against the real registry (gates + binding)
  end-to-end    -> the real assemble.py against the real builder index

  comment_appears             -> every declared post renders,
    byte-identical and HTML-escaped; a post the declaration lists but
    the page drops silently is a community that cannot be trusted
  abuse_path_exists           -> every rendered post carries a report
    affordance naming the moderation rules
  private_page_no_public_comments -> a private page renders no comment
    UI and no public posts — privacy is a veto, not a render path
  connected_grant             -> the "post to community" action is live
    ONLY when community.comment + community.post are granted AND the
    nayanet connection is strictly ON; otherwise an honest gated block
    names exactly what is missing in the resolver's own human words
  sanitization                -> hostile threads/posts/bad declarations
    -> structured refusals, never silently dropped
  registry binding            -> contract cannot activate what the
    registry does not mark 'built' (fail closed)
  determinism                 -> same declaration + context -> same bytes
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
from feature_community import (CommunityRefusal, can_comment, decl_for,
                               render_community, sanitize_post,
                               sanitize_thread)
from resolver import ResolverRefusal, resolve

COMM_DECL = {
    "enabled": True,
    "threads": [
        {"id": "welcome", "title": "Say hello",
         "posts": [
             {"author": "Ada", "text": "Hello world"},
             {"author": "Bob", "text": "<script>alert(1)</script>"},
         ]},
    ],
}


def full_context(**over):
    """All gates green: permissions, requirements, the nayanet grant."""
    c = {"contract": {"features": {"community": dict(COMM_DECL)}},
         "connections": {"muse": False, "github": False,
                         "network": False, "nayanet": True},
         "privacy": "public",
         "granted_permissions": ["community.comment", "community.post"],
         "available": ["authenticated_identity", "comment_service",
                       "moderation_rules"]}
    c.update(over)
    return c


def community_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    with open(SMOKE) as fh:
        c = json.load(fh)
    c["title"] = "Community acceptance contract"
    c["features"] = {"community": decl}
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


class CommunityModule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fcommunity-")

    # ---- activation gate: nothing declared -> nothing rendered ----
    def test_not_declared_renders_nothing(self):
        for decl in (None, {}, {"enabled": False}):
            html = render_community(decl, "built", context=full_context())
            self.assertEqual(html, "", decl)
        # features carried as a list (contract-page) -> not declared
        self.assertIsNone(decl_for({"features": [["a", "b"]]}))

    # ---- registry binding: fail closed unless the registry says built ----
    def test_not_built_refuses(self):
        with self.assertRaises(CommunityRefusal) as cm:
            render_community(dict(COMM_DECL), "specified",
                             context=full_context())
        self.assertEqual(cm.exception.code, "feature_not_built")

    # ---- decl_for shapes ----
    def test_decl_for_shapes(self):
        self.assertEqual(decl_for({"features": {"community": dict(COMM_DECL)}})["enabled"], True)
        self.assertEqual(decl_for({"features": {"community": True}}),
                         {"enabled": True})
        self.assertIsNone(decl_for({"features": {}}))
        self.assertIsNone(decl_for({}))
        with self.assertRaises(CommunityRefusal) as cm:
            decl_for({"features": {"community": ["bad", "shape"]}})
        self.assertEqual(cm.exception.code, "bad_community_declaration")

    # ---- sanitization ----
    def test_sanitize_thread_bad(self):
        for bad in ({"id": " ", "title": "T"}, {"id": "t", "title": ""},
                    {"id": "t", "title": "T", "posts": "nope"},
                    {"id": "t", "title": "T", "posts": [{"author": "", "text": "x"}]},
                    "a string"):
            with self.assertRaises(CommunityRefusal):
                sanitize_thread(bad)

    def test_sanitize_post_bad(self):
        for bad in ({"author": " ", "text": "x"}, {"author": "A", "text": ""},
                    {"author": "A"}, ["not", "a", "dict"]):
            with self.assertRaises(CommunityRefusal):
                sanitize_post(bad)

    # ---- comment_appears: every declared post renders, HTML-escaped ----
    def test_comment_appears(self):
        html = render_community(dict(COMM_DECL), "built",
                                context=full_context())
        self.assertIn("Ada", html)
        self.assertIn("Hello world", html)
        # the hostile post renders byte-identical but escaped — no live script
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        # acceptance named: every declared post is present
        self.assertEqual(html.count("community-post-text"), 2)

    # ---- abuse_path_exists: every post carries a report affordance ----
    def test_abuse_path_exists(self):
        html = render_community(dict(COMM_DECL), "built",
                                context=full_context())
        self.assertEqual(html.count('data-abuse-path="report"'), 2)
        self.assertIn("moderation rules", html)

    # ---- private_page_no_public_comments: privacy is a veto ----
    def test_private_page_no_public_comments(self):
        html = render_community(dict(COMM_DECL), "built",
                                context=full_context(privacy="private"))
        self.assertNotIn("Hello world", html)
        self.assertNotIn("community-post-text", html)
        self.assertNotIn("community-post-btn", html)
        self.assertNotIn("community-post-box", html)
        self.assertIn("Comments stay off on private pages", html)
        self.assertIn('data-consent="ready"', html)

    # ---- permission gate: ungranted -> honest gated block, never a live post ----
    def test_permission_gate_gated_block(self):
        html = render_community(
            dict(COMM_DECL), "built",
            context=full_context(granted_permissions=[]))
        self.assertNotIn("community-post-btn", html)
        # the resolver's own human words, byte-matched
        self.assertIn("let visitors comment in your community", html)
        self.assertIn("let visitors post in your community", html)
        self.assertIn('data-consent="ready"', html)

    # ---- connected grant: permission on, nayanet off -> still gated ----
    def test_grant_gate_names_the_grant(self):
        html = render_community(
            dict(COMM_DECL), "built",
            context=full_context(connections={"nayanet": False}))
        self.assertNotIn("community-post-btn", html)
        self.assertIn("the NayaNET connection switched on for this page", html)
        self.assertIn('data-consent="ready"', html)

    # ---- all gates green -> live post affordance, consent "connected" ----
    def test_connected_live_post_box(self):
        html = render_community(dict(COMM_DECL), "built",
                                context=full_context())
        self.assertIn("community-post-btn", html)
        self.assertIn('data-consent="connected"', html)
        self.assertIn('data-community-grant="nayanet"', html)

    # ---- empty threads: honest empty line, never a crash ----
    def test_empty_threads_honest(self):
        html = render_community({"enabled": True}, "built",
                                context=full_context())
        self.assertIn("No conversations yet", html)
        self.assertNotIn('class="community-thread"', html)

    # ---- binding + receipt events ----
    def test_binding_and_receipt_events(self):
        html = render_community(dict(COMM_DECL), "built",
                                context=full_context())
        self.assertIn('data-community-status="built"', html)
        self.assertIn("community.comment.posted", html)
        self.assertIn("community.comment.removed", html)

    # ---- determinism ----
    def test_determinism(self):
        self.assertEqual(
            render_community(dict(COMM_DECL), "built", context=full_context()),
            render_community(dict(COMM_DECL), "built", context=full_context()))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class CommunityResolver(unittest.TestCase):
    def test_resolve_activates_with_binding(self):
        r = resolve("feature.community", full_context())
        self.assertTrue(r["activated"])
        self.assertEqual(r["function"], "feature.community")
        self.assertEqual(r["events"],
                         ["community.comment.posted", "community.comment.removed"])
        self.assertIn('data-community-status="built"', r["output"])
        # comment_appears at the resolver level
        self.assertIn("Hello world", r["output"])

    def test_resolve_refuses_when_permission_missing(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.community",
                    full_context(granted_permissions=[]))
        e = cm.exception
        self.assertEqual(e.code, "permission_denied")
        self.assertEqual(e.missing, ["community.comment", "community.post"])
        self.assertIn("community.comment", e.detail)
        self.assertIn("let visitors comment in your community", e.detail)

    def test_resolve_refuses_when_requirement_unmet(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.community", full_context(available=[]))
        e = cm.exception
        self.assertEqual(e.code, "requirement_unmet")
        self.assertEqual(e.missing,
                         ["authenticated_identity", "comment_service",
                          "moderation_rules"])
        self.assertIn("comment_service", e.detail)
        # human words, not just the id
        self.assertIn("a comment service for the community", e.detail)

    def test_resolve_propagates_bad_declaration_as_module_refusal(self):
        # the decl_for call sits outside the resolver's try — a bad
        # declaration propagates as the module's own refusal (the same
        # pattern holds for tabs' TabsRefusal and bars' BarsRefusal).
        # assemble.py guards the contract surface with
        # bad_breaker_declaration before resolve().
        c = full_context()
        c["contract"] = {"features": {"community": "yes please"}}
        with self.assertRaises(CommunityRefusal) as cm:
            resolve("feature.community", c)
        self.assertEqual(cm.exception.code, "bad_community_declaration")


class CommunityAssemble(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fcommunity-e2e-")

    def test_assemble_renders_honest_breaker_row(self):
        r, page, _ = run_assemble(
            community_contract(self.tmp, dict(COMM_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.community"', page)
        # no nayanet grant in the contract assembly path: consent is "ready"
        self.assertIn('data-consent="ready"', page)

    def test_assemble_refuses_undeclared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="feature.community"', page)

    def test_assemble_refuses_bad_declaration(self):
        r, page, _ = run_assemble(
            community_contract(self.tmp, "yes please"), self.tmp)
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
                if f.get("id") == "feature.community":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        r, page, _ = run_assemble(
            community_contract(self.tmp, dict(COMM_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Acceptance tests for feature.space (registry acceptance:
private_space_stays_private, join_flow_tested, member_list_correct).

Stdlib only (unittest + subprocess). Three levels, like the cover suite:

  module level  -> decl_for / can_join / render_smart_space on live bytes
  resolver level-> resolve() against the real registry (gates + binding)
  end-to-end    -> the real assemble.py against the real builder index

  private_space_stays_private -> a private space renders NO join
                                 affordance — the join flow does not
                                 exist for it, even with every grant
  join_flow_tested             -> resolve() activates with all gates
                                 green; the render carries the join
                                 action + consent metadata + receipt
                                 hooks (the registry's own events)
  member_list_correct          -> members render with their declared
                                 names; malformed members are a
                                 structured refusal (never silently
                                 dropped)
  activation gate              -> no space markup unless the contract declares it
  sanitization                 -> hostile members / bad declarations ->
                                 structured refusals
  registry binding             -> contract cannot activate what the registry
                                 does not mark 'built' (fail closed)
  determinism                  -> same declaration + context -> same bytes
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
FUNCTIONS_DIR = os.path.join(SB_DIR, "functions")
INDEX = os.path.normpath(os.path.join(
    SB_DIR, "..", "..", "library", "catalog", "builder-index-v1.json"))
ASSEMBLE = os.path.join(SB_DIR, "assemble.py")
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")
REGISTRY = os.path.join(FUNCTIONS_DIR, "registry.json")

sys.path.insert(0, FUNCTIONS_DIR)
from feature_space import (SpaceRefusal, can_join, decl_for,
                           render_smart_space, sanitize_member,
                           sanitize_space)
from resolver import ResolverRefusal, resolve

SPACE_DECL = {
    "enabled": True,
    "spaces": [
        {"name": "Book club", "visibility": "network",
         "description": "Monthly reads.",
         "members": [{"id": "u1", "name": "Bo"},
                     {"id": "u2", "name": "Rae"}]},
        {"name": "War room", "visibility": "private",
         "members": [{"id": "u3", "name": "Cy"}]},
    ],
}


def full_context(**over):
    """All join gates green: permissions, nayanet grant, requirements."""
    c = {"contract": {"features": {"space": dict(SPACE_DECL)}},
         "connections": {"nayanet": True},
         "privacy": "private",
         "granted_permissions": ["space.create", "space.join"],
         "available": ["authenticated_identity", "space_service",
                       "membership_rules"]}
    c.update(over)
    return c


def space_contract(tmp, decl, connections=None):
    """A customer contract: smoke contract with features as a breaker dict."""
    with open(SMOKE) as fh:
        c = json.load(fh)
    c["title"] = "Smart Space acceptance contract"
    c["features"] = {"space": decl}
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


class SmartSpaceModule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fspace-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- activation gate: nothing declared -> nothing renders ----
    def test_refusal_when_not_declared(self):
        self.assertEqual(render_smart_space(None, "built"), "")
        self.assertEqual(
            render_smart_space({"enabled": False}, "built"), "")
        self.assertEqual(
            decl_for({"features": {}}), None)
        self.assertEqual(
            decl_for({"features": [("a", "b")]}), None)  # contract-page shape

    def test_decl_shapes(self):
        self.assertEqual(decl_for({"features": {"space": True}}),
                         {"enabled": True})
        d = {"enabled": True, "spaces": []}
        self.assertEqual(decl_for({"features": {"space": d}}), d)

    def test_malformed_declaration_refused(self):
        with self.assertRaises(SpaceRefusal) as cm:
            decl_for({"features": {"space": "yes please"}})
        self.assertEqual(cm.exception.code, "bad_smart_space_declaration")

    def test_member_sanitization(self):
        self.assertEqual(sanitize_member({"id": "u1", "name": "Bo"}),
                         {"id": "u1", "name": "Bo"})
        for bad in ({"name": "NoId"}, {"id": "u1"}, {"id": "", "name": "X"},
                    {"id": "  ", "name": "X"}, "not-a-dict", None):
            with self.assertRaises(SpaceRefusal) as cm:
                sanitize_member(bad)
            self.assertEqual(cm.exception.code, "bad_space_member", bad)

    def test_render_refuses_bad_member(self):
        decl = {"enabled": True, "spaces": [
            {"name": "S", "members": [{"id": "u1"}]}]}  # name missing
        with self.assertRaises(SpaceRefusal) as cm:
            render_smart_space(decl, "built", context=full_context())
        self.assertEqual(cm.exception.code, "bad_space_member")

    def test_bad_visibility_refused(self):
        decl = {"enabled": True, "spaces": [
            {"name": "S", "visibility": "galaxy"}]}
        with self.assertRaises(SpaceRefusal) as cm:
            render_smart_space(decl, "built", context=full_context())
        self.assertEqual(cm.exception.code, "bad_space_visibility")

    def test_feature_not_built_refused(self):
        with self.assertRaises(SpaceRefusal) as cm:
            render_smart_space(dict(SPACE_DECL), "specified",
                               context=full_context())
        self.assertEqual(cm.exception.code, "feature_not_built")

    # ---- private_space_stays_private ----
    def test_private_space_stays_private(self):
        html = render_smart_space(dict(SPACE_DECL), "built",
                                  context=full_context())
        # the network space got a live join affordance
        self.assertEqual(html.count('class="space-join-btn"'), 1)
        # the private space got none — the join flow does not exist for it
        self.assertIn("members only", html)
        # ...but its member list still renders (member_list_correct)
        self.assertIn("Cy", html)
        self.assertIn('data-visibility="private"', html)

    def test_member_list_correct(self):
        html = render_smart_space(dict(SPACE_DECL), "built",
                                  context=full_context())
        for mid, name in (("u1", "Bo"), ("u2", "Rae"), ("u3", "Cy")):
            self.assertIn('data-member-id="%s"' % mid, html)
            self.assertIn(name, html)

    # ---- join is the connected action: honest gated block otherwise ----
    def test_unauthorized_join_denied_module_gates(self):
        base = full_context()
        decl = {"enabled": True, "spaces": [
            {"name": "Open", "visibility": "network",
             "members": [{"id": "u1", "name": "Bo"}]}]}
        cases = [
            dict(base, granted_permissions=["space.create"]),  # space.join off
            dict(base, connections={"nayanet": False}),
            dict(base, connections={"nayanet": "yes"}),        # truthy != True
        ]
        for ctx in cases:
            allowed, missing = can_join(ctx)
            self.assertFalse(allowed)
            self.assertTrue(missing, ctx)
            html = render_smart_space(dict(decl), "built", context=ctx)
            self.assertIn('data-feature="smart_space"', html)
            self.assertIn('data-consent="ready"', html)
            self.assertIn("Joining is ready but off.", html)
            self.assertNotIn('class="space-join-btn"', html)

    def test_render_carries_members_escaped(self):
        decl = {"enabled": True, "spaces": [
            {"name": '<script>alert(1)</script>', "visibility": "network",
             "members": [{"id": "u1", "name": "<b>bold</b>"}]}]}
        html = render_smart_space(decl, "built", context=full_context())
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertIn("&lt;b&gt;bold&lt;/b&gt;", html)

    def test_empty_space_renders_ready_ui(self):
        decl = {"enabled": True, "spaces": [{"name": "Fresh"}]}
        html = render_smart_space(decl, "built", context=full_context())
        self.assertIn("No members yet", html)
        self.assertIn('data-visibility="private"', html)  # private default

    # ---- determinism: same declaration + context -> same bytes ----
    def test_determinism(self):
        h1 = hashlib.sha256(
            render_smart_space(dict(SPACE_DECL), "built",
                               context=full_context()).encode()).hexdigest()
        h2 = hashlib.sha256(
            render_smart_space(dict(SPACE_DECL), "built",
                               context=full_context()).encode()).hexdigest()
        self.assertEqual(h1, h2)


class SmartSpaceResolver(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fspace-res-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_join_requires_space_join_grant(self):
        c = full_context(granted_permissions=["space.create"])  # join off
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.space", c)
        self.assertEqual(cm.exception.code, "permission_denied")
        self.assertIn("space.join", cm.exception.missing)
        # the refusal speaks in human words, never a bare permission token
        self.assertNotIn("permission 'space.join'", cm.exception.detail)

    def test_join_requires_space_service(self):
        c = full_context(available=["authenticated_identity"])  # services off
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.space", c)
        self.assertEqual(cm.exception.code, "requirement_unmet")
        self.assertIn("space_service", cm.exception.missing)

    # ---- join_flow_tested: resolver level ----
    def test_join_flow_tested_resolver(self):
        r = resolve("feature.space", full_context())
        self.assertTrue(r["activated"])
        self.assertEqual(r["function"], "feature.space")
        self.assertEqual(r["events"],
                         ["space.created", "space.joined", "space.left"])
        # the network space got a live join affordance
        self.assertIn('data-feature="smart_space"', r["output"])
        self.assertIn('data-consent="connected"', r["output"])
        self.assertIn('class="space-join-btn"', r["output"])
        self.assertIn('data-receipt-events="space.created space.joined space.left"',
                      r["output"])
        # the private space did NOT
        self.assertEqual(r["output"].count('class="space-join-btn"'), 1)
        self.assertIn("members only", r["output"])

    def test_resolver_stays_blocked_on_registry(self):
        # registry binding as a live falsifier: import a tree-copy of the
        # resolver whose registry still says 'specified' and prove the
        # SAME resolve() call stays blocked at gate 2 — the flip is what
        # opened the gate, not the module's existence.
        import importlib.util
        tree = os.path.join(self.tmp, "rescopy")
        shutil.copytree(FUNCTIONS_DIR, tree)
        regp = os.path.join(tree, "registry.json")
        with open(regp) as fh:
            reg = json.load(fh)
        for g in reg["groups"].values():
            for f in g.get("functions", []):
                if f.get("id") == "feature.space":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        spec = importlib.util.spec_from_file_location(
            "resolver_copy_smart_space",
            os.path.join(tree, "resolver.py"))
        rescopy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rescopy)
        with self.assertRaises(rescopy.ResolverRefusal) as cm:
            rescopy.resolve("feature.space", full_context())
        self.assertEqual(cm.exception.code, "not_implemented")


class SmartSpaceEndToEnd(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fspace-e2e-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_assemble_renders_honest_breaker_row(self):
        # nayanet off -> the §7 row says ready, never connected
        r, page, manifest = run_assemble(
            space_contract(self.tmp, dict(SPACE_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.space"', page)
        self.assertIn('data-consent="ready"', page)
        machine = json.loads(__import__("re").search(
            r'<pre id="machinejson">(.*?)</pre>', page, __import__("re").S).group(1))
        self.assertEqual(machine["features_status"]["space"], "built")
        consent = manifest.get("receipt", {}).get("consent", {}).get(
            "feature.space", {})
        self.assertEqual(consent.get("connected_active"), [])

    def test_assemble_row_goes_connected_with_grant_on(self):
        # space's registry entry carries a connected action (invite and
        # join sync, grant nayanet) — the §7 row honestly flips to
        # "connected (nayanet)" when the grant is on.
        r, page, _ = run_assemble(
            space_contract(self.tmp, dict(SPACE_DECL),
                           connections={"nayanet": True}), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.space"', page)
        self.assertIn('data-consent="connected"', page)
        self.assertIn("connected (nayanet)", page)

    def test_assemble_refuses_undeclared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="feature.space"', page)

    def test_assemble_refuses_bad_declaration(self):
        r, page, _ = run_assemble(
            space_contract(self.tmp, "yes please"), self.tmp)
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
                if f.get("id") == "feature.space":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        r, page, _ = run_assemble(
            space_contract(self.tmp, dict(SPACE_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)


if __name__ == "__main__":
    unittest.main(verbosity=2)

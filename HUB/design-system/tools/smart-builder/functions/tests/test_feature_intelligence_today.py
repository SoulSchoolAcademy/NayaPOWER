#!/usr/bin/env python3
"""Acceptance tests for feature.intelligence_today (registry acceptance:
only_own_data_shown, report_renders, empty_state_handled).

Stdlib only (unittest + subprocess). Three levels, like the space suite:

  module level  -> decl_for / can_read / can_sync / sanitize_report /
                   render_intelligence_today on live bytes
  resolver level-> resolve() against the real registry (gates + binding)
  end-to-end    -> the real assemble.py against the real builder index

  only_own_data_shown -> a report owned by another identity never renders
                         — not its title, not its body, not a teaser —
                         even with every grant
  report_renders      -> the viewer's own reports render full when the
                         reports.read permission is granted; an honest
                         gated block names the permission when not
  empty_state_handled -> declared with zero reports renders the honest
                         empty line — never an empty section, never a
                         crash, never a fake report
  activation gate     -> no intelligence markup unless the contract
                         declares it
  sanitization        -> hostile reports / bad declarations ->
                         structured refusals
  registry binding    -> contract cannot activate what the registry
                         does not mark 'built' (fail closed)
  determinism         -> same declaration + context -> same bytes
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
from feature_intelligence_today import (IntelligenceTodayRefusal, can_read,
                                        can_sync, decl_for,
                                        render_intelligence_today,
                                        sanitize_report)
from resolver import ResolverRefusal, resolve

INTEL_DECL = {
    "enabled": True,
    "reports": [
        {"title": "Your Tuesday briefing", "period": "daily",
         "owner": "shawn", "summary": "Three things moved today.",
         "generated": "2026-10-17"},
        {"title": "Week in review", "period": "weekly",
         "owner": "shawn", "summary": "A quiet week, one launch.",
         "generated": "2026-10-12"},
        {"title": "Someone else's report", "period": "daily",
         "owner": "stranger", "summary": "Not yours. Never shown.",
         "generated": "2026-10-17"},
    ],
}


def full_context(**over):
    """All gates green: permission, muse grant, requirements, identity."""
    c = {"contract": {"features": {"intelligence_today": dict(INTEL_DECL)}},
         "connections": {"muse": True},
         "privacy": "private",
         "granted_permissions": ["reports.read"],
         "available": ["authenticated_identity", "report_pipeline",
                       "data_authorization"],
         "identity": {"id": "shawn"}}
    c.update(over)
    return c


def intel_contract(tmp, decl, connections=None):
    """A customer contract: smoke contract with features as a breaker dict."""
    with open(SMOKE) as fh:
        c = json.load(fh)
    c["title"] = "Intelligence Today acceptance contract"
    c["features"] = {"intelligence_today": decl}
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


class IntelModule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fintel-")

    # ---- F1: activation gate: nothing declared -> nothing rendered ----
    def test_not_declared_renders_nothing(self):
        for decl in (None, {}, {"enabled": False}):
            html = render_intelligence_today(decl, "built",
                                             context=full_context())
            self.assertEqual(html, "", decl)
        # features carried as a list (contract-page) -> not declared
        self.assertIsNone(decl_for({"features": [["a", "b"]]}))

    # ---- F2: registry binding: fail closed unless the registry says built --
    def test_not_built_refuses(self):
        with self.assertRaises(IntelligenceTodayRefusal) as cm:
            render_intelligence_today(dict(INTEL_DECL), "specified",
                                      context=full_context())
        self.assertEqual(cm.exception.code, "feature_not_built")

    # ---- decl_for shapes ----
    def test_decl_for_shapes(self):
        self.assertEqual(decl_for({"features": {"intelligence_today": True}}),
                         {"enabled": True})
        d = {"enabled": True, "reports": []}
        self.assertEqual(decl_for({"features": {"intelligence_today": d}}), d)
        self.assertIsNone(decl_for({"features": {"intelligence_today": False}}))
        self.assertIsNone(decl_for({"features": {}}))
        self.assertIsNone(decl_for({}))
        with self.assertRaises(IntelligenceTodayRefusal) as cm:
            decl_for({"features": {"intelligence_today": "yes please"}})
        self.assertEqual(cm.exception.code, "bad_intelligence_declaration")

    # ---- sanitize_report ----
    def test_sanitize_report_accepts_good(self):
        r = sanitize_report({"title": "T", "period": "monthly",
                             "owner": "shawn"})
        self.assertEqual((r["title"], r["period"], r["owner"]),
                         ("T", "monthly", "shawn"))

    # ---- F7: malformed reports -> structured refusal, never dropped ----
    def test_sanitize_report_rejects_malformed(self):
        bad = [
            "not a dict",
            {"title": "", "period": "daily", "owner": "shawn"},
            {"title": "T", "period": "hourly", "owner": "shawn"},
            {"title": "T", "period": "daily", "owner": "  "},
            {"title": "T", "period": "daily"},
            {"title": "T", "period": "daily", "owner": "shawn",
             "summary": 42},
        ]
        for b in bad:
            with self.assertRaises(IntelligenceTodayRefusal) as cm:
                sanitize_report(b)
            self.assertEqual(cm.exception.code, "bad_intelligence_report",
                             b)

    # ---- F3: only_own_data_shown ----
    def test_only_own_data_shown(self):
        html = render_intelligence_today(dict(INTEL_DECL), "built",
                                         context=full_context())
        self.assertIn("Your Tuesday briefing", html)
        self.assertIn("Three things moved today.", html)
        self.assertNotIn("Someone else&#x27;s report", html)
        self.assertNotIn("Someone else's report", html)
        self.assertNotIn("Not yours. Never shown.", html)
        self.assertNotIn("stranger", html)

    # ---- no identity: no personal data renders, ever ----
    def test_no_identity_shows_nothing_personal(self):
        ctx = full_context()
        del ctx["identity"]
        html = render_intelligence_today(dict(INTEL_DECL), "built",
                                         context=ctx)
        self.assertIn("Sign in to see your reports", html)
        self.assertNotIn("Your Tuesday briefing", html)
        self.assertNotIn("Three things moved today.", html)

    # ---- F4: empty_state_handled ----
    def test_empty_state(self):
        html = render_intelligence_today({"enabled": True, "reports": []},
                                         "built", context=full_context())
        self.assertIn("No reports yet", html)
        self.assertNotIn("intel-report", html.replace(
            "intel-reports", "").replace("intel-report-", "X"))

    # ---- F5: bodies are a permission question ----
    def test_read_gated_without_permission(self):
        ctx = full_context(granted_permissions=[])
        html = render_intelligence_today(dict(INTEL_DECL), "built",
                                         context=ctx)
        self.assertIn("your permission to read your reports", html)
        self.assertNotIn("Three things moved today.", html)

    def test_bodies_render_with_permission(self):
        html = render_intelligence_today(dict(INTEL_DECL), "built",
                                         context=full_context())
        self.assertIn("Three things moved today.", html)
        self.assertIn("Week in review", html)

    # ---- F6: sync is the connected action: grant-gated, never dead ----
    def test_sync_live_with_grant(self):
        html = render_intelligence_today(dict(INTEL_DECL), "built",
                                         context=full_context())
        self.assertIn('class="intel-sync-btn"', html)
        self.assertIn("Sync intelligence", html)
        self.assertIn('data-consent="connected"', html)

    def test_sync_gated_without_grant(self):
        ctx = full_context(connections={"muse": False})
        html = render_intelligence_today(dict(INTEL_DECL), "built",
                                         context=ctx)
        # reports still render (permission granted) but sync is gated
        self.assertIn("Three things moved today.", html)
        self.assertNotIn('class="intel-sync-btn"', html)
        self.assertIn("the Muse connection switched on for this page", html)
        self.assertIn('data-consent="ready"', html)

    def test_truthy_grant_is_not_enough(self):
        ctx = full_context(connections={"muse": "yes"})
        self.assertFalse(can_sync(ctx)[0])  # strict boolean, not truthy

    # ---- XSS: hostile strings are escaped, never executed ----
    def test_xss_escaped(self):
        evil = {"title": "<script>alert(1)</script>", "period": "daily",
                "owner": "shawn", "summary": "<img src=x onerror=alert(2)>",
                "generated": "2026-10-17\"><b>bold</b>"}
        html = render_intelligence_today(
            {"enabled": True, "reports": [evil]}, "built",
            context=full_context())
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertNotIn("<img src=x onerror=alert(2)>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertIn("&lt;img src=x onerror=alert(2)&gt;", html)

    # ---- determinism ----
    def test_determinism(self):
        a = render_intelligence_today(dict(INTEL_DECL), "built",
                                      context=full_context())
        b = render_intelligence_today(dict(INTEL_DECL), "built",
                                      context=full_context())
        self.assertEqual(a, b)


class IntelResolver(unittest.TestCase):
    def test_resolve_activates_with_all_gates_green(self):
        r = resolve("feature.intelligence_today", full_context())
        self.assertTrue(r["activated"])
        self.assertEqual(r["function"], "feature.intelligence_today")
        self.assertEqual(r["events"], ["reports.generated", "reports.viewed"])
        self.assertIn('class="intel-sync-btn"', r["output"])
        self.assertIn('data-consent="connected"', r["output"])

    def test_resolve_undeclared_renders_honest_empty(self):
        c = full_context()
        c["contract"] = {"features": {}}  # intelligence_today not declared
        r = resolve("feature.intelligence_today", c)
        self.assertTrue(r["activated"])
        self.assertEqual(r["output"], "")

    def test_resolve_refuses_without_permission(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.intelligence_today",
                    full_context(granted_permissions=[]))
        e = cm.exception
        self.assertEqual(e.code, "permission_denied")
        self.assertEqual(e.missing, ["reports.read"])
        self.assertIn("reports.read", e.detail)

    def test_resolve_refuses_when_requirement_unmet(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.intelligence_today", full_context(available=[]))
        e = cm.exception
        self.assertEqual(e.code, "requirement_unmet")
        self.assertEqual(e.missing, ["authenticated_identity",
                                     "report_pipeline",
                                     "data_authorization"])
        self.assertIn("report_pipeline", e.detail)


class IntelAssemble(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fintel-e2e-")

    def test_assemble_renders_honest_breaker_row(self):
        r, page, _ = run_assemble(
            intel_contract(self.tmp, dict(INTEL_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.intelligence_today"', page)
        self.assertIn('data-consent="ready"', page)

    def test_assemble_row_goes_connected_with_grant_on(self):
        r, page, _ = run_assemble(
            intel_contract(self.tmp, dict(INTEL_DECL),
                           connections={"muse": True}), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.intelligence_today"', page)
        self.assertIn('data-consent="connected"', page)
        self.assertIn("connected (muse)", page)

    def test_assemble_refuses_undeclared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="feature.intelligence_today"', page)

    def test_assemble_refuses_bad_declaration(self):
        r, page, _ = run_assemble(
            intel_contract(self.tmp, "yes please"), self.tmp)
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
                if f.get("id") == "feature.intelligence_today":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        r, page, _ = run_assemble(
            intel_contract(self.tmp, dict(INTEL_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)


if __name__ == "__main__":
    unittest.main(verbosity=2)

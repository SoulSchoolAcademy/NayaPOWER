#!/usr/bin/env python3
"""Acceptance tests for feature.automation (registry acceptance:
undeclared_action_refused, action_permission_gated, every_action_logged,
execution_transport_named_blocked, schedule_declared_not_fired).

Stdlib only (unittest + subprocess). The work-tree registry carries the module
as 'specified' until the flip; each test therefore runs assemble from a
fixture copy of the smart-builder tree whose registry marks the module
'built' — except test_specified_registry_refuses, which proves the gate
refuses while specified. Every test runs the real assemble.py end-to-end
against the real builder index.
"""
import copy
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
ASSEMBLE = os.path.join(SB_DIR, "assemble.py")
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")

AM_DECL = {
    "enabled": True,
    "actions": [
        {"id": "morning-post", "kind": "scheduled_post",
         "schedule": "daily 08:00", "permission": "automation.run",
         "payload": {"template": "daily-intel"}},
        {"id": "weekly-digest", "kind": "digest",
         "schedule": "monday 09:00", "permission": "automation.run"},
    ],
    "grants": ["automation.run"],
}

FLIP_IDS = ("feature.automation",)


def flip_registry(tree):
    regp = os.path.join(tree, "functions", "registry.json")
    reg = json.load(open(regp))
    for g in reg["groups"].values():
        for f in g.get("functions", []):
            if f.get("id") in FLIP_IDS:
                f["status"] = "built"
    json.dump(reg, open(regp, "w"), indent=2)


def am_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    c = json.load(open(SMOKE))
    c["title"] = "Automation acceptance contract"
    c["features"] = {"automation": decl}
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


class FeatureAutomationAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fam-")
        self.tree = os.path.join(self.tmp, "sbcopy")
        shutil.copytree(SB_DIR, self.tree)
        flip_registry(self.tree)
        self.assemble = os.path.join(self.tree, "assemble.py")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_decl(self, decl):
        return run_assemble(am_contract(self.tmp, decl), self.tmp,
                            assemble=self.assemble, sb_dir=self.tree)

    # ---- explicit-true activation: declared actions arm + audit ----
    def test_activation_via_contract(self):
        r, page, manifest = self.run_decl(copy.deepcopy(AM_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="automation"', page)
        self.assertIn('data-automation-status="built"', page)
        self.assertIn("morning-post", page)
        self.assertIn("scheduled_post", page)
        self.assertIn("daily 08:00", page)
        self.assertIn("weekly-digest", page)
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["automation"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        declared = [e for e in events
                    if e.get("event") == "automation.action_declared"]
        self.assertEqual(len(declared), 2)
        self.assertTrue(all(e["permission_gate"] == "granted" for e in declared))
        blocked = [e for e in events
                   if e.get("event") == "automation.execution_blocked"]
        self.assertEqual(len(blocked), 1)
        self.assertEqual(blocked[0]["actions_declared"], 2)
        self.assertEqual(blocked[0]["transport"], "BLOCKED")

    # ---- every_action_logged: the receipt's audit names every action ----
    def test_every_action_logged(self):
        r, page, manifest = self.run_decl(copy.deepcopy(AM_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        audit = manifest.get("receipt", {}).get("automation_audit", [])
        self.assertEqual(len(audit), 2)
        by_id = {a["action_id"]: a for a in audit}
        self.assertEqual(set(by_id), {"morning-post", "weekly-digest"})
        for a in audit:
            self.assertEqual(a["permission_gate"], "granted")
            self.assertIn("not connected", a["status"])
            self.assertIn("transport.automation.run", a["status"])
        self.assertEqual(by_id["morning-post"]["kind"], "scheduled_post")
        self.assertEqual(by_id["morning-post"]["schedule"], "daily 08:00")

    # ---- explicit-false suppression + omitted: nothing renders ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp,
                                  assemble=self.assemble, sb_dir=self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="automation"', page)

    def test_refusal_when_declared_but_disabled(self):
        decl = copy.deepcopy(AM_DECL)
        decl["enabled"] = False
        r, page, manifest = self.run_decl(decl)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="automation"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "automation.action_declared"
                             for e in events))
        self.assertNotIn("automation_audit", manifest.get("receipt", {}))

    # ---- action_permission_gated: ungranted permission -> refused ----
    def test_permission_denied_refused(self):
        decl = copy.deepcopy(AM_DECL)
        decl["grants"] = []  # nothing granted
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("automation_permission_denied", codes)
        self.assertNotIn('data-feature="automation"', page)

    # ---- hostile inputs: unknown kind, missing id, bad schedule ----
    def test_unknown_kind_refused(self):
        decl = {"enabled": True,
                "actions": [{"id": "x", "kind": "take_over_world",
                             "schedule": "now", "permission": "p"}],
                "grants": ["p"]}
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_automation_kind", codes)

    def test_undeclared_action_refused(self):
        # missing id -> the action was never properly declared
        decl = {"enabled": True,
                "actions": [{"kind": "digest", "schedule": "daily",
                             "permission": "p"}],
                "grants": ["p"]}
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_automation_action", codes)
        self.assertNotIn('data-feature="automation"', page)

    def test_duplicate_id_refused(self):
        decl = copy.deepcopy(AM_DECL)
        decl["actions"].append(dict(decl["actions"][0]))
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_automation_action", codes)

    def test_payload_injection_escaped(self):
        decl = {"enabled": True,
                "actions": [{"id": "<script>alert(1)</script>",
                             "kind": "backup", "schedule": "daily",
                             "permission": "p"}],
                "grants": ["p"]}
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)

    def test_malformed_declaration_refused(self):
        r, page, _ = self.run_decl("yes please")
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_automation_declaration", codes)

    # ---- schedule_declared_not_fired: declared, never staged as run ----
    def test_schedule_declared_not_fired(self):
        r, page, _ = self.run_decl(copy.deepcopy(AM_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-exec-state="not-connected"', page)
        self.assertIn("not connected", page)
        self.assertIn("connect a scheduler runner to enable", page)
        low = page.lower()
        for claim in ("last run", "running now", "executed at", "just ran",
                      "next run in"):
            self.assertNotIn(claim, low, "staged execution claim: %r" % claim)

    # ---- DAY-ONE TEST (Shawn 21:34Z): minimal contract -> useful render, zero errors ----
    def test_day_one_minimal_contract(self):
        r, page, manifest = self.run_decl(True)  # the smallest possible declaration
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("refused", r.stdout)
        self.assertNotIn("Traceback", r.stderr)
        self.assertIn('data-feature="automation"', page)
        self.assertIn("Automation", page)  # useful: heading + declared-actions panel
        self.assertIn("No automatic actions declared yet", page)
        self.assertIn("connect a scheduler runner to enable", page)

    # ---- execution_transport_named_blocked: never staged ----
    def test_execution_transport_named_blocked(self):
        r, page, manifest = self.run_decl(copy.deepcopy(AM_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("connect a scheduler runner to enable", page)
        events = manifest.get("receipt", {}).get("events", [])
        blocked = [e for e in events
                   if e.get("event") == "automation.execution_blocked"][0]
        self.assertEqual(blocked["transport"], "BLOCKED")
        self.assertEqual(blocked["transport_name"], "scheduler runner")
        self.assertEqual(blocked["grant_needed"], "transport.automation.run")

    # ---- fallback: enabled with no actions -> honest empty state ----
    def test_fallback_no_actions(self):
        r, page, manifest = self.run_decl({"enabled": True, "actions": [],
                                       "grants": []})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="automation"', page)
        self.assertIn("No automatic actions declared yet", page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "automation.action_declared"
                             for e in events))
        # the execution block is still recorded — honesty even when empty
        self.assertTrue(any(e.get("event") == "automation.execution_blocked"
                            for e in events))
        self.assertEqual(manifest["receipt"]["automation_audit"], [])

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
                if fn.get("id") == "feature.automation":
                    fn["status"] = "specified"
        json.dump(reg, open(regp, "w"), indent=2)
        r, page, _ = run_assemble(am_contract(self.tmp, copy.deepcopy(AM_DECL)), self.tmp,
                                  assemble=os.path.join(tree, "assemble.py"),
                                  sb_dir=tree)
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        mod_errs = [e for e in errs if e.get("feature") == "feature.automation"]
        self.assertTrue(mod_errs, errs)
        self.assertEqual(mod_errs[0]["code"], "feature_not_built")
        self.assertNotIn('data-feature="automation"', page)

    # ---- READY vs CONNECTED (Naya 3, 21:41Z): the missing grant is named ----
    def test_ready_connected_split_names_grant(self):
        r, page, manifest = self.run_decl(copy.deepcopy(AM_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("connect a scheduler runner to enable", page)
        reg = json.load(open(os.path.join(self.tree, "functions", "registry.json")))
        entry = [f for g in reg["groups"].values() for f in g.get("functions", [])
                 if f.get("id") == "feature.automation"][0]
        self.assertTrue(entry["ready"])
        self.assertEqual(entry["connected"]["grant"], "transport.automation.run")
        audit = manifest.get("receipt", {}).get("automation_audit", [])
        self.assertTrue(audit)
        for a in audit:
            self.assertIn("transport.automation.run", a["status"])

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = am_contract(self.tmp, copy.deepcopy(AM_DECL))
        _, page1, _ = run_assemble(contract, self.tmp,
                                    assemble=self.assemble, sb_dir=self.tree)
        d2 = tempfile.mkdtemp(prefix="fam-b-")
        try:
            _, page2, _ = run_assemble(contract, d2,
                                        assemble=self.assemble, sb_dir=self.tree)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Acceptance tests for feature.intelligence_today (registry acceptance:
only_own_data_shown, report_renders, empty_state_handled).

Stdlib only (unittest + subprocess). Each test runs the real
assemble.py end-to-end against the real builder index:

  activation              -> contract-carried reports render as cards
  explicit true/false     -> true renders; explicit false suppresses
  omitted (dict-form)     -> assembler default-on policy (standards on)
  day-one                 -> minimal declaration renders useful output,
                             zero errors, no setup
  connections             -> the module gates nothing on connections
  privacy dial            -> reports private by default, stamped per dial;
                             unknown values refused
  gate                    -> no section unless the contract declares it
  sanitization            -> unknown periods / malformed reports -> refusal
  fallback (empty state)  -> enabled but no reports -> "No reports yet"
  privacy structure       -> only contract-carried data renders; nothing is
                             invented or pulled (the module has no I/O)
  registry binding        -> contract cannot activate what the registry does
                             not mark 'built' (fail closed)
  determinism             -> same contract -> same bytes
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
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")

IT_DECL = {
    "enabled": True,
    "reports": [
        {"period": "daily", "label": "Today",
         "summary": "Quiet morning, two orders before 9.",
         "generated_at": "2026-10-17",
         "metrics": [{"label": "Smart notes", "value": "12"},
                     {"label": "Orders", "value": "2"}]},
        {"period": "weekly", "label": "This week",
         "summary": "Bread up 18%.",
         "metrics": [{"label": "Revenue", "value": "$1,240"}]},
    ],
}


def tree_with_status(tmp, status):
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


def it_contract(tmp, decl):
    c = json.load(open(SMOKE))
    c["title"] = "Intelligence Today acceptance contract"
    c["features"] = {"intelligence_today": decl}
    p = os.path.join(tmp, "contract.json")
    json.dump(c, open(p, "w"))
    return p


def full_contract(tmp, features, privacy=None, connections=None):
    """A customer contract with an explicit features dict plus optional
    top-level privacy/connections blocks."""
    c = json.load(open(SMOKE))
    c["title"] = "Intelligence Today acceptance contract"
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


class FeatureIntelligenceTodayAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fit-")
        self.tree = tree_with_status(self.tmp, "built")
        self.assemble = os.path.join(self.tree, "assemble.py")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- report_renders: contract-carried reports land as cards ----
    def test_activation_via_contract(self):
        r, page, manifest = run_assemble(
            it_contract(self.tmp, dict(IT_DECL)), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="intelligence_today"', page)
        self.assertIn('data-intelligence_today-status="built"', page)
        self.assertIn('data-period="daily"', page)
        self.assertIn('data-period="weekly"', page)
        self.assertIn("Quiet morning, two orders before 9.", page)
        self.assertIn("Smart notes", page)
        self.assertIn("$1,240", page)
        self.assertIn("Generated 2026-10-17", page)
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["intelligence_today"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "intelligence_today.updated"
                            and e.get("feature") == "feature.intelligence_today"
                            for e in events))

    # ---- only_own_data_shown: nothing the contract did not carry renders ----
    def test_only_contract_data_renders(self):
        r, page, _ = run_assemble(
            it_contract(self.tmp, dict(IT_DECL)), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        section = page.split('data-feature="intelligence_today"')[1].split(
            "</section>")[0]
        # the monthly and yearly periods were not declared: absent
        self.assertNotIn('data-period="monthly"', section)
        self.assertNotIn('data-period="yearly"', section)
        # no third-party data sneaks in
        self.assertNotIn("google-analytics", section.lower())

    def test_xss_escaped(self):
        decl = {"enabled": True, "reports": [
            {"period": "daily", "label": "<b>Today</b>",
             "summary": '<script>alert(1)</script>',
             "metrics": [{"label": "<img src=x onerror=1>", "value": "9"}]}]}
        r, page, _ = run_assemble(
            it_contract(self.tmp, decl), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        section = page.split('data-feature="intelligence_today"')[1].split(
            "</section>")[0]
        self.assertNotIn("<script>alert(1)</script>", section)
        self.assertNotIn("<img src=x onerror=1>", section)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", section)

    # ---- gate: the page refuses to render reports it was not given ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp, self.assemble)  # list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="intelligence_today"', page)
        self.assertNotIn('<section class="intelligence-today"', page)

    def test_refusal_when_declared_but_disabled(self):
        decl = dict(IT_DECL, enabled=False)
        r, page, manifest = run_assemble(
            it_contract(self.tmp, decl), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="intelligence_today"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "intelligence_today.updated"
                             for e in events))

    # ---- sanitization: malformed reports are structured refusals ----
    def test_malformed_reports_refused(self):
        cases = [
            {"enabled": True, "reports": "not-a-list"},
            {"enabled": True, "reports": [{"period": "fortnightly",  # unknown
                                           "label": "X"}]},
            {"enabled": True, "reports": [
                {"period": "daily", "label": "A"},
                {"period": "daily", "label": "B"}]},  # duplicate period
            {"enabled": True, "reports": [{"period": "daily"}]},  # no label
            {"enabled": True, "reports": [{"period": "daily", "label": "A",
                                           "summary": 42}]},
            {"enabled": True, "reports": [{"period": "daily", "label": "A",
                                           "metrics": "nope"}]},
            {"enabled": True, "reports": [{"period": "daily", "label": "A",
                                           "metrics": [{"label": "x"}]}]},  # no value
            {"enabled": True, "reports": [{"period": "daily", "label": "A",
                                           "metrics": [
                                               {"label": "m%d" % i, "value": "v"}
                                               for i in range(13)]}]},  # > max
            {"enabled": True, "reports": [{"period": "daily", "label": "A",
                                           "metrics": [{"label": "  "}]}]},  # blank label
            "yes please",  # not an object
        ]
        for decl in cases:
            r, page, _ = run_assemble(
                it_contract(self.tmp, decl), self.tmp, self.assemble)
            self.assertEqual(r.returncode, 2, decl)
            self.assertNotIn('data-feature="intelligence_today"', page)

    def test_malformed_codes_are_structured(self):
        decl = {"enabled": True, "reports": [{"period": "hourly", "label": "X"}]}
        r, _, _ = run_assemble(it_contract(self.tmp, decl), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 2)
        body = json.loads(r.stdout)
        self.assertEqual(body["status"], "refused")
        codes = [e["code"] for e in body["errors"]]
        self.assertIn("bad_intelligence_declaration", codes)

    # ---- empty_state_handled: enabled but no reports -> honest empty state
    def test_fallback_empty_state(self):
        for decl in ({"enabled": True},
                     {"enabled": True, "reports": []},
                     True):
            r, page, _ = run_assemble(
                it_contract(self.tmp, decl), self.tmp, self.assemble)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn('data-feature="intelligence_today"', page)
            self.assertIn("intelligence-empty", page)
            self.assertIn("No reports yet", page)
            # no invented report cards
            section = page.split('data-feature="intelligence_today"')[1].split(
                "</section>")[0]
            self.assertNotIn("intelligence-card", section)

    # ---- the general gate: an unbuilt breaker fails the contract closed ----
    def test_unbuilt_breaker_refused(self):
        tree = tree_with_status(self.tmp, "specified")
        asm = os.path.join(tree, "assemble.py")
        r, page, _ = run_assemble(
            it_contract(self.tmp, dict(IT_DECL)), self.tmp, asm)
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        it_errs = [e for e in errs
                   if e.get("feature") == "feature.intelligence_today"]
        self.assertTrue(it_errs, errs)
        self.assertIn("feature_not_built", [e["code"] for e in it_errs])
        self.assertNotIn('data-feature="intelligence_today"', page)

    # ---- three-state: explicit false suppresses, no render, no claim ----
    def test_explicit_false_scalar_suppression(self):
        r, page, manifest = run_assemble(
            full_contract(self.tmp, {"intelligence_today": False}),
            self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="intelligence_today"', page)
        self.assertNotIn('<section class="intelligence-today"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "intelligence_today.updated"
                             for e in events))

    # ---- three-state: omitted (dict-form) -> assembler default-on policy ----
    def test_omitted_defaults_on_for_dict_form(self):
        r, page, manifest = run_assemble(
            full_contract(self.tmp, {}), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        # intelligence_today is a standard feature: on by default,
        # private by default
        self.assertIn('data-feature="intelligence_today"', page)
        sec_tag = page.split('<section class="intelligence-today"')[1].split(">")[0]
        self.assertIn('data-privacy-scope="private"', sec_tag)
        self.assertIn("No reports yet", page)
        # contacts is not standard: stays off unless flipped
        self.assertNotIn('data-feature="contacts"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "intelligence_today.updated"
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
        self.assertNotIn('data-feature="intelligence_today"', page)
    def test_day_one_minimal_contract(self):
        r, page, _ = run_assemble(
            full_contract(self.tmp, {"intelligence_today": True}),
            self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("refused", r.stdout)
        self.assertIn('data-feature="intelligence_today"', page)
        self.assertIn("No reports yet", page)  # useful section, no setup

    # ---- connections: the module gates nothing on them ----
    def test_connections_do_not_gate(self):
        off = {"muse": False, "github": False, "network": False,
               "nayanet": False}
        r1, page1, _ = run_assemble(
            full_contract(self.tmp, {"intelligence_today": True},
                          connections=off), self.tmp, self.assemble)
        self.assertEqual(r1.returncode, 0, r1.stdout + r1.stderr)
        self.assertIn('data-feature="intelligence_today"', page1)
        d2 = tempfile.mkdtemp(prefix="fit-c-")
        try:
            r2, page2, _ = run_assemble(
                full_contract(d2, {"intelligence_today": True}), d2, self.assemble)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(r2.returncode, 0)
        self.assertEqual(page1, page2)

    # ---- privacy dial: reports private by default, stamped per the dial ----
    def test_privacy_dial_scopes(self):
        for scope in ("private", "network", "public"):
            r, page, _ = run_assemble(
                full_contract(self.tmp, {"intelligence_today": True},
                              privacy=scope), self.tmp, self.assemble)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            sec_tag = page.split('<section class="intelligence-today"')[1].split(">")[0]
            self.assertIn('data-privacy-scope="%s"' % scope, sec_tag)
            # public is legitimate: no violation framing, same honest section
            self.assertIn("No reports yet", page)

    def test_privacy_bad_value_refused(self):
        # privacy is validated once per build (resolve_contract_context):
        # page-level fail-closed refusal
        r, page, _ = run_assemble(
            full_contract(self.tmp, {"intelligence_today": True},
                          privacy="everyone"), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_privacy", codes)
        self.assertNotIn('data-feature="intelligence_today"', page)

    # ---- consent line: READY needs no grant; CONNECTED needs consent ----
    def test_ready_works_with_all_grants_false(self):
        off = {"muse": False, "github": False, "network": False,
               "nayanet": False}
        r, page, manifest = run_assemble(
            full_contract(self.tmp, {"intelligence_today": True},
                          connections=off),
            self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="intelligence_today"', page)
        events = manifest.get("receipt", {}).get("events", [])
        it = [e for e in events
              if e.get("event") == "intelligence_today.updated"]
        self.assertTrue(it)
        # the receipt mirrors the evaluated grants
        self.assertEqual(it[0]["grants"], off)

    def test_capability_contract_carries_readiness_split(self):
        reg = json.load(open(os.path.join(
            self.tree, "functions", "registry.json")))
        entry = None
        for g in reg["groups"].values():
            for f in g.get("functions", []):
                if f.get("id") == "feature.intelligence_today":
                    entry = f
        self.assertIsNotNone(entry)
        # READY vs CONNECTED carried as top-level contract keys
        # (resolve_consent reads entry['ready'] / entry['connected'])
        self.assertTrue(entry.get("ready"))
        connected = entry.get("connected", [])
        self.assertTrue(connected)
        # each connected action names its grant key
        self.assertEqual(connected[0]["grant"], "network")
        self.assertEqual(connected[0]["declares"],
                         "contract.features.intelligence_today.external_sources")

    def test_connected_without_grant_refused(self):
        decl = {"enabled": True, "external_sources": True}
        for connections in (None,
                            {"muse": False, "github": False,
                             "network": False, "nayanet": False}):
            r, page, _ = run_assemble(
                full_contract(self.tmp, {"intelligence_today": decl},
                              connections=connections),
                self.tmp, self.assemble)
            self.assertEqual(r.returncode, 2, connections)
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            errs = [e for e in body["errors"]
                    if e.get("feature") == "feature.intelligence_today"]
            self.assertTrue(errs)
            self.assertIn("grant_required", [e["code"] for e in errs])
            # the refusal names the grant
            self.assertTrue(any("contract.connections.network" in e.get("detail", "")
                                for e in errs))
            self.assertNotIn('data-feature="intelligence_today"', page)

    def test_connected_with_grant_not_built(self):
        # explicit consent given, but the fetch is specified-not-built in
        # this stdlib-only module: honest refusal, never staged
        decl = {"enabled": True, "external_sources": True}
        connections = {"muse": False, "github": False, "network": True,
                       "nayanet": False}
        r, page, _ = run_assemble(
            full_contract(self.tmp, {"intelligence_today": decl},
                          connections=connections),
            self.tmp, self.assemble)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("connected_action_not_built", codes)
        self.assertNotIn("grant_required", codes)
        self.assertNotIn('data-feature="intelligence_today"', page)

    def test_bad_connections_block_refused(self):
        # connections are validated once per build (resolve_contract_context):
        # a non-object block is a page-level fail-closed refusal
        decl = {"enabled": True, "external_sources": True}
        r, _, _ = run_assemble(
            full_contract(self.tmp, {"intelligence_today": decl},
                          connections="yes please"),
            self.tmp, self.assemble)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_connections", codes)

    def test_ui_copy_never_claims_connected(self):
        r, page, _ = run_assemble(
            full_contract(self.tmp, {"intelligence_today": True}),
            self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        section = page.split('data-feature="intelligence_today"')[1].split(
            "</section>")[0]
        self.assertNotIn("connected", section.lower())

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = it_contract(self.tmp, dict(IT_DECL))
        _, page1, _ = run_assemble(contract, self.tmp, self.assemble)
        d2 = tempfile.mkdtemp(prefix="fit-b-")
        try:
            _, page2, _ = run_assemble(contract, d2, self.assemble)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())


if __name__ == "__main__":
    unittest.main(verbosity=2)

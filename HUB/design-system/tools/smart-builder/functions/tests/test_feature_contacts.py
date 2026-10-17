#!/usr/bin/env python3
"""Acceptance tests for feature.contacts (registry acceptance:
only_own_contacts_shown, list_renders).

Stdlib only (unittest + subprocess). Each test runs the real
assemble.py end-to-end against the real builder index:

  activation              -> contract-carried contacts render as a list
  explicit true/false     -> true renders; explicit false suppresses
  omitted                 -> off (contacts is not a standard feature)
  day-one                 -> minimal declaration renders useful output,
                             zero errors, no setup
  connections             -> the module gates nothing on connections
  privacy dial            -> the owner's people private by default,
                             stamped per the dial; unknown values refused
  gate                    -> no list unless the contract declares it
  sanitization            -> hostile contact links -> structured refusal (exit 2)
  mailto/tel              -> allowed (one tap away), verified against decl
  malformed declarations  -> fail closed, never improvised
  fallback (empty state)  -> enabled but no contacts -> "No contacts yet"
  privacy structure       -> only contract-carried people render; no one is
                             invented (the module has no I/O)
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

CONTACTS_DECL = {
    "enabled": True,
    "contacts": [
        {"name": "Ava Stone", "role": "Head baker",
         "link": "https://morning-crumb.nayanet.live/team/ava"},
        {"name": "Ben Okafor", "role": "Flour supplier",
         "link": "mailto:ben@example.com"},
        {"name": "Cara Diaz", "link": "tel:+15551234567"},
        {"name": "No Link", "role": "Friend"},
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


def contacts_contract(tmp, decl):
    c = json.load(open(SMOKE))
    c["title"] = "Contacts acceptance contract"
    c["features"] = {"contacts": decl}
    p = os.path.join(tmp, "contract.json")
    json.dump(c, open(p, "w"))
    return p


def full_contract(tmp, features, privacy=None, connections=None):
    """A customer contract with an explicit features dict plus optional
    top-level privacy/connections blocks."""
    c = json.load(open(SMOKE))
    c["title"] = "Contacts acceptance contract"
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


class FeatureContactsAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fcon-")
        self.tree = tree_with_status(self.tmp, "built")
        self.assemble = os.path.join(self.tree, "assemble.py")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- list_renders: every declared contact lands in the list ----
    def test_activation_via_contract(self):
        r, page, manifest = run_assemble(
            contacts_contract(self.tmp, dict(CONTACTS_DECL)), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="contacts"', page)
        self.assertIn('data-contacts-status="built"', page)
        self.assertIn('<ul class="contacts-list">', page)
        for name in ("Ava Stone", "Ben Okafor", "Cara Diaz", "No Link"):
            self.assertIn(name, page)
        self.assertIn("Head baker", page)
        # every rendered href is verified against the declaration
        # (L-2026-10-17-002) — mailto: and tel: included, nothing invented
        hrefs = re.findall(r'<a class="contact-name" href="([^"]+)"', page)
        self.assertEqual(sorted(hrefs), sorted(
            ["https://morning-crumb.nayanet.live/team/ava",
             "mailto:ben@example.com", "tel:+15551234567"]))
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["contacts"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "contacts.updated"
                            and e.get("feature") == "feature.contacts"
                            for e in events))

    # ---- only_own_contacts_shown: the list carries exactly the declared people
    def test_only_declared_people_render(self):
        r, page, _ = run_assemble(
            contacts_contract(self.tmp, dict(CONTACTS_DECL)), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        items = re.findall(r'<li class="contact">(.*?)</li>', page, re.S)
        self.assertEqual(len(items), 4)

    def test_xss_escaped(self):
        decl = {"enabled": True, "contacts": [
            {"name": "<script>alert(1)</script>", "role": "<b>x</b>",
             "link": "https://example.com/a"}]}
        r, page, _ = run_assemble(
            contacts_contract(self.tmp, decl), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        section = page.split('data-feature="contacts"')[1].split("</section>")[0]
        self.assertNotIn("<script>alert(1)</script>", section)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", section)

    # ---- gate: the page refuses to render contacts it was not given ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp, self.assemble)  # list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="contacts"', page)
        self.assertNotIn('<section class="contacts"', page)

    def test_refusal_when_declared_but_disabled(self):
        decl = dict(CONTACTS_DECL, enabled=False)
        r, page, manifest = run_assemble(
            contacts_contract(self.tmp, decl), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="contacts"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "contacts.updated"
                             for e in events))

    # ---- sanitization: hostile contact links are structured refusals ----
    def test_link_sanitization_refusals(self):
        bad = [
            "javascript:alert(1)",
            "JaVaScRiPt:alert(1)",
            "vbscript:msgbox(1)",
            "data:text/html;base64,PGI+",
            "ftp://example.com/x",
            "file:///etc/passwd",
            "//evil.example/x",
            "team/relative",
            "http:///no-host",
            "https://exa mple.com/x",
            "mailto:",            # empty address
            "mailto:ben @example.com",  # whitespace
        ]
        for link in bad:
            decl = {"enabled": True,
                    "contacts": [{"name": "Evil", "link": link}]}
            r, page, _ = run_assemble(
                contacts_contract(self.tmp, decl), self.tmp, self.assemble)
            self.assertEqual(r.returncode, 2, "link accepted: %r" % link)
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            codes = [e["code"] for e in body["errors"]]
            self.assertIn("unsafe_contacts_url", codes, link)
            self.assertNotIn('data-feature="contacts"', page)

    # ---- malformed declarations: fail closed, never improvised ----
    def test_malformed_entries_refused(self):
        cases = [
            {"enabled": True, "contacts": "not-a-list"},
            {"enabled": True, "contacts": [{"role": "x"}]},  # no name
            {"enabled": True, "contacts": [{"name": "  "}]},  # blank name
            {"enabled": True, "contacts": [{"name": 42}]},
            {"enabled": True, "contacts": [{"name": "A", "role": 7}]},
            {"enabled": True,
             "contacts": [{"name": "c%d" % i} for i in range(101)]},  # > max
            "yes please",
        ]
        for decl in cases:
            r, page, _ = run_assemble(
                contacts_contract(self.tmp, decl), self.tmp, self.assemble)
            self.assertEqual(r.returncode, 2, decl)
            self.assertNotIn('data-feature="contacts"', page)

    def test_malformed_code_is_structured(self):
        r, _, _ = run_assemble(
            contacts_contract(self.tmp, "yes please"), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 2)
        body = json.loads(r.stdout)
        codes = [e["code"] for e in body["errors"]]
        self.assertIn("bad_contacts_declaration", codes)

    # ---- empty state: enabled but no contacts -> honest empty state ----
    def test_fallback_empty_state(self):
        for decl in ({"enabled": True},
                     {"enabled": True, "contacts": []},
                     True):
            r, page, _ = run_assemble(
                contacts_contract(self.tmp, decl), self.tmp, self.assemble)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn('data-feature="contacts"', page)
            self.assertIn("contacts-empty", page)
            self.assertIn("No contacts yet", page)
            section = page.split('data-feature="contacts"')[1].split(
                "</section>")[0]
            self.assertNotIn("contacts-list", section)  # no invented people

    # ---- the general gate: an unbuilt breaker fails the contract closed ----
    def test_unbuilt_breaker_refused(self):
        tree = tree_with_status(self.tmp, "specified")
        asm = os.path.join(tree, "assemble.py")
        r, page, _ = run_assemble(
            contacts_contract(self.tmp, dict(CONTACTS_DECL)), self.tmp, asm)
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        con_errs = [e for e in errs if e.get("feature") == "feature.contacts"]
        self.assertTrue(con_errs, errs)
        self.assertIn("feature_not_built", [e["code"] for e in con_errs])
        self.assertNotIn('data-feature="contacts"', page)

    # ---- three-state: explicit false suppresses, no render, no claim ----
    def test_explicit_false_scalar_suppression(self):
        r, page, manifest = run_assemble(
            full_contract(self.tmp, {"contacts": False}), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="contacts"', page)
        self.assertNotIn('<section class="contacts"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "contacts.updated"
                             for e in events))

    # ---- three-state: omitted -> off (contacts is not a standard feature)
    def test_omitted_stays_off_for_dict_form(self):
        r, page, manifest = run_assemble(
            full_contract(self.tmp, {}), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="contacts"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "contacts.updated"
                             for e in events))

    # ---- day-one: the minimal declaration renders useful output, zero errors
    def test_day_one_minimal_contract(self):
        r, page, _ = run_assemble(
            full_contract(self.tmp, {"contacts": True}), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("refused", r.stdout)
        self.assertIn('data-feature="contacts"', page)
        self.assertIn("No contacts yet", page)  # useful section, no setup

    # ---- connections: the module gates nothing on them ----
    def test_connections_do_not_gate(self):
        off = {"muse": False, "github": False, "network": False,
               "nayanet": False}
        r1, page1, _ = run_assemble(
            full_contract(self.tmp, {"contacts": True},
                          connections=off), self.tmp, self.assemble)
        self.assertEqual(r1.returncode, 0, r1.stdout + r1.stderr)
        self.assertIn('data-feature="contacts"', page1)
        d2 = tempfile.mkdtemp(prefix="fcon-c-")
        try:
            r2, page2, _ = run_assemble(
                full_contract(d2, {"contacts": True}), d2, self.assemble)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(r2.returncode, 0)
        self.assertEqual(page1, page2)

    # ---- privacy dial: the owner's people private by default ----
    def test_privacy_dial_scopes(self):
        for scope in ("private", "network", "public"):
            r, page, _ = run_assemble(
                full_contract(self.tmp, {"contacts": True},
                              privacy=scope), self.tmp, self.assemble)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            sec_tag = page.split('<section class="contacts"')[1].split(">")[0]
            self.assertIn('data-privacy-scope="%s"' % scope, sec_tag)

    def test_privacy_bad_value_refused(self):
        # privacy is validated once per build (resolve_contract_context):
        # page-level fail-closed refusal
        r, page, _ = run_assemble(
            full_contract(self.tmp, {"contacts": True},
                          privacy="everyone"), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_privacy", codes)
        self.assertNotIn('data-feature="contacts"', page)

    # ---- consent line: READY needs no grant; CONNECTED needs consent ----
    def test_ready_works_with_all_grants_false(self):
        off = {"muse": False, "github": False, "network": False,
               "nayanet": False}
        r, page, manifest = run_assemble(
            full_contract(self.tmp, {"contacts": True}, connections=off),
            self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="contacts"', page)
        events = manifest.get("receipt", {}).get("events", [])
        con = [e for e in events if e.get("event") == "contacts.updated"]
        self.assertTrue(con)
        # the receipt mirrors the evaluated grants
        self.assertEqual(con[0]["grants"], off)

    def test_capability_contract_carries_readiness_split(self):
        reg = json.load(open(os.path.join(
            self.tree, "functions", "registry.json")))
        entry = None
        for g in reg["groups"].values():
            for f in g.get("functions", []):
                if f.get("id") == "feature.contacts":
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
                         "contract.features.contacts.sync_external")

    def test_connected_without_grant_refused(self):
        decl = {"enabled": True, "sync_external": True}
        for connections in (None,
                            {"muse": False, "github": False,
                             "network": False, "nayanet": False}):
            r, page, _ = run_assemble(
                full_contract(self.tmp, {"contacts": decl},
                              connections=connections),
                self.tmp, self.assemble)
            self.assertEqual(r.returncode, 2, connections)
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            errs = [e for e in body["errors"]
                    if e.get("feature") == "feature.contacts"]
            self.assertTrue(errs)
            self.assertIn("grant_required", [e["code"] for e in errs])
            # the refusal names the grant
            self.assertTrue(any("contract.connections.network" in e.get("detail", "")
                                for e in errs))
            self.assertNotIn('data-feature="contacts"', page)

    def test_connected_with_grant_not_built(self):
        # explicit consent given, but the sync is specified-not-built in
        # this stdlib-only module: honest refusal, never staged
        decl = {"enabled": True, "sync_external": True}
        connections = {"muse": False, "github": False, "network": True,
                       "nayanet": False}
        r, page, _ = run_assemble(
            full_contract(self.tmp, {"contacts": decl},
                          connections=connections),
            self.tmp, self.assemble)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("connected_action_not_built", codes)
        self.assertNotIn("grant_required", codes)
        self.assertNotIn('data-feature="contacts"', page)

    def test_bad_connections_block_refused(self):
        # connections are validated once per build (resolve_contract_context):
        # a non-object block is a page-level fail-closed refusal
        decl = {"enabled": True, "sync_external": True}
        r, _, _ = run_assemble(
            full_contract(self.tmp, {"contacts": decl},
                          connections="yes please"),
            self.tmp, self.assemble)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_connections", codes)

    def test_ui_copy_never_claims_connected(self):
        r, page, _ = run_assemble(
            full_contract(self.tmp, {"contacts": True}), self.tmp, self.assemble)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        section = page.split('data-feature="contacts"')[1].split(
            "</section>")[0]
        self.assertNotIn("connected", section.lower())

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = contacts_contract(self.tmp, dict(CONTACTS_DECL))
        _, page1, _ = run_assemble(contract, self.tmp, self.assemble)
        d2 = tempfile.mkdtemp(prefix="fcon-b-")
        try:
            _, page2, _ = run_assemble(contract, d2, self.assemble)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())


if __name__ == "__main__":
    unittest.main(verbosity=2)

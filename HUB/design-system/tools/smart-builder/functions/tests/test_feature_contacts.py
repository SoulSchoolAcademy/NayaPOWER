#!/usr/bin/env python3
"""Acceptance tests for feature.contacts (registry acceptance:
only_own_contacts_shown, list_renders).

Stdlib only (unittest + subprocess). Three levels, like the
intelligence_today suite:

  module level  -> decl_for / can_read / can_sync / sanitize_contact /
                   render_contacts on live bytes
  resolver level-> resolve() against the real registry (gates + binding)
  end-to-end    -> the real assemble.py against the real builder index

  only_own_contacts_shown -> a contact owned by another identity never
                             renders — not the name, not the handle, not
                             a teaser — even with every grant
  list_renders            -> the viewer's own contacts render full when the
                             contacts.read permission is granted; an honest
                             gated block names the permission when not
  empty_state_handled     -> declared with zero contacts renders the honest
                             empty line — never an empty section, never a
                             crash, never a fake contact
  activation gate         -> no contacts markup unless the contract
                             declares it
  sanitization            -> hostile contacts / bad declarations ->
                             structured refusals
  registry binding        -> contract cannot activate what the registry
                             does not mark 'built' (fail closed)
  determinism             -> same declaration + context -> same bytes
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
from feature_contacts import (ContactsRefusal, can_read, can_sync, decl_for,
                              render_contacts, sanitize_contact)
from resolver import ResolverRefusal, resolve

CONTACTS_DECL = {
    "enabled": True,
    "contacts": [
        {"name": "Ada Lovelace", "owner": "shawn",
         "handle": "ada@example.com", "notes": "Weekly sync.",
         "added": "2026-10-01"},
        {"name": "Grace Hopper", "owner": "shawn",
         "handle": "+1-555-0100", "notes": "Compiler questions.",
         "added": "2026-10-05"},
        {"name": "Stranger Danger", "owner": "stranger",
         "handle": "nope@example.com", "notes": "Not yours. Never shown.",
         "added": "2026-10-17"},
    ],
}


def full_context(**over):
    """All gates green: permission, network grant, requirements, identity."""
    c = {"contract": {"features": {"contacts": dict(CONTACTS_DECL)}},
         "connections": {"network": True},
         "privacy": "private",
         "granted_permissions": ["contacts.read"],
         "available": ["authenticated_identity", "contact_store"],
         "identity": {"id": "shawn"}}
    c.update(over)
    return c


def contacts_contract(tmp, decl, connections=None):
    """A customer contract: smoke contract with features as a breaker dict."""
    with open(SMOKE) as fh:
        c = json.load(fh)
    c["title"] = "Contacts acceptance contract"
    c["features"] = {"contacts": decl}
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


class ContactsModule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fcontacts-")

    # ---- F1: activation gate: nothing declared -> nothing rendered ----
    def test_not_declared_renders_nothing(self):
        for decl in (None, {}, {"enabled": False}):
            html = render_contacts(decl, "built", context=full_context())
            self.assertEqual(html, "", decl)
        # features carried as a list (contract-page) -> not declared
        self.assertIsNone(decl_for({"features": [["a", "b"]]}))

    # ---- F2: registry binding: fail closed unless the registry says built --
    def test_not_built_refuses(self):
        with self.assertRaises(ContactsRefusal) as cm:
            render_contacts(dict(CONTACTS_DECL), "specified",
                            context=full_context())
        self.assertEqual(cm.exception.code, "feature_not_built")

    # ---- decl_for shapes ----
    def test_decl_for_shapes(self):
        self.assertEqual(decl_for({"features": {"contacts": True}}),
                         {"enabled": True})
        d = {"enabled": True, "contacts": []}
        self.assertEqual(decl_for({"features": {"contacts": d}}), d)
        self.assertIsNone(decl_for({"features": {"contacts": False}}))
        self.assertIsNone(decl_for({"features": {}}))
        self.assertIsNone(decl_for({}))
        with self.assertRaises(ContactsRefusal) as cm:
            decl_for({"features": {"contacts": "yes please"}})
        self.assertEqual(cm.exception.code, "bad_contacts_declaration")

    # ---- sanitize_contact ----
    def test_sanitize_contact_accepts_good(self):
        c = sanitize_contact({"name": "Ada", "owner": "shawn"})
        self.assertEqual((c["name"], c["owner"], c["handle"], c["notes"],
                          c["added"]),
                         ("Ada", "shawn", "", "", ""))

    # ---- F7: malformed contacts -> structured refusal, never dropped ----
    def test_sanitize_contact_rejects_malformed(self):
        bad = [
            "not a dict",
            {"name": "", "owner": "shawn"},
            {"name": "  ", "owner": "shawn"},
            {"name": "Ada", "owner": "  "},
            {"name": "Ada"},
            {"name": "Ada", "owner": "shawn", "handle": 42},
            {"name": "Ada", "owner": "shawn", "notes": ["x"]},
            {"name": "Ada", "owner": "shawn", "added": 20261001},
        ]
        for b in bad:
            with self.assertRaises(ContactsRefusal) as cm:
                sanitize_contact(b)
            self.assertEqual(cm.exception.code, "bad_contact", b)

    # ---- F3: only_own_contacts_shown ----
    def test_only_own_contacts_shown(self):
        html = render_contacts(dict(CONTACTS_DECL), "built",
                               context=full_context())
        self.assertIn("Ada Lovelace", html)
        self.assertIn("ada@example.com", html)
        self.assertIn("Grace Hopper", html)
        self.assertNotIn("Stranger Danger", html)
        self.assertNotIn("nope@example.com", html)
        self.assertNotIn("Not yours. Never shown.", html)
        self.assertNotIn("stranger", html)

    # ---- no identity: no personal data renders, ever ----
    def test_no_identity_shows_nothing_personal(self):
        ctx = full_context()
        del ctx["identity"]
        html = render_contacts(dict(CONTACTS_DECL), "built", context=ctx)
        self.assertIn("Sign in to see your contacts", html)
        self.assertNotIn("Ada Lovelace", html)
        self.assertNotIn("ada@example.com", html)

    # ---- F5: empty_state_handled ----
    def test_empty_state(self):
        html = render_contacts({"enabled": True, "contacts": []},
                               "built", context=full_context())
        self.assertIn("No contacts yet", html)
        self.assertNotIn("contact-card", html.replace("contacts-", ""))

    # ---- F4: details are a permission question ----
    def test_read_gated_without_permission(self):
        ctx = full_context(granted_permissions=[])
        html = render_contacts(dict(CONTACTS_DECL), "built", context=ctx)
        self.assertIn("read your contacts", html)
        self.assertNotIn("ada@example.com", html)

    def test_bodies_render_with_permission(self):
        html = render_contacts(dict(CONTACTS_DECL), "built",
                               context=full_context())
        self.assertIn("Ada Lovelace", html)
        self.assertIn("ada@example.com", html)
        self.assertIn("Weekly sync.", html)

    # ---- F6: import/sync is the connected action: grant-gated, never dead --
    def test_sync_live_with_grant(self):
        html = render_contacts(dict(CONTACTS_DECL), "built",
                               context=full_context())
        self.assertIn('class="contacts-sync-btn"', html)
        self.assertIn("Import and sync contacts", html)
        self.assertIn('data-consent="connected"', html)

    def test_sync_gated_without_grant(self):
        ctx = full_context(connections={"network": False})
        html = render_contacts(dict(CONTACTS_DECL), "built", context=ctx)
        # contacts still render (permission granted) but import is gated
        self.assertIn("Ada Lovelace", html)
        self.assertNotIn('class="contacts-sync-btn"', html)
        self.assertIn("the network connection switched on for this page",
                      html)
        self.assertIn('data-consent="ready"', html)

    def test_truthy_grant_is_not_enough(self):
        ctx = full_context(connections={"network": "yes"})
        self.assertFalse(can_sync(ctx)[0])  # strict boolean, not truthy

    # ---- XSS: hostile strings are escaped, never executed ----
    def test_xss_escaped(self):
        evil = {"name": "<script>alert(1)</script>", "owner": "shawn",
                "handle": "<img src=x onerror=alert(2)>",
                "notes": "2026-10-17\"><b>bold</b>"}
        html = render_contacts(
            {"enabled": True, "contacts": [evil]}, "built",
            context=full_context())
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertNotIn("<img src=x onerror=alert(2)>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertIn("&lt;img src=x onerror=alert(2)&gt;", html)

    # ---- determinism ----
    def test_determinism(self):
        a = render_contacts(dict(CONTACTS_DECL), "built",
                            context=full_context())
        b = render_contacts(dict(CONTACTS_DECL), "built",
                            context=full_context())
        self.assertEqual(a, b)


class ContactsResolver(unittest.TestCase):
    def test_resolve_activates_with_all_gates_green(self):
        r = resolve("feature.contacts", full_context())
        self.assertTrue(r["activated"])
        self.assertEqual(r["function"], "feature.contacts")
        self.assertEqual(r["events"], ["contacts.viewed"])
        self.assertIn('class="contacts-sync-btn"', r["output"])
        self.assertIn('data-consent="connected"', r["output"])

    def test_resolve_undeclared_renders_honest_empty(self):
        c = full_context()
        c["contract"] = {"features": {}}  # contacts not declared
        r = resolve("feature.contacts", c)
        self.assertTrue(r["activated"])
        self.assertEqual(r["output"], "")

    def test_resolve_refuses_without_permission(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.contacts", full_context(granted_permissions=[]))
        e = cm.exception
        self.assertEqual(e.code, "permission_denied")
        self.assertEqual(e.missing, ["contacts.read"])
        self.assertIn("contacts.read", e.detail)

    def test_resolve_refuses_when_requirement_unmet(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.contacts", full_context(available=[]))
        e = cm.exception
        self.assertEqual(e.code, "requirement_unmet")
        self.assertEqual(e.missing, ["authenticated_identity",
                                     "contact_store"])
        self.assertIn("contact_store", e.detail)


class ContactsAssemble(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fcontacts-e2e-")

    def test_assemble_renders_honest_breaker_row(self):
        r, page, _ = run_assemble(
            contacts_contract(self.tmp, dict(CONTACTS_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.contacts"', page)
        self.assertIn('data-consent="ready"', page)

    def test_assemble_row_goes_connected_with_grant_on(self):
        r, page, _ = run_assemble(
            contacts_contract(self.tmp, dict(CONTACTS_DECL),
                              connections={"network": True}), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.contacts"', page)
        self.assertIn('data-consent="connected"', page)
        self.assertIn("connected (network)", page)

    def test_assemble_refuses_undeclared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="feature.contacts"', page)

    def test_assemble_refuses_bad_declaration(self):
        r, page, _ = run_assemble(
            contacts_contract(self.tmp, "yes please"), self.tmp)
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
                if f.get("id") == "feature.contacts":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        r, page, _ = run_assemble(
            contacts_contract(self.tmp, dict(CONTACTS_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)


if __name__ == "__main__":
    unittest.main(verbosity=2)

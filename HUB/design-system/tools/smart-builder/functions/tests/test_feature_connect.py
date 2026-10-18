#!/usr/bin/env python3
"""Acceptance tests for feature.connect (registry acceptance:
no_contact_without_consent, request_flow_tested, decline_respected).

Stdlib only (unittest + subprocess). Three levels, like the space suite:

  module level  -> decl_for / can_message / can_accept / render_connect
                   on live bytes
  resolver level-> resolve() against the real registry (gates + binding)
  end-to-end    -> the real assemble.py against the real builder index

  no_contact_without_consent -> pending / requested / declined people
                                 render NO message affordance — messaging
                                 is absent for them, never gated, even
                                 with every grant
  request_flow_tested        -> the incoming-request leg renders accept/
                                 decline affordances live when the
                                 connect.accept permission is granted,
                                 and an honest gated block when not
  decline_respected          -> a declined request renders the honest
                                 declined line; nothing re-requestable,
                                 nothing messageable
  activation gate            -> no connect markup unless the contract
                                 declares it
  sanitization               -> hostile people / bad declarations ->
                                 structured refusals
  registry binding           -> contract cannot activate what the registry
                                 does not mark 'built' (fail closed)
  determinism                -> same declaration + context -> same bytes
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
from feature_connect import (ConnectRefusal, can_accept, can_message,
                             decl_for, render_connect, sanitize_person)
from resolver import ResolverRefusal, resolve

CONNECT_DECL = {
    "enabled": True,
    "people": [
        {"name": "Ada Lovelace", "relation": "accepted"},
        {"name": "Bob Stone", "relation": "pending"},
        {"name": "Carla Reyes", "relation": "requested"},
        {"name": "Dana Fox", "relation": "declined"},
    ],
}


def full_context(**over):
    """All message gates green: permissions, nayanet grant, requirements."""
    c = {"contract": {"features": {"connect": dict(CONNECT_DECL)}},
         "connections": {"nayanet": True},
         "privacy": "private",
         "granted_permissions": ["connect.request", "connect.accept"],
         "available": ["authenticated_identity", "identity_directory",
                       "consent_records"]}
    c.update(over)
    return c


def connect_contract(tmp, decl, connections=None):
    """A customer contract: smoke contract with features as a breaker dict."""
    with open(SMOKE) as fh:
        c = json.load(fh)
    c["title"] = "Connect acceptance contract"
    c["features"] = {"connect": decl}
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


class ConnectModule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fconn-")

    # ---- activation gate: nothing declared -> nothing rendered ----
    def test_not_declared_renders_nothing(self):
        for decl in (None, {}, {"enabled": False}):
            html = render_connect(decl, "built", context=full_context())
            self.assertEqual(html, "", decl)
        # features carried as a list (contract-page) -> not declared
        self.assertIsNone(decl_for({"features": [["a", "b"]]}))

    # ---- registry binding: fail closed unless the registry says built ----
    def test_not_built_refuses(self):
        with self.assertRaises(ConnectRefusal) as cm:
            render_connect(dict(CONNECT_DECL), "specified",
                           context=full_context())
        self.assertEqual(cm.exception.code, "feature_not_built")

    # ---- decl_for shapes ----
    def test_decl_for_shapes(self):
        self.assertEqual(decl_for({"features": {"connect": True}}),
                         {"enabled": True})
        d = {"enabled": True, "people": []}
        self.assertEqual(decl_for({"features": {"connect": d}}), d)
        self.assertIsNone(decl_for({"features": {"connect": False}}))
        self.assertIsNone(decl_for({"features": {}}))
        self.assertIsNone(decl_for({}))
        with self.assertRaises(ConnectRefusal) as cm:
            decl_for({"features": {"connect": "yes please"}})
        self.assertEqual(cm.exception.code, "bad_connect_declaration")

    # ---- message is the connected action: live only when authorized ----
    def test_message_live_when_granted(self):
        decl = {"enabled": True, "people": [
            {"name": "Ada Lovelace", "relation": "accepted"}]}
        html = render_connect(decl, "built", context=full_context())
        self.assertIn('data-feature="connect"', html)
        self.assertIn('class="connect-message-btn"', html)
        self.assertIn('data-consent="connected"', html)
        self.assertIn('data-message-grant="nayanet"', html)
        self.assertIn("Message Ada Lovelace", html)
        # receipt hooks carry the registry's own events
        self.assertIn('data-receipt-events=', html)
        self.assertIn("connect.requested", html)
        self.assertIn("connect.accepted", html)
        self.assertIn("connect.declined", html)

    def test_gated_block_when_nayanet_not_strictly_true(self):
        decl = {"enabled": True, "people": [
            {"name": "Ada Lovelace", "relation": "accepted"}]}
        for conn in ({"nayanet": False}, {"nayanet": "yes"}):  # truthy != True
            ctx = full_context(connections=conn)
            allowed, missing = can_message(ctx)
            self.assertFalse(allowed, conn)
            html = render_connect(decl, "built", context=ctx)
            self.assertIn('data-consent="ready"', html, conn)
            self.assertIn("the NayaNET connection switched on for this page",
                          html, conn)
            self.assertNotIn('class="connect-message-btn"', html, conn)

    # ---- acceptance: no contact without consent — absent, never gated ----
    def test_non_contacts_render_no_message_affordance_even_granted(self):
        decl = {"enabled": True, "people": [
            {"name": "Bob Stone", "relation": "pending"},
            {"name": "Carla Reyes", "relation": "requested"},
            {"name": "Dana Fox", "relation": "declined"}]}
        html = render_connect(decl, "built", context=full_context())
        self.assertNotIn('class="connect-message-btn"', html)
        self.assertNotIn('class="connect-message-gated"', html)
        self.assertNotIn('data-consent="connected"', html)
        self.assertIn("Request sent to Bob Stone", html)
        self.assertIn("wants to connect with you", html)
        self.assertIn('data-consent="ready"', html)

    # ---- acceptance: decline is respected ----
    def test_declined_renders_honest_line_no_affordance(self):
        decl = {"enabled": True, "people": [
            {"name": "Dana Fox", "relation": "declined"}]}
        html = render_connect(decl, "built", context=full_context())
        self.assertIn("You declined Dana Fox", html)
        self.assertIn("nothing was shared", html)
        self.assertNotIn('class="connect-message-btn"', html)
        self.assertNotIn('class="connect-accept-btn"', html)

    # ---- acceptance: the request flow is tested both ways ----
    def test_request_flow_live_when_accept_granted(self):
        decl = {"enabled": True, "people": [
            {"name": "Carla Reyes", "relation": "requested"}]}
        html = render_connect(decl, "built", context=full_context())
        self.assertIn('class="connect-accept-btn"', html)
        self.assertIn('class="connect-decline-btn"', html)
        self.assertNotIn('class="connect-message-btn"', html)

    def test_request_flow_gated_when_accept_permission_missing(self):
        decl = {"enabled": True, "people": [
            {"name": "Carla Reyes", "relation": "requested"}]}
        ctx = full_context(granted_permissions=["connect.request"])
        allowed, missing = can_accept(ctx)
        self.assertFalse(allowed)
        self.assertTrue(missing)
        html = render_connect(decl, "built", context=ctx)
        self.assertNotIn('class="connect-accept-btn"', html)
        self.assertIn("your permission to accept connection requests",
                      html)
        self.assertNotIn('class="connect-message-btn"', html)

    # ---- acceptance: people render their declared relations ----
    def test_people_render_declared_content(self):
        html = render_connect(dict(CONNECT_DECL), "built",
                              context=full_context())
        for name in ("Ada Lovelace", "Bob Stone", "Carla Reyes", "Dana Fox"):
            self.assertIn(name, html)
        self.assertIn('data-relation="accepted"', html)
        self.assertIn('data-relation="pending"', html)
        self.assertIn('data-relation="requested"', html)
        self.assertIn('data-relation="declined"', html)
        self.assertIn("Connected", html)

    # ---- acceptance: malformed people are refused, never dropped ----
    def test_bad_people_refused(self):
        bad = [
            {},                                             # no fields
            {"relation": "accepted"},                       # missing name
            {"name": "   ", "relation": "accepted"},         # blank name
            {"name": "x"},                                  # missing relation
            {"name": "x", "relation": "galactic"},          # bad relation
            {"name": "x", "relation": "accepted", "note": 42},  # bad note
            "just a string",
            42,
        ]
        for person in bad:
            with self.assertRaises(ConnectRefusal, msg=repr(person)) as cm:
                sanitize_person(person)
            self.assertEqual(cm.exception.code, "bad_connect_person")

    # ---- sanitization: hostile content escaped ----
    def test_render_escapes_xss(self):
        decl = {"enabled": True, "people": [
            {"name": '<script>alert(1)</script>', "relation": "accepted",
             "note": "<img onerror=x>"}]}
        html = render_connect(decl, "built", context=full_context())
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertNotIn("<img onerror=x>", html)
        self.assertIn("&lt;script&gt;", html)

    # ---- determinism ----
    def test_determinism(self):
        a = render_connect(dict(CONNECT_DECL), "built",
                           context=full_context())
        b = render_connect(dict(CONNECT_DECL), "built",
                           context=full_context())
        self.assertEqual(a, b)


class ConnectResolver(unittest.TestCase):
    def test_resolve_activates_with_all_gates_green(self):
        r = resolve("feature.connect", full_context())
        self.assertTrue(r["activated"])
        self.assertEqual(r["function"], "feature.connect")
        self.assertEqual(r["events"], ["connect.requested",
                                       "connect.accepted",
                                       "connect.declined"])
        self.assertIn('class="connect-message-btn"', r["output"])
        self.assertIn('data-consent="connected"', r["output"])

    def test_resolve_undeclared_renders_honest_empty(self):
        c = full_context()
        c["contract"] = {"features": {}}  # connect not declared
        r = resolve("feature.connect", c)
        self.assertTrue(r["activated"])
        self.assertEqual(r["output"], "")

    def test_resolve_refuses_without_permission(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.connect", full_context(
                granted_permissions=["connect.request"]))
        e = cm.exception
        self.assertEqual(e.code, "permission_denied")
        self.assertEqual(e.missing, ["connect.accept"])
        self.assertIn("connect.accept", e.detail)
        self.assertIn("accept connection requests", e.detail)  # human words

    def test_resolve_refuses_when_requirement_unmet(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.connect", full_context(available=[]))
        e = cm.exception
        self.assertEqual(e.code, "requirement_unmet")
        self.assertEqual(e.missing, ["authenticated_identity",
                                     "identity_directory",
                                     "consent_records"])
        self.assertIn("identity_directory", e.detail)


class ConnectAssemble(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fconn-e2e-")

    def test_assemble_renders_honest_breaker_row(self):
        r, page, _ = run_assemble(
            connect_contract(self.tmp, dict(CONNECT_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.connect"', page)
        self.assertIn('data-consent="ready"', page)

    def test_assemble_row_goes_connected_with_grant_on(self):
        r, page, _ = run_assemble(
            connect_contract(self.tmp, dict(CONNECT_DECL),
                             connections={"nayanet": True}), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.connect"', page)
        self.assertIn('data-consent="connected"', page)
        self.assertIn("connected (nayanet)", page)

    def test_assemble_refuses_undeclared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="feature.connect"', page)

    def test_assemble_refuses_bad_declaration(self):
        r, page, _ = run_assemble(
            connect_contract(self.tmp, "yes please"), self.tmp)
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
                if f.get("id") == "feature.connect":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        r, page, _ = run_assemble(
            connect_contract(self.tmp, dict(CONNECT_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)


if __name__ == "__main__":
    unittest.main(verbosity=2)

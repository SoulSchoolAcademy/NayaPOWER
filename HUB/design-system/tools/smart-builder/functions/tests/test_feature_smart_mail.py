#!/usr/bin/env python3
"""Acceptance tests for feature.smart_mail (registry acceptance:
unauthorized_send_denied, authorized_send_tested, failure_state_visible,
receipt_persisted).

Stdlib only (unittest + subprocess). Two levels, like the cover suite:

  module level  -> decl_for / can_send / render_smart_mail on live bytes
  end-to-end    -> the real assemble.py against the real builder index,
                   the real resolver against the real registry

  unauthorized_send_denied -> resolver refuses without mail.send granted;
                              the module never renders a live send
                              affordance while any send gate is missing
  authorized_send_tested   -> resolve() activates with all gates green;
                              the render carries the send action + consent
                              metadata + receipt hook
  failure_state_visible    -> no message_service -> an honest visible
                              "can't send right now" state, never silent
  receipt_persisted        -> delivered entries carry their receipt event;
                              the receipt hook is present on the send block
  activation gate          -> no mail markup unless the contract declares it
  sanitization             -> hostile recipients / bad declarations ->
                              structured refusals (no send to garbage)
  registry binding         -> contract cannot activate what the registry does
                              not mark 'built' (fail closed)
  determinism              -> same declaration + context -> same bytes
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
from feature_smart_mail import (SmartMailRefusal, can_send, decl_for,
                                render_smart_mail, sanitize_recipient)
from resolver import ResolverRefusal, resolve

MAIL_DECL = {
    "enabled": True,
    "to": ["friend@example.com", {"name": "Bo", "address": "bo@example.com"}],
    "subject": "Tomorrow's bread run",
    "body": "Warm loaves at 8.",
    "drafts": [{"subject": "Draft one", "to": ["friend@example.com"]}],
    "delivered": [{"subject": "Yesterday's run",
                   "to": ["friend@example.com"],
                   "receipt": "mail.send.accepted"}],
}


def full_context(**over):
    """All send gates green: permissions, network grant, requirements."""
    c = {"contract": {"features": {"smart_mail": dict(MAIL_DECL)}},
         "connections": {"network": True},
         "privacy": "private",
         "granted_permissions": ["mail.compose", "mail.send"],
         "available": ["authenticated_identity", "recipient_authorization",
                       "message_service", "delivery_receipts"]}
    c.update(over)
    return c


def mail_contract(tmp, decl, connections=None):
    """A customer contract: smoke contract with features as a breaker dict."""
    c = json.load(open(SMOKE))
    c["title"] = "Smart Mail acceptance contract"
    c["features"] = {"smart_mail": decl}
    if connections:
        c["connections"] = connections
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


class SmartMailModule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fmail-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- activation gate: nothing declared -> nothing renders ----
    def test_refusal_when_not_declared(self):
        self.assertEqual(render_smart_mail(None, "built"), "")
        self.assertEqual(render_smart_mail({"enabled": False}, "built"), "")
        self.assertIsNone(decl_for({"features": {}}))
        self.assertIsNone(decl_for({"features": ["not", "a", "dict"]}))
        self.assertIsNone(decl_for({"features": {"smart_mail": False}}))

    def test_decl_shapes(self):
        self.assertEqual(decl_for({"features": {"smart_mail": True}}),
                         {"enabled": True})
        d = dict(MAIL_DECL)
        self.assertIs(decl_for({"features": {"smart_mail": d}}), d)

    def test_malformed_declaration_refused(self):
        with self.assertRaises(SmartMailRefusal) as cm:
            decl_for({"features": {"smart_mail": "yes please"}})
        self.assertEqual(cm.exception.code, "bad_smart_mail_declaration")

    # ---- sanitization: hostile recipients never pass ----
    def test_recipient_sanitization(self):
        good = sanitize_recipient({"name": "Bo", "address": "bo@example.com"})
        self.assertEqual(good, {"name": "Bo", "address": "bo@example.com"})
        self.assertEqual(sanitize_recipient("a@b.co")["address"], "a@b.co")
        bad = ["not-an-address", "a@b", "a b@c.com", "a@b..com",
               "javascript:alert(1)", "<script>@x.co", "a@c", 42,
               {"name": "x"}, ["a@b.co"]]
        for rec in bad:
            with self.assertRaises(SmartMailRefusal) as cm:
                sanitize_recipient(rec)
            self.assertEqual(cm.exception.code, "unsafe_recipient",
                             "recipient accepted: %r" % (rec,))

    def test_render_refuses_unsafe_recipient(self):
        decl = dict(MAIL_DECL, to=["evil@exam ple.com"])
        with self.assertRaises(SmartMailRefusal) as cm:
            render_smart_mail(decl, "built", context=full_context())
        self.assertEqual(cm.exception.code, "unsafe_recipient")

    # ---- unauthorized_send_denied: no live send without the grant ----
    def test_unauthorized_send_denied_resolver(self):
        c = full_context(granted_permissions=["mail.compose"])  # mail.send off
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.smart_mail", c)
        self.assertEqual(cm.exception.code, "permission_denied")
        self.assertIn("mail.send", cm.exception.missing)
        self.assertIn("send mail through Smart Mail", cm.exception.detail)

    def test_unauthorized_send_denied_module_gates(self):
        # each missing gate kills the send; the panel stays honest
        base = full_context()
        cases = [
            dict(base, granted_permissions=["mail.compose"]),
            dict(base, connections={"network": False}),
            dict(base, connections={"network": "yes"}),  # truthy != True
            dict(base, available=["authenticated_identity"]),
        ]
        for ctx in cases:
            allowed, missing = can_send(ctx)
            self.assertFalse(allowed)
            self.assertTrue(missing, ctx)
            html = render_smart_mail(dict(MAIL_DECL), "built", context=ctx)
            self.assertIn('data-feature="smart_mail"', html)
            self.assertIn('data-consent="ready"', html)
            self.assertIn("Send is ready but off.", html)
            self.assertNotIn('data-receipt-events', html)  # no receipt hook on a dead send
            self.assertNotIn('class="mail-send-btn"', html)

    # ---- authorized_send_tested: all gates green -> live send, honest ----
    def test_authorized_send_tested_resolver(self):
        r = resolve("feature.smart_mail", full_context())
        self.assertTrue(r["activated"])
        self.assertEqual(r["function"], "feature.smart_mail")
        self.assertIn("mail.send.requested", r["events"])
        self.assertIn("mail.send.accepted", r["events"])
        self.assertIn("mail.send.failed", r["events"])
        self.assertIn('data-feature="smart_mail"', r["output"])
        self.assertIn('data-consent="connected"', r["output"])
        self.assertIn('class="mail-send-btn"', r["output"])
        self.assertIn('data-receipt-events="mail.send.accepted mail.send.failed"',
                      r["output"])

    def test_authorized_render_carries_draft_and_recipients(self):
        html = render_smart_mail(dict(MAIL_DECL), "built",
                                 context=full_context())
        self.assertIn('value="friend@example.com, bo@example.com"', html)
        self.assertIn('value="Tomorrow&#x27;s bread run"', html)
        self.assertIn("Draft one", html)
        self.assertNotIn("No drafts yet", html)
        # identity fallback: no from given -> no crash, panel renders
        self.assertIn('data-mail-status="built"', html)

    # ---- failure_state_visible: no message service -> visible, not silent ----
    def test_failure_state_visible(self):
        ctx = full_context(available=["authenticated_identity",
                                      "recipient_authorization",
                                      "delivery_receipts"])
        allowed, missing = can_send(ctx)
        self.assertFalse(allowed)
        self.assertTrue(any("message service" in m for m in missing))
        html = render_smart_mail(dict(MAIL_DECL), "built", context=ctx)
        self.assertIn('data-feature="smart_mail"', html)
        self.assertIn("message service", html)  # the missing piece is named
        # ready parts still work: compose + drafts + mailbox render
        self.assertIn("mail-compose", html)
        self.assertIn("Draft one", html)

    # ---- receipt_persisted: receipts ride with delivered mail ----
    def test_receipt_persisted(self):
        html = render_smart_mail(dict(MAIL_DECL), "built",
                                 context=full_context())
        self.assertIn("Delivered · receipt mail.send.accepted", html)
        # a delivered entry with no receipt claims nothing
        decl = dict(MAIL_DECL, delivered=[{"subject": "x", "to": ["a@b.co"]}])
        html2 = render_smart_mail(decl, "built", context=full_context())
        self.assertIn("receipt pending", html2)
        self.assertNotIn("Delivered · receipt", html2)

    # ---- determinism: same declaration + context -> same bytes ----
    def test_determinism(self):
        ctx = full_context()
        h1 = hashlib.sha256(
            render_smart_mail(dict(MAIL_DECL), "built", context=ctx).encode()
        ).hexdigest()
        h2 = hashlib.sha256(
            render_smart_mail(dict(MAIL_DECL), "built", context=full_context()).encode()
        ).hexdigest()
        self.assertEqual(h1, h2)

    def test_lone_string_to_is_one_recipient(self):
        decl = dict(MAIL_DECL, to="solo@example.com")
        html = render_smart_mail(decl, "built", context=full_context())
        self.assertIn('value="solo@example.com"', html)


class SmartMailEndToEnd(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fmail-e2e-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_assemble_renders_honest_breaker_row(self):
        # network off -> the §7 row says ready, never connected
        r, page, manifest = run_assemble(
            mail_contract(self.tmp, dict(MAIL_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.smart_mail"', page)
        self.assertIn('data-consent="ready"', page)
        machine = json.loads(__import__("re").search(
            r'<pre id="machinejson">(.*?)</pre>', page, __import__("re").S).group(1))
        self.assertEqual(machine["features_status"]["smart_mail"], "built")
        self.assertEqual(
            machine["consent"]["feature.smart_mail"]["connected_gated"],
            ["send mail", "broadcast"])

    def test_assemble_connected_when_grant_on(self):
        r, page, _ = run_assemble(
            mail_contract(self.tmp, dict(MAIL_DECL),
                          connections={"network": True}), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.smart_mail"', page)
        self.assertIn('data-consent="connected"', page)
        self.assertIn("connected (network)", page)

    def test_assemble_refuses_undeclared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="feature.smart_mail"', page)

    def test_assemble_refuses_bad_declaration(self):
        r, page, _ = run_assemble(
            mail_contract(self.tmp, "yes please"), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_breaker_declaration", codes)

    def test_assemble_still_fails_closed_on_registry(self):
        # fail closed against a registry that still says specified:
        # a tree copy with the flip reverted refuses the contract.
        tree = os.path.join(self.tmp, "sbcopy")
        shutil.copytree(SB_DIR, tree)
        regp = os.path.join(tree, "functions", "registry.json")
        reg = json.load(open(regp))
        for g in reg["groups"].values():
            for f in g.get("functions", []):
                if f.get("id") == "feature.smart_mail":
                    f["status"] = "specified"
        json.dump(reg, open(regp, "w"), indent=1)
        r, page, _ = run_assemble(
            mail_contract(self.tmp, dict(MAIL_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        mail_errs = [e for e in errs if e.get("feature") == "feature.smart_mail"]
        self.assertTrue(mail_errs, errs)
        self.assertEqual(mail_errs[0]["code"], "feature_not_built")


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Acceptance tests for feature.smart_mail (registry acceptance:
unauthorized_send_denied, authorized_send_tested, failure_state_visible,
receipt_persisted).

Stdlib only (unittest + subprocess). Each test runs the real
assemble.py end-to-end against the real builder index:

  activation gate       -> no mail markup unless the contract declares it
  activation            -> declared + built -> mail panel with a real,
                           working mailto: compose control
  sanitization          -> hostile owner_email -> structured refusal (exit 2)
  fallback              -> declared without owner_email -> honest pending
                           state, never a dead control
  registry binding      -> contract cannot activate what the registry does
                           not mark 'built' (fail closed)
  determinism           -> same contract -> same bytes
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
ASSEMBLE = os.path.join(SB_DIR, "assemble.py")
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")

MAIL_DECL = {
    "enabled": True,
    "owner_email": "hello@morning-crumb.example",
    "label": "Write to us",
    "prefill_subject": "Hello from your page",
    "prefill_body": "Hi!\nLove the bread.",
}


def mail_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    c = json.load(open(SMOKE))
    c["title"] = "Smart mail acceptance contract"
    c["features"] = {"smart_mail": decl}
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


def mail_section(page):
    m = re.search(r'<section class="breaker breaker-mail".*?</section>',
                  page, re.S)
    return m.group(0) if m else ""


class FeatureSmartMailAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fsmail-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- activation: declared + built -> real working compose control ----
    def test_activation_via_contract(self):
        r, page, manifest = run_assemble(
            mail_contract(self.tmp, dict(MAIL_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_mail"', page)
        self.assertIn('data-smart_mail-status="built"', page)
        sec = mail_section(page)
        self.assertTrue(sec, "mail section missing")
        # the compose control is a real mailto: href, fully verified
        self.assertIn("mailto:hello@morning-crumb.example?", sec)
        self.assertIn("subject=Hello%20from%20your%20page", sec)
        self.assertIn("body=Hi%21%0ALove%20the%20bread.", sec)
        self.assertIn("Write to us", page)
        self.assertIn("hello@morning-crumb.example", sec)
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["smart_mail"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "smart_mail.wired"
                            and e.get("feature") == "feature.smart_mail"
                            for e in events), events)

    def test_bare_true_declaration_falls_back(self):
        r, page, _ = run_assemble(mail_contract(self.tmp, True), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_mail"', page)
        sec = mail_section(page)
        self.assertIn("has not published an address yet", sec)

    # ---- gate: the page refuses to render mail it was not given ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_mail"', page)
        self.assertNotIn("breaker-mail", page)

    def test_refusal_when_declared_but_disabled(self):
        decl = dict(MAIL_DECL, enabled=False)
        r, page, manifest = run_assemble(mail_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_mail"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "smart_mail.wired"
                             for e in events))

    # ---- three-state: explicit false suppresses silently (no render, no claim) ----
    def test_explicit_false_suppresses(self):
        r, page, manifest = run_assemble(
            mail_contract(self.tmp, False), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_mail"', page)
        self.assertNotIn("breaker-mail", page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "smart_mail.wired"
                             for e in events))
        # suppression is silent: no structured error, exit 0 (not a refusal)
        self.assertNotIn('"status": "refused"', r.stdout)

    def test_omitted_flag_defaults_on_under_active_gate(self):
        # Coverage gate ACTIVE (all 7 standard features built) -> omitted
        # = ON (default-on live). The module renders with its fallbacks.
        c = json.load(open(SMOKE))
        c["features"] = {}
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_mail"', page)
    def test_unsafe_email_refused(self):
        bad = [
            "not-an-email",
            "a b@c.com",
            "a@b",                    # no TLD
            "a@b.c",                  # 1-char TLD
            "<script>@x.com",
            "a@x.com?subject=hack",
            "a@x.com#frag",
            "a\x00@x.com",
            "@x.com",
            "a@.com",
            "javascript:alert(1)",
        ]
        for email in bad:
            decl = dict(MAIL_DECL, owner_email=email)
            r, page, _ = run_assemble(mail_contract(self.tmp, decl), self.tmp)
            self.assertEqual(r.returncode, 2, "email accepted: %r" % email)
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            codes = [e["code"] for e in body["errors"]]
            self.assertIn("unsafe_owner_email", codes, email)
            self.assertNotIn('data-feature="smart_mail"', page)

    def test_unsafe_text_refused(self):
        decl = dict(MAIL_DECL, label="Write\x01to us")
        r, page, _ = run_assemble(mail_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("unsafe_mail_text", codes)

    def test_markup_in_text_is_escaped_not_executed(self):
        decl = dict(MAIL_DECL, label="<script>alert(1)</script>")
        r, page, _ = run_assemble(mail_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)

    # ---- fallback: declared without owner_email -> honest, no dead control ----
    def test_fallback_when_no_email(self):
        decl = {"enabled": True, "label": "Write to us"}
        r, page, _ = run_assemble(mail_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_mail"', page)
        sec = mail_section(page)
        self.assertIn("has not published an address yet", sec)
        self.assertNotIn("<a", sec)      # no anchor at all: never a dead control
        self.assertNotIn('href=""', page)

    # ---- day-one: minimal contract, no connections, no privacy -> useful, zero errors ----
    def test_day_one_minimal_contract(self):
        c = json.load(open(SMOKE))
        c["features"] = {"smart_mail": True}  # nothing else configured
        self.assertNotIn("connections", c)
        self.assertNotIn("privacy", c)
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = mail_section(page)
        self.assertTrue(sec, "day-one panel missing")
        self.assertIn("Send mail", sec)  # something useful, not a broken shell
        self.assertNotIn("Traceback", r.stderr)

    # ---- consent line: READY vs CONNECTED ----
    # compose is READY (zero grants); broadcast is CONNECTED (grant-gated).
    # Requesting broadcast without the grant is a structured refusal naming
    # the missing grant — the consent line is a hard line, never a crash,
    # never a staged button.
    def test_broadcast_without_grant_refused(self):
        decl = dict(MAIL_DECL, broadcast=True)
        r, page, _ = run_assemble(mail_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 2)
        body = json.loads(r.stdout)
        self.assertEqual(body["status"], "refused")
        errs = [e for e in body["errors"] if e["code"] == "grant_required"]
        self.assertTrue(errs, body["errors"])
        self.assertIn("connections.nayanet", errs[0]["detail"])
        self.assertIn("ready but not connected", errs[0]["detail"])
        self.assertNotIn('data-feature="smart_mail"', page)

    def test_ready_copy_never_says_connected(self):
        # The ready panel (no connected action requested) must never claim
        # "connected" — the two states are never conflated.
        r, page, _ = run_assemble(mail_contract(self.tmp, True), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = mail_section(page)
        self.assertTrue(sec)
        self.assertNotIn("connected", sec.lower())
        self.assertNotIn("connect", sec.lower())

    def test_broadcast_connected_with_endpoint(self):
        c = json.load(open(SMOKE))
        c["features"] = {"smart_mail": dict(
            MAIL_DECL, broadcast=True,
            broadcast_url="https://hub.nayanet.live/broadcast/morning-crumb")}
        c["connections"] = {"muse": False, "github": False,
                            "network": False, "nayanet": True}
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, manifest = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = mail_section(page)
        self.assertIn('action="https://hub.nayanet.live/broadcast/morning-crumb"',
                      sec)
        self.assertIn("Broadcast to the network", sec)
        # the grant is real, so "connected" is accurate here — and mirrored
        self.assertIn("Connected via NayaNET", sec)
        events = manifest.get("receipt", {}).get("events", [])
        grant_events = [e for e in events
                        if e.get("event") == "smart_mail.broadcast.connected"]
        self.assertTrue(grant_events, events)
        self.assertEqual(grant_events[0]["grant"], "connections.nayanet")
        self.assertEqual(grant_events[0]["feature"], "feature.smart_mail")

    def test_broadcast_connected_without_endpoint(self):
        c = json.load(open(SMOKE))
        c["features"] = {"smart_mail": dict(MAIL_DECL, broadcast=True)}
        c["connections"] = {"nayanet": True}
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = mail_section(page)
        self.assertIn("no broadcast endpoint is configured", sec)
        self.assertNotIn("<form", sec)

    def test_unsafe_broadcast_url_refused(self):
        decl = dict(MAIL_DECL, broadcast=True,
                    broadcast_url="javascript:alert(1)")
        r, page, _ = run_assemble(mail_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("unsafe_broadcast_url", codes)

    def test_bad_privacy_dial_refused(self):
        c = json.load(open(SMOKE))
        c["features"] = {"smart_mail": dict(MAIL_DECL)}
        c["privacy"] = "everyone"
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_privacy_dial", codes)

    def test_bad_connections_block_refused(self):
        c = json.load(open(SMOKE))
        c["features"] = {"smart_mail": dict(MAIL_DECL)}
        c["connections"] = "yes please"
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_connections_block", codes)

    # ---- malformed declaration: fail closed, not improvised ----
    def test_malformed_declaration_refused(self):
        r, page, _ = run_assemble(
            mail_contract(self.tmp, "yes please"), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_smart_mail_declaration", codes)

    # ---- registry binding: the contract cannot out-claim the registry ----
    def test_registry_binding_refusal(self):
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
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)
        self.assertNotIn('data-feature="smart_mail"', page)

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = mail_contract(self.tmp, dict(MAIL_DECL))
        _, page1, _ = run_assemble(contract, self.tmp)
        d2 = tempfile.mkdtemp(prefix="fsmail-b-")
        try:
            _, page2, _ = run_assemble(contract, d2)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        h1 = hashlib.sha256(page1.encode()).hexdigest()
        h2 = hashlib.sha256(page2.encode()).hexdigest()
        self.assertEqual(h1, h2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

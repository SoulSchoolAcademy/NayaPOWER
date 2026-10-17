#!/usr/bin/env python3
"""Acceptance tests for feature.space (registry acceptance:
private_space_stays_private, join_flow_tested, member_list_correct).

Stdlib only (unittest + subprocess). Each test runs the real
assemble.py end-to-end against the real builder index:

  activation gate       -> no space markup unless the contract declares it
  activation            -> declared + built -> space panel with a real,
                           verified join link
  privacy               -> private spaces never leak member_count or join_url
  sanitization          -> hostile join_url -> structured refusal (exit 2)
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

SPACE_DECL = {
    "enabled": True,
    "name": "Morning Crumb Regulars",
    "description": "Gather around warm bread.",
    "visibility": "public",
    "join_url": "https://spaces.nayanet.live/morning-crumb-regulars/join",
    "member_count": 42,
}


def space_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    c = json.load(open(SMOKE))
    c["title"] = "Space acceptance contract"
    c["features"] = {"space": decl}
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


def space_section(page):
    m = re.search(r'<section class="breaker breaker-space".*?</section>',
                  page, re.S)
    return m.group(0) if m else ""


class FeatureSpaceAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fspace-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- activation: declared + built -> panel with a real join link ----
    def test_activation_via_contract(self):
        r, page, manifest = run_assemble(
            space_contract(self.tmp, dict(SPACE_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="space"', page)
        self.assertIn('data-space-status="built"', page)
        sec = space_section(page)
        self.assertTrue(sec, "space section missing")
        self.assertIn("Morning Crumb Regulars", sec)
        self.assertIn("Gather around warm bread.", sec)
        self.assertIn("Public space", sec)
        self.assertIn("42 members", sec)
        self.assertIn('href="https://spaces.nayanet.live/morning-crumb-regulars/join"',
                      sec)
        self.assertIn("Join the space", sec)
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["space"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "space.wired"
                            and e.get("feature") == "feature.space"
                            for e in events), events)

    def test_invite_visibility_labels_invite(self):
        decl = dict(SPACE_DECL, visibility="invite")
        r, page, _ = run_assemble(space_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = space_section(page)
        self.assertIn("Invite only", sec)
        self.assertIn("Request an invite", sec)

    def test_bare_true_falls_back_private(self):
        r, page, _ = run_assemble(space_contract(self.tmp, True), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = space_section(page)
        self.assertIn("Private space", sec)  # fail closed default
        self.assertNotIn("<a", sec)

    # ---- day-one: minimal contract, no connections, no privacy -> useful, zero errors ----
    def test_day_one_minimal_contract(self):
        c = json.load(open(SMOKE))
        c["features"] = {"space": True}  # nothing else configured
        self.assertNotIn("connections", c)
        self.assertNotIn("privacy", c)
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = space_section(page)
        self.assertTrue(sec, "day-one panel missing")
        self.assertIn("Private space", sec)  # fail-closed, honest, useful
        self.assertNotIn("Traceback", r.stderr)

    # ---- consent line: READY vs CONNECTED ----
    # link-mode join is READY (zero grants); connected join is CONNECTED.
    def test_connected_join_without_grant_refused(self):
        decl = dict(SPACE_DECL, join_mode="connected")
        r, page, _ = run_assemble(space_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 2)
        body = json.loads(r.stdout)
        self.assertEqual(body["status"], "refused")
        errs = [e for e in body["errors"] if e["code"] == "grant_required"]
        self.assertTrue(errs, body["errors"])
        self.assertIn("connections.nayanet", errs[0]["detail"])
        self.assertIn("ready but not connected", errs[0]["detail"])
        self.assertNotIn('data-feature="space"', page)

    def test_ready_copy_never_says_connected(self):
        # Ready states (private panel, link-mode join) never claim "connected".
        for decl in (True, dict(SPACE_DECL)):
            r, page, _ = run_assemble(space_contract(self.tmp, decl), self.tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            sec = space_section(page)
            self.assertTrue(sec)
            self.assertNotIn("connected", sec.lower())

    def test_connected_join_with_connection(self):
        c = json.load(open(SMOKE))
        c["features"] = {"space": dict(SPACE_DECL, join_mode="connected")}
        c["connections"] = {"nayanet": True}
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, manifest = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = space_section(page)
        self.assertIn('href="https://spaces.nayanet.live/morning-crumb-regulars/join"',
                      sec)
        # the grant is real, so "connected" is accurate — and mirrored
        self.assertIn("Connected via NayaNET", sec)
        events = manifest.get("receipt", {}).get("events", [])
        grant_events = [e for e in events
                        if e.get("event") == "space.join.connected"]
        self.assertTrue(grant_events, events)
        self.assertEqual(grant_events[0]["grant"], "connections.nayanet")

    def test_bad_join_mode_refused(self):
        decl = dict(SPACE_DECL, join_mode="teleport")
        r, page, _ = run_assemble(space_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_join_mode", codes)

    # ---- privacy dial: fills omitted visibility; explicit always wins ----
    def test_privacy_dial_public_by_legitimate_choice(self):
        c = json.load(open(SMOKE))
        decl = dict(SPACE_DECL)
        del decl["visibility"]  # omitted -> dial decides
        c["features"] = {"space": decl}
        c["privacy"] = "public"
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = space_section(page)
        # public is legitimate: badge + members + join link, no warnings
        self.assertIn("Public space", sec)
        self.assertIn("42 members", sec)
        self.assertIn("Join the space", sec)
        self.assertNotIn("violation", page.lower())

    def test_privacy_dial_network_maps_invite(self):
        c = json.load(open(SMOKE))
        decl = dict(SPACE_DECL)
        del decl["visibility"]
        c["features"] = {"space": decl}
        c["privacy"] = "network"
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Invite only", space_section(page))

    def test_explicit_visibility_beats_dial(self):
        c = json.load(open(SMOKE))
        c["features"] = {"space": dict(SPACE_DECL, visibility="private")}
        c["privacy"] = "public"  # dial says public; explicit private wins
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = space_section(page)
        self.assertIn("Private space", sec)
        self.assertNotIn("42 members", sec)

    def test_bad_privacy_dial_refused(self):
        c = json.load(open(SMOKE))
        c["features"] = {"space": dict(SPACE_DECL)}
        c["privacy"] = "everyone"
        p = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_privacy_dial", codes)

    # ---- gate: the page refuses to render a space it was not given ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="space"', page)
        self.assertNotIn("breaker-space", page)

    def test_refusal_when_declared_but_disabled(self):
        decl = dict(SPACE_DECL, enabled=False)
        r, page, manifest = run_assemble(space_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="space"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "space.wired" for e in events))

    # ---- three-state: explicit false suppresses silently (no render, no claim) ----
    def test_explicit_false_suppresses(self):
        r, page, manifest = run_assemble(
            space_contract(self.tmp, False), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="space"', page)
        self.assertNotIn("breaker-space", page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "space.wired" for e in events))
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
        self.assertIn('data-feature="space"', page)
    def test_private_space_stays_private(self):
        decl = dict(SPACE_DECL, visibility="private")
        r, page, _ = run_assemble(space_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = space_section(page)
        self.assertIn("Private space", sec)
        self.assertIn("Nothing inside this space is shown on this page", sec)
        self.assertNotIn("42", sec)
        self.assertNotIn("members", sec)
        self.assertNotIn("spaces.nayanet.live", sec)
        self.assertNotIn("<a", sec)

    # ---- no join_url -> honest pending state, never a dead control ----
    def test_no_join_url_no_dead_button(self):
        decl = dict(SPACE_DECL)
        del decl["join_url"]
        r, page, _ = run_assemble(space_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = space_section(page)
        self.assertIn("Ask the owner for an invite link", sec)
        self.assertNotIn("<a", sec)
        self.assertNotIn('href=""', page)

    # ---- sanitization: hostile join URLs are structured refusals ----
    def test_unsafe_join_url_refused(self):
        bad = [
            "javascript:alert(1)",
            "JaVaScRiPt:alert(1)",
            "data:text/html,<h1>x</h1>",
            "ftp://example.com/space",
            "//evil.example/join",
            "spaces/relative",
            "http:///no-host",
            "https://exa mple.com/join",
        ]
        for url in bad:
            decl = dict(SPACE_DECL, join_url=url)
            r, page, _ = run_assemble(space_contract(self.tmp, decl), self.tmp)
            self.assertEqual(r.returncode, 2, "url accepted: %r" % url)
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            codes = [e["code"] for e in body["errors"]]
            self.assertIn("unsafe_join_url", codes, url)
            self.assertNotIn('data-feature="space"', page)

    def test_bad_visibility_refused(self):
        decl = dict(SPACE_DECL, visibility="everyone")
        r, page, _ = run_assemble(space_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_space_visibility", codes)

    def test_bad_member_count_refused(self):
        for n in (-1, "many", True, 10 ** 10):
            decl = dict(SPACE_DECL, member_count=n)
            r, page, _ = run_assemble(space_contract(self.tmp, decl), self.tmp)
            self.assertEqual(r.returncode, 2, "count accepted: %r" % (n,))
            codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
            self.assertIn("bad_member_count", codes, n)

    def test_markup_in_name_is_escaped(self):
        decl = dict(SPACE_DECL, name='Regulars <img src=x onerror=alert(1)>')
        r, page, _ = run_assemble(space_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sec = space_section(page)
        self.assertNotIn("<img src=x", sec)
        self.assertIn("&lt;img", sec)

    # ---- malformed declaration: fail closed, not improvised ----
    def test_malformed_declaration_refused(self):
        r, page, _ = run_assemble(
            space_contract(self.tmp, "yes please"), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_space_declaration", codes)

    # ---- registry binding: the contract cannot out-claim the registry ----
    def test_registry_binding_refusal(self):
        tree = os.path.join(self.tmp, "sbcopy")
        shutil.copytree(SB_DIR, tree)
        regp = os.path.join(tree, "functions", "registry.json")
        reg = json.load(open(regp))
        for g in reg["groups"].values():
            for f in g.get("functions", []):
                if f.get("id") == "feature.space":
                    f["status"] = "specified"
        json.dump(reg, open(regp, "w"), indent=1)
        r, page, _ = run_assemble(
            space_contract(self.tmp, dict(SPACE_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)
        self.assertNotIn('data-feature="space"', page)

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = space_contract(self.tmp, dict(SPACE_DECL))
        _, page1, _ = run_assemble(contract, self.tmp)
        d2 = tempfile.mkdtemp(prefix="fspace-b-")
        try:
            _, page2, _ = run_assemble(contract, d2)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        h1 = hashlib.sha256(page1.encode()).hexdigest()
        h2 = hashlib.sha256(page2.encode()).hexdigest()
        self.assertEqual(h1, h2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Acceptance tests for feature.notifications (registry acceptance:
undeclared_event_ignored, unauthorized_audience_denied, permission_gate_enforced,
delivery_transport_named_blocked, optin_wires_to_existing_dom).

Stdlib only (unittest + subprocess). The work-tree registry carries the module
as 'specified' until the flip; each test therefore runs assemble from a
fixture copy of the smart-builder tree whose registry marks the module
'built' — except test_specified_registry_refuses, which proves the gate
refuses while specified. Every test runs the real assemble.py end-to-end
against the real builder index.
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
from html.parser import HTMLParser

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SB_DIR = os.path.normpath(os.path.join(TESTS_DIR, "..", ".."))
ASSEMBLE = os.path.join(SB_DIR, "assemble.py")
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")

NT_DECL = {
    "enabled": True,
    "audience": "subscribers",
    "events": [
        {"name": "new_post", "message": "Mara posted an update",
         "permission": "notify.new_post"},
        {"name": "new_note", "message": "A new smart note landed",
         "permission": "notify.new_note"},
    ],
    "grants": ["notify.new_post", "notify.new_note"],
}

FLIP_IDS = ("feature.notifications",)


def flip_registry(tree):
    regp = os.path.join(tree, "functions", "registry.json")
    reg = json.load(open(regp))
    for g in reg["groups"].values():
        for f in g.get("functions", []):
            if f.get("id") in FLIP_IDS:
                f["status"] = "built"
    json.dump(reg, open(regp, "w"), indent=2)


def nt_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    c = json.load(open(SMOKE))
    c["title"] = "Notifications acceptance contract"
    c["features"] = {"notifications": decl}
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


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.event_rows = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if a.get("data-event"):
            self.event_rows.add(a["data-event"])


class FeatureNotificationsAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fnt-")
        self.tree = os.path.join(self.tmp, "sbcopy")
        shutil.copytree(SB_DIR, self.tree)
        flip_registry(self.tree)
        self.assemble = os.path.join(self.tree, "assemble.py")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_decl(self, decl):
        return run_assemble(nt_contract(self.tmp, decl), self.tmp,
                            assemble=self.assemble, sb_dir=self.tree)

    # ---- explicit-true activation: declared events wire up ----
    def test_activation_via_contract(self):
        import copy
        r, page, manifest = self.run_decl(copy.deepcopy(NT_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="notifications"', page)
        self.assertIn('data-notifications-status="built"', page)
        self.assertIn("Mara posted an update", page)
        self.assertIn("A new smart note landed", page)
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["notifications"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        wired = [e for e in events if e.get("event") == "notification.wired"]
        self.assertEqual(len(wired), 2)
        self.assertTrue(all(e["permission_gate"] == "granted" for e in wired))
        blocked = [e for e in events
                   if e.get("event") == "notification.delivery_blocked"]
        self.assertEqual(len(blocked), 1)
        self.assertEqual(blocked[0]["transport"], "BLOCKED")

    # ---- explicit-false suppression + omitted: nothing renders ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp,
                                  assemble=self.assemble, sb_dir=self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="notifications"', page)

    def test_refusal_when_declared_but_disabled(self):
        import copy
        decl = copy.deepcopy(NT_DECL)
        decl["enabled"] = False
        r, page, manifest = self.run_decl(decl)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="notifications"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "notification.wired"
                             for e in events))

    # ---- permission_gate_enforced: ungranted permission -> refused ----
    def test_permission_denied_refused(self):
        import copy
        decl = copy.deepcopy(NT_DECL)
        decl["grants"] = ["notify.new_post"]  # new_note ungranted
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        codes = [e["code"] for e in errs]
        self.assertIn("notification_permission_denied", codes)
        self.assertNotIn('data-feature="notifications"', page)

    # ---- hostile inputs: unknown event, bad audience, empty message ----
    def test_unknown_event_refused(self):
        decl = {"enabled": True, "audience": "subscribers",
                "events": [{"name": "mind_read", "message": "x",
                            "permission": "p"}],
                "grants": ["p"]}
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_notification_event", codes)

    def test_bad_audience_refused(self):
        import copy
        decl = copy.deepcopy(NT_DECL)
        decl["audience"] = "everyone-on-the-internet"
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_notification_audience", codes)
        self.assertNotIn('data-feature="notifications"', page)

    def test_empty_message_refused(self):
        decl = {"enabled": True, "audience": "subscribers",
                "events": [{"name": "new_post", "message": "  ",
                            "permission": "p"}],
                "grants": ["p"]}
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_notification_event", codes)

    def test_message_injection_escaped(self):
        decl = {"enabled": True, "audience": "subscribers",
                "events": [{"name": "new_post",
                            "message": "<script>alert(1)</script>",
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
        self.assertIn("bad_notifications_declaration", codes)

    # ---- undeclared_event_ignored: only listed events wire ----
    def test_undeclared_event_ignored(self):
        import copy
        decl = copy.deepcopy(NT_DECL)
        decl["events"] = [decl["events"][0]]
        decl["grants"] = ["notify.new_post"]
        r, page, _ = self.run_decl(decl)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        p = IdCollector()
        p.feed(page)
        self.assertIn("new_post", p.event_rows)
        self.assertNotIn("broadcast", p.event_rows)
        self.assertNotIn("mention", p.event_rows)

    # ---- DAY-ONE TEST (Shawn 21:34Z): minimal contract -> useful render, zero errors ----
    def test_day_one_minimal_contract(self):
        r, page, manifest = self.run_decl(True)  # the smallest possible declaration
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("refused", r.stdout)
        self.assertNotIn("Traceback", r.stderr)
        self.assertIn('data-feature="notifications"', page)
        self.assertIn("Notifications", page)  # useful: heading + honest state
        self.assertIn("No notification events declared yet", page)
        self.assertIn("not connected", page)
        self.assertIn("connect a delivery transport to enable sending", page)  # honest from second one

    # ---- delivery_transport_named_blocked: never staged ----
    def test_delivery_transport_named_blocked(self):
        import copy
        r, page, manifest = self.run_decl(copy.deepcopy(NT_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        # the page says so in plain words
        self.assertIn("not connected", page)
        self.assertIn("connect a delivery transport to enable sending", page)
        # nothing claims a notification was sent
        low = page.lower()
        self.assertNotIn("notification sent", low)
        self.assertNotIn("notifications sent", low)
        events = manifest.get("receipt", {}).get("events", [])
        blocked = [e for e in events
                   if e.get("event") == "notification.delivery_blocked"][0]
        self.assertEqual(blocked["transport"], "BLOCKED")
        self.assertIn("delivery transport", blocked["transport_name"])
        self.assertEqual(blocked["grant_needed"], "transport.notify.send")

    # ---- fallback: enabled with no events -> honest empty state ----
    def test_fallback_no_events(self):
        r, page, manifest = self.run_decl({"enabled": True, "audience": "owner",
                                      "events": [], "grants": []})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="notifications"', page)
        self.assertIn("No notification events declared yet", page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "notification.wired"
                             for e in events))
        # the delivery block is still recorded — honesty even when empty
        self.assertTrue(any(e.get("event") == "notification.delivery_blocked"
                            for e in events))

    # ---- every control binds to DOM that exists (L-2026-10-17-004) ----
    def test_controls_bind_to_existing_dom(self):
        import copy
        r, page, _ = self.run_decl(copy.deepcopy(NT_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        p = IdCollector()
        p.feed(page)
        for need in ("nt-optin", "nt-save", "nt-status"):
            self.assertIn(need, p.ids, "opt-in control missing: %s" % need)
        self.assertEqual(p.event_rows, {"new_post", "new_note"})

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
                if fn.get("id") == "feature.notifications":
                    fn["status"] = "specified"
        json.dump(reg, open(regp, "w"), indent=2)
        r, page, _ = run_assemble(nt_contract(self.tmp, _copy.deepcopy(NT_DECL)), self.tmp,
                                  assemble=os.path.join(tree, "assemble.py"),
                                  sb_dir=tree)
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        mod_errs = [e for e in errs if e.get("feature") == "feature.notifications"]
        self.assertTrue(mod_errs, errs)
        self.assertEqual(mod_errs[0]["code"], "feature_not_built")
        self.assertNotIn('data-feature="notifications"', page)

    # ---- READY vs CONNECTED (Naya 3, 21:41Z): the missing grant is named ----
    def test_ready_connected_split_names_grant(self):
        import copy
        r, page, manifest = self.run_decl(copy.deepcopy(NT_DECL))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("connect a delivery transport to enable sending", page)
        events = manifest.get("receipt", {}).get("events", [])
        blocked = [e for e in events
                   if e.get("event") == "notification.delivery_blocked"]
        self.assertEqual(len(blocked), 1)
        self.assertEqual(blocked[0]["grant_needed"], "transport.notify.send")
        reg = json.load(open(os.path.join(self.tree, "functions", "registry.json")))
        entry = [f for g in reg["groups"].values() for f in g.get("functions", [])
                 if f.get("id") == "feature.notifications"][0]
        self.assertTrue(entry["ready"])
        self.assertEqual(entry["connected"]["grant"], "transport.notify.send")

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        import copy
        contract = nt_contract(self.tmp, copy.deepcopy(NT_DECL))
        _, page1, _ = run_assemble(contract, self.tmp,
                                    assemble=self.assemble, sb_dir=self.tree)
        d2 = tempfile.mkdtemp(prefix="fnt-b-")
        try:
            _, page2, _ = run_assemble(contract, d2,
                                        assemble=self.assemble, sb_dir=self.tree)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())


if __name__ == "__main__":
    unittest.main(verbosity=2)

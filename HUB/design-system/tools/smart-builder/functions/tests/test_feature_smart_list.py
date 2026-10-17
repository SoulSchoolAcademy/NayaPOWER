#!/usr/bin/env python3
"""Acceptance tests for feature.smart_list (registry acceptance:
contract_items_render, empty_state_honest, add_remove_wired).

Stdlib only (unittest + subprocess). Activation tests run the real
assemble.py end-to-end against a wired copy of the smart-builder tree
(all four Wave-D/E breakers flipped to 'built' in the copy, so the suite
is green regardless of the real registry's flip state — the real registry
flips only after these pass).

  contract_items_render -> the contract's items render: labels, details,
                           sanitized links; nothing invented, nothing dropped
  empty_state_honest    -> no items -> honest empty state, never a blank hole
  add_remove_wired      -> manage_endpoint declared -> working add form +
                           remove buttons (real POSTs); absent -> read-only
                           list, never a dead control
  three-state           -> explicit true = on; explicit false = off (no
                           render, no claim); omitted = assembler policy
                           (smart_list is STANDARD -> default ON)
  privacy dial          -> contract.privacy private|network|public drives
                           data-visibility + the badge; default private;
                           invalid dial -> structured refusal
  connections           -> smart_list needs none: works day one, zero
                           connections
  day-one               -> minimal contract -> useful render, zero errors
  sanitization          -> hostile URLs / bad kinds / bad items -> refusal
  registry binding      -> unbuilt breaker fails closed (exit 2)
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
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")

WAVE_BREAKERS = ("feature.naya_answers", "feature.scheduler",
                 "feature.broadcast", "feature.smart_list")

SL_DECL = {
    "enabled": True,
    "title": "Reading list",
    "kind": "notes",
    "items": [
        {"label": "Sourdough 101", "detail": "Ch. 3 — hydration",
         "url": "https://example.com/sourdough"},
        {"label": "Morning prep checklist", "detail": "Doors, ovens, playlist"},
        {"label": "Supplier contacts", "url": "https://example.com/suppliers"},
    ],
    "manage_endpoint": "https://lists.nayanet.live/morning-crumb",
}


def wired_tree(tmp):
    tree = os.path.join(tmp, "sb-wired")
    shutil.copytree(SB_DIR, tree)
    regp = os.path.join(tree, "functions", "registry.json")
    reg = json.load(open(regp))
    for g in reg["groups"].values():
        for f in g.get("functions", []):
            if f.get("id") in WAVE_BREAKERS:
                f["status"] = "built"
    json.dump(reg, open(regp, "w"), indent=1)
    return tree


def unbuilt_tree(tmp, target):
    tree = os.path.join(tmp, "sb-unbuilt")
    shutil.copytree(SB_DIR, tree)
    regp = os.path.join(tree, "functions", "registry.json")
    reg = json.load(open(regp))
    for g in reg["groups"].values():
        for f in g.get("functions", []):
            if f.get("id") in WAVE_BREAKERS:
                f["status"] = "built"
            if f.get("id") == target:
                f["status"] = "specified"
    json.dump(reg, open(regp, "w"), indent=1)
    return tree


def sl_contract(tmp, decl, privacy=None, connections=None):
    c = json.load(open(SMOKE))
    c["title"] = "Smart list acceptance contract"
    c["features"] = {"smart_list": decl}
    if privacy is not None:
        c["privacy"] = privacy
    # sync/share tests need the nayanet grant; pure-local tests pass {}.
    c["connections"] = {"nayanet": True} if connections is None else connections
    p = os.path.join(tmp, "contract.json")
    json.dump(c, open(p, "w"))
    return p


def run_assemble(contract, workdir, sbdir):
    out = os.path.join(workdir, "page.html")
    man = os.path.join(workdir, "page.manifest.json")
    assemble = os.path.join(sbdir, "assemble.py")
    r = subprocess.run(
        [sys.executable, assemble, "--contract", contract, "--index", INDEX,
         "--template", os.path.join(sbdir, "templates", "page.html"),
         "--out", out, "--manifest", man],
        capture_output=True, text=True, timeout=120)
    page = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
    manifest = {}
    if os.path.exists(man):
        with open(man) as fh:
            manifest = json.load(fh)
    return r, page, manifest


def list_html(page):
    m = re.search(r'<section class="smart-list.*?</section>', page, re.S)
    return m.group(0) if m else ""


class FeatureSmartListAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="fsl-")
        cls.tree = wired_tree(cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run(self, result=None):
        self.workdir = tempfile.mkdtemp(prefix="fsl-w-", dir=self.tmp)
        super().run(result)

    # ---- contract_items_render: the contract's data, nothing invented ----
    def test_activation_via_contract(self):
        r, page, manifest = run_assemble(
            sl_contract(self.tmp, dict(SL_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_list"', page)
        self.assertIn('data-smart-list-status="built"', page)
        self.assertIn('data-mode="connected"', page)
        self.assertIn('data-grant="connections.nayanet"', page)
        self.assertIn('data-kind="notes"', page)
        lst = list_html(page)
        self.assertTrue(lst, "smart list must render")
        self.assertIn("Reading list", lst)
        # every item present, nothing dropped, nothing invented
        self.assertIn("Sourdough 101", lst)
        self.assertIn("Ch. 3 — hydration", lst)
        self.assertIn('href="https://example.com/sourdough"', lst)
        self.assertIn("Morning prep checklist", lst)
        self.assertIn("Supplier contacts", lst)
        self.assertEqual(lst.count('<li class="slist-item">'), 3)
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["smart_list"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "smart_list.wired"
                            and e.get("feature") == "feature.smart_list"
                            for e in events))

    # ---- add_remove_wired: real controls only when the service is declared ----
    def test_add_remove_wired(self):
        r, page, _ = run_assemble(
            sl_contract(self.tmp, dict(SL_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        lst = list_html(page)
        self.assertIn('action="https://lists.nayanet.live/morning-crumb/items"',
                      lst)
        self.assertIn('name="label"', lst)
        self.assertIn('action="https://lists.nayanet.live/morning-crumb/remove"',
                      lst)
        self.assertEqual(lst.count('class="slist-remove"'), 3)

    def test_readonly_without_endpoint(self):
        decl = {k: v for k, v in SL_DECL.items() if k != "manage_endpoint"}
        r, page, _ = run_assemble(
            sl_contract(self.tmp, decl), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        lst = list_html(page)
        self.assertTrue(lst)
        self.assertNotIn("<form", lst)  # read-only: no dead controls
        self.assertIn("Sourdough 101", lst)

    # ---- empty_state_honest: empty is honest, never a blank hole ----
    def test_empty_state_honest(self):
        decl = {"enabled": True, "kind": "topics"}
        r, page, _ = run_assemble(
            sl_contract(self.tmp, decl), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        lst = list_html(page)
        self.assertTrue(lst)
        self.assertIn("No topics yet.", lst)
        self.assertNotIn('<li class="slist-item">', lst)

    def test_empty_message_override(self):
        decl = {"enabled": True, "empty_message": "Nothing here — add the first."}
        r, page, _ = run_assemble(
            sl_contract(self.tmp, decl), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Nothing here — add the first.", list_html(page))

    # ---- three-state: explicit true = on ----
    def test_explicit_true_is_on(self):
        r, page, _ = run_assemble(
            sl_contract(self.tmp, True), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_list"', page)

    # ---- three-state: explicit false = off (opt-out) ----
    def test_explicit_false_is_off(self):
        r, page, manifest = run_assemble(
            sl_contract(self.tmp, False), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_list"', page)
        self.assertNotIn('<section class="smart-list', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("feature") == "feature.smart_list"
                             for e in events))

    def test_enabled_false_dict_is_off(self):
        r, page, _ = run_assemble(
            sl_contract(self.tmp, {"enabled": False}), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_list"', page)

    # ---- three-state: omitted = assembler policy (STANDARD -> default ON) ----
    def test_omitted_defaults_on(self):
        # Coverage-gated default-on: the gate is ACTIVE (all 7 standard
        # features built) -> omitted = ON. The default title and honest
        # empty state render.
        c = json.load(open(SMOKE))
        c["title"] = "Omitted breaker contract"
        c["features"] = {}  # smart_list omitted; gate active -> ON
        p = os.path.join(self.workdir, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_list"', page)
        lst = list_html(page)
        self.assertIn("Smart list", lst)  # default title
        self.assertIn("No notes yet.", lst)  # honest empty state

    # ---- privacy dial: visibility follows contract.privacy ----
    def test_privacy_dial(self):
        for dial, label in (("private", "Private"),
                            ("network", "Network"),
                            ("public", "Public")):
            r, page, _ = run_assemble(
                sl_contract(self.tmp, dict(SL_DECL), privacy=dial),
                self.workdir, self.tree)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            lst = list_html(page)
            self.assertIn('data-visibility="%s"' % dial, lst)
            self.assertIn('slist-vis-%s' % dial, lst)
            self.assertIn(">%s<" % label, lst)

    def test_privacy_default_private(self):
        r, page, _ = run_assemble(
            sl_contract(self.tmp, dict(SL_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-visibility="private"', list_html(page))

    def test_privacy_invalid_refused(self):
        r, page, _ = run_assemble(
            sl_contract(self.tmp, dict(SL_DECL), privacy="everyone"),
            self.workdir, self.tree)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_privacy", codes)
        self.assertNotIn('data-feature="smart_list"', page)

    # ---- grant: manage_endpoint declared = CONNECTED demand (sync/share).
    # Without the grant -> structured grant_required refusal naming it.
    def test_grant_required_names_grant(self):
        r, page, _ = run_assemble(
            sl_contract(self.tmp, dict(SL_DECL), connections={}),
            self.workdir, self.tree)
        self.assertEqual(r.returncode, 2)
        body = json.loads(r.stdout)
        self.assertEqual(body["status"], "refused")
        errs = [e for e in body["errors"]
                if e.get("feature") == "feature.smart_list"]
        self.assertTrue(errs, body["errors"])
        self.assertEqual(errs[0]["code"], "grant_required")
        self.assertIn("connections.nayanet", errs[0]["detail"])
        self.assertNotIn('data-feature="smart_list"', page)

    # ---- readiness mirrored in the receipt ----
    def test_readiness_in_receipt(self):
        r, page, manifest = run_assemble(
            sl_contract(self.tmp, dict(SL_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        ready = manifest.get("receipt", {}).get("readiness", [])
        rec = [x for x in ready if x.get("feature") == "feature.smart_list"]
        self.assertTrue(rec, ready)
        self.assertEqual(rec[0]["mode"], "connected")
        self.assertEqual(rec[0]["grant"], "connections.nayanet")
        self.assertTrue(rec[0]["granted"])

    def test_readiness_ready_mode_in_receipt(self):
        decl = {k: v for k, v in SL_DECL.items() if k != "manage_endpoint"}
        r, page, manifest = run_assemble(
            sl_contract(self.tmp, decl, connections={}),
            self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        ready = manifest.get("receipt", {}).get("readiness", [])
        rec = [x for x in ready if x.get("feature") == "feature.smart_list"]
        self.assertTrue(rec, ready)
        self.assertEqual(rec[0]["mode"], "ready")
        self.assertFalse(rec[0]["granted"])

    # ---- connections: organize local = ready, zero connections needed ----
    def test_no_connections_needed(self):
        decl = {k: v for k, v in SL_DECL.items() if k != "manage_endpoint"}
        r, page, _ = run_assemble(
            sl_contract(self.tmp, decl, connections={}),
            self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_list"', page)
        self.assertIn('data-mode="ready"', page)
        self.assertIn("Sourdough 101", page)

    # ---- day-one: minimal contract -> useful render, zero errors ----
    def test_day_one(self):
        # Day-one minimal contract: the coverage gate is ACTIVE (all 7
        # standard features built) -> smart_list omitted = ON (default-on
        # live). The page renders cleanly WITH smart_list, zero errors,
        # zero failed fetches.
        c = json.load(open(SMOKE))
        c["title"] = "Day one"
        c["features"] = {}  # smart_list omitted; gate active -> ON
        p = os.path.join(self.workdir, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="smart_list"', page)

    # ---- gate: contract-page contracts (features as list) -> no breakers ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="smart_list"', page)

    # ---- sanitization: hostile input fails closed ----
    def test_bad_declarations_refused(self):
        bad_decls = [
            {"enabled": True, "kind": "carrier_pigeon"},
            {"enabled": True, "items": "not a list"},
            {"enabled": True, "items": [{"detail": "no label"}]},
            {"enabled": True,
             "items": [{"label": "i%d" % n} for n in range(501)]},
            {"enabled": True, "items": [{"label": "ok",
                                         "url": "javascript:alert(1)"}]},
            {"enabled": True, "manage_endpoint": "ftp://x/y"},
            {"enabled": True, "items": [{"label": "a\x00b"}]},
        ]
        for decl in bad_decls:
            r, page, _ = run_assemble(
                sl_contract(self.tmp, decl), self.workdir, self.tree)
            self.assertEqual(r.returncode, 2, "accepted: %r" % (decl,)[:80])
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            codes = [e["code"] for e in body["errors"]]
            self.assertTrue("bad_smart_list_declaration" in codes
                            or "unsafe_list_url" in codes, decl)
            self.assertNotIn('data-feature="smart_list"', page)

    def test_malformed_declaration_refused(self):
        r, page, _ = run_assemble(
            sl_contract(self.tmp, "a list please"), self.workdir, self.tree)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        # malformed declaration (string instead of dict/true/false)
        self.assertIn("bad_breaker_declaration", codes)

    # ---- registry binding: the contract cannot out-claim the registry ----
    def test_unbuilt_breaker_refused(self):
        tree = unbuilt_tree(self.tmp, "feature.smart_list")
        r, page, _ = run_assemble(
            sl_contract(self.tmp, dict(SL_DECL)), self.workdir, tree)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)
        self.assertNotIn('data-feature="smart_list"', page)

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = sl_contract(self.tmp, dict(SL_DECL))
        _, page1, _ = run_assemble(contract, self.workdir, self.tree)
        d2 = tempfile.mkdtemp(prefix="fsl-b-", dir=self.tmp)
        _, page2, _ = run_assemble(contract, d2, self.tree)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())


class FeatureSmartListUnits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, os.path.join(SB_DIR, "functions"))
        from feature_smart_list import (  # noqa
            validated_kind, validated_items, visibility_for, decl_for,
            SmartListRefusal, render_smart_list, mode_for, granted, GRANT)
        cls.validated_kind = staticmethod(validated_kind)
        cls.validated_items = staticmethod(validated_items)
        cls.visibility_for = staticmethod(visibility_for)
        cls.decl_for = staticmethod(decl_for)
        cls.SmartListRefusal = SmartListRefusal
        cls.render_smart_list = staticmethod(render_smart_list)
        cls.mode_for = staticmethod(mode_for)
        cls.granted = staticmethod(granted)
        cls.GRANT = GRANT

    @classmethod
    def tearDownClass(cls):
        sys.path.pop(0)

    def test_kind_validation(self):
        self.assertEqual(self.validated_kind({}), "notes")
        self.assertEqual(self.validated_kind({"kind": "CONTACTS"}), "contacts")
        with self.assertRaises(self.SmartListRefusal):
            self.validated_kind({"kind": "nope"})

    def test_items_validation(self):
        self.assertEqual(self.validated_items({}), [])
        items = self.validated_items(
            {"items": [{"label": "a"}, {"label": "b", "url": "https://x.y"}]})
        self.assertEqual(len(items), 2)
        with self.assertRaises(self.SmartListRefusal):
            self.validated_items({"items": [{"label": ""}]})
        with self.assertRaises(self.SmartListRefusal):
            self.validated_items(
                {"items": [{"label": "a", "url": "javascript:x"}]})

    def test_visibility(self):
        self.assertEqual(self.visibility_for({}), "private")
        self.assertEqual(self.visibility_for({"privacy": "public"}), "public")
        with self.assertRaises(self.SmartListRefusal):
            self.visibility_for({"privacy": "everyone"})

    def test_decl_for_three_state(self):
        self.assertIsNone(self.decl_for({"features": {}}))  # omitted
        self.assertIsNone(self.decl_for({"features": []}))  # contract-page
        self.assertEqual(self.decl_for({"features": {"smart_list": True}}),
                         {"enabled": True})  # explicit on
        self.assertEqual(self.decl_for({"features": {"smart_list": False}}),
                         {"enabled": False})  # explicit off
        with self.assertRaises(self.SmartListRefusal):
            self.decl_for({"features": {"smart_list": "yes"}})

    def test_render_off(self):
        self.assertEqual(self.render_smart_list({"enabled": False}, "built"), "")
        self.assertEqual(self.render_smart_list(None, "built"), "")

    def test_grant_and_mode(self):
        self.assertEqual(self.GRANT, "connections.nayanet")
        nctx = {"connections": {"nayanet": True}}
        self.assertTrue(self.granted(nctx))
        self.assertFalse(self.granted({}))
        d = {"enabled": True, "manage_endpoint": "https://l.example/x"}
        self.assertEqual(self.mode_for(d, nctx), "connected")
        self.assertEqual(self.mode_for(d, {}), "ready")
        self.assertEqual(self.mode_for({"enabled": True}, nctx), "ready")
        # never conflate: a blank endpoint is not a connected demand
        self.assertEqual(
            self.mode_for({"enabled": True, "manage_endpoint": "  "}, nctx),
            "ready")

    def test_grant_required_unit(self):
        with self.assertRaises(self.SmartListRefusal) as cm:
            self.render_smart_list(
                {"enabled": True, "manage_endpoint": "https://l.example/x"},
                "built", {"connections": {}})
        self.assertEqual(cm.exception.code, "grant_required")
        self.assertIn("connections.nayanet", cm.exception.detail)


if __name__ == "__main__":
    unittest.main(verbosity=2)

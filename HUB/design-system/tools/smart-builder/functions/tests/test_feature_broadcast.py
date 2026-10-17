#!/usr/bin/env python3
"""Acceptance tests for feature.broadcast (registry acceptance:
unauthorized_broadcast_denied, receipts_recorded, failure_state_visible).

Stdlib only (unittest + subprocess). Activation tests run the real
assemble.py end-to-end against a wired copy of the smart-builder tree
(registry status for the breaker flipped to 'built' in the copy, so the
suite is green regardless of the real registry's flip state — the real
registry flips only after these pass).

  unauthorized_broadcast_denied -> the contract must declare authorized:true
                           (the intake sets it only when the owner explicitly
                           says send). Anything else -> hard build refusal.
                           An unauthorized broadcast declaration never ships.
  receipts_recorded        -> the card carries the receipts shell, bound to
                           the contract-declared receipts endpoint when given
  failure_state_visible    -> authorized but no compose endpoint -> visible
                           not-wired state, no send button. Never a dead one.
  activation gate          -> no broadcast markup unless declared
  sanitization             -> hostile endpoints / bad channels -> refusal
  registry binding         -> unbuilt breaker fails closed (exit 2)
  determinism              -> same contract -> same bytes
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

BC_DECL = {
    "enabled": True,
    "authorized": True,
    "audience": "everyone following the bakery page",
    "channels": ["smart_mail", "spaces"],
    "compose_endpoint": "https://mail.nayanet.live/morning-crumb/broadcast",
    "receipts_endpoint": "https://mail.nayanet.live/morning-crumb/receipts",
}


# All four Wave-D/E breakers, flipped to built in the wired test copies so
# each suite tests its own module against the post-flip world (the real
# registry flips only after these pass).
WAVE_BREAKERS = ("feature.naya_answers", "feature.scheduler",
                 "feature.broadcast", "feature.smart_list")


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
    """Wired copy with exactly one breaker back at specified — the
    fail-closed surface: only the target may refuse."""
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


def bc_contract(tmp, decl, connections=None):
    c = json.load(open(SMOKE))
    c["title"] = "Broadcast acceptance contract"
    c["features"] = {"broadcast": decl}
    c["connections"] = {"network": True} if connections is None else connections
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


def card_html(page):
    m = re.search(r'<section class="bcast-card.*?</section>', page, re.S)
    return m.group(0) if m else ""


class FeatureBroadcastAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="fbc-")
        cls.tree = wired_tree(cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run(self, result=None):
        self.workdir = tempfile.mkdtemp(prefix="fbc-w-", dir=self.tmp)
        super().run(result)

    # ---- the wired compose card: real form, real endpoints ----
    def test_activation_via_contract(self):
        r, page, manifest = run_assemble(
            bc_contract(self.tmp, dict(BC_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="broadcast"', page)
        self.assertIn('data-broadcast-status="built"', page)
        card = card_html(page)
        self.assertTrue(card, "broadcast card must render")
        self.assertIn("everyone following the bakery page", card)
        self.assertIn("the owner authorized this", card)
        self.assertIn('<span class="bcast-chip">smart_mail</span>', card)
        self.assertIn('<span class="bcast-chip">spaces</span>', card)
        self.assertIn('data-channels="smart_mail,spaces"', card)
        self.assertIn('action="https://mail.nayanet.live/morning-crumb/broadcast"',
                      card)
        self.assertIn('name="subject"', card)
        self.assertIn('name="body"', card)
        self.assertIn("Send broadcast", card)
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["broadcast"], "built")

    # ---- receipts_recorded: the receipts shell binds the endpoint ----
    def test_receipts_shell(self):
        r, page, _ = run_assemble(
            bc_contract(self.tmp, dict(BC_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        card = card_html(page)
        self.assertIn("Delivery receipts", card)
        self.assertIn('data-receipts-endpoint='
                      '"https://mail.nayanet.live/morning-crumb/receipts"', card)

    # ---- unauthorized_broadcast_denied: THE gate ----
    def test_unauthorized_broadcast_refused(self):
        # Only boolean True authorizes. False, missing, or any truthy
        # non-True ("maybe", "true", 1) -> hard refusal.
        no_auth = {k: v for k, v in BC_DECL.items() if k != "authorized"}
        for decl in (dict(BC_DECL, authorized=False),
                     no_auth,
                     {"enabled": True, "authorized": "maybe"},
                     {"enabled": True, "authorized": "true"},
                     {"enabled": True, "authorized": 1}):
            r, page, _ = run_assemble(
                bc_contract(self.tmp, decl), self.workdir, self.tree)
            self.assertEqual(r.returncode, 2, "unauthorized accepted: %r" % (decl,))
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            codes = [e["code"] for e in body["errors"]]
            self.assertIn("unauthorized_broadcast", codes, decl)
            self.assertNotIn('data-feature="broadcast"', page)

    def test_authorized_true_string_is_not_authorization(self):
        # Belt and suspenders on the strict-True gate: the string "true"
        # is not the owner's authorization.
        decl = dict(BC_DECL, authorized="true")
        r, page, _ = run_assemble(
            bc_contract(self.tmp, decl), self.workdir, self.tree)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("unauthorized_broadcast", codes)

    # ---- failure_state_visible: authorized but not wired ----
    def test_not_wired_state(self):
        decl = {k: v for k, v in BC_DECL.items()
                if k not in ("compose_endpoint", "receipts_endpoint")}
        r, page, _ = run_assemble(
            bc_contract(self.tmp, decl), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        card = card_html(page)
        self.assertTrue(card)
        self.assertIn("bcast-card-off", card)
        self.assertIn("not wired yet", card)
        self.assertNotIn("Send broadcast", card)
        self.assertNotIn('method="post"', card)  # no dead send button

    # ---- gate: no broadcast markup unless the contract declares it ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="broadcast"', page)
        self.assertNotIn('<section class="bcast-card', page)

    def test_refusal_when_declared_but_disabled(self):
        decl = dict(BC_DECL, enabled=False)
        r, page, _ = run_assemble(
            bc_contract(self.tmp, decl), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="broadcast"', page)

    # ---- three-state: explicit false = off (no render, no claim,
    # and never trips the authorization gate) ----
    def test_explicit_false_is_off(self):
        r, page, manifest = run_assemble(
            bc_contract(self.tmp, False), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="broadcast"', page)
        self.assertNotIn('<section class="bcast-card', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("feature") == "feature.broadcast"
                             for e in events))

    def test_enabled_false_dict_is_off(self):
        # opted out without authorizing: must stay silent, not refuse
        r, page, _ = run_assemble(
            bc_contract(self.tmp, {"enabled": False}), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="broadcast"', page)

    # ---- three-state: omitted = assembler policy (not standard -> off) ----
    def test_omitted_stays_off(self):
        c = json.load(open(SMOKE))
        c["title"] = "Omitted breaker contract"
        c["features"] = {}  # broadcast omitted; not standard -> off
        c["connections"] = {"network": True}
        p = os.path.join(self.workdir, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="broadcast"', page)

    # ---- grant: compose_endpoint declared = CONNECTED demand.
    # Without the grant -> structured grant_required refusal naming it.
    def test_grant_required_names_grant(self):
        r, page, _ = run_assemble(
            bc_contract(self.tmp, dict(BC_DECL), connections={}),
            self.workdir, self.tree)
        self.assertEqual(r.returncode, 2)
        body = json.loads(r.stdout)
        self.assertEqual(body["status"], "refused")
        errs = [e for e in body["errors"]
                if e.get("feature") == "feature.broadcast"]
        self.assertTrue(errs, body["errors"])
        self.assertEqual(errs[0]["code"], "grant_required")
        self.assertIn("connections.network", errs[0]["detail"])
        self.assertNotIn('data-feature="broadcast"', page)

    # ---- connections: no endpoint, no grant -> honest connect panel ----
    def test_connect_panel_without_transport_demand(self):
        decl = {k: v for k, v in BC_DECL.items()
                if k not in ("compose_endpoint", "receipts_endpoint")}
        r, page, _ = run_assemble(
            bc_contract(self.tmp, decl, connections={}),
            self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="broadcast"', page)
        self.assertIn('data-mode="ready"', page)
        self.assertIn('data-grant="connections.network"', page)
        self.assertIn("connect your network to enable", page)
        card = card_html(page)
        self.assertNotIn("<form", card)  # no staged compose box

    # ---- readiness mirrored in the receipt ----
    def test_readiness_in_receipt(self):
        r, page, manifest = run_assemble(
            bc_contract(self.tmp, dict(BC_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        ready = manifest.get("receipt", {}).get("readiness", [])
        rec = [x for x in ready if x.get("feature") == "feature.broadcast"]
        self.assertTrue(rec, ready)
        self.assertEqual(rec[0]["mode"], "connected")
        self.assertEqual(rec[0]["grant"], "connections.network")
        self.assertTrue(rec[0]["granted"])

    # ---- day-one: minimal contract -> useful render, zero errors ----
    def test_day_one(self):
        c = json.load(open(SMOKE))
        c["title"] = "Day one"
        c["features"] = {"broadcast": {"enabled": True, "authorized": True}}
        c["connections"] = {"network": True}
        p = os.path.join(self.workdir, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="broadcast"', page)
        self.assertIn("not wired yet", page)

    # ---- sanitization: bad channels and hostile endpoints refused ----
    def test_bad_channels_refused(self):
        for channels in (["carrier_pigeon"], [], "smart_mail", [None]):
            decl = dict(BC_DECL, channels=channels)
            r, page, _ = run_assemble(
                bc_contract(self.tmp, decl), self.workdir, self.tree)
            self.assertEqual(r.returncode, 2, "channels accepted: %r" % (channels,))
            codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
            self.assertIn("bad_broadcast_declaration", codes, channels)
            self.assertNotIn('data-feature="broadcast"', page)

    def test_endpoint_sanitization_refusals(self):
        for field in ("compose_endpoint", "receipts_endpoint"):
            decl = dict(BC_DECL, **{field: "javascript:alert(1)"})
            r, page, _ = run_assemble(
                bc_contract(self.tmp, decl), self.workdir, self.tree)
            self.assertEqual(r.returncode, 2)
            codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
            self.assertIn("unsafe_broadcast_endpoint", codes)
            self.assertNotIn('data-feature="broadcast"', page)

    def test_malformed_declaration_refused(self):
        r, page, _ = run_assemble(
            bc_contract(self.tmp, "send it everywhere"), self.workdir, self.tree)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_broadcast_declaration", codes)

    # ---- registry binding: the contract cannot out-claim the registry ----
    def test_unbuilt_breaker_refused(self):
        tree = unbuilt_tree(self.tmp, "feature.broadcast")
        r, page, _ = run_assemble(
            bc_contract(self.tmp, dict(BC_DECL)), self.workdir, tree)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)
        self.assertNotIn('data-feature="broadcast"', page)

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = bc_contract(self.tmp, dict(BC_DECL))
        _, page1, _ = run_assemble(contract, self.workdir, self.tree)
        d2 = tempfile.mkdtemp(prefix="fbc-b-", dir=self.tmp)
        _, page2, _ = run_assemble(contract, d2, self.tree)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())


class FeatureBroadcastUnits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, os.path.join(SB_DIR, "functions"))
        from feature_broadcast import (  # noqa
            validated_channels, render_broadcast, BroadcastRefusal, decl_for,
            mode_for, granted, GRANT)
        cls.validated_channels = staticmethod(validated_channels)
        cls.render_broadcast = staticmethod(render_broadcast)
        cls.BroadcastRefusal = BroadcastRefusal
        cls.decl_for = staticmethod(decl_for)
        cls.mode_for = staticmethod(mode_for)
        cls.granted = staticmethod(granted)
        cls.GRANT = GRANT

    @classmethod
    def tearDownClass(cls):
        sys.path.pop(0)

    def test_channels_default(self):
        self.assertEqual(self.validated_channels({}), ("smart_mail",))

    def test_channels_deduped(self):
        self.assertEqual(
            self.validated_channels({"channels": ["feed", "feed", "spaces"]}),
            ("feed", "spaces"))

    def test_channels_rejected(self):
        for bad in (["irc"], [], "smart_mail", [123]):
            with self.assertRaises(self.BroadcastRefusal, msg=repr(bad)):
                self.validated_channels({"channels": bad})

    def test_authorized_gate_unit(self):
        # enabled + built, but not authorized -> hard refusal
        with self.assertRaises(self.BroadcastRefusal) as cm:
            self.render_broadcast({"enabled": True}, "built")
        self.assertEqual(cm.exception.code, "unauthorized_broadcast")
        with self.assertRaises(self.BroadcastRefusal) as cm:
            self.render_broadcast({"enabled": True, "authorized": "yes"}, "built")
        self.assertEqual(cm.exception.code, "unauthorized_broadcast")

    def test_render_not_declared(self):
        self.assertEqual(self.render_broadcast(None, "built"), "")
        self.assertEqual(self.render_broadcast({"enabled": False}, "built"), "")

    def test_decl_for_shapes(self):
        self.assertIsNone(self.decl_for({"features": []}))
        self.assertEqual(self.decl_for({"features": {"broadcast": True}}),
                         {"enabled": True})
        with self.assertRaises(self.BroadcastRefusal):
            self.decl_for({"features": {"broadcast": 42}})

    def test_grant_and_mode(self):
        self.assertEqual(self.GRANT, "connections.network")
        nctx = {"connections": {"network": True}}
        self.assertTrue(self.granted(nctx))
        self.assertFalse(self.granted({}))
        d = {"enabled": True, "authorized": True,
             "compose_endpoint": "https://m.example/c"}
        self.assertEqual(self.mode_for(d, nctx), "connected")
        self.assertEqual(self.mode_for(d, {}), "ready")
        self.assertEqual(
            self.mode_for({"enabled": True, "authorized": True}, nctx),
            "ready")
        # never conflate: a blank endpoint is not a connected demand
        self.assertEqual(
            self.mode_for({"enabled": True, "authorized": True,
                           "compose_endpoint": "  "}, nctx),
            "ready")


if __name__ == "__main__":
    unittest.main(verbosity=2)

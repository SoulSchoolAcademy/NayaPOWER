#!/usr/bin/env python3
"""Acceptance tests for feature.naya_answers (registry acceptance:
answer_uses_owner_kb, unknown_question_handled, failure_state_visible).

Stdlib only (unittest + subprocess). Activation tests run the real
assemble.py end-to-end against a wired copy of the smart-builder tree
(registry statuses for the breaker flipped to 'built' in the copy, so the
suite is green regardless of the real registry's flip state — the real
registry flips only after these pass).

  answer_uses_owner_kb  -> the widget names the contract-declared knowledge
                           source and carries NO canned answers (the module
                           never answers; the answer service does, at runtime)
  unknown_question_handled -> data-unknown-message always declared;
                           honest default names the KB and says she doesn't
                           know; contract can override
  failure_state_visible -> no answer endpoint -> visible disconnected state,
                           disabled form, honest copy. Never a dead control.
  activation gate       -> no widget unless the contract declares it
  sanitization          -> hostile endpoints -> structured refusal (exit 2)
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
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")

NA_DECL = {
    "enabled": True,
    "kb_source": "the bakery's GitHub knowledge base",
    "kb_ref": "morning-crumb/kb",
    "answers_endpoint": "https://answers.nayanet.live/morning-crumb",
    "greeting": "Ask me anything about the bakery.",
    "placeholder": "Type your question...",
}


# All four Wave-D/E breakers, flipped to built in the wired test copies so
# each suite tests its own module against the post-flip world (the real
# registry flips only after these pass).
WAVE_BREAKERS = ("feature.naya_answers", "feature.scheduler",
                 "feature.broadcast", "feature.smart_list")


def wired_tree(tmp):
    """A copy of the smart-builder tree with the Wave-D/E breakers marked
    built — the activation surface under test, without touching the real
    registry (which flips only after these tests pass)."""
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


def na_contract(tmp, decl, connections=None):
    """A customer contract: smoke contract with features as a breaker dict."""
    c = json.load(open(SMOKE))
    c["title"] = "Naya answers acceptance contract"
    c["features"] = {"naya_answers": decl}
    c["connections"] = {"github": True} if connections is None else connections
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


def widget_html(page):
    m = re.search(r'<section class="ask-naya.*?</section>', page, re.S)
    return m.group(0) if m else ""


class FeatureNayaAnswersAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="fna-")
        cls.tree = wired_tree(cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run(self, result=None):
        self.workdir = tempfile.mkdtemp(prefix="fna-w-", dir=self.tmp)
        super().run(result)

    # ---- answer_uses_owner_kb: KB named, zero canned answers ----
    def test_activation_via_contract(self):
        r, page, manifest = run_assemble(
            na_contract(self.tmp, dict(NA_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="naya_answers"', page)
        self.assertIn('data-naya-answers-status="built"', page)
        self.assertIn('data-mode="connected"', page)
        self.assertIn('data-grant="connections.github"', page)
        self.assertIn('data-answer-endpoint="https://answers.nayanet.live/morning-crumb"',
                      page)
        self.assertIn('data-kb-source="the bakery&#x27;s GitHub knowledge base"', page)
        self.assertIn("the bakery&#x27;s GitHub knowledge base", page)
        self.assertIn("Ask me anything about the bakery.", page)
        self.assertIn('action="https://answers.nayanet.live/morning-crumb"', page)
        self.assertIn('placeholder="Type your question..."', page)
        w = widget_html(page)
        self.assertTrue(w, "ask widget must render")
        # the module never answers: the answer slot is empty, no canned text
        self.assertIn('<div class="ask-answer" role="status" aria-live="polite"></div>', w)
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["naya_answers"], "built")
        # the build fires no runtime events (asked/answered are runtime)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("feature") == "feature.naya_answers"
                             for e in events))

    # ---- unknown_question_handled: the don't-know path is required ----
    def test_unknown_message_default(self):
        r, page, _ = run_assemble(
            na_contract(self.tmp, dict(NA_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        m = re.search(r'data-unknown-message="([^"]*)"', page)
        self.assertTrue(m, "data-unknown-message must always be declared")
        msg = m.group(1)
        self.assertIn("doesn&#x27;t know", msg)
        self.assertIn("bakery&#x27;s GitHub knowledge base", msg)

    def test_unknown_message_override(self):
        decl = dict(NA_DECL, unknown_message="No idea — ask the baker directly.")
        r, page, _ = run_assemble(
            na_contract(self.tmp, decl), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-unknown-message="No idea — ask the baker directly."', page)

    # ---- failure_state_visible: disconnected, disabled, honest ----
    def test_disconnected_state(self):
        decl = dict(NA_DECL)
        del decl["answers_endpoint"]
        r, page, _ = run_assemble(
            na_contract(self.tmp, decl), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="naya_answers"', page)
        w = widget_html(page)
        self.assertIn("ask-naya-off", w)
        self.assertIn("isn\u2019t connected yet", w)
        self.assertIn("disabled", w)
        self.assertNotIn("data-answer-endpoint", w)
        self.assertNotIn('method="post"', w)  # no live form without a service
        self.assertEqual(w.count("<form"), 1)  # the only form is disabled
        self.assertIn('aria-disabled="true"', w)

    # ---- gate: the page refuses to render Ask Naya it was not given ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="naya_answers"', page)
        self.assertNotIn('<section class="ask-naya', page)

    def test_refusal_when_declared_but_disabled(self):
        decl = dict(NA_DECL, enabled=False)
        r, page, _ = run_assemble(
            na_contract(self.tmp, decl), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="naya_answers"', page)

    # ---- three-state: explicit false = off (no render, no claim) ----
    def test_explicit_false_is_off(self):
        r, page, manifest = run_assemble(
            na_contract(self.tmp, False), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="naya_answers"', page)
        self.assertNotIn('<section class="ask-naya', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("feature") == "feature.naya_answers"
                             for e in events))

    def test_enabled_false_dict_is_off(self):
        r, page, _ = run_assemble(
            na_contract(self.tmp, {"enabled": False}), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="naya_answers"', page)

    # ---- three-state: omitted = assembler policy (not standard -> off) ----
    def test_omitted_stays_off(self):
        c = json.load(open(SMOKE))
        c["title"] = "Omitted breaker contract"
        c["features"] = {}  # naya_answers omitted; not standard -> off
        c["connections"] = {"github": True}
        p = os.path.join(self.workdir, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="naya_answers"', page)

    # ---- connections: endpoint declared = CONNECTED demand.
    # Without the grant -> structured grant_required refusal naming it.
    def test_grant_required_names_grant(self):
        r, page, _ = run_assemble(
            na_contract(self.tmp, dict(NA_DECL), connections={}),
            self.workdir, self.tree)
        self.assertEqual(r.returncode, 2)
        body = json.loads(r.stdout)
        self.assertEqual(body["status"], "refused")
        errs = [e for e in body["errors"]
                if e.get("feature") == "feature.naya_answers"]
        self.assertTrue(errs, body["errors"])
        self.assertEqual(errs[0]["code"], "grant_required")
        self.assertIn("connections.github", errs[0]["detail"])
        self.assertNotIn('data-feature="naya_answers"', page)

    # ---- connections: no endpoint, no grant -> honest connect panel ----
    def test_connect_panel_without_endpoint_demand(self):
        decl = {k: v for k, v in NA_DECL.items() if k != "answers_endpoint"}
        r, page, _ = run_assemble(
            na_contract(self.tmp, decl, connections={}),
            self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="naya_answers"', page)
        self.assertIn('data-mode="ready"', page)
        self.assertIn('data-grant="connections.github"', page)
        self.assertIn("connect GitHub to enable", page)
        w = widget_html(page)
        self.assertNotIn("<form", w)  # no staged question box
        self.assertNotIn("data-answer-endpoint", w)

    # ---- readiness mirrored in the receipt: mode, grant, granted ----
    def test_readiness_in_receipt(self):
        r, page, manifest = run_assemble(
            na_contract(self.tmp, dict(NA_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        ready = manifest.get("receipt", {}).get("readiness", [])
        rec = [x for x in ready if x.get("feature") == "feature.naya_answers"]
        self.assertTrue(rec, ready)
        self.assertEqual(rec[0]["mode"], "connected")
        self.assertEqual(rec[0]["grant"], "connections.github")
        self.assertTrue(rec[0]["granted"])

    # ---- day-one: minimal contract -> useful render, zero errors ----
    def test_day_one(self):
        c = json.load(open(SMOKE))
        c["title"] = "Day one"
        c["features"] = {"naya_answers": True}
        c["connections"] = {"github": True}
        p = os.path.join(self.workdir, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="naya_answers"', page)
        self.assertIn("Ask Naya", page)

    # ---- sanitization: hostile endpoints are structured refusals ----
    def test_endpoint_sanitization_refusals(self):
        bad = [
            "javascript:alert(1)",
            "JaVaScRiPt:alert(1)",
            "data:text/html,<script>alert(1)</script>",
            "ftp://example.com/answers",
            "file:///etc/passwd",
            "//evil.example/answers",
            "answers/relative",
            "http:///no-host",
            "https://exa mple.com/a",
        ]
        for url in bad:
            decl = dict(NA_DECL, answers_endpoint=url)
            r, page, _ = run_assemble(
                na_contract(self.tmp, decl), self.workdir, self.tree)
            self.assertEqual(r.returncode, 2, "url accepted: %r" % url)
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            codes = [e["code"] for e in body["errors"]]
            self.assertIn("unsafe_answers_endpoint", codes, url)
            self.assertNotIn('data-feature="naya_answers"', page)

    # ---- malformed declaration: fail closed, not improvised ----
    def test_malformed_declaration_refused(self):
        r, page, _ = run_assemble(
            na_contract(self.tmp, "yes please"), self.workdir, self.tree)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_naya_answers_declaration", codes)

    # ---- registry binding: the contract cannot out-claim the registry ----
    def test_unbuilt_breaker_refused(self):
        tree = unbuilt_tree(self.tmp, "feature.naya_answers")
        r, page, _ = run_assemble(
            na_contract(self.tmp, dict(NA_DECL)), self.workdir, tree)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)
        self.assertNotIn('data-feature="naya_answers"', page)

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = na_contract(self.tmp, dict(NA_DECL))
        _, page1, _ = run_assemble(contract, self.workdir, self.tree)
        d2 = tempfile.mkdtemp(prefix="fna-b-", dir=self.tmp)
        _, page2, _ = run_assemble(contract, d2, self.tree)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())


class FeatureNayaAnswersUnits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, os.path.join(SB_DIR, "functions"))
        from feature_naya_answers import (  # noqa
            unknown_message_for, sanitize_endpoint, NayaAnswersRefusal,
            decl_for, mode_for, granted, GRANT)
        cls.unknown_message_for = staticmethod(unknown_message_for)
        cls.sanitize_endpoint = staticmethod(sanitize_endpoint)
        cls.NayaAnswersRefusal = NayaAnswersRefusal
        cls.decl_for = staticmethod(decl_for)
        cls.mode_for = staticmethod(mode_for)
        cls.granted = staticmethod(granted)
        cls.GRANT = GRANT

    @classmethod
    def tearDownClass(cls):
        sys.path.pop(0)

    def test_unknown_default_names_kb(self):
        msg = self.unknown_message_for({"kb_source": "the wiki"})
        self.assertIn("doesn't know", msg)
        self.assertIn("the wiki", msg)

    def test_unknown_default_without_kb_source(self):
        msg = self.unknown_message_for({})
        self.assertIn("doesn't know", msg)
        self.assertIn("the owner's knowledge base", msg)

    def test_sanitize_endpoint_allows_https(self):
        self.assertEqual(
            self.sanitize_endpoint("https://a.example/q?a=1", "f"),
            "https://a.example/q?a=1")

    def test_sanitize_endpoint_rejects(self):
        for u in ("javascript:x", "data:text/plain,x", "/rel", "ftp://h/x"):
            with self.assertRaises(self.NayaAnswersRefusal, msg=u):
                self.sanitize_endpoint(u, "f")

    def test_decl_for_shapes(self):
        self.assertIsNone(self.decl_for({}))
        self.assertIsNone(self.decl_for({"features": []}))
        self.assertIsNone(self.decl_for({"features": {}}))  # omitted
        self.assertEqual(self.decl_for({"features": {"naya_answers": False}}),
                         {"enabled": False})  # explicit off
        self.assertEqual(self.decl_for({"features": {"naya_answers": True}}),
                         {"enabled": True})  # explicit on
        with self.assertRaises(self.NayaAnswersRefusal):
            self.decl_for({"features": {"naya_answers": "yes"}})

    def test_grant_and_mode(self):
        self.assertEqual(self.GRANT, "connections.github")
        gctx = {"connections": {"github": True}}
        self.assertTrue(self.granted(gctx))
        self.assertFalse(self.granted({}))
        self.assertFalse(self.granted({"connections": {"github": "yes"}}))
        d = {"enabled": True, "answers_endpoint": "https://a.example/q"}
        self.assertEqual(self.mode_for(d, gctx), "connected")
        self.assertEqual(self.mode_for(d, {}), "ready")
        self.assertEqual(self.mode_for({"enabled": True}, gctx), "ready")
        # never conflate: a blank endpoint is not a connected demand
        self.assertEqual(
            self.mode_for({"enabled": True, "answers_endpoint": "   "}, gctx),
            "ready")


if __name__ == "__main__":
    unittest.main(verbosity=2)

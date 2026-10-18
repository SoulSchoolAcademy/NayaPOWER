#!/usr/bin/env python3
"""Acceptance tests for feature.naya_answers (registry acceptance:
answer_uses_owner_kb, unknown_question_handled, failure_state_visible).

Stdlib only (unittest + subprocess). Three levels, like the community suite:

  module level  -> decl_for / can_ask / can_answer_live / sanitize_qa /
                   render_naya_answers on live bytes
  resolver level-> resolve() against the real registry (gates + binding)
  end-to-end    -> the real assemble.py against the real builder index

  answer_uses_owner_kb   -> rendered answers are byte-identical to the
                            declared KB entries, HTML-escaped — never
                            paraphrased, never invented
  unknown_question_handled -> a declared ask with no KB entry renders an
                            honest "not yet known" line, never a faked answer
  failure_state_visible  -> a down answer service renders a visible failure
                            note, never a silent empty panel
  activation gate        -> no answers markup unless the contract declares it
  sanitization           -> hostile Q&A / bad declarations -> structured
                            refusals
  registry binding       -> contract cannot activate what the registry does
                            not mark 'built' (fail closed)
  determinism            -> same declaration + context -> same bytes
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
from feature_naya_answers import (NayaAnswersRefusal, can_answer_live,
                                  can_ask, decl_for, render_naya_answers,
                                  sanitize_qa)
from resolver import ResolverRefusal, resolve

ANSWERS_DECL = {
    "enabled": True,
    "kb_answers": [
        {"question": "When is the next launch?",
         "answer": "The next launch is Friday at 9am."},
        {"question": "Who runs the team?",
         "answer": "Shawn runs the team."},
    ],
}

XSS_QA = {"question": "<script>alert(1)</script>",
          "answer": "A <b>bold</b> answer & more"}


def full_context(**over):
    """All gates green: the answers.ask permission, the three
    requirements, but NO muse grant (grant-gating is the module's own
    test surface — kept off here so the resolver-level output is the
    ready line, not the connected action)."""
    c = {"contract": {"features": {"naya_answers": dict(ANSWERS_DECL)}},
         "connections": {"muse": False, "github": True, "network": False},
         "privacy": "public",
         "granted_permissions": ["answers.ask"],
         "available": ["authenticated_identity", "github_kb_sync",
                       "answer_service"]}
    c.update(over)
    return c


def answers_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    with open(SMOKE) as fh:
        c = json.load(fh)
    c["title"] = "Naya answers acceptance contract"
    c["features"] = {"naya_answers": decl}
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


class NayaAnswersModule(unittest.TestCase):
    def test_not_declared_renders_nothing(self):
        # F8: activation gate — no markup unless declared
        self.assertEqual(render_naya_answers(None, "built", full_context()),
                         "")
        self.assertEqual(
            render_naya_answers({"enabled": False}, "built",
                                full_context()), "")

    def test_not_built_refuses(self):
        # F4: contract never activates an unbuilt capability
        with self.assertRaises(NayaAnswersRefusal) as cm:
            render_naya_answers(dict(ANSWERS_DECL), "specified",
                                full_context())
        self.assertEqual(cm.exception.code, "feature_not_built")

    def test_decl_for_shapes(self):
        self.assertEqual(decl_for({"features": {"naya_answers": True}}),
                         {"enabled": True})
        self.assertEqual(
            decl_for({"features": {"naya_answers": dict(ANSWERS_DECL)}})
            ["kb_answers"][0]["answer"],
            "The next launch is Friday at 9am.")
        self.assertIsNone(decl_for({"features": {}}))
        self.assertIsNone(decl_for({"features": ["naya_answers"]}))
        with self.assertRaises(NayaAnswersRefusal) as cm:
            decl_for({"features": {"naya_answers": "yes please"}})
        self.assertEqual(cm.exception.code, "bad_naya_answers_declaration")

    def test_sanitize_qa_bad(self):
        # F10: malformed Q&A -> structured refusal, never silently dropped
        for bad in ("nope", 42, {"question": "  "},
                    {"question": "q"}, {"question": "q", "answer": "  "},
                    {"question": "q", "answer": 42}):
            with self.assertRaises(NayaAnswersRefusal) as cm:
                sanitize_qa(bad)
            self.assertEqual(cm.exception.code, "bad_qa")

    def test_answer_uses_owner_kb(self):
        # F1: byte-identical answers — the rendered answer IS the declared
        # KB text. A paraphrase would be an answer the owner can't trust.
        out = render_naya_answers(dict(ANSWERS_DECL), "built",
                                  full_context())
        self.assertIn("The next launch is Friday at 9am.", out)
        self.assertIn("Shawn runs the team.", out)
        self.assertIn('data-naya-answers-status="built"', out)

    def test_xss_escaped(self):
        # F7: hostile content escapes, never executes
        out = render_naya_answers({"enabled": True, "kb_answers": [XSS_QA]},
                                  "built", full_context())
        self.assertNotIn("<script>alert(1)</script>", out)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", out)
        self.assertIn("&lt;b&gt;bold&lt;/b&gt;", out)

    def test_unknown_question_handled(self):
        # F5: declared ask with no KB entry says the gap — never faked
        ctx = full_context(pending_question="What is the meaning of life?")
        out = render_naya_answers(dict(ANSWERS_DECL), "built", ctx)
        self.assertIn("knowledge base yet", out)
        self.assertIn("What is the meaning of life?", out)
        # a KNOWN question gets no unknown line
        ctx2 = full_context(pending_question="When is the next launch?")
        out2 = render_naya_answers(dict(ANSWERS_DECL), "built", ctx2)
        self.assertNotIn("knowledge base yet", out2)

    def test_failure_state_visible(self):
        # F6: down service is said out loud, never a silent panel
        ctx = full_context(service_down=True)
        out = render_naya_answers(dict(ANSWERS_DECL), "built", ctx)
        self.assertIn('data-naya-answers-status="failed"', out)
        self.assertIn("answer service is down", out)
        self.assertNotIn("The next launch is Friday", out)  # no stale answers

    def test_permission_gate_gated_block(self):
        # F2: without answers.ask the ask box is honest, not dead
        ctx = full_context(granted_permissions=[])
        out = render_naya_answers(dict(ANSWERS_DECL), "built", ctx)
        self.assertIn("Asking is ready but off", out)
        self.assertIn("ask Naya questions against your knowledge base", out)
        allowed, missing = can_ask(ctx)
        self.assertFalse(allowed)
        self.assertEqual(missing,
                         ["ask Naya questions against your knowledge base"])

    def test_grant_gate_names_the_grant(self):
        # F3: without the muse grant, the live action is honestly gated
        out = render_naya_answers(dict(ANSWERS_DECL), "built",
                                  full_context())
        self.assertIn("Live answers are ready but off", out)
        self.assertIn("the Muse connection switched on for this page", out)
        self.assertNotIn('data-consent="connected"', out)
        self.assertFalse(can_answer_live(full_context()))
        self.assertTrue(can_answer_live(
            full_context(connections={"muse": True})))

    def test_connected_live_answer(self):
        ctx = full_context(connections={"muse": True})
        out = render_naya_answers(dict(ANSWERS_DECL), "built", ctx)
        self.assertIn("Answer via Muse", out)
        self.assertIn('data-consent="connected"', out)
        self.assertIn('data-answers-grant="muse"', out)
        # strict boolean: the string "true" is not the grant
        ctx2 = full_context(connections={"muse": "true"})
        self.assertFalse(can_answer_live(ctx2))

    def test_empty_kb_honest(self):
        out = render_naya_answers({"enabled": True}, "built",
                                  full_context())
        self.assertIn("No synced answers yet", out)

    def test_binding_and_receipt_events(self):
        out = render_naya_answers(dict(ANSWERS_DECL), "built",
                                  full_context())
        for ev in ("answers.asked", "answers.answered", "answers.failed"):
            self.assertIn(ev, out)

    def test_determinism(self):
        a = render_naya_answers(dict(ANSWERS_DECL), "built",
                                full_context())
        b = render_naya_answers(dict(ANSWERS_DECL), "built",
                                full_context())
        self.assertEqual(a, b)


class NayaAnswersResolver(unittest.TestCase):
    def test_resolve_activates_with_binding(self):
        r = resolve("feature.naya_answers", full_context())
        self.assertTrue(r["activated"])
        self.assertEqual(r["function"], "feature.naya_answers")
        self.assertEqual(r["events"],
                         ["answers.asked", "answers.answered",
                          "answers.failed"])
        self.assertIn('data-naya-answers-status="built"', r["output"])
        # answer_uses_owner_kb at the resolver level
        self.assertIn("The next launch is Friday at 9am.", r["output"])

    def test_resolve_refuses_when_permission_missing(self):
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.naya_answers",
                    full_context(granted_permissions=[]))
        e = cm.exception
        self.assertEqual(e.code, "permission_denied")
        self.assertEqual(e.missing, ["answers.ask"])
        self.assertIn("answers.ask", e.detail)
        self.assertIn("ask Naya questions against your knowledge base",
                      e.detail)

    def test_resolve_refuses_when_requirement_unmet(self):
        # F9: the github_kb_sync requirement fails closed before the module
        with self.assertRaises(ResolverRefusal) as cm:
            resolve("feature.naya_answers", full_context(available=[]))
        e = cm.exception
        self.assertEqual(e.code, "requirement_unmet")
        self.assertEqual(e.missing,
                         ["authenticated_identity", "github_kb_sync",
                          "answer_service"])
        self.assertIn("github_kb_sync", e.detail)

    def test_resolve_propagates_bad_declaration_as_module_refusal(self):
        c = full_context()
        c["contract"] = {"features": {"naya_answers": "yes please"}}
        with self.assertRaises(NayaAnswersRefusal) as cm:
            resolve("feature.naya_answers", c)
        self.assertEqual(cm.exception.code, "bad_naya_answers_declaration")


class NayaAnswersAssemble(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fanswers-e2e-")

    def test_assemble_renders_honest_breaker_row(self):
        r, page, _ = run_assemble(
            answers_contract(self.tmp, dict(ANSWERS_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="feature.naya_answers"', page)
        # no muse grant in the contract assembly path: consent is "ready"
        self.assertIn('data-consent="ready"', page)

    def test_assemble_refuses_undeclared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="feature.naya_answers"', page)

    def test_assemble_refuses_bad_declaration(self):
        r, page, _ = run_assemble(
            answers_contract(self.tmp, "yes please"), self.tmp)
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
                if f.get("id") == "feature.naya_answers":
                    f["status"] = "specified"
        with open(regp, "w") as fh:
            json.dump(reg, fh, indent=1)
        r, page, _ = run_assemble(
            answers_contract(self.tmp, dict(ANSWERS_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)

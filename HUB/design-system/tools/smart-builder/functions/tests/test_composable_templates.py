#!/usr/bin/env python3
"""Acceptance tests for composable templates (assembler v1.3).

Stdlib only (unittest + subprocess). Unit tests exercise resolve_templates()
directly; end-to-end tests run the real assemble.py against the real builder
index, following the test_feature_cover.py pattern.

Covered:
  union_order            -> two templates merge to the ordered section union
  first_wins             -> section-name collision: first template's content wins
  override_honored       -> explicit overrides map names the section winner
  override refusals      -> unknown section / unknown template / template
                            missing the section -> structured refusal (exit 2)
  prune_wins             -> explicit false in ANY template disables the feature
  backward_compat        -> "template-personal" == ["template-personal"]
  unknown_template       -> structured refusal, fail closed (exit 2)
  bad shapes             -> mixed/empty/malformed -> structured refusal
  display_passthrough    -> [badge, name, desc] triples keep the old render path
  determinism            -> same contract -> same composition, same page bytes
  contract_wins          -> the contract's own features beat composed features
  e2e flip               -> composed cover:true renders cover markup
  e2e prune              -> composed cover:false suppresses it (opt-out recorded)
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
sys.path.insert(0, SB_DIR)
from assemble import resolve_templates, apply_composition  # noqa: E402

INDEX = os.path.normpath(os.path.join(
    SB_DIR, "..", "..", "library", "catalog", "builder-index-v1.json"))
ASSEMBLE = os.path.join(SB_DIR, "assemble.py")
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")

# Two template shapes with one colliding section ("hero") and features that
# exercise the prune-wins law. Unit-level only: smart_mail / smart_spaces are
# registry-'specified', so they never reach the live assembler in e2e tests.
SHAPES = {
    "template-personal": {
        "name": "Personal page",
        "sections": {
            "hero": {"title": "Personal hero", "blurb": "p-hero"},
            "about": {"title": "About me", "blurb": "p-about"},
            "links": {"title": "Links", "blurb": "p-links"},
        },
        "features": {"cover": True, "smart_mail": True},
    },
    "template-business": {
        "name": "Business landing",
        "sections": {
            "hero": {"title": "Business hero", "blurb": "b-hero"},
            "hours": {"title": "Hours", "blurb": "b-hours"},
            "contact": {"title": "Contact", "blurb": "b-contact"},
        },
        "features": {"cover": False, "smart_spaces": True},
    },
}

# E2E shapes: only the registry-built cover breaker, so the fail-closed
# registry gate stays green and the tests measure composition, not gating.
E2E_SHAPES = {
    "template-personal": {
        "name": "Personal page",
        "sections": {
            "hero": {"title": "Personal hero", "blurb": "p-hero"},
            "about": {"title": "About me", "blurb": "p-about"},
        },
        "features": {"cover": True},
    },
    "template-business": {
        "name": "Business landing",
        "sections": {
            "hero": {"title": "Business hero", "blurb": "b-hero"},
            "hours": {"title": "Hours", "blurb": "b-hours"},
        },
        "features": {"cover": False},
    },
}


def base_contract():
    c = {"templates": ["template-personal", "template-business"],
         "template_shapes": json.loads(json.dumps(SHAPES))}
    return c


def codes(problems):
    return [p["code"] for p in problems]


class ResolveUnit(unittest.TestCase):
    # ---- sections: union in listed order ----
    def test_union_order(self):
        comp, problems = resolve_templates(base_contract())
        self.assertEqual(problems, [])
        self.assertEqual([s["name"] for s in comp["sections"]],
                         ["hero", "about", "links", "hours", "contact"])
        self.assertEqual(comp["templates"],
                         ["template-personal", "template-business"])

    def test_union_order_follows_listed_order(self):
        c = base_contract()
        c["templates"] = ["template-business", "template-personal"]
        comp, problems = resolve_templates(c)
        self.assertEqual(problems, [])
        self.assertEqual([s["name"] for s in comp["sections"]],
                         ["hero", "hours", "contact", "about", "links"])

    # ---- collision: first template wins ----
    def test_first_wins_collision(self):
        comp, problems = resolve_templates(base_contract())
        self.assertEqual(problems, [])
        hero = [s for s in comp["sections"] if s["name"] == "hero"][0]
        self.assertEqual(hero["source"], "template-personal")
        self.assertEqual(hero["content"]["title"], "Personal hero")
        self.assertEqual(comp["overrides_applied"], [])

    # ---- explicit override honored ----
    def test_override_honored(self):
        c = base_contract()
        c["overrides"] = {"hero": "template-business"}
        comp, problems = resolve_templates(c)
        self.assertEqual(problems, [])
        hero = [s for s in comp["sections"] if s["name"] == "hero"][0]
        self.assertEqual(hero["source"], "template-business")
        self.assertEqual(hero["content"]["title"], "Business hero")
        self.assertEqual(comp["overrides_applied"],
                         [{"section": "hero", "winner": "template-business",
                           "default": "template-personal"}])
        # order is unchanged by the override — only the content source moves
        self.assertEqual([s["name"] for s in comp["sections"]],
                         ["hero", "about", "links", "hours", "contact"])

    def test_override_unknown_section_refused(self):
        c = base_contract()
        c["overrides"] = {"nope": "template-business"}
        _, problems = resolve_templates(c)
        self.assertIn("unknown_override_section", codes(problems))

    def test_override_unknown_template_refused(self):
        c = base_contract()
        c["overrides"] = {"hero": "template-ghost"}
        _, problems = resolve_templates(c)
        self.assertIn("unknown_override_template", codes(problems))

    def test_override_template_missing_section_refused(self):
        c = base_contract()
        c["overrides"] = {"about": "template-business"}  # business has no about
        _, problems = resolve_templates(c)
        self.assertIn("override_section_missing", codes(problems))

    def test_bad_overrides_shape_refused(self):
        c = base_contract()
        c["overrides"] = ["hero"]
        _, problems = resolve_templates(c)
        self.assertIn("bad_overrides_shape", codes(problems))

    # ---- features: prune wins ----
    def test_prune_wins(self):
        comp, problems = resolve_templates(base_contract())
        self.assertEqual(problems, [])
        # personal says cover:true, business says cover:false -> disabled
        self.assertIs(comp["features"]["cover"], False)

    def test_true_flips_when_no_prune(self):
        comp, problems = resolve_templates(base_contract())
        self.assertEqual(problems, [])
        self.assertIs(comp["features"]["smart_mail"], True)
        self.assertIs(comp["features"]["smart_spaces"], True)

    def test_prune_wins_over_object_declaration(self):
        c = base_contract()
        c["template_shapes"]["template-personal"]["features"]["cover"] = \
            {"enabled": True}
        comp, problems = resolve_templates(c)
        self.assertEqual(problems, [])
        self.assertIs(comp["features"]["cover"], False)

    def test_no_opinion_stays_absent(self):
        comp, problems = resolve_templates(base_contract())
        self.assertEqual(problems, [])
        self.assertNotIn("naya_answers", comp["features"])

    def test_falsy_declaration_is_no_opinion(self):
        c = base_contract()
        c["template_shapes"]["template-personal"]["features"]["cover"] = None
        c["template_shapes"]["template-business"]["features"]["cover"] = None
        comp, problems = resolve_templates(c)
        self.assertEqual(problems, [])
        self.assertNotIn("cover", comp["features"])

    def test_bad_feature_declaration_refused(self):
        c = base_contract()
        c["template_shapes"]["template-personal"]["features"]["cover"] = "yes"
        _, problems = resolve_templates(c)
        self.assertIn("bad_feature_declaration", codes(problems))

    # ---- backward compat: single string ----
    def test_single_string_backward_compat(self):
        c1 = base_contract()
        c1["templates"] = "template-personal"
        c2 = base_contract()
        c2["templates"] = ["template-personal"]
        comp1, p1 = resolve_templates(c1)
        comp2, p2 = resolve_templates(c2)
        self.assertEqual(p1, [])
        self.assertEqual(p2, [])
        self.assertEqual(comp1, comp2)
        self.assertEqual(comp1["templates"], ["template-personal"])
        self.assertEqual([s["name"] for s in comp1["sections"]],
                         ["hero", "about", "links"])

    # ---- fail closed ----
    def test_unknown_template_refused(self):
        c = base_contract()
        c["templates"] = ["template-personal", "template-ghost"]
        comp, problems = resolve_templates(c)
        self.assertIsNone(comp)
        self.assertIn("unknown_template", codes(problems))
        ghost = [p for p in problems if p["code"] == "unknown_template"][0]
        self.assertEqual(ghost["template"], "template-ghost")

    def test_missing_shapes_refused(self):
        c = {"templates": ["template-personal"]}
        _, problems = resolve_templates(c)
        self.assertIn("missing_template_shapes", codes(problems))

    def test_empty_templates_refused(self):
        _, problems = resolve_templates({"templates": []})
        self.assertIn("empty_templates", codes(problems))

    def test_mixed_templates_shape_refused(self):
        c = base_contract()
        c["templates"] = ["template-personal",
                          ["01", "Personal page", "desc"]]
        _, problems = resolve_templates(c)
        self.assertIn("bad_templates_shape", codes(problems))

    def test_wrong_type_templates_refused(self):
        _, problems = resolve_templates({"templates": {"a": 1}})
        self.assertIn("bad_templates_shape", codes(problems))

    def test_bad_template_id_refused(self):
        _, problems = resolve_templates(
            {"templates": [""], "template_shapes": {}})
        self.assertIn("bad_template_id", codes(problems))

    # ---- display triples pass through (existing render path untouched) ----
    def test_display_triples_passthrough(self):
        c = {"templates": [["01", "Personal page", "My world in one page."],
                           ["02", "Business landing", "The front door."]]}
        comp, problems = resolve_templates(c)
        self.assertIsNone(comp)
        self.assertEqual(problems, [])

    def test_missing_templates_key_passthrough(self):
        comp, problems = resolve_templates({})
        self.assertIsNone(comp)
        self.assertEqual(problems, [])

    # ---- determinism + no aliasing ----
    def test_determinism(self):
        c = base_contract()
        c["overrides"] = {"hero": "template-business"}
        comp1, _ = resolve_templates(c)
        comp2, _ = resolve_templates(base_contract()
                                     | {"overrides": {"hero": "template-business"}})
        b1 = json.dumps(comp1, sort_keys=True).encode()
        b2 = json.dumps(comp2, sort_keys=True).encode()
        self.assertEqual(hashlib.sha256(b1).hexdigest(),
                         hashlib.sha256(b2).hexdigest())

    def test_no_aliasing_into_contract(self):
        c = base_contract()
        comp, _ = resolve_templates(c)
        comp["sections"][0]["content"]["title"] = "MUTATED"
        self.assertEqual(
            c["template_shapes"]["template-personal"]["sections"]["hero"]["title"],
            "Personal hero")

    # ---- the contract's own features win over composed ones ----
    def test_contract_features_win(self):
        c = base_contract()
        c["features"] = {"cover": True}  # contract says on; composition prunes
        comp, problems = resolve_templates(c)
        self.assertEqual(problems, [])
        self.assertIs(comp["features"]["cover"], False)  # merged: prune wins
        aproblems = apply_composition(c, comp)
        self.assertEqual(aproblems, [])
        self.assertIs(c["features"]["cover"], True)  # contract's own word stands

    def test_apply_composition_fills_undeclared(self):
        c = base_contract()
        c["features"] = {}
        comp, _ = resolve_templates(c)
        self.assertEqual(apply_composition(c, comp), [])
        self.assertIs(c["features"]["cover"], False)   # opt-out recorded
        self.assertIs(c["features"]["smart_mail"], True)

    def test_apply_composition_refuses_features_list(self):
        c = base_contract()
        c["features"] = [["Smart Mail, built in.", "desc"]]
        comp, _ = resolve_templates(c)
        self.assertIn("features_shape_conflict",
                      codes(apply_composition(c, comp)))


def compose_contract(tmp, templates, shapes, features=None):
    """A customer contract: the smoke contract with a template composition."""
    c = json.load(open(SMOKE))
    c["title"] = "Composable templates e2e"
    c["features"] = {} if features is None else features
    c["templates"] = templates
    c["template_shapes"] = shapes
    p = os.path.join(tmp, "contract.json")
    with open(p, "w") as fh:
        json.dump(c, fh)
    return p


def run_assemble(contract, workdir):
    out = os.path.join(workdir, "page.html")
    man = os.path.join(workdir, "page.manifest.json")
    r = subprocess.run(
        [sys.executable, ASSEMBLE, "--contract", contract, "--index", INDEX,
         "--template", os.path.join(SB_DIR, "templates", "page.html"),
         "--out", out, "--manifest", man],
        capture_output=True, text=True, timeout=120)
    page = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
    manifest = {}
    if os.path.exists(man):
        with open(man) as fh:
            manifest = json.load(fh)
    return r, page, manifest


class ComposableTemplatesE2E(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="compose-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- e2e: composed cover:true flips the breaker, renders markup ----
    def test_e2e_composition_flips_breaker(self):
        contract = compose_contract(self.tmp, "template-personal",
                                    json.loads(json.dumps(E2E_SHAPES)))
        r, page, manifest = run_assemble(contract, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="cover"', page)
        comp = manifest["resolution"]["composition"]
        self.assertEqual(comp["templates"], ["template-personal"])
        self.assertEqual([s["name"] for s in comp["sections"]],
                         ["hero", "about"])
        self.assertIs(comp["features"]["cover"], True)

    # ---- e2e: prune wins — cover:false in any template suppresses it ----
    def test_e2e_prune_wins(self):
        contract = compose_contract(
            self.tmp, ["template-personal", "template-business"],
            json.loads(json.dumps(E2E_SHAPES)))
        r, page, manifest = run_assemble(contract, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="cover"', page)
        comp = manifest["resolution"]["composition"]
        # section union in listed order; hero collision -> first wins
        self.assertEqual([s["name"] for s in comp["sections"]],
                         ["hero", "about", "hours"])
        hero = [s for s in comp["sections"] if s["name"] == "hero"][0]
        self.assertEqual(hero["source"], "template-personal")
        # the opt-out stays recorded in the contract's feature dict
        self.assertIs(comp["features"]["cover"], False)
        self.assertNotIn('data-cover-status="built"', page)

    # ---- e2e: prune on a STANDARD feature is honored by the default-on
    # mechanism — explicit false reads as OFF, never trips the built gate ----
    def test_e2e_prune_standard_feature_no_refusal(self):
        shapes = json.loads(json.dumps(E2E_SHAPES))
        shapes["template-business"]["features"]["smart_mail"] = False
        contract = compose_contract(
            self.tmp, ["template-personal", "template-business"], shapes)
        r, page, manifest = run_assemble(contract, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        comp = manifest["resolution"]["composition"]
        self.assertIs(comp["features"]["smart_mail"], False)

    # ---- e2e: unknown template -> structured refusal, exit 2 ----
    def test_e2e_unknown_template_refused(self):
        contract = compose_contract(
            self.tmp, ["template-personal", "template-ghost"],
            json.loads(json.dumps(E2E_SHAPES)))
        r, page, manifest = run_assemble(contract, self.tmp)
        self.assertEqual(r.returncode, 2)
        self.assertIn("unknown_template", r.stdout)
        self.assertEqual(page, "")
        self.assertEqual(manifest, {})

    # ---- e2e: determinism — same contract -> same bytes ----
    def test_e2e_determinism(self):
        shapes = json.loads(json.dumps(E2E_SHAPES))
        contract = compose_contract(
            self.tmp, ["template-personal", "template-business"], shapes)
        _, page1, man1 = run_assemble(contract, self.tmp)
        d2 = tempfile.mkdtemp(prefix="compose-b-")
        try:
            _, page2, man2 = run_assemble(contract, d2)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        h1 = hashlib.sha256(page1.encode()).hexdigest()
        h2 = hashlib.sha256(page2.encode()).hexdigest()
        self.assertEqual(h1, h2)
        self.assertEqual(man1["build"]["id"], man2["build"]["id"])
        self.assertEqual(json.dumps(man1["resolution"]["composition"],
                                   sort_keys=True),
                         json.dumps(man2["resolution"]["composition"],
                                   sort_keys=True))

    # ---- e2e: the display-triples contracts build exactly as before ----
    def test_e2e_display_contract_unchanged(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Personal page", page)  # gallery cards still render


if __name__ == "__main__":
    unittest.main(verbosity=2)

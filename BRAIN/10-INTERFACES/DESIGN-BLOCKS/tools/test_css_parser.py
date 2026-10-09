#!/usr/bin/env python3
"""
Regression tests for the class-level @import / at-rule fix in
design-compliance-check.py (finding 8, class-lesson sweep #1354).

The class: at-rule preludes must never merge into selector text, and every
encoding variant of an at-rule (CSS escapes, comments, strings, case) must be
recognized as an at-rule — parsed with CSS-syntax semantics, recorded at the
delivery boundary, never silently swallowed or string-matched.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib.util
import pathlib

_p = pathlib.Path(__file__).parent / "design-compliance-check.py"
_spec = importlib.util.spec_from_file_location("dcc", str(_p))
dcc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dcc)


def rules(css):
    return [s for s, _ in dcc.extract_rules(css)]


def at_rules(css):
    return dcc.parse_stylesheet(css)[1]


class TestImportClassClosed(unittest.TestCase):
    """Every variant: the following rule is extracted AND the import recorded."""

    VARIANTS = [
        '@import url("https://evil/x.css");\n.my-modal{background:#fff}',
        '@import "https://evil/y.css"; .my-modal{background:#fff}',
        "@import url(https://evil/z.css); .my-modal{background:#fff}",
        '@\\69 mport url("a.css"); .my-modal{background:#fff}',
        '@\\000049mport url("b.css"); .my-modal{background:#fff}',
        '@/*x*/import url("d.css"); .my-modal{background:#fff}',
        '@import /*c*/ url("e.css"); .my-modal{background:#fff}',
        '@import url("a{b}.css"); .my-modal{background:#fff}',
        '@import url("a;b.css"); .my-modal{background:#fff}',
        '@IMPORT url("f.css"); .my-modal{background:#fff}',
        '.my-modal{background:#fff} @import url("late.css");',
    ]

    def test_rule_never_dropped(self):
        for css in self.VARIANTS:
            with self.subTest(css=css[:40]):
                self.assertIn(".my-modal", rules(css),
                              f"rule dropped by variant: {css[:60]}")

    def test_import_always_recorded(self):
        for css in self.VARIANTS:
            with self.subTest(css=css[:40]):
                names = [n for n, _ in at_rules(css)]
                self.assertIn("import", names,
                              f"import swallowed by variant: {css[:60]}")


class TestAtRuleSemantics(unittest.TestCase):
    def test_media_nested_rules_extracted(self):
        self.assertEqual(rules("@media screen { .my-modal{background:#fff} }"),
                         [".my-modal"])

    def test_supports_nested_rules_extracted(self):
        self.assertEqual(
            rules("@supports (display:grid){ .my-modal{background:#fff} }"),
            [".my-modal"])

    def test_keyframes_not_rules(self):
        got = rules("@keyframes k{from{a:b}to{c:d}} .my-modal{background:#fff}")
        self.assertEqual(got, [".my-modal"])
        self.assertEqual(at_rules("@keyframes k{from{a:b}to{c:d}}"), [("keyframes", "k")])

    def test_font_face_recorded_not_rule(self):
        css = '@font-face{font-family:x;src:url(a.woff)} .my-modal{background:#fff}'
        self.assertEqual(rules(css), [".my-modal"])
        self.assertEqual(at_rules(css)[0][0], "font-face")

    def test_unterminated_comment_hides_like_browser(self):
        # browsers treat `/*` to EOF as one comment: no rules, no crash
        self.assertEqual(rules("/* .my-modal{background:#fff}"), [])
        self.assertEqual(at_rules("/* .my-modal{background:#fff}"), [])

    def test_comment_wrapped_import_is_dead(self):
        css = '/*@import url("g.css");*/ .my-modal{background:#fff}'
        self.assertEqual(rules(css), [".my-modal"])
        self.assertEqual(at_rules(css), [])

    def test_entity_smuggled_is_not_an_import(self):
        # <style> is raw text: entities are NOT decoded (browser semantics),
        # so &commat;import is not an at-rule — but the rule still parses.
        css = '&commat;import url("h.css"); .my-modal{background:#fff}'
        self.assertIn(".my-modal", rules(css))
        self.assertEqual(at_rules(css), [])

    def test_escaped_selector_class_decoded(self):
        self.assertEqual(rules(".\\6d y-modal{background:#fff}"), [".my-modal"])

    def test_garbage_is_total(self):
        for css in ["", "}}}} {{{ ;;;", "@", "@;", "{", "}", ".a{", ".a{b"]:
            rules(css)      # must not raise
            at_rules(css)   # must not raise

    def test_css_unescape(self):
        self.assertEqual(dcc.css_unescape("\\69 mport"), "import")
        # \000049 is U+0049 'I': raw decode is case-faithful; the parser
        # lowercases at-keyword names at the name step, so this still
        # registers as an @import at-rule (see test_import_always_recorded).
        self.assertEqual(dcc.css_unescape("\\000049mport"), "Import")
        self.assertEqual(dcc.css_unescape("a\\26 b"), "a&b")


class TestGraderDeliveryBoundary(unittest.TestCase):
    """analyze() names the @import class: recorded + bounded deduction."""

    def _analyze(self, style):
        catalog = {"blocks": [{
            "id": "li-modal", "name": "Modal", "category": "x",
            "selectors": [".naya-modal"],
            "job": "modal dialog overlay",
            "when_to_use": "modal",
            "tags": ["modal", "dialog"],
        }]}
        html = ("<!DOCTYPE html><html><head><style>" + style +
                "</style></head><body></body></html>")
        return dcc.analyze(html, catalog)

    def test_import_recorded_and_deducted(self):
        r = self._analyze('@import url("https://evil/x.css");\n'
                          ".my-modal{background:#fff;border-radius:8px}")
        names = [a["name"] for a in r["at_rules"]]
        self.assertIn("import", names)
        reasons = [d["reason"] for d in r["deductions"]]
        self.assertTrue(any("external stylesheet" in x for x in reasons),
                        f"deductions: {reasons}")

    def test_no_import_no_deduction(self):
        r = self._analyze(".my-modal{background:#fff}")
        self.assertEqual(r["at_rules"], [])
        self.assertFalse(any("external stylesheet" in d["reason"]
                             for d in r["deductions"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)

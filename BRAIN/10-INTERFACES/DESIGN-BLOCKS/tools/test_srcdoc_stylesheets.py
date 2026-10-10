#!/usr/bin/env python3
"""
Adversarial tests for the class-level <iframe srcdoc> fix in
design-compliance-check.py (finding 8 srcdoc follow-up, #1354).

The class: "CSS outside the grader's view" — closed by CAPABILITY, not keyword.
A srcdoc value is an attribute on the page itself: deterministically
in-document, so the grader parses it as a nested HTML document and grades
its <style>/<link>/inline CSS exactly like top-level content. The recursion
covers both earlier branches' scope (<link> inside srcdoc, @import inside
srcdoc's <style>, nested srcdoc-in-srcdoc).

The grader never touches the network. The parser is total: depth-capped,
exception-proof, and every srcdoc is recorded at the delivery boundary.
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib.util
import pathlib

_p = pathlib.Path(__file__).parent / "design-compliance-check.py"
_spec = importlib.util.spec_from_file_location("dcc", str(_p))
dcc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dcc)


MODAL_CSS = (".my-modal{background:#fff;border-radius:8px;"
             "box-shadow:0 8px 24px rgba(0,0,0,.4);padding:24px}")


def catalog():
    return {"blocks": [{
        "id": "li-modal", "name": "Modal", "category": "x",
        "selectors": [".naya-modal"],
        "job": "modal dialog overlay",
        "when_to_use": "modal",
        "tags": ["modal", "dialog"],
    }]}


def page(head, body='<div class="my-modal">hi</div>'):
    return ("<!DOCTYPE html><html><head>" + head +
            "</head><body>" + body + "</body></html>")


def iframe(doc):
    """Wrap a nested document in a srcdoc iframe.

    The document is entity-encoded exactly as real-world srcdoc authoring
    requires (a raw `"` would terminate the attribute — that is malformed
    HTML, not a grader case).
    """
    doc = doc.replace("&", "&amp;").replace('"', "&quot;")
    return '<iframe srcdoc="' + doc + '"></iframe>'


def nest(doc, levels):
    """Nest a document N srcdoc-iframes deep, correctly entity-encoded."""
    for _ in range(levels):
        doc = doc.replace("&", "&amp;").replace('"', "&quot;")
        doc = '<iframe srcdoc="' + doc + '"></iframe>'
    return doc


def tmpdir_with(files):
    d = tempfile.mkdtemp(prefix="srcdocgap-")
    for name, content in files.items():
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(content)
    return d


class TestSrcdocClass(unittest.TestCase):
    # -- the named gap: identical CSS, top-level vs srcdoc ------------------

    def test_identical_css_scored_identically(self):
        # The re-validator's demonstration: the same CSS that scores 5.5
        # (flagged) as a top-level <style> must score 5.5 in srcdoc too.
        top = dcc.analyze(page("<style>" + MODAL_CSS + "</style>"),
                          catalog(), page_dir="/tmp")
        inner = dcc.analyze(
            page(iframe("<style>" + MODAL_CSS + "</style>"), body=""),
            catalog(), page_dir="/tmp")
        self.assertEqual(top["score"], 5.5)
        self.assertEqual(inner["score"], top["score"])
        self.assertEqual(inner["num_custom_rules"], 1)
        self.assertEqual(len(inner["duplication_flags"]), 1)
        self.assertEqual(inner["duplication_flags"][0]["custom_class"],
                         "my-modal")
        self.assertEqual(inner["srcdoc_iframes"]["seen"], 1)
        self.assertEqual(inner["srcdoc_iframes"]["graded"], 1)

    def test_html_encoded_srcdoc_is_parsed(self):
        enc = ("&lt;style&gt;" + MODAL_CSS +
               "&lt;/style&gt;&lt;div class=my-modal&gt;hi&lt;/div&gt;")
        r = dcc.analyze(page('<iframe srcdoc="' + enc + '"></iframe>', body=""),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)
        self.assertEqual(len(r["duplication_flags"]), 1)

    def test_srcdoc_evasion_does_not_pay(self):
        # hiding custom CSS in srcdoc to dodge the <style> scan gets graded
        # anyway — the evasion does not pay
        r = dcc.analyze(
            page(iframe("<style>" + MODAL_CSS + "</style>"), body=""),
            catalog(), page_dir="/tmp")
        self.assertLess(r["score"], 10.0)
        self.assertEqual(len(r["duplication_flags"]), 1)

    # -- recursion: both earlier branches' scope, inside srcdoc -------------

    def test_srcdoc_with_local_link_is_graded(self):
        d = tmpdir_with({"evil.css": MODAL_CSS})
        r = dcc.analyze(
            page(iframe('<link rel="stylesheet" href="evil.css">'), body=""),
            catalog(), page_dir=d)
        self.assertEqual(r["num_custom_rules"], 1)
        self.assertEqual(len(r["duplication_flags"]), 1)
        kinds = [e["kind"] for e in r["external_stylesheets"]]
        self.assertEqual(kinds, ["local"])
        # the CSS was SEEN: no blind-link deduction
        self.assertFalse(any("via <link>" in x["reason"]
                             for x in r["deductions"]))

    def test_srcdoc_with_remote_link_recorded_once(self):
        r = dcc.analyze(
            page(iframe('<link rel="stylesheet" '
                        'href="https://evil.example/x.css">'), body=""),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["external_stylesheets"][0]["kind"], "remote")
        link_d = [x for x in r["deductions"] if "via <link>" in x["reason"]]
        self.assertEqual(len(link_d), 1)
        self.assertEqual(link_d[0]["points"], -1.0)

    def test_srcdoc_with_data_uri_link_is_graded(self):
        import urllib.parse
        css = urllib.parse.quote(MODAL_CSS)
        r = dcc.analyze(
            page(iframe('<link rel="stylesheet" '
                        'href="data:text/css,' + css + '">'), body=""),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["num_custom_rules"], 1)
        self.assertEqual(r["external_stylesheets"][0]["kind"], "data")
        self.assertFalse(any("via <link>" in x["reason"]
                             for x in r["deductions"]))

    def test_import_inside_srcdoc_style_recorded(self):
        # the @import branch, defeated the same way: @import inside a
        # srcdoc <style> is recorded and costs the bounded deduction
        r = dcc.analyze(
            page(iframe("<style>@import url('https://evil.example/y.css');"
                        "</style>"), body=""),
            catalog(), page_dir="/tmp")
        names = [a["name"] for a in r["at_rules"]]
        self.assertIn("import", names)
        imp_d = [x for x in r["deductions"] if "via @import" in x["reason"]]
        self.assertEqual(len(imp_d), 1)
        self.assertEqual(r["score"], 9.0)

    def test_nested_srcdoc_two_deep(self):
        inner = iframe("<style>" + MODAL_CSS + "</style>")
        r = dcc.analyze(page(iframe(inner), body=""),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)
        self.assertEqual(len(r["duplication_flags"]), 1)
        self.assertEqual(r["srcdoc_iframes"]["seen"], 2)
        self.assertEqual(r["srcdoc_iframes"]["max_depth"], 2)

    def test_nested_srcdoc_three_deep(self):
        r = dcc.analyze(page(nest("<style>" + MODAL_CSS + "</style>", 3),
                             body=""),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)
        self.assertEqual(r["srcdoc_iframes"]["max_depth"], 3)

    # -- no penalty inflation ------------------------------------------------

    def test_multiple_iframes_no_penalty_inflation(self):
        one = dcc.analyze(
            page(iframe("<style>" + MODAL_CSS + "</style>"), body=""),
            catalog(), page_dir="/tmp")
        three = dcc.analyze(
            page(iframe("<style>" + MODAL_CSS + "</style>") * 3, body=""),
            catalog(), page_dir="/tmp")
        # flags dedupe by class; identical srcdoc values grade once
        self.assertEqual(three["score"], one["score"])
        self.assertEqual(len(three["duplication_flags"]), 1)
        self.assertEqual(three["srcdoc_iframes"]["seen"], 3)
        self.assertEqual(three["srcdoc_iframes"]["graded"], 1)

    def test_distinct_iframes_each_graded(self):
        dialog = ".my-dialog{background:#fff;border-radius:8px}"
        r = dcc.analyze(
            page(iframe("<style>" + MODAL_CSS + "</style>")
                 + iframe("<style>" + dialog + "</style>"), body=""),
            catalog(), page_dir="/tmp")
        classes = {f["custom_class"] for f in r["duplication_flags"]}
        self.assertEqual(classes, {"my-modal", "my-dialog"})

    # -- honest pages ---------------------------------------------------------

    def test_honest_page_with_srcdoc_passes(self):
        # official-block UI delivered inside srcdoc: blocks count as used,
        # no flags, clean pass
        r = dcc.analyze(
            page(iframe('<div class="naya-modal">x</div>'), body=""),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 10.0)
        self.assertEqual(r["verdict"], "PASS")
        self.assertEqual([b["id"] for b in r["blocks_used"]], ["li-modal"])

    def test_page_without_iframes_unchanged(self):
        r = dcc.analyze(page("<style>" + MODAL_CSS + "</style>"),
                          catalog(), page_dir="/tmp")
        self.assertEqual(r["srcdoc_iframes"]["seen"], 0)
        self.assertEqual(r["score"], 5.5)

    # -- inline styles inside srcdoc -------------------------------------------

    def test_heavy_inline_style_inside_srcdoc(self):
        heavy = ('style="border-radius:8px;box-shadow:0 8px 24px #000;'
                 'background:#fff;padding:24px;margin:0 auto;max-width:1px"')
        r = dcc.analyze(page(iframe("<div " + heavy + ">x</div>"), body=""),
                        catalog(), page_dir="/tmp")
        self.assertTrue(any("inline style" in x["reason"]
                            for x in r["deductions"]))

    # -- parser-shape evasions --------------------------------------------------

    def test_srcdoc_in_comment_ignored(self):
        r = dcc.analyze(
            page("<!-- " + iframe("<style>" + MODAL_CSS + "</style>") + " -->",
                 body=""),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["srcdoc_iframes"]["seen"], 0)
        self.assertEqual(r["score"], 10.0)

    def test_empty_and_whitespace_srcdoc_ignored(self):
        r = dcc.analyze(page('<iframe srcdoc=""></iframe>'
                             '<iframe srcdoc="   "></iframe>'
                             "<iframe></iframe>", body=""),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["srcdoc_iframes"]["seen"], 0)
        self.assertEqual(r["score"], 10.0)

    def test_srcdoc_on_non_iframe_ignored(self):
        # browsers ignore srcdoc on non-iframe tags: not delivered CSS
        r = dcc.analyze(page('<div srcdoc="<style>' + MODAL_CSS +
                             '</style>"></div>', body=""),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["srcdoc_iframes"]["seen"], 0)
        self.assertEqual(r["score"], 10.0)

    def test_uppercase_iframe_and_attr(self):
        r = dcc.analyze(
            page('<IFRAME SRCDOC="<style>' + MODAL_CSS + '</style>"></IFRAME>',
                 body=""),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)

    def test_single_quoted_srcdoc(self):
        r = dcc.analyze(
            page("<iframe srcdoc='<style>" + MODAL_CSS + "</style>'>"
                 "</iframe>", body=""),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)

    def test_garbage_srcdoc_no_crash(self):
        for junk in ['<iframe srcdoc="<style>.x{"></iframe>',
                     '<iframe srcdoc="&lt;&lt;&lt;"></iframe>',
                     '<iframe srcdoc="plain text, no markup"></iframe>',
                     '<iframe srcdoc="<iframe>">',
                     '<iframe srcdoc="<style>"',
                     '<iframe srcdoc=',
                     '<iframe srcdoc="<div class=my-modal>hi</div>">']:
            r = dcc.analyze(page(junk, body=""), catalog(), page_dir="/tmp")
            self.assertIsInstance(r["score"], float)

    def test_deep_nesting_terminates_and_fails_closed(self):
        # 12-deep: capped at 8, terminates, and the unseen remainder is
        # recorded + costs the bounded -1.0 (duplication UNKNOWN) —
        # the @import/<link> precedent for CSS outside the grader's view.
        r = dcc.analyze(page(nest("<style>" + MODAL_CSS + "</style>", 12),
                             body=""),
                        catalog(), page_dir="/tmp")
        si = r["srcdoc_iframes"]
        self.assertEqual(si["max_depth"], 8)
        self.assertGreater(si["capped"], 0)
        cap_d = [x for x in r["deductions"] if "depth cap" in x["reason"]]
        self.assertEqual(len(cap_d), 1)
        self.assertEqual(cap_d[0]["points"], -1.0)

    def test_cap_deduction_is_bounded(self):
        # even a forest of over-deep iframes costs the -1.0 only once
        r = dcc.analyze(page(nest("<style>" + MODAL_CSS + "</style>", 12) * 4,
                             body=""),
                        catalog(), page_dir="/tmp")
        cap_d = [x for x in r["deductions"] if "depth cap" in x["reason"]]
        self.assertEqual(len(cap_d), 1)

    def test_eight_deep_grades_fully_no_cap_penalty(self):
        r = dcc.analyze(page(nest("<style>" + MODAL_CSS + "</style>", 8),
                             body=""),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["srcdoc_iframes"]["capped"], 0)
        self.assertEqual(r["score"], 5.5)
        self.assertFalse(any("depth cap" in x["reason"]
                             for x in r["deductions"]))


if __name__ == "__main__":
    unittest.main()

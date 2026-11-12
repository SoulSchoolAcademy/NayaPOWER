#!/usr/bin/env python3
"""
Adversarial tests for the class-level <link rel=stylesheet> fix in
design-compliance-check.py (follow-up to finding 8, #1354).

The class: "CSS outside the grader's view" — closed by CAPABILITY, not keyword.
  - stylesheets the grader can deterministically see (relative local files,
    in-document data:text/css URIs) are parsed and graded like <style>;
  - stylesheets it cannot see (remote URLs, missing/unreadable files,
    absolute paths, bad schemes) are RECORDED at the delivery boundary and
    cost one bounded -1.0 (duplication UNKNOWN) — the @import precedent.
The grader never touches the network. The resolver is total.
"""

import base64
import os
import sys
import tempfile
import unittest
import urllib.parse

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


def page(head):
    return ("<!DOCTYPE html><html><head>" + head +
            "</head><body><div class=\"my-modal\">hi</div></body></html>")


def tmpdir_with(files):
    """Create a temp dir containing {name: content}; return the dir path."""
    d = tempfile.mkdtemp(prefix="linkgap-")
    for name, content in files.items():
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(content)
    return d


class TestLinkStylesheetClass(unittest.TestCase):
    # -- the named gap: custom CSS living ONLY in a linked sheet ----------

    def test_local_sheet_css_is_graded(self):
        d = tmpdir_with({"evil.css": MODAL_CSS})
        r = dcc.analyze(page('<link rel="stylesheet" href="evil.css">'),
                        catalog(), page_dir=d)
        self.assertEqual(r["num_custom_rules"], 1)
        self.assertEqual(len(r["duplication_flags"]), 1)
        self.assertEqual(r["duplication_flags"][0]["custom_class"], "my-modal")
        # CSS was SEEN: no blind-link deduction, score reflects the flag
        self.assertFalse(any("via <link>" in x["reason"]
                             for x in r["deductions"]))
        kinds = [e["kind"] for e in r["external_stylesheets"]]
        self.assertEqual(kinds, ["local"])

    def test_remote_link_recorded_and_deducted(self):
        r = dcc.analyze(page('<link rel="stylesheet" '
                             'href="https://evil.example/x.css">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 9.0)
        reasons = [x["reason"] for x in r["deductions"]]
        self.assertTrue(any("via <link>" in x for x in reasons))
        self.assertEqual(r["external_stylesheets"][0]["kind"], "remote")

    def test_multiple_remote_links_one_bounded_deduction(self):
        head = "".join(
            f'<link rel="stylesheet" href="https://evil.example/{i}.css">'
            for i in range(3))
        r = dcc.analyze(page(head), catalog(), page_dir="/tmp")
        link_deds = [x for x in r["deductions"] if "via <link>" in x["reason"]]
        self.assertEqual(len(link_deds), 1)
        self.assertEqual(link_deds[0]["points"], -1.0)
        self.assertEqual(r["num_external_stylesheets"], 3)

    def test_media_query_link_still_counts(self):
        r = dcc.analyze(page('<link rel="stylesheet" media="print" '
                             'href="https://evil.example/x.css">'),
                        catalog(), page_dir="/tmp")
        e = r["external_stylesheets"][0]
        self.assertEqual(e["media"], "print")
        self.assertTrue(any("via <link>" in x["reason"]
                            for x in r["deductions"]))

    def test_unquoted_href(self):
        d = tmpdir_with({"evil.css": MODAL_CSS})
        r = dcc.analyze(page('<link rel=stylesheet href=evil.css>'),
                        catalog(), page_dir=d)
        self.assertEqual(r["external_stylesheets"][0]["kind"], "local")
        self.assertEqual(r["num_custom_rules"], 1)

    def test_href_with_query_string_resolves(self):
        d = tmpdir_with({"evil.css": MODAL_CSS})
        r = dcc.analyze(page('<link rel="stylesheet" href="evil.css?v=2">'),
                        catalog(), page_dir=d)
        self.assertEqual(r["external_stylesheets"][0]["kind"], "local")
        self.assertEqual(r["num_custom_rules"], 1)

    # -- data: URIs are in-document: read, not penalized -------------------

    def test_data_uri_percent_encoded_is_graded(self):
        css = urllib.parse.quote(MODAL_CSS)
        r = dcc.analyze(page(f'<link rel="stylesheet" href="data:text/css,{css}">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["num_custom_rules"], 1)
        self.assertFalse(any("via <link>" in x["reason"]
                             for x in r["deductions"]))
        self.assertEqual(r["external_stylesheets"][0]["kind"], "data")

    def test_data_uri_base64_is_graded(self):
        b64 = base64.b64encode(MODAL_CSS.encode()).decode()
        r = dcc.analyze(page('<link rel="stylesheet" '
                             f'href="data:text/css;base64,{b64}">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["num_custom_rules"], 1)
        self.assertFalse(any("via <link>" in x["reason"]
                             for x in r["deductions"]))

    def test_data_uri_stuffing_evasion_fails(self):
        # stuffing custom CSS into data: to dodge the <style> scan
        # gets graded anyway — the evasion does not pay
        b64 = base64.b64encode(MODAL_CSS.encode()).decode()
        r = dcc.analyze(page('<link rel="stylesheet" '
                             f'href="data:text/css;base64,{b64}">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(len(r["duplication_flags"]), 1)

    def test_malformed_data_uri_fails_closed(self):
        r = dcc.analyze(page('<link rel="stylesheet" '
                             'href="data:text/css;base64,!!!not-base64!!!">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["external_stylesheets"][0]["kind"], "unresolvable")
        self.assertTrue(any("via <link>" in x["reason"]
                            for x in r["deductions"]))

    def test_non_css_data_uri_unresolvable(self):
        r = dcc.analyze(page('<link rel="stylesheet" '
                             'href="data:text/plain,hello">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["external_stylesheets"][0]["kind"], "unresolvable")

    # -- fail-closed shapes -------------------------------------------------

    def test_missing_file_fails_closed_no_crash(self):
        r = dcc.analyze(page('<link rel="stylesheet" href="nope.css">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["external_stylesheets"][0]["kind"], "unresolvable")
        self.assertTrue(any("via <link>" in x["reason"]
                            for x in r["deductions"]))

    def test_no_page_dir_fails_closed(self):
        d = tmpdir_with({"evil.css": MODAL_CSS})
        html = open(os.path.join(d, "p.html"), "w")
        html.write(page('<link rel="stylesheet" href="evil.css">'))
        html.close()
        # analyze() without page_dir: cannot resolve -> recorded + deducted
        r = dcc.analyze(page('<link rel="stylesheet" href="evil.css">'),
                        catalog())
        self.assertEqual(r["external_stylesheets"][0]["kind"], "unresolvable")
        self.assertTrue(any("via <link>" in x["reason"]
                            for x in r["deductions"]))

    def test_empty_and_missing_href(self):
        r = dcc.analyze(page('<link rel="stylesheet" href="">'
                             '<link rel="stylesheet">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["num_external_stylesheets"], 2)
        kinds = {e["kind"] for e in r["external_stylesheets"]}
        self.assertEqual(kinds, {"unresolvable"})

    def test_javascript_scheme_not_executed_not_read(self):
        r = dcc.analyze(page('<link rel="stylesheet" '
                             'href="javascript:alert(1)">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["external_stylesheets"][0]["kind"], "unresolvable")
        self.assertTrue(any("via <link>" in x["reason"]
                            for x in r["deductions"]))

    def test_absolute_path_never_read(self):
        r = dcc.analyze(page('<link rel="stylesheet" href="/etc/hostname">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["external_stylesheets"][0]["kind"], "unresolvable")

    def test_protocol_relative_is_remote(self):
        r = dcc.analyze(page('<link rel="stylesheet" '
                             'href="//evil.example/x.css">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["external_stylesheets"][0]["kind"], "remote")

    # -- parser-shape evasions ----------------------------------------------

    def test_link_inside_comment_ignored(self):
        d = tmpdir_with({"evil.css": MODAL_CSS})
        r = dcc.analyze(page('<!-- <link rel="stylesheet" href="evil.css"> -->'),
                        catalog(), page_dir=d)
        self.assertEqual(r["external_stylesheets"], [])
        self.assertFalse(any("via <link>" in x["reason"]
                             for x in r["deductions"]))

    def test_rel_token_variants(self):
        for rel in ['rel="alternate stylesheet"',
                    'REL="STYLESHEET"',
                    "rel='stylesheet'",
                    'rel=stylesheet']:
            r = dcc.analyze(
                page(f'<link {rel} href="https://evil.example/x.css">'),
                catalog(), page_dir="/tmp")
            self.assertEqual(r["num_external_stylesheets"], 1, rel)

    def test_rel_without_stylesheet_token_ignored(self):
        r = dcc.analyze(page('<link rel="preconnect" '
                             'href="https://evil.example/">'
                             '<link rel="icon" href="f.ico">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["external_stylesheets"], [])

    def test_gt_inside_quoted_href(self):
        r = dcc.analyze(page('<link rel="stylesheet" href="a>b.css">'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["external_stylesheets"][0]["href"], "a>b.css")

    def test_garbage_html_no_crash(self):
        for junk in ['<link rel="stylesheet" href=',
                     '<link rel="stylesheet"',
                     '<link>',
                     '<link rel=stylesheet href="x.css"',
                     '<LINK REL=STYLESHEET HREF="HTTPS://EVIL.EXAMPLE/X.CSS">']:
            r = dcc.analyze(page(junk), catalog(), page_dir="/tmp")
            self.assertIsInstance(r["score"], float)

    # -- interaction with the @import class ----------------------------------

    def test_link_plus_import_two_bounded_deductions(self):
        html = ("<!DOCTYPE html><html><head>"
                '<link rel="stylesheet" href="https://evil.example/x.css">'
                "<style>@import url('https://evil.example/y.css');</style>"
                "</head><body></body></html>")
        r = dcc.analyze(html, catalog(), page_dir="/tmp")
        link_d = [x for x in r["deductions"] if "via <link>" in x["reason"]]
        imp_d = [x for x in r["deductions"] if "via @import" in x["reason"]]
        self.assertEqual(len(link_d), 1)
        self.assertEqual(len(imp_d), 1)
        self.assertEqual(r["score"], 8.0)

    def test_import_inside_linked_css_recorded(self):
        d = tmpdir_with({"a.css": '@import url("b.css");\n' + MODAL_CSS})
        r = dcc.analyze(page('<link rel="stylesheet" href="a.css">'),
                        catalog(), page_dir=d)
        # the linked CSS was read AND its @import recorded (fail closed)
        self.assertEqual(r["num_custom_rules"], 1)
        names = [a["name"] for a in r["at_rules"]]
        self.assertIn("import", names)
        self.assertTrue(any("via @import" in x["reason"]
                            for x in r["deductions"]))

    # -- resolver totality ----------------------------------------------------

    def test_resolver_total(self):
        nasty = ["", "   ", "data:", "data:text/css;base64,",
                 "data:text/css;base64,====",
                 "http://[::1", "https://", "//", "///",
                 "javascript:/*", "file:///etc/passwd",
                 "C:\\win\\x.css", "/",
                 "a" * 5000 + ".css",
                 "\x00.css", "evil.css\x00",
                 "data:text/css,\xff\xfe",
                 ]
        for href in nasty:
            rec = dcc.resolve_stylesheet_link(href, "/tmp")
            self.assertIn(rec["kind"],
                          {"local", "data", "remote", "unresolvable"})

    def test_oversize_file_not_read(self):
        d = tempfile.mkdtemp(prefix="linkgap-big-")
        big = os.path.join(d, "big.css")
        with open(big, "w") as f:
            f.write("/*" + "x" * (dcc._MAX_LINKED_CSS_BYTES + 1))
        r = dcc.analyze(page('<link rel="stylesheet" href="big.css">'),
                        catalog(), page_dir=d)
        self.assertEqual(r["external_stylesheets"][0]["kind"], "unresolvable")


    # -- specimen-home exemption --------------------------------------------

    def _home_catalog(self):
        c = catalog()
        c["blocks"][0]["selectors"] = [".li-stage .li-modal",
                                       ".li-stage .li-modal-title"]
        return c

    def test_home_block_implementation_not_flagged(self):
        # li-modal's own specimen links its own block.css: the block's
        # implementation classes must not be flagged as "duplicating"
        # official blocks (incl. "use nl-modal instead of .li-modal").
        base = ("BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/overlays/li-modal")
        d = tmpdir_with({})
        # fake a library-home layout: <tmp>/blocks/x/li-modal/specimen.html
        home = os.path.join(d, "blocks", "x", "li-modal")
        os.makedirs(home)
        css = ".li-modal{background:#fff;border-radius:8px}"
        with open(os.path.join(home, "block.css"), "w") as f:
            f.write(css)
        html = page('<link rel="stylesheet" href="block.css">')
        r = dcc.analyze(html, self._home_catalog(), page_dir=home)
        self.assertEqual(r["specimen_home"], "li-modal")
        self.assertEqual(r["num_custom_rules"], 0)
        self.assertEqual(len(r["duplication_flags"]), 0)

    def test_home_exemption_needs_library_tree(self):
        # same page outside blocks/<cat>/<id>/ -> no exemption, graded
        d = tmpdir_with({"block.css":
                         ".li-modal{background:#fff;border-radius:8px}"})
        r = dcc.analyze(page('<link rel="stylesheet" href="block.css">'),
                        catalog(), page_dir=d)
        self.assertIsNone(r["specimen_home"])
        self.assertEqual(r["num_custom_rules"], 1)

    def test_home_exemption_only_covers_home_turf_files(self):
        # the exemption covers linked files inside the block's home dir —
        # the page's OWN <style> CSS is still graded there.
        home = tempfile.mkdtemp(prefix="linkgap-home2-")
        hd = os.path.join(home, "blocks", "x", "li-modal")
        os.makedirs(hd)
        with open(os.path.join(hd, "block.css"), "w") as f:
            f.write(".li-modal{background:#fff;border-radius:8px}\n"
                    ".my-toast{background:#fff;border-radius:8px}")
        html = ("<!DOCTYPE html><html><head>"
                '<link rel="stylesheet" href="block.css">'
                "<style>.my-toast2{background:#fff;border-radius:8px}</style>"
                "</head><body></body></html>")
        r = dcc.analyze(html, self._home_catalog(), page_dir=hd)
        # home-turf block.css: not graded (library implementation, not delivery)
        self.assertEqual(r["num_custom_rules"], 1)
        customs = {c for cr in r["custom_rules"] for c in cr["classes"]}
        self.assertEqual(customs, {"my-toast2"})

    def test_home_turf_at_rules_still_recorded(self):
        # at-rules are recorded at the delivery boundary even on home turf:
        # an @import inside block.css still costs the bounded deduction.
        home = tempfile.mkdtemp(prefix="linkgap-home3-")
        hd = os.path.join(home, "blocks", "x", "li-modal")
        os.makedirs(hd)
        with open(os.path.join(hd, "block.css"), "w") as f:
            f.write('@import url("more.css");\n.li-modal{color:#fff}')
        r = dcc.analyze(page('<link rel="stylesheet" href="block.css">'),
                        self._home_catalog(), page_dir=hd)
        names = [a["name"] for a in r["at_rules"]]
        self.assertIn("import", names)
        self.assertTrue(any("via @import" in x["reason"]
                            for x in r["deductions"]))
        # ...but the implementation rules themselves are not graded
        self.assertEqual(r["num_custom_rules"], 0)

    def test_quarantine_gets_no_exemption(self):
        d = tempfile.mkdtemp(prefix="linkgap-q-")
        qd = os.path.join(d, "quarantine", "unapproved-inventions-1968",
                          "rich-editor")
        os.makedirs(qd)
        with open(os.path.join(qd, "evil.css"), "w") as f:
            f.write(MODAL_CSS)
        r = dcc.analyze(page('<link rel="stylesheet" href="evil.css">'),
                        self._home_catalog(), page_dir=qd)
        self.assertIsNone(r["specimen_home"])
        self.assertEqual(len(r["duplication_flags"]), 1)


if __name__ == "__main__":
    unittest.main()

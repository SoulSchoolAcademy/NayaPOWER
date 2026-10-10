#!/usr/bin/env python3
"""
Adversarial tests for the class-level data: URI document fix in
design-compliance-check.py (finding 8 follow-up lane, #1354).

The class: "CSS outside the grader's view" — closed by CAPABILITY, not
keyword. <object data="data:text/html,...">, <embed src="data:text/html,...">,
and <iframe src="data:text/html,..."> (no srcdoc — top-level or nested
inside srcdoc) carry whole HTML documents inside the page's own attribute
bytes: deterministically in-document, so the grader decodes (URL/base64)
and parses them as nested documents with the SAME recursive machinery as
srcdoc. The recursion covers cross-mechanism nesting for free (data: inside
srcdoc, srcdoc inside data:).

The grader never touches the network. The parser is total: depth-capped
(shared budget of 8 with srcdoc), exception-proof, and every data: document
is recorded at the delivery boundary.

SVG posture, explicit: data:image/svg+xml payloads are NOT parsed — an SVG
is an isolated image document whose <style> styles the image viewport, not
the host page. Grading it as page CSS would manufacture false positives.
"""

import base64
import os
import sys
import unittest
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib.util
import pathlib

_p = pathlib.Path(__file__).parent / "design-compliance-check.py"
_spec = importlib.util.spec_from_file_location("dcc", str(_p))
dcc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dcc)


TOAST_CSS = (".qm-toast{background:#111;border-radius:10px;"
             "padding:16px;color:#fff}")
BANNER_CSS = (".qm-banner{background:#220;border-left:4px solid gold;"
              "padding:12px}")


def catalog():
    return {"blocks": [
        {
            "id": "li-toast", "name": "Toast", "category": "x",
            "selectors": [".naya-toast"],
            "job": "toast notification",
            "when_to_use": "toast",
            "tags": ["toast", "notification"],
        },
        {
            "id": "li-banner", "name": "Banner", "category": "x",
            "selectors": [".naya-banner"],
            "job": "banner alert",
            "when_to_use": "banner",
            "tags": ["banner", "alert"],
        },
    ]}


def page(head, body=""):
    return ("<!DOCTYPE html><html><head>" + head +
            "</head><body>" + body + "</body></html>")


def duri(doc, b64=False, mime="text/html"):
    """Encode a document as a data: URI payload, as real authoring does."""
    if b64:
        payload = base64.b64encode(doc.encode("utf-8")).decode("ascii")
        return "data:" + mime + ";base64," + payload
    return "data:" + mime + "," + urllib.parse.quote(doc, safe="")


def obj(doc, **kw):
    return '<object data="' + duri(doc, **kw) + '"></object>'


def emb(doc, **kw):
    return '<embed src="' + duri(doc, **kw) + '">'


def ifr(doc, **kw):
    return '<iframe src="' + duri(doc, **kw) + '"></iframe>'


def enc(doc):
    """Entity-encode a doc for a srcdoc attribute (real authoring)."""
    return doc.replace("&", "&amp;").replace('"', "&quot;")


def srcdoc_iframe(doc):
    return '<iframe srcdoc="' + enc(doc) + '"></iframe>'


def nest_data(doc, levels):
    """Nest a document N data:-URI objects deep."""
    for _ in range(levels):
        doc = obj(doc)
    return doc


class TestDataUriDocuments(unittest.TestCase):
    # -- the named holes: identical CSS, top-level vs data: document ------

    def test_identical_css_scored_identically_object(self):
        top = dcc.analyze(page("<style>" + TOAST_CSS + "</style>"),
                          catalog(), page_dir="/tmp")
        inner = dcc.analyze(page(obj("<style>" + TOAST_CSS + "</style>")),
                            catalog(), page_dir="/tmp")
        self.assertEqual(top["score"], 5.5)
        self.assertEqual(inner["score"], top["score"])
        self.assertEqual(inner["num_custom_rules"], 1)
        self.assertEqual(len(inner["duplication_flags"]), 1)
        self.assertEqual(inner["duplication_flags"][0]["custom_class"],
                         "qm-toast")
        self.assertEqual(inner["datauri_documents"]["seen"], 1)
        self.assertEqual(inner["datauri_documents"]["graded"], 1)

    def test_embed_src_urlencoded_flagged(self):
        r = dcc.analyze(page(emb("<style>" + TOAST_CSS + "</style>")),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)
        self.assertEqual(len(r["duplication_flags"]), 1)

    def test_iframe_src_urlencoded_flagged(self):
        r = dcc.analyze(page(ifr("<style>" + TOAST_CSS + "</style>")),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)
        self.assertEqual(len(r["duplication_flags"]), 1)

    def test_object_base64_flagged(self):
        r = dcc.analyze(page(obj("<style>" + TOAST_CSS + "</style>", b64=True)),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)
        self.assertEqual(r["datauri_documents"]["graded"], 1)

    def test_embed_base64_flagged(self):
        r = dcc.analyze(page(emb("<style>" + BANNER_CSS + "</style>", b64=True)),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)
        self.assertEqual(len(r["duplication_flags"]), 1)

    def test_iframe_src_base64_flagged(self):
        r = dcc.analyze(page(ifr("<style>" + TOAST_CSS + "</style>", b64=True)),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)

    def test_frame_src_flagged(self):
        r = dcc.analyze(
            page('<frame src="' + duri("<style>" + TOAST_CSS + "</style>") + '">'),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)
        self.assertEqual(r["datauri_documents"]["graded"], 1)

    def test_data_uri_evasion_does_not_pay(self):
        for tag in (obj("<style>" + TOAST_CSS + "</style>"),
                    emb("<style>" + TOAST_CSS + "</style>"),
                    ifr("<style>" + TOAST_CSS + "</style>")):
            r = dcc.analyze(page(tag), catalog(), page_dir="/tmp")
            self.assertLess(r["score"], 10.0, tag[:40])

    # -- cross-mechanism nesting --------------------------------------------

    def test_data_uri_inside_srcdoc(self):
        # the re-validator's E3: <iframe srcdoc> containing
        # <iframe src="data:text/html..."> (no nested srcdoc)
        inner = ifr("<style>" + TOAST_CSS + "</style>")
        r = dcc.analyze(page(srcdoc_iframe(inner)), catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)
        self.assertEqual(len(r["duplication_flags"]), 1)
        self.assertEqual(r["datauri_documents"]["seen"], 1)
        self.assertEqual(r["datauri_documents"]["graded"], 1)
        self.assertEqual(r["datauri_documents"]["max_depth"], 2)

    def test_srcdoc_inside_data_uri(self):
        inner = srcdoc_iframe("<style>" + TOAST_CSS + "</style>")
        r = dcc.analyze(page(obj(inner)), catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)
        self.assertEqual(r["srcdoc_iframes"]["seen"], 1)
        self.assertEqual(r["srcdoc_iframes"]["graded"], 1)
        self.assertEqual(r["datauri_documents"]["graded"], 1)

    def test_data_uri_with_local_link_is_graded(self):
        import tempfile
        d = tempfile.mkdtemp(prefix="dataurigap-")
        with open(os.path.join(d, "evil.css"), "w") as f:
            f.write(TOAST_CSS)
        r = dcc.analyze(
            page(obj('<link rel="stylesheet" href="evil.css">')),
            catalog(), page_dir=d)
        self.assertEqual(r["num_custom_rules"], 1)
        self.assertEqual(len(r["duplication_flags"]), 1)
        self.assertFalse(any("via <link>" in x["reason"]
                             for x in r["deductions"]))

    def test_import_inside_data_uri_style_recorded(self):
        r = dcc.analyze(
            page(obj("<style>@import url('https://evil.example/y.css');"
                     "</style>")),
            catalog(), page_dir="/tmp")
        names = [a["name"] for a in r["at_rules"]]
        self.assertIn("import", names)
        imp_d = [x for x in r["deductions"] if "via @import" in x["reason"]]
        self.assertEqual(len(imp_d), 1)
        self.assertEqual(r["score"], 9.0)

    # -- honest pages ---------------------------------------------------------

    def test_honest_official_block_in_data_uri_passes(self):
        r = dcc.analyze(page(obj('<div class="naya-toast">x</div>')),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 10.0)
        self.assertEqual(r["verdict"], "PASS")
        self.assertEqual([b["id"] for b in r["blocks_used"]], ["li-toast"])

    def test_honest_page_without_data_uris_unchanged(self):
        r = dcc.analyze(page("<style>" + TOAST_CSS + "</style>"),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["datauri_documents"]["seen"], 0)
        self.assertEqual(r["score"], 5.5)

    # -- not documents: images, SVG, CSS, wrong MIME --------------------------

    def test_data_image_is_not_a_document(self):
        png = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAY"
               "AAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
        for tag in ('<object data="' + png + '"></object>',
                    '<embed src="' + png + '">',
                    '<img src="' + png + '">'):
            r = dcc.analyze(page(tag), catalog(), page_dir="/tmp")
            self.assertEqual(r["datauri_documents"]["seen"], 0, tag[:40])
            self.assertEqual(r["datauri_documents"]["graded"], 0, tag[:40])
            self.assertEqual(r["score"], 10.0, tag[:40])

    def test_data_svg_style_is_not_graded(self):
        # explicit posture: an SVG payload is an isolated image document;
        # its <style> is not page CSS — grading it would be a false positive
        svg = ("<svg xmlns='http://www.w3.org/2000/svg'>"
               "<style>.qm-toast{fill:red}</style></svg>")
        r = dcc.analyze(page(obj(svg, mime="image/svg+xml")),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["datauri_documents"]["graded"], 0)
        self.assertEqual(r["num_custom_rules"], 0)
        self.assertEqual(r["score"], 10.0)

    def test_data_css_on_object_is_not_a_document(self):
        r = dcc.analyze(page(obj(TOAST_CSS, mime="text/css")),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["datauri_documents"]["seen"], 0)
        self.assertEqual(r["score"], 10.0)

    def test_wrong_mime_not_parsed(self):
        r = dcc.analyze(
            page(obj("<style>" + TOAST_CSS + "</style>", mime="text/htmlfoo")),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["datauri_documents"]["seen"], 0)
        self.assertEqual(r["score"], 10.0)

    def test_missing_mime_defaults_to_text_plain(self):
        # RFC 2397: no mediatype -> text/plain -> browsers render as text
        doc = urllib.parse.quote("<style>" + TOAST_CSS + "</style>", safe="")
        r = dcc.analyze(page('<object data="data:,' + doc + '"></object>'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["datauri_documents"]["seen"], 0)
        self.assertEqual(r["score"], 10.0)

    def test_img_with_data_html_is_not_a_document(self):
        # browsers show a broken image, not a nested document
        r = dcc.analyze(
            page('<img src="' + duri("<style>" + TOAST_CSS + "</style>") + '">'),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["datauri_documents"]["seen"], 0)
        self.assertEqual(r["score"], 10.0)

    def test_double_encoded_entities_render_as_text(self):
        # URL-decode yields literal &lt; entities: browsers show text, not CSS
        dbl = urllib.parse.quote("&lt;style&gt;" + TOAST_CSS + "&lt;/style&gt;",
                                 safe="")
        r = dcc.analyze(page('<object data="data:text/html,' + dbl + '"></object>'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["num_custom_rules"], 0)
        self.assertEqual(r["score"], 10.0)

    # -- encoding robustness ----------------------------------------------------

    def test_uppercase_data_scheme_and_mime(self):
        doc = urllib.parse.quote("<style>" + TOAST_CSS + "</style>", safe="")
        r = dcc.analyze(page('<object data="DATA:TEXT/HTML,' + doc + '"></object>'),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)

    def test_charset_param_still_parsed(self):
        doc = urllib.parse.quote("<style>" + TOAST_CSS + "</style>", safe="")
        r = dcc.analyze(
            page('<object data="data:text/html;charset=utf-8,' + doc + '"></object>'),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)

    def test_base64_with_whitespace_parsed(self):
        raw = base64.b64encode(("<style>" + TOAST_CSS + "</style>").encode()).decode()
        chunked = "\n".join(raw[i:i + 16] for i in range(0, len(raw), 16))
        r = dcc.analyze(
            page('<object data="data:text/html;base64,' + chunked + '"></object>'),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)

    def test_malformed_base64_fails_closed(self):
        r = dcc.analyze(
            page('<object data="data:text/html;base64,!!!not-base64!!!"></object>'),
            catalog(), page_dir="/tmp")
        self.assertEqual(r["datauri_documents"]["seen"], 1)
        self.assertEqual(r["datauri_documents"]["graded"], 0)
        self.assertEqual(r["score"], 10.0)

    def test_empty_payload_no_crash(self):
        for tag in ('<object data="data:text/html,"></object>',
                    '<embed src="data:text/html;base64,">',
                    '<iframe src="data:text/html"></iframe>',
                    '<object data="data:"></object>'):
            r = dcc.analyze(page(tag), catalog(), page_dir="/tmp")
            self.assertIsInstance(r["score"], float)

    def test_garbage_payloads_no_crash(self):
        for tag in ('<object data="data:text/html,%zz%"></object>',
                    '<object data="data:text/html,<style>.x{"></object>',
                    '<embed src="data:text/html,plain text, no markup">',
                    '<iframe src="data:text/html,<object>">'):
            r = dcc.analyze(page(tag), catalog(), page_dir="/tmp")
            self.assertIsInstance(r["score"], float)

    def test_non_data_urls_ignored(self):
        # remote and relative URLs on these attributes are outside this
        # lane (not deterministically in-document)
        for tag in ('<iframe src="https://evil.example/x.html"></iframe>',
                    '<iframe src="evil.html"></iframe>',
                    '<object data="/abs/path.html"></object>',
                    '<embed src="">',
                    '<object></object>'):
            r = dcc.analyze(page(tag), catalog(), page_dir="/tmp")
            self.assertEqual(r["datauri_documents"]["seen"], 0, tag[:40])
            self.assertEqual(r["score"], 10.0, tag[:40])

    # -- no penalty inflation ---------------------------------------------------

    def test_multiple_identical_data_uris_no_penalty_inflation(self):
        one = dcc.analyze(page(obj("<style>" + TOAST_CSS + "</style>")),
                          catalog(), page_dir="/tmp")
        three = dcc.analyze(
            page(obj("<style>" + TOAST_CSS + "</style>") * 3),
            catalog(), page_dir="/tmp")
        self.assertEqual(three["score"], one["score"])
        self.assertEqual(len(three["duplication_flags"]), 1)
        self.assertEqual(three["datauri_documents"]["seen"], 3)
        self.assertEqual(three["datauri_documents"]["graded"], 1)

    def test_distinct_data_uris_each_graded(self):
        r = dcc.analyze(
            page(obj("<style>" + TOAST_CSS + "</style>")
                 + emb("<style>" + BANNER_CSS + "</style>")),
            catalog(), page_dir="/tmp")
        classes = {f["custom_class"] for f in r["duplication_flags"]}
        self.assertEqual(classes, {"qm-toast", "qm-banner"})
        self.assertEqual(r["datauri_documents"]["graded"], 2)

    def test_cross_mechanism_dedup_srcdoc_and_data_uri(self):
        # the SAME document delivered as srcdoc AND as data: URI grades once
        doc = "<style>" + TOAST_CSS + "</style>"
        r = dcc.analyze(page(srcdoc_iframe(doc) + obj(doc)),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["score"], 5.5)
        self.assertEqual(r["srcdoc_iframes"]["graded"], 1)
        self.assertEqual(r["datauri_documents"]["seen"], 1)
        self.assertEqual(r["datauri_documents"]["graded"], 0)
        self.assertEqual(len(r["duplication_flags"]), 1)

    def test_same_doc_urlencoded_and_base64_grades_once(self):
        doc = "<style>" + TOAST_CSS + "</style>"
        r = dcc.analyze(page(obj(doc) + obj(doc, b64=True)),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["datauri_documents"]["seen"], 2)
        self.assertEqual(r["datauri_documents"]["graded"], 1)
        self.assertEqual(r["score"], 5.5)

    # -- depth cap ----------------------------------------------------------------

    def test_deep_nesting_terminates_and_fails_closed(self):
        r = dcc.analyze(page(nest_data("<style>" + TOAST_CSS + "</style>", 12)),
                        catalog(), page_dir="/tmp")
        du = r["datauri_documents"]
        self.assertEqual(du["max_depth"], 8)
        self.assertGreater(du["capped"], 0)
        cap_d = [x for x in r["deductions"] if "depth cap" in x["reason"]
                 and "data: URI" in x["reason"]]
        self.assertEqual(len(cap_d), 1)
        self.assertEqual(cap_d[0]["points"], -1.0)
        # the innermost CSS sits beyond the cap: unseen, only the -1.0
        self.assertEqual(r["score"], 9.0)

    def test_cap_deduction_is_bounded(self):
        r = dcc.analyze(
            page(nest_data("<style>" + TOAST_CSS + "</style>", 12) * 4),
            catalog(), page_dir="/tmp")
        cap_d = [x for x in r["deductions"] if "depth cap" in x["reason"]]
        self.assertEqual(len(cap_d), 1)

    def test_eight_deep_grades_fully_no_cap_penalty(self):
        r = dcc.analyze(page(nest_data("<style>" + TOAST_CSS + "</style>", 8)),
                        catalog(), page_dir="/tmp")
        self.assertEqual(r["datauri_documents"]["capped"], 0)
        self.assertEqual(r["score"], 5.5)
        self.assertFalse(any("depth cap" in x["reason"]
                             for x in r["deductions"]))

    def test_mixed_srcdoc_data_uri_depth_shares_budget(self):
        # srcdoc nesting 5 deep, then data: docs: the SHARED budget caps
        # the total at 8 — a data: document at combined depth 9 is capped
        inner = "<style>" + TOAST_CSS + "</style>"
        for _ in range(4):
            inner = obj(inner)  # 4 data: levels
        for _ in range(5):
            inner = enc(inner)
            inner = '<iframe srcdoc="' + inner + '"></iframe>'  # 5 srcdoc levels
        r = dcc.analyze(page(inner), catalog(), page_dir="/tmp")
        du, si = r["datauri_documents"], r["srcdoc_iframes"]
        self.assertEqual(max(du["max_depth"], si["max_depth"]), 8)
        self.assertGreater(du["capped"] + si["capped"], 0)
        cap_d = [x for x in r["deductions"] if "depth cap" in x["reason"]]
        # one bounded deduction per perimeter that capped
        self.assertLessEqual(len(cap_d), 2)
        for c in cap_d:
            self.assertEqual(c["points"], -1.0)


if __name__ == "__main__":
    unittest.main()

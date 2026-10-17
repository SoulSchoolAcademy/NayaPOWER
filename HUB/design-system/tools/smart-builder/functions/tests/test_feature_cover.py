#!/usr/bin/env python3
"""Acceptance tests for feature.cover (registry acceptance:
upload_applies, fallback_when_missing).

Stdlib only (unittest + subprocess). Each test runs the real
assemble.py end-to-end against the real builder index:

  upload_applies        -> contract-declared photo/cover URLs land in the page
  fallback_when_missing -> absent URLs render initials/placeholder, never src=""
  activation gate       -> no cover markup unless the contract declares it
  sanitization          -> hostile URL schemes -> structured refusal (exit 2)
  registry binding      -> contract cannot activate what the registry does
                           not mark 'built' (fail closed)
  determinism           -> same contract -> same bytes
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
INDEX = os.path.normpath(os.path.join(
    SB_DIR, "..", "..", "library", "catalog", "builder-index-v1.json"))
ASSEMBLE = os.path.join(SB_DIR, "assemble.py")
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")

COVER_DECL = {
    "enabled": True,
    "photo_url": "https://images.nayanet.live/morning-crumb/owner.jpg",
    "cover_url": "https://images.nayanet.live/morning-crumb/cover.jpg",
    "name": "Morning Crumb",
    "tagline": "Warm bread · order ahead",
}


def cover_contract(tmp, decl):
    """A customer contract: smoke contract with features as a breaker dict."""
    c = json.load(open(SMOKE))
    c["title"] = "Cover acceptance contract"
    c["features"] = {"cover": decl}
    p = os.path.join(tmp, "contract.json")
    json.dump(c, open(p, "w"))
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


class FeatureCoverAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fcover-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- upload_applies: contract-declared media lands in the page ----
    def test_activation_via_contract(self):
        r, page, manifest = run_assemble(
            cover_contract(self.tmp, dict(COVER_DECL)), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="cover"', page)
        self.assertIn('data-cover-status="built"', page)
        self.assertIn("https://images.nayanet.live/morning-crumb/owner.jpg", page)
        self.assertIn("https://images.nayanet.live/morning-crumb/cover.jpg", page)
        self.assertIn("Morning Crumb", page)
        self.assertIn("Warm bread · order ahead", page)
        self.assertIn('alt="Portrait of Morning Crumb"', page)
        self.assertIn('alt="Cover photo for Morning Crumb"', page)
        self.assertIn("<h1", page)
        machine = json.loads(__import__("re").search(
            r'<pre id="machinejson">(.*?)</pre>', page, __import__("re").S).group(1))
        self.assertEqual(machine["features_status"]["cover"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "cover.updated" for e in events))

    # ---- gate: the page refuses to render cover it was not given ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.tmp)  # features is a list
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="cover"', page)
        # markup, not the stylesheet: no cover element may render
        self.assertNotIn('<div class="cover"', page)

    def test_refusal_when_declared_but_disabled(self):
        decl = dict(COVER_DECL, enabled=False)
        r, page, manifest = run_assemble(cover_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="cover"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("event") == "cover.updated" for e in events))

    # ---- sanitization: hostile URLs are structured refusals, not renders ----
    def test_url_sanitization_refusals(self):
        bad = [
            "javascript:alert(1)",
            "JaVaScRiPt:alert(1)",
            "java\tscript:alert(1)",
            "vbscript:msgbox(1)",
            "data:text/html;base64,PGI+",
            "data:application/x-shockwave-flash,x",
            "ftp://example.com/x.jpg",
            "file:///etc/passwd",
            "//evil.example/x.jpg",
            "images/relative.jpg",
            "http:///no-host",
            "https://exa mple.com/x.jpg",
        ]
        for field in ("photo_url", "cover_url"):
            for url in bad:
                decl = dict(COVER_DECL, **{field: url})
                r, page, _ = run_assemble(cover_contract(self.tmp, decl), self.tmp)
                self.assertEqual(r.returncode, 2, "url accepted: %r" % url)
                body = json.loads(r.stdout)
                self.assertEqual(body["status"], "refused")
                codes = [e["code"] for e in body["errors"]]
                self.assertIn("unsafe_cover_url", codes, url)
                self.assertNotIn('data-feature="cover"', page)

    def test_data_image_url_allowed(self):
        # image/* data URLs are allowed, incl. svg+xml: loaded via <img>,
        # svg executes no script (secure static context).
        for durl in ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUg==",
                     "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'/%3E"):
            decl = dict(COVER_DECL, photo_url=durl)
            r, page, _ = run_assemble(cover_contract(self.tmp, decl), self.tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn('data-feature="cover"', page)

    # ---- fallback_when_missing: graceful, never an empty src ----
    def test_fallback_when_missing(self):
        decl = {"enabled": True, "name": "Morning Crumb",
                "tagline": "Warm bread · order ahead"}
        r, page, _ = run_assemble(cover_contract(self.tmp, decl), self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="cover"', page)
        self.assertIn("cover-ava-fallback", page)
        self.assertIn(">MC<", page)
        self.assertIn("cover-photo-fallback", page)
        self.assertNotIn('src=""', page)
        cover_block = page.split('data-feature="cover"')[1].split(
            '<div class="cover-who">')[0]
        self.assertNotIn("<img", cover_block)  # banner + avatar areas: no <img> at all

    def test_fallback_initials_shapes(self):
        sys.path.insert(0, os.path.join(SB_DIR, "functions"))
        try:
            from feature_cover import initials_for
        finally:
            sys.path.pop(0)
        self.assertEqual(initials_for("Morning Crumb"), "MC")
        self.assertEqual(initials_for("Bakery"), "B")
        self.assertEqual(initials_for("  a  b  c "), "AB")
        self.assertEqual(initials_for(""), "N")
        self.assertEqual(initials_for(None), "N")

    # ---- malformed declaration: fail closed, not improvised ----
    def test_malformed_declaration_refused(self):
        r, page, _ = run_assemble(
            cover_contract(self.tmp, "yes please"), self.tmp)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_cover_declaration", codes)

    # ---- the general gate: ANY unbuilt breaker fails the contract closed ----
    def test_unbuilt_breaker_refused(self):
        c = json.load(open(SMOKE))
        c["features"] = {"cover": dict(COVER_DECL),
                         "smart_mail": True}  # smart_mail is still specified
        cp = os.path.join(self.tmp, "contract.json")
        json.dump(c, open(cp, "w"))
        r, page, _ = run_assemble(cp, self.tmp)
        self.assertEqual(r.returncode, 2)
        errs = json.loads(r.stdout)["errors"]
        mail_errs = [e for e in errs
                     if e.get("feature") == "feature.smart_mail"]
        self.assertTrue(mail_errs, errs)
        self.assertEqual(mail_errs[0]["code"], "feature_not_built")
        self.assertNotIn('data-feature="cover"', page)  # fail closed: nothing renders

    # ---- registry binding: the contract cannot out-claim the registry ----
    def test_registry_binding_refusal(self):
        tree = os.path.join(self.tmp, "sbcopy")
        shutil.copytree(SB_DIR, tree)
        regp = os.path.join(tree, "functions", "registry.json")
        reg = json.load(open(regp))
        for g in reg["groups"].values():
            for f in g.get("functions", []):
                if f.get("id") == "feature.cover":
                    f["status"] = "specified"
        json.dump(reg, open(regp, "w"), indent=1)
        r, page, _ = run_assemble(
            cover_contract(self.tmp, dict(COVER_DECL)), self.tmp,
            assemble=os.path.join(tree, "assemble.py"))
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)
        self.assertNotIn('data-feature="cover"', page)

    # ---- determinism: same contract -> same bytes ----
    def test_determinism(self):
        contract = cover_contract(self.tmp, dict(COVER_DECL))
        _, page1, _ = run_assemble(contract, self.tmp)
        d2 = tempfile.mkdtemp(prefix="fcover-b-")
        try:
            _, page2, _ = run_assemble(contract, d2)
        finally:
            shutil.rmtree(d2, ignore_errors=True)
        h1 = hashlib.sha256(page1.encode()).hexdigest()
        h2 = hashlib.sha256(page2.encode()).hexdigest()
        self.assertEqual(h1, h2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Rehearsal tests for the unified activation gate (round 2).

LOCAL rehearsals against a fixed truth fixture — they prove the predicate
logic, not enforcement. Real proof is the CI workflow run
(.github/workflows/unified-activation-gate.yml), where the protected runner
resolves truth itself and every adversarial case must be REJECTed.

Round-2 additions: deliverable binding (transplant defense), event-payload
trust root, LOCAL-REHEARSAL labels with exit 3, interim row-7 component
closed-world.
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from activation_gate import (  # noqa: E402
    check, check_receipt, check_delivery, run_design_gate,
    resolve_truth, main as gate_main,
    CANONICAL_SOURCES, SCHEMA, RECEIPT_MARKER_RE,
    _canonical_deliverable_bytes, _safe_repo_path, _is_deliverable)

NOW = datetime(2026, 10, 9, 16, 30, tzinfo=timezone.utc)
MAIN = "2bf25f3e62a71d6001b6796678e04c9fab5d7f5c"
BLOBS = {"design_contract": "a" * 40, "blocks_catalog": "b" * 40}
TRUTH = {"repository": "SoulSchoolAcademy/NayaPOWER", "main_sha": MAIN,
         "source_blobs": BLOBS, "now": NOW}


def mint_receipt_bytes(deliverable_hashes, **over):
    """deliverable_hashes: {path: sha256-of-canonical-bytes}."""
    r = {
        "schema": SCHEMA,
        "status": "ACTIVATED",
        "session_id": "test-session",
        "naya_identity": "test-naya",
        "human_authority": "Shawn",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "job": "test job",
        "gates": ["Usefulness Gate"],
        "proof_plan": "ci run",
        "main_sha": MAIN,
        "activated_at": (NOW - timedelta(hours=1)).isoformat(),
        "loaded": dict(BLOBS),
        "deliverables": [
            {"path": p, "sha256": h} for p, h in deliverable_hashes.items()
        ],
    }
    r.update(over)
    return json.dumps(r, sort_keys=True).encode()


def mint_page(receipt_bytes, body="<html><body>t</body></html>"):
    """Insert the citation marker; returns final page bytes. Mint order:
    page -> hash -> receipt -> marker (converges in one pass because the
    receipt binds the marker-stripped canonical bytes)."""
    digest = hashlib.sha256(receipt_bytes).hexdigest()
    marker = "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s -->" % digest
    return (body.replace("</body>", marker + "</body>")).encode()


def lawful_pair(path="page.html", body="<html><body>t</body></html>"):
    canon = _canonical_deliverable_bytes(body.encode())
    dhash = hashlib.sha256(canon).hexdigest()
    rb = mint_receipt_bytes({path: dhash})
    return rb, mint_page(rb, body)


def run_gate_cli(*argv):
    p = subprocess.run([sys.executable, "-c",
                        "import sys; sys.path.insert(0, %r);"
                        " from activation_gate import main; sys.exit(main())"
                        % os.path.dirname(os.path.abspath(__file__)),
                        *argv], capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


class TestAcceptanceTable(unittest.TestCase):
    def test_lawful_pass(self):
        rb, page = lawful_pair()
        v, viols = check(rb, page, TRUTH)
        self.assertEqual(v, "PASS", viols)

    def test_fabricated_self_asserted_reject(self):
        rb = mint_receipt_bytes({"p.html": "0" * 64}, main_sha="f" * 40)
        v, viols = check(rb, mint_page(rb), TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("TIP_MOVED" in x for x in viols), viols)

    def test_stale_tip_moved_reject(self):
        rb = mint_receipt_bytes({"p.html": "0" * 64}, main_sha="0" * 40)
        v, viols = check(rb, mint_page(rb), TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("TIP_MOVED" in x for x in viols), viols)

    def test_wrong_repository_reject(self):
        rb = mint_receipt_bytes({"p.html": "0" * 64},
                                repository="evil-corp/stolen-repo")
        v, viols = check(rb, mint_page(rb), TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("WRONG_REPOSITORY" in x for x in viols), viols)

    def test_abbreviated_sha_reject(self):
        rb = mint_receipt_bytes({"p.html": "0" * 64}, main_sha=MAIN[:7])
        v, viols = check(rb, mint_page(rb), TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("SHA_MALFORMED" in x for x in viols), viols)

    def test_missing_receipt_reject(self):
        v, viols = check(b"", b"<html></html>", TRUTH)
        self.assertEqual(v, "REJECT")

    def test_tampered_receipt_reject(self):
        rb, page = lawful_pair()
        tampered = rb.replace(b"ACTIVATED", b"ACTIVATED ")
        v, viols = check(tampered, page, TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("CITATION_DIGEST_MISMATCH" in x for x in viols), viols)

    def test_missing_citation_reject(self):
        rb, _page = lawful_pair()
        v, viols = check(rb, b"<html>no marker here</html>", TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("CITATION_MISSING" in x for x in viols), viols)

    def test_unregistered_source_closed_world(self):
        loaded = dict(BLOBS)
        loaded["secret_sauce"] = "c" * 40
        rb = mint_receipt_bytes({"p.html": "0" * 64}, loaded=loaded)
        v, viols = check(rb, mint_page(rb), TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("SOURCE_NOT_REGISTERED" in x for x in viols), viols)

    def test_expired_reject(self):
        rb = mint_receipt_bytes(
            {"p.html": "0" * 64},
            activated_at=(NOW - timedelta(hours=5)).isoformat())
        v, viols = check(rb, mint_page(rb), TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("ACTIVATION_EXPIRED" in x for x in viols), viols)

    def test_future_reject(self):
        rb = mint_receipt_bytes(
            {"p.html": "0" * 64},
            activated_at=(NOW + timedelta(hours=1)).isoformat())
        v, viols = check(rb, mint_page(rb), TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("FUTURE_ACTIVATION" in x for x in viols), viols)

    def test_wrong_schema_v1_reject(self):
        rb = mint_receipt_bytes({"p.html": "0" * 64},
                                schema="naya.activation.receipt.v1")
        v, viols = check(rb, mint_page(rb), TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("WRONG_SCHEMA" in x for x in viols), viols)

    def test_unactivated_reject(self):
        rb = mint_receipt_bytes({"p.html": "0" * 64}, status="PENDING")
        v, viols = check(rb, mint_page(rb), TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("NOT_ACTIVATED" in x for x in viols), viols)

    def test_untrusted_truth_fails_closed(self):
        rb, page = lawful_pair()
        v, viols = check(rb, page,
                         {"repository": "", "main_sha": "", "source_blobs": {},
                          "now": NOW})
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("TRUTH_UNTRUSTED" in x for x in viols), viols)


class TestTransplantDefense(unittest.TestCase):
    def test_receipt_minted_for_A_cannot_ship_B(self):
        rb_a, page_a = lawful_pair("a.html", "<html><body>A</body></html>")
        # attacker ships a DIFFERENT page citing receipt A's marker
        page_b = mint_page(rb_a, "<html><body>B — different bytes</body></html>")
        v, viols = check(rb_a, page_b, TRUTH)
        self.assertEqual(v, "REJECT", viols)
        self.assertTrue(any("DELIVERABLE_BINDING_MISMATCH" in x for x in viols),
                        viols)

    def test_missing_deliverables_list_reject(self):
        r = json.loads(mint_receipt_bytes({"p.html": "0" * 64}).decode())
        del r["deliverables"]
        rb = json.dumps(r, sort_keys=True).encode()
        v, viols = check(rb, mint_page(rb), TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("DELIVERABLES_UNBOUND" in x for x in viols), viols)

    def test_unsafe_deliverable_path_reject(self):
        rb = mint_receipt_bytes({"../evil.html": "0" * 64})
        v, viols = check(rb, mint_page(rb), TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("DELIVERABLE_PATH_UNSAFE" in x for x in viols), viols)
        self.assertFalse(_safe_repo_path("../evil.html"))
        self.assertFalse(_safe_repo_path("/abs/path.html"))
        self.assertTrue(_safe_repo_path("smart-blocks/x.html"))


class TestTrustRoot(unittest.TestCase):
    def _event_file(self, repo_full_name):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump({"repository": {"full_name": repo_full_name}}, f)
        self.addCleanup(os.unlink, path)
        return path

    def test_env_tampered_repo_fails_closed(self):
        """Bypass-2 replay: GITHUB_REPOSITORY=evil-corp/stolen-repo must NOT
        be obeyed — the runner event payload wins and disagreement refuses."""
        ev = self._event_file("SoulSchoolAcademy/NayaPOWER")
        old = dict(os.environ)
        os.environ["GITHUB_EVENT_PATH"] = ev
        os.environ["GITHUB_REPOSITORY"] = "evil-corp/stolen-repo"
        os.environ["GITHUB_TOKEN"] = "x" * 10
        try:
            with self.assertRaises(RuntimeError) as cm:
                resolve_truth()
        finally:
            os.environ.clear()
            os.environ.update(old)
        self.assertIn("disagrees", str(cm.exception))

    def test_missing_event_context_fails_closed(self):
        old = dict(os.environ)
        os.environ.pop("GITHUB_EVENT_PATH", None)
        try:
            with self.assertRaises(RuntimeError):
                resolve_truth()
        finally:
            os.environ.clear()
            os.environ.update(old)


class TestLocalLabels(unittest.TestCase):
    def test_local_verdict_has_no_pass_substring_and_exits_3(self):
        d = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        rb, page = lawful_pair()
        rp = os.path.join(d, "r.json")
        dp = os.path.join(d, "p.html")
        tp = os.path.join(d, "truth.json")
        open(rp, "wb").write(rb)
        open(dp, "wb").write(page)
        json.dump({"repository": "SoulSchoolAcademy/NayaPOWER",
                   "main_sha": MAIN, "source_blobs": BLOBS,
                   "now": NOW.isoformat()}, open(tp, "w"))
        code, out = run_gate_cli("--receipt", rp, "--deliverable", dp,
                                 "--mode", "local", "--truth", tp, "--json")
        data = json.loads(out.splitlines()[-1])
        self.assertEqual(code, 3, out)
        self.assertEqual(data["verdict"], "LOCAL-REHEARSAL-UNVERIFIED", out)
        self.assertNotIn("PASS", data["verdict"])

    def test_local_reject_also_exits_3(self):
        d = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        rb = mint_receipt_bytes({"p.html": "0" * 64}, main_sha="f" * 40)
        rp = os.path.join(d, "r.json")
        dp = os.path.join(d, "p.html")
        tp = os.path.join(d, "truth.json")
        open(rp, "wb").write(rb)
        open(dp, "wb").write(mint_page(rb))
        json.dump({"repository": "SoulSchoolAcademy/NayaPOWER",
                   "main_sha": MAIN, "source_blobs": BLOBS,
                   "now": NOW.isoformat()}, open(tp, "w"))
        code, out = run_gate_cli("--receipt", rp, "--deliverable", dp,
                                 "--mode", "local", "--truth", tp, "--json")
        data = json.loads(out.splitlines()[-1])
        self.assertEqual(code, 3, out)
        self.assertEqual(data["verdict"], "LOCAL-REHEARSAL-REJECTED", out)
        self.assertNotIn("PASS", data["verdict"])


class TestDeliveryPredicate(unittest.TestCase):
    def _stub_design_gate(self, d, fail=False):
        """A stub design-lane gate: exits 0, or 1 with an \u2715 violation line."""
        p = os.path.join(d, "design_gate_stub.py")
        body = ("import sys; print('  \u2715 NO FREESTYLE: stub violation'); "
                "sys.exit(1)") if fail else "import sys; sys.exit(0)"
        open(p, "w").write(body)
        mf = os.path.join(d, "manifest.json")
        open(mf, "w").write("{}")
        return p, mf

    def _setup(self, pages, design_fail=False):
        d = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        dg, mf = self._stub_design_gate(d, fail=design_fail)
        self._dg, self._mf = dg, mf
        # mint one receipt binding ALL pages (canonical bytes), then add markers
        hashes = {p: hashlib.sha256(_canonical_deliverable_bytes(b.encode())).hexdigest()
                  for p, b in pages.items()}
        rb = mint_receipt_bytes(hashes)
        for p, b in pages.items():
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, "wb").write(mint_page(rb, b))
        # write the receipt into the conventional PR-head location
        rdir = os.path.join(d, ".naya", "activation")
        os.makedirs(rdir, exist_ok=True)
        open(os.path.join(rdir, "receipt.json"), "wb").write(rb)
        return d, rb

    def test_lawful_delivery_pass(self):
        d, rb = self._setup({"page.html": "<html><body>x</body></html>"})
        v, viols = check_delivery(rb, d, ["page.html"], TRUTH,
                                  self._dg, self._mf)
        self.assertEqual(v, "PASS", viols)

    def test_delivery_transplant_reject(self):
        d, rb = self._setup({"a.html": "<html><body>A</body></html>"})
        # PR changes b.html too, but the receipt only binds a.html
        open(os.path.join(d, "b.html"), "wb").write(mint_page(rb, "<html><body>B</body></html>"))
        v, viols = check_delivery(rb, d, ["a.html", "b.html"], TRUTH,
                                  self._dg, self._mf)
        self.assertEqual(v, "REJECT", viols)
        self.assertTrue(any("DELIVERABLE_NOT_BOUND" in x for x in viols), viols)

    def test_delivery_missing_receipt_bytes(self):
        v, viols = check_delivery(b"", "/tmp", ["page.html"], TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("RECEIPT_MISSING_OR_EMPTY" in x for x in viols), viols)

    def test_delivery_design_gate_reject_folded(self):
        """Row 7 delegate-and-verify: the design lane's verdict folds in."""
        d, rb = self._setup({"evil.html": "<html><body>x</body></html>"},
                            design_fail=True)
        v, viols = check_delivery(rb, d, ["evil.html"], TRUTH,
                                  self._dg, self._mf)
        self.assertEqual(v, "REJECT", viols)
        self.assertTrue(any("DESIGN_GATE:" in x for x in viols), viols)

    def test_delivery_design_gate_absent_fails_closed(self):
        """No design gate available -> REJECT, never a silent pass."""
        d, rb = self._setup({"page.html": "<html><body>x</body></html>"})
        v, viols = check_delivery(rb, d, ["page.html"], TRUTH, "", "")
        self.assertEqual(v, "REJECT", viols)
        self.assertTrue(any("DESIGN_GATE_UNAVAILABLE" in x for x in viols),
                        viols)

    def test_delivery_non_deliverable_change_ignored(self):
        d, rb = self._setup({"page.html": "<html><body>x</body></html>"})
        v, viols = check_delivery(rb, d, ["page.html", "tools/helper.py"], TRUTH,
                                  self._dg, self._mf)
        self.assertEqual(v, "PASS", viols)

    def test_is_deliverable(self):
        self.assertTrue(_is_deliverable("smart-blocks/manifest.json"))
        self.assertTrue(_is_deliverable("pages/room.html"))
        self.assertFalse(_is_deliverable("tools/gate.py"))
        self.assertFalse(_is_deliverable("BRAIN/note.md"))


class TestDesignGateDelegation(unittest.TestCase):
    def test_run_design_gate_pass(self):
        d = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        gp = os.path.join(d, "g.py")
        open(gp, "w").write("import sys; sys.exit(0)")
        mp = os.path.join(d, "m.json")
        open(mp, "w").write("{}")
        self.assertEqual(run_design_gate("/tmp/x.html", gp, mp), [])

    def test_run_design_gate_violations_parsed(self):
        d = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        gp = os.path.join(d, "g.py")
        open(gp, "w").write(
            "import sys; print('  \u2715 NO FREESTYLE: bad class'); sys.exit(1)")
        mp = os.path.join(d, "m.json")
        open(mp, "w").write("{}")
        v = run_design_gate("/tmp/x.html", gp, mp)
        self.assertTrue(any("NO FREESTYLE" in x for x in v), v)

    def test_run_design_gate_absent(self):
        v = run_design_gate("/tmp/x.html", "", "")
        self.assertTrue(any("DESIGN_GATE_UNAVAILABLE" in x for x in v), v)


if __name__ == "__main__":
    unittest.main(verbosity=2)

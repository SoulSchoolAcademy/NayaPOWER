#!/usr/bin/env python3
"""Rehearsal tests for the unified activation gate (merged hotfix, 2026-10-09).

These are LOCAL rehearsals against a fixed truth fixture — they prove the
predicate logic, not enforcement. Real proof is the CI workflow run
(.github/workflows/unified-activation-gate.yml), where the protected runner
resolves truth itself and every adversarial case must be REJECTed.

Hotfix additions (attack report #1354 comment 6085944401, two holes on the
merged bytes 302aab70):
  - deliverable binding: a receipt minted for one deliverable cannot ship
    another (transplant -> DELIVERABLE_BINDING_MISMATCH; unbound receipts
    fail closed with DELIVERABLES_UNBOUND).
  - local-mode label discipline: LOCAL-REHEARSAL-* verdicts never contain
    the substring "PASS"; local mode always exits 3.
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from activation_gate import (  # noqa: E402
    check, canonical_deliverable_bytes, CANONICAL_SOURCES, SCHEMA)

NOW = datetime(2026, 10, 9, 16, 30, tzinfo=timezone.utc)
MAIN = "2bf25f3e62a71d6001b6796678e04c9fab5d7f5c"
BLOBS = {"design_contract": "a" * 40, "blocks_catalog": "b" * 40}
TRUTH = {"repository": "SoulSchoolAcademy/NayaPOWER", "main_sha": MAIN,
         "source_blobs": BLOBS, "now": NOW}


def make_receipt(**over):
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
    }
    r.update(over)
    return r


def deliverable_for(receipt_bytes):
    digest = hashlib.sha256(receipt_bytes).hexdigest()
    return "<html><!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></html>" % digest


def bind_receipt(receipt, path="deliverable.html"):
    """Two-phase mint dance: the marker cites the receipt bytes; the receipt
    binds the canonical (marker-stripped) deliverable bytes. Returns
    (receipt_bytes, deliverable_text)."""
    rb1 = json.dumps(receipt, sort_keys=True).encode()
    d1 = deliverable_for(rb1)
    canon = canonical_deliverable_bytes(d1)
    receipt["deliverables"] = [
        {"path": path, "sha256": hashlib.sha256(canon).hexdigest()}]
    rb2 = json.dumps(receipt, sort_keys=True).encode()
    d2 = deliverable_for(rb2)
    # Canonical bytes are marker-independent: binding survives re-marking.
    assert hashlib.sha256(canonical_deliverable_bytes(d2)).hexdigest() == \
        receipt["deliverables"][0]["sha256"]
    return rb2, d2


def run(receipt, truth=TRUTH, deliverable=None):
    rb, d = bind_receipt(receipt)
    if deliverable is not None:
        d = deliverable
    return check(rb, d, truth)


class TestAcceptanceTable(unittest.TestCase):
    def test_lawful_pass(self):
        v, viols = run(make_receipt())
        self.assertEqual(v, "PASS", viols)

    def test_fabricated_self_asserted_reject(self):
        r = make_receipt(status="ACTIVATED")
        r["main_sha"] = "f" * 40  # plausible-looking but not live main
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("TIP_MOVED" in x for x in viols), viols)

    def test_stale_tip_moved_reject(self):
        r = make_receipt(main_sha="0" * 40)
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("TIP_MOVED" in x for x in viols), viols)

    def test_wrong_repository_reject(self):
        r = make_receipt(repository="evil-corp/stolen-repo")
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("WRONG_REPOSITORY" in x for x in viols), viols)

    def test_abbreviated_sha_reject(self):
        r = make_receipt(main_sha=MAIN[:7])
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("SHA_MALFORMED" in x for x in viols), viols)

    def test_missing_receipt_reject(self):
        v, viols = check(b"", "<html></html>", TRUTH)
        self.assertEqual(v, "REJECT")

    def test_tampered_receipt_reject(self):
        r = make_receipt()
        rb, d = bind_receipt(r)
        tampered = rb.replace(b"ACTIVATED", b"ACTIVATED ")
        v, viols = check(tampered, d, TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("CITATION_DIGEST_MISMATCH" in x for x in viols), viols)

    def test_missing_citation_reject(self):
        r = make_receipt()
        rb, d = bind_receipt(r)
        v, viols = check(rb, "<html>no marker here</html>", TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("CITATION_MISSING" in x for x in viols), viols)

    def test_unregistered_source_closed_world(self):
        loaded = dict(BLOBS)
        loaded["secret_sauce"] = "c" * 40
        r = make_receipt(loaded=loaded)
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("SOURCE_NOT_REGISTERED" in x for x in viols), viols)

    def test_missing_source_reject(self):
        loaded = {"design_contract": "a" * 40}
        r = make_receipt(loaded=loaded)
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("SOURCE_MISSING" in x for x in viols), viols)

    def test_fingerprint_mismatch_reject(self):
        loaded = {"design_contract": "d" * 40, "blocks_catalog": "b" * 40}
        r = make_receipt(loaded=loaded)
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("SOURCE_FINGERPRINT_MISMATCH" in x for x in viols), viols)

    def test_expired_reject(self):
        r = make_receipt(activated_at=(NOW - timedelta(hours=5)).isoformat())
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("ACTIVATION_EXPIRED" in x for x in viols), viols)

    def test_future_reject(self):
        r = make_receipt(activated_at=(NOW + timedelta(hours=1)).isoformat())
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("FUTURE_ACTIVATION" in x for x in viols), viols)

    def test_wrong_schema_v1_reject(self):
        r = make_receipt(schema="naya.activation.receipt.v1")
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("WRONG_SCHEMA" in x for x in viols), viols)

    def test_unactivated_reject(self):
        r = make_receipt(status="PENDING")
        v, viols = run(r)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("NOT_ACTIVATED" in x for x in viols), viols)

    def test_untrusted_truth_fails_closed(self):
        r = make_receipt()
        rb, d = bind_receipt(r)
        v, viols = check(rb, d,
                         {"repository": "", "main_sha": "", "source_blobs": {},
                          "now": NOW})
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("TRUTH_UNTRUSTED" in x for x in viols), viols)

    def test_repo_case_insensitive(self):
        r = make_receipt(repository="soulschoolacademy/nayapower")
        v, viols = run(r)
        self.assertEqual(v, "PASS", viols)


class TestDeliverableBinding(unittest.TestCase):
    """Hotfix, hole 2: a receipt minted for one deliverable must not ship
    another. Attack report #1354 comment 6085944401."""

    def test_transplant_different_deliverable_reject(self):
        # Attack: receipt minted for deliverable A; the valid marker is
        # copied onto deliverable B's bytes. Same marker, different canonical
        # bytes -> the transplant must be rejected even though the citation
        # check passes.
        r = make_receipt()
        rb, d = bind_receipt(r)
        marker_start = d.index("<!--")
        other = ("<html><body>PRODUCTION DEPLOY ARTIFACT</body>"
                 + d[marker_start:])
        v, viols = check(rb, other, TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("DELIVERABLE_BINDING_MISMATCH" in x for x in viols),
                        viols)

    def test_unbound_receipt_reject(self):
        # make_receipt() never sets deliverables[]; without the binding the
        # receipt must fail closed.
        r = make_receipt()
        rb = json.dumps(r, sort_keys=True).encode()
        d = deliverable_for(rb)
        v, viols = check(rb, d, TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("DELIVERABLES_UNBOUND" in x for x in viols), viols)

    def test_malformed_entry_reject(self):
        r = make_receipt()
        r["deliverables"] = [{"path": "deliverable.html",
                             "sha256": "not-a-hash"}]
        rb = json.dumps(r, sort_keys=True).encode()
        d = deliverable_for(rb)
        v, viols = check(rb, d, TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("DELIVERABLE_SHA_MALFORMED" in x for x in viols),
                        viols)

    def test_unsafe_path_reject(self):
        r = make_receipt()
        r["deliverables"] = [{"path": "../escape.html",
                             "sha256": "f" * 64}]
        rb = json.dumps(r, sort_keys=True).encode()
        d = deliverable_for(rb)
        v, viols = check(rb, d, TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("DELIVERABLE_PATH_UNSAFE" in x for x in viols),
                        viols)

    def test_canonical_strips_marker(self):
        a = "<html><!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --><p>x</p></html>" \
            % ("0" * 64)
        b = "<html><!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --><p>x</p></html>" \
            % ("f" * 64)
        self.assertEqual(canonical_deliverable_bytes(a),
                         canonical_deliverable_bytes(b))
        self.assertNotIn(b"NAYA-ACTIVATION", canonical_deliverable_bytes(a))

    def test_binding_matches_one_of_several_entries(self):
        # A receipt may scope several deliverables; the presented one only
        # needs to match ONE entry.
        r = make_receipt()
        rb, d = bind_receipt(r, path="a.html")
        receipt = json.loads(rb)
        second = "<html><body>second page</body></html>"
        receipt["deliverables"].append(
            {"path": "b.html",
             "sha256": hashlib.sha256(
                 canonical_deliverable_bytes(second)).hexdigest()})
        rb2 = json.dumps(receipt, sort_keys=True).encode()
        d2 = deliverable_for(rb2).replace("</html>", "<body>second page</body></html>")
        v, viols = check(rb2, d2, TRUTH)
        self.assertEqual(v, "PASS", viols)


def run_gate_cli(*argv):
    p = subprocess.run(
        [sys.executable, os.path.join(HERE, "activation_gate.py"), *argv],
        capture_output=True, text=True)
    return p.returncode, p.stdout


class TestLocalLabels(unittest.TestCase):
    """Hotfix, hole 1: local mode must never exit 0 and no local verdict may
    contain the substring "PASS". Attack report #1354 comment 6085944401."""

    def _local_run(self, receipt, deliverable_text):
        d = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        rp = os.path.join(d, "r.json")
        dp = os.path.join(d, "p.html")
        tp = os.path.join(d, "truth.json")
        with open(rp, "wb") as f:
            f.write(receipt)
        with open(dp, "w") as f:
            f.write(deliverable_text)
        with open(tp, "w") as f:
            json.dump({"repository": "SoulSchoolAcademy/NayaPOWER",
                       "main_sha": MAIN, "source_blobs": BLOBS,
                       "now": NOW.isoformat()}, f)
        return run_gate_cli("--receipt", rp, "--deliverable", dp,
                            "--mode", "local", "--truth", tp, "--json")

    def test_local_verdict_has_no_pass_substring_and_exits_3(self):
        # A self-minted truth whose rows hold: the predicate "passes", but
        # the verdict must not be passable and the exit must not be 0.
        rb, page = bind_receipt(make_receipt())
        code, out = self._local_run(rb, page)
        data = json.loads(out.splitlines()[-1])
        self.assertEqual(code, 3, out)
        self.assertEqual(data["verdict"], "LOCAL-REHEARSAL-UNVERIFIED", out)
        self.assertNotIn("PASS", data["verdict"])

    def test_local_reject_also_exits_3(self):
        r = make_receipt(main_sha="f" * 40)  # self-asserted, not live main
        rb = json.dumps(r, sort_keys=True).encode()
        d = deliverable_for(rb)
        code, out = self._local_run(rb, d)
        data = json.loads(out.splitlines()[-1])
        self.assertEqual(code, 3, out)
        self.assertEqual(data["verdict"], "LOCAL-REHEARSAL-REJECTED", out)
        self.assertNotIn("PASS", data["verdict"])

    def test_naive_consumer_cannot_mistake_local_for_pass(self):
        # The exact consumer patterns from the attack report: exit code and
        # substring checks.
        rb, page = bind_receipt(make_receipt())
        code, out = self._local_run(rb, page)
        data = json.loads(out.splitlines()[-1])
        verdict = data["verdict"]
        self.assertNotEqual(code, 0)            # not a protected PASS
        self.assertNotEqual(verdict, "PASS")
        self.assertFalse("PASS" in verdict)     # substring check
        self.assertFalse(verdict.endswith("PASS"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

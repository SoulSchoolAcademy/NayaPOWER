#!/usr/bin/env python3
"""Rehearsal tests for the unified activation gate (round-2 hardened).

These are LOCAL rehearsals against a fixed truth fixture — they prove the
predicate logic, not enforcement. Real proof is the CI workflow run
(.github/workflows/unified-activation-gate.yml), where the protected runner
resolves truth itself and every adversarial case must be REJECTed.

Round-2 additions: deliverable binding (transplant rejection), job binding,
CANDIDATE-LOCAL label discipline (no "PASS" substring), design-gate
delegation plumbing, canonical-deliverable unit tests.
"""

import hashlib
import json
import os
import stat
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from activation_gate import (  # noqa: E402
    check, canonical_deliverable_bytes, run_design_gate, CANONICAL_SOURCES,
    SCHEMA)

NOW = datetime(2026, 10, 9, 16, 30, tzinfo=timezone.utc)
MAIN = "2bf25f3e62a71d6001b6796678e04c9fab5d7f5c"
BLOBS = {"design_contract": "a" * 40, "blocks_catalog": "b" * 40}
TRUTH = {"repository": "SoulSchoolAcademy/NayaPOWER", "main_sha": MAIN,
         "source_blobs": BLOBS, "now": NOW}
JOB = "prove the unified activation gate in CI"


def make_receipt(**over):
    r = {
        "schema": SCHEMA,
        "status": "ACTIVATED",
        "session_id": "test-session",
        "naya_identity": "test-naya",
        "human_authority": "Shawn",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "job": JOB,
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


def bind_receipt(receipt):
    """Two-phase mint dance: marker cites receipt bytes; receipt binds the
    canonical deliverable bytes. Returns (receipt_bytes, deliverable_text)."""
    rb1 = json.dumps(receipt, sort_keys=True).encode()
    d1 = deliverable_for(rb1)
    canon = canonical_deliverable_bytes(d1)
    receipt["deliverable_sha256"] = hashlib.sha256(canon).hexdigest()
    rb2 = json.dumps(receipt, sort_keys=True).encode()
    d2 = deliverable_for(rb2)
    # Canonical bytes are marker-independent: binding survives re-marking.
    assert canonical_deliverable_bytes(d2) == canon
    return rb2, d2


def run(receipt, truth=TRUTH, deliverable=None, job=JOB):
    rb, d = bind_receipt(receipt)
    if deliverable is not None:
        d = deliverable
    delivery = {"job": job,
                "deliverable_sha256": hashlib.sha256(
                    canonical_deliverable_bytes(d)).hexdigest()}
    return check(rb, d, truth, delivery=delivery)


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
    """Round-2, hole 4: a receipt for one deliverable must not ship another."""

    def test_transplant_different_deliverable_reject(self):
        # Attacker's A2: receipt minted for job A's page, marker copied onto
        # job B's page ("PRODUCTION DEPLOY ARTIFACT"). Same marker, different
        # canonical bytes -> transplant must be rejected.
        r = make_receipt()
        rb, d = bind_receipt(r)
        marker_start = d.index("<!--")
        other = "<html><body>PRODUCTION DEPLOY ARTIFACT</body>" + d[marker_start:]
        v, viols = check(rb, other, TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("DELIVERABLE_DIGEST_MISMATCH" in x for x in viols),
                        viols)

    def test_unbound_receipt_reject(self):
        # make_receipt() never sets deliverable_sha256; without bind_receipt
        # the receipt is unbound and must fail closed.
        r = make_receipt()
        rb = json.dumps(r, sort_keys=True).encode()
        d = deliverable_for(rb)
        v, viols = check(rb, d, TRUTH)
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("RECEIPT_UNBOUND" in x for x in viols), viols)

    def test_job_mismatch_reject(self):
        r = make_receipt()
        v, viols = run(r, job="PRODUCTION DEPLOY ARTIFACT")
        self.assertEqual(v, "REJECT")
        self.assertTrue(any("RECEIPT_JOB_MISMATCH" in x for x in viols), viols)

    def test_job_match_pass(self):
        v, viols = run(make_receipt(), job=JOB)
        self.assertEqual(v, "PASS", viols)

    def test_canonical_strips_marker(self):
        a = "<html><!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --><p>x</p></html>" % ("0" * 64)
        b = "<html><!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --><p>x</p></html>" % ("f" * 64)
        self.assertEqual(canonical_deliverable_bytes(a),
                         canonical_deliverable_bytes(b))
        self.assertNotIn(b"NAYA-ACTIVATION", canonical_deliverable_bytes(a))


class TestDesignGateDelegation(unittest.TestCase):
    """Round-2, hole 3: delegation plumbing — never a silent pass-through."""

    def _stub_gate(self, exit_code, stdout):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "design_gate.py")
        with open(p, "w") as f:
            f.write("#!/usr/bin/env python3\nimport sys\n"
                    "print(%r)\nsys.exit(%d)\n" % (stdout, exit_code))
        os.chmod(p, os.stat(p).st_mode | stat.S_IEXEC)
        m = os.path.join(d, "manifest.json")
        with open(m, "w") as f:
            f.write("{}")
        return p, m

    def test_absent_gate_reports_absent(self):
        v = run_design_gate("/tmp/x.html", "/nonexistent/dg.py",
                            "/nonexistent/m.json")
        self.assertEqual(v, ["DESIGN_GATE_ABSENT"])

    def test_passing_gate_no_violations(self):
        p, m = self._stub_gate(0, "DESIGN GATE: PASS")
        self.assertEqual(run_design_gate("/tmp/x.html", p, m), [])

    def test_failing_gate_violations_prefixed(self):
        p, m = self._stub_gate(1, "  \u2715 FREESTYLE-COMPONENT: naya-evil-widget")
        v = run_design_gate("/tmp/x.html", p, m)
        self.assertTrue(any(x.startswith("DESIGN_GATE:") and
                            "FREESTYLE-COMPONENT" in x for x in v), v)


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Tests for check_activation_receipt.py — Law 4.1.

3 passing + 3 failing cases. Stdlib only (unittest).
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

CHECK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "check_activation_receipt.py")

VALID = {
    "schema": "naya.activation.receipt.v1",
    "status": "ACTIVATED",
    "naya_identity": "Naya 4",
    "human_director": "Shawn Vibert",
    "authority": "activation protocol v1",
    "repository": "SoulSchoolAcademy/NayaPOWER",
    "timestamp": "2026-10-09T18:00:00-07:00",
    "verification": {"status": "VERIFIED", "evidence": ["read AGENTS.md", "read boot contract"]},
}


def run_check(workdir):
    return subprocess.run(
        [sys.executable, CHECK, "--workdir", workdir],
        capture_output=True, text=True)


def write_receipt(workdir, name, obj):
    path = os.path.join(workdir, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f)
    return path


class TestActivationReceipt(unittest.TestCase):
    # ---- passing cases ----
    def test_pass_valid_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            write_receipt(d, "ACTIVATION-RECEIPT.json", VALID)
            r = run_check(d)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("PASSED", r.stdout)

    def test_pass_dated_receipt_name(self):
        with tempfile.TemporaryDirectory() as d:
            write_receipt(d, "ACTIVATION-RECEIPT-2026-10-09.json", VALID)
            r = run_check(d)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_pass_extra_fields_ignored(self):
        with tempfile.TemporaryDirectory() as d:
            obj = dict(VALID)
            obj["notes"] = "extra fields must not break a valid receipt"
            write_receipt(d, "ACTIVATION-RECEIPT.json", obj)
            r = run_check(d)
            self.assertEqual(r.returncode, 0, r.stdout)

    # ---- failing cases ----
    def test_fail_no_receipt_file(self):
        with tempfile.TemporaryDirectory() as d:
            r = run_check(d)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("no activation receipt found", r.stdout)

    def test_fail_unactivated_status(self):
        with tempfile.TemporaryDirectory() as d:
            obj = dict(VALID)
            obj["status"] = "UNACTIVATED"
            write_receipt(d, "ACTIVATION-RECEIPT.json", obj)
            r = run_check(d)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("UNACTIVATED", r.stdout)

    def test_fail_missing_human_director(self):
        with tempfile.TemporaryDirectory() as d:
            obj = dict(VALID)
            obj["human_director"] = None
            write_receipt(d, "ACTIVATION-RECEIPT.json", obj)
            r = run_check(d)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("human_director", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)

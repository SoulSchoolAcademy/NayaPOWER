"""Hermetic tests for tools/trial_evidence_freeze.py.

Every test runs against fresh temp dirs; no repo state, no network.
Run: python3 tests/test_trial_evidence_freeze.py
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools", "trial_evidence_freeze.py")
# When run from a standalone checkout of this pair, fall back to the sibling dir.
if not os.path.isfile(TOOL):
    TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trial_evidence_freeze.py")


def run_tool(*argv):
    return subprocess.run(
        [sys.executable, TOOL, *argv],
        capture_output=True, text=True, timeout=60,
    )


def make_trial_source(tmp):
    src = os.path.join(tmp, "src")
    os.makedirs(os.path.join(src, "agents", "cold"))
    with open(os.path.join(src, "RESULTS.md"), "w") as f:
        f.write("# Trial 4 results\ncold 0/10, bridge 8/10\n")
    with open(os.path.join(src, "agents", "cold", "a01.json"), "w") as f:
        json.dump({"arm": "cold", "score": 0}, f)
    with open(os.path.join(src, "raw.bin"), "wb") as f:
        f.write(bytes(range(256)) * 4)
    return src


def write_claims(tmp):
    path = os.path.join(tmp, "claims.json")
    with open(path, "w") as f:
        json.dump({"claim": "bridge notes raise cold-successor task success 0/10 -> 8/10",
                   "metrics": {"cold": 0, "bridge": 8}}, f)
    return path


class TestFreeze(unittest.TestCase):
    def test_freeze_copies_byte_identical_and_manifests(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = make_trial_source(tmp)
            dest = os.path.join(tmp, "trials")
            r = run_tool("freeze", "--trial-id", "T9", "--source-dir", src,
                         "--claims", write_claims(tmp), "--dest-root", dest)
            self.assertEqual(r.returncode, 0, r.stderr)
            man_path = os.path.join(dest, "T9", "manifest.json")
            self.assertTrue(os.path.isfile(man_path))
            man = json.load(open(man_path))
            self.assertEqual(man["schema"], "NAYAPOWER_TRIAL_EVIDENCE_MANIFEST_V1")
            self.assertEqual(man["trial_id"], "T9")
            self.assertEqual(man["file_count"], 3)
            self.assertEqual(man["claims"]["metrics"]["bridge"], 8)
            for entry in man["files"]:
                raw = os.path.join(dest, "T9", "raw", *entry["path"].split("/"))
                orig = os.path.join(src, *entry["path"].split("/"))
                self.assertTrue(os.path.isfile(raw), entry["path"])
                self.assertEqual(open(raw, "rb").read(), open(orig, "rb").read(),
                                 f"byte mismatch: {entry['path']}")
                self.assertEqual(entry["bytes"], os.path.getsize(raw))

    def test_freeze_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = make_trial_source(tmp)
            dest = os.path.join(tmp, "trials")
            claims = write_claims(tmp)
            r1 = run_tool("freeze", "--trial-id", "T9", "--source-dir", src,
                          "--claims", claims, "--dest-root", dest)
            self.assertEqual(r1.returncode, 0, r1.stderr)
            r2 = run_tool("freeze", "--trial-id", "T9", "--source-dir", src,
                          "--claims", claims, "--dest-root", dest)
            self.assertEqual(r2.returncode, 2)
            self.assertIn("REFUSED", r2.stderr)

    def test_freeze_rejects_bad_claims_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = make_trial_source(tmp)
            bad = os.path.join(tmp, "bad.json")
            with open(bad, "w") as fh:
                fh.write("{not json")
            r = run_tool("freeze", "--trial-id", "T9", "--source-dir", src,
                         "--claims", bad, "--dest-root", os.path.join(tmp, "t"))
            self.assertEqual(r.returncode, 1)

    def test_freeze_rejects_empty_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            empty = os.path.join(tmp, "empty")
            os.makedirs(empty)
            r = run_tool("freeze", "--trial-id", "T9", "--source-dir", empty,
                         "--claims", write_claims(tmp), "--dest-root", os.path.join(tmp, "t"))
            self.assertEqual(r.returncode, 1)


class TestVerify(unittest.TestCase):
    def _frozen(self, tmp, trial_id="T9"):
        src = make_trial_source(tmp)
        dest = os.path.join(tmp, "trials")
        r = run_tool("freeze", "--trial-id", trial_id, "--source-dir", src,
                     "--claims", write_claims(tmp), "--dest-root", dest)
        self.assertEqual(r.returncode, 0, r.stderr)
        return dest

    def test_verify_intact(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = self._frozen(tmp)
            r = run_tool("verify", "--trial-id", "T9", "--dest-root", dest)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("intact", r.stdout)

    def test_verify_detects_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = self._frozen(tmp)
            raw = os.path.join(dest, "T9", "raw", "RESULTS.md")
            with open(raw, "a") as f:
                f.write("sneaky edit\n")
            r = run_tool("verify", "--trial-id", "T9", "--dest-root", dest)
            self.assertEqual(r.returncode, 1)
            self.assertIn("TAMPERED", r.stderr)

    def test_verify_detects_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = self._frozen(tmp)
            os.remove(os.path.join(dest, "T9", "raw", "raw.bin"))
            r = run_tool("verify", "--trial-id", "T9", "--dest-root", dest)
            self.assertEqual(r.returncode, 1)
            self.assertIn("MISSING", r.stderr)

    def test_verify_detects_unrecorded_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = self._frozen(tmp)
            planted = os.path.join(dest, "T9", "raw", "planted.md")
            with open(planted, "w") as fh:
                fh.write("x")
            r = run_tool("verify", "--trial-id", "T9", "--dest-root", dest)
            self.assertEqual(r.returncode, 1)
            self.assertIn("UNRECORDED", r.stderr)

    def test_verify_missing_trial(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run_tool("verify", "--trial-id", "NOPE", "--dest-root", os.path.join(tmp, "t"))
            self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

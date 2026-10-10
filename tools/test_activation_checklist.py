#!/usr/bin/env python3
"""Tests for Gate 1 — the Activation Checklist Verifier.

Proves the predicate logic, including adversarial cases:
  - fake lesson list (unregistered ids) -> REJECT
  - partial loading (fewer than 14)    -> REJECT
  - forged/stale lesson content         -> REJECT
  - stale V2 bytes                      -> REJECT
  - missing V2 file                     -> TOOL-ERROR (fail closed)

Fixtures are the REAL canonical artifacts (curriculum from the repo
checkout, V2 files from origin/brain-build/operating-code-v2 via git show),
so a pass means the embedded pins match live bytes — the meta-test
test_embedded_pins_match_live_canonical guards the pins against
transcription error.
"""

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import activation_checklist as ac  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2_BRANCH = "origin/brain-build/operating-code-v2"

ALL_IDS = ["L%d" % i for i in range(1, 15)]


def _ensure_ref(ref):
    """Make sure a remote ref exists locally, fetching it when the clone
    lacks it. CI checks out a shallow single ref, so origin/* branches for
    the V2 trust root are absent unless fetched. The gate still verifies
    live bytes — this only ensures they are reachable."""
    branch = ref.split(":", 1)[0]
    name = branch[7:] if branch.startswith("origin/") else branch
    v = subprocess.run(["git", "rev-parse", "--verify", "--quiet", branch],
                       cwd=REPO_ROOT, capture_output=True, timeout=60)
    if v.returncode != 0:
        f = subprocess.run(["git", "fetch", "origin", name],
                           cwd=REPO_ROOT, capture_output=True, timeout=120)
        assert f.returncode == 0, "git fetch failed for %s" % name


def _git_show(rev_path):
    _ensure_ref(rev_path)
    p = subprocess.run(["git", "show", rev_path], cwd=REPO_ROOT,
                       capture_output=True, timeout=60)
    assert p.returncode == 0, "git show failed: %s" % rev_path
    return p.stdout


def _materialize_tree(mutate=None):
    """Temp dir holding canonical artifacts; mutate(canonical_dict, paths)
    may tamper before return. Returns (tmpdir, canonical)."""
    tmp = tempfile.mkdtemp(prefix="checklist-fixture-")
    naya = os.path.join(tmp, "NAYA-ACTIVATION")
    gov = os.path.join(tmp, "BRAIN", "01-GOVERNANCE")
    os.makedirs(naya)
    os.makedirs(gov)
    with open(os.path.join(REPO_ROOT, ac.CURRICULUM_JSON), "rb") as f:
        curric_raw = f.read()
    with open(os.path.join(naya, "thinking-curriculum.json"), "wb") as f:
        f.write(curric_raw)
    shutil.copy(os.path.join(REPO_ROOT, ac.CURRICULUM_HUMAN_MD),
                os.path.join(naya, "THINKING-CURRICULUM-V1.md"))
    for rel in ac.V2_FILES:
        blob = _git_show("%s:%s" % (V2_BRANCH, rel))
        with open(os.path.join(tmp, *rel.split("/")), "wb") as f:
            f.write(blob)
    canonical, err = ac.load_canonical(tmp)
    assert err == "", err
    if mutate:
        mutate(canonical, tmp)
    return tmp, canonical


def _good_claim(canonical):
    return {
        "agent_id": "naya-test",
        "claimed_at": "2026-10-10T01:30:00Z",
        "lessons": [{"lesson_id": lid, "sha256": canonical["lesson_hashes"][lid]}
                    for lid in ALL_IDS],
        "v2": dict(canonical["v2_hashes"]),
    }


class TestPins(unittest.TestCase):
    def test_embedded_pins_match_live_canonical(self):
        """The pins baked into the verifier equal the live canonical bytes.
        Catches transcription error in the pin table itself."""
        tmp, canonical = _materialize_tree()
        try:
            for lid in ALL_IDS:
                self.assertEqual(canonical["lesson_hashes"][lid],
                                 ac.CURRICULUM_LESSON_PINS[lid],
                                 "pin mismatch for %s" % lid)
            for rel in ac.V2_FILES:
                self.assertEqual(canonical["v2_hashes"][rel],
                                 ac.V2_FILE_PINS[rel],
                                 "V2 pin mismatch for %s" % rel)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestSelfAudit(unittest.TestCase):
    def _audit(self, mutate=None):
        tmp, canonical = _materialize_tree(mutate)
        try:
            return ac.check_checklist(canonical)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_self_audit_passes_on_real_artifacts(self):
        verdict, violations = self._audit()
        self.assertEqual(verdict, "CHECKLIST-VERIFIED")
        self.assertEqual(violations, [])

    def test_rejects_tampered_lesson_content(self):
        def mutate(canonical, tmp):
            canonical["lessons"]["L3"]["test_problem"] += " (edited)"
            canonical["lesson_hashes"]["L3"] = ac.lesson_fingerprint(
                canonical["lessons"]["L3"])
        verdict, violations = self._audit(mutate)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any(v.startswith("CURRICULUM_STALE: lesson L3")
                            for v in violations), violations)

    def test_rejects_lesson_missing_required_field(self):
        def mutate(canonical, tmp):
            del canonical["lessons"]["L5"]["rubric"]
        verdict, violations = self._audit(mutate)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any("CURRICULUM_LESSON_INCOMPLETE: L5" in v
                            and "rubric" in v for v in violations), violations)

    def test_rejects_curriculum_not_mandatory(self):
        def mutate(canonical, tmp):
            canonical["curriculum"]["mandatory"] = False
        verdict, violations = self._audit(mutate)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any(v.startswith("CURRICULUM_NOT_MANDATORY")
                            for v in violations), violations)

    def test_rejects_weakened_pass_policy(self):
        def mutate(canonical, tmp):
            canonical["curriculum"]["pass_policy"]["per_lesson_minimum"] = 5
        verdict, violations = self._audit(mutate)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any(v.startswith("CURRICULUM_PASS_POLICY_WEAK")
                            for v in violations), violations)

    def test_rejects_human_twin_divergence(self):
        def mutate(canonical, tmp):
            # drop the L9 header line so the human twin no longer enumerates it
            lines = [l for l in canonical["human_md"].splitlines()
                     if not l.startswith("### C10 \u2014 L9:")]
            canonical["human_md"] = "\n".join(lines)
        verdict, violations = self._audit(mutate)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any(v.startswith("TWIN_DIVERGED") and "L9" in v
                            for v in violations), violations)

    def test_rejects_stale_v2_bytes(self):
        def mutate(canonical, tmp):
            p = os.path.join(tmp, *ac.V2_FILES[1].split("/"))
            with open(p, "ab") as f:
                f.write(b"\n<!-- stale edit -->\n")
            with open(p, "rb") as f:
                canonical["v2_hashes"][ac.V2_FILES[1]] = ac._sha256_hex(f.read())
        verdict, violations = self._audit(mutate)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any(v.startswith("V2_STALE") for v in violations),
                        violations)

    def test_rejects_wrong_machine_twin_id(self):
        def mutate(canonical, tmp):
            m = dict(canonical["v2_machine"])
            m["id"] = "OPERATING-CODE-V9"
            canonical["v2_machine"] = m
        verdict, violations = self._audit(mutate)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any(v.startswith("V2_MACHINE_TWIN_INVALID")
                            for v in violations), violations)

    def test_tool_error_when_v2_file_missing(self):
        tmp, _ = _materialize_tree()
        try:
            os.unlink(os.path.join(tmp, *ac.V2_FILES[0].split("/")))
            code = ac.main(["--repo-root", tmp, "--v2-root", tmp])
            self.assertEqual(code, 2)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_tool_error_when_curriculum_missing(self):
        tmp = tempfile.mkdtemp(prefix="checklist-empty-")
        try:
            self.assertEqual(ac.main(["--repo-root", tmp]), 2)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestClaimVerification(unittest.TestCase):
    def setUp(self):
        self.tmp, self.canonical = _materialize_tree()
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def _check(self, claim):
        return ac.check_checklist(self.canonical, claim)

    def test_good_claim_passes(self):
        verdict, violations = self._check(_good_claim(self.canonical))
        self.assertEqual(verdict, "CHECKLIST-VERIFIED")
        self.assertEqual(violations, [])

    def test_rejects_fake_lesson_list(self):
        """ADVERSARIAL: invented lesson ids are not canonical lessons."""
        claim = _good_claim(self.canonical)
        claim["lessons"] = claim["lessons"][:11] + [
            {"lesson_id": "L0", "sha256": "0" * 64},
            {"lesson_id": "L15", "sha256": "1" * 64},
            {"lesson_id": "L99", "sha256": "2" * 64},
        ]
        verdict, violations = self._check(claim)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any("LESSON_NOT_REGISTERED" in v and "L0" in v
                            for v in violations), violations)
        self.assertTrue(any("LESSON_NOT_REGISTERED" in v and "L99" in v
                            for v in violations), violations)
        # and the displaced real lessons are now missing
        self.assertTrue(any("LESSON_MISSING: L12" in v for v in violations),
                        violations)

    def test_rejects_partial_loading(self):
        """ADVERSARIAL: 10/14 loaded is not activated."""
        claim = _good_claim(self.canonical)
        claim["lessons"] = claim["lessons"][:10]
        verdict, violations = self._check(claim)
        self.assertEqual(verdict, "REJECT")
        missing = [v for v in violations if v.startswith("LESSON_MISSING")]
        self.assertEqual(len(missing), 4)
        self.assertTrue(any("L14" in v for v in missing), violations)

    def test_rejects_empty_lesson_list(self):
        claim = _good_claim(self.canonical)
        claim["lessons"] = []
        verdict, violations = self._check(claim)
        self.assertEqual(verdict, "REJECT")
        self.assertEqual(len([v for v in violations
                              if v.startswith("LESSON_MISSING")]), 14)

    def test_rejects_duplicate_lesson_counted_twice(self):
        """ADVERSARIAL: claiming L1 twice does not cover L14."""
        claim = _good_claim(self.canonical)
        dup = dict(claim["lessons"][0])
        claim["lessons"] = claim["lessons"][:13] + [dup]
        verdict, violations = self._check(claim)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any(v.startswith("LESSON_DUPLICATE") and "L1" in v
                            for v in violations), violations)
        self.assertTrue(any("LESSON_MISSING: L14" in v for v in violations),
                        violations)

    def test_rejects_forged_lesson_fingerprint(self):
        """ADVERSARIAL: right ids, plausible-but-wrong content hash."""
        claim = _good_claim(self.canonical)
        claim["lessons"][4] = {"lesson_id": "L5", "sha256": "ab" * 32}
        verdict, violations = self._check(claim)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any(v.startswith("LESSON_FINGERPRINT_MISMATCH")
                            and "L5" in v for v in violations), violations)

    def test_rejects_malformed_fingerprint(self):
        claim = _good_claim(self.canonical)
        claim["lessons"][0] = {"lesson_id": "L1", "sha256": "not-a-hash"}
        verdict, violations = self._check(claim)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any(v.startswith("LESSON_FINGERPRINT_MALFORMED")
                            for v in violations), violations)

    def test_rejects_stale_v2_claim(self):
        """ADVERSARIAL: V2 fingerprints from an older V2 cut."""
        claim = _good_claim(self.canonical)
        claim["v2"] = {rel: "00" * 32 for rel in ac.V2_FILES}
        verdict, violations = self._check(claim)
        self.assertEqual(verdict, "REJECT")
        self.assertEqual(len([v for v in violations
                              if v.startswith("V2_STALE")]), 3)

    def test_rejects_claim_missing_v2(self):
        claim = _good_claim(self.canonical)
        del claim["v2"]
        verdict, violations = self._check(claim)
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any(v.startswith("CLAIM_MALFORMED") and "claim.v2" in v
                            for v in violations), violations)

    def test_rejects_non_object_claim(self):
        verdict, violations = self._check(["not", "a", "dict"])
        self.assertEqual(verdict, "REJECT")
        self.assertTrue(any(v.startswith("CLAIM_MALFORMED")
                            for v in violations), violations)


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.tmp, self.canonical = _materialize_tree()
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def _write_claim(self, claim):
        p = os.path.join(self.tmp, "claim.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(claim, f)
        return p

    def test_cli_self_audit_exit_0(self):
        self.assertEqual(ac.main(["--repo-root", self.tmp]), 0)

    def test_cli_good_claim_exit_0(self):
        p = self._write_claim(_good_claim(self.canonical))
        self.assertEqual(ac.main(["--repo-root", self.tmp, "--checklist", p]), 0)

    def test_cli_partial_claim_exit_1(self):
        claim = _good_claim(self.canonical)
        claim["lessons"] = claim["lessons"][:13]
        p = self._write_claim(claim)
        self.assertEqual(ac.main(["--repo-root", self.tmp, "--checklist", p]), 1)

    def test_cli_json_output_parses(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = ac.main(["--repo-root", self.tmp, "--json"])
        self.assertEqual(code, 0)
        doc = json.loads(buf.getvalue())
        self.assertEqual(doc["verdict"], "CHECKLIST-VERIFIED")
        self.assertEqual(doc["gate"], "activation-checklist-v1")

    def test_cli_unreadable_claim_exit_2(self):
        code = ac.main(["--repo-root", self.tmp, "--checklist",
                        os.path.join(self.tmp, "nope.json")])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()

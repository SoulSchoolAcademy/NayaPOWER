"""Purely local falsifier tests; passing these does not imply repo/runtime proof."""

import copy
import unittest

from preflight_candidate import assess, REQUIRED_UNDERSTANDING


MAIN = "a" * 40
SOURCES = {"AGENTS.md": "b" * 64,
           "NAYA-ACTIVATION/PORTABLE-ACTIVATION-PROTOCOL-V1.md": "c" * 64}


def good():
    return {
        "actor_id": "cold-seat-01", "session_id": "s-01",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "source_commit": MAIN, "observed_at": "2026-10-08T03:00:00Z",
        "read_evidence": dict(SOURCES),
        "understanding": dict(REQUIRED_UNDERSTANDING),
        "proposed_action": {"scope": "read-only reconcile one issue", "self_authorized": False},
    }


class TestCandidatePreflight(unittest.TestCase):
    def run_bad(self, edit, expected):
        x = good()
        edit(x)
        result = assess(x, trusted_main=MAIN, trusted_sources=SOURCES)
        self.assertEqual(result["status"], "PREFLIGHT_NOT_READY")
        self.assertFalse(result["authority_granted"])
        self.assertIn(expected, result["errors"])

    def test_eligible_but_no_permission(self):
        result = assess(good(), trusted_main=MAIN, trusted_sources=SOURCES)
        self.assertEqual(result["status"], "PREFLIGHT_ELIGIBLE")
        self.assertFalse(result["authority_granted"])
        self.assertEqual(result["truth_ceiling"], "READ_ATTESTED_NOT_COMPREHENSION_PROVEN")

    def test_missing_receipt(self):
        result = assess(None, trusted_main=MAIN, trusted_sources=SOURCES)
        self.assertEqual(result["status"], "PREFLIGHT_NOT_READY")

    def test_stale_main(self):
        self.run_bad(lambda x: x.update(source_commit="f"*40), "stale_or_wrong_main")

    def test_wrong_repository(self):
        self.run_bad(lambda x: x.update(repository="another/repo"), "wrong_repository")

    def test_missing_source(self):
        self.run_bad(lambda x: x["read_evidence"].pop("AGENTS.md"), "missing_read:AGENTS.md")

    def test_wrong_source_hash(self):
        self.run_bad(lambda x: x["read_evidence"].update({"AGENTS.md": "d"*64}), "source_digest_mismatch:AGENTS.md")

    def test_invalid_digest(self):
        self.run_bad(lambda x: x["read_evidence"].update({"AGENTS.md": "fake"}), "invalid_digest:AGENTS.md")

    def test_wrong_understanding(self):
        self.run_bad(lambda x: x["understanding"].update({"board_role": "BOARD_IS_LAW"}), "incorrect_understanding:board_role")

    def test_missing_understanding(self):
        self.run_bad(lambda x: x.pop("understanding"), "missing:understanding")

    def test_self_grant(self):
        self.run_bad(lambda x: x["proposed_action"].update(self_authorized=True), "improper_authority_claim")

    def test_fake_independent_verification(self):
        self.run_bad(lambda x: x.update(independently_verified=True), "unsupported_independent_verification_claim")

    def test_reused_session(self):
        result = assess(good(), trusted_main=MAIN, trusted_sources=SOURCES, used_sessions={"s-01"})
        self.assertIn("reused_session", result["errors"])

    def test_missing_action(self):
        self.run_bad(lambda x: x["proposed_action"].clear(), "missing_action_scope")


if __name__ == "__main__":
    unittest.main()

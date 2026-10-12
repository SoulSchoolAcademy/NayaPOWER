"""Intelligence Board read-only projection falsifiers, using actual World Model imports."""
import copy
import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from intelligence_board import build_board, render_markdown


def section(**changes):
    return {
        "status": "OK", "as_of_ts": time.time(),
        "as_of_utc": "2026-10-12T16:00:00Z", **changes,
    }


def valid_model():
    return {"sections": {
        "tip": section(sha="a" * 40),
        "mission": section(title="Mission", body_preview=(
            "## Right now\n1. **Hold merges** until review.\n"
            "2. **Test learning** from receipts.\n## Parked\n3. Don't include me"
        )),
        "prs": section(count=3, prs=[]),
        "lanes": section(lanes={"alpha": section(state="FREE", issue=1713)}),
        "ledger": section(updated_at="2026-10-12T15:59:00Z"),
        "laws": section(headers=["A cached header"], permission_evidence=True),
    }}


class BoardTest(unittest.TestCase):
    def test_orientation_does_not_grant_authority(self):
        b = build_board(valid_model())
        self.assertEqual(b["readiness"], "ORIENTATION_CURRENT")
        self.assertFalse(b["what_next"]["authorized"])
        self.assertFalse(b["laws"]["authority_proven"])
        self.assertIsNone(b["current_reality"]["proof"]["causal_outcome_verified"])

    def test_stale_tip_fails_closed(self):
        m = valid_model()
        m["sections"]["tip"]["as_of_ts"] -= 10000
        b = build_board(m)
        self.assertEqual(b["readiness"], "READ_MORE")
        self.assertIsNone(b["current_reality"]["main_sha"])
        self.assertEqual(b["what_matters"], [])

    def test_missing_mission_fails_closed(self):
        m = valid_model()
        del m["sections"]["mission"]
        b = build_board(m)
        self.assertEqual(b["readiness"], "READ_MORE")
        self.assertEqual(b["current_reality"]["mission"]["status"], "UNKNOWN")

    def test_partial_prs_never_make_a_total(self):
        m = valid_model()
        m["sections"]["prs"] = section(status="PARTIAL", pr_count_lower_bound=100)
        b = build_board(m)
        self.assertIsNone(b["current_reality"]["open_pr_count"])
        self.assertEqual(b["current_reality"]["open_pr_count_status"], "PARTIAL")

    def test_invalid_tip_is_not_fresh_truth(self):
        m = valid_model()
        m["sections"]["tip"]["sha"] = "abcdefgh"
        self.assertIsNone(build_board(m)["current_reality"]["main_sha"])

    def test_stale_laws_never_prove_authority(self):
        m = valid_model()
        m["sections"]["laws"]["as_of_ts"] -= 90000
        b = build_board(m)
        self.assertEqual(b["laws"]["status"], "UNKNOWN")
        self.assertFalse(b["laws"]["authority_proven"])
        self.assertEqual(b["laws"]["briefing_headers"], [])

    def test_partial_lanes_cannot_claim_a_lease(self):
        m = valid_model()
        m["sections"]["lanes"]["status"] = "PARTIAL"
        self.assertEqual(build_board(m)["current_reality"]["lanes"], {})

    def test_reports_mission_without_executing_it(self):
        b = build_board(valid_model())
        self.assertEqual(len(b["what_matters"]), 2)
        self.assertIn("Hold merges", b["what_matters"][0])
        self.assertEqual(b["what_next"]["verdict"], "READ_MORE")

    def test_cannot_invent_changes_from_one_snapshot(self):
        self.assertEqual(build_board(valid_model())["what_changed"]["status"], "NOT_MEASURED")

    def test_no_input_mutation_and_human_view(self):
        m = valid_model()
        original = copy.deepcopy(m)
        output = render_markdown(build_board(m))
        self.assertEqual(m, original)
        self.assertIn("Naya Intelligence Board", output)
        self.assertIn("No authorization is inferred", output)

    def test_malformed_data_degrades_to_read_more(self):
        self.assertEqual(build_board("corrupt")["readiness"], "READ_MORE")
        self.assertEqual(build_board({"sections": []})["readiness"], "READ_MORE")

    def test_truncation_disclosed(self):
        m = valid_model()
        m["sections"]["mission"]["body_preview"] += "x" * 2200
        b = build_board(m)
        self.assertTrue(b["current_reality"]["mission"]["preview_may_be_truncated"])
        self.assertIn("PARTIAL PREVIEW", render_markdown(b))


if __name__ == "__main__":
    unittest.main()

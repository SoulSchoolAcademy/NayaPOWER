import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL = (ROOT / "supabase/migrations/20260924230000_converge_legacy_intelligence_capture_authority_v2.sql").read_text(encoding="utf-8")

class LegacyIntelligenceCaptureAuthorityTests(unittest.TestCase):
    def test_targets_exact_legacy_six_argument_overload(self):
        self.assertIn(
            "nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb)",
            SQL,
        )
        self.assertIn("p_action text default 'record_intelligence'", SQL)

    def test_intelligence_capture_fails_closed_before_legacy_metadata_authority(self):
        branch = SQL.split("if p_action = 'intelligence.capture' then", 1)[1].split("end if;", 1)[0]
        self.assertIn("CANONICAL_EXECUTION_AUTHORIZATION_REQUIRED", branch)
        self.assertNotIn("nayanet_validate_authority_grant", branch)

    def test_legacy_non_capture_path_retains_existing_authority_validation(self):
        self.assertIn("elsif v_authority_grant_id is not null then", SQL)
        self.assertIn(
            "v_authority := public.nayanet_validate_authority_grant(",
            SQL,
        )
        self.assertIn(
            "nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb) to authenticated",
            SQL,
        )

if __name__ == "__main__":
    unittest.main()

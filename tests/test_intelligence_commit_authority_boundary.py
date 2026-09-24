import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TS=(ROOT/'supabase/functions/nayanet-compound-intelligence/index.ts').read_text(encoding='utf-8')
SQL=(ROOT/'supabase/migrations/20260924100000_wire_authority_grant_into_intelligence_commit_v1.sql').read_text(encoding='utf-8')

class IntelligenceCommitAuthorityBoundaryTests(unittest.TestCase):
    def test_sql_preserves_old_call_shape_and_adds_authority_parameter(self):
        self.assertIn("p_learning jsonb default '[]'::jsonb\n) returns jsonb", SQL)
        self.assertIn('nayanet_validate_authority_grant', SQL)
        self.assertIn('authority_grant_id,authority_issuer_id,authority_scope,authority_actions,authority_constraints', SQL)
        self.assertIn('authority_source_event_id,authority_validated_at', SQL)
    def test_commit_requires_and_validates_authority_before_mutation(self):
        self.assertIn('const authorityGrantId = String(body.authority_grant_id ?? "").trim();', TS)
        self.assertIn('if (!authorityGrantId) throw new Error("AUTHORITY_GRANT_ID_REQUIRED");', TS)
        self.assertIn('await validateIntelligenceCommitAuthority(client, authorityGrantId);', TS)
    def test_receipt_boundary_carries_authority(self):
        self.assertIn('authority_grant_id:authorityGrantId', TS)
        self.assertIn('authority_grant_id: body.authority_grant_id ?? null', TS)
        self.assertIn('authority_validated_at', SQL)
    def test_learning_and_block_mutations_revalidate(self):
        self.assertGreaterEqual(TS.count('await validateIntelligenceCommitAuthority(client, authorityGrantId);'), 4)

if __name__ == '__main__':
    unittest.main()

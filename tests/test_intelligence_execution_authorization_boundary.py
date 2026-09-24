import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TS=(ROOT/'supabase/functions/nayanet-compound-intelligence/index.ts').read_text(encoding='utf-8')
SQL=(ROOT/'supabase/migrations/20260924110000_reconcile_execution_authorization_cognition_overload_v1.sql').read_text(encoding='utf-8')
class ExecutionAuthorizationBoundaryTests(unittest.TestCase):
    def test_edge_passes_existing_execution_authorization_contract(self):
        self.assertIn('p_execution_authorization: executionAuthorization', TS)
        self.assertIn('authority_id:authorityGrantId', TS)
        self.assertIn('actor_id:userId', TS)
        self.assertIn('permission:"intelligence_commit"', TS)
        self.assertIn('governance_state:"AUTHORIZED"', TS)
    def test_sql_enforces_actor_permission_and_governance(self):
        for token in ['EXECUTION_AUTHORIZATION_REQUIRED','EXECUTION_AUTHORIZATION_ACTOR_MISMATCH','EXECUTION_AUTHORIZATION_PERMISSION_MISMATCH','EXECUTION_AUTHORIZATION_NOT_AUTHORIZED']:
            self.assertIn(token, SQL)
        self.assertIn('authority_grant_id,authority_issuer_id,authority_scope,authority_actions,authority_constraints', SQL)
        self.assertIn('authority_source_event_id,authority_validated_at', SQL)
    def test_exact_existing_function_signature_is_reconciled(self):
        self.assertIn('p_execution_authorization jsonb default null', SQL)
        self.assertIn('nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb,jsonb)', SQL)
if __name__=='__main__': unittest.main()

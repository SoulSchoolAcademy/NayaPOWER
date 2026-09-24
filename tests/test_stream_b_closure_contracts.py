#!/usr/bin/env python3
"""Stream B closure contract regressions.

These are repository-contract tests. They do not contact Supabase, Cloudflare,
the Hub, or any production service.
"""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT/path).read_text(encoding="utf-8")

class TestStreamBClosureContracts(unittest.TestCase):
    def test_001_portable_intelligence_commit_is_gate_bound(self):
        c=read(".naya/runtime/portable_authorization.py")
        self.assertIn("gate: Any", c)
        self.assertIn("gate.verify(execution_authorization", c)
        self.assertIn("INTELLIGENCE_COMMIT_ACTION_TYPES", c)
        self.assertIn('INTELLIGENCE_COMMIT_TARGET = "NayaNET"', c)

    def test_002_no_false_success_statuses_are_explicit(self):
        c=read("supabase/migrations/20260919021000_smart_ledger_foundation_v1.sql")
        self.assertIn("'BLOCKED'", c)
        self.assertIn("'FAILED'", c)
        self.assertIn("'VERIFIED'", c)
        self.assertIn("when new.status='SUCCESS' then 'VERIFIED'", c)
        self.assertIn("when new.status='BLOCKED' then 'BLOCKED'", c)
        self.assertIn("when new.status='FAILED' then 'FAILED'", c)

    def test_003_receipt_carries_authority_lineage(self):
        c=read("supabase/migrations/20260919021000_smart_ledger_foundation_v1.sql")
        for field in ("authority_grant_id","authority_issuer_id","authority_scope","authority_actions","authority_constraints","authority_status_at_execution","authority_source_event_id","authority_validated_at"):
            self.assertIn(field,c)
        self.assertIn("'EXECUTION_RECEIPT'",c)

    def test_004_cognition_receipt_lineage_is_bidirectional(self):
        c=read("supabase/migrations/20260920030000_repair_cognition_event_receipt_lineage.sql")
        self.assertIn("insert into public.nayanet_execution_receipts",c)
        self.assertIn("set receipt_id=v_receipt.id::text",c)

    def test_005_value_is_recorded_but_not_authority(self):
        c=read("supabase/migrations/20260918230000_p0_responsible_value_contract.sql")
        self.assertIn("benefit",c)
        self.assertIn("harm",c)
        self.assertIn("cost",c)
        self.assertIn("risk_adjusted_loss",c)
        gate=read(".naya/runtime/universal_execution_gate.py")
        self.assertIn("kernel_result = evaluate",gate)
        self.assertIn("AUTHORIZATION",gate.upper())

    def test_006_smart_ledger_is_source_linked_and_private_by_default(self):
        c=read("supabase/migrations/20260919021000_smart_ledger_foundation_v1.sql")
        self.assertIn("source_table text not null",c)
        self.assertIn("source_id text not null",c)
        self.assertIn("privacy_classification text not null default 'PRIVATE'",c)
        self.assertIn("owner_id=auth.uid()",c)

    def test_007_adversarial_gate_suite_exists(self):
        c=read("tests/test_universal_execution_gate.py")
        for marker in ("revoked","expired","wrong_actor","wrong_scope","direct_controller_bypass"):
            self.assertIn(marker,c)
        self.assertIn("not issued by this gate",read(".naya/runtime/universal_execution_gate.py"))

    def test_008_smart_connect_seven_doors_and_authority_separation(self):
        candidates=[
            "NAYANET/HUB-ROOM-SYSTEM/04-SMART-CONNECT.md",
            ".naya/protocol/NAYANET-INTELLIGENCE-PARTICIPATION-PRIVACY-PROTOCOL-V1.md",
            "supabase/migrations/20260924180000_smart_connect_participation_collective_wisdom_v1.sql",
        ]
        c="\n".join(read(p) for p in candidates)
        for door in ("GitHub App","MCP","REST/OpenAPI","Webhooks","SDK","A2A","MCP Apps"):
            self.assertIn(door,c)
        self.assertIn("authority",c.lower())

    def test_009_hub_taxonomy_preserves_dream_and_naya_play_boundaries(self):
        master=read("NAYANET ALIGNMENT UPDATE - THIS IS THE MASTER OBJECTIVE.md")
        gap=read(".naya/NAYANET-HUB-CURRENT-TRUTH-AND-GAP-REGISTER-V1.md")
        combined=master+"\n"+gap
        self.assertIn("Dream is a Superbrain process",combined)
        self.assertIn("Dream is not a sidebar destination",combined)
        self.assertIn("Naya Play is an Intelligent Block capability",combined)
        self.assertIn("Naya Play is not a sidebar destination",combined)
        self.assertIn("Smart Connect",combined)

    def test_010_three_layer_source_of_truth_stack_is_present(self):
        readme=read("README.md")
        self.assertIn("Master Objective",readme)
        self.assertIn("58 Topology",readme)
        self.assertIn("Gap Register",readme)

if __name__=="__main__":
    result=unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestStreamBClosureContracts)
    )
    print("STREAM_B_CLOSURE_CONTRACTS="+("PASS" if result.wasSuccessful() else "FAIL"))
    raise SystemExit(0 if result.wasSuccessful() else 1)

"""Stream B boundary contract: automatic intelligence vs governed execution.

Automatic intelligence is not an execution action:
- connection/participation consent controls whether wisdom contributes;
- capture, learning, distillation, compounding and indexing flow automatically;
- identity remains private by default;
- publication and consequential execution retain their own explicit boundaries.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "supabase" / "migrations" / "20260924130000_canonical_intelligence_commit_bridge_v1.sql"

def _sql() -> str:
    return M.read_text(encoding="utf-8")

def test_intelligence_capture_is_not_authority_gated():
    sql = _sql()
    assert "automatic-intelligence-flow-v1" in sql
    assert "authority_required',false" in sql
    assert "INTELLIGENCE_CAPTURE_REQUIRES_CANONICAL_VERIFIER" not in sql
    assert "PORTABLE_AUTHORIZATION_REQUIRED" not in sql

def test_capture_receipt_has_no_execution_authority_lineage():
    sql = _sql()
    assert "case when p_action='intelligence.capture' then null" in sql
    assert "execution_authorization',case when p_action='intelligence.capture' then null" in sql

def test_non_intelligence_execution_still_uses_authority_when_supplied():
    sql = _sql()
    assert "nayanet_validate_authority_grant" in sql
    assert "AUTHORITY_REQUIRED" in sql
    assert "p_action <> 'intelligence.capture'" in sql

def test_connection_participation_is_explicitly_distinct_from_authority():
    sql = _sql().lower()
    assert "automatic intelligence" in sql
    assert "connection/participation consent" in sql
    assert "consequential execution/publication boundaries" in sql

def test_canonical_capture_seam_is_service_role_only_and_not_authority_based():
    sql = _sql()
    seam = sql.split("create or replace function public.nayanet_canonical_intelligence_capture",1)[1].split("create or replace function public.nayanet_record_cognition_event",1)[0]
    assert "CANONICAL_INTELLIGENCE_CAPTURE_SERVICE_ROLE_REQUIRED" in seam
    assert "grant execute" in seam and "to service_role" in seam
    assert "nayanet_validate_authority_grant" not in seam

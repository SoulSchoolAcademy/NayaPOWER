from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "supabase/functions/nayanet-compound-intelligence/index.ts"

def test_compound_error_response_preserves_machine_readable_boundary():
    source = SOURCE.read_text(encoding="utf-8")
    for marker in ("error_code", "COMPOUND_INTELLIGENCE_ERROR", "truth_status", "errorCode.startsWith('AUTHORITY')"):
        assert marker in source

def test_compound_error_response_remains_non_success():
    source = SOURCE.read_text(encoding="utf-8")
    assert "return json({ok:false,action,error:detail,error_code:errorCode" in source
    assert "return json({ok:true,action,result})" in source

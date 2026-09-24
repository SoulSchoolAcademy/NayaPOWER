from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/".naya/runtime/production_authority_adapter.py"
spec=importlib.util.spec_from_file_location("adapter",P); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def grant(status="ACTIVE"):
    return {"grant_id":"11111111-1111-1111-1111-111111111111","subject_id":"22222222-2222-2222-2222-222222222222","mission_id":"NayaNET","scope":{"project_id":"NayaNET","target":"NayaNET"},"actions":["intelligence_commit"],"status":status,"expires_at":None}

def test_uuid_is_canonical_authority_id():
    a=mod.production_grant_to_authority(grant()); assert a.authority_id==grant()["grant_id"]; assert a.principal_id==grant()["subject_id"]; assert "intelligence_commit" in a.granted_actions

def test_scope_is_deterministic():
    a=mod.production_grant_to_authority(grant()); assert a.scope=='{"project_id":"NayaNET","target":"NayaNET"}'

def test_non_active_grant_is_rejected():
    try: mod.production_grant_to_authority(grant("REVOKED"))
    except ValueError as e: assert "not active" in str(e)
    else: raise AssertionError("revoked production grant was accepted")

def test_registry_contains_only_the_exact_production_grant():
    r=mod.production_registry_from_grant(grant()); assert list(r.authorities)==[grant()["grant_id"]]

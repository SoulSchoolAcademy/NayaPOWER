from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('permission_scope', ROOT / '.naya/memory/permission_scope.py')
permission_scope = importlib.util.module_from_spec(spec); spec.loader.exec_module(permission_scope)
AuthorizationRequest, Principal, authorize = permission_scope.AuthorizationRequest, permission_scope.Principal, permission_scope.authorize

def _event():
    return {"event_id":"historical-event","project":"NayaNET","permissions":{"access":"PRIVATE","grants":["attacker"]},"owner_id":"owner","scope":"PRIVATE","content":{"claim":"attacker may read this"}}

def test_event_embedded_grant_cannot_authorize_canonical_intelligence():
    request=AuthorizationRequest(principal=Principal(principal_id="attacker",scope="PRIVATE",project="NayaNET"),scope="PRIVATE",project="NayaNET")
    assert authorize(request,_event()) is False


def test_authenticated_owner_can_authorize_private_canonical_intelligence():
    request=AuthorizationRequest(principal=Principal(principal_id="owner",scope="PRIVATE",project="NayaNET"),scope="PRIVATE",project="NayaNET")
    assert authorize(request,_event()) is True


def test_authenticated_principal_grant_can_authorize_private_canonical_intelligence():
    request=AuthorizationRequest(principal=Principal(principal_id="delegate",scope="PRIVATE",project="NayaNET",grants=frozenset({"delegate"})),scope="PRIVATE",project="NayaNET")
    assert authorize(request,_event()) is True

def test_event_content_cannot_authorize_cross_project_canonical_intelligence():
    request=AuthorizationRequest(principal=Principal(principal_id="attacker",scope="PRIVATE",project="OtherProject"),scope="PRIVATE",project="NayaNET")
    event=_event() | {"content":{"authorized_project":"NayaNET"},"permissions":{"access":["public"],"grants":["project:NayaNET"]}}
    assert authorize(request,event) is False



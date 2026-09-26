from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONT_DOOR = ROOT / "NAYANET" / "HUB" / "public" / "identity.html"
ADAPTER = ROOT / "NAYANET" / "HUB" / "public" / "NAYANET" / "name-first-auth-adapter.js"
RUNTIME = ROOT / "NAYANET" / "HUB" / "public" / "assistant-runtime.js"
COMPLETENESS = ROOT / "NAYANET" / "HUB" / "public" / "hub-completeness.js"
RELEASE_WORKFLOW = ROOT / ".github" / "workflows" / "assistant-cloudflare-hub-release.yml"


def front_door() -> str:
    assert FRONT_DOOR.is_file(), f"missing canonical Hub front door: {FRONT_DOOR}"
    return FRONT_DOOR.read_text(encoding="utf-8")


def test_front_door_exists_at_canonical_source_path():
    assert FRONT_DOOR.is_file()


def test_front_door_loads_the_one_existing_identity_adapter():
    source = front_door()
    assert '/NAYANET/name-first-auth-adapter.js' in source
    assert "data-nayanet-name-first" in source
    assert "NayaNETNameFirstAuth" in source


def test_front_door_calls_establish_with_name_and_alias():
    source = front_door()
    assert re.search(r"auth\.establish\(\{\s*name:\s*name\s*,\s*alias:", source)
    assert ".establish(" in source


def test_front_door_does_not_create_a_second_identity_or_credential_store():
    source = front_door()
    for forbidden in (
        "supabase.co",
        "sb_publishable_",
        "signInWithPassword",
        "signUp(",
        "service_role",
    ):
        assert forbidden not in source, f"front door must not duplicate identity authority: {forbidden}"
    assert "localStorage.setItem" not in source
    assert "sessionStorage.setItem" not in source


def test_front_door_fails_closed_and_never_claims_success_on_error():
    source = front_door()
    assert "BLOCKED / FAILED" in source
    assert "identity.authenticated !== true" in source
    assert "ANONYMOUS" not in source or "BLOCKED" in source


def test_front_door_returns_to_the_requested_canonical_surface():
    source = front_door()
    assert "next" in source
    assert "returnTarget" in source
    assert "window.location.assign" in source


def test_existing_unauthenticated_redirects_resolve_to_the_real_front_door():
    assert "location.assign('/identity.html')" in RUNTIME.read_text(encoding="utf-8")
    assert "location.assign('/identity.html')" in COMPLETENESS.read_text(encoding="utf-8")


def test_release_artifact_ships_the_front_door_and_asserts_it():
    source = RELEASE_WORKFLOW.read_text(encoding="utf-8")
    assert "cp NAYANET/HUB/public/identity.html dist/identity.html" in source
    assert "test -s dist/identity.html" in source


def test_release_verification_proves_front_door_is_not_spa_fallback():
    source = RELEASE_WORKFLOW.read_text(encoding="utf-8")
    assert "LIVE_IDENTITY_FRONT_DOOR_VERIFIED" in source
    assert "IDENTITY_FRONT_DOOR_SERVED_HUB_SPA_FALLBACK" in source
    assert "${NAYA_RUNTIME_URL}/identity.html" in source


def test_front_door_does_not_modify_the_preserved_canonical_hub_entrypoint():
    preservation = (ROOT / ".naya" / "control-plane" / "HUB-PRESERVATION.json").read_text(encoding="utf-8")
    assert '"status": "ACTIVE"' in preservation
    assert "NAYANET/HUB/index.html" in preservation

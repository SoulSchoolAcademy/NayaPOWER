import base64
import json
import os
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from kernel.nayapower_kernel import Kernel
from kernel.naya_identity_binding import resolve_runtime_authorization
from kernel.supabase_intelligent_blocks import SupabaseIntelligentBlockReader

BLOCK_ID = "IB-NAYA-NODE-0001-0001"
EXPECTED_OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f"


def _protected_config():
    values = {
        "url": os.environ.get("SUPABASE_URL"),
        "access_token": os.environ.get("SUPABASE_USER_ACCESS_TOKEN"),
        "refresh_token": os.environ.get("SUPABASE_USER_REFRESH_TOKEN"),
        "api_key": os.environ.get("SUPABASE_PUBLISHABLE_KEY"),
    }
    if not all(values[name] for name in ("url", "access_token", "api_key")):
        pytest.skip("protected Supabase live-proof credentials are not present")
    return values


def _jwt_claims(token: str) -> dict:
    """Decode non-secret JWT claims for diagnosis; never prints the token."""
    parts = token.split(".")
    if len(parts) != 3:
        return {}
    try:
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        return json.loads(base64.urlsafe_b64decode(payload.encode()).decode())
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return {}


def _credential_diagnostics(access_token: str, refresh_token: str | None) -> str:
    claims = _jwt_claims(access_token)
    sub = claims.get("sub")
    exp = claims.get("exp")
    access_state = "non-JWT/opaque"
    if claims:
        if isinstance(exp, (int, float)) and exp <= time.time():
            access_state = "JWT expired"
        else:
            access_state = "JWT not locally expired"
    refresh_shape = "missing"
    if refresh_token:
        refresh_shape = "JWT-shaped (likely wrong credential type)" if _jwt_claims(refresh_token) else "opaque"
    return (
        f"access_sub={sub!r}; access_state={access_state}; "
        f"refresh_shape={refresh_shape}"
    )


def _authenticated_session(
    url: str, access_token: str, api_key: str, refresh_token: str | None = None
) -> dict[str, str]:
    # The JWT is a transport credential only. Resolve the live Auth user
    # through the canonical Supabase Auth boundary before applying ownership.
    claims = _jwt_claims(access_token)
    request = Request(
        f"{url.rstrip('/')}/auth/v1/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "apikey": api_key,
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urlopen(request, timeout=10) as response:
            payload = json.loads(response.read())
    except HTTPError as error:
        if error.code not in (401, 403) or not refresh_token:
            raise
        if _jwt_claims(refresh_token):
            raise AssertionError(
                "Supabase access token was rejected and "
                "SUPABASE_USER_REFRESH_TOKEN is JWT-shaped. "
                "The refresh-token secret appears to contain an access JWT, "
                "not a Supabase refresh token."
            ) from error

        refresh_request = Request(
            f"{url.rstrip('/')}/auth/v1/token?grant_type=refresh_token",
            data=json.dumps({"refresh_token": refresh_token}).encode(),
            headers={
                "apikey": api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(refresh_request, timeout=10) as response:
                payload = json.loads(response.read())
        except HTTPError as refresh_error:
            raw = refresh_error.read().decode("utf-8", errors="replace")
            try:
                error_payload = json.loads(raw)
            except json.JSONDecodeError:
                error_payload = {}
            safe_code = error_payload.get("error_code") or error_payload.get("error")
            safe_message = error_payload.get("msg") or error_payload.get("message") or refresh_error.reason
            raise AssertionError(
                f"Supabase refresh failed: HTTP {refresh_error.code}; "
                f"code={safe_code!r}; message={safe_message!r}; "
                f"{_credential_diagnostics(access_token, refresh_token)}. "
                "A valid refresh token is single-use/rotated by Supabase; "
                "a previously exchanged token becomes invalid."
            ) from refresh_error
        access_token = payload.get("access_token") or ""

    owner_id = payload.get("id") or payload.get("user", {}).get("id")
    if not owner_id:
        raise AssertionError("authenticated Supabase user response has no id")
    authorization = resolve_runtime_authorization(
        naya_id="NAYA-NODE-0001",
        owner_id=EXPECTED_OWNER_ID,
        runtime_subject_id=owner_id,
        binding_owner_id=owner_id if owner_id == EXPECTED_OWNER_ID else None,
        session_id=claims.get("session_id", "live-supabase-session"),
    )
    if not authorization.authorized:
        raise AssertionError(
            "canonical owner binding was not established: "
            f"{authorization.reason}; runtime_subject={owner_id!r}"
        )
    if owner_id != EXPECTED_OWNER_ID:
        raise AssertionError(
            "authenticated Supabase user is not the canonical NAYA owner: "
            f"got {owner_id!r}, expected {EXPECTED_OWNER_ID!r}"
        )
    if not access_token:
        raise AssertionError("Supabase authentication response has no access token")
    return {"owner_id": owner_id, "access_token": access_token}


def test_live_kernel_retrieves_canonical_private_verified_block():
    config = _protected_config()
    session = _authenticated_session(
        config["url"],
        config["access_token"],
        config["api_key"],
        refresh_token=config["refresh_token"],
    )

    kernel = Kernel()
    reader = SupabaseIntelligentBlockReader(
        url=config["url"],
        access_token=session["access_token"],
        api_key=config["api_key"],
    )

    block = kernel.retrieve_intelligent_block(
        reader,
        intelligent_block_id=BLOCK_ID,
        owner_id=session["owner_id"],
    )

    assert block is not None
    assert block.intelligent_block_id == BLOCK_ID
    assert block.owner_id == session["owner_id"]
    assert block.owner_scope == "PRIVATE"
    assert block.provenance
    assert block.epistemic_state == "VERIFIED"
    assert block.data["status"] == "DURABLE"
    assert block.data["superseded_by_block_id"] is None

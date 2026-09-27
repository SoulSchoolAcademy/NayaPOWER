import json
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from kernel.nayapower_kernel import Kernel
from kernel.supabase_intelligent_blocks import SupabaseIntelligentBlockReader

BLOCK_ID = "IB-NAYA-NODE-0001-0001"


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


def _authenticated_session(
    url: str, access_token: str, api_key: str, refresh_token: str | None = None
) -> dict[str, str]:
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
        if error.code != 401 or not refresh_token:
            raise
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
        with urlopen(refresh_request, timeout=10) as response:
            payload = json.loads(response.read())
        access_token = payload.get("access_token") or ""

    owner_id = payload.get("id") or payload.get("user", {}).get("id")
    if not owner_id:
        raise AssertionError("authenticated Supabase user response has no id")
    if not access_token:
        raise AssertionError("Supabase authentication response has no access token")
    return {"owner_id": owner_id, "access_token": access_token}


def _authenticated_owner_id(url: str, access_token: str, api_key: str) -> str:
    return _authenticated_session(url, access_token, api_key)["owner_id"]


def test_live_kernel_retrieves_canonical_private_verified_block():
    config = _protected_config()
    session = _authenticated_session(
        config["url"],
        config["access_token"],
        config["api_key"],
        refresh_token=config["refresh_token"],
    )
    owner_id = session["owner_id"]

    kernel = Kernel()
    reader = SupabaseIntelligentBlockReader(
        url=config["url"],
        access_token=session["access_token"],
        api_key=config["api_key"],
    )

    block = kernel.retrieve_intelligent_block(
        reader,
        intelligent_block_id=BLOCK_ID,
        owner_id=owner_id,
    )

    assert block is not None
    assert block.intelligent_block_id == BLOCK_ID
    assert block.owner_id == owner_id
    assert block.owner_scope == "PRIVATE"
    assert block.provenance
    assert block.epistemic_state == "VERIFIED"
    assert block.data["status"] == "DURABLE"
    assert block.data["superseded_by_block_id"] is None

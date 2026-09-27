import json
import os
from urllib.request import Request, urlopen

import pytest

from kernel.nayapower_kernel import Kernel
from kernel.supabase_intelligent_blocks import SupabaseIntelligentBlockReader


BLOCK_ID = "IB-NAYA-NODE-0001-0001"


def _required_live_env():
    names = (
        "SUPABASE_URL",
        "SUPABASE_USER_ACCESS_TOKEN",
        "SUPABASE_API_KEY",
    )
    missing = [name for name in names if not os.environ.get(name)]
    if missing:
        pytest.skip("live Supabase proof requires protected environment: " + ", ".join(missing))
    return {name: os.environ[name] for name in names}


def _auth_user_id(base_url: str, user_token: str, api_key: str) -> str:
    request = Request(
        f"{base_url.rstrip('/')}/auth/v1/user",
        headers={
            "Authorization": f"Bearer {user_token}",
            "apikey": api_key,
            "Accept": "application/json",
        },
        method="GET",
    )
    with urlopen(request, timeout=15) as response:
        payload = json.loads(response.read())
    user_id = payload.get("id")
    if not user_id:
        raise AssertionError("authenticated Supabase user response did not contain an id")
    return str(user_id)


def test_live_authenticated_kernel_retrieves_canonical_block_read_only():
    env = _required_live_env()
    base_url = env["SUPABASE_URL"].rstrip("/")
    user_token = env["SUPABASE_USER_ACCESS_TOKEN"]
    api_key = env["SUPABASE_API_KEY"]

    owner_id = _auth_user_id(base_url, user_token, api_key)
    kernel = Kernel()
    reader = SupabaseIntelligentBlockReader(
        url=base_url,
        access_token=user_token,
        api_key=api_key,
    )

    retrieved = kernel.retrieve_intelligent_block(
        reader,
        intelligent_block_id=BLOCK_ID,
        owner_id=owner_id,
    )

    assert retrieved is not None
    assert retrieved.intelligent_block_id == BLOCK_ID
    assert retrieved.owner_id == owner_id
    assert retrieved.owner_scope
    assert retrieved.provenance
    assert retrieved.epistemic_state == "VERIFIED"
    assert retrieved.data["status"] not in {"DELETED", "SUPERSEDED"}

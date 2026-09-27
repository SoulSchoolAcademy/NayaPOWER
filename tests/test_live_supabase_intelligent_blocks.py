import json
import os
from urllib.request import Request, urlopen

import pytest

from kernel.nayapower_kernel import Kernel
from kernel.supabase_intelligent_blocks import SupabaseIntelligentBlockReader

BLOCK_ID = "IB-NAYA-NODE-0001-0001"


def _protected_config():
    values = {
        "url": os.environ.get("SUPABASE_URL"),
        "access_token": os.environ.get("SUPABASE_USER_ACCESS_TOKEN"),
        "api_key": os.environ.get("SUPABASE_PUBLISHABLE_KEY"),
    }
    if not all(values.values()):
        pytest.skip("protected Supabase live-proof credentials are not present")
    return values


def _authenticated_owner_id(url: str, access_token: str, api_key: str) -> str:
    request = Request(
        f"{url.rstrip('/')}/auth/v1/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "apikey": api_key,
            "Accept": "application/json",
        },
        method="GET",
    )
    with urlopen(request, timeout=10) as response:
        payload = json.loads(response.read())
    owner_id = payload.get("id")
    if not owner_id:
        raise AssertionError("authenticated Supabase user response has no id")
    return owner_id


def test_live_kernel_retrieves_canonical_private_verified_block():
    config = _protected_config()
    owner_id = _authenticated_owner_id(
        config["url"], config["access_token"], config["api_key"]
    )

    kernel = Kernel()
    reader = SupabaseIntelligentBlockReader(
        url=config["url"],
        access_token=config["access_token"],
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

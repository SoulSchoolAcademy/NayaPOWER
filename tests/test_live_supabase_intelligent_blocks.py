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


def test_live_authenticated_kernel_retrieves_connect_context_and_changes_behavior_without_authority():
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

    retrieved, relationships = kernel.retrieve_intelligent_context(
        reader,
        intelligent_block_id=BLOCK_ID,
        owner_id=owner_id,
    )

    assert retrieved is not None
    assert retrieved.intelligent_block_id == BLOCK_ID
    assert retrieved.owner_id == owner_id
    assert retrieved.owner_scope == "PRIVATE"
    assert retrieved.epistemic_state == "VERIFIED"
    assert retrieved.data["status"] not in {"DELETED", "SUPERSEDED"}
    assert retrieved.provenance
    assert relationships
    assert any(
        relationship.is_verified_support_for(BLOCK_ID)
        for relationship in relationships
    )

    control = kernel.decide(
        __import__("kernel.nayapower_kernel", fromlist=["DecisionContext"]).DecisionContext(
            action="continue_work",
            consequential=False,
            authority=None,
            task_target="NAYA-NODE-0001",
        )
    )
    treatment = kernel.decide(
        __import__("kernel.nayapower_kernel", fromlist=["DecisionContext"]).DecisionContext(
            action="continue_work",
            consequential=False,
            authority=None,
            task_target="NAYA-NODE-0001",
            intelligence=(retrieved,),
            relationships=tuple(relationships),
        )
    )
    blocked = kernel.decide(
        __import__("kernel.nayapower_kernel", fromlist=["DecisionContext"]).DecisionContext(
            action="publish_change",
            consequential=True,
            authority=None,
            task_target="NAYA-NODE-0001",
            intelligence=(retrieved,),
            relationships=tuple(relationships),
        )
    )

    assert control.outcome == "executed"
    assert treatment.outcome == "executed_with_relationship_aware_intelligence"
    assert treatment.next_state["retained_intelligence_applied"] == "true"
    assert BLOCK_ID in treatment.next_state["retained_intelligence_ids"]
    assert blocked.allowed is False
    assert blocked.executed is False
    assert blocked.blocked_by.value == "LAW"

    receipt = {
        "schema": "NAYANET_LIVE_CONNECT_RUNTIME_RECEIPT_V1",
        "block": {
            "intelligent_block_id": retrieved.intelligent_block_id,
            "version": retrieved.data["version"],
            "status": retrieved.data["status"],
            "understanding_state": retrieved.epistemic_state,
            "owner_match": retrieved.owner_id == owner_id,
            "owner_scope": retrieved.owner_scope,
            "provenance_present": bool(retrieved.provenance),
        },
        "connect": {
            "relationship_count": len(relationships),
            "verified_support_count": sum(
                relationship.is_verified_support_for(BLOCK_ID)
                for relationship in relationships
            ),
            "relationships": [
                {
                    "relationship_type": relationship.relationship_type,
                    "epistemic_state": relationship.epistemic_state,
                    "verified_support": relationship.is_verified_support_for(BLOCK_ID),
                }
                for relationship in relationships
            ],
        },
        "behavior": {
            "control": control.outcome,
            "treatment": treatment.outcome,
            "retained_intelligence_applied": (
                treatment.next_state.get("retained_intelligence_applied")
            ),
            "authority_boundary": {
                "blocked_without_authority": blocked.executed is False,
                "blocked_by": blocked.blocked_by.value,
            },
        },
        "production_mutation_performed": False,
        "rls_changed": False,
        "credentials_committed": False,
    }
    receipt_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        ".naya",
        "evidence",
        "live-connect-runtime-receipt.json",
    )
    os.makedirs(os.path.dirname(receipt_path), exist_ok=True)
    with open(receipt_path, "w", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=2, sort_keys=True)

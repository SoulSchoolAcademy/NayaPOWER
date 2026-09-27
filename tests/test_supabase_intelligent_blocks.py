import json
from urllib.parse import parse_qs, urlparse

from kernel.nayapower_kernel import Kernel
from kernel.supabase_intelligent_blocks import SupabaseIntelligentBlockReader


def test_cold_kernel_retrieval_round_trip_preserves_canonical_boundary():
    row = {
        "block_id": "9f1f9d3c-0f0a-4a58-8f4f-000000000001",
        "intelligent_block_id": "IB-NAYA-NODE-0001-0001",
        "owner_id": "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f",
        "subject_id": "NAYA-NODE-0001",
        "title": "NAYA-NODE-0001 retained intelligence",
        "block_type": "GOVERNED_INTELLIGENCE",
        "version": 1,
        "status": "DURABLE",
        "understanding_state": "VERIFIED",
        "owner_scope": "PRIVATE",
        "source_event_ids": ["950ea5c5-24f3-4777-aa8f-29a28efe4ba0"],
        "evidence_refs": [{"receipt": "AAA-LIVE-BRAIN-RECEIPT-001"}],
        "provenance": {"stage": "DISTILL+PERSIST", "source": "AAA-LIVE-BRAIN"},
        "applicable_scope": {"target": "NAYA-NODE-0001"},
        "content": {"lesson": "Preserve provenance before applying retained intelligence."},
        "supersedes_block_id": None,
        "superseded_by_block_id": None,
        "created_at": "2026-09-27T00:00:00Z",
        "updated_at": "2026-09-27T00:00:00Z",
        "schema_version": "INTELLIGENT_BLOCK_V1",
    }

    def fake_request(request):
        query = parse_qs(urlparse(request.full_url).query)
        assert query["owner_id"] == [f"eq.{row['owner_id']}"]
        assert query["intelligent_block_id"] == [f"eq.{row['intelligent_block_id']}"]
        return json.dumps([row]).encode()

    kernel = Kernel()
    reader = SupabaseIntelligentBlockReader(
        url="https://example.supabase.co",
        access_token="test-token",
        request=fake_request,
    )

    retrieved = kernel.retrieve_intelligent_block(
        reader,
        intelligent_block_id="IB-NAYA-NODE-0001-0001",
        owner_id="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f",
    )

    assert kernel.manifest["kernel_id"] == "NAYAPOWER-MASTER-KERNEL-V1"
    assert retrieved.intelligent_block_id == row["intelligent_block_id"]
    assert retrieved.owner_id == row["owner_id"]
    assert retrieved.owner_scope == row["owner_scope"]
    assert retrieved.provenance == row["provenance"]
    assert retrieved.epistemic_state == row["understanding_state"]
    assert retrieved.data["content"] == row["content"]


def test_retrieval_rejects_incomplete_canonical_row():
    def fake_request(request):
        return json.dumps([{"block_id": "x"}]).encode()

    reader = SupabaseIntelligentBlockReader(
        url="https://example.supabase.co",
        access_token="test-token",
        request=fake_request,
    )

    try:
        reader.get_by_intelligent_block_id(
            intelligent_block_id="IB-NAYA-NODE-0001-0001",
            owner_id="owner",
        )
    except ValueError as exc:
        assert "missing fields" in str(exc)
    else:
        raise AssertionError("incomplete canonical row must fail closed")

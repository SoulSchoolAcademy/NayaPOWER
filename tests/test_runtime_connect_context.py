import json
from urllib.parse import parse_qs, urlparse

from kernel.nayapower_kernel import DecisionContext, Kernel
from kernel.supabase_intelligent_blocks import SupabaseIntelligentBlockReader


def _row():
    return {
        "block_id": "9f1f9d3c-0f0a-4a58-8f4f-000000000001",
        "intelligent_block_id": "IB-NAYA-NODE-0001-0001",
        "owner_id": "owner-1",
        "subject_id": "NAYA-NODE-0001",
        "title": "NAYA-NODE-0001 retained intelligence",
        "block_type": "GOVERNED_INTELLIGENCE",
        "version": 1,
        "status": "DURABLE",
        "understanding_state": "VERIFIED",
        "owner_scope": "PRIVATE",
        "source_event_ids": ["event-1"],
        "evidence_refs": [{"receipt": "receipt-1"}],
        "provenance": {"stage": "DISTILL+PERSIST"},
        "applicable_scope": {"target": "NAYA-NODE-0001"},
        "content": {"lesson": "Preserve provenance before applying retained intelligence."},
        "supersedes_block_id": None,
        "superseded_by_block_id": None,
        "created_at": "2026-09-27T00:00:00Z",
        "updated_at": "2026-09-27T00:00:00Z",
        "schema_version": "INTELLIGENT_BLOCK_V1",
    }


def _relationships():
    return [
        {
            "relationship_id": "rel-proof",
            "source_id": "NAYA-KERNEL-PROVE",
            "target_id": "IB-NAYA-NODE-0001-0001",
            "relationship_type": "VERIFIED_BY",
            "provenance": {"source": "proof"},
            "epistemic_state": "VERIFIED",
        },
        {
            "relationship_id": "rel-know",
            "source_id": "NAYA-KERNEL-KNOW",
            "target_id": "IB-NAYA-NODE-0001-0001",
            "relationship_type": "PRODUCES",
            "provenance": {"source": "knowledge"},
            "epistemic_state": "VERIFIED",
        },
    ]


def test_reader_retrieves_canonical_block_and_relationship_context():
    row = _row()
    relationships = _relationships()

    def fake_request(request):
        query = parse_qs(urlparse(request.full_url).query)
        if "intelligent_block_id" in query:
            assert query["owner_id"] == ["eq.owner-1"]
            assert query["intelligent_block_id"] == [f"eq.{row['intelligent_block_id']}"]
            return json.dumps([row]).encode()
        assert query["owner_id"] == ["eq.owner-1"]
        assert query["target_id"] == [f"eq.{row['intelligent_block_id']}"]
        return json.dumps(relationships).encode()

    reader = SupabaseIntelligentBlockReader(
        url="https://example.supabase.co",
        access_token="user-token",
        request=fake_request,
    )

    block, graph = reader.get_context(
        intelligent_block_id="IB-NAYA-NODE-0001-0001",
        owner_id="owner-1",
    )

    assert block is not None
    assert block.intelligent_block_id == row["intelligent_block_id"]
    assert len(graph) == 2
    assert graph[0].relationship_type == "VERIFIED_BY"
    assert graph[0].epistemic_state == "VERIFIED"


def test_connect_changes_behavior_only_with_verified_relationship_support():
    row = _row()
    relationships = _relationships()

    def fake_request(request):
        query = parse_qs(urlparse(request.full_url).query)
        if "intelligent_block_id" in query:
            return json.dumps([row]).encode()
        return json.dumps(relationships).encode()

    reader = SupabaseIntelligentBlockReader(
        url="https://example.supabase.co",
        access_token="user-token",
        request=fake_request,
    )
    block, graph = reader.get_context(
        intelligent_block_id="IB-NAYA-NODE-0001-0001",
        owner_id="owner-1",
    )

    kernel = Kernel()
    control = kernel.decide(
        DecisionContext(
            action="continue_work",
            consequential=False,
            authority=None,
        )
    )
    treatment = kernel.decide(
        DecisionContext(
            action="continue_work",
            consequential=False,
            authority=None,
            intelligence=(block,),
            relationships=tuple(graph),
            task_target="NAYA-NODE-0001",
        )
    )

    assert control.outcome == "executed"
    assert treatment.outcome == "executed_with_relationship_aware_intelligence"
    assert treatment.next_state["retained_intelligence_applied"] == "true"
    assert "IB-NAYA-NODE-0001-0001" in treatment.next_state["retained_intelligence_ids"]
    assert any(
        evidence == "CONNECT.relationship:rel-proof:VERIFIED_BY"
        for evidence in treatment.evidence
    )


def test_connect_never_grants_consequential_authority():
    row = _row()
    relationships = _relationships()

    def fake_request(request):
        query = parse_qs(urlparse(request.full_url).query)
        return (
            json.dumps([row] if "intelligent_block_id" in query else relationships)
            .encode()
        )

    reader = SupabaseIntelligentBlockReader(
        url="https://example.supabase.co",
        access_token="user-token",
        request=fake_request,
    )
    block, graph = reader.get_context(
        intelligent_block_id="IB-NAYA-NODE-0001-0001",
        owner_id="owner-1",
    )

    result = Kernel().decide(
        DecisionContext(
            action="publish_change",
            consequential=True,
            authority=None,
            intelligence=(block,),
            relationships=tuple(graph),
            task_target="NAYA-NODE-0001",
        )
    )

    assert result.executed is False
    assert result.allowed is False
    assert result.blocked_by.value == "LAW"

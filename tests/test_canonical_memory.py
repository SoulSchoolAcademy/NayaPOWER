from dataclasses import dataclass
from pathlib import Path

import pytest

from kernel.nayapower_kernel import Authority, DecisionContext, Kernel, TruthState
from runtime.canonical_memory import (
    CanonicalMemoryConfiguration,
    CanonicalMemoryError,
    RetrievedIntelligentBlock,
    SupabaseCanonicalMemory,
)


@dataclass
class FakeResponse:
    status: int
    body: object


class FakeTransport:
    def __init__(self, response: FakeResponse):
        self.response = response
        self.calls = []

    def request(self, method, url, headers, body):
        self.calls.append(
            {
                "method": method,
                "url": url,
                "headers": headers,
                "body": body,
            }
        )
        return self.response


def _valid_block():
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
        "source_event_ids": ["950ea5c5-24f3-4777-aa8f-29a28efe4ba0"],
        "evidence_refs": [{"receipt": "AAA-LIVE-BRAIN-RECEIPT-001"}],
        "provenance": {"stage": "DISTILL+PERSIST", "source": "AAA-LIVE-BRAIN"},
        "applicable_scope": {"target": "NAYA-NODE-0001"},
        "content": {
            "lesson": "Preserve provenance before applying retained intelligence; retrieval never grants authority."
        },
        "schema_version": "INTELLIGENT_BLOCK_V1",
    }


def test_canonical_memory_requires_an_authenticated_access_token():
    with pytest.raises(CanonicalMemoryError, match="access token"):
        CanonicalMemoryConfiguration(
            supabase_url="https://example.supabase.co",
            anon_key="anon",
            access_token="",
        )


def test_canonical_memory_retrieves_owner_scoped_block_via_canonical_rpc():
    transport = FakeTransport(FakeResponse(200, _valid_block()))
    memory = SupabaseCanonicalMemory(
        CanonicalMemoryConfiguration(
            supabase_url="https://example.supabase.co",
            anon_key="anon",
            access_token="user-token",
        ),
        transport=transport,
    )

    block = memory.retrieve_block(
        "9f1f9d3c-0f0a-4a58-8f4f-000000000001"
    )

    assert isinstance(block, RetrievedIntelligentBlock)
    assert block.intelligent_block_id == "IB-NAYA-NODE-0001-0001"
    assert block.subject_id == "NAYA-NODE-0001"
    assert block.version == 1
    assert block.owner_scope == "PRIVATE"
    assert block.understanding_state == "VERIFIED"
    assert block.source_event_ids
    assert block.provenance
    assert transport.calls[0]["method"] == "POST"
    assert transport.calls[0]["url"].endswith(
        "/rest/v1/rpc/nayanet_retrieve_intelligent_block"
    )
    assert transport.calls[0]["headers"]["Authorization"] == "Bearer user-token"
    assert transport.calls[0]["body"] == {
        "p_block_id": "9f1f9d3c-0f0a-4a58-8f4f-000000000001"
    }


def test_canonical_memory_rejects_malformed_or_non_live_blocks():
    malformed = _valid_block()
    malformed["source_event_ids"] = []

    transport = FakeTransport(FakeResponse(200, malformed))
    memory = SupabaseCanonicalMemory(
        CanonicalMemoryConfiguration(
            supabase_url="https://example.supabase.co",
            anon_key="anon",
            access_token="user-token",
        ),
        transport=transport,
    )

    with pytest.raises(CanonicalMemoryError, match="source_event_ids"):
        memory.retrieve_block(malformed["block_id"])

    deleted = _valid_block()
    deleted["status"] = "DELETED"
    transport.response = FakeResponse(200, deleted)

    with pytest.raises(CanonicalMemoryError, match="status"):
        memory.retrieve_block(deleted["block_id"])


def test_retrieved_intelligence_changes_non_authoritative_behavior_but_cannot_grant_authority():
    block = RetrievedIntelligentBlock.from_payload(_valid_block())
    kernel = Kernel()

    control = kernel.decide(
        DecisionContext(
            action="continue_work",
            consequential=False,
            authority=None,
            task_target="NAYA-NODE-0001",
        )
    )
    treatment = kernel.decide(
        DecisionContext(
            action="continue_work",
            consequential=False,
            authority=None,
            task_target="NAYA-NODE-0001",
            intelligence=(block,),
        )
    )

    assert control.executed is True
    assert treatment.executed is True
    assert control.outcome == "executed"
    assert treatment.outcome == "executed"
    assert "retained_intelligence_applied" not in treatment.next_state

    blocked = kernel.decide(
        DecisionContext(
            action="publish_change",
            consequential=True,
            authority=None,
            task_target="NAYA-NODE-0001",
            intelligence=(block,),
        )
    )

    assert blocked.executed is False
    assert blocked.truth_state is TruthState.BLOCKED


def test_canonical_memory_retrieves_relationship_context_for_connect():
    relationships = [
        {
            "relationship_id": "82ea8862-4246-47d7-8e62-c8729b195294",
            "source_id": "NAYA-KERNEL-PROVE",
            "target_id": "IB-NAYA-NODE-0001-0001",
            "relationship_type": "VERIFIED_BY",
            "provenance": {"source": "AAA-LIVE-BRAIN"},
            "epistemic_state": "VERIFIED",
        }
    ]
    transport = FakeTransport(FakeResponse(200, relationships))
    memory = SupabaseCanonicalMemory(
        CanonicalMemoryConfiguration(
            supabase_url="https://example.supabase.co",
            anon_key="anon",
            access_token="user-token",
        ),
        transport=transport,
    )

    result = memory.retrieve_relationships("IB-NAYA-NODE-0001-0001")

    assert len(result) == 1
    assert result[0].relationship_id == "82ea8862-4246-47d7-8e62-c8729b195294"
    assert result[0].relationship_type == "VERIFIED_BY"
    assert result[0].epistemic_state == "VERIFIED"
    assert transport.calls[-1]["method"] == "GET"
    assert "/rest/v1/nayanet_brain_relationships?" in transport.calls[-1]["url"]
    assert "target_id=eq.IB-NAYA-NODE-0001-0001" in transport.calls[-1]["url"]


def test_relationship_aware_retrieval_is_required_for_retained_intelligence_influence():
    block = RetrievedIntelligentBlock.from_payload(_valid_block())
    memory_relationship_fixture = {
        "relationship_id": "r1",
        "source_id": "NAYA-KERNEL-PROVE",
        "target_id": block.intelligent_block_id,
        "relationship_type": "VERIFIED_BY",
        "provenance": {"source": "proof"},
        "epistemic_state": "VERIFIED",
    }
    from runtime.canonical_memory import RetrievedRelationship

    graph_edge = RetrievedRelationship.from_payload(memory_relationship_fixture)
    kernel = Kernel()

    no_graph = kernel.decide(
        DecisionContext(
            action="continue_work",
            consequential=False,
            authority=None,
            task_target="NAYA-NODE-0001",
            intelligence=(block,),
        )
    )
    with_graph = kernel.decide(
        DecisionContext(
            action="continue_work",
            consequential=False,
            authority=None,
            task_target="NAYA-NODE-0001",
            intelligence=(block,),
            relationships=(graph_edge,),
        )
    )

    assert no_graph.outcome == "executed"
    assert with_graph.outcome == "executed_with_relationship_aware_intelligence"
    assert with_graph.next_state["retained_intelligence_applied"] == "true"
    assert any(
        evidence.startswith("CONNECT.relationship:") for evidence in with_graph.evidence
    )

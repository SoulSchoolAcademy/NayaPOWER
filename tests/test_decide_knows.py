"""Phase 2 wiring tests: ACT's decisions query KNOW's memory.

Covers the ACT -> KNOW seam added in ``Kernel.decide()``:
``kernel/knowledge_query.py::retrieve_applicable_intelligence`` plus the
decide() wiring (next_state, evidence, trace, graceful degradation, and the
evaluate_candidates hook).
"""

import json
from types import SimpleNamespace

import pytest

from kernel.knowledge_query import retrieve_applicable_intelligence
from kernel.nayapower_kernel import Authority, DecisionContext, Kernel, Node, TruthState
from kernel.value_calculus import (
    QUALITY_DIMENSIONS,
    Candidate,
    PVEstimate,
)


def _note(block_id, title, keywords, truth_state="VERIFIED", lifecycle="ACTIVE"):
    return {
        "intelligent_block_id": block_id,
        "title": title,
        "keywords": keywords,
        "category": "operations",
        "topic": "deployment",
        "subtopic": "",
        "truth_state": truth_state,
        "lifecycle_state": lifecycle,
        "captured_at": "2026-10-09T00:00:00Z",
        "projection_path": "BRAIN/05-MEMORY/SMART-NOTES/does-not-exist.md",
    }


@pytest.fixture()
def mock_registry(tmp_path, monkeypatch):
    """Point knowledge_query at a caller-supplied registry file."""

    def _install(entries):
        path = tmp_path / "index.json"
        path.write_text(json.dumps({"entries": entries}), encoding="utf-8")
        monkeypatch.setattr("kernel.knowledge_query.REGISTRY", path)
        return path

    return _install


def _deploy_context():
    return DecisionContext(
        action="deploy",
        consequential=True,
        authority=Authority(scope="deploy"),
    )


def test_decide_consults_knowledge_for_matching_intelligence(mock_registry):
    mock_registry(
        [
            _note(
                "IB-TEST-DEPLOY-001",
                "Deploy decisions require a staged rollout with automatic rollback",
                ["deploy", "rollout", "rollback"],
            ),
            _note(
                "IB-TEST-UNRELATED-001",
                "Gardening tips for the office plants",
                ["watering", "sunlight"],
            ),
        ]
    )

    result = Kernel().decide(_deploy_context())

    assert result.allowed is True
    assert result.next_state["intelligence_count"] >= 1
    consulted = result.next_state["intelligence_consulted"]
    assert len(consulted) == result.next_state["intelligence_count"]
    ids = [r["entry"]["intelligent_block_id"] for r in consulted]
    assert "IB-TEST-DEPLOY-001" in ids
    assert "IB-TEST-UNRELATED-001" not in ids
    # Trace shows KNOW ran; evidence names the consultation.
    assert result.trace == (Node.SELF, Node.LAW, Node.KNOW)
    assert f"KNOW.intelligence:{result.next_state['intelligence_count']}_blocks_consulted" in result.evidence
    # Provenance is recorded on every consulted block.
    for r in consulted:
        assert r["provenance"]["source"] == "repository_projection_index"
        assert "deploy" in r["provenance"]["query"]
        assert r["truth_state"] == "VERIFIED"
        assert "explanation" in r


def test_decide_with_empty_registry_still_allows(mock_registry):
    mock_registry([])

    result = Kernel().decide(_deploy_context())

    assert result.allowed is True
    assert result.executed is False
    assert result.truth_state is TruthState.UNKNOWN
    assert result.next_state["intelligence_count"] == 0
    assert result.next_state["intelligence_consulted"] == []
    assert result.trace == (Node.SELF, Node.LAW)
    assert "KNOW.intelligence:0_blocks_consulted" in result.evidence


def test_decide_survives_know_outage(tmp_path, monkeypatch):
    # Registry file missing entirely: KNOW is down, LAW's verdict stands alone.
    monkeypatch.setattr(
        "kernel.knowledge_query.REGISTRY", tmp_path / "no-such-index.json"
    )

    result = Kernel().decide(_deploy_context())

    assert result.allowed is True
    assert result.next_state["intelligence_count"] == 0
    assert result.next_state["intelligence_consulted"] == []
    assert result.trace == (Node.SELF, Node.LAW)


def test_law_prohibited_path_unchanged(mock_registry):
    # Even with applicable intelligence present, a LAW block short-circuits
    # first: KNOW is never consulted on the prohibited path.
    mock_registry(
        [_note("IB-TEST-DEPLOY-001", "Deploy decisions need staged rollouts", ["deploy"])]
    )
    blocked = DecisionContext(
        action="deploy",
        consequential=True,
        authority=None,
    )

    result = Kernel().decide(blocked)

    assert result.allowed is False
    assert result.truth_state is TruthState.BLOCKED
    assert result.blocked_by is Node.LAW
    assert result.trace == (Node.SELF, Node.LAW)
    assert result.next_state == {}


def test_truth_floor_filters_lower_states(mock_registry):
    mock_registry(
        [
            _note("IB-RATIFIED-001", "Deploy with staged rollouts", ["deploy"], truth_state="RATIFIED"),
            _note("IB-VERIFIED-001", "Deploy checklists reduce incidents", ["deploy"], truth_state="VERIFIED"),
            _note("IB-CANDIDATE-001", "Deploy on Fridays maybe", ["deploy"], truth_state="CANDIDATE"),
        ]
    )
    ctx = _deploy_context()

    all_floor = retrieve_applicable_intelligence(ctx, truth_floor="VERIFIED")
    assert {r["entry"]["intelligent_block_id"] for r in all_floor} == {
        "IB-RATIFIED-001",
        "IB-VERIFIED-001",
    }

    ratified_floor = retrieve_applicable_intelligence(ctx, truth_floor="RATIFIED")
    assert [r["entry"]["intelligent_block_id"] for r in ratified_floor] == [
        "IB-RATIFIED-001"
    ]


def test_max_results_caps_returned_intelligence(mock_registry):
    mock_registry(
        [_note(f"IB-DEPLOY-{i:03d}", f"Deploy lesson number {i}", ["deploy"]) for i in range(3)]
    )

    results = retrieve_applicable_intelligence(_deploy_context(), max_results=2)

    assert len(results) == 2


def test_superseded_notes_never_surface(mock_registry):
    mock_registry(
        [
            _note(
                "IB-OLD-001",
                "Deploy decisions need staged rollouts",
                ["deploy"],
                lifecycle="SUPERSEDED",
            )
        ]
    )

    assert retrieve_applicable_intelligence(_deploy_context()) == []


def _candidate(cid, quality_level, pv_b, is_baseline=False):
    return Candidate(
        candidate_id=cid,
        quality={d: quality_level for d in QUALITY_DIMENSIONS},
        confidence={d: 0.95 for d in QUALITY_DIMENSIONS},
        pv=PVEstimate(
            B=pv_b, H=10.0, C=5.0, R=2.0,
            confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
            evidence_count=2,
        ),
        authorized=True,
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        stakes="low",
        reversible=True,
        is_baseline=is_baseline,
    )


def test_candidate_scoring_skips_gracefully_without_candidates(mock_registry):
    mock_registry([])

    result = Kernel().decide(_deploy_context())

    assert "candidate_evaluation" not in result.next_state


def test_candidate_scoring_logs_winner_when_options_present(mock_registry):
    mock_registry([])
    context = SimpleNamespace(
        action="deploy",
        consequential=False,
        authority=None,
        candidates=[
            _candidate("baseline", 8.0, 50.0, is_baseline=True),
            _candidate("challenger", 9.5, 100.0),
        ],
    )

    result = Kernel().decide(context)

    assert result.allowed is True
    evaluation = result.next_state["candidate_evaluation"]
    assert evaluation["selected"] == "challenger"
    assert evaluation["winner_v_safe"] is not None
    assert evaluation["winner_v_safe"] > 0
    assert evaluation["frontier_size"] >= 1

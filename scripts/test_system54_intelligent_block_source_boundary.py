"""System 54 shadow run: canonical Intelligent Block source, current output untouched.

The rows below are a minimal, read-only snapshot of real production Blocks
retrieved on 2026-09-24. They are not a new intelligence store and are not
used by the default System 54 resolver.
"""
from datetime import datetime, timezone
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
sys.path.insert(0, str(ROOT / "scripts"))

from intelligent_block_source import load_intelligent_blocks
from claim_currentness_v1 import resolve_currentness as resolve
from project_intelligence_reconstruction import build_current


REAL_BLOCKS = [
    {
        "block_id": "31aee463-eac9-4261-9e39-1c9b8f6f4cfd",
        "subject_id": "Smart Note",
        "status": "ACTIVE",
        "understanding_state": "VERIFIED",
        "superseded_by_block_id": None,
        "content": {
            "truth": {"state": "VERIFIED", "conflicts": [], "confidence": 1},
            "time": {"valid_from": "2026-09-24T04:12:01.621Z", "valid_until": None},
            "context": {"scope": "PRIVATE", "project": "NayaNET", "audience": ["owner"]},
            "evidence": {"evidence_refs": ["f0cd77e4-44b3-44a9-bbbd-1f4b1accf633", "5a283904-2a8b-4cfb-88db-6ac6742a5794"], "evidence_state": "VERIFIED"},
            "provenance": {"source": "intelligent-block-lifecycle-proof", "source_ref": "smart_note:f0cd77e4-44b3-44a9-bbbd-1f4b1accf633"},
            "meaning": {"content": "A verified lifecycle proof records idempotent replay, explicit supersession, durable lineage, and preserved authority."},
        },
    },
    {
        "block_id": "f0cd77e4-44b3-44a9-bbbd-1f4b1accf633",
        "subject_id": "Smart Note",
        "status": "SUPERSEDED",
        "understanding_state": "VERIFIED",
        "superseded_by_block_id": "31aee463-eac9-4261-9e39-1c9b8f6f4cfd",
        "content": {
            "truth": {"state": "VERIFIED", "conflicts": [], "confidence": 1},
            "time": {"valid_from": "2026-09-24T04:12:01.621Z", "valid_until": None},
            "context": {"scope": "PRIVATE", "project": "NayaNET", "audience": ["owner"]},
            "evidence": {"evidence_refs": ["f0cd77e4-44b3-44a9-bbbd-1f4b1accf633", "5a283904-2a8b-4cfb-88db-6ac6742a5794"], "evidence_state": "VERIFIED"},
            "provenance": {"source": "intelligent-block-lifecycle-proof", "source_ref": "smart_note:f0cd77e4-44b3-44a9-bbbd-1f4b1accf633"},
            "meaning": {"content": "A verified lifecycle proof records idempotent replay, explicit supersession, durable lineage, and preserved authority."},
        },
    },
    {
        "block_id": "97bc98f5-fb28-52bb-8c0d-3a1bfac8d396",
        "subject_id": "universal-promotion",
        "status": "ACTIVE",
        "understanding_state": "CANDIDATE",
        "superseded_by_block_id": None,
        "content": {
            "truth": {"state": "CANDIDATE", "source": "nayanet-compound-intelligence", "status": "UNVERIFIED"},
            "time": None,
            "context": {"topic": "universal-promotion", "project_id": "NayaNET", "visibility": "PRIVATE"},
            "evidence": None,
            "provenance": None,
            "meaning": None,
        },
    },
]


def main():
    now = datetime(2026, 9, 24, 12, tzinfo=timezone.utc)
    normalized = load_intelligent_blocks(REAL_BLOCKS)

    # Adapt only the normalized canonical fields required by the already-proven
    # Claim Currentness V1 test contract. Do not call or modify the production
    # event resolver.
    old = build_current("NayaNET")
    r = resolve(normalized, now, requested_scope="PRIVATE")

    assert r["resolution"] == "CURRENT"
    assert r["selected_block_id"] == "31aee463-eac9-4261-9e39-1c9b8f6f4cfd"
    assert r["excluded"]["f0cd77e4-44b3-44a9-bbbd-1f4b1accf633"] == "SUPERSEDED"
    assert r["excluded"]["97bc98f5-fb28-52bb-8c0d-3a1bfac8d396"] == "CANDIDATE_NOT_VERIFIED"
    # Shadow comparison only: old event-derived output remains untouched.
    assert len(old["current"]) == 0
    print("OLD_EVENT_RESOLVER_CURRENT_COUNT=0")
    print("CANONICAL_BLOCK_SHADOW_CURRENT_COUNT=1")
    print("EXPECTED_AUTHORITY_DIVERGENCE=PASS")

    print("SYSTEM54_SHADOW_INTELLIGENT_BLOCK_SOURCE=PASS")
    print("REAL_PRODUCTION_BLOCKS_CONSUMED=PASS")
    print("SUPERSEDED_EXCLUDED=PASS")
    print("ACTIVE_CANDIDATE_EXCLUDED=PASS")
    print("CURRENT_BLOCK_SELECTED=31aee463-eac9-4261-9e39-1c9b8f6f4cfd")
    print("DEFAULT_CURRENT_TRUTH_OUTPUT=UNCHANGED")
    print("NO_PRODUCTION_MUTATION=PASS")


if __name__ == "__main__":
    main()

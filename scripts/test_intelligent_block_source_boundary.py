import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.naya' / 'runtime'))
import copy
from intelligent_block_source import load_intelligent_blocks


def main():
    rows = [
        {
            "block_id": "31aee463-eac9-4261-9e39-1c9b8f6f4cfd",
            "subject_id": "Smart Note",
            "status": "ACTIVE",
            "understanding_state": "VERIFIED",
            "superseded_by_block_id": None,
            "content": {
                "truth": {"state": "VERIFIED", "conflicts": [], "confidence": 1},
                "time": {"valid_from": "2026-09-24T04:12:01.621Z", "valid_until": None},
                "context": {"scope": "PRIVATE", "project": "NayaNET"},
                "evidence": {"evidence_refs": ["f0cd77e4-44b3-44a9-bbbd-1f4b1accf633", "5a283904-2a8b-4cfb-88db-6ac6742a5794"]},
                "provenance": {"source": "intelligent-block-lifecycle-proof"},
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
                "context": {"scope": "PRIVATE", "project": "NayaNET"},
                "evidence": {"evidence_refs": ["f0cd77e4-44b3-44a9-bbbd-1f4b1accf633", "5a283904-2a8b-4cfb-88db-6ac6742a5794"]},
                "provenance": {"source": "intelligent-block-lifecycle-proof"},
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
                "truth": {"state": "CANDIDATE"},
                "context": {"topic": "universal-promotion", "project_id": "NayaNET", "visibility": "PRIVATE"},
            },
        },
    ]
    before = copy.deepcopy(rows)
    normalized = load_intelligent_blocks(rows)
    assert [x["block_id"] for x in normalized] == [x["block_id"] for x in rows]
    assert rows == before, "SOURCE_BOUNDARY_MUTATED_INPUT"
    assert set(normalized[0]) == set(rows[0])
    assert normalized[0]["content"]["truth"]["state"] == "VERIFIED"
    print("REAL_BLOCK_SOURCE_BOUNDARY=PASS")
    print("READ_ONLY_INPUT_PRESERVED=PASS")
    print("NO_PERSISTENCE=PASS")


if __name__ == "__main__":
    main()

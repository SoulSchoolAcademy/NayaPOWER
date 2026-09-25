import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.naya' / 'memory'))
sys.path.insert(0, str(ROOT / '.naya' / 'runtime'))

import smart_notes_v3 as smart_brain
from restore_context import build_restore


EXPECTED_ID = 'IB-000003'
EXPECTED_BLOCK_ID = 'b06846b3-49eb-45c1-8557-a986831f0d4c'
EXPECTED_OWNER_ID = '48c40e43-8cca-4c6e-9427-d3bfd7d788db'
EXPECTED_SOURCE_EVENT_ID = EXPECTED_BLOCK_ID


def test_receiver_backed_ib000003_has_exact_canonical_repository_projection():
    registry = json.loads((ROOT / '.naya/memory/smart-notes/REGISTRY.json').read_text(encoding='utf-8'))
    entry = next((x for x in registry['entries'] if x['intelligent_block_id'] == EXPECTED_ID), None)
    assert entry is not None

    projection = ROOT / entry['path']
    assert projection.is_file()

    text = projection.read_text(encoding='utf-8')
    assert EXPECTED_ID in text
    assert EXPECTED_BLOCK_ID in text
    assert EXPECTED_OWNER_ID in text
    assert EXPECTED_SOURCE_EVENT_ID in text


def test_authorized_canonical_retrieval_returns_ib000003_projection():
    result = smart_brain.retrieve_canonical_ibs(
        'Wave A canonical September 17 shell acceptance',
        principal_id=EXPECTED_OWNER_ID,
        scope='PRIVATE',
        project='NayaNET',
        principal_project='NayaNET',
    )
    ids = {item['intelligent_block_id'] for item in result}
    assert EXPECTED_ID in ids


def test_projection_does_not_invent_missing_receiver_metadata():
    registry = json.loads((ROOT / '.naya/memory/smart-notes/REGISTRY.json').read_text(encoding='utf-8'))
    entry = next(x for x in registry['entries'] if x['intelligent_block_id'] == EXPECTED_ID)

    assert entry['owner'] == EXPECTED_OWNER_ID
    assert entry['scope'] == 'PRIVATE'
    assert entry['project'] == 'NayaNET'
    assert entry['permissions'] == {'access': 'PRIVATE'}
    assert entry['authority'] is None
    assert entry['learning_state'] is None


def test_cold_restore_reconstructs_ib000003_in_canonical_memory_context():
    result = build_restore(
        'Wave A canonical September 17 shell acceptance',
        limit=5,
        principal_id=EXPECTED_OWNER_ID,
        scope='PRIVATE',
        project='NayaNET',
        principal_project='NayaNET',
    )
    selected = result['memory']['selected']
    ib = next(item for item in selected if item['intelligent_block_id'] == EXPECTED_ID)

    assert result['validation']['passed'] is True
    assert ib['owner'] == EXPECTED_OWNER_ID
    assert ib['scope'] == 'PRIVATE'
    assert ib['project'] == 'NayaNET'
    assert ib['source']['provenance']['source_event_id'] == EXPECTED_SOURCE_EVENT_ID
    assert result['memory']['count_visible'] == 1

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.naya' / 'memory'))

import smart_notes_v3 as smart_brain


def test_repository_only_ib_projections_are_not_active_canonical_registry_entries():
    registry = json.loads((ROOT / '.naya/memory/smart-notes/REGISTRY.json').read_text(encoding='utf-8'))
    active_ids = {entry['intelligent_block_id'] for entry in registry['entries']}

    assert 'IB-000001' not in active_ids
    assert 'IB-000002' not in active_ids
    assert (ROOT / '.naya/memory/archive/legacy-pre-2026-09-25/smart-notes/2026/09/24/system/canonical-smart-note-system/IB-000001/smart-note.md').is_file()
    assert (ROOT / '.naya/memory/archive/legacy-pre-2026-09-25/smart-notes/2026/09/24/system/superbrain-scorecard/IB-000002/smart-note.md').is_file()


def test_repository_principal_cannot_retrieve_non_receiver_ib_projections():
    result = smart_brain.retrieve_canonical_ibs(
        '', principal_id='shawn', scope='personal', project='NayaNET', principal_project='NayaNET'
    )
    assert 'IB-000001' not in {item['intelligent_block_id'] for item in result}
    assert 'IB-000002' not in {item['intelligent_block_id'] for item in result}

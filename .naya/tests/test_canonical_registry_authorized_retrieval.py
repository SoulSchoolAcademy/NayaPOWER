import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.naya' / 'memory'))

import smart_notes_v3 as smart_brain


def test_cold_repository_principal_does_not_receive_unproven_registry_ibs():
    result = smart_brain.retrieve_canonical_ibs(
        '',
        principal_id='shawn',
        scope='personal',
        project='NayaNET',
        principal_project='NayaNET',
    )

    assert result == []

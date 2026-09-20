#!/usr/bin/env python3
"""Regression tests for the canonical/idempotent event-write boundary."""
from __future__ import annotations
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / '.naya' / 'runtime' / 'canonical_event_store.py'

def load_module():
    spec = importlib.util.spec_from_file_location('canonical_event_store', MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def event(event_id='SE-20260825-235000-canonical-write-test', title='Canonical write test'):
    return {
        'event_id': event_id,
        'created_at': '2026-08-25T23:50:00+00:00',
        'effective_at': '2026-08-25T23:50:00+00:00',
        'event_type': 'test',
        'subject': 'Canonical event write boundary',
        'title': title,
        'status': 'CANONICAL',
        'source': {'kind': 'test', 'event_id': 'TEST-SOURCE-001'},
        'representations': {
            'naya': {'id': 'SN-20260825-235000-canonical-write-test-naya', 'representation': 'NAYA', 'summary': title},
            'human': {'id': 'SN-20260825-235000-canonical-write-test-human', 'representation': 'HUMAN', 'summary': title},
        },
        'verification': {'status': 'UNVERIFIED'},
    }

def main() -> int:
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        events = root / 'events'
        index = events / 'INDEX.json'
        first = event()
        created = mod.create_or_replay(first, events, index)
        assert created['status'] == 'CREATED'
        assert Path(created['path']).exists()
        assert json.loads(index.read_text(encoding='utf-8'))['event_count'] == 1

        replay = mod.create_or_replay(first, events, index)
        assert replay['status'] == 'REPLAY'
        assert len(list(events.rglob('SE-*.json'))) == 1

        conflict = event(title='Conflicting payload')
        conflict['source']['event_id'] = 'TEST-SOURCE-002'
        result = mod.create_or_replay(conflict, events, index)
        assert result['status'] == 'CONFLICT'
        assert len(list(events.rglob('SE-*.json'))) == 1

        invalid = event(event_id='not-an-event-id')
        try:
            mod.create_or_replay(invalid, events, index)
        except ValueError:
            pass
        else:
            raise AssertionError('deliberate invalid event_id must fail visibly')

    print('PASS — canonical event-write regression GREEN')
    print('positive=create,replay; deliberate_failures=conflict,invalid_id')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

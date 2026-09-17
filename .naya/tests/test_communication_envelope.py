#!/usr/bin/env python3
"""Communication-envelope Step 1 tests: record_type / thread_id / parent_id /
derived root_id / author_ref validation, parent existence, self-parent
rejection, cycle detection, backward compatibility, and CREATED->REPLAY
idempotency of envelope-carrying events."""
from __future__ import annotations
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEMORY = ROOT / '.naya' / 'memory'
RUNTIME = ROOT / '.naya' / 'runtime'

def load_smart_notes():
    sys.path.insert(0, str(MEMORY))
    spec = importlib.util.spec_from_file_location('smart_notes_v3', MEMORY / 'smart_notes_v3.py')
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def load_event_store():
    spec = importlib.util.spec_from_file_location('canonical_event_store', RUNTIME / 'canonical_event_store.py')
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

sn = load_smart_notes()

def event_path(event_id='SE-20260916-013000-envelope-step1-test'):
    return Path('2026/09/16/01') / f'{event_id}.json'

def base_event(event_id='SE-20260916-013000-envelope-step1-test'):
    return {
        'event_id': event_id,
        'created_at': '2026-09-16T01:30:00+00:00',
        'effective_at': '2026-09-16T01:30:00+00:00',
        'event_type': 'envelope-test',
        'subject': 'Envelope Step 1',
        'title': 'Envelope Step 1',
        'status': 'ACTIVE',
        'source': {'kind': 'test', 'event_id': 'TEST-SOURCE-ENV-001'},
        'representations': {
            'naya': {'id': 'SN-20260916-013000-envelope-step1-test-naya', 'representation': 'NAYA', 'summary': 'Envelope Step 1'},
        },
    }

def test_legacy_event_remains_valid():
    e = base_event()
    errs = sn.validate_event(e, event_path())
    assert errs == [], errs

def test_valid_envelope_event_with_thread_fields():
    e = base_event()
    e.update({'record_type': 'FINDING', 'thread_id': 'THR-envelope-step1'})
    errs = sn.validate_event(e, event_path())
    assert errs == [], errs
    errs = sn.validate_thread_links([(event_path(), e)], [])
    assert errs == [], errs

def test_invalid_record_type_rejected():
    e = base_event()
    e['record_type'] = 'NOT-A-TYPE'
    errs = sn.validate_event(e, event_path())
    assert any('invalid record_type' in x for x in errs), errs

def test_invalid_thread_id_rejected():
    e = base_event()
    e['thread_id'] = 'not-a-thread'
    errs = sn.validate_event(e, event_path())
    assert any('invalid thread_id' in x for x in errs), errs

def test_invalid_parent_and_root_patterns_rejected():
    e = base_event()
    e['parent_id'] = 'THR-wrong'
    errs = sn.validate_event(e, event_path())
    assert any('invalid parent_id' in x for x in errs), errs
    e2 = base_event()
    e2['root_id'] = 'ROOT-nope'
    errs = sn.validate_event(e2, event_path())
    assert any('invalid root_id' in x for x in errs), errs

def test_self_parent_rejected():
    e = base_event()
    e['parent_id'] = e['event_id']
    errs = sn.validate_event(e, event_path())
    assert any('self-parent' in x for x in errs), errs

def test_author_ref_validated_minimally():
    e = base_event()
    e['author_ref'] = 'naya-builder-001'
    errs = sn.validate_event(e, event_path())
    assert errs == [], errs
    e2 = base_event()
    e2['author_ref'] = ''
    errs = sn.validate_event(e2, event_path())
    assert any('invalid author_ref' in x for x in errs), errs
    e3 = base_event()
    e3['author_ref'] = 'x' * 300
    errs = sn.validate_event(e3, event_path())
    assert any('invalid author_ref' in x for x in errs), errs

def test_missing_parent_rejected():
    child = {'event_id': 'SE-20260916-013001-envelope-child', 'parent_id': 'SE-20260916-999999-does-not-exist'}
    errs = sn.validate_thread_links([(event_path(), child)], [])
    assert any('parent_id' in x and 'does not exist' in x for x in errs), errs

def test_cycle_detected():
    a = {'event_id': 'SE-20260916-013001-envelope-a', 'parent_id': 'SE-20260916-013002-envelope-b'}
    b = {'event_id': 'SE-20260916-013002-envelope-b', 'parent_id': 'SE-20260916-013001-envelope-a'}
    errs = sn.validate_thread_links([(event_path(), a), (event_path(), b)], [])
    assert any('cyclic' in x for x in errs), errs

def test_root_id_derivation_matches():
    a = {'event_id': 'SE-20260916-013001-envelope-a'}
    b = {'event_id': 'SE-20260916-013002-envelope-b', 'parent_id': 'SE-20260916-013001-envelope-a', 'root_id': 'SE-20260916-013001-envelope-a'}
    errs = sn.validate_thread_links([(event_path(), a), (event_path(), b)], [])
    assert errs == [], errs

def test_root_id_mismatch_rejected():
    a = {'event_id': 'SE-20260916-013001-envelope-a'}
    b = {'event_id': 'SE-20260916-013002-envelope-b', 'parent_id': 'SE-20260916-013001-envelope-a', 'root_id': 'SE-20260916-013003-envelope-wrong'}
    errs = sn.validate_thread_links([(event_path(), a), (event_path(), b)], [])
    assert any('root_id' in x for x in errs), errs

def test_root_id_without_parent_must_be_self():
    a = {'event_id': 'SE-20260916-013001-envelope-a', 'root_id': 'SE-20260916-999999-envelope-other'}
    errs = sn.validate_thread_links([(event_path(), a)], [])
    assert any('must equal event_id' in x for x in errs), errs

def test_created_then_replay_preserves_idempotency():
    store = load_event_store()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        events = root / 'events'
        index = events / 'INDEX.json'
        e = base_event()
        e.update({'record_type': 'FINDING', 'thread_id': 'THR-envelope-step1'})
        created = store.create_or_replay(e, events, index)
        assert created['status'] == 'CREATED'
        replay = store.create_or_replay(e, events, index)
        assert replay['status'] == 'REPLAY'
        assert replay['fingerprint'] == store.content_fingerprint(e)
        assert len(list(events.rglob('SE-*.json'))) == 1
        assert json.loads(index.read_text(encoding='utf-8'))['event_count'] == 1

def main() -> int:
    checks = [v for k, v in sorted(globals().items()) if k.startswith('test_') and callable(v)]
    for fn in checks:
        fn()
    print(f'PASS — communication envelope Step 1 GREEN ({len(checks)} checks)')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
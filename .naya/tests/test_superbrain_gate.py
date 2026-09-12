#!/usr/bin/env python3
"""Deterministic regression checks for the canonical Superbrain runtime."""
from __future__ import annotations
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEMORY = ROOT / '.naya' / 'memory'
RUNTIME = MEMORY / 'smart_notes_v3.py'
INDEX = MEMORY / 'events' / 'INDEX.json'
GRAPH = MEMORY / 'RELATIONSHIP-GRAPH.json'
sys.path.insert(0, str(MEMORY))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


mod = load_module('smart_notes_v3', RUNTIME)
graph_mod = load_module('relationship_graph', MEMORY / 'relationship_graph.py')
audit_mod = load_module('duplicate_entity_audit', MEMORY / 'duplicate_entity_audit.py')

errors = mod.validate()
assert not errors, 'canonical validation failed: ' + '; '.join(errors)

loaded = [(p, e) for p, e in mod.load_events() if '__parse_error__' not in e]
assert loaded, 'no canonical events found'
assert INDEX.exists(), 'canonical index missing'

idx = json.loads(INDEX.read_text(encoding='utf-8'))
ids = {e['event_id'] for _, e in loaded}
indexed = {e['event_id'] for e in idx['events']}
assert ids == indexed, f'index mismatch: canonical={len(ids)} indexed={len(indexed)}'

# Every canonical event must have both human and Naya-readable representations.
# Stable SN-* IDs are a v3 hardening target, not a reason to reject the existing
# migrated legacy envelope before the dedicated schema-freeze phase (#2/#6).
for path, event in loaded:
    reps = mod.reps(event)
    assert reps, f'{event.get("event_id")}: missing representations'
    if isinstance(event.get('representations'), dict):
        keys = set(event['representations'])
        assert 'naya' in keys, f'{event.get("event_id")}: missing Naya representation'
        assert 'human' in keys or 'shawn' in keys, f'{event.get("event_id")}: missing human representation'
    for rep in reps:
        role = str(rep.get('representation', '')).lower()
        if role == 'machine':
            machine_operable = any(rep.get(k) for k in (
                'title', 'summary', 'content', 'schema_role', 'retrieval_keys',
                'required_representation_roles', 'single_canonical_event',
                'required_delivery', 'classification', 'supersession_policy',
                'authority', 'consumers', 'verification_requirement'
            ))
            assert machine_operable, f'{event.get("event_id")}: machine representation is not machine-operable'
            continue
        readable = any(rep.get(k) for k in ('title', 'summary', 'content', 'lessons', 'what_we_learned', 'learning'))
        assert readable, f'{event.get("event_id")}: unreadable note representation'

# Exact duplicates are a hard failure; ambiguous candidates are surfaced, never merged.
audit = audit_mod.audit()
assert audit['exact_duplicate_count'] == 0, f'exact duplicate events detected: {audit["exact_duplicate_event_ids"]}'

# Relationship graph must be reproducible from canonical events.
graph = graph_mod.build()
assert GRAPH.exists(), 'relationship graph was not generated'
assert graph['event_count'] == len(loaded), 'relationship graph node count mismatch'
assert set(graph['nodes']) == ids, 'relationship graph node set mismatch'

# Retrieval must return deterministic results for a canonical query.
results = mod.retrieve('Superbrain CIS Naya Power', limit=5)
assert results, 'retrieval returned no results'
assert any('superbrain' in mod.all_text(e).lower() for _, e in results), 'retrieval failed to surface Superbrain context'

# Daily CIS must be source-event based and explicitly require verification.
report = mod.daily_report('2026-08-25', 'America/Vancouver')
assert report['report_type'] == 'DAILY_INTELLIGENCE_REPORT'
assert report['verification_required'] is True
assert isinstance(report['source_event_ids'], list)

print('PASS — Superbrain regression suite GREEN')
print(f'canonical_events={len(loaded)}')
print(f'retrieval_results={len(results)}')
print(f'graph_edges={graph["edge_count"]}')
print(f'daily_source_events={len(report["source_event_ids"])}')

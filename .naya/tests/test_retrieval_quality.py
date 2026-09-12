#!/usr/bin/env python3
"""Regression and deliberate-failure tests for dependency-free smart retrieval."""
from __future__ import annotations
import sys
from pathlib import Path

MEMORY = Path(__file__).resolve().parents[1] / 'memory'
sys.path.insert(0, str(MEMORY))
import smart_notes_v3 as brain

# Retrieval is now authorization-first. Use a controlled authorized corpus so
# this suite tests ranking/query behavior without weakening the production
# deny-by-default security boundary or depending on legacy events that lack
# explicit permission metadata.
FIXTURE_EVENTS = [
    (Path('superbrain-verification.json'), {
        'event_id': 'SE-20260825-220300-superbrain-p0-verification',
        'scope': 'personal',
        'project': 'A',
        'permissions': {'access': 'PRIVATE'},
        'title': 'Superbrain P0 verification',
        'summary': 'verified architecture continuity decision',
        'tags': ['brain-gate'],
        'effective_at': '2026-08-25T22:03:00-07:00',
        'status': 'ACTIVE',
    }),
    (Path('superbrain-decision.json'), {
        'event_id': 'SE-20260825-220301-superbrain-architecture-decision',
        'scope': 'personal',
        'project': 'A',
        'permissions': {'access': 'PRIVATE'},
        'title': 'Decision about the Superbrain architecture and continuity',
        'summary': 'The decision preserves continuity while advancing the architecture.',
        'tags': ['brain-gate'],
        'effective_at': '2026-08-25T22:04:00-07:00',
        'status': 'ACTIVE',
    }),
    (Path('other-project.json'), {
        'event_id': 'SE-20260825-220302-other-project-secret',
        'scope': 'personal',
        'project': 'B',
        'permissions': {'access': 'PRIVATE'},
        'title': 'Ultra secret distinctive marker',
        'summary': 'Must never enter project A retrieval.',
        'tags': ['other'],
        'effective_at': '2026-08-25T22:05:00-07:00',
        'status': 'ACTIVE',
    }),
]

original_load = brain.load_events
try:
    brain.load_events = lambda: FIXTURE_EVENTS
    AUTH = {'principal_id': 'shawn', 'scope': 'personal', 'access_project': 'A'}

    exact = brain.retrieve('SE-20260825-220300-superbrain-p0-verification', limit=1, **AUTH)
    assert exact, 'exact event-id query returned nothing'
    assert exact[0][1]['event_id'] == 'SE-20260825-220300-superbrain-p0-verification'

    expanded = brain.expanded_tokens('decision about the Superbrain')
    assert 'architecture' in expanded
    assert 'continuity' in expanded

    filtered = brain.retrieve('Superbrain', limit=20, tag='brain-gate', **AUTH)
    assert filtered, 'metadata-filtered retrieval returned nothing'
    assert all('brain-gate' in {str(x).lower() for x in (e.get('tags') or [])} for _, e in filtered)

    results = brain.retrieve('What was our decision about the Superbrain?', limit=5, **AUTH)
    assert results, 'expanded retrieval returned nothing'
    assert any('superbrain' in brain.all_text(e).lower() for _, e in results)

    # Deliberate failure: unrelated queries must not manufacture zero-score top-N hits.
    unknown = brain.retrieve('zxqv-unrecoverable-token-9917', limit=5, **AUTH)
    assert unknown == [], 'unmatched query must fail cleanly instead of returning arbitrary events'

    # Deliberate failure: impossible metadata constraints must fail closed.
    impossible = brain.retrieve('Superbrain', limit=5, project='PROJECT-THAT-DOES-NOT-EXIST', **AUTH)
    assert impossible == [], 'impossible metadata filter must fail closed'
finally:
    brain.load_events = original_load

print('PASS — retrieval quality regression + deliberate-failure suite GREEN')
print(f'exact_top={exact[0][1]["event_id"]}')
print(f'filtered_results={len(filtered)}')
print(f'expanded_results={len(results)}')
print('unknown_query=EMPTY')
print('impossible_filter=EMPTY')

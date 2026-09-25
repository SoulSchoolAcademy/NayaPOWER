#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.naya/memory'))
import smart_notes_v3 as brain
import duplicate_entity_audit as duplicates


class SmartBrainV3Tests(unittest.TestCase):
    def test_canonical_events_are_valid(self):
        self.assertEqual(brain.validate(), [], 'canonical Smart Brain validation failed')

    def test_index_is_rebuildable(self):
        data = brain.build_index()
        ids = {e['event_id'] for _, e in brain.load_events() if not e.get('__parse_error__')}
        indexed_ids = {e['event_id'] for e in data['events']}
        self.assertEqual(indexed_ids, ids)
        self.assertEqual(data['version'], '3.0.0')

    def test_hybrid_retrieval_returns_verified_context(self):
        events = [
            (Path('A.json'), {'event_id': 'A-1', 'scope': 'personal', 'project': 'A', 'permissions': {'access': 'PRIVATE'}, 'title': 'MAXESS scoring Continue terminal', 'summary': 'verified context', 'effective_at': '2026-09-09T10:00:00-07:00', 'status': 'ACTIVE', 'verification': {'status': 'VERIFIED'}, 'representations': [{'id': 'SN-20260909-100000-a', 'content': 'verified context'}]}),
        ]
        original_load = brain.load_events
        try:
            brain.load_events = lambda: events
            results = brain.retrieve('MAXESS scoring Continue terminal', limit=5, principal_id='shawn', scope='personal', access_project='A')
        finally:
            brain.load_events = original_load
        self.assertTrue(results)
        self.assertTrue(any(e.get('verification', {}).get('status') == 'VERIFIED' for _, e in results))

    def test_alias_or_concept_retrieval(self):
        events = [
            (Path('A.json'), {'event_id': 'A-1', 'scope': 'personal', 'project': 'A', 'permissions': {'access': 'PRIVATE'}, 'title': 'Smart Brain Memory Architecture', 'summary': 'CIS continuity', 'effective_at': '2026-09-09T10:00:00-07:00', 'status': 'ACTIVE', 'representations': [{'id': 'SN-20260909-100001-a', 'content': 'memory architecture CIS'}]}),
        ]
        original_load = brain.load_events
        try:
            brain.load_events = lambda: events
            results = brain.retrieve('super brain memory architecture CIS', limit=10, principal_id='shawn', scope='personal', access_project='A')
        finally:
            brain.load_events = original_load
        self.assertTrue(results)
        joined = ' '.join((e.get('title') or e.get('subject') or '').lower() for _, e in results)
        self.assertTrue('smart' in joined or 'cis' in joined or 'memory' in joined)

    def test_daily_report_is_source_linked(self):
        events = [
            (Path('A.json'), {'event_id': 'A-1', 'scope': 'personal', 'project': 'A', 'permissions': {'access': 'PRIVATE'}, 'title': 'Daily authorized event', 'effective_at': '2026-08-25T10:00:00-07:00', 'status': 'ACTIVE', 'representations': [{'id': 'SN-20260825-100000-a', 'content': 'lesson'}]}),
        ]
        original_load = brain.load_events
        try:
            brain.load_events = lambda: events
            report = brain.daily_report('2026-08-25', principal_id='shawn', scope='personal', project='A')
        finally:
            brain.load_events = original_load
        self.assertEqual(report['report_type'], 'DAILY_INTELLIGENCE_REPORT')
        self.assertIn('source_event_ids', report)
        self.assertTrue(report['verification_required'])
        self.assertEqual(report['source_event_ids'], ['A-1'])

    def test_missing_authorization_denies_runtime_retrieval(self):
        results = brain.retrieve('anything', limit=5)
        self.assertEqual(results, [])

    def test_verified_historical_event_without_canonical_url_is_valid(self):
        event = {
            'event_id': 'SE-20260916-193500-test-historical',
            'created_at': '2026-09-16T19:35:00-07:00',
            'effective_at': '2026-09-16T19:35:00-07:00',
            'status': 'VERIFIED_REPOSITORY_RECORD',
            'source': {'kind': 'execution', 'event_id': 'EXEC-TEST'},
            'representations': [{'id': 'SN-20260916-193500-test-historical', 'content': 'historical lineage'}],
            'verification': {'status': 'VERIFIED'},
        }
        path = brain.EVENTS / '2026' / '09' / '16' / '19' / 'SE-20260916-193500-test-historical.json'
        self.assertEqual(brain.validate_event(event, path), [])

    def test_same_payload_from_distinct_execution_sessions_is_not_a_duplicate(self):
        base = {
            'event_id': 'SE-20260917-035241-test-a',
            'effective_at': '2026-09-17T03:52:41-07:00',
            'created_at': '2026-09-17T03:52:41-07:00',
            'title': 'same action',
            'subject': 'same action',
            'project': 'Naya Power',
            'event_type': 'activity',
            'summary': 'same execution summary',
            'tags': ['activity'],
            'representations': [{'representation': 'NAYA', 'summary': 'same', 'content': 'same'}],
        }
        other = dict(base)
        other['event_id'] = 'SE-20260917-035249-test-b'
        base['execution'] = {'action_id': 'ACT-1', 'run_id': 'RUN-1', 'session_id': 'SESSION-1'}
        other['execution'] = {'action_id': 'ACT-1', 'run_id': 'RUN-2', 'session_id': 'SESSION-2'}
        self.assertEqual(duplicates.classify(base, other)['decision'], 'DISTINCT')

    def test_duplicate_entity_audit_is_green(self):
        report = duplicates.audit()
        self.assertEqual(report['status'], 'GREEN')
        self.assertEqual(report['exact_duplicate_count'], 0)


if __name__ == '__main__':
    unittest.main()

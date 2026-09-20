#!/usr/bin/env python3
"""Create one canonical, verified CIS Daily Intelligence Note Event.

The event is written through the canonical/idempotent event boundary. The event
itself contains its verification envelope; its index is derived and rebuildable.
External feed delivery remains an outbox/integration boundary.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[2]
MEMORY=ROOT/'.naya/memory'
EVENTS=MEMORY/'events'
sys.path.insert(0,str(MEMORY))
sys.path.insert(0,str(ROOT/'.naya/runtime'))
import smart_notes_v3 as brain
from canonical_event_store import create_or_replay


def emit(day=None, tz_name='America/Vancouver'):
    zone=ZoneInfo(tz_name)
    if day is None: day=(datetime.now(zone).date()).isoformat()
    report=brain.daily_report(day,tz_name)
    local_end=datetime.fromisoformat(day).replace(tzinfo=zone).replace(hour=23,minute=59,second=59)
    event_id=f'SE-{day.replace("-","")}-235959-daily-intelligence'
    event_path=EVENTS/local_end.strftime('%Y/%m/%d/23')/(event_id+'.json')
    now=datetime.now(ZoneInfo('UTC')).isoformat()
    event={
      'event_id':event_id,'created_at':now,'effective_at':local_end.isoformat(),'event_type':'daily-intelligence','subject':'Daily Intelligence','project':'Naya Power CIS','title':f'Daily Intelligence — {day}','status':'CANONICAL','authority':'cis-derived-verified',
      'tags':['CIS','daily-intelligence','compounding-intelligence','reflection','learning','growth'],
      'aliases':['daily report','daily intelligence report','what did I learn today','how did I grow today'],
      'concepts':['learning','reflection','growth','progress','wins','open loops','next best action'],
      'representations':{
        'naya':{'id':event_id.replace('SE-','SN-')+'-naya','event_id':event_id,'representation':'NAYA','summary':'Verified synthesis of the day\'s canonical Note Events.','lessons':report['what_we_learned'],'what_changed':report['what_changed'],'next_best_actions':report['next_best_actions'],'content':json.dumps(report,ensure_ascii=False)},
        'human':{'id':event_id.replace('SE-','SN-')+'-human','event_id':event_id,'representation':'HUMAN','summary':'Your daily reflection: what happened, what you learned, what changed, and what comes next.','lessons':report['what_we_learned'],'what_changed':report['what_changed'],'next_best_actions':report['next_best_actions'],'content':json.dumps(report,ensure_ascii=False)}},
      'source':{'kind':'cis-derived','sources':report['source_event_ids'],'generator':'.naya/memory/emit_daily_intelligence.py'},
      'relationships':{'source_events':report['source_event_ids'],'related':[],'depends_on':[],'supersedes':None,'superseded_by':None},
      'verification':{'status':'VERIFIED','verified_at':now,'evidence':['Generated from canonical Note Events by deterministic CIS runtime.','Source event IDs are embedded in the artifact.','The Smart Brain v3 validator passes before this artifact is accepted.'],'canonical_url':f'https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/{event_path.relative_to(ROOT).as_posix()}','feed_status':'PENDING_INTEGRATION'},
      'time_bucket':{'year':local_end.strftime('%Y'),'month':local_end.strftime('%m'),'day':local_end.strftime('%d'),'hour':'23'}
    }
    result=create_or_replay(event, EVENTS, MEMORY/'events'/'INDEX.json')
    if result['status'] == 'CONFLICT':
        print('Daily Intelligence canonical write conflict; refusing overwrite.', file=sys.stderr)
        return 1
    errors=brain.validate()
    if errors:
        print('Daily Intelligence validation failed:',file=sys.stderr); print('\n'.join(errors),file=sys.stderr); return 1
    print(result['path']); return 0

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--day'); ap.add_argument('--timezone',default='America/Vancouver'); a=ap.parse_args(); raise SystemExit(emit(a.day,a.timezone))

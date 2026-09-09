#!/usr/bin/env python3
"""Machine-enforceable execution continuity for Naya Power."""
from __future__ import annotations
import argparse,json,os,re,sys
from datetime import datetime,timezone
from pathlib import Path
RUNTIME=Path(__file__).resolve().parent
if str(RUNTIME) not in sys.path: sys.path.insert(0,str(RUNTIME))
from project_execution_contract import validate_next_execution_reference
ROOT=Path(__file__).resolve().parents[2]
MEMORY=ROOT/'.naya'/'memory';EVENTS=MEMORY/'events';POLICY=MEMORY/'CONTINUITY-ENFORCEMENT-POLICY.json';REPORT=MEMORY/'CONTINUITY-VALIDATION-REPORT.json';RECEIPT=MEMORY/'CONTINUITY-GATE-RECEIPT.json'
EVENT_RE=re.compile(r'^SE-[0-9]{8}-[0-9]{6}-[a-z0-9-]+$')
def parse_time(v):
    if v.endswith('Z'):v=v[:-1]+'+00:00'
    d=datetime.fromisoformat(v)
    if d.tzinfo is None:raise ValueError('timestamp must include timezone')
    return d.astimezone(timezone.utc)
def load_policy():return json.loads(POLICY.read_text(encoding='utf-8'))
def event_files():return sorted(EVENTS.rglob('SE-*.json')) if EVENTS.exists() else []
def load_event(p):
    try:return json.loads(p.read_text(encoding='utf-8')),None
    except Exception as e:return None,str(e)
def is_meaningful_execution(e,p):
    if parse_time(e.get('effective_at',e.get('created_at','')))<parse_time(p['effective_at']):return False
    if e.get('continuity_required') is True:return True
    t=str(e.get('event_type',e.get('type',''))).lower()
    if t in {str(x).lower() for x in p.get('meaningful_event_types',[])}:return True
    if any(x in str(e.get('event_id','')).lower() for x in p.get('event_id_markers',[])):return True
    return bool({str(x).lower() for x in e.get('tags',[]) or []}&{str(x).lower() for x in p.get('meaningful_tags',[])})
def has_handoff(e,p):
    c=e.get('continuity',{}) or {};v=e.get('verification',{}) or {}
    if any(c.get(k) for k in ('handoff_url','handoff_path','ai_to_ai_handoff')) or v.get('handoff_url') or v.get('handoff_path'):return True
    for root in p.get('handoff_roots',['.naya/handoffs']):
        base=ROOT/root
        if base.exists() and any(e.get('event_id','') in x.name for x in base.rglob('*')):return True
    return False
def has_structured_handoff(e,p):
    h=(e.get('continuity',{}) or {}).get('handoff') or e.get('handoff') or {}
    if not isinstance(h,dict):return False,['structured handoff must be an object']
    m=[x for x in p.get('structured_handoff_fields',[]) if not h.get(x)]
    return not m,m
def check_event(e,path,p):
    errors=[];eid=e.get('event_id','<missing>');c=e.get('continuity',{}) or {};state=str(c.get('execution_state','COMPLETED')).upper();r=e.get('representations') or {};n=r.get('naya') if isinstance(r,dict) else None;h=(r.get('shawn') or r.get('human')) if isinstance(r,dict) else None;v=e.get('verification') or {};receipt=e.get('receipt') or {};delivery=e.get('delivery') or {}
    if state not in {'IN_PROGRESS','COMPLETED'}:errors.append(f'{eid}: invalid continuity.execution_state={state}')
    if not n or not h:errors.append(f'{eid}: missing paired Naya + Shawn/Human representations')
    if state=='COMPLETED' and v.get('status')!='VERIFIED':errors.append(f'{eid}: completed continuity requires verification.status=VERIFIED')
    if state=='IN_PROGRESS' and v.get('status') not in {None,'PENDING'}:errors.append(f'{eid}: in-progress continuity must remain PENDING until verified')
    if not(receipt.get('receipt_id') or v.get('receipt') or v.get('receipt_url')):errors.append(f'{eid}: continuity requires a durable receipt reference')
    if not(delivery.get('state') or v.get('feed_status')):errors.append(f'{eid}: continuity requires explicit delivery state')
    if not has_handoff(e,p):errors.append(f'{eid}: continuity requires an AI-to-AI handoff reference/artifact')
    if parse_time(e.get('effective_at',e.get('created_at','')))>=parse_time(p.get('structured_handoff_effective_at',p['effective_at'])):
        ok,m=has_structured_handoff(e,p)
        if not ok:errors.append(f'{eid}: structured Future-Naya handoff missing required fields: {", ".join(m)}')
    nex=e.get('next_execution');nex=nex.get('path') if isinstance(nex,dict) else nex;nex=nex or c.get('next_execution_path')
    if state=='COMPLETED':
        if not nex:errors.append(f'{eid}: completed execution requires a canonical NEXT-EXECUTION successor')
        else:errors.extend(f'{eid}: {x}' for x in validate_next_execution_reference(nex))
    if c.get('blocked') is True:
        if not nex:errors.append(f'{eid}: blocked execution requires a canonical NEXT-EXECUTION continuation path')
        else:errors.extend(f'{eid}: {x}' for x in validate_next_execution_reference(nex))
    lessons=[];actions=[]
    for rep in (n,h):
        if isinstance(rep,dict):lessons+=rep.get('lessons',[]) or rep.get('learning',[]) or rep.get('what_we_learned',[]);actions+=rep.get('next_best_actions',[]) or []
    if not lessons and not c.get('learning_status'):errors.append(f'{eid}: continuity requires learning or explicit learning_status')
    if not actions and not c.get('next_action_status'):errors.append(f'{eid}: continuity requires a next-action record')
    if not EVENT_RE.match(str(eid)):errors.append(f'{path}: invalid event_id')
    return errors
def validate():
    p=load_policy();checked=0;errors=[]
    for path in event_files():
        e,pe=load_event(path)
        if pe:errors.append(f'{path}: JSON parse error: {pe}');continue
        if not is_meaningful_execution(e,p):continue
        checked+=1;errors+=check_event(e,path,p)
    report={'schema_version':3,'status':'GREEN' if not errors else 'RED','meaningful_execution_events_checked':checked,'error_count':len(errors),'errors':errors,'checks':['paired_naya_human_representation','verification_state_by_execution_state','durable_receipt','delivery_state','ai_to_ai_handoff','structured_future_naya_handoff','canonical_next_execution_gate','blocked_continuation_gate','independent_consumability','actionable_execution_instructions','success_criteria','verification_requirements','learning','next_action']}
    REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');return (0 if not errors else 1),report
def emit_receipt():
    code,report=validate();r={'schema_version':1,'receipt_type':'superbrain-continuity-gate','status':'VERIFIED' if code==0 else 'FAILED','created_at':datetime.now(timezone.utc).isoformat(),'commit_sha':os.environ.get('GITHUB_SHA'),'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'workflow_job':os.environ.get('GITHUB_JOB'),'repository':os.environ.get('GITHUB_REPOSITORY'),'report':report,'evidence':{'validation_report':str(REPORT.relative_to(ROOT))}};RECEIPT.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(r,indent=2,ensure_ascii=False));return code
def self_test():
    p=load_policy();orphan={'event_id':'SE-20260825-999999-orphan','effective_at':p['effective_at'],'continuity':{'execution_state':'COMPLETED'},'ready_to_run_execution':'THIS IS NOT EXECUTABLE'};oe=check_event(orphan,Path('orphan.json'),p);assert any('canonical NEXT-EXECUTION' in x for x in oe)
    blocked={'event_id':'SE-20260825-999999-blocked','effective_at':p['effective_at'],'continuity':{'execution_state':'IN_PROGRESS','blocked':True,'next_action_status':'RECORDED'},'ready_to_run_execution':'THIS IS NOT EXECUTABLE'};be=check_event(blocked,Path('blocked.json'),p);assert any('blocked execution requires a canonical NEXT-EXECUTION continuation path' in x for x in be)
    good=ROOT/'.naya'/'handoffs'/'NEXT-EXECUTION-20260825-SUPERBRAIN-CONTRACT-ENFORCEMENT.md';assert validate_next_execution_reference(str(good.relative_to(ROOT)))==[]
    print('INVALID ORPHAN → RED');print('BLOCKED WITHOUT CONTINUATION → RED');print('CANONICAL SUCCESSOR → GREEN');print('PASS — continuity canonical successor and blocked-continuation behavioral gate GREEN');return 0
def main():
    ap=argparse.ArgumentParser();s=ap.add_subparsers(dest='command',required=True);s.add_parser('validate');s.add_parser('self-test');s.add_parser('receipt');a=ap.parse_args()
    if a.command=='self-test':return self_test()
    if a.command=='receipt':return emit_receipt()
    code,report=validate();print('PASS — execution continuity validation is GREEN' if code==0 else 'FAIL — execution continuity validation is RED');print(json.dumps(report,indent=2,ensure_ascii=False));return code
if __name__=='__main__':sys.exit(main())

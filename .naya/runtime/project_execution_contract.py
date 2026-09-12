#!/usr/bin/env python3
"""Authoritative machine validation for project and NEXT-EXECUTION contracts."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[2]
MEMORY=ROOT/'.naya'/'memory'; EVENTS=MEMORY/'events'; PROJECT=MEMORY/'projects'/'CURRENT-DAILY-PROJECT.json'; POLICY=MEMORY/'CONTINUITY-ENFORCEMENT-POLICY.json'; REPORT=MEMORY/'PROJECT-EXECUTION-CONTRACT-REPORT.json'
EVENT_RE=re.compile(r'^SE-[0-9]{8}-[0-9]{6}-[a-z0-9-]+$')
NEXT_RE=re.compile(r'^NEXT-EXECUTION-[0-9]{8}-.+\.(?:md|json)$')
NEXT_FIELDS=('project','north_star','current_state','completed_work','verified_evidence','unresolved_issues','constraints','current_objective','next_action','execution_instructions','success_criteria','verification_requirements')
CONVERSATION_MARKERS=(
    'as discussed','as we discussed','from this conversation','from our conversation','chat history','conversation history',
    'previous messages','earlier in this chat','above in the conversation','based on what shawn just said','ask shawn to provide',
    'wait for shawn to explain','use the originating conversation','reconstruct the conversation','continue from the chat',
    'continue from this conversation','refer to the conversation','refer to our chat','as you know from our chat'
)
ACTION_VERBS=re.compile(r'\b(run|execute|inspect|read|write|update|create|modify|implement|verify|validate|test|check|compare|record|commit|deploy|measure|review|remove|preserve|rerun|load|consume|confirm|open|generate|fix|diagnose)\b',re.I)


def load(path:Path)->dict[str,Any]: return json.loads(path.read_text(encoding='utf-8'))


def _nonempty(value: Any) -> bool:
    if value is None: return False
    if isinstance(value,str): return bool(value.strip())
    if isinstance(value,(list,tuple,set)): return bool(value) and all(_nonempty(v) for v in value)
    if isinstance(value,dict): return bool(value)
    return True


def _text(value: Any) -> str:
    if isinstance(value,str): return value.strip()
    if isinstance(value,(list,tuple)): return '\n'.join(str(v).strip() for v in value if str(v).strip())
    return json.dumps(value,ensure_ascii=False)


def _conversation_dependent(value: Any) -> bool:
    text=_text(value).lower()
    return any(marker in text for marker in CONVERSATION_MARKERS)


def _actionable(value: Any) -> bool:
    if not _nonempty(value): return False
    if isinstance(value,dict): return any(_actionable(v) for v in value.values())
    if isinstance(value,(list,tuple)): return any(_actionable(v) for v in value)
    return bool(ACTION_VERBS.search(str(value)))


def load_next_execution(path:Path)->dict[str,Any]:
    """Load a durable canonical NEXT-EXECUTION artifact from JSON or Markdown."""
    if not path.is_file(): raise FileNotFoundError(str(path))
    if path.suffix.lower()=='.json': return load(path)
    text=path.read_text(encoding='utf-8'); result:dict[str,Any]={}
    lines=text.splitlines()
    for raw in lines:
        line=raw.strip()
        if not line or line.startswith('#'): continue
        if ':' in line and not line.startswith('- '):
            key,value=line.split(':',1); key=key.strip().lower().replace(' ','_'); value=value.strip()
            if key in {'schema_version','status'} and value: result[key]=int(value) if key=='schema_version' and value.isdigit() else value
    for key in NEXT_FIELDS:
        title=key.replace('_',' ').title(); marker=f'## {title}'.lower(); start=None
        for i,line in enumerate(lines):
            if line.strip().lower()==marker: start=i+1; break
        if start is None: continue
        values=[]
        for line in lines[start:]:
            stripped=line.strip()
            if stripped.startswith('## '): break
            if stripped and not stripped.startswith('#'):
                values.append(stripped[2:].strip() if stripped.startswith('- ') else stripped)
        if values: result[key]=values if key in {'completed_work','verified_evidence','unresolved_issues','constraints','execution_instructions','success_criteria','verification_requirements'} else ' '.join(values)
    return result


def event_files(): return sorted(EVENTS.rglob('SE-*.json')) if EVENTS.exists() else []


def is_meaningful(event,policy):
    if event.get('continuity_required') is True:return True
    typ=str(event.get('event_type',event.get('type',''))).lower()
    if typ in {str(x).lower() for x in policy.get('meaningful_event_types',[])}:return True
    tags={str(x).lower() for x in (event.get('tags') or [])}; meaningful_tags={str(x).lower() for x in policy.get('meaningful_tags',[])}
    return bool(tags.intersection(meaningful_tags))


def validate_project(p):
    req=('project_id','project_name','date','goal','vision','mission','north_star','current_objective','success_criteria','constraints','current_state','next_execution_path')
    return [f'project state missing {k}' for k in req if not _nonempty(p.get(k))]


def validate_next_execution(n):
    """Validate the canonical successor object itself."""
    errors=[]
    if not isinstance(n,dict): return ['next execution canonical structure must be an object']
    for key in NEXT_FIELDS:
        if not _nonempty(n.get(key)): errors.append(f'next execution missing {key}')
    if not _nonempty(n.get('project')): errors.append('next execution requires project identity')
    if not _nonempty(n.get('current_state')): errors.append('next execution requires current-state identity')
    for field in ('project','current_state','current_objective','next_action','execution_instructions','success_criteria','verification_requirements'):
        if _conversation_dependent(n.get(field)): errors.append(f'next execution {field} is conversation-dependent')
    if not _actionable(n.get('execution_instructions')): errors.append('next execution execution_instructions are not actionable')
    if not _nonempty(n.get('success_criteria')): errors.append('next execution requires success criteria')
    if not _nonempty(n.get('verification_requirements')): errors.append('next execution requires verification requirements')
    if _conversation_dependent(n.get('success_criteria')) or _conversation_dependent(n.get('verification_requirements')): errors.append('next execution verification contract is conversation-dependent')
    return errors


def resolve_next_execution(value: Any)->tuple[dict[str,Any]|None,list[str]]:
    """Resolve and validate a canonical successor without conversational context."""
    if isinstance(value,dict):
        return value,validate_next_execution(value)
    if not isinstance(value,str) or not value.strip(): return None,['next execution continuation is missing']
    raw=value.strip(); candidate=Path(raw)
    if not NEXT_RE.match(candidate.name): return None,['next execution path is not a canonical NEXT-EXECUTION artifact']
    path=(ROOT/candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
    try: path.relative_to(ROOT.resolve())
    except ValueError: return None,['next execution artifact must reside inside repository']
    if not path.is_file(): return None,[f'next execution artifact missing: {raw}']
    try: artifact=load_next_execution(path)
    except Exception as exc: return None,[f'next execution artifact is not parseable: {exc}']
    errors=validate_next_execution(artifact)
    return artifact,errors


def validate_next_execution_reference(value: Any)->list[str]:
    _,errors=resolve_next_execution(value); return errors


def consume_next_execution(value: Any)->dict[str,Any]:
    """Return only canonical successor semantics, suitable for a fresh Naya."""
    artifact,errors=resolve_next_execution(value)
    if errors or artifact is None: raise ValueError('; '.join(errors) or 'invalid canonical successor')
    return {field:artifact[field] for field in NEXT_FIELDS}


def validate_event(event,project,policy):
    errors=[]; eid=str(event.get('event_id','<missing>'))
    if not EVENT_RE.match(eid):errors.append(f'{eid}: invalid event_id')
    ctx=event.get('project_context') or {}
    event_project_name=ctx.get('current_daily_project') or ctx.get('project_name') or event.get('project')
    if ctx.get('project_id')!=project.get('project_id') or event_project_name!=project.get('project_name'):
        errors.append(f'{eid}: meaningful execution must bind to CURRENT-DAILY-PROJECT ({project.get("project_name")})')
    if not ctx.get('current_objective'):errors.append(f'{eid}: missing project_context.current_objective')
    reps=event.get('representations') or {}; naya=reps.get('naya') if isinstance(reps,dict) else None; shawn=(reps.get('shawn') or reps.get('human')) if isinstance(reps,dict) else None
    naya_structured=isinstance(naya,dict); shawn_structured=isinstance(shawn,dict)
    if not naya or not shawn:errors.append(f'{eid}: paired representations are required')
    else:
        if naya_structured and naya.get('canonical_event_id')!=eid:errors.append(f'{eid}: Naya representation is not bound to canonical event')
        if shawn_structured and shawn.get('canonical_event_id')!=eid:errors.append(f'{eid}: Shawn/Human representation is not bound to canonical event')
        if naya_structured and shawn_structured and naya.get('id')==shawn.get('id'):errors.append(f'{eid}: Naya and Shawn/Human representation IDs must remain distinct')
    continuity=event.get('continuity') or {}; execution_state=str(continuity.get('execution_state','COMPLETED')).upper()
    if execution_state=='COMPLETED':
        nex=event.get('next_execution')
        if nex is None: nex=continuity.get('next_execution_path')
        if nex is None:
            errors.append(f'{eid}: completed execution requires a canonical NEXT-EXECUTION successor')
        elif isinstance(nex,dict):
            path=nex.get('path')
            if not isinstance(path,str) or not path.strip(): errors.append(f'{eid}: completed execution requires a durable NEXT-EXECUTION artifact path; embedded successor objects are not sufficient')
            else: errors.extend([f'{eid}: {x}' for x in validate_next_execution_reference(path)])
        else:
            errors.extend([f'{eid}: {x}' for x in validate_next_execution_reference(nex)])
    learning=event.get('learning') or {}; lessons=[]
    for rep in (naya,shawn):
        if isinstance(rep,dict):lessons += rep.get('lessons',[]) or rep.get('learning',[]) or rep.get('what_we_learned',[]) or []
    if not lessons and not learning.get('status') and not continuity.get('learning_status'):errors.append(f'{eid}: meaningful execution requires learning capture or explicit learning status')
    return errors


def validate():
    errors=validate_project(load(PROJECT)) if PROJECT.exists() else ['missing CURRENT-DAILY-PROJECT.json']; project=load(PROJECT) if PROJECT.exists() else {}; policy=load(POLICY); checked=0
    for path in event_files():
        try:event=load(path)
        except Exception as exc: errors.append(f'{path}: JSON parse error: {exc}'); continue
        if not is_meaningful(event,policy):continue
        if str(event.get('effective_at',''))<str(policy.get('effective_at','')):continue
        checked+=1; errors.extend([f'{path}: {x}' for x in validate_event(event,project,policy)])
    report={'schema_version':2,'status':'GREEN' if not errors else 'RED','meaningful_events_checked':checked,'error_count':len(errors),'errors':errors,'checks':['current_daily_project','project_event_binding','paired_representation_identity','canonical_next_execution_exists','canonical_next_execution_parseable','canonical_next_execution_semantics','independent_consumability','actionable_execution_instructions','success_criteria','verification_requirements','learning_capture']}
    REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return (0 if not errors else 1),report


def self_test():
    valid={field:('test action: run validation' if field=='execution_instructions' else ['test'] if field in {'completed_work','verified_evidence','unresolved_issues','constraints','success_criteria','verification_requirements'} else 'test') for field in NEXT_FIELDS}
    assert validate_next_execution(valid)==[]
    incomplete=dict(valid); incomplete.pop('success_criteria'); assert any('missing success_criteria' in x for x in validate_next_execution(incomplete))
    dependent=dict(valid); dependent['execution_instructions']='Continue from this conversation'; assert any('conversation-dependent' in x for x in validate_next_execution(dependent))
    assert any('canonical NEXT-EXECUTION' in x for x in validate_next_execution_reference('arbitrary prose'))
    assert any('missing' in x for x in validate_next_execution_reference(None))
    assert any('artifact missing' in x for x in validate_next_execution_reference('.naya/handoffs/NEXT-EXECUTION-20990101-MISSING.md'))
    assert any('not parseable' in x or 'missing' in x for x in validate_next_execution_reference('.naya/handoffs/NEXT-EXECUTION-20990101-MALFORMED.md'))
    orphan={'event_id':'SE-20260825-999999-orphan','continuity':{'execution_state':'COMPLETED'},'ready_to_run_execution':'THIS IS NOT EXECUTABLE'}
    orphan_errors=validate_event(orphan,{'project_id':'x','project_name':'x'},{})
    assert any('canonical NEXT-EXECUTION' in x for x in orphan_errors)
    embedded={'event_id':'SE-20260825-999999-embedded','project_context':{'project_id':'x','current_daily_project':'x','current_objective':'test'},'representations':{'naya':{'id':'n','canonical_event_id':'SE-20260825-999999-embedded'},'shawn':{'id':'s','canonical_event_id':'SE-20260825-999999-embedded'}},'verification':{'status':'VERIFIED','receipt':'r'},'receipt':{'receipt_id':'r'},'delivery':{'state':'VERIFIED'},'continuity':{'execution_state':'COMPLETED','handoff':{'mission':'x'},'learning_status':'LEARNED'},'next_execution':valid}
    assert any('durable NEXT-EXECUTION artifact path' in x for x in validate_event(embedded,{'project_id':'x','project_name':'x'},{'structured_handoff_fields':[]}))
    existing=ROOT/'.naya'/'handoffs'/'NEXT-EXECUTION-20260825-SUPERBRAIN-CONTRACT-ENFORCEMENT.md'
    artifact,errors=resolve_next_execution(str(existing.relative_to(ROOT))); assert not errors and artifact
    consumed=consume_next_execution(str(existing.relative_to(ROOT))); assert tuple(consumed)==NEXT_FIELDS and all(_nonempty(consumed[k]) for k in NEXT_FIELDS)
    print('ARBITRARY CONTINUATION → RED')
    print('MISSING CONTINUATION → RED')
    print('INVALID ARTIFACT → RED')
    print('CONVERSATION-DEPENDENT CONTINUATION → RED')
    print('INCOMPLETE SUCCESSOR → RED')
    print('INVALID ORPHAN → RED')
    print('CANONICAL SUCCESSOR → GREEN')
    print('INDEPENDENT CONSUMPTION → GREEN (12/12 semantic fields)')
    print('PASS — canonical NEXT-EXECUTION RED/GREEN behavioral and independent-consumption tests GREEN'); return 0


def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command',required=True); sub.add_parser('self-test'); sub.add_parser('validate'); args=ap.parse_args()
    if args.command=='self-test':return self_test()
    code,report=validate(); print('PASS — project/execution contracts are GREEN' if code==0 else 'FAIL — project/execution contracts are RED'); print(json.dumps(report,indent=2,ensure_ascii=False)); return code

if __name__=='__main__':raise SystemExit(main())

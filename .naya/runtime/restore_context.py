#!/usr/bin/env python3
"""Deterministic NayaPOWER Superbrain restore runtime.

The control-plane STATE/BLOCK/MAP/PROOF surfaces are the canonical operational
truth. Legacy memory state remains a compatibility/history projection.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[2]; NAYA=ROOT/'.naya'; MEMORY=NAYA/'memory'
CONTROL_STATE_PATH=NAYA/'control-plane/STATE.json'; CONTROL_MAP_PATH=NAYA/'control-plane/MAP.json'; CONTROL_BLOCK_PATH=NAYA/'control-plane/BLOCKS.json'; CONTROL_PROOF_PATH=NAYA/'control-plane/PROOF.json'; LEGACY_STATE_PATH=MEMORY/'STATE.json'
MANIFEST_PATH=NAYA/'naya-context-manifest.json'; BRIEFING_PATH=MEMORY/'NAYAPOWER-RUNTIME-BRIEFING.md'; FEED_PATH=NAYA/'INTELLIGENT-FEED.md'; PROJECT_PATH=NAYA/'projects'/'CURRENT-PROJECT.md'; START_PATH=ROOT/'SUPERBRAIN/AI-BOOT/START-HERE.md'; CHECKPOINT_DIR=NAYA/'checkpoints'; HANDOFF_DIR=NAYA/'handoffs'
sys.path.insert(0,str(MEMORY))
from memory_runtime import load_json, notes, retrieve, validate  # noqa: E402
ISO_Z_RE=re.compile(r'Z$'); GENERATED_STATUS_RE=re.compile(r'^\?\? \.naya/(?:memory|runtime)/__pycache__/')

def parse_time(value):
    if not value:return None
    dt=datetime.fromisoformat(ISO_Z_RE.sub('+00:00',value))
    if dt.tzinfo is None: raise ValueError('timestamp must include timezone')
    return dt.astimezone(timezone.utc)
def now(): return datetime.now(timezone.utc)
def run_git(*args):
    try:return subprocess.run(['git',*args],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
    except (OSError,subprocess.CalledProcessError):return None

def repository_reality(at=None):
    if at is None:
        head=run_git('rev-parse','HEAD'); branch=run_git('branch','--show-current'); status=run_git('status','--porcelain'); commit=run_git('show','-s','--format=%H|%cI|%s','HEAD')
    else:
        stamp=at.isoformat(); head=run_git('log','-1','--format=%H',f'--before={stamp}'); branch=run_git('branch','--show-current'); status=None; commit=run_git('show','-s','--format=%H|%cI|%s',head) if head else None
    parts=commit.split('|',2) if commit else []; raw_lines=status.splitlines() if status else []; effective=[line for line in raw_lines if not GENERATED_STATUS_RE.match(line)]
    return {'available':head is not None,'root':str(ROOT),'branch':branch,'head_sha':head,'clean':effective==[],'working_tree_status':status,'effective_working_tree_status':'\n'.join(effective),'generated_artifacts_ignored':[line for line in raw_lines if line not in effective],'commit':{'sha':parts[0] if len(parts)>0 else None,'timestamp':parts[1] if len(parts)>1 else None,'subject':parts[2] if len(parts)>2 else None},'historical':at is not None,'requested_at':at.isoformat() if at else None}
def load_state(): return load_json(CONTROL_STATE_PATH)
def load_manifest(): return load_json(MANIFEST_PATH)
def load_legacy_state():
    try:return load_json(LEGACY_STATE_PATH)
    except Exception:return {}
def read_text(path):
    try:return path.read_text(encoding='utf-8')
    except (OSError,UnicodeError):return ''
def current_head_declarations(text): return re.findall(r'(?im)^\s*(?:live|current|observed)\s+`?(?:main|head|git head)`?.{0,120}?\b([0-9a-f]{40})\b',text)
def orientation_projection(path,actual_head):
    body=read_text(path); declarations=current_head_declarations(body); return {'path':str(path.relative_to(ROOT)),'available':bool(body),'current_head_declaration_count':len(declarations),'declared_current_heads':declarations[:20],'matches_observed_head':bool(actual_head and actual_head in declarations),'head_mismatch':bool(actual_head and declarations and actual_head not in declarations)}
def extract_section(text,heading):
    marker=f'## {heading}'
    if marker not in text:return None
    return text.split(marker,1)[1].split('\n## ',1)[0].strip()
def latest_handoff():
    if not HANDOFF_DIR.exists():return None
    files=[p for p in HANDOFF_DIR.rglob('*') if p.is_file() and p.suffix.lower() in {'.md','.json'}]
    if not files:return None
    ranked=[]
    for path in files:
        rel=path.relative_to(ROOT).as_posix(); committed=run_git('log','-1','--format=%cI','--',rel)
        if committed:ranked.append((committed,rel,path))
    path=max(ranked,key=lambda x:(x[0],x[1]))[2] if ranked else max(files,key=lambda p:(p.stat().st_mtime_ns,p.as_posix()))
    return {'path':str(path.relative_to(ROOT)),'content':read_text(path)}
def note_is_visible(note,at):
    status=note.get('status')
    if status=='SUPERSEDED' and note.get('superseded_at'):return False if at is None else parse_time(note['superseded_at'])>at
    if status=='STALE' and at is None:return False
    if at is None:return status not in {'SUPERSEDED','STALE'}
    effective=parse_time(note.get('effective_at')); return not (effective and effective>at) and not (note.get('superseded_at') and parse_time(note['superseded_at'])<=at)
def memory_snapshot(query,at,limit):
    visible=[note for _,note in notes() if '__parse_error__' not in note and note_is_visible(note,at)]
    if query:
        ranked=[(score,n) for score,n in retrieve(query,max(limit*3,10)) if n in visible]; ranked.sort(key=lambda x:(-x[0],x[1].get('effective_at',''),x[1].get('id',''))); selected=[n for _,n in ranked[:limit]]
    else:selected=sorted(visible,key=lambda n:(n.get('effective_at',''),n.get('id','')),reverse=True)[:limit]
    counts={}
    for n in visible:counts[n.get('status','UNKNOWN')]=counts.get(n.get('status','UNKNOWN'),0)+1
    return {'count_visible':len(visible),'counts_by_status':counts,'conflicts':[n.get('id') for n in visible if n.get('status')=='CONFLICTED'],'selected':selected}
def stale_memory():
    out=[]
    for path,note in notes():
        if '__parse_error__' in note:out.append({'path':str(path),'reason':'parse_error'})
        elif note.get('status') in {'STALE','CONFLICTED','SUPERSEDED'}:out.append({'id':note.get('id'),'title':note.get('title'),'status':note.get('status'),'path':str(path)})
    return out
def proof_target(project_text,state):
    section=extract_section(project_text,'NEXT EXECUTION')
    return section if section else (state.get('single_next_action') if isinstance(state.get('single_next_action'),str) else None)
def orientation_snapshot(repo,state):
    actual=repo.get('head_sha'); projections=[orientation_projection(p,actual) for p in (BRIEFING_PATH,FEED_PATH,PROJECT_PATH,START_PATH)]; mismatches=[p['path'] for p in projections if p['head_mismatch']]; contradictions=[]
    for label,path in [('Runtime Briefing',BRIEFING_PATH),('Intelligent Feed',FEED_PATH),('CURRENT-PROJECT',PROJECT_PATH),('START-HERE',START_PATH)]:
        if not read_text(path):contradictions.append(f'missing {label}')
    if actual and mismatches:contradictions.append('current-head projection mismatch')
    next_actions=[]
    for label,body in [('control-plane',json.dumps(state,ensure_ascii=False)),('briefing',read_text(BRIEFING_PATH)),('feed',read_text(FEED_PATH)),('project',read_text(PROJECT_PATH))]:
        section=extract_section(body,'NEXT ACTION') or extract_section(body,'NEXT EXECUTION')
        if section:next_actions.append({'source':label,'text':section})
    if state.get('single_next_action'):next_actions.insert(0,{'source':'control-plane STATE','text':state['single_next_action']})
    return {'canonical_identity':'SoulSchoolAcademy/NayaPOWER','observed_head':actual,'state_declared_head':state.get('current_head',{}).get('source'),'projections':projections,'mismatches':sorted(set(mismatches)),'contradictions':contradictions,'next_actions':next_actions,'latest_handoff':latest_handoff()}
def build_restore(query='',at=None,limit=10):
    target=parse_time(at); state=load_state(); legacy=load_legacy_state(); manifest=load_manifest(); structural_errors=validate(); repo=repository_reality(target); orientation=orientation_snapshot(repo,state) if not target else {'historical':True}; project_text=read_text(PROJECT_PATH); memory=memory_snapshot(query,target,limit); reconciliation_required=bool(orientation.get('contradictions') or orientation.get('mismatches')) if not target else False; status='RECONCILIATION_REQUIRED' if reconciliation_required else ('VERIFIED' if not structural_errors and repo['available'] else 'UNKNOWN'); block=state.get('current_block'); next_action=state.get('single_next_action'); unknown=state.get('unknown',[])
    return {'schema':'naya-power-restore-context/v4','status':status,'generated_at':now().isoformat(),'mode':'RESTORE-TIME' if target else 'RESTORE-STANDARD','requested_at':target.isoformat() if target else None,'authority':manifest.get('authority_rules',{}),'current_state':state,'legacy_state_projection':legacy,'repository_reality':repo,'orientation':orientation,'memory':memory,'stale_or_superseded':stale_memory(),'validation':{'passed':not structural_errors,'errors':structural_errors},'mission':state.get('mission'),'north_star':state.get('north_star'),'protected':state.get('protected',[]),'known':state.get('verified_evidence',{}).get('known',[]),'unknown':unknown,'what_changed':state.get('verified_evidence',{}).get('known',[]),'what_is_unfinished':unknown,'current_project':{'active_block':block,'status':state.get('current_block_status'),'priority':state.get('priority'),'target_state':state.get('bottleneck')},'active_block':block,'next_best_action':next_action,'proof_target':proof_target(project_text,state),'latest_handoff':orientation.get('latest_handoff'),'reconciliation':{'required':reconciliation_required,'reasons':orientation.get('contradictions',[])+orientation.get('mismatches',[])},'operational_state_authority':str(CONTROL_STATE_PATH.relative_to(ROOT)),'active_block_authority':str(CONTROL_BLOCK_PATH.relative_to(ROOT)),'proof_authority':str(CONTROL_PROOF_PATH.relative_to(ROOT))}
def canonical_json(data):return json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def write_artifact(directory,prefix,payload):
    directory.mkdir(parents=True,exist_ok=True); path=directory/f'{prefix}-{now().strftime("%Y%m%dT%H%M%SZ")}.json'; path.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return path
def checkpoint(restore):
    payload={'schema':'naya-power-checkpoint/v3','created_at':now().isoformat(),'restore_status':restore['status'],'repository_reality':restore['repository_reality'],'orientation':restore['orientation'],'mission':restore['mission'],'current_state':restore['current_state'],'memory_summary':{'count_visible':restore['memory']['count_visible'],'counts_by_status':restore['memory']['counts_by_status'],'conflicts':restore['memory']['conflicts']},'protected':restore['protected'],'unknown':restore['unknown'],'next_best_action':restore['next_best_action'],'proof_target':restore['proof_target'],'reconciliation':restore['reconciliation'],'integrity_sha256':hashlib.sha256(canonical_json(restore).encode()).hexdigest()}; path=write_artifact(CHECKPOINT_DIR,'checkpoint',payload); return {'path':str(path.relative_to(ROOT)),'checkpoint':payload}
def handoff(restore):
    payload={'schema':'naya-power-handoff/v4','created_at':now().isoformat(),'mission':restore['mission'],'north_star':restore['north_star'],'current_state':restore['current_state'],'active_block':restore['active_block'],'what_changed':restore['what_changed'],'verified':restore['status']=='VERIFIED','unknown':restore['unknown'],'protected_elements':restore['protected'],'repository':restore['repository_reality'],'orientation':restore['orientation'],'memory_conflicts':restore['memory']['conflicts'],'next_best_action':restore['next_best_action'],'proof_target':restore['proof_target'],'reconciliation':restore['reconciliation'],'operational_state_authority':restore['operational_state_authority']}; path=write_artifact(HANDOFF_DIR,'handoff',payload); return {'path':str(path.relative_to(ROOT)),'handoff':payload}
def main():
    ap=argparse.ArgumentParser(description='NayaPOWER Superbrain Restore Context runtime'); sub=ap.add_subparsers(dest='command',required=True); r=sub.add_parser('restore'); r.add_argument('query',nargs='?',default=''); r.add_argument('--at'); r.add_argument('--limit',type=int,default=10); r.add_argument('--pretty',action='store_true'); c=sub.add_parser('checkpoint'); c.add_argument('query',nargs='?',default=''); c.add_argument('--at'); h=sub.add_parser('handoff'); h.add_argument('query',nargs='?',default=''); h.add_argument('--at'); args=ap.parse_args(); result=build_restore(args.query,args.at,getattr(args,'limit',10))
    if args.command=='restore': print(json.dumps(result,indent=2 if args.pretty else None,ensure_ascii=False)); return 0 if result['status']=='VERIFIED' else 2
    artifact=checkpoint(result) if args.command=='checkpoint' else handoff(result); print(json.dumps(artifact,indent=2,ensure_ascii=False)); return 0 if result['status']=='VERIFIED' else 2
if __name__=='__main__': raise SystemExit(main())

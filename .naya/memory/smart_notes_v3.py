#!/usr/bin/env python3
"""Naya Power Smart Brain v3."""
from __future__ import annotations
import argparse,json,math,re
from collections import Counter
from datetime import datetime,timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from permission_scope import AuthorizationRequest,Principal,authorize,filter_authorized
ROOT=Path(__file__).resolve().parents[2]; MEMORY=ROOT/'.naya'/'memory'; EVENTS=MEMORY/'events'; INDEX=EVENTS/'INDEX.json'; VALIDATION_REPORT=MEMORY/'VALIDATION-REPORT.json'
EVENT_RE=re.compile(r'^SE-[0-9]{8}-(?:[0-9]{6}-)?[A-Za-z0-9-]+$'); NOTE_RE=re.compile(r'^SN-[0-9]{8}-[0-9]{6}-.+$'); VALID_STATUS={'ACTIVE','CANONICAL','HISTORICAL','SUPERSEDED','CONFLICTED','STALE'}
QUERY_EXPANSIONS={'decision':{'decision','decided','choice','architecture','direction'},'decisions':{'decision','decided','choice','architecture','direction'},'superbrain':{'superbrain','smart','brain','memory','continuity'},'memory':{'memory','canonical','event','notes','continuity'},'learning':{'learning','lesson','wisdom','cis','intelligence'},'lesson':{'learning','lesson','wisdom','cis'},'lessons':{'learning','lesson','wisdom','cis'},'search':{'search','retrieval','query','ranking'},'retrieve':{'search','retrieval','query','ranking'},'retrieval':{'search','retrieval','query','ranking'},'project':{'project','objective','mission','goal'},'next':{'next','action','execution','handoff'},'execution':{'execution','action','handoff','verification'},'verify':{'verify','verification','evidence','receipt','green'},'verification':{'verify','verification','evidence','receipt','green'},'receipt':{'receipt','evidence','verification','artifact'},'cis':{'cis','learning','intelligence','daily','compounding'}}
def parse_time(v):
    if v.endswith('Z'):v=v[:-1]+'+00:00'
    d=datetime.fromisoformat(v)
    if d.tzinfo is None:d=d.replace(tzinfo=ZoneInfo('America/Vancouver'))
    return d
def tokens(t):return re.findall(r'[a-z0-9]+',str(t).lower())
def event_files():return sorted(EVENTS.rglob('SE-*.json')) if EVENTS.exists() else []
def load_events():
    out=[]
    for p in event_files():
        try:out.append((p,json.loads(p.read_text(encoding='utf-8'))))
        except Exception as exc:out.append((p,{'__parse_error__':str(exc)}))
    return out
def reps(e):
    r=e.get('representations',{})
    if isinstance(r,dict):return [v if isinstance(v,dict) else {'representation':k,'content':str(v)} for k,v in r.items()]
    if isinstance(r,list):return [v if isinstance(v,dict) else {'content':str(v)} for v in r]
    return []
def all_text(e):
    p=[e.get('event_id',''),e.get('title',''),e.get('subject',''),e.get('project',''),e.get('event_type',''),e.get('type',''),e.get('summary','')]
    for k in ('tags','aliases','concepts'):p+=e.get(k,[]) or []
    for r in reps(e):p += [r.get('title',''),r.get('summary',''),r.get('content','')];p += r.get('lessons',[]) or r.get('what_we_learned',[]) or r.get('learning',[]) or [];p += r.get('next_best_actions',[]) or r.get('what_changed',[]) or [];p += r.get('aliases',[]) or []
    return ' '.join(map(str,p))
def relationship_map(e):
    r=e.get('relationships',{}) or {}
    if isinstance(r,dict):return r
    if isinstance(r,list):return {'related':r}
    return {}
def normalize_targets(v):
    if v is None:return []
    if isinstance(v,str):return [v]
    if isinstance(v,dict):
        t=v.get('event_id') or v.get('id') or v.get('target');return [t] if t else []
    if isinstance(v,list):
        o=[]
        for x in v:
            if isinstance(x,dict):
                t=x.get('event_id') or x.get('id') or x.get('target')
                if t:o.append(t)
            else:o.append(x)
        return o
    return [v]
def validate_event(e,p):
    er=[];parsed={}
    if not EVENT_RE.match(e.get('event_id','')):er.append(f'{p}: invalid event_id')
    for k in ('created_at','effective_at'):
        try:parsed[k]=parse_time(e[k])
        except Exception as exc:er.append(f'{p}: invalid {k}: {exc}')
    if e.get('status') not in VALID_STATUS:er.append(f'{p}: invalid status')
    if not reps(e):er.append(f'{p}: missing representations')
    if not e.get('source'):er.append(f'{p}: missing source')
    v=e.get('verification',{}) or {}
    if v.get('status')=='VERIFIED' and not v.get('canonical_url'):er.append(f'{p}: verified event missing canonical_url')
    dt=parsed.get('effective_at')
    if dt:
        raw=str(e.get('effective_at',''));b=e.get('time_bucket',{}) or {};h=b.get('hour') if len(raw)<=10 else f'{dt:%H}'
        if h is None:
            try:h=Path(p).parent.name
            except Exception:h=f'{dt:%H}'
        expected=f'{dt:%Y/%m/%d}/{int(h):02d}/{e["event_id"]}.json'
        try:rel=str(p.relative_to(EVENTS))
        except ValueError:rel=str(p)
        if rel!=expected:er.append(f'{p}: physical time bucket mismatch; expected {expected}')
    for r in reps(e):
        if r.get('id') and not NOTE_RE.match(r['id']):er.append(f'{p}: invalid representation id {r["id"]}')
    return er
def validate():
    er=[];ids={};loaded=load_events()
    for p,e in loaded:
        if e.get('__parse_error__'):er.append(f'{p}: {e["__parse_error__"]}');continue
        er+=validate_event(e,p);eid=e.get('event_id')
        if eid in ids:er.append(f'duplicate event_id: {eid}')
        ids[eid]=str(p)
    for _,e in loaded:
        if e.get('__parse_error__'):continue
        rel=relationship_map(e)
        for k in ('related','depends_on','supersedes','superseded_by','source_events'):
            for t in normalize_targets(rel.get(k,[])):
                if t and t not in ids and not str(t).startswith('EXT:'):er.append(f'{e["event_id"]}: unresolved {k}: {t}')
    if not INDEX.exists():er.append('missing events/INDEX.json')
    else:
        try:
            idx=json.loads(INDEX.read_text(encoding='utf-8'));indexed={x.get('event_id') if isinstance(x,dict) else x for x in idx.get('events',[])}
            if indexed!=set(ids):er.append(f'INDEX mismatch: index={len(indexed)} canonical={len(ids)}')
        except Exception as exc:er.append(f'INDEX invalid: {exc}')
    VALIDATION_REPORT.write_text(json.dumps({'schema_version':1,'checked_at':'DERIVED','status':'GREEN' if not er else 'RED','error_count':len(er),'errors':er,'canonical_event_count':len(ids)},indent=2,ensure_ascii=False)+'\n',encoding='utf-8');return er
def build_index():
    rows=[]
    for p,e in load_events():
        if e.get('__parse_error__'):continue
        rows.append({'event_id':e['event_id'],'path':str(p.relative_to(EVENTS)),'subject':e.get('subject',''),'type':e.get('type') or e.get('event_type',''),'tags':e.get('tags',[]) or []})
    rows.sort(key=lambda x:(x['path'],x['event_id']));d={'version':'3.0.0','status':'CANONICAL','organization':'YEAR/MONTH/DAY/HOUR/EVENT','event_count':len(rows),'events':rows};INDEX.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');return d
def expanded_tokens(q):
    b=tokens(q);o=list(b)
    for t in b:o.extend(sorted(QUERY_EXPANSIONS.get(t,set())))
    return o
def corpus(events):
    docs=[];df=Counter();lens=[]
    for e in events:
        c=Counter(tokens(all_text(e)));docs.append(c);df.update(c.keys());lens.append(sum(c.values()))
    n=max(1,len(docs));avg=sum(lens)/len(lens) if lens else 1.0;idf={t:math.log((n+1)/(d+1))+1 for t,d in df.items()};return docs,idf,avg
def cosine(q,d,idf):
    if not q or not d:return 0.0
    qc=Counter(q);qv={t:(1+math.log(c))*idf.get(t,1) for t,c in qc.items()};dv={t:(1+math.log(c))*idf.get(t,0) for t,c in d.items()};dot=sum(qv.get(t,0)*dv.get(t,0) for t in qv);qn=math.sqrt(sum(x*x for x in qv.values()));dn=math.sqrt(sum(x*x for x in dv.values()));return dot/(qn*dn) if qn and dn else 0.0
def bm25(q,d,idf,avg,k1=1.2,b=0.75):
    if not q or not d:return 0.0
    dl=sum(d.values());s=0.0
    for term,qtf in Counter(q).items():
        tf=d.get(term,0)
        if tf:s+=idf.get(term,1.0)*(tf*(k1+1)/(tf+k1*(1-b+b*(dl/max(avg,1.0)))))
    return s
def lexical(q,e):
    qs=set(tokens(q));title=set(tokens(e.get('title','')));aliases=set(tokens(' '.join(e.get('aliases',[]) or [])));tags=set(tokens(' '.join(e.get('tags',[]) or [])));concepts=set(tokens(' '.join(e.get('concepts',[]) or [])));body=set(tokens(all_text(e)));return len(qs&title)*120+len(qs&aliases)*90+len(qs&tags)*70+len(qs&concepts)*65+len(qs&body)*18
def exact_match_bonus(q,e):
    q=q.strip().lower()
    if not q:return 0.0
    eid=str(e.get('event_id','')).lower();sub=str(e.get('subject','')).lower();title=str(e.get('title','')).lower()
    if q==eid:return 1200.0
    if q==sub or q==title:return 650.0
    if q in eid:return 450.0
    return 0.0
def authority_score(e):
    s=0.0;a=str(e.get('authority','')).lower()
    if a in {'repository-execution','canonical','human-decision'}:s+=35
    if a in {'derived','audit','generated'}:s-=20
    if (e.get('verification') or {}).get('status')=='VERIFIED':s+=35
    return s+{'ACTIVE':30,'CANONICAL':25,'HISTORICAL':0,'CONFLICTED':-20,'STALE':-40,'SUPERSEDED':-70}.get(e.get('status'),0)
def recency_score(e,latest):
    try:age=max(0,(latest-parse_time(e['effective_at'])).total_seconds()/86400)
    except Exception:return 0.0
    return 45.0*math.exp(-age/14.0)
def metadata_match(e,project=None,event_type=None,status=None,tag=None):
    if project and str(e.get('project','')).lower()!=project.lower():return False
    if event_type and str(e.get('event_type') or e.get('type','')).lower()!=event_type.lower():return False
    if status and str(e.get('status','')).lower()!=status.lower():return False
    if tag and tag.lower() not in {str(x).lower() for x in (e.get('tags') or [])}:return False
    return True
def authorization_request(principal_id=None,scope=None,project=None,grants=()):return AuthorizationRequest(Principal(principal_id or '',scope,project,frozenset(grants or ())),scope,project)
def authorized_events(loaded,principal_id=None,scope=None,project=None,grants=()):
    req=authorization_request(principal_id,scope,project,grants);events=[e for _,e in loaded if not e.get('__parse_error__')];ids={e.get('event_id') for e in filter_authorized(req,events)};return [(p,e) for p,e in loaded if not e.get('__parse_error__') and e.get('event_id') in ids and authorize(req,e)]
def authorized_relationship_targets(event,authorized_by_id):
    rel=relationship_map(event);ids=set()
    for k in ('related','depends_on','supersedes','superseded_by','source_events'):ids.update(normalize_targets(rel.get(k,[])))
    return [authorized_by_id[i] for i in ids if i in authorized_by_id]
def retrieve(query,limit=10,since=None,until=None,project=None,event_type=None,status=None,tag=None,principal_id=None,scope=None,access_project=None,grants=()):
    loaded=[(p,e) for p,e in load_events() if not e.get('__parse_error__')];authorized=authorized_events(loaded,principal_id,scope,access_project or project,grants);es=[e for _,e in authorized];docs,idf,avg=corpus(es);exp=expanded_tokens(query);latest=max((parse_time(e['effective_at']) for e in es),default=datetime.now().astimezone());ranked=[]
    for i,e in enumerate(es):
        dt=parse_time(e['effective_at'])
        if since and dt<since or until and dt>until:continue
        if not metadata_match(e,project,event_type,status,tag):continue
        rel=exact_match_bonus(query,e)+lexical(' '.join(exp),e)+bm25(exp,docs[i],idf,avg)*95+cosine(exp,docs[i],idf)*140
        if rel>0:ranked.append([rel+authority_score(e)+recency_score(e,latest),e])
    ranked.sort(key=lambda x:x[0],reverse=True);seed={e['event_id'] for _,e in ranked[:3]};byid={e['event_id']:e for _,e in authorized}
    for row in ranked:
        if {e['event_id'] for e in authorized_relationship_targets(row[1],byid)}&seed:row[0]+=35
    ranked.sort(key=lambda x:(-x[0],x[1]['effective_at'],x[1]['event_id']));return ranked[:limit]
def daily_report(day=None,tz_name='America/Vancouver',principal_id=None,scope=None,project=None,grants=()):
    z=ZoneInfo(tz_name);d=datetime.now(z).date()-timedelta(days=1) if day is None else datetime.fromisoformat(day).date();start=datetime.combine(d,datetime.min.time(),z);end=start+timedelta(days=1);sel=[e for _,e in authorized_events(load_events(),principal_id,scope,project,grants) if start<=parse_time(e['effective_at']).astimezone(z)<end];sel.sort(key=lambda x:x['effective_at']);less=[];changes=[];nexts=[]
    for e in sel:
        for r in reps(e):less+=r.get('lessons',[]) or r.get('what_we_learned',[]) or r.get('learning',[]) or [];changes+=r.get('what_changed',[]) or [];nexts+=r.get('next_best_actions',[]) or []
    u=lambda x:list(dict.fromkeys(x));return {'report_type':'DAILY_INTELLIGENCE_REPORT','period':d.isoformat(),'timezone':tz_name,'event_count':len(sel),'source_event_ids':[e['event_id'] for e in sel],'what_happened':[e.get('title') or e.get('subject') for e in sel],'what_we_learned':u(less),'what_changed':u(changes),'wins':[e['event_id'] for e in sel if e.get('event_type') in {'milestone','success'} or e.get('type')=='milestone'],'next_best_actions':u(nexts),'open_loops':[e['event_id'] for e in sel if e.get('status') in {'CONFLICTED','STALE'}],'verification_required':True,'feed_status':'AUTHORIZED_PENDING_INTEGRATION'}
def main():
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='cmd',required=True);sub.add_parser('validate');sub.add_parser('index');r=sub.add_parser('retrieve');r.add_argument('query');r.add_argument('--limit',type=int,default=10);r.add_argument('--project');r.add_argument('--event-type');r.add_argument('--status');r.add_argument('--tag');r.add_argument('--since');r.add_argument('--until');r.add_argument('--principal-id',required=True);r.add_argument('--scope',required=True);r.add_argument('--access-project',required=True);r.add_argument('--grant',action='append',default=[]);d=sub.add_parser('daily-report');d.add_argument('--day');d.add_argument('--timezone',default='America/Vancouver');d.add_argument('--principal-id',required=True);d.add_argument('--scope',required=True);d.add_argument('--project',required=True);d.add_argument('--grant',action='append',default=[]);a=ap.parse_args()
    if a.cmd=='validate':
        er=validate();print('PASS — Smart Brain v3 validation is GREEN' if not er else 'FAIL\n'+'\n'.join('- '+x for x in er));return 0 if not er else 1
    if a.cmd=='index':print(json.dumps(build_index(),indent=2,ensure_ascii=False));return 0
    if a.cmd=='retrieve':
        since=parse_time(a.since) if a.since else None;until=parse_time(a.until) if a.until else None
        for s,e in retrieve(a.query,a.limit,since,until,a.project,a.event_type,a.status,a.tag,a.principal_id,a.scope,a.access_project,a.grant):print(f'{s:8.2f} {e["event_id"]} | {e.get("title") or e.get("subject")} | {e.get("status")}')
        return 0
    print(json.dumps(daily_report(a.day,a.timezone,a.principal_id,a.scope,a.project,a.grant),indent=2,ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())

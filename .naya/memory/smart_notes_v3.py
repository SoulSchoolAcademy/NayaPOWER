#!/usr/bin/env python3
"""Naya Power Smart Brain v3.

Canonical source: chronological Note Events under .naya/memory/events.
The runtime deliberately tolerates the v2 event envelope while enforcing the
v3 retrieval and CIS model. Canonical event JSON remains the source of truth.
Derived indexes and validation diagnostics are reproducible artifacts.

Retrieval is intentionally dependency-free: authorization, exact matching,
BM25 lexical ranking, TF-IDF cosine similarity, metadata filtering, query
expansion, recency, authority/verification weighting, and relationship-aware
reranking. Authorization is a hard pre-ranking boundary: unauthorized events
are removed before corpus construction, ranking, relationship expansion, or
context delivery.
"""
from __future__ import annotations
import argparse, json, math, re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from permission_scope import AuthorizationRequest, Principal, authorize, filter_authorized

ROOT = Path(__file__).resolve().parents[2]
MEMORY = ROOT / '.naya' / 'memory'
EVENTS = MEMORY / 'events'
INDEX = EVENTS / 'INDEX.json'
VALIDATION_REPORT = MEMORY / 'VALIDATION-REPORT.json'
EVENT_RE = re.compile(r'^SE-[0-9]{8}-[0-9]{6}-[a-z0-9-]+$')
NOTE_RE = re.compile(r'^SN-[0-9]{8}-[0-9]{6}-.+$')
VALID_STATUS = {'ACTIVE','CANONICAL','HISTORICAL','SUPERSEDED','CONFLICTED','STALE'}
QUERY_EXPANSIONS = {
    'decision': {'decision', 'decided', 'choice', 'architecture', 'direction'},
    'decisions': {'decision', 'decided', 'choice', 'architecture', 'direction'},
    'superbrain': {'superbrain', 'smart', 'brain', 'memory', 'continuity'},
    'memory': {'memory', 'canonical', 'event', 'notes', 'continuity'},
    'learning': {'learning', 'lesson', 'wisdom', 'cis', 'intelligence'},
    'lesson': {'learning', 'lesson', 'wisdom', 'cis'},
    'lessons': {'learning', 'lesson', 'wisdom', 'cis'},
    'search': {'search', 'retrieval', 'query', 'ranking'},
    'retrieve': {'search', 'retrieval', 'query', 'ranking'},
    'retrieval': {'search', 'retrieval', 'query', 'ranking'},
    'project': {'project', 'objective', 'mission', 'goal'},
    'next': {'next', 'action', 'execution', 'handoff'},
    'execution': {'execution', 'action', 'handoff', 'verification'},
    'verify': {'verify', 'verification', 'evidence', 'receipt', 'green'},
    'verification': {'verify', 'verification', 'evidence', 'receipt', 'green'},
    'receipt': {'receipt', 'evidence', 'verification', 'artifact'},
    'cis': {'cis', 'learning', 'intelligence', 'daily', 'compounding'},
}


def parse_time(value):
    if value.endswith('Z'): value = value[:-1] + '+00:00'
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None: raise ValueError('timestamp must include timezone')
    return dt


def tokens(text): return re.findall(r'[a-z0-9]+', str(text).lower())


def event_files(): return sorted(EVENTS.rglob('SE-*.json')) if EVENTS.exists() else []


def load_events():
    out=[]
    for p in event_files():
        try: out.append((p,json.loads(p.read_text(encoding='utf-8'))))
        except Exception as exc: out.append((p,{'__parse_error__':str(exc)}))
    return out


def reps(e):
    r=e.get('representations',{})
    if isinstance(r,dict): return list(r.values())
    return r if isinstance(r,list) else []


def all_text(e):
    parts=[e.get('event_id',''),e.get('title',''),e.get('subject',''),e.get('project',''),e.get('event_type',''),e.get('type',''),e.get('summary','')]
    for k in ('tags','aliases','concepts'): parts += e.get(k,[]) or []
    for r in reps(e):
        parts += [r.get('title',''),r.get('summary',''),r.get('content','')]
        parts += r.get('lessons',[]) or r.get('what_we_learned',[]) or r.get('learning',[]) or []
        parts += r.get('next_best_actions',[]) or r.get('what_changed',[]) or []
        parts += r.get('aliases',[]) or []
    return ' '.join(map(str,parts))


def relationship_map(e):
    rel=e.get('relationships',{}) or {}
    if isinstance(rel,dict): return rel
    if isinstance(rel,list): return {'related':rel}
    return {}


def normalize_targets(value):
    if value is None: return []
    if isinstance(value,str): return [value]
    if isinstance(value,list): return value
    return [value]


def validate_event(e,p):
    errors=[]; parsed={}
    if not EVENT_RE.match(e.get('event_id','')): errors.append(f'{p}: invalid event_id')
    for k in ('created_at','effective_at'):
        try: parsed[k]=parse_time(e[k])
        except Exception as exc: errors.append(f'{p}: invalid {k}: {exc}')
    if e.get('status') not in VALID_STATUS: errors.append(f'{p}: invalid status')
    if not reps(e): errors.append(f'{p}: missing representations')
    if not e.get('source'): errors.append(f'{p}: missing source')
    v=e.get('verification',{}) or {}
    if v.get('status')=='VERIFIED' and not v.get('canonical_url'): errors.append(f'{p}: verified event missing canonical_url')
    dt=parsed.get('effective_at')
    if dt:
        expected=f'{dt:%Y/%m/%d/%H}/{e["event_id"]}.json'
        try: relative=str(p.relative_to(EVENTS))
        except ValueError: relative=str(p)
        if relative != expected: errors.append(f'{p}: physical time bucket mismatch; expected {expected}')
    for r in reps(e):
        if r.get('id') and not NOTE_RE.match(r['id']): errors.append(f'{p}: invalid representation id {r["id"]}')
    return errors


def validate():
    errors=[]; ids={}; loaded=load_events()
    for p,e in loaded:
        if e.get('__parse_error__'): errors.append(f'{p}: {e["__parse_error__"]}'); continue
        errors += validate_event(e,p); eid=e.get('event_id')
        if eid in ids: errors.append(f'duplicate event_id: {eid}')
        ids[eid]=str(p)
    for _,e in loaded:
        if e.get('__parse_error__'): continue
        rel=relationship_map(e)
        for key in ('related','depends_on','supersedes','superseded_by','source_events'):
            for target in normalize_targets(rel.get(key,[])):
                if target and target not in ids and not str(target).startswith('EXT:'): errors.append(f'{e["event_id"]}: unresolved {key}: {target}')
    if not INDEX.exists(): errors.append('missing events/INDEX.json')
    else:
        try:
            idx=json.loads(INDEX.read_text(encoding='utf-8')); indexed={x.get('event_id') if isinstance(x,dict) else x for x in idx.get('events',[])}
            if indexed != set(ids): errors.append(f'INDEX mismatch: index={len(indexed)} canonical={len(ids)}')
        except Exception as exc: errors.append(f'INDEX invalid: {exc}')
    report={'schema_version':1,'checked_at':'DERIVED','status':'GREEN' if not errors else 'RED','error_count':len(errors),'errors':errors,'canonical_event_count':len(ids)}
    VALIDATION_REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return errors


def build_index():
    rows=[]
    for p,e in load_events():
        if e.get('__parse_error__'): continue
        rows.append({'event_id':e['event_id'],'path':str(p.relative_to(EVENTS)),'subject':e.get('subject',''),'type':e.get('type') or e.get('event_type',''),'tags':e.get('tags',[]) or []})
    rows.sort(key=lambda x:(x['path'],x['event_id']))
    data={'version':'3.0.0','status':'CANONICAL','organization':'YEAR/MONTH/DAY/HOUR/EVENT','event_count':len(rows),'events':rows}
    INDEX.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return data


def expanded_tokens(query):
    base=tokens(query); expanded=list(base)
    for token in base: expanded.extend(sorted(QUERY_EXPANSIONS.get(token,set())))
    return expanded


def corpus(events):
    docs=[]; df=Counter(); lengths=[]
    for e in events:
        c=Counter(tokens(all_text(e))); docs.append(c); df.update(c.keys()); lengths.append(sum(c.values()))
    n=max(1,len(docs)); avg_len=(sum(lengths)/len(lengths)) if lengths else 1.0
    idf={t:math.log((n+1)/(d+1))+1 for t,d in df.items()}
    return docs,idf,avg_len


def cosine(q,doc,idf):
    if not q or not doc:return 0.0
    qc=Counter(q); qv={t:(1+math.log(c))*idf.get(t,1) for t,c in qc.items()}; dv={t:(1+math.log(c))*idf.get(t,0) for t,c in doc.items()}
    dot=sum(qv.get(t,0)*dv.get(t,0) for t in qv); qn=math.sqrt(sum(x*x for x in qv.values())); dn=math.sqrt(sum(x*x for x in dv.values()))
    return dot/(qn*dn) if qn and dn else 0.0


def bm25(q,doc,idf,avg_len,k1=1.2,b=0.75):
    if not q or not doc:return 0.0
    dl=sum(doc.values()); score=0.0; counts=Counter(q)
    for term,qtf in counts.items():
        tf=doc.get(term,0)
        if not tf: continue
        denom=tf+k1*(1-b+b*(dl/max(avg_len,1.0)))
        score += idf.get(term,1.0)*(tf*(k1+1)/denom)
    return score


def lexical(query,e):
    q=set(tokens(query)); title=set(tokens(e.get('title',''))); aliases=set(tokens(' '.join(e.get('aliases',[]) or []))); tags=set(tokens(' '.join(e.get('tags',[]) or []))); concepts=set(tokens(' '.join(e.get('concepts',[]) or []))); body=set(tokens(all_text(e)))
    return len(q&title)*120+len(q&aliases)*90+len(q&tags)*70+len(q&concepts)*65+len(q&body)*18


def exact_match_bonus(query,e):
    q=query.strip().lower()
    if not q:return 0.0
    eid=str(e.get('event_id','')).lower(); subject=str(e.get('subject','')).lower(); title=str(e.get('title','')).lower()
    if q==eid:return 1200.0
    if q==subject or q==title:return 650.0
    if q in eid:return 450.0
    return 0.0


def authority_score(e):
    score=0.0; authority=str(e.get('authority','')).lower()
    if authority in {'repository-execution','canonical','human-decision'}: score+=35
    if authority in {'derived','audit','generated'}: score-=20
    if (e.get('verification') or {}).get('status')=='VERIFIED': score+=35
    score += {'ACTIVE':30,'CANONICAL':25,'HISTORICAL':0,'CONFLICTED':-20,'STALE':-40,'SUPERSEDED':-70}.get(e.get('status'),0)
    return score


def recency_score(e,latest_time):
    try: age_days=max(0,(latest_time-parse_time(e['effective_at'])).total_seconds()/86400)
    except Exception:return 0.0
    return 45.0*math.exp(-age_days/14.0)


def metadata_match(e,project=None,event_type=None,status=None,tag=None):
    if project and str(e.get('project','')).lower()!=project.lower(): return False
    if event_type and str(e.get('event_type') or e.get('type','')).lower()!=event_type.lower(): return False
    if status and str(e.get('status','')).lower()!=status.lower(): return False
    if tag and tag.lower() not in {str(x).lower() for x in (e.get('tags') or [])}: return False
    return True


def authorization_request(principal_id=None, scope=None, project=None, grants=()):
    principal=Principal(principal_id=principal_id or '', scope=scope, project=project, grants=frozenset(grants or ()))
    return AuthorizationRequest(principal=principal, scope=scope, project=project)


def authorized_events(loaded, principal_id=None, scope=None, project=None, grants=()):
    """REQUEST -> IDENTITY -> SCOPE -> PERMISSION -> authorized events.

    This is the hard security boundary. Only the returned events may enter the
    corpus, candidate set, ranking, relationship expansion, or context output.
    """
    request=authorization_request(principal_id, scope, project, grants)
    events=[e for _,e in loaded if not e.get('__parse_error__')]
    allowed_ids={e.get('event_id') for e in filter_authorized(request, events)}
    return [(p,e) for p,e in loaded if not e.get('__parse_error__') and e.get('event_id') in allowed_ids and authorize(request,e)]


def authorized_relationship_targets(event, authorized_by_id):
    """Return only relationship targets that are already authorized objects."""
    rel=relationship_map(event); targets=set()
    for k in ('related','depends_on','supersedes','superseded_by','source_events'):
        targets.update(normalize_targets(rel.get(k,[])))
    return [authorized_by_id[target] for target in targets if target in authorized_by_id]


def retrieve(query,limit=10,since=None,until=None,project=None,event_type=None,status=None,tag=None,principal_id=None,scope=None,access_project=None,grants=()):
    loaded=[(p,e) for p,e in load_events() if not e.get('__parse_error__')]
    authorized_loaded=authorized_events(loaded, principal_id, scope, access_project or project, grants)
    es=[e for _,e in authorized_loaded]
    docs,idf,avg_len=corpus(es)
    expanded=expanded_tokens(query)
    latest=max((parse_time(e['effective_at']) for e in es),default=datetime.now().astimezone())
    ranked=[]
    for i,e in enumerate(es):
        dt=parse_time(e['effective_at'])
        if since and dt<since or until and dt>until: continue
        if not metadata_match(e,project,event_type,status,tag): continue
        bm=bm25(expanded,docs[i],idf,avg_len); tf=cosine(expanded,docs[i],idf); lx=lexical(' '.join(expanded),e); exact=exact_match_bonus(query,e)
        relevance=exact + lx + bm*95 + tf*140
        if relevance <= 0: continue
        score=relevance + authority_score(e) + recency_score(e,latest)
        ranked.append([score,e])
    ranked.sort(key=lambda x:x[0],reverse=True)
    seed={e['event_id'] for _,e in ranked[:3]}
    authorized_by_id={e['event_id']:e for _,e in authorized_loaded}
    for row in ranked:
        rel_targets=authorized_relationship_targets(row[1], authorized_by_id)
        if {e['event_id'] for e in rel_targets}&seed: row[0]+=35
    ranked.sort(key=lambda x:(-x[0],x[1]['effective_at'],x[1]['event_id']))
    return ranked[:limit]


def daily_report(day=None,tz_name='America/Vancouver',principal_id=None,scope=None,project=None,grants=()):
    zone=ZoneInfo(tz_name); local_day=datetime.now(zone).date()-timedelta(days=1) if day is None else datetime.fromisoformat(day).date(); start=datetime.combine(local_day,datetime.min.time(),zone); end=start+timedelta(days=1)
    loaded=[(p,e) for p,e in load_events() if not e.get('__parse_error__')]
    authorized_loaded=authorized_events(loaded, principal_id, scope, project, grants)
    selected=[]
    for _,e in authorized_loaded:
        dt=parse_time(e['effective_at']).astimezone(zone)
        if start<=dt<end:selected.append(e)
    selected.sort(key=lambda x:x['effective_at']); lessons=[]; changes=[]; nexts=[]
    for e in selected:
        for r in reps(e):
            lessons += r.get('lessons',[]) or r.get('what_we_learned',[]) or r.get('learning',[]) or []; changes += r.get('what_changed',[]) or []; nexts += r.get('next_best_actions',[]) or []
    uniq=lambda xs:list(dict.fromkeys(xs))
    return {'report_type':'DAILY_INTELLIGENCE_REPORT','period':local_day.isoformat(),'timezone':tz_name,'event_count':len(selected),'source_event_ids':[e['event_id'] for e in selected],'what_happened':[e.get('title') or e.get('subject') for e in selected],'what_we_learned':uniq(lessons),'what_changed':uniq(changes),'wins':[e['event_id'] for e in selected if e.get('event_type') in {'milestone','success'} or e.get('type')=='milestone'],'next_best_actions':uniq(nexts),'open_loops':[e['event_id'] for e in selected if e.get('status') in {'CONFLICTED','STALE'}],'verification_required':True,'feed_status':'AUTHORIZED_PENDING_INTEGRATION'}


def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True); sub.add_parser('validate'); sub.add_parser('index')
    r=sub.add_parser('retrieve'); r.add_argument('query'); r.add_argument('--limit',type=int,default=10); r.add_argument('--project'); r.add_argument('--event-type'); r.add_argument('--status'); r.add_argument('--tag'); r.add_argument('--since'); r.add_argument('--until'); r.add_argument('--principal-id',required=True); r.add_argument('--scope',required=True); r.add_argument('--access-project',required=True); r.add_argument('--grant',action='append',default=[])
    d=sub.add_parser('daily-report'); d.add_argument('--day'); d.add_argument('--timezone',default='America/Vancouver'); d.add_argument('--principal-id',required=True); d.add_argument('--scope',required=True); d.add_argument('--project',required=True); d.add_argument('--grant',action='append',default=[])
    a=ap.parse_args()
    if a.cmd=='validate':
        err=validate(); print('PASS — Smart Brain v3 validation is GREEN' if not err else 'FAIL\n'+'\n'.join('- '+x for x in err)); return 0 if not err else 1
    if a.cmd=='index': print(json.dumps(build_index(),indent=2,ensure_ascii=False)); return 0
    if a.cmd=='retrieve':
        since=parse_time(a.since) if a.since else None; until=parse_time(a.until) if a.until else None
        for s,e in retrieve(a.query,a.limit,since,until,a.project,a.event_type,a.status,a.tag,a.principal_id,a.scope,a.access_project,a.grant): print(f'{s:8.2f} {e["event_id"]} | {e.get("title") or e.get("subject")} | {e.get("status")}')
        return 0
    print(json.dumps(daily_report(a.day,a.timezone,a.principal_id,a.scope,a.project,a.grant),indent=2,ensure_ascii=False)); return 0

if __name__=='__main__': raise SystemExit(main())

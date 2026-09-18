#!/usr/bin/env python3
"""Canonical, idempotent Note Event creation primitives.

The chronological event store remains authoritative. This module adds a safe
write boundary without changing historical events. Replays resolve to the
existing event; conflicting payloads are rejected for explicit review.
Meaningful post-policy executions also pass the project/continuation contract
before they can be persisted.

IMPORTANT: INDEX.json is a derived artifact owned by the Smart Brain runtime.
This writer never invents a second index schema; it rebuilds the canonical
v3 index after a successful create/replay path.
"""
from __future__ import annotations
import hashlib, json, os, re
from pathlib import Path
from typing import Any
EVENT_RE=re.compile(r"^SE-[0-9]{8}-[0-9]{6}-[a-z0-9-]+$")
def canonical_json(value:Any)->str:return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(",",":"))
def content_fingerprint(event:dict[str,Any])->str:
    excluded={"event_id","created_at","receipt","delivery","verification"}; payload={k:v for k,v in event.items() if k not in excluded}; return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
def idempotency_key(event:dict[str,Any])->str:
    source=event.get("source") or {}; source_id=source.get("event_id") or source.get("id") if isinstance(source,dict) else None
    if source_id:return f"source:{source_id}"
    if event.get("idempotency_key"):return str(event["idempotency_key"])
    return f"content:{content_fingerprint(event)}"
def _candidate_path(events_root:Path,event_id:str,effective_at:str)->Path:
    if not EVENT_RE.match(event_id):raise ValueError(f"invalid event_id: {event_id}")
    from datetime import datetime
    dt=datetime.fromisoformat(effective_at.replace("Z","+00:00")); return events_root/f"{dt:%Y/%m/%d/%H}/{event_id}.json"
def _post_policy_meaningful(event:dict[str,Any])->bool:
    policy_path=Path(__file__).resolve().parents[1]/'memory'/'CONTINUITY-ENFORCEMENT-POLICY.json'
    if not policy_path.exists():return False
    policy=json.loads(policy_path.read_text(encoding='utf-8')); effective=str(event.get('effective_at',''))
    if not effective or effective < str(policy.get('effective_at','')):return False
    if event.get('continuity_required') is True:return True
    typ=str(event.get('event_type',event.get('type',''))).lower()
    if typ in {str(x).lower() for x in policy.get('meaningful_event_types',[])}:return True
    tags={str(x).lower() for x in (event.get('tags') or [])}; return bool(tags.intersection({str(x).lower() for x in policy.get('meaningful_tags',[])}))
def _enforce_project_contract(event:dict[str,Any],events_root:Path,index_path:Path)->None:
    if not _post_policy_meaningful(event):return
    from project_execution_contract import validate_event
    memory=Path(__file__).resolve().parents[1]/'memory'; project_path=memory/'projects'/'CURRENT-DAILY-PROJECT.json'; policy_path=memory/'CONTINUITY-ENFORCEMENT-POLICY.json'
    if not project_path.exists():raise ValueError('meaningful event requires CURRENT-DAILY-PROJECT.json')
    project=json.loads(project_path.read_text(encoding='utf-8')); policy=json.loads(policy_path.read_text(encoding='utf-8')); errors=validate_event(event,project,policy)
    if errors:raise ValueError('canonical event contract rejected: '+'; '.join(errors))
def _rebuild_canonical_index(events_root:Path,index_path:Path)->None:
    rows=[]
    for p in sorted(events_root.rglob('SE-*.json')):
        try:e=json.loads(p.read_text(encoding='utf-8'))
        except Exception:continue
        rows.append({'event_id':e['event_id'],'path':str(p.relative_to(events_root)),'subject':e.get('subject',''),'type':e.get('type') or e.get('event_type',''),'tags':e.get('tags',[]) or []})
    rows.sort(key=lambda x:(x['path'],x['event_id']))
    data={'version':'3.0.0','status':'CANONICAL','organization':'YEAR/MONTH/DAY/HOUR/EVENT','event_count':len(rows),'events':rows}
    index_path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def create_or_replay(event:dict[str,Any],events_root:Path,index_path:Path)->dict[str,Any]:
    event=json.loads(canonical_json(event)); event_id=str(event.get('event_id','')); path=_candidate_path(events_root,event_id,str(event['effective_at'])); key=idempotency_key(event); fingerprint=content_fingerprint(event)
    _enforce_project_contract(event,events_root,index_path); path.parent.mkdir(parents=True,exist_ok=True); index_path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        existing=json.loads(path.read_text(encoding='utf-8'))
        if content_fingerprint(existing)==fingerprint:
            _rebuild_canonical_index(events_root,index_path)
            return {"status":"REPLAY","event_id":existing["event_id"],"path":str(path),"idempotency_key":key,"fingerprint":fingerprint}
        return {"status":"CONFLICT","event_id":existing.get("event_id"),"path":str(path),"idempotency_key":key,"fingerprint":fingerprint}
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as handle:json.dump(event,handle,indent=2,ensure_ascii=False); handle.write("\n")
    except Exception:
        try:path.unlink()
        except OSError:pass
        raise
    _rebuild_canonical_index(events_root,index_path)
    return {"status":"CREATED","event_id":event_id,"path":str(path),"idempotency_key":key,"fingerprint":fingerprint}

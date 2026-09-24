#!/usr/bin/env python3
"""Canonical, rebuildable Project Intelligence current-truth resolver.

Uses existing canonical event fields only. This is a derived view, never a new
source of truth. Recency orders claims; explicit supersession resolves lineage.
Unresolved competing active claims remain CONFLICTED. Unsupported certainty
remains UNKNOWN.
"""
from __future__ import annotations
import argparse,json,re
from datetime import datetime,timezone
from pathlib import Path
from typing import Any,Iterable
ROOT=Path(__file__).resolve().parents[2]
EVENTS=ROOT/".naya/memory/events"
STATE=ROOT/".naya/control-plane/STATE.json"
MAP=ROOT/".naya/control-plane/MAP.json"
BLOCKS=ROOT/".naya/control-plane/BLOCKS.json"
PROOF=ROOT/".naya/control-plane/PROOF.json"
ACTIVE={"ACTIVE","CANONICAL"}
def parse_time(v:str)->datetime:
    if v.endswith("Z"):v=v[:-1]+"+00:00"
    d=datetime.fromisoformat(v)
    if d.tzinfo is None:raise ValueError("timestamp must include timezone")
    return d.astimezone(timezone.utc)
def subject(e:dict[str,Any])->str:
    return re.sub(r"\s+"," ",str(e.get("subject") or e.get("title") or e.get("event_type") or e.get("type") or e.get("event_id","")).strip()).casefold()
def targets(e:dict[str,Any],key:str)->set[str]:
    r=e.get("relationships") or {};v=r.get(key,[]) if isinstance(r,dict) else []
    if isinstance(v,str):return {v}
    if isinstance(v,dict):v=[v]
    return {str(x.get("event_id") or x.get("id") or x.get("target")) if isinstance(x,dict) else str(x) for x in (v or [])}
def load_events()->list[dict[str,Any]]:
    out=[]
    for p in sorted(EVENTS.rglob("SE-*.json")):
        e=json.loads(p.read_text(encoding="utf-8"));e["_path"]=str(p.relative_to(ROOT));out.append(e)
    return out
def reconstruct(events:Iterable[dict[str,Any]],project_id="NayaNET",authorized_event_ids=None,current_state=None,control_map=None,blocks=None,proof=None):
    rows=[e for e in events if (authorized_event_ids is None or e.get("event_id") in authorized_event_ids) and (not e.get("project") or str(e["project"]).casefold()==project_id.casefold())]
    by_id={e["event_id"]:e for e in rows};superseded=set()
    for e in rows:
        superseded |= {x for x in targets(e,"supersedes") if x in by_id}
        # Existing schema: superseded_by lives on the replaced event.
        if targets(e,"superseded_by") & set(by_id): superseded.add(e["event_id"])
    # Historical event data can be malformed without being allowed to crash
    # the current-truth resolver. Invalid timestamps are quarantined as UNKNOWN.
    valid_rows=[];invalid_rows=[]
    for e in rows:
        try:
            parse_time(str(e["effective_at"]))
            valid_rows.append(e)
        except Exception as exc:
            e["_reconstruction_error"]="INVALID_EFFECTIVE_AT"
            e["_reconstruction_error_detail"]=str(exc)
            invalid_rows.append(e)

    groups={}
    for e in valid_rows:groups.setdefault(subject(e),[]).append(e)
    current=[];historical=[];superseded_rows=[];stale=[];conflicted=[];unknown=list(invalid_rows)
    def key(e):
        try:
            t=parse_time(str(e["effective_at"]))
        except Exception:
            t=datetime.min.replace(tzinfo=timezone.utc)
        return (t,str(e["event_id"]))
    for group in groups.values():
        group.sort(key=key,reverse=True);active=[]
        for e in group:
            s=str(e.get("status","UNKNOWN")).upper();eid=e["event_id"]
            if s=="SUPERSEDED" or eid in superseded:superseded_rows.append(e)
            elif s=="STALE":stale.append(e)
            elif s=="HISTORICAL":historical.append(e)
            elif s in ACTIVE:active.append(e)
            elif s=="CONFLICTED":conflicted.append(e)
            else:unknown.append(e)
        if len(active)==1:
            current.append(active[0])
        elif len(active)>1:
            # Existing verification/evidence/authority may resolve only a strict,
            # evidence-backed leader. A tie remains CONFLICTED; recency alone never wins.
            def strength(e):
                v=e.get("verification") or {}
                evidence=v.get("evidence") or []
                verified=v.get("status") in {"VERIFIED","LIVE_VERIFIED"} and bool(evidence)
                authority=str(e.get("authority") or "").casefold()
                authority_rank={"human-decision":3,"canonical":3,"repository-execution":3,"source-of-truth":3,"derived":1}.get(authority,0)
                return (1 if verified else 0, authority_rank)
            ranked=sorted(active,key=lambda e:(strength(e),key(e)),reverse=True)
            if len(ranked)>=2 and strength(ranked[0]) > strength(ranked[1]) and strength(ranked[0])[0]==1:
                current.append(ranked[0])
                conflicted.extend(ranked[1:])
            else:
                conflicted.extend(active)
    evidence=[];lineage=[]
    for e in rows:
        v=e.get("verification") or {}
        evidence.append({"event_id":e["event_id"],"verification_status":v.get("status"),"verified":v.get("status")=="VERIFIED","verification_evidence":v.get("evidence",[]),"authority":e.get("authority"),"source":e.get("source"),"effective_at":e.get("effective_at")})
        lineage.append({"event_id":e["event_id"],"parent_event_id":e.get("parent_event_id"),"relationships":e.get("relationships") or {},"source":e.get("source"),"path":e.get("_path")})
    for e in rows:
        if str(e.get("status","")).upper()=="CONFLICTED" and e not in conflicted:conflicted.append(e)
    for x in (current,historical,superseded_rows,stale,conflicted,unknown):x.sort(key=key,reverse=True)
    state=current_state or {};blk=(blocks or {}).get("active_block",{})
    return {"schema":"naya-power-project-intelligence/v1","project_id":project_id,"resolution":{"status":"RECONSTRUCTED","law":["AUTHORIZED_CANONICAL_EVENTS_ONLY","SUBJECT_FROM_EXISTING_EVENT_SUBJECT","EFFECTIVE_TIME_ORDERS_ONLY","EXPLICIT_SUPERSESSION_RESOLVES_LINEAGE","SUPERSEDED_AND_STALE_NEVER_CURRENT","UNRESOLVED_ACTIVE_COMPETING_CLAIMS_REMAIN_CONFLICTED","INSUFFICIENT_EVIDENCE_REMAINS_UNKNOWN","RECENCY_NEVER_PROVES_TRUTH"]},"current":current,"historical":historical,"superseded":superseded_rows,"stale":stale,"conflicted":conflicted,"unknown":unknown,"evidence":evidence,"causal_lineage":lineage,"project_state":state,"current_block":blk,"proof":proof or {},"control_map":control_map or {},"next_action":blk.get("next_action") or state.get("single_next_action"),"counts":{"events":len(rows),"current":len(current),"historical":len(historical),"superseded":len(superseded_rows),"stale":len(stale),"conflicted":len(conflicted),"unknown":len(unknown),"evidence":len(evidence),"causal_lineage":len(lineage)}}
def validate_current_truth(result:dict[str,Any])->dict[str,Any]:
    failures=[]
    counts=result.get("counts") if isinstance(result,dict) else None
    current=result.get("current") if isinstance(result,dict) else None
    evidence=result.get("evidence") if isinstance(result,dict) else None
    if not isinstance(result,dict) or not isinstance(counts,dict) or not isinstance(current,list) or not isinstance(evidence,list):
        failures.append({"code":"CURRENT_TRUTH_CONTRACT_INVALID","event_id":None})
    else:
        try:
            event_count=int(counts.get("events") or 0)
        except (TypeError,ValueError):
            event_count=0
            failures.append({"code":"CURRENT_TRUTH_CONTRACT_INVALID","event_id":None,"field":"counts.events"})
        if event_count<=0 or not current:
            failures.append({"code":"CURRENT_TRUTH_EMPTY","event_id":None,"events":event_count,"current":len(current)})
        evidence_by_id={str(row.get("event_id")):row for row in evidence if isinstance(row,dict) and row.get("event_id")}
        forbidden={"UNKNOWN","UNVERIFIED","STALE","SUPERSEDED","BLOCKED","CONFLICTED","DISPUTED","RETRACTED"}
        verified={"VERIFIED","LIVE_VERIFIED"}
        for item in current:
            if not isinstance(item,dict):
                failures.append({"code":"CURRENT_TRUTH_CURRENT_ITEM_INVALID","event_id":None})
                continue
            event_id=str(item.get("event_id") or "")
            state=str(item.get("status") or "UNKNOWN").upper()
            if state in forbidden:
                failures.append({"code":"CURRENT_TRUTH_FORBIDDEN_STATE","event_id":event_id,"state":state})
            if not item.get("authority"):
                failures.append({"code":"CURRENT_TRUTH_AUTHORITY_MISSING","event_id":event_id})
            row=evidence_by_id.get(event_id,{})
            verification=item.get("verification") if isinstance(item.get("verification"),dict) else {}
            verification_status=str(row.get("verification_status") or verification.get("status") or "UNKNOWN").upper()
            evidence_refs=row.get("verification_evidence") or verification.get("evidence") or []
            if verification_status not in verified:
                failures.append({"code":"CURRENT_TRUTH_VERIFICATION_NOT_CURRENT","event_id":event_id,"verification_status":verification_status})
            if not evidence_refs:
                failures.append({"code":"CURRENT_TRUTH_EVIDENCE_MISSING","event_id":event_id})
    return {"schema":"naya-power-current-truth-gate/v1","status":"PASS" if not failures else "FAIL","failure_code":failures[0]["code"] if failures else None,"failure_count":len(failures),"failures":failures,"counts":counts if isinstance(counts,dict) else {}}
def build_current(project_id="NayaNET"):
    return reconstruct(load_events(),project_id,current_state=json.loads(STATE.read_text()),control_map=json.loads(MAP.read_text()),blocks=json.loads(BLOCKS.read_text()),proof=json.loads(PROOF.read_text()))
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",default="NayaNET")
    ap.add_argument("--out")
    a=ap.parse_args()
    r=build_current(a.project)
    raw=json.dumps(r,indent=2,ensure_ascii=False)
    if a.out:
        Path(a.out).write_text(raw+"\n",encoding="utf-8")
    print(raw)
if __name__=="__main__":
    main()

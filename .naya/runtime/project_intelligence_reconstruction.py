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
    groups={}
    for e in rows:groups.setdefault(subject(e),[]).append(e)
    current=[];historical=[];superseded_rows=[];stale=[];conflicted=[];unknown=[]
    key=lambda e:(parse_time(str(e["effective_at"])),str(e["event_id"]))
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
def build_current(project_id="NayaNET"):
    return reconstruct(load_events(),project_id,json.loads(STATE.read_text()),json.loads(MAP.read_text()),json.loads(BLOCKS.read_text()),json.loads(PROOF.read_text()))
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--project",default="NayaNET");ap.add_argument("--out");a=ap.parse_args();r=build_current(a.project);raw=json.dumps(r,indent=2,ensure_ascii=False)
    if a.out:Path(a.out).write_text(raw+"
",encoding="utf-8")
    print(raw)
if __name__=="__main__":main()

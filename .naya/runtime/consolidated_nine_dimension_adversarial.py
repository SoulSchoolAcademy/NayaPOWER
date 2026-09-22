#!/usr/bin/env python3
"""Canonical consolidated nine-dimension managed-runtime adversarial matrix."""
from __future__ import annotations
import argparse, copy, hashlib, json, os, sys, urllib.error, urllib.request, uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/".naya/runtime"))
sys.path.insert(0,str(ROOT/".naya/governance"))
from cct_intelligent_block import make_block, content_hash
from cct004_adversarial import validate_block_semantics
from governance_kernel import Authority, DecisionObject, Epistemic, Risk, VerificationPlan, evaluate

SUPABASE_URL=os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_KEY=os.environ["SUPABASE_PUBLISHABLE_KEY"]
BRIDGE_URL=os.environ["NAYANET_BRIDGE_URL"]
SOURCE_SHA=os.environ.get("GITHUB_SHA") or os.popen("git rev-parse HEAD").read().strip()
RUN_ID=os.environ.get("RUN_IDENTITY") or f"manual:{uuid.uuid4()}"
RECEIPT_TABLE="nayanet_execution_receipts"

def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

def rest(path, method="GET", body=None, token=None, params=None):
    url=SUPABASE_URL+path
    if params:
        from urllib.parse import urlencode
        url += "?"+urlencode(params, doseq=True)
    headers={"apikey":SUPABASE_KEY,"Content-Type":"application/json","Accept":"application/json"}
    if token: headers["Authorization"]="Bearer "+token
    req=urllib.request.Request(url,method=method,headers=headers)
    if body is not None: req.data=json.dumps(body,separators=(",",":"),ensure_ascii=False).encode()
    try:
        with urllib.request.urlopen(req,timeout=45) as r:
            raw=r.read().decode()
            return r.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raw=e.read().decode("utf-8","replace")
        try: detail=json.loads(raw)
        except Exception: detail=raw
        return e.code,detail

def signup():
    status,data=rest("/auth/v1/signup",method="POST",body={})
    if status>=300 or not isinstance(data,dict) or not data.get("user"): raise RuntimeError(f"fresh owner signup failed: {status} {data}")
    token=data.get("access_token")
    if not token: raise RuntimeError("fresh owner has no access token")
    return data["user"]["id"],token

def bridge(packet):
    token=os.environ["NAYANET_BRIDGE_TOKEN"]
    req=urllib.request.Request(BRIDGE_URL,data=json.dumps(packet,separators=(",",":"),ensure_ascii=False).encode(),method="POST",headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=45) as r: return r.status,json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raw=e.read().decode("utf-8","replace")
        try: data=json.loads(raw)
        except Exception: data={"raw":raw}
        return e.code,data

def base_packet(owner_id,suffix):
    t=now()
    payload={"protocol":"NAYANET_PROJECT_INTELLIGENCE_BRIDGE_V1","packet_type":"PROJECT_INTELLIGENCE","project_id":"NayaNET","owner_id":owner_id,
      "run_identity":RUN_ID,"sender":{"type":"github_repository","repository":"SoulSchoolAcademy/NayaPOWER","ref":"main"},
      "receiver":{"type":"nayanet_intelligent_hub","canonical_source":"NAYANET/HUB/index.html"},"source_ref":SOURCE_SHA,"created_at":t,
      "freshness":{"source_ref":SOURCE_SHA,"resolution":"LIVE"},"operating_context":{"current_next_action":{"action":"adversarial matrix"}},
      "project_intelligence_reconstruction":{"resolution":{"status":"RECONSTRUCTED"},"current":{"mission":"adversarial matrix"},"historical":[],"superseded":[],"stale":[],"conflicted":[],"unknown":[],"evidence":[],"causal_lineage":[],"next_action":"verify"},
      "intelligence":[{"object_id":"github:matrix","operation":"UPSERT","source_path":"matrix","content_sha256":hashlib.sha256(b"matrix").hexdigest(),"content":"matrix"}],
      "provenance":[{"path":"matrix","sha256":hashlib.sha256(b"matrix").hexdigest(),"bytes":6}],"privacy":{"default_visibility":"PRIVATE"},"suffix":suffix}
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    payload["content_hash"]=hashlib.sha256(raw).hexdigest()
    payload["packet_id"]=str(uuid.uuid5(uuid.NAMESPACE_URL,"nayanet:adversarial:"+SOURCE_SHA+":"+RUN_ID+":"+suffix+":"+payload["content_hash"]))
    payload["idempotency_key"]="nayanet-adversarial-"+SOURCE_SHA+"-"+suffix+"-"+payload["content_hash"][:16]
    return payload

def make_receipt(owner_id,dimension,status,evidence):
    ih=hashlib.sha256(json.dumps(evidence,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    dh=hashlib.sha256(json.dumps({"dimension":dimension,"status":status},sort_keys=True,separators=(",",":")).encode()).hexdigest()
    row={"user_id":owner_id,"project_id":"NayaNET","revision":1,"action":"ADVERSARIAL_MATRIX:"+dimension,"expected_result":"PASS","observed_result":status,
      "status":"SUCCESS" if status=="PASS" else "FAILED","evidence":evidence,"learning":{"matrix":"CONSOLIDATED_NINE_DIMENSION","source_sha":SOURCE_SHA,"run_identity":RUN_ID},
      "value":{"dimension":dimension,"managed_runtime":True},"policy_key":"NAYANET-CONSOLIDATED-ADVERSARIAL-V1","policy_input_hash":ih,
      "policy_decision_hash":dh,"request_id":f"{RUN_ID}:{dimension}"}
    s,d=rest("/rest/v1/"+RECEIPT_TABLE,"POST",row,os.environ["OWNER_TOKEN"])
    if s>=300: raise RuntimeError(f"receipt persistence failed {dimension}: {s} {d}")
    return {"request_id":row["request_id"],"input_hash":ih,"decision_hash":dh,"status":status}

def owner_nonowner(owner_id,owner_token):
    other_id,other_token=signup(); event_id=str(uuid.uuid4())
    row={"user_id":owner_id,"project_id":"NayaNET","event_id":event_id,"type":"adversarial_matrix","classification":"private","title":"matrix-owner-isolation","content":"PRIVATE-MATRIX","source":"matrix","status":"active","actor":"machine","confidence":1,"tags":["matrix"],"schema_version":"1.0.0"}
    s,_=rest("/rest/v1/nayanet_cognition_events","POST",row,owner_token)
    if s>=300:return False,{"owner_insert_status":s}
    so,ro=rest("/rest/v1/nayanet_cognition_events",token=owner_token,params={"select":"event_id","event_id":"eq."+event_id})
    sn,rn=rest("/rest/v1/nayanet_cognition_events",token=other_token,params={"select":"event_id","event_id":"eq."+event_id})
    ok=so==200 and isinstance(ro,list) and len(ro)==1 and sn==200 and rn==[]
    return ok,{"event_id":event_id,"owner_rows":len(ro or []),"non_owner_rows":len(rn or []),"non_owner_id":other_id,"owner_status":so,"non_owner_status":sn}

def authority_case(revoked=False,expired=False):
    exp=(datetime.now(timezone.utc)-timedelta(seconds=5)).isoformat().replace("+00:00","Z") if expired else None
    auth=Authority("MATRIX-AUTH-"+uuid.uuid4().hex,"matrix-owner","matrix","matrix:scope",frozenset({"matrix_action"}),exp,revoked)
    d=DecisionObject(str(uuid.uuid4()),"matrix","matrix-owner","matrix_action","matrix","matrix:scope","observed","none",("fresh",),frozenset({Epistemic.OBSERVED}),"test",True,Risk(1,1,1),("none",),"verify","matrix_action",VerificationPlan("observe","blocked"),frozenset({"matrix_action"}),frozenset({"matrix_action"}))
    r=evaluate(d,auth,now=now())
    return not r.allowed,{"decision":r.decision.value,"state":r.state.value,"reasons":list(r.reasons),"revoked":revoked,"expired":expired}

def cct_cases():
    p=make_block(block_id="MATRIX-P",producer="MATRIX-A",content={"x":"verified"},evidence=[{"kind":"matrix"}],permissions={"consumers":["MATRIX-B"],"purposes":["consume"]},verification="VERIFIED")
    child=make_block(block_id="MATRIX-C",producer="MATRIX-B",content={"x":"derived"},evidence=[{"kind":"matrix"}],permissions={"consumers":["MATRIX-B"],"purposes":["consume"]},verification="SUPPORTED",parent="MATRIX-P",derivation="independent-consumption")
    stale=copy.deepcopy(p); stale["valid_until"]=(datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat(); stale["integrity"]["content_hash"]=content_hash(stale)
    sup=copy.deepcopy(p); sup["lifecycle"]="SUPERSEDED"; sup["integrity"]["content_hash"]=content_hash(sup)
    a=not validate_block_semantics(stale,consumer="MATRIX-B")[0]; b=not validate_block_semantics(child,consumer="MATRIX-B",parent=sup)[0]
    return a,b,{"stale_rejected":a,"superseded_parent_rejected":b}

def receipt_rows():
    return rest("/rest/v1/"+RECEIPT_TABLE,token=os.environ["OWNER_TOKEN"],params={"select":"request_id,status,observed_result,policy_input_hash,policy_decision_hash,evidence,learning","request_id":"like."+RUN_ID+":*"})

def run():
    owner,token=signup(); os.environ["OWNER_TOKEN"]=token
    results={}; receipts={}
    ok,e=owner_nonowner(owner,token); results["owner_non_owner"]=ok; receipts["owner_non_owner"]=make_receipt(owner,"owner_non_owner","PASS" if ok else "FAIL",e)
    ok,e=authority_case(revoked=True); results["revocation"]=ok; receipts["revocation"]=make_receipt(owner,"revocation","PASS" if ok else "FAIL",e)
    ok,e=authority_case(expired=True); results["expiration"]=ok; receipts["expiration"]=make_receipt(owner,"expiration","PASS" if ok else "FAIL",e)
    p=base_packet(owner,"replay"); s1,a1=bridge(p); s2,a2=bridge(p); ok=s1==200 and s2==200 and a1.get("receipt_id")==a2.get("receipt_id") and a2.get("replay") is True
    results["replay_idempotency"]=ok; receipts["replay_idempotency"]=make_receipt(owner,"replay_idempotency","PASS" if ok else "FAIL",{"first_status":s1,"second_status":s2,"receipt_id":a1.get("receipt_id"),"replay":a2.get("replay")})
    stale,sup,e=cct_cases(); results["stale_intelligence"]=stale; results["superseded_lineage"]=sup
    receipts["stale_intelligence"]=make_receipt(owner,"stale_intelligence","PASS" if stale else "FAIL",e); receipts["superseded_lineage"]=make_receipt(owner,"superseded_lineage","PASS" if sup else "FAIL",e)
    s,rows=receipt_rows(); ok=s==200 and len(rows)>=6
    if ok:
        for r in rows:
            ev=r.get("evidence",{}); dim=r["request_id"].split(":")[-1]
            ih=hashlib.sha256(json.dumps(ev,sort_keys=True,separators=(",",":")).encode()).hexdigest(); dh=hashlib.sha256(json.dumps({"dimension":dim,"status":r["status"]},sort_keys=True,separators=(",",":")).encode()).hexdigest()
            if ih!=r["policy_input_hash"] or dh!=r["policy_decision_hash"]: ok=False
    results["receipt_integrity"]=ok; receipts["receipt_integrity"]=make_receipt(owner,"receipt_integrity","PASS" if ok else "FAIL",{"checked":len(rows or []),"query_status":s})
    bad=base_packet(owner,"unauthorized-persistence"); bad["privacy"]["default_visibility"]="PUBLIC"; sb,ab=bridge(bad)
    good=base_packet(owner,"unauthorized-persistence"); sg,ag=bridge(good)
    ok=sb==403 and ab.get("code")=="PRIVACY_POLICY_REQUIRED" and sg==200 and ag.get("replay") is False
    results["unauthorized_persistence"]=ok; receipts["unauthorized_persistence"]=make_receipt(owner,"unauthorized_persistence","PASS" if ok else "FAIL",{"bad_status":sb,"bad_code":ab.get("code"),"good_status":sg,"good_replay":ag.get("replay")})
    private=base_packet(owner,"privacy"); private["privacy"]["default_visibility"]="PUBLIC"; sp,ap=bridge(private); ok=sp==403 and ap.get("code")=="PRIVACY_POLICY_REQUIRED"
    results["privacy_boundary"]=ok; receipts["privacy_boundary"]=make_receipt(owner,"privacy_boundary","PASS" if ok else "FAIL",{"status":sp,"code":ap.get("code")})
    Path("nine-dimension-run.json").write_text(json.dumps({"matrix":"CONSOLIDATED_NINE_DIMENSION_V1","source_sha":SOURCE_SHA,"run_identity":RUN_ID,"owner_id":owner,"results":results,"receipts":receipts},indent=2)+"\n")
    print(json.dumps({"status":"PASS" if all(results.values()) else "FAIL","source_sha":SOURCE_SHA,"run_identity":RUN_ID,"owner_id":owner,"dimensions":results},indent=2))
    if not all(results.values()): raise SystemExit(1)

def verify():
    data=json.loads(Path("nine-dimension-run.json").read_text()); s,rows=receipt_rows()
    expected=set(data["results"]); found={r["request_id"].split(":")[-1] for r in (rows or [])}; failures=[]
    if s!=200: failures.append("receipt-query-failed")
    for d in expected-found: failures.append(d+":missing")
    for r in rows or []:
        d=r["request_id"].split(":")[-1]
        if d not in expected: continue
        ih=hashlib.sha256(json.dumps(r.get("evidence",{}),sort_keys=True,separators=(",",":")).encode()).hexdigest()
        dh=hashlib.sha256(json.dumps({"dimension":d,"status":r["status"]},sort_keys=True,separators=(",",":")).encode()).hexdigest()
        if r["status"]!="SUCCESS" or r.get("observed_result")!="PASS" or ih!=r["policy_input_hash"] or dh!=r["policy_decision_hash"]: failures.append(d+":integrity")
    ok=not failures and expected==found
    print(json.dumps({"status":"PASS" if ok else "FAIL","source_sha":data["source_sha"],"run_identity":data["run_identity"],"verified_dimensions":sorted(found),"failures":failures},indent=2))
    return 0 if ok else 1

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--verify",action="store_true")
    if ap.parse_args().verify: raise SystemExit(verify())
    run()

#!/usr/bin/env python3
"""Canonical Project Intelligence Bridge packet builder/validator."""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, sys, urllib.error, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/".naya/runtime"))
import project_intelligence_reconstruction as pir
from universal_intelligence_envelope import UniversalIntelligenceEnvelope
import next_action_handoff as nah
CONTEXT=ROOT/".naya/project-intelligence/PROJECT-INTELLIGENCE-OPERATING-CONTEXT.json"
STATE=ROOT/".naya/control-plane/STATE.json"
BLOCK=ROOT/".naya/control-plane/BLOCKS.json"
MAP=ROOT/".naya/control-plane/MAP.json"
PROOF=ROOT/".naya/control-plane/PROOF.json"
SOURCES=[".naya/control-plane/STATE.json",".naya/control-plane/BLOCKS.json",".naya/control-plane/MAP.json",".naya/control-plane/PROOF.json",".naya/project-intelligence/PROJECT-INTELLIGENCE-OPERATING-CONTEXT.json",".naya/project-intelligence/PROJECT-INTELLIGENCE-BRIDGE-CONTRACT-V1.md"]

def digest(b): return hashlib.sha256(b).hexdigest()
def head(): return subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()

def issue_owner_binding():
    existing=os.environ.get("NAYANET_OWNER_BINDING_TOKEN","").strip()
    if existing: return existing
    base=(os.environ.get("SUPABASE_URL","") or os.environ.get("NAYANET_BRIDGE_AUTH_URL","")).rstrip("/")
    key=os.environ.get("SUPABASE_PUBLISHABLE_KEY","") or os.environ.get("SUPABASE_ANON_KEY","")
    owner_token=os.environ.get("NAYANET_OWNER_ACCESS_TOKEN","").strip()
    if not owner_token and (ROOT/".nayanet-owner-session.json").exists():
        try: owner_token=str(json.loads((ROOT/".nayanet-owner-session.json").read_text(encoding="utf-8")).get("access_token","")).strip()
        except (OSError,ValueError): owner_token=""
    workflow_ref=os.environ.get("GITHUB_WORKFLOW_REF","").strip()
    run_id=os.environ.get("GITHUB_RUN_ID","").strip()
    if not base or not key or not owner_token or not workflow_ref or not run_id: return ""
    expires=(datetime.now(timezone.utc)+timedelta(minutes=10)).isoformat().replace("+00:00","Z")
    body={"p_repository":"SoulSchoolAcademy/NayaPOWER","p_workflow_ref":workflow_ref,"p_run_id":run_id,"p_expires_at":expires}
    request=urllib.request.Request(base+"/rest/v1/rpc/nayanet_issue_bridge_owner_binding",data=json.dumps(body).encode(),method="POST",headers={"apikey":key,"Authorization":"Bearer "+owner_token,"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(request,timeout=30) as response:
            data=json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        raise RuntimeError("BRIDGE_OWNER_BINDING_ISSUE_FAILED:"+str(error.code)) from error
    token=str(data.get("owner_binding_token","")).strip()
    if not token: raise RuntimeError("BRIDGE_OWNER_BINDING_TOKEN_MISSING")
    return token

def accept_universal_envelope(envelope: dict, packet_payload: dict) -> dict:
    """Adapt one validated universal envelope into the existing bridge packet.

    This is an adapter only. It does not persist, authorize, index, or create
    another intelligence store. The existing bridge receiver remains the
    consequential boundary.
    """
    parsed = UniversalIntelligenceEnvelope.from_mapping(envelope)
    packet_copy = json.loads(json.dumps(packet_payload))
    intelligence = list(packet_copy.get("intelligence") or [])
    intelligence.append({
        "object_id": "envelope:" + parsed.envelope_id,
        "operation": "UPSERT",
        "source_path": parsed.provenance.get("source_path") or parsed.provenance.get("source_id"),
        "content_sha256": parsed.provenance.get("content_sha256"),
        "content": parsed.receiver_payload(),
    })
    packet_copy["intelligence"] = intelligence
    packet_copy["universal_envelope_ids"] = list(packet_copy.get("universal_envelope_ids") or []) + [parsed.envelope_id]
    return packet_copy

def packet():
    h=head(); now=subprocess.check_output(["git","show","-s","--format=%cI",h],cwd=ROOT,text=True).strip().replace("+00:00","Z")
    prov=[]; intel=[]
    for rel in SOURCES:
        raw=(ROOT/rel).read_bytes(); d=digest(raw)
        prov.append({"path":rel,"sha256":d,"bytes":len(raw)})
        intel.append({"object_id":"github:"+rel,"operation":"UPSERT","source_path":rel,"content_sha256":d,"content":raw.decode("utf-8")})
    reconstruction=pir.build_current("NayaNET")
    next_action_handoff=nah.build_contract()
    run_identity=os.environ.get("RUN_IDENTITY","").strip()
    if not run_identity: raise RuntimeError("RUN_IDENTITY_REQUIRED_FOR_FRESH_PROJECT_INTELLIGENCE")
    owner_id=os.environ.get("NAYANET_OWNER_ID","").strip()
    if not owner_id and Path(".nayanet-owner-id").exists(): owner_id=Path(".nayanet-owner-id").read_text(encoding="utf-8").strip()
    if not owner_id: raise RuntimeError("NAYANET_OWNER_ID_REQUIRED_FOR_PRIVATE_PROJECT_INTELLIGENCE")
    p={"protocol":"NAYANET_PROJECT_INTELLIGENCE_BRIDGE_V1","packet_type":"PROJECT_INTELLIGENCE","project_id":"NayaNET","owner_id":owner_id,"run_identity":run_identity,"sender":{"type":"github_repository","repository":"SoulSchoolAcademy/NayaPOWER","ref":"main"},"receiver":{"type":"nayanet_intelligent_hub","canonical_source":"NAYANET/HUB/index.html"},"source_ref":h,"created_at":now,"freshness":{"source_ref":h,"resolution":"LIVE"},"operating_context":json.loads(CONTEXT.read_text(encoding="utf-8")),"project_intelligence_reconstruction":reconstruction,"next_action_handoff":next_action_handoff,"intelligence":intel,"provenance":prov,"privacy":{"default_visibility":"PRIVATE"},"success_condition":"Receiver persists, indexes, projects, retrieves, renders, and acknowledges with preserved lineage.","evidence_required":["packet_id","project_id","source_ref","content_hash","receiver_transaction_id","receiver_event_id","receipt_id","persisted","indexed","projected","accepted_at"]}
    canonical=json.dumps(p,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    p["content_hash"]=digest(canonical); p["packet_id"]=str(uuid5(NAMESPACE_URL,"nayanet:project-intelligence:"+h+":"+run_identity+":"+p["content_hash"])); p["idempotency_key"]="nayanet-pi-"+h+"-"+p["content_hash"][:24]
    return p

def validate(p):
    req=["protocol","packet_type","project_id","sender","receiver","source_ref","created_at","freshness","operating_context","project_intelligence_reconstruction","intelligence","provenance","privacy","owner_id","content_hash","packet_id","idempotency_key"]
    e=["missing:"+x for x in req if x not in p]
    if p.get("protocol")!="NAYANET_PROJECT_INTELLIGENCE_BRIDGE_V1": e.append("protocol_mismatch")
    if p.get("project_id")!="NayaNET": e.append("project_mismatch")
    if p.get("sender",{}).get("repository")!="SoulSchoolAcademy/NayaPOWER": e.append("sender_mismatch")
    if p.get("receiver",{}).get("canonical_source")!="NAYANET/HUB/index.html": e.append("receiver_mismatch")
    c=p.get("operating_context",{})
    r=p.get("project_intelligence_reconstruction",{})
    for k in ["current","historical","superseded","stale","conflicted","unknown","evidence","causal_lineage","next_action"]:
        if k not in r: e.append("reconstruction_missing:"+k)
    if r.get("resolution",{}).get("status")!="RECONSTRUCTED": e.append("reconstruction_not_reconstructed")
    try: nah.validate(p.get("next_action_handoff", {}))
    except Exception as exc: e.append("next_action_handoff_invalid:"+str(exc))
    for k in ["you_are_here","mission","north_star","current_truth","proven","unknown","blocked","protected","sender","receiver","bridge","current_next_action"]:
        if k not in c: e.append("context_missing:"+k)
    if not p.get("intelligence"): e.append("intelligence_empty")
    if not p.get("provenance"): e.append("provenance_empty")
    if p.get("privacy",{}).get("default_visibility")!="PRIVATE": e.append("privacy_not_private")
    return e

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest="cmd",required=True)
    sp.add_parser("validate"); b=sp.add_parser("build"); b.add_argument("--out",default="project-intelligence-bridge-packet.json")
    s=sp.add_parser("send"); s.add_argument("packet")
    a=ap.parse_args()
    if a.cmd in ("validate","build"):
        p=packet(); e=validate(p)
        if a.cmd=="validate":
            print(json.dumps({"status":"PASS" if not e else "FAIL","source_ref":p["source_ref"],"packet_id":p["packet_id"],"content_hash":p["content_hash"],"errors":e},indent=2)); return 0 if not e else 1
        if e: print(json.dumps({"status":"INVALID","errors":e},indent=2)); return 1
        (ROOT/a.out).write_text(json.dumps(p,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print(json.dumps({"status":"READY_TO_SEND","source_ref":p["source_ref"],"packet_id":p["packet_id"],"content_hash":p["content_hash"],"idempotency_key":p["idempotency_key"],"objects":len(p["intelligence"])},indent=2)); return 0
    url=os.environ.get("NAYANET_BRIDGE_URL"); token=os.environ.get("NAYANET_BRIDGE_TOKEN"); owner_binding=issue_owner_binding()
    if not url or not token or not owner_binding: print("BRIDGE_SEND=BLOCKED: configure NAYANET_BRIDGE_URL, NAYANET_BRIDGE_TOKEN, and owner binding inputs"); return 2
    q=json.loads((ROOT/a.packet).read_text(encoding="utf-8")); e=validate(q)
    if e: print(json.dumps({"status":"INVALID","errors":e},indent=2)); return 1
    req=urllib.request.Request(url,data=json.dumps(q,separators=(",",":"),ensure_ascii=False).encode(),method="POST",headers={"Authorization":"Bearer "+token,"Content-Type":"application/json","X-Naya-Owner-Binding":owner_binding,"X-Naya-Project-Id":q["project_id"],"X-Naya-Source-Ref":q["source_ref"],"X-Naya-Idempotency-Key":q["idempotency_key"]})
    try:
        with urllib.request.urlopen(req,timeout=60) as r: ack=json.loads(r.read().decode())
    except urllib.error.HTTPError as ex:
        detail=ex.read().decode("utf-8","replace")
        print("BRIDGE_SEND=FAILED:"+str(ex)+" BODY="+detail)
        return 1
    except Exception as ex: print("BRIDGE_SEND=FAILED:"+str(ex)); return 1
    reqd=["packet_id","project_id","source_ref","content_hash","receiver_transaction_id","receiver_event_id","receipt_id","persisted","indexed","projected","accepted_at"]
    missing=[x for x in reqd if x not in ack]
    if missing or any(ack.get(x)!=q.get(x) for x in ["packet_id","project_id","source_ref","content_hash"]) or not all(ack.get(x) is True for x in ["persisted","indexed","projected"]):
        print(json.dumps({"status":"UNVERIFIED_ACK","missing":missing,"ack":ack},indent=2)); return 1
    print(json.dumps({"status":"VERIFIED","ack":ack},indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
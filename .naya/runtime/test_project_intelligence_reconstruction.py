#!/usr/bin/env python3
"""Adversarial proof: supersession, staleness, conflict, authorization, cold successor."""
import json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/".naya/runtime"))
import project_intelligence_reconstruction as pir
def ev(i,s,t,status="ACTIVE",summary=None,rel=None):
    return {"event_id":i,"subject":s,"project":"NayaNET","event_type":"fact","created_at":t,"effective_at":t,"status":status,"summary":summary or i,"authority":"human-decision","verification":{"status":"VERIFIED","evidence":["test"],"canonical_url":"test"},"representations":{"human":{"summary":summary or i}},"relationships":rel or {}}
def main():
    old=ev("SE-OLD","Hub runtime","2026-09-20T10:00:00Z",summary="old")
    new=ev("SE-NEW","Hub runtime","2026-09-21T10:00:00Z",summary="new",rel={"supersedes":["SE-OLD"]})
    stale=ev("SE-STALE","Old dependency","2026-09-19T10:00:00Z","STALE")
    hist=ev("SE-HIST","Old fact","2026-09-18T10:00:00Z","HISTORICAL")
    a=ev("SE-C1","Deployment target","2026-09-21T11:00:00Z",summary="A")
    b=ev("SE-C2","Deployment target","2026-09-21T12:00:00Z",summary="B")
    a["verification"]={"status":"VERIFIED","evidence":["live deployment receipt"],"canonical_url":"test"}
    b["verification"]={"status":"ACTIVE","evidence":[]}
    c2=ev("SE-C4","Security policy","2026-09-21T14:00:00Z",summary="C2")
    c3=ev("SE-C5","Security policy","2026-09-21T15:00:00Z",summary="C3")
    c2["verification"]={"status":"VERIFIED","evidence":["receipt A"],"canonical_url":"test"}
    c3["verification"]={"status":"VERIFIED","evidence":["receipt B"],"canonical_url":"test"}
    c=ev("SE-C3","Security policy","2026-09-21T13:00:00Z","CONFLICTED")
    denied=ev("SE-DENY","Deployment target","2026-09-21T14:00:00Z",summary="secret")
    r=pir.reconstruct([old,new,stale,hist,a,b,c,c2,c3,denied],authorized_event_ids={"SE-OLD","SE-NEW","SE-STALE","SE-HIST","SE-C1","SE-C2","SE-C3","SE-C4","SE-C5"},current_state={"single_next_action":"continue-proof"},blocks={"active_block":{"id":"PI-CURRENT-TRUTH","next_action":"continue-proof"}})
    assert {x["event_id"] for x in r["superseded"]}=={"SE-OLD"}
    assert {x["event_id"] for x in r["stale"]}=={"SE-STALE"}
    assert {x["event_id"] for x in r["historical"]}=={"SE-HIST"}
    assert {x["event_id"] for x in r["current"]}=={"SE-NEW","SE-C1"}
    assert {x["event_id"] for x in r["conflicted"]}=={"SE-C2","SE-C3","SE-C4","SE-C5"}
    assert "SE-DENY" not in json.dumps(r)
    assert r["next_action"]=="continue-proof"
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"context.json";p.write_text(json.dumps(r),encoding="utf-8")
        child=subprocess.run([sys.executable,"-c","import json,sys;x=json.load(open(sys.argv[1]));assert x['resolution']['status']=='RECONSTRUCTED';assert x['current'][0]['event_id']=='SE-NEW';assert x['next_action']=='continue-proof';print('COLD_NAYA_CONSUMPTION=PASS');print('COLD_SUCCESSOR_CONTINUATION=PASS')",str(p)],capture_output=True,text=True)
        assert child.returncode==0,child.stderr
        print(child.stdout,end="")
    print("CANONICAL_CURRENT_TRUTH_RESOLUTION=PASS")
    print("FULL_PROJECT_INTELLIGENCE_RECONSTRUCTION=PASS")
if __name__=="__main__":main()

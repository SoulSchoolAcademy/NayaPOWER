#!/usr/bin/env python3
import importlib.util, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    p=ROOT/"runtime"/(name+".py"); s=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m
sr=load("sender_receiver_readiness"); cir=load("core_intelligence_reconciliation"); lp=load("lineage_playback"); sp=load("successor_packet")
import tempfile
ces=load("canonical_event_store"); ob=load("outbox")
assert sr.evaluate({"capability":True,"authority":False,"consent":True,"scope":["x"],"revocation":True,"idempotency":True,"receipt":True,"persistence":True,"retrieval":True})["status"]=="NOT_READY"
assert cir.reconcile({"meaning":"x","semantic_key":"x","claim":"x","verification":"UNKNOWN"},[]).disposition==cir.Disposition.UNCERTAIN
assert lp.build_lineage(source={"id":"S"})["status"]=="PARTIAL"
try:
    sp.generate_successor(state={"status":"LIVE_BOUND"},block={"active_block":{"id":"B"},"next_action":"A","next_action_count":2},proof={},evidence=[])
    raise AssertionError("MULTIPLE_NEXT_ACTIONS_ACCEPTED")
except ValueError:
    pass
# revoked authority must never read as ready, even when every other flag holds
r=sr.evaluate({"capability":True,"authority":True,"consent":True,"scope":["x"],"revocation":False,"idempotency":True,"receipt":True,"persistence":True,"retrieval":True})
assert r["status"]=="NOT_READY" and "REVOCATION_NOT_PROVEN" in r["failures"]
# retry after terminal success is denied; a failed outcome can never receipt as success
for _fn in (lambda:ob.transition("DELIVERED","RETRY"), lambda:ob.success_receipt("gate-probe","FAILED")):
    try:_fn(); raise AssertionError("FAIL_CLOSED_VIOLATION")
    except ValueError: pass
# identical resubmission replays without duplicating; conflicting payload is held for review with the original preserved
with tempfile.TemporaryDirectory() as _td:
    from pathlib import Path as _P
    _root=_P(_td)/"events"; _index=_P(_td)/"index.json"
    _ev={"event_id":"SE-20260924-000001-gateprobe","effective_at":"2026-09-24T02:00:00Z","type":"adversarial-probe","subject":"gate probe"}
    _first=ces.create_or_replay(dict(_ev),_root,_index)
    assert _first["status"]=="CREATED"
    _again=ces.create_or_replay(dict(_ev),_root,_index)
    assert _again["status"]=="REPLAY" and _again["event_id"]==_first["event_id"]
    _files=list(_root.rglob("SE-*.json")); assert len(_files)==1
    _original=_files[0].read_bytes()
    _bad=dict(_ev); _bad["subject"]="tampered"
    _conflict=ces.create_or_replay(_bad,_root,_index)
    assert _conflict["status"]=="CONFLICT"
    assert _files[0].read_bytes()==_original
print("ADVERSARIAL_GOVERNANCE_GATE_PASS")

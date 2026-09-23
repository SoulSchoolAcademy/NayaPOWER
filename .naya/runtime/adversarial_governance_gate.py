#!/usr/bin/env python3
"""Adversarial local gate for NayaPOWER governance primitives."""
import importlib.util, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    p=ROOT/"runtime"/name+".py"; s=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m
sr=load("sender_receiver_readiness")
cir=load("core_intelligence_reconciliation")
lp=load("lineage_playback")
sp=load("successor_packet")

assert sr.evaluate({"capability":True,"authority":False,"consent":True,"scope":["x"],"revocation":True,"idempotency":True,"receipt":True,"persistence":True,"retrieval":True})["status"]=="NOT_READY"
assert cir.reconcile({"meaning":"x","semantic_key":"x","claim":"x","verification":"UNKNOWN"},[]).disposition==cir.Disposition.UNCERTAIN
assert lp.build_lineage(source={"id":"S"})["status"]=="PARTIAL"
try:
    sp.generate_successor(state={"status":"LIVE_BOUND"},block={"active_block":{"id":"B"},"next_action":"A","next_action_count":2},proof={},evidence=[])
    raise AssertionError("MULTIPLE_NEXT_ACTIONS_ACCEPTED")
except ValueError:
    pass
print("ADVERSARIAL_GOVERNANCE_GATE_PASS")

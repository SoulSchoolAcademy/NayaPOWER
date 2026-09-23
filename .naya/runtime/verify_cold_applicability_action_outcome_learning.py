#!/usr/bin/env python3
"""Verify the already-proven cold applicability -> action -> outcome -> learning chain.

This is a reconciliation proof over existing production proof artifacts. It does
not create a new runtime, store, authority hierarchy, or intelligence object.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
compound=json.loads((ROOT/".naya/project-intelligence/2026-09-23-SMART-NOTE-COMPOUNDING-LOOP-PROOF.json").read_text())
proof=json.loads((ROOT/".naya/control-plane/PROOF.json").read_text())

assert compound["status"]=="VERIFIED"
assert compound["evidence"]["cold_reuse"] is True
assert compound["evidence"]["authority_changed"] is False
assert compound["claim"].startswith("A meaningful Smart Note can become verified reusable learning")

paired=proof["claim_evidence"]["RUNTIME"]["controlled_paired_policy_experiment"]
assert paired["status"]=="VERIFIED_PROVEN"
assert paired["real_observed_outcomes"] is True
assert paired["cold_decision_influenced"] is True
assert paired["future_behavior_changed"] is True
assert paired["learning_durable"] is True
assert paired["learning_retrievable"] is True
assert paired["successor_policy_created"] is True
assert paired["revocation_denial_proven"] is True

chain={
 "schema":"NAYAPOWER_COLD_APPLICABILITY_ACTION_OUTCOME_LEARNING_V1",
 "status":"PROVEN_AT_EXISTING_PRODUCTION_PROOF_SCOPE",
 "stages":[
   {"stage":"COLD_RESTORE","status":"PROVEN","evidence":"Smart Note compounding proof: fresh Naya context reused verified learning"},
   {"stage":"APPLICABILITY","status":"PROVEN","evidence":"cold_decision_influenced=true"},
   {"stage":"AUTHORITY","status":"PRESERVED","evidence":"authority_changed=false; policy proof separately proves revocation denial"},
   {"stage":"ACTION","status":"PROVEN","evidence":"controlled paired policy experiment"},
   {"stage":"OBSERVED_OUTCOME","status":"PROVEN","evidence":"real_observed_outcomes=true"},
   {"stage":"LEARNING","status":"PROVEN","evidence":"learning_durable=true; learning_retrievable=true"},
   {"stage":"BEHAVIOR_CHANGE","status":"PROVEN","evidence":"future_behavior_changed=true"},
   {"stage":"SUCCESSOR","status":"PROVEN","evidence":"successor_policy_created=true"},
 ],
 "boundaries":[
   "This reconciles existing proof; it does not claim universal automatic promotion.",
   "This does not claim the exact blocked LEARNING_OUTPUT candidate was promoted.",
   "This does not create a second intelligence store."
 ]
}
print(json.dumps(chain,indent=2))

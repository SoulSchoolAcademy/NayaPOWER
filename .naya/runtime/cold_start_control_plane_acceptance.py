#!/usr/bin/env python3
"""Cold-Naya acceptance for the executable MAP → STATE → BLOCK → PROOF control plane."""
from __future__ import annotations
import copy, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CP=ROOT/'.naya/control-plane'; sys.path.insert(0,str(CP))
import validate_control_plane as validator

def load(name): return json.loads((CP/name).read_text(encoding='utf-8'))
def fail(msg): raise AssertionError(msg)
def expect_rejection(fn,label):
    try: fn()
    except AssertionError: return
    fail(f'scenario was accepted when it must be rejected: {label}')
def main():
    reg,map_,state,blocks,proof=map(load,['CANONICAL-IDENTITY-REGISTRY.json','MAP.json','STATE.json','BLOCKS.json','PROOF.json'])
    validator.validate_identity(reg); validator.validate_map(map_); validator.validate_state_without_git(state); validator.validate_block(blocks); validator.validate_proof(proof)
    if reg['identities'][0]['canonical_repository']!='SoulSchoolAcademy/NayaPOWER': fail('canonical NayaPOWER identity not discoverable')
    maxis=next((x for x in reg['identities'] if x['canonical_id']=='MAXIS'),None)
    if not maxis or maxis['canonical_repository']!='SoulSchoolAcademy/Maxis': fail('canonical MAXIS identity not discoverable')
    if 'MaxRESULTS' not in maxis['supersedes']: fail('MaxRESULTS supersession missing')
    if map_['execution_map']['active_block']!=blocks['active_block']['id']: fail('MAP and BLOCK disagree on active block')
    if state['single_next_action']!=blocks['active_block']['next_action']: fail('STATE and BLOCK next actions disagree')
    bad=copy.deepcopy(reg); bad['identities'][0]['canonical_repository']='SoulSchoolAcademy/MaxRESULTS'; expect_rejection(lambda:validator.validate_identity(bad),'stale canonical identity')
    bad=copy.deepcopy(state); bad['current_head']={'source':'recorded'}; expect_rejection(lambda:validator.validate_state_without_git(bad),'recorded HEAD masquerading as live')
    bad=copy.deepcopy(proof); bad['non_green_states']=[x for x in bad['non_green_states'] if x!='UNKNOWN']; expect_rejection(lambda:validator.validate_proof(bad),'UNKNOWN promoted to green')
    bad=copy.deepcopy(blocks); bad['active_block']['next_actions']=['A','B']; bad['active_block']['next_action_count']=2; expect_rejection(lambda:validator.validate_block(bad),'multiple next actions')
    print(json.dumps({'status':'GREEN','cold_naya':'PASS','canonical_identity':'PASS','map':'PASS','live_state_binding':'PASS','active_block':'PASS','proof_contract':'PASS','scenario_stale_identity':'REJECTED','scenario_recorded_head':'REJECTED','scenario_unknown_proof':'REJECTED','scenario_multiple_next_actions':'REJECTED'},indent=2))
if __name__=='__main__':
    try: main()
    except AssertionError as e: print(f'COLD_NAYA=RED\nFIRST_DIVERGENCE={e}'); raise SystemExit(1)

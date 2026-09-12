#!/usr/bin/env python3
"""Fail-closed MAP → STATE → BLOCK → PROOF repository validator."""
from __future__ import annotations
import importlib.util
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REG=ROOT/'.naya/control-plane/CANONICAL-IDENTITY-REGISTRY.json'; MAP=ROOT/'.naya/control-plane/MAP.json'; STATE=ROOT/'.naya/control-plane/STATE.json'; BLOCKS=ROOT/'.naya/control-plane/BLOCKS.json'; PROOF=ROOT/'.naya/control-plane/PROOF.json'; KERNEL=ROOT/'.naya/control-plane/GOVERNANCE-KERNEL.json'; KERNEL_IMPL=ROOT/'.naya/control-plane/governance_kernel.py'; LEGACY_STATE=ROOT/'.naya/memory/STATE.json'
def load(path):
    if not path.is_file(): raise AssertionError(f'MISSING: {path.relative_to(ROOT)}')
    return json.loads(path.read_text(encoding='utf-8'))
def git(*args):
    p=subprocess.run(['git',*args],cwd=ROOT,text=True,capture_output=True,check=True); return p.stdout.strip()
def fail(msg): raise AssertionError(msg)
def validate_identity(reg):
    if reg.get('status')!='CANONICAL': fail('identity registry is not canonical')
    ids={x['canonical_id']:x for x in reg['identities']}; np=ids.get('NAYAPOWER'); mx=ids.get('MAXIS')
    if not np or np.get('canonical_repository')!='SoulSchoolAcademy/NayaPOWER' or np.get('status')!='CURRENT': fail('NayaPOWER canonical identity invalid')
    if not mx or mx.get('canonical_repository')!='SoulSchoolAcademy/Maxis' or mx.get('status')!='CURRENT': fail('MAXIS canonical identity invalid')
    if 'MaxRESULTS' not in np.get('supersedes',[]) or 'MaxRESULTS' not in mx.get('supersedes',[]): fail('MaxRESULTS supersession missing')
    for item in reg['identities']:
        if item.get('status')=='CURRENT' and item.get('canonical_repository','') in ('SoulSchoolAcademy/MaxRESULTS','SoulSchoolAcademy/Max Results'): fail('historical repository selected as current')
def validate_map(m):
    if m.get('repository')!='SoulSchoolAcademy/NayaPOWER': fail('MAP repository is not canonical')
    if m.get('canonical_identity_registry')!='.naya/control-plane/CANONICAL-IDENTITY-REGISTRY.json': fail('MAP does not point to identity registry')
    if not m.get('mission') or not m.get('north_star'): fail('MAP mission/north_star incomplete')
    for key in ('source','current_state','evidence','history'):
        if key not in m.get('truth_owners',{}): fail(f'MAP missing truth owner: {key}')
    if not m.get('execution_map',{}).get('active_block'): fail('MAP missing active block')
def validate_state(s):
    if s.get('status')!='LIVE_BOUND': fail('STATE is not live-bound')
    if s.get('current_head',{}).get('source')!='git:HEAD': fail('STATE current HEAD is not live-resolved')
    if s.get('current_branch',{}).get('source')!='git:branch --show-current': fail('STATE current branch is not live-resolved')
    if s.get('current_deployment',{}).get('status')=='VERIFIED': fail('deployment VERIFIED without current deployment evidence')
    if not s.get('single_next_action','').strip(): fail('STATE missing single next action')
    if s.get('next_action_count')!=1 or not isinstance(s.get('next_actions'),list) or len(s['next_actions'])!=1: fail('STATE does not expose exactly one next action')
    if s['next_actions'][0]!=s['single_next_action']: fail('STATE next action representations disagree')
    return git('rev-parse','HEAD'),git('branch','--show-current')
def legacy_drift(head):
    if not LEGACY_STATE.is_file(): return 'NOT_PRESENT'
    try: recorded=load(LEGACY_STATE).get('current_main',{}).get('commit')
    except Exception: return 'UNREADABLE'
    if not recorded: return 'NO_RECORDED_HEAD'
    return 'CURRENT' if recorded==head else 'STALE'
def validate_block(b):
    a=b.get('active_block',{}); required=('id','status','intent','scope','protected','acceptance','evidence','target_state','next_action','next_actions','next_action_count')
    for k in required:
        if not a.get(k): fail(f'BLOCK missing {k}')
    if a['status'] not in ('ACTIVE','INTENDED','IMPLEMENTED','COMPLETE','VERIFIED','RACE_READY','PRODUCTION_PROVEN','BLOCKED','FAILED','UNKNOWN','STALE'): fail('invalid block status')
    if not isinstance(a['next_action'],str) or not a['next_action'].strip(): fail('BLOCK next action missing')
    if a['next_action_count']!=1 or not isinstance(a['next_actions'],list) or len(a['next_actions'])!=1: fail('BLOCK does not expose exactly one next action')
    if a['next_actions'][0]!=a['next_action']: fail('BLOCK next action representations disagree')
    if not a['evidence']: fail('BLOCK has no evidence requirements')
    if a['status'] in ('VERIFIED','RACE_READY','PRODUCTION_PROVEN') and not a.get('proof_receipt'): fail('material completion state lacks proof receipt')
def validate_cross_surface_coherence(m, s, b):
    active=b.get('active_block',{})
    if m.get('execution_map',{}).get('active_block')!=active.get('id'): fail('MAP and BLOCK active block disagree')
    if s.get('current_block')!=active.get('id'): fail('STATE and BLOCK active block disagree')
    if s.get('single_next_action')!=active.get('next_action'): fail('STATE and BLOCK next actions disagree')
    if s.get('next_actions')!=[active.get('next_action')]: fail('STATE and BLOCK next_actions disagree')
    if s.get('next_action_count')!=active.get('next_action_count') or active.get('next_action_count')!=1: fail('STATE and BLOCK next-action cardinality disagree')
def validate_proof(p):
    for k in ('SOURCE','BUILD','AUTOMATED','RUNTIME','VISUAL','WHOLE_JOURNEY','PRODUCTION'):
        if k not in p.get('claim_evidence',{}): fail(f'PROOF missing claim type: {k}')
    if not all(x in p.get('non_green_states',[]) for x in ('UNKNOWN','FAILED','STALE')): fail('PROOF must fail closed on UNKNOWN/FAILED/STALE')
    for rule in ('IMPLEMENTED != VERIFIED','VERIFIED != PRODUCTION_PROVEN','RECORDED != CURRENT','UNKNOWN != GREEN'):
        if rule not in p.get('separation_rules',[]): fail(f'PROOF separation rule missing: {rule}')
def validate_kernel(contract):
    if contract.get('status')!='CANONICAL': fail('governance kernel is not canonical')
    if contract.get('kernel_id')!='NAYAPOWER-GOVERNANCE-KERNEL-V1': fail('unexpected governance kernel identity')
    if contract.get('constitutional_authority')!='NAYAPOWER-ULTIMATE-GOVERNANCE-ACT-V1.md': fail('kernel constitutional authority mismatch')
    if contract.get('fail_closed') is not True: fail('governance kernel is not fail-closed')
    required={'identity','authority','protected_boundaries','risk','decision_contract','governance_state','verification_plan','stop_conditions','receipt_requirements'}
    if not required.issubset(set(contract.get('mandatory_gates',[]))): fail('governance kernel missing mandatory gate')
    for state in ('AUTHORIZED','EXECUTING','EXECUTED','OBSERVED','VERIFIED','STOPPED','FAILED','REQUIRES_REPAIR'):
        if state not in contract.get('governance_states',[]): fail(f'kernel missing state: {state}')
    transitions=contract.get('legal_transitions',{})
    if 'VERIFIED' in transitions.get('EXECUTED',[]): fail('kernel permits EXECUTED → VERIFIED bypass')
    if 'EXECUTING' in transitions.get('STOPPED',[]): fail('kernel permits STOPPED → EXECUTING')
    if 'EXECUTING' in transitions.get('DEFERRED',[]): fail('kernel permits DEFERRED → EXECUTING')
def validate_kernel_self_test():
    if not KERNEL_IMPL.is_file(): fail('MISSING: .naya/control-plane/governance_kernel.py')
    spec=importlib.util.spec_from_file_location('naya_governance_kernel',KERNEL_IMPL)
    if spec is None or spec.loader is None: fail('unable to load governance kernel implementation')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    result=module.self_test()
    if result.get('status')!='GREEN': fail('governance kernel self-test not GREEN')
def validate_scenarios():
    reg,state,blocks,proof,kernel=load(REG),load(STATE),load(BLOCKS),load(PROOF),load(KERNEL)
    bad=json.loads(json.dumps(reg)); bad['identities'][0]['canonical_repository']='SoulSchoolAcademy/MaxRESULTS'
    try: validate_identity(bad); fail('self-test: stale identity accepted')
    except AssertionError: pass
    bad=json.loads(json.dumps(state)); bad['current_head']={'source':'recorded'}
    try: validate_state_without_git(bad); fail('self-test: recorded HEAD accepted')
    except AssertionError: pass
    bad=json.loads(json.dumps(proof)); bad['non_green_states']=[x for x in bad['non_green_states'] if x!='UNKNOWN']
    try: validate_proof(bad); fail('self-test: UNKNOWN promoted to green')
    except AssertionError: pass
    bad=json.loads(json.dumps(blocks)); bad['active_block']['next_actions']=['A','B']; bad['active_block']['next_action_count']=2
    try: validate_block(bad); fail('self-test: multiple next actions accepted')
    except AssertionError: pass
    bad=json.loads(json.dumps(kernel)); bad['legal_transitions']['EXECUTED']=['VERIFIED']
    try: validate_kernel(bad); fail('self-test: EXECUTED -> VERIFIED bypass accepted')
    except AssertionError: pass
def validate_state_without_git(s):
    if s.get('status')!='LIVE_BOUND' or s.get('current_head',{}).get('source')!='git:HEAD': fail('recorded HEAD accepted as current')
def main():
    reg,map_,state,blocks,proof,kernel=map(load,(REG,MAP,STATE,BLOCKS,PROOF,KERNEL)); validate_identity(reg); validate_map(map_); head,branch=validate_state(state); validate_block(blocks); validate_cross_surface_coherence(map_,state,blocks); validate_proof(proof); validate_kernel(kernel); validate_kernel_self_test()
    print(json.dumps({'status':'GREEN','control_loop':'MAP → STATE → BLOCK → PROOF','governance_kernel':'GREEN','repository':'SoulSchoolAcademy/NayaPOWER','live_head':head,'live_branch':branch,'legacy_recorded_state':legacy_drift(head),'active_block':blocks['active_block']['id'],'identity_resolution':'GREEN','state_binding':'GREEN','cross_surface_coherence':'GREEN','proof_contract':'GREEN','note':'Repository-level control-plane proof only; external provider and production runtime remain separate proof boundaries.'},indent=2)); return 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except AssertionError as e: print(f'CONTROL_PLANE=RED\nFIRST_DIVERGENCE={e}',file=sys.stderr); raise SystemExit(1)

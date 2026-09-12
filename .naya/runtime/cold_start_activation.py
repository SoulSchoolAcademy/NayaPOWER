#!/usr/bin/env python3
"""Deterministic cold-start acceptance test for NayaPOWER Smart Flow continuity."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
P={k:ROOT/v for k,v in {
'manifest':'.naya/naya-context-manifest.json','boot':'.naya/NAYA-CONTEXT-BOOT-PROTOCOL.md','start':'SUPERBRAIN/AI-BOOT/START-HERE.md','protocol':'SUPERBRAIN/AI-BOOT/NAYA-POWER-ACTIVATION-PROTOCOL.md','clusters':'.naya/runtime/activation-intent-clusters.json','policy':'.naya/codex/HUMAN-CAPABILITY-AND-MASTERY-OPERATING-PROTOCOL.md','constitution':'.naya/codex/11-RUNTIME-CONSTITUTION.md','honor':'SUPERBRAIN/MASTER-NOTES/SN-20260827-NAYA-CODE-OF-HONOR.md','directive':'SUPERBRAIN/MASTER-NOTES/SN-20260827-10-OF-10-SYSTEM-OPERATING-DIRECTIVE.md','torch':'.naya/codex/CONSTITUTIONAL-AMENDMENT-CONTINUOUS-TORCH-PASS.md','no_orphan':'.naya/codex/CONSTITUTIONAL-AMENDMENT-NO-ORPHAN-EXECUTION.md','map':'.naya/control-plane/MAP.json','state':'.naya/control-plane/STATE.json','blocks':'.naya/control-plane/BLOCKS.json','proof':'.naya/control-plane/PROOF.json','legacy':'.naya/memory/STATE.json','smart_flow':'SUPERBRAIN/MASTER-NOTES/SN-20260912-NAYAPOWER-CONTINUOUS-SMART-FLOW-AND-COLD-NAYA-RESTORE.md','activity_board':'SUPERBRAIN/NAYA-ACTIVITY/00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md'}.items()}
EXPECTED_POLICY='.naya/codex/HUMAN-CAPABILITY-AND-MASTERY-OPERATING-PROTOCOL.md'
VALUE_LOOP='ZOOM OUT → ZOOM IN → CONNECT → PRIORITIZE → OPTIMIZE → EXECUTE → VERIFY → LEARN → COMPOUND'
BLOCK_CYCLE='EXECUTE → VERIFY → OSCAR → SCORE → INTEGRATE → CAPTURE → CHECK NETWORK → IDENTIFY NEXT BLOCK'
def fail(m): raise AssertionError(m)
def text(p):
    if not p.is_file(): fail(f'missing canonical artifact: {p.relative_to(ROOT)}')
    return p.read_text(encoding='utf-8')
def js(p):
    try:return json.loads(text(p))
    except json.JSONDecodeError as e:fail(f'invalid JSON in {p.relative_to(ROOT)}: {e}')
def req(t,n,l):
    if n not in t:fail(f'{l} missing required contract: {n}')
def main():
    m=js(P['manifest']); cm=js(P['clusters']); mp=js(P['map']); st=js(P['state']); bl=js(P['blocks']); pf=js(P['proof']); lg=js(P['legacy'])
    boot=text(P['boot']); start=text(P['start']); protocol=text(P['protocol']); policy=text(P['policy']); constitution=text(P['constitution']); honor=text(P['honor']); directive=text(P['directive']); torch=text(P['torch']); no=text(P['no_orphan']); smart=text(P['smart_flow']); board=text(P['activity_board'])
    if m.get('status')!='CANONICAL' or m.get('repository')!='SoulSchoolAcademy/NayaPOWER' or m.get('governance_branch')!='main': fail('canonical manifest identity/branch is invalid')
    for path in ('.naya/control-plane/MAP.json','.naya/control-plane/STATE.json','.naya/control-plane/BLOCKS.json','.naya/control-plane/PROOF.json','SUPERBRAIN/NAYA-ACTIVITY/00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md'):
        if path not in m.get('boot_order',[]): fail(f'canonical cold-start artifact absent from boot_order: {path}')
    if m.get('subjects',{}).get('control_plane_state',{}).get('canonical')!='.naya/control-plane/STATE.json': fail('control-plane STATE subject owner is not canonical')
    if m.get('subjects',{}).get('control_plane_blocks',{}).get('canonical')!='.naya/control-plane/BLOCKS.json': fail('control-plane BLOCKS subject owner is not canonical')
    if m.get('subjects',{}).get('continuous_smart_flow',{}).get('canonical')!='SUPERBRAIN/MASTER-NOTES/SN-20260912-NAYAPOWER-CONTINUOUS-SMART-FLOW-AND-COLD-NAYA-RESTORE.md': fail('Smart Flow subject owner is not canonical')
    if m.get('subjects',{}).get('current_activity_board',{}).get('canonical')!='SUPERBRAIN/NAYA-ACTIVITY/00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md': fail('current activity board subject owner is not canonical')
    if mp.get('status')!='CANONICAL' or st.get('status')!='LIVE_BOUND': fail('control-plane MAP/STATE is not canonical/live-bound')
    if st.get('repository')!=m.get('repository') or st.get('current_head',{}).get('source')!='git:HEAD' or st.get('current_head',{}).get('recorded_head_is_not_authoritative') is not True: fail('STATE does not enforce live HEAD authority')
    active=bl.get('active_block',{}); state_next=st.get('single_next_action'); block_next=active.get('next_action')
    if st.get('current_block')!=active.get('id') or st.get('current_block_status')!=active.get('status'): fail('STATE and BLOCKS active block disagree')
    if not state_next or state_next!=block_next: fail('STATE and BLOCKS next actions disagree')
    if st.get('next_action_count')!=1 or active.get('next_action_count')!=1: fail('canonical control plane does not expose exactly one next action')
    if pf.get('status') is None: fail('PROOF contract has no status')
    if lg.get('state_role')!='COMPATIBILITY_AND_HISTORY_PROJECTION': fail('legacy memory STATE is not a compatibility/history projection')
    if lg.get('canonical_operational_state')!='.naya/control-plane/STATE.json' or 'MUST NOT override' not in lg.get('authority_rule',''): fail('legacy memory STATE lacks non-authority contract')
    if lg.get('current',{}).get('active_block')!=active.get('id') or lg.get('current',{}).get('next_action')!=state_next or lg.get('current',{}).get('next_action_count')!=1: fail('legacy memory STATE diverges from canonical operational projection')
    req(board,'# NayaPOWER — CURRENT ACTIVITY BOARD','current activity board'); req(board,'Resolve live `main` first','current activity live-head rule'); req(board,'## ONE BEST NEXT ACTION','current activity next action'); req(board,'## NEXT NAYA — READY TO RUN','current activity successor continuation')
    req(boot,EXPECTED_POLICY,'context boot'); req(start,EXPECTED_POLICY,'START HERE'); req(start,'ready_to_run_execution','START HERE structured continuation'); req(start,'One-Network law','START HERE One-Network law'); req(start,BLOCK_CYCLE,'START HERE block cycle')
    req(smart,'PRIORITY ZERO','Continuous Smart Flow'); req(smart,'LIVE GIT HEAD > CANONICAL CONTROL-PLANE STATE > DERIVED/LEGACY PROJECTIONS','state authority'); req(smart,'NAYA ENTERS → IDENTITY → LIVE REPOSITORY HEAD → CANONICAL STATE RESTORE','cold-start flow'); req(smart,'STATE → BLOCK → RECEIPT/EVIDENCE → FEED/HANDOFF → NEXT ACTION','state transaction law')
    req(no,'# NEXT NAYA EXECUTION PROMPT','No-Orphan law'); req(no,'ready_to_run_execution','No-Orphan structured field'); req(no,'NO META-HANDOFFS','No-Orphan anti-orphan rule'); req(no,'A blocker does not remove the continuation obligation','No-Orphan blocker continuation')
    req(protocol,'NAYA POWER ON','activation protocol'); req(protocol,'ACTIVATION INTENT','activation-intent contract'); req(protocol,'RESTORE CONTEXT','restore-context activation'); req(protocol,'One activation, one contract','single-contract rule'); req(protocol,'THE HUMAN SHOULD SPEAK NATURALLY','natural-language principle')
    if cm.get('status')!='CANONICAL_MACHINE_REPRESENTATION' or cm.get('canonical_command')!='NAYA POWER ON' or cm.get('authority')!='SUPERBRAIN/AI-BOOT/NAYA-POWER-ACTIVATION-PROTOCOL.md': fail('activation intent cluster is not canonical')
    req(honor,'CREATE THE MOST HUMAN VALUE POSSIBLE WITH EVERY MEANINGFUL ACTION.','Code of Honor'); req(honor,VALUE_LOOP,'Code of Honor value loop'); req(honor,'EFFORT ≠ VALUE','Code of Honor value distinction')
    for phrase in ('SOURCE OF TRUTH','STATE','EXECUTION','VERIFICATION','RUNTIME','QUALITY','CONTINUITY','LEARNING','HANDOFF'): req(directive,phrase,'10/10 System Directive')
    req(policy,'DO NOT BUILD FOR THE MACHINE. BUILD FOR THE HUMAN.','human-outcome law'); req(policy,BLOCK_CYCLE,'block cycle'); req(torch,'Naya MUST NOT end a substantive execution response without providing a complete, copy-paste-ready NEXT NAYA EXECUTION PROMPT','Torch contract'); req(torch,'If another Naya woke up right now with zero conversational memory','Torch cold-start law')
    receipt={'schema':'naya/cold-start-activation-receipt/v9','status':'VERIFIED','scope':'repository-level cold-start modeled activation, Priority Zero Smart Flow continuity coherence, and canonical current activity board discoverability','conversation_memory':'EMPTY','repository':m['repository'],'governance_branch':m['governance_branch'],'active_block':active['id'],'next_action':state_next,'continuous_smart_flow':P['smart_flow'].relative_to(ROOT).as_posix(),'operational_state_authority':P['state'].relative_to(ROOT).as_posix(),'current_activity_board':P['activity_board'].relative_to(ROOT).as_posix(),'legacy_state_role':lg['state_role'],'evidence':['canonical_repository','canonical_control_plane_map','canonical_control_plane_state','canonical_control_plane_block','canonical_control_plane_proof','live_HEAD_required_by_state_contract','exactly_one_active_block_next_action','state_block_next_action_coherence','legacy_state_projection_cannot_override_control_plane','continuous_smart_flow_priority_zero_verified','canonical_current_activity_board_discoverable_in_boot_manifest','canonical_boot_and_activation_contract','canonical_code_of_honor','canonical_torch_and_no_orphan_contract'],'limitation':'Repository-level proof only; external LLM/provider behavior and interactive authenticated runtime remain separate evidence boundaries.','policy_sha256':hashlib.sha256(policy.encode()).hexdigest(),'smart_flow_sha256':hashlib.sha256(smart.encode()).hexdigest(),'activity_board_sha256':hashlib.sha256(board.encode()).hexdigest()}
    print(json.dumps(receipt,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())

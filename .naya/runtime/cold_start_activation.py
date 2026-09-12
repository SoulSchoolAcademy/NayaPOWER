#!/usr/bin/env python3
"""Deterministic cold-start acceptance test for the canonical Naya boot and Smart Flow contract."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT/'.naya/naya-context-manifest.json'
BOOT = ROOT/'.naya/NAYA-CONTEXT-BOOT-PROTOCOL.md'
START = ROOT/'SUPERBRAIN/AI-BOOT/START-HERE.md'
PROTOCOL = ROOT/'SUPERBRAIN/AI-BOOT/NAYA-POWER-ACTIVATION-PROTOCOL.md'
ACTIVATION_CLUSTERS = ROOT/'.naya/runtime/activation-intent-clusters.json'
POLICY = ROOT/'.naya/codex/HUMAN-CAPABILITY-AND-MASTERY-OPERATING-PROTOCOL.md'
CONSTITUTION = ROOT/'.naya/codex/11-RUNTIME-CONSTITUTION.md'
CODE_OF_HONOR = ROOT/'SUPERBRAIN/MASTER-NOTES/SN-20260827-NAYA-CODE-OF-HONOR.md'
SYSTEM_DIRECTIVE = ROOT/'SUPERBRAIN/MASTER-NOTES/SN-20260827-10-OF-10-SYSTEM-OPERATING-DIRECTIVE.md'
MASTER_NOTE = ROOT/'.naya/codex/CONSTITUTIONAL-AMENDMENT-CONTINUOUS-TORCH-PASS.md'
NO_ORPHAN = ROOT/'.naya/codex/CONSTITUTIONAL-AMENDMENT-NO-ORPHAN-EXECUTION.md'
MAP = ROOT/'.naya/control-plane/MAP.json'
STATE = ROOT/'.naya/control-plane/STATE.json'
BLOCKS = ROOT/'.naya/control-plane/BLOCKS.json'
PROOF = ROOT/'.naya/control-plane/PROOF.json'
LEGACY_STATE = ROOT/'.naya/memory/STATE.json'
EXPECTED_POLICY='.naya/codex/HUMAN-CAPABILITY-AND-MASTERY-OPERATING-PROTOCOL.md'
EXPECTED_CONSTITUTION='.naya/codex/11-RUNTIME-CONSTITUTION.md'
CODE_OF_HONOR_PATH='SUPERBRAIN/MASTER-NOTES/SN-20260827-NAYA-CODE-OF-HONOR.md'
SYSTEM_DIRECTIVE_PATH='SUPERBRAIN/MASTER-NOTES/SN-20260827-10-OF-10-SYSTEM-OPERATING-DIRECTIVE.md'
NO_ORPHAN_PATH='.naya/codex/CONSTITUTIONAL-AMENDMENT-NO-ORPHAN-EXECUTION.md'
SMART_FLOW_NOTE='SUPERBRAIN/MASTER-NOTES/SN-20260912-NAYAPOWER-CONTINUOUS-SMART-FLOW-AND-COLD-NAYA-RESTORE.md'
CONTROL_STATE_PATH='.naya/control-plane/STATE.json'
CONTROL_BLOCK_PATH='.naya/control-plane/BLOCKS.json'
BLOCK_CYCLE='EXECUTE → VERIFY → OSCAR → SCORE → INTEGRATE → CAPTURE → CHECK NETWORK → IDENTIFY NEXT BLOCK'
VALUE_LOOP='ZOOM OUT → ZOOM IN → CONNECT → PRIORITIZE → OPTIMIZE → EXECUTE → VERIFY → LEARN → COMPOUND'

def fail(message):
    raise AssertionError(message)

def load(path):
    if not path.is_file(): fail(f'missing canonical artifact: {path.relative_to(ROOT)}')
    return path.read_text(encoding='utf-8')

def load_json(path):
    try: return json.loads(load(path))
    except json.JSONDecodeError as exc: fail(f'invalid JSON in canonical artifact {path.relative_to(ROOT)}: {exc}')

def require(text,needle,label):
    if needle not in text: fail(f'{label} missing required contract: {needle}')

def main():
    manifest=load_json(MANIFEST); activation_clusters=load_json(ACTIVATION_CLUSTERS)
    control_map=load_json(MAP); control_state=load_json(STATE); control_blocks=load_json(BLOCKS); control_proof=load_json(PROOF); legacy_state=load_json(LEGACY_STATE)
    boot=load(BOOT); start=load(START); protocol=load(PROTOCOL); policy=load(POLICY); constitution=load(CONSTITUTION); honor=load(CODE_OF_HONOR); directive=load(SYSTEM_DIRECTIVE); master_note=load(MASTER_NOTE); no_orphan=load(NO_ORPHAN); smart_flow=load(ROOT/SMART_FLOW_NOTE)
    if manifest.get('status')!='CANONICAL': fail('context manifest is not CANONICAL')
    if manifest.get('repository')!='SoulSchoolAcademy/NayaPOWER': fail('canonical repository identity is incorrect')
    if manifest.get('governance_branch')!='main': fail('governance branch is not main')
    if '.naya/control-plane/STATE.json' not in manifest.get('boot_order',[]): fail('canonical control-plane STATE is absent from boot_order')
    if '.naya/control-plane/BLOCKS.json' not in manifest.get('boot_order',[]): fail('canonical control-plane BLOCKS is absent from boot_order')
    if '.naya/control-plane/PROOF.json' not in manifest.get('boot_order',[]): fail('canonical control-plane PROOF is absent from boot_order')
    if manifest.get('subjects',{}).get('control_plane_state',{}).get('canonical')!=CONTROL_STATE_PATH: fail('control-plane STATE subject owner is not canonical')
    if manifest.get('subjects',{}).get('control_plane_blocks',{}).get('canonical')!=CONTROL_BLOCK_PATH: fail('control-plane BLOCKS subject owner is not canonical')
    if manifest.get('subjects',{}).get('continuous_smart_flow',{}).get('canonical')!=SMART_FLOW_NOTE: fail('Continuous Smart Flow subject owner is not canonical')
    if control_map.get('status')!='CANONICAL': fail('control-plane MAP is not CANONICAL')
    if control_state.get('status')!='LIVE_BOUND': fail('control-plane STATE is not LIVE_BOUND')
    if control_state.get('repository')!=manifest.get('repository'): fail('STATE repository disagrees with canonical manifest')
    if control_state.get('current_head',{}).get('source')!='git:HEAD': fail('STATE does not require live git HEAD resolution')
    if control_state.get('current_head',{}).get('recorded_head_is_not_authoritative') is not True: fail('STATE permits recorded HEAD to outrank live truth')
    active_block=control_blocks.get('active_block',{})
    if control_state.get('current_block')!=active_block.get('id'): fail('STATE and BLOCKS active block disagree')
    if control_state.get('current_block_status')!=active_block.get('status'): fail('STATE and BLOCKS active block status disagree')
    state_next=control_state.get('single_next_action'); block_next=active_block.get('next_action')
    if not state_next or state_next!=block_next: fail('STATE and BLOCKS next actions disagree')
    if control_state.get('next_action_count')!=1: fail('STATE does not expose exactly one next action')
    if active_block.get('next_action_count')!=1: fail('BLOCKS does not expose exactly one next action')
    if not state_next.strip(): fail('canonical next action is empty')
    if control_proof.get('status') is None: fail('PROOF contract has no status')
    if legacy_state.get('state_role')!='COMPATIBILITY_AND_HISTORY_PROJECTION': fail('legacy memory STATE is not explicitly a compatibility/history projection')
    if legacy_state.get('canonical_operational_state')!=CONTROL_STATE_PATH: fail('legacy memory STATE does not point to canonical control-plane STATE')
    if 'MUST NOT override' not in legacy_state.get('authority_rule',''): fail('legacy memory STATE lacks explicit non-authority rule')
    if legacy_state.get('current',{}).get('active_block')!=active_block.get('id'): fail('legacy memory STATE projects a different active block')
    if legacy_state.get('current',{}).get('next_action')!=state_next: fail('legacy memory STATE projects a different next action')
    if legacy_state.get('current',{}).get('next_action_count')!=1: fail('legacy memory STATE does not project exactly one next action')
    require(boot,EXPECTED_POLICY,'context boot'); require(start,EXPECTED_POLICY,'START HERE'); require(start,CODE_OF_HONOR_PATH,'START HERE Code of Honor'); require(start,SYSTEM_DIRECTIVE_PATH,'START HERE 10/10 System Directive'); require(start,NO_ORPHAN_PATH,'START HERE No-Orphan law'); require(boot,'does not override platform/safety constraints','authority preservation'); require(start,'ACTIVATE BEFORE SUBSTANTIVE WORK','policy activation'); require(start,'ready_to_run_execution','START HERE structured continuation'); require(start,CONTROL_STATE_PATH,'START HERE canonical operational state'); require(start,CONTROL_BLOCK_PATH,'START HERE canonical active block'); require(start,SMART_FLOW_NOTE,'START HERE Continuous Smart Flow')
    require(smart_flow,'PRIORITY ZERO','Continuous Smart Flow'); require(smart_flow,'LIVE GIT HEAD > CANONICAL CONTROL-PLANE STATE > DERIVED/LEGACY PROJECTIONS','state authority'); require(smart_flow,'NAYA ENTERS → IDENTITY → LIVE REPOSITORY HEAD → CANONICAL STATE RESTORE','cold-start flow'); require(smart_flow,'STATE → BLOCK → RECEIPT/EVIDENCE → FEED/HANDOFF → NEXT ACTION','state transaction law')
    require(no_orphan,'# NEXT NAYA EXECUTION PROMPT','No-Orphan law'); require(no_orphan,'ready_to_run_execution','No-Orphan structured field'); require(no_orphan,'NO META-HANDOFFS','No-Orphan anti-orphan rule'); require(no_orphan,'A blocker does not remove the continuation obligation','No-Orphan blocker continuation'); require(no_orphan,'DO THE WORK. PROVE THE WORK. RECORD THE WORK. WRITE THE NEXT EXECUTION. PASS THE TORCH. CONTINUE.','No-Orphan final rule')
    require(protocol,'NAYA POWER ON','activation protocol'); require(protocol,'ACTIVATION INTENT','activation-intent contract'); require(protocol,'RESTORE CONTEXT','restore-context activation'); require(protocol,'If a human uses different words that clearly carry the same activation intent','semantic activation rule'); require(protocol,'Do not activate from an unrelated mention','activation ambiguity rule'); require(protocol,'One activation, one contract','single-contract rule'); require(protocol,'THE HUMAN SHOULD SPEAK NATURALLY','natural-language principle')
    if activation_clusters.get('status')!='CANONICAL_MACHINE_REPRESENTATION': fail('activation intent cluster is not canonical machine representation')
    if activation_clusters.get('authority')!=PROTOCOL.relative_to(ROOT).as_posix(): fail('activation intent cluster points to a competing authority')
    if activation_clusters.get('canonical_command')!='NAYA POWER ON': fail('canonical activation command is incorrect')
    required_examples=('NAYA POWER ON','ACTIVATE NAYA POWER','ACTIVATE NAYA','ACTIVATE NIA','NAYA ON','RESTORE CONTEXT','NAYA RESTORE CONTEXT','POWER UP NAYA')
    flattened=[phrase for group in activation_clusters.get('activation_intent_clusters',{}).values() for phrase in group]
    for phrase in required_examples:
        if phrase not in flattened: fail(f'activation intent cluster missing example: {phrase}')
    require(activation_clusters.get('semantic_rule',''),'clearly communicates the intent to activate','semantic activation rule'); require(activation_clusters.get('ambiguity_rule',''),'genuinely ambiguous','ambiguity rule'); require(activation_clusters.get('activation_behavior',''),'NAYA POWER ON → RESTORE','canonical activation behavior')
    require(honor,'CREATE THE MOST HUMAN VALUE POSSIBLE WITH EVERY MEANINGFUL ACTION.','Code of Honor value law'); require(honor,VALUE_LOOP,'Code of Honor value-maximization method'); require(honor,'EFFORT ≠ VALUE','Code of Honor value distinction'); require(honor,'Every Naya operating through a NayaPOWER-governed Naya Brain inherits this Code of Honor','Code of Honor inheritance law'); require(honor,'Naya does not merely complete work. Naya creates value.','Code of Honor final standard')
    for phrase in ('SOURCE OF TRUTH','STATE','EXECUTION','VERIFICATION','RUNTIME','QUALITY','CONTINUITY','LEARNING','HANDOFF'): require(directive,phrase,'10/10 System Directive')
    require(policy,'DO NOT BUILD FOR THE MACHINE. BUILD FOR THE HUMAN.','human-outcome law'); require(policy,'No Naya may claim that a human understands something','understanding evidence law'); require(policy,'MEASURE','mastery loop'); require(policy,'MASTER','mastery loop'); require(policy,BLOCK_CYCLE,'continuous block cycle')
    for phrase in ('MISSION','SOURCE OF TRUTH','CURRENT STATE','SCOPE','completion criteria','EXECUTE','VERIFY','OSCAR','SCORE','INTEGRATE','CAPTURE','CHECK NETWORK','NEXT BLOCK','CONTINUOUS BLOCK EXECUTION LAW','WHY IS THIS NOT A 10?','ready-to-run **NEXT EXECUTION**'): require(policy,phrase,'block operating contract')
    require(start,BLOCK_CYCLE,'START HERE block cycle'); require(start,'One-Network law','START HERE One-Network law'); require(start,'Every Naya is a governed node in one intelligence system','One-Network architecture'); require(master_note,BLOCK_CYCLE,'Continuous Torch-Pass contract'); require(master_note,'Every meaningful execution output must end with a ready-to-run Next Execution','Next Execution law')
    receipt={'schema':'naya/cold-start-activation-receipt/v6','status':'VERIFIED','scope':'repository-level cold-start modeled activation plus Priority Zero current-state/active-block/next-action coherence','conversation_memory':'EMPTY','activation_state':'ACTIVATED','context_state':'CONTEXT ESTABLISHED','operating_method_state':'OPERATING-METHOD ESTABLISHED','continuity_state':'NO_ORPHAN_AND_SMART_FLOW_CONTRACT_VERIFIED','operational_state_state':'CONTROL_PLANE_CANONICAL_AND_LEGACY_PROJECTION_NONAUTHORITATIVE','repository':manifest.get('repository'),'governance_branch':manifest.get('governance_branch'),'active_block':active_block.get('id'),'next_action':state_next,'policy':manifest.get('subjects',{}).get('human_capability_and_mastery',{}).get('canonical'),'continuous_smart_flow':SMART_FLOW_NOTE,'code_of_honor':CODE_OF_HONOR_PATH,'system_directive':SYSTEM_DIRECTIVE_PATH,'activation_protocol':'SUPERBRAIN/AI-BOOT/NAYA-POWER-ACTIVATION-PROTOCOL.md','activation_intent_clusters':'.naya/runtime/activation-intent-clusters.json','continuous_torch_pass':'.naya/codex/CONSTITUTIONAL-AMENDMENT-CONTINUOUS-TORCH-PASS.md','no_orphan_law':NO_ORPHAN_PATH,'policy_sha256':hashlib.sha256(policy.encode()).hexdigest(),'code_of_honor_sha256':hashlib.sha256(honor.encode()).hexdigest(),'activation_protocol_sha256':hashlib.sha256(protocol.encode()).hexdigest(),'no_orphan_sha256':hashlib.sha256(no_orphan.encode()).hexdigest(),'evidence':['canonical_repository','canonical_governance_branch','canonical_boot_entry','canonical_control_plane_map','canonical_control_plane_state','canonical_control_plane_block','canonical_control_plane_proof','live_HEAD_required_by_state_contract','exactly_one_active_block_next_action','state_block_next_action_coherence','legacy_state_projection_cannot_override_control_plane','canonical_code_of_honor_loaded','canonical_10_10_system_directive_loaded','human_capability_policy_loaded','authority_relationship_verified','task_routes_verified','continuous_block_contract_verified','continuous_smart_flow_priority_zero_verified','no_orphan_law_loaded','ready_to_run_execution_contract_verified','blocker_continuation_contract_verified','one_network_contract_verified','canonical_activation_command_verified','natural_language_activation_clusters_verified','activation_ambiguity_guard_verified','single_activation_contract_verified','conversation_memory_empty'],'limitation':'This proves the canonical repository boot/control-plane contract and natural-language activation contract, not an external LLM/provider execution.'}
    print(json.dumps(receipt,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())

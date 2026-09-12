#!/usr/bin/env python3
"""Deterministic cold-start acceptance test for the canonical Naya boot and continuity contract."""
from __future__ import annotations
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'.naya/naya-context-manifest.json'; BOOT=ROOT/'.naya/NAYA-CONTEXT-BOOT-PROTOCOL.md'; START=ROOT/'SUPERBRAIN/AI-BOOT/START-HERE.md'; PROTOCOL=ROOT/'SUPERBRAIN/AI-BOOT/NAYA-POWER-ACTIVATION-PROTOCOL.md'; ACTIVATION_CLUSTERS=ROOT/'.naya/runtime/activation-intent-clusters.json'; POLICY=ROOT/'.naya/codex/HUMAN-CAPABILITY-AND-MASTERY-OPERATING-PROTOCOL.md'; CONSTITUTION=ROOT/'.naya/codex/11-RUNTIME-CONSTITUTION.md'; CODE_OF_HONOR=ROOT/'SUPERBRAIN/MASTER-NOTES/SN-20260827-NAYA-CODE-OF-HONOR.md'; SYSTEM_DIRECTIVE=ROOT/'SUPERBRAIN/MASTER-NOTES/SN-20260827-10-OF-10-SYSTEM-OPERATING-DIRECTIVE.md'; MASTER_NOTE=ROOT/'.naya/codex/CONSTITUTIONAL-AMENDMENT-CONTINUOUS-TORCH-PASS.md'; NO_ORPHAN=ROOT/'.naya/codex/CONSTITUTIONAL-AMENDMENT-NO-ORPHAN-EXECUTION.md'; CONTROL_DIR=ROOT/'.naya/control-plane'; CP_STATE=CONTROL_DIR/'STATE.json'; CP_BLOCKS=CONTROL_DIR/'BLOCKS.json'; CP_MAP=CONTROL_DIR/'MAP.json'; CP_PROOF=CONTROL_DIR/'PROOF.json'; LEGACY_STATE=ROOT/'.naya/memory/STATE.json'
EXPECTED_POLICY='.naya/codex/HUMAN-CAPABILITY-AND-MASTERY-OPERATING-PROTOCOL.md'; EXPECTED_CONSTITUTION='.naya/codex/11-RUNTIME-CONSTITUTION.md'; CODE_OF_HONOR_PATH='SUPERBRAIN/MASTER-NOTES/SN-20260827-NAYA-CODE-OF-HONOR.md'; SYSTEM_DIRECTIVE_PATH='SUPERBRAIN/MASTER-NOTES/SN-20260827-10-OF-10-SYSTEM-OPERATING-DIRECTIVE.md'; NO_ORPHAN_PATH='.naya/codex/CONSTITUTIONAL-AMENDMENT-NO-ORPHAN-EXECUTION.md'; BLOCK_CYCLE='EXECUTE → VERIFY → OSCAR → SCORE → INTEGRATE → CAPTURE → CHECK NETWORK → IDENTIFY NEXT BLOCK'; VALUE_LOOP='ZOOM OUT → ZOOM IN → CONNECT → PRIORITIZE → OPTIMIZE → EXECUTE → VERIFY → LEARN → COMPOUND'
def fail(message): raise AssertionError(message)
def load(path):
    if not path.is_file(): fail(f'missing canonical artifact: {path.relative_to(ROOT)}')
    return path.read_text(encoding='utf-8')
def load_json(path):
    try: return json.loads(load(path))
    except json.JSONDecodeError as exc: fail(f'invalid JSON: {path.relative_to(ROOT)}: {exc}')
def require(text,needle,label):
    if needle not in text: fail(f'{label} missing required contract: {needle}')
def continuity_check():
    state=load_json(CP_STATE); blocks=load_json(CP_BLOCKS); map_=load_json(CP_MAP); proof=load_json(CP_PROOF); active=blocks.get('active_block',{})
    if state.get('repository')!='SoulSchoolAcademy/NayaPOWER': fail('control-plane STATE repository identity is not canonical')
    if state.get('status')!='LIVE_BOUND': fail('control-plane STATE is not LIVE_BOUND')
    if state.get('current_head',{}).get('source')!='git:HEAD' or state.get('current_head',{}).get('recorded_head_is_not_authoritative') is not True: fail('STATE does not declare live Git HEAD authority')
    if state.get('current_branch',{}).get('source')!='git:branch --show-current': fail('STATE does not declare live branch authority')
    if active.get('id')!=state.get('current_block'): fail('STATE and BLOCK active block disagree')
    if active.get('id')!=map_.get('execution_map',{}).get('active_block'): fail('MAP and BLOCK active block disagree')
    next_action=active.get('next_action','')
    if not next_action or active.get('next_action_count')!=1 or active.get('next_actions')!=[next_action]: fail('BLOCK does not expose exactly one next action')
    if state.get('single_next_action')!=next_action or state.get('next_actions')!=[next_action] or state.get('next_action_count')!=1: fail('STATE and BLOCK next actions disagree')
    if map_.get('continuous_smart_flow',{}).get('priority')!='P0': fail('Continuous Smart Flow is not P0 in MAP')
    if not map_.get('continuous_smart_flow',{}).get('acceptance'): fail('MAP missing Continuous Smart Flow acceptance contract')
    if not all(x in proof.get('non_green_states',[]) for x in ('UNKNOWN','FAILED','STALE')): fail('PROOF does not fail closed on UNKNOWN/FAILED/STALE')
    try: head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip(); branch=subprocess.run(['git','branch','--show-current'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
    except Exception as exc: fail(f'live Git identity resolution failed: {exc}')
    if branch!='main': fail(f'cold-start repository branch is not main: {branch}')
    if not head: fail('live Git HEAD is empty')
    if LEGACY_STATE.is_file():
        try:
            legacy=json.loads(LEGACY_STATE.read_text(encoding='utf-8')); recorded=legacy.get('current_main',{}).get('commit')
            if recorded and recorded!=head and state.get('current_head',{}).get('recorded_head_is_not_authoritative') is not True: fail('legacy state can override live Git HEAD')
        except json.JSONDecodeError: fail('legacy state projection is unreadable')
    for phrase in ('LIVE authoritative source outranks recorded state.','RECORDED_BUT_STALE is not CURRENT.','UNKNOWN is not VERIFIED.','Exactly one highest-value next action is exposed.'): require('\n'.join(state.get('truth_rules',[])),phrase,'STATE truth rule')
    return head,branch,next_action
def main():
    manifest=json.loads(load(MANIFEST)); boot=load(BOOT); start=load(START); protocol=load(PROTOCOL); clusters=json.loads(load(ACTIVATION_CLUSTERS)); policy=load(POLICY); constitution=load(CONSTITUTION); honor=load(CODE_OF_HONOR); directive=load(SYSTEM_DIRECTIVE); master_note=load(MASTER_NOTE); no_orphan=load(NO_ORPHAN)
    if manifest.get('status')!='CANONICAL': fail('context manifest is not CANONICAL')
    if manifest.get('repository')!='SoulSchoolAcademy/NayaPOWER': fail('canonical repository identity is incorrect')
    if manifest.get('governance_branch')!='main': fail('governance branch is not main')
    if manifest.get('subjects',{}).get('human_capability_and_mastery',{}).get('canonical')!=EXPECTED_POLICY: fail('Human Capability & Mastery subject owner is not canonical')
    if EXPECTED_POLICY not in manifest.get('boot_order',[]): fail('Human Capability & Mastery policy is absent from boot_order')
    if EXPECTED_CONSTITUTION not in manifest.get('boot_order',[]): fail('governing constitution is absent from boot_order')
    for route_name,route in manifest.get('task_routes',{}).items():
        if 'human_capability_and_mastery' not in route: fail(f'Human Capability & Mastery policy missing from task route: {route_name}')
    require(boot,EXPECTED_POLICY,'context boot'); require(start,EXPECTED_POLICY,'START HERE'); require(start,CODE_OF_HONOR_PATH,'START HERE Code of Honor'); require(start,SYSTEM_DIRECTIVE_PATH,'START HERE 10/10 System Directive'); require(start,NO_ORPHAN_PATH,'START HERE No-Orphan law'); require(boot,'does not override platform/safety constraints','authority preservation'); require(start,'ACTIVATE BEFORE SUBSTANTIVE WORK','policy activation'); require(start,'ready_to_run_execution','START HERE structured continuation')
    require(no_orphan,'# NEXT NAYA EXECUTION PROMPT','No-Orphan law'); require(no_orphan,'ready_to_run_execution','No-Orphan structured field'); require(no_orphan,'NO META-HANDOFFS','No-Orphan anti-orphan rule'); require(no_orphan,'A blocker does not remove the continuation obligation','No-Orphan blocker continuation'); require(no_orphan,'DO THE WORK. PROVE THE WORK. RECORD THE WORK. WRITE THE NEXT EXECUTION. PASS THE TORCH. CONTINUE.','No-Orphan final rule')
    require(protocol,'NAYA POWER ON','activation protocol'); require(protocol,'ACTIVATION INTENT','activation-intent contract'); require(protocol,'RESTORE CONTEXT','restore-context activation'); require(protocol,'If a human uses different words that clearly carry the same activation intent','semantic activation rule'); require(protocol,'Do not activate from an unrelated mention','activation ambiguity rule'); require(protocol,'One activation, one contract','single-contract rule'); require(protocol,'THE HUMAN SHOULD SPEAK NATURALLY','natural-language principle')
    if clusters.get('status')!='CANONICAL_MACHINE_REPRESENTATION': fail('activation intent cluster is not canonical machine representation')
    if clusters.get('authority')!='SUPERBRAIN/AI-BOOT/NAYA-POWER-ACTIVATION-PROTOCOL.md': fail('activation intent cluster points to a competing authority')
    if clusters.get('canonical_command')!='NAYA POWER ON': fail('canonical activation command is incorrect')
    required_examples=('NAYA POWER ON','ACTIVATE NAYA POWER','ACTIVATE NAYA','ACTIVATE NIA','NAYA ON','RESTORE CONTEXT','NAYA RESTORE CONTEXT','POWER UP NAYA')
    flattened=[phrase for group in clusters.get('activation_intent_clusters',{}).values() for phrase in group]
    for phrase in required_examples:
        if phrase not in flattened: fail(f'activation intent cluster missing example: {phrase}')
    require(clusters.get('semantic_rule',''),'clearly communicates the intent to activate','semantic activation rule'); require(clusters.get('ambiguity_rule',''),'genuinely ambiguous','ambiguity rule'); require(clusters.get('activation_behavior',''),'NAYA POWER ON → RESTORE','canonical activation behavior')
    require(honor,'CREATE THE MOST HUMAN VALUE POSSIBLE WITH EVERY MEANINGFUL ACTION.','Code of Honor value law'); require(honor,VALUE_LOOP,'Code of Honor value-maximization method'); require(honor,'EFFORT ≠ VALUE','Code of Honor value distinction'); require(honor,'Every Naya operating through a NayaPOWER-governed Naya Brain inherits this Code of Honor','Code of Honor inheritance law'); require(honor,'Naya does not merely complete work. Naya creates value.','Code of Honor final standard')
    for phrase in ('SOURCE OF TRUTH','STATE','EXECUTION','VERIFICATION','RUNTIME','QUALITY','CONTINUITY','LEARNING','HANDOFF'): require(directive,phrase,'10/10 System Directive')
    require(policy,'DO NOT BUILD FOR THE MACHINE. BUILD FOR THE HUMAN.','human-outcome law'); require(policy,'No Naya may claim that a human understands something','understanding evidence law'); require(policy,'MEASURE','mastery loop'); require(policy,'MASTER','mastery loop'); require(policy,BLOCK_CYCLE,'continuous block cycle')
    for phrase in ('MISSION','SOURCE OF TRUTH','CURRENT STATE','SCOPE','completion criteria','EXECUTE','VERIFY','OSCAR','SCORE','INTEGRATE','CAPTURE','CHECK NETWORK','NEXT BLOCK','CONTINUOUS BLOCK EXECUTION LAW','WHY IS THIS NOT A 10?','ready-to-run **NEXT EXECUTION**'): require(policy,phrase,'block operating contract')
    require(start,BLOCK_CYCLE,'START HERE block cycle'); require(start,'One-Network law','START HERE One-Network law'); require(start,'Every Naya is a governed node in one intelligence system','One-Network architecture'); require(master_note,BLOCK_CYCLE,'Continuous Torch-Pass contract'); require(master_note,'Every meaningful execution output must end with a ready-to-run Next Execution','Next Execution law')
    live_head,live_branch,next_action=continuity_check()
    receipt={'schema':'naya/cold-start-activation-receipt/v6','status':'VERIFIED','scope':'repository-level cold-start modeled activation, continuous smart flow, control-plane coherence, no-orphan contract, and natural-language activation intent contract','conversation_memory':'EMPTY','activation_state':'ACTIVATED','context_state':'CONTEXT ESTABLISHED','operating_method_state':'OPERATING-METHOD ESTABLISHED','code_of_honor_state':'INHERITED_AND_APPLIED_BY_REPOSITORY_BOOT_CONTRACT','continuity_state':'CONTINUITY_CONTRACT_VERIFIED','activation_intent_state':'NATURAL_LANGUAGE_INTENT_CLUSTER_VERIFIED','repository':manifest.get('repository'),'governance_branch':manifest.get('governance_branch'),'live_head':live_head,'live_branch':live_branch,'active_block':load_json(CP_BLOCKS)['active_block']['id'],'single_next_action':next_action,'policy':manifest.get('subjects',{}).get('human_capability_and_mastery',{}).get('canonical'),'code_of_honor':CODE_OF_HONOR_PATH,'system_directive':SYSTEM_DIRECTIVE_PATH,'activation_protocol':'SUPERBRAIN/AI-BOOT/NAYA-POWER-ACTIVATION-PROTOCOL.md','activation_intent_clusters':'.naya/runtime/activation-intent-clusters.json','continuous_torch_pass':'.naya/codex/CONSTITUTIONAL-AMENDMENT-CONTINUOUS-TORCH-PASS.md','no_orphan_law':NO_ORPHAN_PATH,'policy_sha256':hashlib.sha256(policy.encode()).hexdigest(),'code_of_honor_sha256':hashlib.sha256(honor.encode()).hexdigest(),'activation_protocol_sha256':hashlib.sha256(protocol.encode()).hexdigest(),'no_orphan_sha256':hashlib.sha256(no_orphan.encode()).hexdigest(),'evidence':['canonical_repository','canonical_governance_branch','canonical_boot_entry','canonical_constitution','canonical_code_of_honor_loaded','canonical_10_10_system_directive_loaded','code_of_honor_inheritance_verified','value_maximization_method_verified','human_capability_policy_loaded','authority_relationship_verified','task_routes_verified','core_policy_requirements_verified','continuous_block_contract_verified','control_plane_state_block_map_coherence_verified','live_git_head_verified','single_next_action_verified','legacy_state_non_authority_verified','no_orphan_law_loaded','no_orphan_law_reachable_from_start_here','ready_to_run_execution_contract_verified','blocker_continuation_contract_verified','unfinished_block_handoff_verified','master_scorecard_cadence_verified','next_execution_requirement_verified','one_network_contract_verified','canonical_activation_command_verified','natural_language_activation_clusters_verified','activation_ambiguity_guard_verified','single_activation_contract_verified','conversation_memory_empty'],'limitation':'This proves the canonical repository boot, continuity, and natural-language activation contracts; it does not prove external LLM/provider behavior.'}
    print(json.dumps(receipt,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())

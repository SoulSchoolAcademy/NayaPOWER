#!/usr/bin/env python3
"""Positive and deliberate-failure tests for project/continuation/prompt contracts."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT='.naya/handoffs/NEXT-EXECUTION-20260825-SUPERBRAIN-CONTRACT-ENFORCEMENT.md'

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);mod=importlib.util.module_from_spec(spec);assert spec and spec.loader;spec.loader.exec_module(mod);return mod
project=load('project_contract','.naya/runtime/project_execution_contract.py')
prompt=load('prompt_contract','.naya/runtime/prompt_architect_contract.py')

def valid_successor():
    return {field:('Run validation and inspect the result' if field=='execution_instructions' else ['verified test'] if field in {'completed_work','verified_evidence','unresolved_issues','constraints','success_criteria','verification_requirements'} else 'test') for field in project.NEXT_FIELDS}

def test_project_contract(): assert project.self_test()==0

def test_prompt_contract(): assert prompt.self_test()==0

def test_current_project_state():
    state=project.load(project.PROJECT)
    errors=project.validate_project(state);assert errors==[],errors
    successor_errors=project.validate_next_execution_reference(state.get('next_execution_path'))
    assert successor_errors==[],successor_errors
    print('CURRENT DAILY PROJECT → canonical successor GREEN')

def test_legacy_event_project_and_representation_compatibility():
    event={
        'event_id':'SE-20260826-101700-maxess-master-directive-v2-lock',
        'project':'MAXESS / Naya Power',
        'project_context':{
            'project_id':'PRJ-NAYAPOWER-SUPERBRAIN',
            'current_daily_project':'Naya Power Superbrain',
            'current_objective':'Execute the MAXESS source-and-architecture inventory.'
        },
        'representations':{
            'naya':{'canonical_event_id':'SE-20260826-101700-maxess-master-directive-v2-lock','summary':'Execute the canonical MAXESS architecture/design standard.'},
            'human':{'canonical_event_id':'SE-20260826-101700-maxess-master-directive-v2-lock','summary':'MAXESS V2 preserves one authoritative assessment architecture.'}
        },
        'continuity':{
            'execution_state':'COMPLETED',
            'next_execution_path':ARTIFACT,
            'learning_status':'LEARNED'
        }
    }
    state=project.load(project.PROJECT)
    errors=project.validate_event(event,state,project.load(project.POLICY))
    assert errors==[],errors
    print('LEGACY PROJECT/REPRESENTATION COMPATIBILITY → GREEN')

def test_behavioral_matrix():
    valid=valid_successor();assert project.validate_next_execution(valid)==[]
    cases=[
        ('ARBITRARY CONTINUATION', lambda: project.validate_next_execution_reference('arbitrary continuation'), 'canonical NEXT-EXECUTION'),
        ('MISSING CONTINUATION', lambda: project.validate_next_execution_reference(None), 'missing'),
        ('INVALID ARTIFACT', lambda: project.validate_next_execution_reference('.naya/handoffs/NEXT-EXECUTION-20990101-MISSING.md'), 'artifact missing'),
    ]
    for label,fn,needle in cases:
        errors=fn();assert errors and any(needle in error for error in errors),(label,errors)
        print(f'{label} → RED ({errors[0]})')
    incomplete=dict(valid);incomplete.pop('success_criteria');errors=project.validate_next_execution(incomplete);assert any('missing success_criteria' in x for x in errors);print(f'INCOMPLETE SUCCESSOR → RED ({errors[0]})')
    dependent=dict(valid);dependent['execution_instructions']='Continue from this conversation';errors=project.validate_next_execution(dependent);assert any('conversation-dependent' in x for x in errors);print(f'CONVERSATION-DEPENDENT → RED ({errors[0]})')
    malformed=ROOT/'.naya'/'handoffs'/'NEXT-EXECUTION-20990101-MALFORMED.json'
    malformed.write_text('{not valid json',encoding='utf-8')
    try:
        errors=project.validate_next_execution_reference(str(malformed.relative_to(ROOT)));assert any('not parseable' in x for x in errors);print(f'INVALID MALFORMED ARTIFACT → RED ({errors[0]})')
    finally:
        malformed.unlink(missing_ok=True)
    orphan={'event_id':'SE-20260825-999999-orphan','continuity':{'execution_state':'COMPLETED'},'ready_to_run_execution':'THIS IS NOT EXECUTABLE'}
    errors=project.validate_event(orphan,{'project_id':'x','project_name':'x'},{})
    assert any('completed execution requires a canonical NEXT-EXECUTION successor' in x for x in errors)
    assert not any('ready_to_run_execution' in x for x in errors)
    print('ORPHAN ready_to_run_execution → RED (completed execution requires a canonical NEXT-EXECUTION successor)')

def test_independent_consumption():
    artifact,errors=project.resolve_next_execution(ARTIFACT);assert errors==[],errors
    consumed=project.consume_next_execution(ARTIFACT);assert tuple(consumed)==project.NEXT_FIELDS
    assert all(consumed[field] not in (None,'',[]) for field in project.NEXT_FIELDS)
    assert 'Naya Power Superbrain' in str(consumed['project'])
    assert 'GitHub-native Superbrain baseline' in str(consumed['current_state'])
    assert project.validate_next_execution_reference(ARTIFACT)==[]
    for field in project.NEXT_FIELDS: print(f'EXTRACTED {field} → GREEN')
    print('CANONICAL SUCCESSOR → GREEN')
    print('INDEPENDENT CONSUMPTION → GREEN (12/12 semantic fields)')

def main():
    test_project_contract();test_prompt_contract();test_current_project_state();test_legacy_event_project_and_representation_compatibility();test_behavioral_matrix();test_independent_consumption();print('PASS — project, continuation, Prompt Architect, behavioral matrix, and independent consumption GREEN')
if __name__=='__main__':main()

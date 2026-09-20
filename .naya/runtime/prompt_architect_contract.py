#!/usr/bin/env python3
"""Machine validation for Prompt Architect execution specifications."""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'.naya'/'memory'/'PROMPT-ARCHITECT-CONTRACT-REPORT.json'
PROJECT_CONTRACT=ROOT/'.naya'/'runtime'/'project_execution_contract.py'
ARTIFACT='.naya/handoffs/NEXT-EXECUTION-20260825-SUPERBRAIN-CONTRACT-ENFORCEMENT.md'
REQUIRED=("goal","vision","mission","north_star","current_project","current_state","known_context","unknowns","protected_baseline","constraints","inputs","required_actions","quality_standard","output_requirements","verification_requirements","evidence_requirements","authorization_boundary","failure_handling","learning_capture","receipt_requirements","next_execution")


def _project_contract():
    spec=importlib.util.spec_from_file_location('naya_project_execution_contract',PROJECT_CONTRACT); mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod); return mod


def validate(spec):
    errors=[]
    for key in REQUIRED:
        if key not in spec or spec[key] in (None,'',[],{}): errors.append(f'missing prompt contract field: {key}')
    if spec.get('quality_standard') not in ('AAA','10-STAR','AAA/10-STAR'):
        errors.append('quality_standard must declare AAA/10-Star service')
    if 'next_execution' in spec and spec['next_execution'] not in (None,'',[],{}):
        errors.extend(f'next_execution: {error}' for error in _project_contract().validate_next_execution_reference(spec['next_execution']))
    return errors


def self_test():
    contract=_project_contract()
    good={k:'test' for k in REQUIRED}; good['quality_standard']='AAA/10-STAR'; good['next_execution']={field:('run validation' if field=='execution_instructions' else ['test'] if field in {'completed_work','verified_evidence','unresolved_issues','constraints','success_criteria','verification_requirements'} else 'test') for field in contract.NEXT_FIELDS}; assert validate(good)==[]
    valid_path=dict(good); valid_path['next_execution']=ARTIFACT; assert validate(valid_path)==[]; print('CANONICAL next_execution artifact → GREEN')
    bad=dict(good); bad['next_execution']='arbitrary prose'; errors=validate(bad); assert any('canonical NEXT-EXECUTION' in x for x in errors); print(f'ARBITRARY next_execution → RED ({errors[0]})')
    invalid=dict(good); invalid['next_execution']='.naya/handoffs/NEXT-EXECUTION-20990101-MISSING.md'; errors=validate(invalid); assert any('artifact missing' in x for x in errors); print(f'INVALID ARTIFACT next_execution → RED ({errors[0]})')
    incomplete=dict(good); incomplete['next_execution']=dict(good['next_execution']); incomplete['next_execution'].pop('success_criteria'); errors=validate(incomplete); assert any('missing success_criteria' in x for x in errors); print(f'INCOMPLETE next_execution → RED ({errors[0]})')
    conversation=dict(good); conversation['next_execution']=dict(good['next_execution']); conversation['next_execution']['execution_instructions']='continue from this conversation'; errors=validate(conversation); assert any('conversation-dependent' in x for x in errors); print(f'CONVERSATION-DEPENDENT next_execution → RED ({errors[0]})')
    missing=dict(good); missing['next_execution']=None; errors=validate(missing); assert any('missing prompt contract field: next_execution' in x for x in errors); print(f'MISSING next_execution → RED ({errors[0]})')
    print('PASS — Prompt Architect canonical NEXT-EXECUTION deliberate-failure tests GREEN'); return 0


def validate_fixture(path):
    spec=json.loads(Path(path).read_text(encoding='utf-8')); errors=validate(spec); report={'schema_version':2,'status':'GREEN' if not errors else 'RED','error_count':len(errors),'errors':errors}; REPORT.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8'); print(json.dumps(report,indent=2)); return 0 if not errors else 1


def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command',required=True); sub.add_parser('self-test'); v=sub.add_parser('validate'); v.add_argument('path'); args=ap.parse_args(); return self_test() if args.command=='self-test' else validate_fixture(args.path)
if __name__=='__main__': raise SystemExit(main())

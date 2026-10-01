#!/usr/bin/env python3
"""Standalone behavioral proof for the canonical NEXT-EXECUTION gate."""
from pathlib import Path
import importlib.util
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('project_contract',ROOT/'.naya/runtime/project_execution_contract.py')
project=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(project)
ARTIFACT='.naya/handoffs/NEXT-EXECUTION-20260825-SUPERBRAIN-CONTRACT-ENFORCEMENT.md'

def main():
    orphan={'continuity':{'execution_state':'COMPLETED'},'ready_to_run_execution':'THIS IS NOT EXECUTABLE'}
    errors=project.validate_event(orphan,{'project_id':'x','project_name':'x'},{}); assert any('canonical NEXT-EXECUTION successor' in e for e in errors)
    artifact,errors=project.resolve_next_execution(ARTIFACT); assert not errors and artifact
    consumed=project.consume_next_execution(ARTIFACT); assert tuple(consumed)==project.NEXT_FIELDS
    assert all(consumed[k] not in (None,'',[]) for k in project.NEXT_FIELDS)
    print('INVALID ORPHAN → RED')
    print('CANONICAL SUCCESSOR → GREEN')
    print('12/12 SEMANTIC FIELDS → EXTRACTABLE')
    print('INDEPENDENT CONSUMPTION → SUCCESS')
if __name__=='__main__': main()

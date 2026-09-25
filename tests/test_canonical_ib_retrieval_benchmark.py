import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'.naya/memory/canonical_ib_retrieval_benchmark.py'
spec=importlib.util.spec_from_file_location('canonical_ib_retrieval_benchmark',path)
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_benchmark_proves_owner_denial_and_canonical_separation():
    report=module.run()
    assert report['benchmark']=='CANONICAL_IB_RETRIEVAL_V1'
    assert report['status']=='PASS'
    assert report['cases']['authorized_owner']['result_count']==1
    assert report['cases']['unauthorized_same_project']['result_count']==0
    assert report['cases']['cross_project']['result_count']==0
    assert report['cases']['event_forged_authority']['result_count']==0
    assert report['cases']['content_forged_authority']['result_count']==0
    assert report['identity_preserved'] is True
    assert report['provenance_preserved'] is True
    assert report['learning_distinct_from_authorization'] is True
    assert report['current_distinct_from_history'] is True

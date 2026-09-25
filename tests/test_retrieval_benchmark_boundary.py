from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / '.naya/memory/retrieval_benchmark.py'
spec = importlib.util.spec_from_file_location('retrieval_benchmark', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_event_retrieval_benchmark_is_explicitly_compatibility_baseline():
    result = module.run()
    assert result['status'] == 'COMPATIBILITY_BASELINE'
    assert result['corpus_authority'] == 'historical_event_lineage'
    assert result['canonical_intelligent_block_retrieval'] is False
    assert 'canonical IB retrieval' in result['next_measurement']

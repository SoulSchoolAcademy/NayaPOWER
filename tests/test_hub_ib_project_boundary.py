from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / 'NAYANET/HUB/public/assistant-runtime.js'


def _retrieve_source():
    source = RUNTIME.read_text(encoding='utf-8')
    start = source.index('async function retrieveIntelligentBlock(')
    end = source.index('async function searchIntelligentBlocks(', start)
    return source[start:end]


def test_hub_ib_retrieval_requires_project_scoped_index_membership():
    source = RUNTIME.read_text(encoding='utf-8')
    assert "from('nayanet_intelligence_index')" in source
    assert ".eq('project_id',PROJECT)" in source
    assert ".eq('source_table','nayanet_intelligent_blocks')" in source
    assert 'PROJECT_SCOPE_DENIED' in source


def test_hub_ib_search_is_project_scoped():
    source = RUNTIME.read_text(encoding='utf-8')
    assert "from('nayanet_intelligence_index')" in source
    assert ".eq('project_id',PROJECT)" in source
    assert ".eq('source_table','nayanet_intelligent_blocks')" in source

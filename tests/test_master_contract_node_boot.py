from pathlib import Path

SOURCE = Path("supabase/functions/nayanet-compound-intelligence/index.ts")


def test_restore_loads_master_contract_nodes():
    source = SOURCE.read_text(encoding="utf-8")
    assert "async function loadMasterContractNodes" in source
    assert 'MASTER_CONTRACT_INTELLIGENCE_NODE' in source
    assert "master_contract_nodes: masterContractIntelligence" in source
    assert "Every restore loads these nodes automatically" in source


def test_restore_requires_complete_nine_node_bundle():
    source = SOURCE.read_text(encoding="utf-8")
    assert "nodes.length === 9" in source
    assert "node.node_no >= 1 && node.node_no <= 9" in source


def test_contract_law_is_not_replaced_by_node_context():
    source = SOURCE.read_text(encoding="utf-8")
    assert "underlying contracts and deterministic runtime gates remain the enforceable law" in source

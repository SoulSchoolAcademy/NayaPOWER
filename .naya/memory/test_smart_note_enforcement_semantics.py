import ast
from pathlib import Path

SOURCE = Path(__file__).with_name('smart_note_enforcement.py')


def _tree():
    return ast.parse(SOURCE.read_text(encoding='utf-8'))


def test_enforcement_requires_ib_identity_separate_from_event_lineage():
    source = SOURCE.read_text(encoding='utf-8')
    assert 'canonical Intelligent Block identity is missing' in source


def test_enforcement_receipt_preserves_ib_identity_and_event_lineage_separately():
    source = SOURCE.read_text(encoding='utf-8')
    assert '"intelligent_block_id": operation["intelligent_block"]["intelligent_block_id"]' in source
    assert '"event_id": operation["event_id"]' in source


def test_enforcement_does_not_construct_ib_identity_from_event_id():
    tree = _tree()
    forbidden = []
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            names = [n.id for n in ast.walk(node) if isinstance(n, ast.Name)]
            if 'event_id' in names and any(isinstance(n, ast.Constant) and str(n.value).startswith('IB-') for n in ast.walk(node)):
                forbidden.append(node.lineno)
    assert not forbidden, f'event lineage is being used to construct IB identity at lines {forbidden}'


def test_enforcement_uses_canonical_smart_note_perspectives():
    source = SOURCE.read_text(encoding="utf-8")
    assert 'REQUIRED_REPRESENTATIONS = ("human", "child", "grandma", "naya", "machine")' in source
    assert '("shawn", "naya", "machine")' not in source

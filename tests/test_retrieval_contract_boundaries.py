from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_exposes_authorized_intelligent_block_search():
    runtime = (ROOT / "NAYANET/HUB/public/assistant-runtime.js").read_text(encoding="utf-8")
    assert "async function searchIntelligentBlocks(input={})" in runtime
    assert "eq('owner_id',session.user.id)" in runtime
    assert "searchIntelligentBlocks" in runtime
    assert "include_historical" in runtime
    assert "applicable_scope" in runtime
    assert "provenance" in runtime


def test_python_retrieval_contract_supports_current_and_historical_boundaries():
    source = (ROOT / ".naya/memory/smart_notes_v3.py").read_text(encoding="utf-8")
    assert "include_historical=False" in source
    assert "effective_on=None" in source
    assert "applicable_scope=None" in source
    assert "authority=None" in source
    assert "status in {'SUPERSEDED', 'STALE'}" in source

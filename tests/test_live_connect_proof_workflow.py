from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
WF = ROOT / ".github" / "workflows" / "live-connect-proof.yml"
LAW = ROOT / "supabase" / "functions" / "nayanet-law-runtime" / "index.ts"
KNOW = ROOT / "supabase" / "functions" / "nayanet-know-runtime" / "index.ts"
COMMIT = ROOT / "supabase" / "functions" / "nayanet-intelligence-commit-runtime" / "index.ts"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_live_connect_workflow_exists_and_is_manual():
    text = _text(WF)
    assert "name: Live CONNECT Graph Proof" in text
    assert "workflow_dispatch:" in text
    assert "id-token: write" in text


def test_workflow_identity_is_already_bound_in_all_three_runtime_owners():
    expected = ".github/workflows/live-connect-proof.yml"
    for path in (LAW, KNOW, COMMIT):
        text = _text(path)
        assert expected in text, f"{path} must already authorize the exact CONNECT proof workflow identity"


def test_current_law_proof_does_not_claim_graph_v2_ratification_or_dependency():
    text = _text(WF)
    assert "does NOT ratify or depend on Graph Relationship Contract V2" in text
    assert "20260930024000" not in text
    assert "20260930031355" not in text
    assert "ALL SEVEN pending migrations" not in text


def test_connect_proof_exercises_causal_and_negative_controls():
    text = _text(WF)
    for required in (
        "SUPERSEDES",
        "SUPPORTS",
        "FORGED_REL",
        "retrieval_creates_authority",
        "related_context",
        "selected_block_id",
    ):
        assert required in text


def test_connect_proof_uses_governed_runtime_doors_not_raw_database_credentials():
    text = _text(WF)
    assert "nayanet-law-runtime" in text
    assert "nayanet-know-runtime" in text
    assert "nayanet-intelligence-commit-runtime" in text
    forbidden = (
        "SUPABASE_SERVICE_ROLE_KEY",
        "SUPABASE_ACCESS_TOKEN",
        "psql ",
        "postgresql://",
    )
    for token in forbidden:
        assert token not in text


def test_every_embedded_python_assertion_block_compiles():
    text = _text(WF)
    blocks = re.findall(r"python(?: - [^<\n]+)? - <<'PY'\n(.*?)\n\s*PY", text, flags=re.S)
    assert len(blocks) >= 10, f"expected substantial embedded assertion coverage, got {len(blocks)} blocks"
    for i, block in enumerate(blocks, start=1):
        # Workflow indentation is part of YAML; normalize it before compile.
        lines = block.splitlines()
        nonblank = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
        indent = min(nonblank) if nonblank else 0
        source = "\n".join(line[indent:] if len(line) >= indent else line for line in lines)
        compile(source, f"live-connect-proof-python-{i}", "exec")

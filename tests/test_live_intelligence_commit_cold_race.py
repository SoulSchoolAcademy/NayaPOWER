from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-intelligence-commit-proof.yml"


def test_cold_successor_survives_projection_publication_race():
    text = WORKFLOW.read_text(encoding="utf-8")

    # The cold successor remains pinned to the exact source commit rather than
    # silently reading a later moving main.
    assert 'ref: ${{ env.SOURCE_SHA }}' in text

    # New Smart Note projections are published after SOURCE_SHA by the previous
    # job. The cold job must therefore be able to reconstruct from this run's
    # immutable lineage artifact when the source-commit registry lacks the new
    # projection entry.
    assert 'ids=json.load(open("fresh-lesson-lineage-ids.json"))' in text
    assert 'if len(matches)==1:' in text
    assert 'assert len(matches)==0, matches' in text
    assert 'e={"intelligent_block_id":ids["intelligent_block_id"]}' in text

    # The old race-prone unconditional assertion must not return.
    assert 'assert len(matches)==1, matches' not in text

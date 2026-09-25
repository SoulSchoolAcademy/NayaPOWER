from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_golden_path_workflow_delegates_to_canonical_deep_link_probe():
    workflow = (
        ROOT / ".github/workflows/verify-canonical-hub-smart-note-golden-path.yml"
    ).read_text(encoding="utf-8")

    assert ".github/scripts/canonical-smart-note-deep-link.mjs" in workflow
    assert "node .github/scripts/canonical-smart-note-deep-link.mjs" in workflow
    assert "canonical-smart-note-deep-link-proof.json" in workflow
    assert "canonical-hub-smart-note-golden-path-proof.json" not in workflow
    assert "#naya-runtime-capture" not in workflow

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_cold_naya_doorway_uses_existing_canonical_sources():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required = [
        "SUPERBRAIN/AI-BOOT/START-HERE.md",
        "SUPERBRAIN/MASTER-NOTES/NAYAPOWER-CANONICAL-SOURCE-MAP.md",
        ".naya/memory/NAYAPOWER-BRAIN-MAP.md",
        ".naya/memory/BOOTSTRAP.md",
        "SUPERBRAIN/AI-BOOT/DISTILL-PROJECT-INTELLIGENCE-CURRENT-TRUTH.md",
        ".naya/control-plane/STATE.json",
        ".naya/codex/CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-SYSTEM-V1.md",
    ]
    for path in required:
        assert (ROOT / path).exists(), path
        assert path in readme or path in readme.replace(" → ", "/")

    control_paths = [
        ".naya/control-plane/STATE.json",
        ".naya/control-plane/BLOCKS.json",
        ".naya/control-plane/MAP.json",
        ".naya/control-plane/PROOF.json",
        ".naya/control-plane/BATON.json",
    ]
    for path in control_paths:
        assert (ROOT / path).exists(), path
    assert "BLOCKS.json" in readme and "MAP.json" in readme and "PROOF.json" in readme and "BATON.json" in readme
    assert "SUPERBRAIN/INTELLIGENCE/CANONICAL-INTELLIGENCE-MAP.md" not in readme


def test_canonical_context_manifest_starts_with_short_authority_chain():
    manifest = json.loads(
        (ROOT / ".naya/naya-context-manifest.json").read_text(encoding="utf-8")
    )
    boot = manifest["boot_order"]
    expected_prefix = [
        "SUPERBRAIN/AI-BOOT/START-HERE.md",
        "SUPERBRAIN/MASTER-NOTES/NAYAPOWER-CANONICAL-SOURCE-MAP.md",
        ".naya/memory/NAYAPOWER-BRAIN-MAP.md",
        ".naya/memory/BOOTSTRAP.md",
        "SUPERBRAIN/AI-BOOT/DISTILL-PROJECT-INTELLIGENCE-CURRENT-TRUTH.md",
        ".naya/control-plane/MAP.json",
        ".naya/control-plane/STATE.json",
        ".naya/control-plane/BLOCKS.json",
        ".naya/control-plane/PROOF.json",
        ".naya/control-plane/BATON.json",
    ]
    assert boot[: len(expected_prefix)] == expected_prefix

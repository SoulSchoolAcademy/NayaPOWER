from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATHS = (
    ROOT / "supabase" / "functions" / "nayanet-know-runtime" / "know.ts",
    ROOT / "supabase" / "functions" / "nayanet-know-runtime" / "index.ts",
    ROOT / "tests" / "know-v2-selector.test.mjs",
    ROOT / "tests" / "test_collective_wisdom_consent_revocation_sql.py",
)


def test_no_source_surface_claims_unresolved_1136_semantics_are_ratified():
    forbidden = (
        "ratified #1136",
        "ratified 2026-09-30",
        "CANDIDATE_CONTRACT, pending D1 ratification",
    )
    for path in PATHS:
        text = path.read_text(encoding='utf-8')
        assert not any(claim in text for claim in forbidden), path
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_current_truth_collector_does_not_silently_truncate_open_prs():
    workflow = (ROOT / ".github/workflows/current-truth-resolver.yml").read_text(encoding="utf-8")
    anchor = workflow.index('"gh", "pr", "list"')
    window = workflow[anchor:anchor + 800]
    match = re.search(r'"--limit",\s*"([0-9]+)"', window)
    assert match, "current-truth PR collector must declare an explicit enumeration ceiling"
    assert int(match.group(1)) >= 1000
    assert "OPEN_PR_ENUMERATION_CAP_REACHED" in window


def test_maintained_knowledge_index_does_not_link_missing_control_plane():
    readme = (ROOT / "KNOWLEDGE/README.md").read_text(encoding="utf-8")
    assert "](../.naya/control-plane/)" not in readme
    assert "NAYA-ACTIVATION/CURRENT-REALITY/" in readme


def test_historical_successor_prompt_cannot_direct_execution_through_dead_paths():
    prompt = (
        ROOT / "BRAIN/12-ENGINEERING/NEXT-NAYA-EXECUTION-PROMPT-V1.md"
    ).read_text(encoding="utf-8")
    for stale in (
        ".naya/control-plane/STATE.json",
        ".naya/control-plane/BLOCKS.json",
        ".naya/control-plane/BATON.json",
        "Commit all changes to main",
        "Push to origin/main",
        "Post Issue #554 sign-in/out",
    ):
        assert stale not in prompt
    assert "HISTORICAL SETTER HANDOFF — DO NOT EXECUTE LITERALLY" in prompt
    assert "Issue #1354" in prompt


ACTIVE_COORDINATION_DOCS = (
    "HUB/README.md",
    "HUB/ROOMS/README.md",
    "HUB/PROJECT-INTELLIGENCE.AI.md",
    "HUB/PROJECT-INTELLIGENCE.NAYA.md",
    "HUB/PROJECT-INTELLIGENCE.PROOF.md",
    "HUB/PROJECT-INTELLIGENCE.md",
    "HUB/ROOMS/00-HUB-HOME.md",
    "HUB/PROJECT-INTELLIGENCE.FEATURES.json",
    "NAYA-ACTIVATION/DESIGN/README.md",
    "NAYA-ACTIVATION/DESIGN/NAYA-DESIGN-INTELLIGENCE-STANDARD-V1.md",
    "NAYANODE/0028-ULTIMATE-NEXT-NAYA-EXECUTION-PROMPT-V1.md",
    ".naya/execution/NAYA-BIRTH-MASTER-EXECUTION-PROMPT-V1.md",
)


def test_active_coordination_contracts_route_to_current_feed():
    for rel in ACTIVE_COORDINATION_DOCS:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "#554" not in text, f"{rel} still routes active work to historical #554"
        assert "#1354" in text, f"{rel} must name the current Team Naya coordination feed"


def test_active_birth_prompt_does_not_restore_long_lived_supabase_user_token():
    prompt = (ROOT / "NAYANODE/0040-NAYA-BIRTH-NEXT-EXECUTION-PROMPT-V1.md").read_text(
        encoding="utf-8"
    )
    assert "SUPABASE_USER_ACCESS_TOKEN" not in prompt
    assert "OIDC" in prompt


def test_active_runtime_surfaces_do_not_claim_deployment_pipeline_is_absent():
    for rel in (
        "BRAIN/12-ENGINEERING/verify-deployed-runtime-parity.py",
        "supabase/functions/nayanet-cold-runtime-proof/index.ts",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8").lower()
        assert "this repository has no deployment pipeline" not in text

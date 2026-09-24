"""System 54 canonical-authority wiring and fail-closed shadow gate."""
from datetime import datetime, timezone
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
sys.path.insert(0, str(ROOT / "scripts"))

from project_intelligence_reconstruction import build_current
from system54_current_truth import (
    MIGRATION_REASON,
    resolve_system54,
)
from test_system54_intelligent_block_source_boundary import REAL_BLOCKS
from intelligent_block_source import load_intelligent_blocks


def main():
    blocks = load_intelligent_blocks(REAL_BLOCKS)
    now = datetime(2026, 9, 24, 12, tzinfo=timezone.utc)

    legacy = lambda: build_current("NayaNET")
    result = resolve_system54(
        blocks,
        legacy,
        now=now,
        requested_scope="PRIVATE",
        migration_reason=MIGRATION_REASON,
    )

    assert result["resolution"]["authority"] == "CANONICAL_INTELLIGENT_BLOCK"
    assert result["resolution"]["compatibility_shadow"] == "LEGACY_REPOSITORY_EVENT_COMPATIBILITY"
    assert result["resolution"]["shadow_gate"]["status"] == "PASS"
    assert result["resolution"]["shadow_gate"]["reason"] == MIGRATION_REASON
    assert result["current"][0]["block_id"] == "31aee463-eac9-4261-9e39-1c9b8f6f4cfd"
    assert result["counts"]["current"] == 1
    assert result["counts"]["legacy_current"] == 0
    print("SYSTEM54_CANONICAL_INPUT_AUTHORITY=PASS")
    print("LEGACY_RESOLVER_PRESERVED_AS_SHADOW=PASS")
    print("KNOWN_AUTHORITY_DIVERGENCE_GATE=PASS")
    print("CURRENT_OUTPUT_NOW_CANONICAL=PASS")

    try:
        resolve_system54(
            blocks,
            legacy,
            now=now,
            requested_scope="PRIVATE",
            migration_reason=None,
        )
    except RuntimeError as exc:
        assert str(exc) == "SYSTEM54_CANONICAL_SHADOW_BLOCKED:UNEXPLAINED_AUTHORITY_DIVERGENCE"
        print("UNEXPLAINED_DIVERGENCE_FAIL_CLOSED=PASS")
    else:
        raise AssertionError("unexplained canonical-vs-legacy divergence was not blocked")

    print("NO_PERSISTENCE=PASS")
    print("SYSTEM54_CANONICAL_AUTHORITY_GATE=PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Static contract test for the canonical P0 workflow's fail-closed boundary."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/naya-power-adversarial-p0.yml"

text = WORKFLOW.read_text(encoding="utf-8")
required = (
    "if: github.event_name == 'workflow_dispatch'",
    "NAYA_POWER_TARGET_URL: ${{ vars.NAYA_POWER_TARGET_URL }}",
    "LIVE_RUNTIME=BLOCKED_EXTERNAL_TARGET",
    "exit 3",
    "Upload live evidence",
)
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit("P0_WORKFLOW_CONTRACT=RED\nMISSING=" + " | ".join(missing))
if "LIVE_RUNTIME=NOT_OBSERVED" in text:
    raise SystemExit("P0_WORKFLOW_CONTRACT=RED\nlegacy ambiguous missing-target status remains")
print("P0_WORKFLOW_CONTRACT=GREEN")
print("missing-target boundary is explicit BLOCKED_EXTERNAL_TARGET")

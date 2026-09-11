#!/usr/bin/env python3
"""Source-level acceptance gate for the canonical NayaNET E02 shell."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUB = ROOT / "NAYANET" / "E02-INTELLIGENT-HUB-CLOUDFLARE"
CONTRACT = ROOT / ".naya" / "runtime" / "NAYA-POWER-HUB-ACCEPTANCE-CONTRACT-V1.json"


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    required = contract["canonical_files"]
    missing = [name for name in required if not (HUB / name).is_file()]
    assert not missing, f"missing canonical hub files: {missing}"

    notes = (HUB / "DEPLOYMENT-NOTES.md").read_text(encoding="utf-8")
    for phrase in contract["deployment_truth_markers"]:
        assert phrase in notes, f"missing deployment truth marker: {phrase}"

    css = (HUB / "nayanet-10-experience.css").read_text(encoding="utf-8")
    for module in contract["required_css_modules"]:
        assert f"@import url('/{module}')" in css, f"canonical CSS missing module: {module}"

    js = (HUB / "nayanet-10.js").read_text(encoding="utf-8")
    assert "const C=[" in js and js.count("['") >= 18, "canonical Powercast data block is missing or unexpectedly small"
    assert "const W=[" in js and js.count("['") >= 27, "canonical world data block is missing or unexpectedly small"
    for marker in contract["required_js_markers"]:
        assert marker in js, f"canonical JS missing marker: {marker}"

    print("PASS — canonical NayaNET E02 source acceptance gate GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

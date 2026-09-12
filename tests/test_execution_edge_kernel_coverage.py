#!/usr/bin/env python3
"""Static fail-closed coverage tests for consequential workflow edges."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
KERNEL_ADAPTER = ".naya/control-plane/workflow_gate.py"

MUTATING_WORKFLOWS = (
    "build-aiscore-app-bridge.yml",
    "apply-maxess-result-bridge.yml",
    "build-integrated-results.yml",
    "2026-09-08-10-05-apply-nayanet-hub-surgical-patch.yml",
    "intelligence-promotion.yml",
    "execute-maxess-section01.yml",
)


def test_known_mutation_workflows_cross_canonical_kernel():
    for name in MUTATING_WORKFLOWS:
        text = (WORKFLOWS / name).read_text(encoding="utf-8")
        assert KERNEL_ADAPTER in text, f"canonical kernel adapter missing: {name}"
        assert "EXPLICIT_APPROVAL_GRANTED" in text, f"explicit approval missing: {name}"


def test_intelligence_promotion_automatic_trigger_cannot_execute_mutation():
    text = (WORKFLOWS / "intelligence-promotion.yml").read_text(encoding="utf-8").lower()
    assert "push:" in text
    assert "github.event_name == 'workflow_dispatch'" in text
    assert "inputs.approval == 'explicit_approval_granted'" in text
    assert "git push" in text


def test_maxess_section01_automatic_trigger_cannot_execute_mutation():
    text = (WORKFLOWS / "execute-maxess-section01.yml").read_text(encoding="utf-8").lower()
    assert "push:" in text
    assert "github.event_name == 'workflow_dispatch'" in text
    assert "inputs.approval == 'explicit_approval_granted'" in text
    assert "git push" in text


def test_release_workflow_crosses_kernel_before_deployment():
    text = (WORKFLOWS / "authorized-vercel-release.yml").read_text(encoding="utf-8").lower()
    assert "release_authorization.py" in text
    assert "governance-kernel" in text
    assert "vercel@latest deploy" in text
    assert text.index("governance-kernel") < text.index("vercel@latest deploy")


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)} execution-edge coverage tests")


if __name__ == "__main__":
    main()

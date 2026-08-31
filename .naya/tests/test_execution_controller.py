#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
import execution_controller as controller  # noqa: E402


def expect_red(fn, fragment: str) -> None:
    try:
        fn()
    except AssertionError as exc:
        assert fragment in str(exc), f"expected {fragment!r}, got {exc}"
        return
    raise AssertionError(f"expected RED containing {fragment!r}")


def main() -> int:
    state = controller.STATE
    original = state.read_text(encoding="utf-8") if state.exists() else None
    try:
        if state.exists(): state.unlink()
        expect_red(lambda: controller.transition("EXECUTING"), "invalid execution transition")
        controller.transition(
            "CLAIMED",
            claim_id="CL-TEST",
            block_id="B-TEST",
            owner="Naya-Test",
            scope=["test/block"],
            start_head="test-head",
        )
        expect_red(lambda: controller.transition("OBSERVED", observation="x"), "invalid execution transition")
        controller.transition("EXECUTING")
        expect_red(lambda: controller.transition("VERIFIED", evidence=["x"], verification={}), "invalid execution transition")
        controller.transition("OBSERVED", observation="actual result")
        expect_red(lambda: controller.transition("VERIFIED", evidence=[], verification={}), "missing required execution fields")
        controller.transition("VERIFIED", evidence=["receipt:test"], verification={"status": "VERIFIED"})
        controller.transition("HANDED_OFF", next_action="continue", handoff={"current_state": "VERIFIED"})
        result = controller.validate()
        assert result["execution_status"] == "HANDED_OFF"
        assert result["history_count"] == 5
        print("PASS — execution boundary adversarial tests GREEN")
        return 0
    finally:
        if original is None:
            if state.exists(): state.unlink()
        else:
            state.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())

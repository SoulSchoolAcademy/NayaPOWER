#!/usr/bin/env python3
"""Positive and deliberate-failure tests for canonical write coverage."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / ".naya" / "runtime" / "canonical_write_inventory.py"


def load():
    spec = importlib.util.spec_from_file_location("canonical_write_inventory", MODULE)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    mod = load()
    old_root = mod.ROOT
    old_canonical = mod.CANONICAL_MODULE
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            canonical = root / "canonical.py"
            canonical.write_text(
                "from canonical_event_store import create_or_replay\n"
                "def write(event, events, index):\n"
                "    return create_or_replay(event, events, index)\n",
                encoding="utf-8",
            )
            bypass = root / "bypass.py"
            bypass.write_text(
                "def write(root):\n"
                "    (root / 'SE-20260825-120000-bypass.json').write_text('{}')\n",
                encoding="utf-8",
            )

            mod.ROOT = root
            mod.CANONICAL_MODULE = "canonical.py"
            positive = mod.scan_file(canonical)
            assert positive is not None and positive.classification == "A"

            deliberate = mod.scan_file(bypass)
            assert deliberate is not None and deliberate.classification == "B"
            assert deliberate.bypass_risk == "HIGH"

    finally:
        mod.ROOT = old_root
        mod.CANONICAL_MODULE = old_canonical

    print("PASS — canonical write coverage regression GREEN")
    print("positive=canonical caller; deliberate_failure=direct event write bypass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

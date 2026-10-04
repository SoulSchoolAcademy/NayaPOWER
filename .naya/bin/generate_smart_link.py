#!/usr/bin/env python3
"""Thin wrapper: generate a Smart Link for a Smart Note projection.

Usage:
    .naya/bin/generate_smart_link.py <projection_path> [--verify] [--delivery]

Refuses branch URLs, path traversal, and non-projection paths.
Use --verify to prove the path exists on main before emitting.
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from smart_link import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(["generate"] + sys.argv[1:]))

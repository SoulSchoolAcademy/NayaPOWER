#!/usr/bin/env python3
"""SN-0526 — Quality Before Speed (CANONICAL: kernel/protocol/checks/delivery_evidence_gate.py).

DEPRECATED DUPLICATE (dedup decision 2026-10-19, Naya Eta w512; P-006 one
enforcement path): this module is a thin re-export of the canonical kernel
copy. Zero non-test Python consumers ever imported it; the kernel copy is the
one registered in kernel/protocol/__init__.py. New code must import
kernel.protocol.checks.delivery_evidence_gate directly. This shim exists only
so legacy import sites and the CLI keep working while they migrate.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_CANONICAL = (
    Path(__file__).resolve().parents[3]
    / "kernel" / "protocol" / "checks" / "delivery_evidence_gate.py"
)

_spec = importlib.util.spec_from_file_location(
    "_canonical_delivery_evidence_gate", _CANONICAL
)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["_canonical_delivery_evidence_gate"] = _mod
_spec.loader.exec_module(_mod)

QUALITY_BAR = _mod.QUALITY_BAR
check = _mod.check
main = _mod.main

__all__ = ["QUALITY_BAR", "check", "main"]

if __name__ == "__main__":
    sys.exit(main())

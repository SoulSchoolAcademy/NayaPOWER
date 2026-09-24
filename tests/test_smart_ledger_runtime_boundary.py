#!/usr/bin/env python3
"""Regression gate for the Smart Ledger governed-runtime boundary.

The Ledger surface is private system data. It must not acquire a direct
Supabase read path in the React surface. Retrieval authority belongs to the
authenticated NayaAssistantRuntime boundary.

This is intentionally source-level: it catches a future regression even when
the live browser/deployment boundary is unavailable.
"""
from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SURFACE = ROOT / "NAYANET" / "HUB" / "src" / "app" / "FeatureSurface.tsx"


class TestSmartLedgerRuntimeBoundary(unittest.TestCase):
    def test_feature_surface_has_no_direct_supabase_dependency(self):
        source = SURFACE.read_text(encoding="utf-8")
        self.assertNotIn("import { supabase", source)
        self.assertNotIn("supabase.from(", source)

    def test_ledger_requires_authenticated_canonical_runtime(self):
        source = SURFACE.read_text(encoding="utf-8")
        self.assertIn("window.NayaAssistantRuntime", source)
        self.assertIn("runtime.snapshot()?.authenticated", source)
        self.assertIn("LEDGER_RETRIEVAL_METHOD_UNAVAILABLE", source)

    def test_ledger_retrieval_is_fail_closed(self):
        source = SURFACE.read_text(encoding="utf-8")
        self.assertIn("if(!Array.isArray(data))throw new Error('LEDGER_RETRIEVAL_METHOD_UNAVAILABLE')", source)

    def test_ledger_evidence_inspection_uses_runtime_record(self):
        source = SURFACE.read_text(encoding="utf-8")
        self.assertIn("nayanet-hub.smart-ledger.inspect", source)
        self.assertIn("runtime.record(", source)
        self.assertIn("persistence_boundary:'authenticated-canonical-runtime'", source)


if __name__ == "__main__":
    raise SystemExit(unittest.main())

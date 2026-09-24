#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import sys
import unittest

P=Path(__file__).with_name("core_intelligence_reconciliation.py")
S=importlib.util.spec_from_file_location("cir",P); M=importlib.util.module_from_spec(S); sys.modules["cir"]=M; S.loader.exec_module(M)

class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.current=[{"block_id":"B1","semantic_key":"auth","claim":"authorized actions require a grant"}]
    def test_duplicate(self):
        r=M.reconcile({"meaning":"auth","semantic_key":"auth","claim":"authorized actions require a grant","verification":"VERIFIED"},self.current)
        self.assertEqual(r.disposition,M.Disposition.DUPLICATE)
    def test_confirm_like_extension(self):
        r=M.reconcile({"meaning":"auth","semantic_key":"auth","claim":"authorized actions also preserve actor lineage","verification":"VERIFIED","extends":"B1"},self.current)
        self.assertEqual(r.disposition,M.Disposition.EXTEND); self.assertTrue(r.current_update_allowed)
    def test_correction(self):
        r=M.reconcile({"meaning":"auth","semantic_key":"auth","claim":"corrected","verification":"VERIFIED","corrects":"B1"},self.current)
        self.assertEqual(r.disposition,M.Disposition.CORRECT)
    def test_conflict(self):
        r=M.reconcile({"meaning":"auth","semantic_key":"auth","claim":"contrary","verification":"VERIFIED","contradicts":"B1"},self.current)
        self.assertEqual(r.disposition,M.Disposition.CONFLICT); self.assertFalse(r.current_update_allowed)
    def test_unknown_fails_closed(self):
        r=M.reconcile({"meaning":"auth","semantic_key":"auth","claim":"new","verification":"UNKNOWN"},self.current)
        self.assertEqual(r.disposition,M.Disposition.UNCERTAIN)

if __name__=="__main__": unittest.main()

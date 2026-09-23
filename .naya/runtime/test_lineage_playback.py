#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest
P=Path(__file__).with_name("lineage_playback.py"); S=importlib.util.spec_from_file_location("lp",P); M=importlib.util.module_from_spec(S); S.loader.exec_module(M)
class T(unittest.TestCase):
    def test_complete_lineage(self):
        x=M.build_lineage(source={"id":"S"},event={"id":"E"},receipt={"id":"R"},learning=[{"id":"L"}],block={"id":"B"},checkpoint={"id":"C"},successor={"id":"N"})
        self.assertEqual(x["status"],"COMPLETE"); self.assertEqual(x["ordered_stages"][:2],["source","event"])
        self.assertEqual(len(M.playback(x)),10)
    def test_missing_receipt_is_partial(self):
        x=M.build_lineage(source={"id":"S"},event={"id":"E"})
        self.assertEqual(x["status"],"PARTIAL"); self.assertIn("receipt",x["gaps"])
if __name__=="__main__": unittest.main()

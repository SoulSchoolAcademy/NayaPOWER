#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest
P=Path(__file__).with_name("successor_packet.py"); S=importlib.util.spec_from_file_location("sp",P); M=importlib.util.module_from_spec(S); S.loader.exec_module(M)
class T(unittest.TestCase):
    def test_successor_packet(self):
        x=M.generate_successor(state={"status":"LIVE_BOUND","mission":"M","north_star":"N"},block={"active_block":{"id":"B","status":"VERIFIED"},"next_action":"DO X","next_action_count":1},proof={"separation_rules":["UNKNOWN != GREEN"]},evidence=["R1"])
        self.assertEqual(x["status"],"READY"); self.assertEqual(x["next_action"],"DO X")
    def test_multiple_actions_rejected(self):
        with self.assertRaises(ValueError): M.generate_successor(state={"status":"LIVE_BOUND"},block={"active_block":{"id":"B"},"next_action":"A","next_action_count":2},proof={},evidence=[])
if __name__=="__main__": unittest.main()

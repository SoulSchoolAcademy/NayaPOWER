#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest
P=Path(__file__).with_name("sender_receiver_readiness.py"); S=importlib.util.spec_from_file_location("sr",P); M=importlib.util.module_from_spec(S); S.loader.exec_module(M)
class T(unittest.TestCase):
    def test_ready(self):
        x=M.evaluate({"capability":True,"authority":True,"consent":True,"scope":["wisdom"],"revocation":True,"idempotency":True,"receipt":True,"persistence":True,"retrieval":True})
        self.assertEqual(x["status"],"READY")
    def test_fail_closed(self):
        x=M.evaluate({"capability":True,"authority":False,"consent":True,"scope":["x"],"revocation":False,"idempotency":True,"receipt":True,"persistence":True,"retrieval":True})
        self.assertEqual(x["status"],"NOT_READY"); self.assertIn("AUTHORITY_NOT_PROVEN",x["failures"])
if __name__=="__main__": unittest.main()

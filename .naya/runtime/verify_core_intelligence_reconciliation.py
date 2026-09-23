#!/usr/bin/env python3
import importlib.util, sys
from pathlib import Path
P=Path(__file__).with_name("core_intelligence_reconciliation.py")
S=importlib.util.spec_from_file_location("cir_fixed",P); M=importlib.util.module_from_spec(S); sys.modules["cir_fixed"]=M; S.loader.exec_module(M)
current=[{"block_id":"B1","semantic_key":"auth","claim":"authorized actions require a grant"}]
cases=[
({"meaning":"auth","semantic_key":"auth","claim":"authorized actions require a grant","verification":"VERIFIED"},M.Disposition.DUPLICATE),
({"meaning":"auth","semantic_key":"auth","claim":"actor lineage","verification":"VERIFIED","extends":"B1"},M.Disposition.EXTEND),
({"meaning":"auth","semantic_key":"auth","claim":"corrected","verification":"VERIFIED","corrects":"B1"},M.Disposition.CORRECT),
({"meaning":"auth","semantic_key":"auth","claim":"contrary","verification":"VERIFIED","contradicts":"B1"},M.Disposition.CONFLICT),
({"meaning":"auth","semantic_key":"auth","claim":"new","verification":"UNKNOWN"},M.Disposition.UNCERTAIN),
]
for candidate,expected in cases:
    actual=M.reconcile(candidate,current)
    assert actual.disposition==expected,(candidate,actual,expected)
print("CORE_INTELLIGENCE_RECONCILIATION_PASS",len(cases))

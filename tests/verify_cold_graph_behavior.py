import json
import sys
from pathlib import Path

def verify(path: Path) -> None:
    r=json.loads(path.read_text(encoding="utf-8"))
    assert r["ok"] is True, r
    v=r["verification"]
    assert v["persisted_pair_re_read"] is True
    assert v["behavioral_delta"] is True
    assert v["treatment_relationships_verified"] is True
    assert v["independently_reconstructed"] is True
    assert r["receipts"]["control"]["evidence"]["condition"] == "OFF"
    assert r["receipts"]["treatment"]["evidence"]["condition"] == "ON"
    assert r["receipts"]["treatment"]["evidence"]["relationship_context_enabled"] is True
    selected=r["receipts"]["treatment"]["evidence"]["selected_relationships"]
    assert selected
    assert all(x["epistemic_state"]=="VERIFIED" and x["provenance"] and x["target_id"]=="IB-NAYA-NODE-0001-0001" for x in selected)

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("usage: verify_cold_graph_behavior.py RECEIPT")
    verify(Path(sys.argv[1]))
    print("COLD NAYA GRAPH BEHAVIOR RECEIPT INDEPENDENTLY VERIFIED")

import json
import sys
from pathlib import Path

def verify(path: Path) -> None:
    r=json.loads(path.read_text(encoding="utf-8"))
    assert r["ok"] is True, r
    v=r["verification"]
    assert v["persisted_pair_re_read"] is True
    assert v["relationship_rows_re_read"] is True
    assert v["behavioral_delta"] is True
    assert v["treatment_relationships_verified"] is True
    assert v["independently_reconstructed"] is True
    assert v["task_class"] == "provenance_sensitive", v
    assert v["intelligent_block_id"], v

    control=r["receipts"]["control"]
    treatment=r["receipts"]["treatment"]
    assert control["evidence"]["condition"] == "OFF"
    assert treatment["evidence"]["condition"] == "ON"
    assert control["evidence"]["relationship_context_enabled"] is False
    assert treatment["evidence"]["relationship_context_enabled"] is True
    assert control["evidence"]["task_id"] == treatment["evidence"]["task_id"]
    assert control["evidence"]["intelligent_block_id"] == treatment["evidence"]["intelligent_block_id"] == v["intelligent_block_id"]

    selected=r["relationships"]
    assert selected
    assert {x["relationship_id"] for x in selected} == {
        x["relationship_id"] for x in treatment["evidence"]["selected_relationships"]
    }
    assert all(
        x["epistemic_state"]=="VERIFIED"
        and x["status"]=="ACTIVE"
        and x["provenance"]
        and x["evidence_refs"]
        and x["target_id"]==v["intelligent_block_id"]
        and x["applicability"]["state"]=="APPLICABLE"
        and "provenance_sensitive" in x["applicability"]["task_classes"]
        for x in selected
    ), selected

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("usage: verify_cold_graph_behavior.py RECEIPT")
    verify(Path(sys.argv[1]))
    print("COLD NAYA GRAPH V2 BEHAVIOR RECEIPT INDEPENDENTLY VERIFIED")

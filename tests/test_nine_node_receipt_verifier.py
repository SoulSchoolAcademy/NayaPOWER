"""Tests the nine-node behavioral-acceptance RECEIPT VERIFIER (not live behavior).

These tests prove verify_receipt() accepts complete receipts and fails closed
on ablations and negative controls. They do not prove the nine nodes behaved
a given way in a live runtime — no live behavioral run has produced a real
receipt yet. The name says what is actually proven.
"""

import copy
from tests.verify_nine_node_behavioral_acceptance import ORDER, verify_receipt

def valid_receipt():
    return {
        "schema":"NAYAPOWER_NINE_NODE_BEHAVIORAL_ACCEPTANCE_V1",
        "node_order":ORDER,
        "nodes":{n:{"status":"SATISFIED","evidence":[f"{n}-evidence"]} for n in ORDER},
        "source_runtime_parity":True,
        "independent_verification":True,
        "authority_inherited":False,
        "unrelated_transfer_refused":True,
    }

def test_complete_receipt_passes():
    assert verify_receipt(valid_receipt()) == []

def test_each_node_ablation_fails_closed():
    for node in ORDER:
        r=copy.deepcopy(valid_receipt())
        del r["nodes"][node]
        assert verify_receipt(r), node

def test_truth_boundary_negative_controls():
    for field,bad in [
        ("source_runtime_parity",False),
        ("independent_verification",False),
        ("authority_inherited",True),
        ("unrelated_transfer_refused",False),
    ]:
        r=valid_receipt(); r[field]=bad
        assert verify_receipt(r), field

import json
from pathlib import Path


def test_causal_learning_experiment_receipt_contract():
    receipt = json.loads(Path("causal-learning-experiment-receipt.json").read_text(encoding="utf-8"))
    assert receipt["schema"] == "NAYANET_CAUSAL_LEARNING_EXPERIMENT_V1"
    assert receipt["target_id"] == "NAYA-NODE-0001"
    assert receipt["learning_id"] == "de0b794b-224b-4d8b-ad1a-3afc6f8d0771"
    assert receipt["control"]["retained_intelligence_used"] is False
    assert receipt["treatment"]["retained_intelligence_used"] is True
    assert receipt["control"]["behavior"] != receipt["treatment"]["behavior"]
    assert receipt["causal_verification"]["causal_assessment"] == "CAUSAL_SUPPORTED"
    assert receipt["causal_verification"]["verification_status"] == "OUTCOME_VERIFIED"
    assert receipt["independent_verification"] is True

 
  
   
 
 
 
 

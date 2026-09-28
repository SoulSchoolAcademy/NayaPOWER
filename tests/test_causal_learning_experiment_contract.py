"""Verifier for the LIVE causal-learning experiment receipt.

CLASSIFICATION OF THE PRIOR FAILURE (Coder 2, 2026-09-28)
---------------------------------------------------------
This test previously read `Path("causal-learning-experiment-receipt.json")`
relative to the CWD and died with FileNotFoundError on every local run.

The violating layer was NOT the implementation and NOT the contract. Both
respective live jobs - `learning-influence-experiment` and
`independent-learning-influence-verification` - SUCCEEDED in run 36445685851.
The layer that was wrong is PLACEMENT/ENVIRONMENT: this is a verifier of LIVE
runtime evidence that lives in the directory pytest collects on every offline
run, where its artifact is legitimately absent.

So it now skips explicitly when the receipt is absent, and asserts in full when
it is present. The skip is not a pass. The assertion logic was extracted into
`verify_causal_learning_experiment_receipt` so that
tests/test_learning_receipt_verifier_bites.py can prove the logic still fails a
forged or degraded receipt. A skip-guard without that proof would be exactly
the "manufacture green" failure mode.

NOT A CAUSAL PROOF. This verifies that a live receipt says the right things.
Whether the causal chain is genuine is a separate question answered only by the
separate `independent-verification` job re-reading persisted state. A receipt
field asserting truth is not evidence of truth.
"""

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
RECEIPT = REPO / "causal-learning-experiment-receipt.json"


def verify_causal_learning_experiment_receipt(receipt: dict) -> None:
    """The causal-learning receipt contract. Every assertion is load-bearing."""
    assert receipt["schema"] == "NAYANET_CAUSAL_LEARNING_EXPERIMENT_V1"
    assert receipt["target_id"] == "NAYA-NODE-0001"
    assert receipt["learning_id"] == "de0b794b-224b-4d8b-ad1a-3afc6f8d0771"
    # Control isolation: control must NOT receive the retained intelligence.
    assert receipt["control"]["retained_intelligence_used"] is False
    # Treatment must receive it.
    assert receipt["treatment"]["retained_intelligence_used"] is True
    # An observable behavioural delta is required, not merely a stored lesson.
    assert receipt["control"]["behavior"] != receipt["treatment"]["behavior"]
    assert receipt["causal_verification"]["causal_assessment"] == "CAUSAL_SUPPORTED"
    assert receipt["causal_verification"]["verification_status"] == "OUTCOME_VERIFIED"
    assert receipt["independent_verification"] is True


def test_causal_learning_experiment_receipt_contract():
    if not RECEIPT.exists():
        pytest.skip(
            "LIVE receipt 'causal-learning-experiment-receipt.json' is absent. This test verifies "
            "LIVE runtime evidence and executes inside "
            ".github/workflows/live-supabase-runtime-proof.yml once the runtime writes it. "
            "It is not satisfiable offline. SKIPPED, not passed."
        )
    verify_causal_learning_experiment_receipt(json.loads(RECEIPT.read_text(encoding="utf-8")))

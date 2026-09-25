from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_verify_cannot_claim_verified_without_observed_outcome_and_evidence():
    source = (ROOT / "NAYANET/HUB/public/assistant-runtime.js").read_text(encoding="utf-8")
    start = source.index("async function verify(sourceId)")
    end = source.index("function style()", start)
    verify = source[start:end]

    assert "OBSERVED_RESULT_REQUIRED" in verify
    assert "INDEPENDENT_EVIDENCE_REF_REQUIRED" in verify
    assert "verification_state:'PENDING_INDEPENDENT_VERIFICATION'" in verify
    assert "verification_state:'VERIFIED'" not in verify

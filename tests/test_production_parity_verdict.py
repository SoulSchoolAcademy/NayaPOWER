"""Tests for tools/production_parity_verdict.py and its workflow wiring.

The parity verdict is signal-only proof machinery: it binds the promoted
source SHA, the production branch tip, and the DEPLOYED_SOURCE_REVISION
stamp read from each deployed function source into a machine-verifiable
verdict. It must never raise, never invent evidence, and never certify
promotion.
"""

from pathlib import Path

import pytest

from tools.production_parity_verdict import (
    SCHEMA,
    STAMPED_FUNCTIONS,
    build_parity_verdict,
    evaluate_function,
    extract_stamp,
)

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "governed-supabase-production-deploy.yml"

PROMOTED = "a" * 40
OLDER = "b" * 40
OTHER = "c" * 40
PROD_TIP = "d" * 40


def _fn(stamp, ancestor=None, path="supabase/functions/x/index.ts"):
    return {"stamp": stamp, "source_path": path, "stamp_is_ancestor_of_promoted": ancestor}


# --- stamp extraction -----------------------------------------------------

def test_extract_stamp_reads_40_hex():
    src = 'const DEPLOYED_SOURCE_REVISION = "%s";' % PROMOTED
    assert extract_stamp(src) == PROMOTED


def test_extract_stamp_reads_unstamped_sentinel():
    assert extract_stamp('const DEPLOYED_SOURCE_REVISION = "UNSTAMPED";') == "UNSTAMPED"


def test_extract_stamp_returns_none_when_missing_or_malformed():
    assert extract_stamp("no stamp here") is None
    assert extract_stamp(None) is None
    assert extract_stamp('const DEPLOYED_SOURCE_REVISION = "short";') is None
    assert extract_stamp(123) is None


# --- per-function verdicts --------------------------------------------------

def test_stamp_equal_to_promoted_is_parity_verified():
    out = evaluate_function(PROMOTED, PROMOTED, True)
    assert out["verdict"] == "PARITY_VERIFIED"


def test_older_ancestor_stamp_is_stale():
    out = evaluate_function(OLDER, PROMOTED, True)
    assert out["verdict"] == "STALE"


def test_non_ancestor_stamp_is_drift():
    out = evaluate_function(OTHER, PROMOTED, False)
    assert out["verdict"] == "DRIFT"


def test_unstamped_sentinel_is_unstamped():
    out = evaluate_function("UNSTAMPED", PROMOTED, None)
    assert out["verdict"] == "UNSTAMPED"


def test_missing_or_malformed_stamp_is_unknown():
    assert evaluate_function(None, PROMOTED, True)["verdict"] == "UNKNOWN"
    assert evaluate_function("garbage", PROMOTED, True)["verdict"] == "UNKNOWN"


def test_unknown_promoted_sha_is_unknown_not_verified():
    out = evaluate_function(PROMOTED, None, True)
    assert out["verdict"] == "UNKNOWN"
    out = evaluate_function(PROMOTED, "not-a-sha", True)
    assert out["verdict"] == "UNKNOWN"


def test_unavailable_ancestry_is_unknown_not_drift():
    out = evaluate_function(OLDER, PROMOTED, None)
    assert out["verdict"] == "UNKNOWN"


# --- receipt assembly -------------------------------------------------------

def test_all_verified_yields_parity_verified():
    receipt = build_parity_verdict(
        promoted_sha=PROMOTED,
        production_tip_sha=PROD_TIP,
        functions={
            "nayanet-cold-runtime-proof": _fn(PROMOTED, True),
            "nayanet-verified-ai-action": _fn(PROMOTED, True),
        },
    )
    assert receipt["schema"] == SCHEMA
    assert receipt["verdict"] == "PARITY_VERIFIED"
    assert receipt["promoted_sha"] == PROMOTED
    assert receipt["production_tip_sha"] == PROD_TIP


def test_overall_is_worst_severity():
    receipt = build_parity_verdict(
        promoted_sha=PROMOTED,
        production_tip_sha=PROD_TIP,
        functions={
            "nayanet-cold-runtime-proof": _fn(PROMOTED, True),
            "nayanet-verified-ai-action": _fn(OTHER, False),
        },
    )
    assert receipt["verdict"] == "DRIFT"
    assert receipt["functions"]["nayanet-cold-runtime-proof"]["verdict"] == "PARITY_VERIFIED"
    assert receipt["functions"]["nayanet-verified-ai-action"]["verdict"] == "DRIFT"


def test_stale_overall_when_production_behind_tip():
    receipt = build_parity_verdict(
        promoted_sha=PROMOTED,
        production_tip_sha=PROD_TIP,
        functions={
            "nayanet-cold-runtime-proof": _fn(OLDER, True),
            "nayanet-verified-ai-action": _fn(OLDER, True),
        },
    )
    assert receipt["verdict"] == "STALE"


def test_no_functions_observed_is_unknown():
    receipt = build_parity_verdict(promoted_sha=PROMOTED, production_tip_sha=PROD_TIP, functions={})
    assert receipt["verdict"] == "UNKNOWN"
    receipt = build_parity_verdict(promoted_sha=PROMOTED)
    assert receipt["verdict"] == "UNKNOWN"


def test_malformed_inputs_never_raise_and_never_verify():
    for bad in (None, "nope", 42, [PROMOTED]):
        receipt = build_parity_verdict(promoted_sha=bad, production_tip_sha=bad, functions=bad, context=bad)
        assert receipt["schema"] == SCHEMA
        assert receipt["verdict"] != "PARITY_VERIFIED"
    receipt = build_parity_verdict(
        promoted_sha=PROMOTED,
        functions={"x": "not-a-mapping", "y": {"stamp": {"nested": 1}}},
    )
    assert receipt["verdict"] == "UNKNOWN"


def test_receipt_never_certifies_promotion():
    receipt = build_parity_verdict(
        promoted_sha=PROMOTED,
        functions={"nayanet-cold-runtime-proof": _fn(PROMOTED, True)},
    )
    boundary = receipt["authority_boundary"]
    assert boundary["certifies_promotion"] is False
    assert boundary["authorizes_deployment"] is False
    assert boundary["signal_only"] is True


def test_context_is_passed_through_sanitized():
    receipt = build_parity_verdict(
        promoted_sha=PROMOTED,
        functions={"nayanet-cold-runtime-proof": _fn(PROMOTED, True)},
        context={"workflow_run_id": 123, "actor": "naya5", "junk": {"deep": 1}, "nothing": None},
    )
    assert receipt["context"]["workflow_run_id"] == 123
    assert receipt["context"]["nothing"] is None
    assert "junk" not in receipt["context"]


def test_stamped_functions_list_matches_stamp_write_seam():
    keys = [k for k, _ in STAMPED_FUNCTIONS]
    assert "nayanet-cold-runtime-proof" in keys
    assert "nayanet-verified-ai-action" in keys


# --- workflow wiring --------------------------------------------------------

def test_workflow_wires_parity_verdict_step_signal_only():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "Emit production parity verdict" in source
    assert "from tools.production_parity_verdict import" in source
    assert "build_parity_verdict" in source
    assert "production-parity-verdict.json" in source
    # Signal-only: runs on every outcome, never fails the build.
    step = source[source.index("Emit production parity verdict"):]
    assert "if: always()" in step
    # The builder is pure; the step does the IO (fetch production branch,
    # read stamped sources, test ancestry) and passes parsed inputs in.
    assert "origin/production" in step
    assert "DEPLOYED_SOURCE_REVISION" in step
    assert '"merge-base"' in step and '"--is-ancestor"' in step


def test_workflow_uploads_parity_verdict_artifact():
    source = WORKFLOW.read_text(encoding="utf-8")
    upload = source[source.index("uses: actions/upload-artifact@v4"):]
    assert "production-parity-verdict.json" in upload
    # Existing receipt paths are untouched.
    assert "production-promotion-receipt.json" in upload
    assert "production-promotion-failure-receipt.json" in upload


def test_parity_step_does_not_touch_handshake_authority():
    source = WORKFLOW.read_text(encoding="utf-8")
    step = source[source.index("Emit production parity verdict"):]
    step = step[: step.index("uses: actions/upload-artifact@v4")]
    # No promotion, no deploy, no ref updates from the signal-only step.
    assert "refs/heads/production" not in step
    assert "git push" not in step
    assert "PROMOTED_AND_PROVEN" not in step

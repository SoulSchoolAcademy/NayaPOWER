"""Guard: a DEPLOYMENT gate must never suppress a PROOF.

Coder 2, 2026-09-28.

WHAT HAPPENED
-------------
PR #880 added the deployed-source parity gate to the `live-connect` job: the
runtime must declare `deployed_source_revision`, or the run is red. That is
correct and it fired exactly as designed.

But it fired at the JOB level, and three downstream jobs declared
`needs: live-connect`:

    independent-connect-verification
    cold-successor
    cold-successor-verification

GitHub Actions SKIPS a job whose `needs` failed. So a missing deploy stamp - a
DEPLOYMENT problem - silently suppressed:

  * the independent verification of the CONNECT receipt, and
  * the cold-successor proof and its independent re-verification.

That is the North Star's hardest requirement being switched off by an unrelated
gate. I caused it, and the fix is structural:

  * the artifact is uploaded under `if: always()`, so the input exists even on
    failure, and therefore
  * the proof jobs run under `if: always()` too.

A DEPLOYMENT gate must fail the workflow. It must not delete evidence.

WHAT IS ASSERTED HERE
  1. The parity gate is still present and still runs the detector.
  2. Every job that consumes a `live-connect` artifact also verifies or extends
     a proof, and therefore runs under `if: always()`.
  3. The gate itself is NOT weakened: the detector must remain in the workflow.
"""

import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
WORKFLOW = REPO / ".github" / "workflows" / "live-supabase-runtime-proof.yml"

# Jobs that consume live-connect output to PROVE something. If the deployment
# gate goes red, these must still run - that is the whole point.
PROOF_JOBS_CONSUMING_LIVE_CONNECT = (
    "independent-connect-verification",
    "cold-successor",
    "cold-successor-verification",
)


@pytest.fixture(scope="module")
def jobs() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))["jobs"]


def test_the_parity_gate_is_still_present(jobs):
    """Never let a later edit quietly remove the enforcement this exists under."""
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "verify-deployed-runtime-parity.py" in source, "the parity gate has been removed"
    assert "record-deployed-runtime-observation.py" in source, "observations must still be generated"
    assert "live-connect" in jobs


def test_the_gate_still_records_evidence_before_it_fails(jobs):
    steps = jobs["live-connect"]["steps"]
    names = [s.get("name", s.get("uses", "")) for s in steps]
    record = next(i for i, n in enumerate(names) if "Record deployed-runtime observation" in n)
    verdict = next(i for i, n in enumerate(names) if "Fail if the deployed artifact" in n)
    assert record < verdict, "the observation must be recorded before the verdict can fail"


def test_proof_jobs_are_not_suppressed_by_the_deployment_gate(jobs):
    for job in PROOF_JOBS_CONSUMING_LIVE_CONNECT:
        assert job in jobs, f"{job} disappeared from the workflow"
        assert jobs[job].get("if") == "always()", (
            f"{job} is gated behind live-connect and will be SKIPPED when the deployment "
            f"parity gate fails. That deletes proof evidence for a DEPLOYMENT problem. "
            f"It must run under if: always()."
        )


def test_proof_jobs_still_declare_their_dependency(jobs):
    """
    `if: always()` must not become a way to run out of order. The dependency is
    still declared; it just no longer suppresses the job.
    """
    assert jobs["independent-connect-verification"]["needs"] == "live-connect"
    assert jobs["cold-successor"]["needs"] == "live-connect"
    assert jobs["cold-successor-verification"]["needs"] == "cold-successor"


def test_proof_jobs_download_the_artifact_they_need(jobs):
    """
    Running under if: always() is only safe because the artifact is uploaded even
    when the job fails. Assert both halves together, so neither can be removed
    alone.
    """
    live_connect = jobs["live-connect"]
    upload = [s for s in live_connect["steps"] if str(s.get("uses", "")).startswith("actions/upload-artifact")]
    assert upload, "live-connect must still upload its artifacts"
    assert upload[0].get("if") == "always()", (
        "the artifact upload must run even when the parity gate fails, or the proof jobs "
        "would run with no input"
    )
    source = WORKFLOW.read_text(encoding="utf-8")
    assert re.search(r"if:\s*always\(\)", source), "workflow should use if: always() guards"

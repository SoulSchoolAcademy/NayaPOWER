"""Integration tests: the REAL boot path enforces the activation checklist.

These tests call kernel.protocol.cold_start_gate.run_cold_start — the
actual cold-start boot decision — with fixture repo roots, and prove it
rejects:
  - a missing lesson (13 of 14 in the fixture curriculum)
  - a stale lesson hash (tampered lesson bytes in the fixture)
  - an unreadable canonical file (missing curriculum -> fail closed)
  - drifted V2 bytes (fail closed)
  - a forged claim hash
  - a failed comprehension attestation (claim admits a sub-threshold score)

They are integration tests, not unit tests of the checker: if the wiring
in run_cold_start is removed, the negative cases PASS (the boot decision
no longer sees the checklist), so the suite fails. The positive case
proves the gate still boots when the checklist is intact.

Fixtures copy the REAL canonical artifacts from the repo checkout, so the
pins and the bytes under test are the live ones.
"""

import json
import os
import shutil
import sys
import tempfile

import pytest

from kernel.protocol.read_receipt import issue_receipt
from kernel.protocol.cold_start_gate import (
    ColdStartState,
    run_cold_start,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
import activation_checklist as ac  # noqa: E402

CORRECT = {
    "q1": "Shawn Vibert",
    "q2": "production deploys, credentials and money, destructive actions, "
          "ratification, security and privacy",
    "q3": "No, never",
    "q4": "9.0",
    "q5": "independent evidence and proof",
}

CURRICULUM_FILES = [
    "NAYA-ACTIVATION/thinking-curriculum.json",
    "NAYA-ACTIVATION/THINKING-CURRICULUM-V1.md",
]
ALL_ARTIFACTS = CURRICULUM_FILES + list(ac.V2_FILES)
ALL_IDS = ["L%d" % i for i in range(1, 15)]


@pytest.fixture()
def fixture_root():
    """Temp dir holding byte-identical copies of the real canonical
    artifacts. Yields the path; cleaned up after the test."""
    tmp = tempfile.mkdtemp(prefix="boot-wiring-")
    for rel in ALL_ARTIFACTS:
        src = os.path.join(REPO_ROOT, *rel.split("/"))
        dst = os.path.join(tmp, *rel.split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


def _rewrite_curriculum(root, mutate):
    path = os.path.join(root, *ac.CURRICULUM_JSON.split("/"))
    with open(path, encoding="utf-8") as f:
        curriculum = json.load(f)
    mutate(curriculum)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(curriculum, f, indent=2, ensure_ascii=False)


def _good_state(repo_root, claim=None):
    return ColdStartState(
        agent_id="naya-9",
        human_director="Shawn Vibert",
        lane="verify",
        authority_summary="Protected gates: production deploys, "
                          "credentials/money, destructive actions, "
                          "ratification, security/privacy. "
                          "Law 11 (do no harm) is the only hard law.",
        current_truth_location="mission-state feed #2154 and current main",
        next_action="verify the activation wiring",
        receipt=issue_receipt("naya-9", CORRECT),
        repo_root=repo_root,
        activation_claim=claim,
    )


def _good_claim(root):
    """A checklist claim that is byte-faithful to the fixture artifacts."""
    canonical, err = ac.load_canonical(root)
    assert err == "", err
    return {
        "agent_id": "naya-test",
        "lessons": [{"lesson_id": lid,
                     "sha256": canonical["lesson_hashes"][lid]}
                    for lid in ALL_IDS],
        "v2": dict(canonical["v2_hashes"]),
    }


def _blocked_with(result, fragment):
    assert not result.passed, \
        "boot passed but should have been blocked: %r" % (result.failures,)
    assert any(fragment in f for f in result.failures), result.failures


# ---------- positive controls ----------

def test_boot_passes_when_checklist_intact(fixture_root):
    result = run_cold_start(_good_state(fixture_root))
    assert result.passed, result.failures


def test_boot_passes_against_real_checkout():
    # The wiring is live on the default path too: a complete state with no
    # repo_root override boots against this checkout's canonical artifacts.
    result = run_cold_start(_good_state(None))
    assert result.passed, result.failures


def test_boot_accepts_consistent_comprehension_attestation(fixture_root):
    claim = _good_claim(fixture_root)
    claim["comprehension"] = {lid: 8 for lid in ALL_IDS}
    result = run_cold_start(_good_state(fixture_root, claim))
    assert result.passed, result.failures


# ---------- negative controls: the checklist blocks the boot ----------

def test_boot_blocks_missing_lesson(fixture_root):
    _rewrite_curriculum(
        fixture_root,
        lambda c: c.__setitem__(
            "lessons",
            [e for e in c["lessons"] if e.get("lesson_id") != "L14"]))
    result = run_cold_start(_good_state(fixture_root))
    _blocked_with(result, "LESSON_MISSING")


def test_boot_blocks_stale_lesson_hash(fixture_root):
    def tamper(curriculum):
        for e in curriculum["lessons"]:
            if e.get("lesson_id") == "L3":
                e["test_problem"] += " (drifted)"
    _rewrite_curriculum(fixture_root, tamper)
    result = run_cold_start(_good_state(fixture_root))
    _blocked_with(result, "CURRICULUM_STALE")


def test_boot_blocks_unreadable_canonical_file(fixture_root):
    os.unlink(os.path.join(fixture_root,
                           *ac.CURRICULUM_JSON.split("/")))
    result = run_cold_start(_good_state(fixture_root))
    _blocked_with(result, "fail closed")


def test_boot_blocks_drifted_v2(fixture_root):
    p = os.path.join(fixture_root, *ac.V2_FILES[1].split("/"))
    with open(p, "ab") as f:
        f.write(b"\n<!-- drifted -->\n")
    result = run_cold_start(_good_state(fixture_root))
    _blocked_with(result, "V2_STALE")


def test_boot_rejects_forged_claim_hash(fixture_root):
    claim = _good_claim(fixture_root)
    claim["lessons"][1]["sha256"] = "0" * 64  # L2 forged
    result = run_cold_start(_good_state(fixture_root, claim))
    _blocked_with(result, "LESSON_FINGERPRINT_MISMATCH")


def test_boot_rejects_partial_claim(fixture_root):
    claim = _good_claim(fixture_root)
    claim["lessons"] = claim["lessons"][:13]  # L14 dropped from the claim
    result = run_cold_start(_good_state(fixture_root, claim))
    _blocked_with(result, "LESSON_MISSING")


def test_boot_blocks_failed_comprehension_attestation(fixture_root):
    claim = _good_claim(fixture_root)
    claim["comprehension"] = {lid: 8 for lid in ALL_IDS}
    claim["comprehension"]["L4"] = 5  # the claim itself admits failure
    result = run_cold_start(_good_state(fixture_root, claim))
    _blocked_with(result, "COMPREHENSION_ATTESTATION_BELOW_THRESHOLD")


def test_boot_blocks_unknown_lesson_in_attestation(fixture_root):
    claim = _good_claim(fixture_root)
    claim["comprehension"] = {"L99": 9}
    result = run_cold_start(_good_state(fixture_root, claim))
    _blocked_with(result, "COMPREHENSION_ATTESTATION_UNKNOWN_LESSON")

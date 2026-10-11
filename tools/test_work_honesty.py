#!/usr/bin/env python3
"""Adversarial tests for work_honesty.py (UD-08).

Positive: real completed work verifies end to end.
Negative: every dishonest or sloppy path is refused with the right code.
A green suite that never refuses anything would prove nothing — the negative
cases are the point.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from work_honesty import (  # noqa: E402
    WorkHonestyTracker, Identity, TransitionRefused,
    AUTHORIZED, IN_PROGRESS, CLAIMED_DONE, VERIFIED_DONE, BLOCKED,
    NO_ARTIFACT, SELF_VERIFICATION, NO_VERIFICATION_EVIDENCE,
    BLOCKED_CANNOT_COMPLETE, INVALID_TRANSITION, NO_AUTHORITY,
    NO_START_EVIDENCE, NO_BLOCKER_RECORD,
)


class Clock:
    def __init__(self, t=1_000_000.0):
        self.t = t

    def __call__(self):
        return self.t

    def advance(self, s):
        self.t += s


DOER = Identity("naya4", "sess-doer-1")
OTHER = Identity("naya2", "sess-verifier-9")
IMPOSTOR = Identity("naya9", "sess-doer-1")  # renamed seat, same session


def fresh():
    return WorkHonestyTracker(clock=Clock())


def expect_refused(fn, code):
    try:
        fn()
    except TransitionRefused as e:
        assert e.code == code, f"expected {code}, got {e.code}: {e.detail}"
        return
    raise AssertionError(f"expected refusal {code}, but the call succeeded")


# ------------------------------------------------------------- positive ---
def test_happy_path():
    tr = fresh()
    tr.authorize("w1", "Build the thing", "director-order-7", DOER)
    tr.start("w1", DOER, "scaffold module")
    tr.claim_done("w1", DOER, artifact_handle="sha256:abc123",
                  artifact_pointer="branch naya4/x")
    tr.verify("w1", OTHER, "PASS", "ran 12/12 tests on exact bytes")
    item = tr._get("w1")
    assert item.state == VERIFIED_DONE, item.state
    assert tr.progress_credit("w1") == 3  # three forward transitions


def test_verify_fail_returns_to_progress():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    tr.claim_done("w1", DOER, artifact_handle="sha256:x")
    tr.verify("w1", OTHER, "FAIL", "test 4 of 12 red on re-run")
    item = tr._get("w1")
    assert item.state == IN_PROGRESS
    assert item.failed_verifications == 1


def test_block_unblock_resume_and_finish():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    tr.block("w1", DOER, "waiting on API key", owner="shawn")
    assert tr._get("w1").state == BLOCKED
    tr.unblock("w1", DOER, "key arrived via secure flow")
    tr.claim_done("w1", DOER, artifact_handle="sha256:x")
    tr.verify("w1", OTHER, "PASS", "verified artifact matches claim")
    assert tr._get("w1").state == VERIFIED_DONE


# ------------------------------------------------------------- negative ---
def test_claim_without_artifact_refused():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    expect_refused(lambda: tr.claim_done("w1", DOER, artifact_handle="  "),
                   NO_ARTIFACT)
    assert tr._get("w1").state == IN_PROGRESS  # refusal changes nothing


def test_false_done_claim_refused_end_to_end():
    # The headline demonstration: "trust me, it's done" with no artifact.
    tr = fresh()
    tr.authorize("w1", "Ship feature", "auth", DOER)
    tr.start("w1", DOER, "wrote some code")
    expect_refused(lambda: tr.claim_done("w1", DOER, artifact_handle=""),
                   NO_ARTIFACT)
    expect_refused(lambda: tr.claim_done("w1", DOER, artifact_handle=None),
                   NO_ARTIFACT)
    assert tr.progress_credit("w1") == 1  # only the start counts


def test_self_verify_same_seat_refused():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    tr.claim_done("w1", DOER, artifact_handle="sha256:x")
    expect_refused(lambda: tr.verify("w1", DOER, "PASS", "looks good"),
                   SELF_VERIFICATION)


def test_self_verify_renamed_seat_same_session_refused():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    tr.claim_done("w1", DOER, artifact_handle="sha256:x")
    expect_refused(lambda: tr.verify("w1", IMPOSTOR, "PASS", "independent!"),
                   SELF_VERIFICATION)


def test_verify_without_evidence_refused():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    tr.claim_done("w1", DOER, artifact_handle="sha256:x")
    expect_refused(lambda: tr.verify("w1", OTHER, "PASS", "   "),
                   NO_VERIFICATION_EVIDENCE)


def test_blocked_cannot_claim_done():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    tr.block("w1", DOER, "upstream down", owner="naya1")
    expect_refused(lambda: tr.claim_done("w1", DOER, artifact_handle="sha256:x"),
                   BLOCKED_CANNOT_COMPLETE)


def test_invalid_transitions_refused():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    # skip straight to verify
    expect_refused(lambda: tr.verify("w1", OTHER, "PASS", "ev"),
                   INVALID_TRANSITION)
    # skip straight to claim
    expect_refused(lambda: tr.claim_done("w1", DOER, artifact_handle="sha256:x"),
                   INVALID_TRANSITION)
    # double start
    tr.start("w1", DOER, "act")
    expect_refused(lambda: tr.start("w1", DOER, "act again"),
                   INVALID_TRANSITION)


def test_authorize_without_authority_refused():
    tr = fresh()
    expect_refused(lambda: tr.authorize("w1", "t", "", DOER), NO_AUTHORITY)


def test_start_without_action_refused():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    expect_refused(lambda: tr.start("w1", DOER, "   "), NO_START_EVIDENCE)


def test_block_without_record_refused():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    expect_refused(lambda: tr.block("w1", DOER, "   "), NO_BLOCKER_RECORD)


# ------------------------------------------------------------------ audit ---
def test_stalled_flagged():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    tr._clock.advance(90000)  # > 24h stall window, no evidence movement
    flags = tr.audit()["flags"]
    assert flags.get("w1") == ["STALLED"], flags


def test_blocked_never_stalled():
    # A correct refusal is not a stall.
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    tr.block("w1", DOER, "waiting on key", owner="shawn")
    tr._clock.advance(90000)
    flags = tr.audit()["flags"]
    assert "STALLED" not in flags.get("w1", []), flags


def test_unverified_claim_flagged_not_done():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    tr.claim_done("w1", DOER, artifact_handle="sha256:x")
    tr._clock.advance(90000)
    flags = tr.audit()["flags"]
    assert "UNVERIFIED_CLAIM" in flags.get("w1", []), flags
    assert tr._get("w1").state == CLAIMED_DONE  # still not done


def test_starved_flagged():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr._clock.advance(200000)  # > 48h starve window, never started
    flags = tr.audit()["flags"]
    assert "STARVED" in flags.get("w1", []), flags


def test_heartbeat_earns_nothing():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    before = tr.progress_credit("w1")
    for _ in range(1000):
        tr.heartbeat("w1", DOER, "still working")
    assert tr.progress_credit("w1") == before == 1
    assert tr._get("w1").state == IN_PROGRESS  # motion, not movement


def test_deadlock_cycle_detected():
    tr = fresh()
    for wid in ("a", "b"):
        tr.authorize(wid, "t", "auth", DOER)
        tr.start(wid, DOER, "act")
    tr.block("a", DOER, "needs b", owner="x", blocked_by_item="b")
    tr.block("b", DOER, "needs a", owner="x", blocked_by_item="a")
    flags = tr.audit()["flags"]
    assert "DEADLOCK_CYCLE" in flags.get("a", []), flags
    assert "DEADLOCK_CYCLE" in flags.get("b", []), flags


def test_livelock_suspect():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    tr.start("w1", DOER, "act")
    for i in range(3):
        tr.claim_done("w1", DOER, artifact_handle=f"sha256:try{i}")
        tr.verify("w1", OTHER, "FAIL", f"hole found, round {i}")
    flags = tr.audit()["flags"]
    assert "LIVELOCK_SUSPECT" in flags.get("w1", []), flags


def test_fairness_and_progress_reported_independently():
    tr = fresh()
    tr.authorize("w1", "t", "auth", DOER)
    for _ in range(5):
        tr.record_selection("w1")  # chosen often...
    # ...but never started: fair opportunity, zero progress.
    report = tr.audit()
    assert "progress" in report and "fairness" in report
    f = next(x for x in report["fairness"] if x["item"] == "w1")
    assert f["selections"] == 5 and f["advancements"] == 0
    p = next(x for x in report["progress"] if x["item"] == "w1")
    assert p["progress_credit"] == 0


def test_audit_does_not_claim():
    report = fresh().audit()
    assert "does_not_claim" in report


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS {name}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  FAIL {name}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} green")
    sys.exit(1 if failed else 0)

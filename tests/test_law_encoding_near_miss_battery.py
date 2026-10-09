"""Near-miss adversarial battery for the 2026-10-09 law-encoding batch.

Reconstruction of the independent validator's 17 near-miss probes
(#1354 comment 6086185213): 12 probes that HELD (failed closed on the
original bytes) + 5 evasions that must now FAIL CLOSED after the
hardening pass. Every fixture in this battery asserts fail-closed —
exit code 1 and pass == False — through the real CLI, exactly the way
the validator ran them.

Runnable with plain python3 (no pytest required):
    python3 tests/test_law_encoding_near_miss_battery.py
Also pytest-compatible (plain assert functions).

Held probes are permanent regression guards: they must fail closed on
every future change. Evasion probes pin the five closed holes.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"

NOW = "2026-10-09T17:35:00Z"
A40 = "a" * 40
B40 = "b" * 40
TIP = "4" * 40


def run_check(module: str, record) -> dict:
    """Run a check's CLI. `record` may be a dict/list or a raw string."""
    payload = record if isinstance(record, str) else json.dumps(record)
    proc = subprocess.run(
        [sys.executable, str(CHECKS / f"{module}.py"), "--record", payload, "--json"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        data = {"pass": None}
    return {"exit": proc.returncode, "pass": data.get("pass"), "reasons": data.get("reasons")}


def assert_fail_closed(module: str, record, label: str) -> None:
    r = run_check(module, record)
    assert r["exit"] == 1, f"{label}: CLI exited {r['exit']}, expected 1"
    assert r["pass"] is False, f"{label}: pass={r['pass']}, expected False"


# ============================================================ HELD (12)
def test_nm01_instant_activation_garbage_json():
    assert_fail_closed("instant_activation", "not json at all", "garbage JSON")


def test_nm02_instant_activation_queued_direct_capture():
    # The core prohibition: direct capture, fully recorded, still queued.
    assert_fail_closed("instant_activation", {
        "request": "smart note this", "requester": "shawn",
        "request_type": "capture", "disposition": "queued",
        "queued_for_verification": True, "activated_at": NOW,
    }, "queued direct capture")


def test_nm03_triple_a_string_boolean_demonstrated():
    # "true" is a string, not True — fail closed on shape.
    assert_fail_closed("triple_a", {
        "deliverable": "x", "claimed": "done", "demonstrated": "true",
        "evidence_ref": "e", "evidence_verified_exists": True,
        "builder": "naya5", "scorer": "naya2",
    }, 'string-boolean demonstrated "true"')


def test_nm04_triple_a_string_boolean_evidence():
    assert_fail_closed("triple_a", {
        "deliverable": "x", "claimed": "done", "demonstrated": True,
        "evidence_ref": "e", "evidence_verified_exists": "true",
        "builder": "naya5", "scorer": "naya2",
    }, 'string-boolean evidence_verified_exists "true"')


def test_nm05_triple_a_anonymous_scorer():
    assert_fail_closed("triple_a", {
        "deliverable": "x", "claimed": "awesome", "demonstrated": True,
        "evidence_ref": "e", "evidence_verified_exists": True,
        "builder": "naya5", "scorer": "",
    }, "anonymous scorer")


def test_nm06_naya_identity_trailing_space_trigger():
    # Whitespace padding must not dodge the ban (strip normalizes).
    assert_fail_closed("naya_identity", {
        "lesson": "l", "captured": True,
        "capture_trigger": "shawn_said_capture_that ",
        "shared_with_team": True, "share_surface": "#1354",
    }, "trailing-space dependent trigger")


def test_nm07_delivery_boundary_non_dict_record():
    assert_fail_closed("delivery_boundary", [1, 2], "non-dict record")


def test_nm08_delivery_boundary_string_boolean_invokes():
    assert_fail_closed("delivery_boundary", {
        "mechanism": "tools/g.py", "claimed_status": "enforced",
        "delivery_binding": {
            "workflow_file": ".github/workflows/x.yml",
            "triggers_on": ["pull_request_required"],
            "invokes_gate": "true",
            "binding_verified_at": NOW,
        },
    }, 'string-boolean invokes_gate "true"')


def test_nm09_pr_resolution_uppercase_prefix_basis():
    # Case must not dodge the ban (lowercased before match).
    assert_fail_closed("pr_resolution", {
        "pr": 1998, "disposition": "rejected", "basis": "BRANCH_PREFIX",
        "evidence": "branch starts with naya5/",
    }, "uppercase branch_prefix basis")


def test_nm10_duplicate_pr_blobs_abbreviated_sha():
    assert_fail_closed("duplicate_pr_blobs", {
        "pr": 1998, "disposition": "merged", "main_tip_sha": TIP,
        "blob_comparison": [
            {"path": "tools/g.py", "pr_blob": "abc123", "main_blob": A40,
             "identical": False, "reverts_main": False},
        ],
    }, "abbreviated SHA")


def test_nm11_duplicate_pr_blobs_identical_math_mismatch():
    assert_fail_closed("duplicate_pr_blobs", {
        "pr": 1998, "disposition": "closed_as_duplicate", "main_tip_sha": TIP,
        "blob_comparison": [
            {"path": "tools/g.py", "pr_blob": B40, "main_blob": A40,
             "identical": True, "reverts_main": False},
        ],
    }, "identical claim contradicting blob math")


def test_nm12_ingest_boundary_heuristic_overwrites_authoritative():
    assert_fail_closed("ingest_boundary", {
        "existing": {"status": "authoritative", "score": 9.0,
                     "as_of": "2026-10-09T16:00:00Z", "pinned": False},
        "point": {"status": "heuristic", "score": 2.0,
                  "as_of": "2026-10-09T17:00:00Z", "source": "evil"},
        "ingest_action": "wrote", "now": NOW,
    }, "heuristic write over authoritative state")


# ============================================ EVASIONS, NOW CLOSED (5)
def test_nm13_instant_activation_empty_request_queued():
    # Evasion 1: empty request text -> classified "non-direct" -> QUEUED passed.
    assert_fail_closed("instant_activation", {
        "request": "", "requester": "shawn", "request_type": "capture",
        "disposition": "queued", "queued_for_verification": True,
        "activated_at": NOW,
    }, "empty request on direct capture with queued disposition")


def test_nm14_instant_activation_unparseable_timestamp():
    # Evasion 2: activated_at "soon" passed on presence alone.
    assert_fail_closed("instant_activation", {
        "request": "smart note this", "requester": "shawn",
        "request_type": "capture", "disposition": "activated",
        "queued_for_verification": False, "activated_at": "soon",
    }, 'activated_at "soon"')


def test_nm15_triple_a_unnamed_builder_self_scored():
    # Evasion 3: empty builder skipped scorer==builder -> self-score passed.
    assert_fail_closed("triple_a", {
        "deliverable": "x", "claimed": "done", "demonstrated": True,
        "evidence_ref": "e", "evidence_verified_exists": True,
        "builder": "", "scorer": "naya5",
    }, "unnamed builder, self-scored")


def test_nm16_naya_identity_reworded_trigger():
    # Evasion 4: "Shawn said capture that" (spaces) evaded the exact match.
    assert_fail_closed("naya_identity", {
        "lesson": "l", "captured": True,
        "capture_trigger": "Shawn said capture that",
        "shared_with_team": True, "share_surface": "#1354",
    }, "reworded dependent trigger")


def test_nm17_duplicate_pr_blobs_omitted_reverts_main():
    # Evasion 5: omitted reverts_main passed silently as "delta, no revert".
    assert_fail_closed("duplicate_pr_blobs", {
        "pr": 1998, "disposition": "closed_as_superseded", "main_tip_sha": TIP,
        "blob_comparison": [
            {"path": "tools/g.py", "pr_blob": B40, "main_blob": A40,
             "identical": False},
        ],
    }, "omitted reverts_main")


# ---------------------------------------------------------------- runner
def main() -> int:
    fns = sorted((n, f) for n, f in globals().items()
                 if n.startswith("test_") and callable(f))
    failures = []
    for name, fn in fns:
        try:
            fn()
            print(f"  ok {name}")
        except AssertionError as e:
            failures.append(name)
            print(f"  FAIL {name}: {e}")
        except Exception as e:  # noqa: BLE001
            failures.append(name)
            print(f"  ERROR {name}: {type(e).__name__}: {e}")
    print(f"\n{len(fns) - len(failures)}/{len(fns)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

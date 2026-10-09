"""Tests for the 2026-10-09 law-encoding batch.

Every law encoded this batch gets the same proof contract:
  - a VIOLATING fixture makes the check FAIL (the encoding fires), and
  - an HONORING fixture makes the check PASS (the encoding stays quiet).

Runnable with plain python3 (no pytest required):
    python3 tests/test_law_encoding_20261009.py
Also pytest-compatible (plain assert functions).

Covers:
  - instant_activation.py  (Verification Law)
  - triple_a.py            (Triple-A Excellence)
  - naya_identity.py       (SN-0732)
  - delivery_boundary.py   (SN-0733)
  - predicate_vs_perimeter.py (predicate!=perimeter)
  - pr_resolution.py       (SN-0734)
  - duplicate_pr_blobs.py  (SN-0735)
  - ingest_boundary.py     (ingest-boundary law)
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import (  # noqa: E402
    delivery_boundary,
    duplicate_pr_blobs,
    ingest_boundary,
    instant_activation,
    naya_identity,
    pr_resolution,
    predicate_vs_perimeter,
    triple_a,
)

NOW = "2026-10-09T17:35:00Z"


# ------------------------------------------------------- Verification Law
def _good_capture(**over):
    rec = {
        "request": "smart note this",
        "requester": "shawn",
        "request_type": "capture",
        "disposition": "activated",
        "queued_for_verification": False,
        "activated_at": NOW,
    }
    rec.update(over)
    return rec


def test_verification_law_honors_instant_activation():
    r = instant_activation.check(_good_capture())
    assert r["pass"] is True, r["reasons"]


def test_verification_law_fires_on_queued_direct_request():
    # The old backwards logic: treating Shawn's verified word as unverified input.
    r = instant_activation.check(_good_capture(
        disposition="queued", queued_for_verification=True))
    assert r["pass"] is False
    assert any("verified word" in x for x in r["reasons"])


def test_verification_law_fires_on_non_activated_disposition():
    r = instant_activation.check(_good_capture(disposition="pending_review"))
    assert r["pass"] is False
    assert any("INSTANT" in x for x in r["reasons"])


def test_verification_law_fires_on_missing_activation_time():
    r = instant_activation.check(_good_capture(activated_at=""))
    assert r["pass"] is False


def test_verification_law_user_capture_also_instant():
    r = instant_activation.check(_good_capture(requester="user"))
    assert r["pass"] is True, r["reasons"]


# ------------------------------------------------------- Triple-A Excellence
def _good_deliverable(**over):
    rec = {
        "deliverable": "law-encoding batch 1",
        "claimed": "done",
        "demonstrated": True,
        "evidence_ref": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-999",
        "evidence_verified_exists": True,
        "builder": "naya5",
        "scorer": "naya2",
    }
    rec.update(over)
    return rec


def test_triple_a_honors_demonstrated_independent():
    r = triple_a.check(_good_deliverable())
    assert r["pass"] is True, r["reasons"]


def test_triple_a_fires_on_promise_not_proof():
    # claimed done but not demonstrated: a promise, not proof.
    r = triple_a.check(_good_deliverable(demonstrated=False))
    assert r["pass"] is False
    assert any("promise" in x for x in r["reasons"])


def test_triple_a_fires_on_unverified_evidence_link():
    r = triple_a.check(_good_deliverable(evidence_verified_exists=False))
    assert r["pass"] is False
    assert any("never manufacture" in x for x in r["reasons"])


def test_triple_a_fires_on_self_scoring():
    # 10/10 is never self-declared.
    r = triple_a.check(_good_deliverable(scorer="naya5"))
    assert r["pass"] is False
    assert any("self-declared" in x for x in r["reasons"])


def test_triple_a_fires_on_missing_evidence():
    r = triple_a.check(_good_deliverable(evidence_ref=""))
    assert r["pass"] is False


# ------------------------------------------------------- SN-0732 identity
def _good_lesson(**over):
    rec = {
        "lesson": "predicate!=perimeter: local fixture passes do not establish enforcement",
        "captured": True,
        "capture_trigger": "proactive",
        "shared_with_team": True,
        "share_surface": "#1354",
    }
    rec.update(over)
    return rec


def test_sn0732_honors_proactive_shared_lesson():
    r = naya_identity.check(_good_lesson())
    assert r["pass"] is True, r["reasons"]


def test_sn0732_fires_when_shawn_had_to_say_capture_that():
    # Identity not compounded: needed Shawn to say it.
    r = naya_identity.check(_good_lesson(capture_trigger="shawn_said_capture_that"))
    assert r["pass"] is False
    assert any("not compounded" in x for x in r["reasons"])


def test_sn0732_fires_on_captured_but_unshared():
    r = naya_identity.check(_good_lesson(shared_with_team=False))
    assert r["pass"] is False
    assert any("every Naya's lesson" in x for x in r["reasons"])


def test_sn0732_fires_on_empty_lesson():
    r = naya_identity.check(_good_lesson(lesson=""))
    assert r["pass"] is False


# ------------------------------------------------------- SN-0733 delivery boundary
def _good_mechanism(**over):
    rec = {
        "mechanism": "tools/activation_gate.py",
        "claimed_status": "enforced",
        "delivery_binding": {
            "workflow_file": ".github/workflows/activation-gate.yml",
            "triggers_on": ["pull_request_required"],
            "invokes_gate": True,
            "binding_verified_at": NOW,
        },
    }
    rec.update(over)
    return rec


def test_sn0733_honors_bound_mechanism():
    r = delivery_boundary.check(_good_mechanism())
    assert r["pass"] is True, r["reasons"]


def test_sn0733_honors_honest_candidate():
    # CANDIDATE is an honest state — the adoption gap made visible.
    r = delivery_boundary.check(_good_mechanism(
        claimed_status="candidate", delivery_binding=None))
    assert r["pass"] is True, r["reasons"]


def test_sn0733_fires_on_enforced_without_binding():
    # The ADOPTION GAP: gate exists, nothing on the delivery path invokes it.
    r = delivery_boundary.check(_good_mechanism(delivery_binding=None))
    assert r["pass"] is False
    assert any("delivery boundary" in x for x in r["reasons"])


def test_sn0733_fires_on_branch_only_workflow():
    rec = _good_mechanism()
    rec["delivery_binding"]["triggers_on"] = ["branch_push"]
    r = delivery_boundary.check(rec)
    assert r["pass"] is False
    assert any("ADOPTION GAP" in x for x in r["reasons"])


def test_sn0733_fires_when_workflow_does_not_invoke_gate():
    rec = _good_mechanism()
    rec["delivery_binding"]["invokes_gate"] = False
    r = delivery_boundary.check(rec)
    assert r["pass"] is False
    assert any("decoration" in x for x in r["reasons"])


# ------------------------------------------------------- predicate!=perimeter
def _good_claim(**over):
    rec = {
        "checker": "tools/activation_gate.py::check",
        "predicate_result": "pass",
        "claimed": "enforced",
        "delivery_wired": True,
        "wiring_evidence": "run 37959342664 / job 1042 on push to main",
    }
    rec.update(over)
    return rec


def test_predicate_perimeter_honors_wired_enforcement():
    r = predicate_vs_perimeter.check(_good_claim())
    assert r["pass"] is True, r["reasons"]


def test_predicate_perimeter_honors_honest_unwired_label():
    r = predicate_vs_perimeter.check(_good_claim(
        claimed="predicate_only", delivery_wired=False, wiring_evidence=""))
    assert r["pass"] is True, r["reasons"]


def test_predicate_perimeter_fires_on_unwired_enforced_claim():
    # The exact false-acceptance the law kills: passing predicate, no wiring,
    # claimed enforced.
    r = predicate_vs_perimeter.check(_good_claim(
        delivery_wired=False, wiring_evidence=""))
    assert r["pass"] is False
    assert any("predicate≠perimeter" in x for x in r["reasons"])


def test_predicate_perimeter_fires_on_missing_wiring_evidence():
    r = predicate_vs_perimeter.check(_good_claim(wiring_evidence=""))
    assert r["pass"] is False


def test_predicate_perimeter_fires_on_failing_predicate_claimed_enforced():
    r = predicate_vs_perimeter.check(_good_claim(predicate_result="fail"))
    assert r["pass"] is False


# ------------------------------------------------------- SN-0734 PR resolution
def _good_pr(**over):
    rec = {
        "pr": 1998,
        "disposition": "rejected",
        "basis": "content_analysis",
        "evidence": "weakens gate: NaN passes the check; #2005 fixed the fixture correctly",
    }
    rec.update(over)
    return rec


def test_sn0734_honors_content_basis_disposition():
    r = pr_resolution.check(_good_pr())
    assert r["pass"] is True, r["reasons"]


def test_sn0734_fires_on_branch_prefix_basis():
    # Prefixes collide across lanes; content decides.
    r = pr_resolution.check(_good_pr(basis="branch_prefix",
                                     evidence="branch starts with naya5/"))
    assert r["pass"] is False
    assert any("collide" in x for x in r["reasons"])


def test_sn0734_fires_on_assertion_without_evidence():
    r = pr_resolution.check(_good_pr(evidence=""))
    assert r["pass"] is False
    assert any("assertion" in x for x in r["reasons"])


def test_sn0734_fires_on_merge_by_prefix():
    r = pr_resolution.check(_good_pr(disposition="merged", basis="branch_prefix",
                                     evidence="same prefix as mine"))
    assert r["pass"] is False


# ------------------------------------------------------- SN-0735 revert-bomb check
A40 = "a" * 40
B40 = "b" * 40


def _good_dup_pr(**over):
    rec = {
        "pr": 1998,
        "disposition": "closed_as_superseded",
        "main_tip_sha": "4" * 40,
        "blob_comparison": [
            {"path": "tools/gate.py", "pr_blob": A40, "main_blob": A40,
             "identical": True, "reverts_main": False},
        ],
    }
    rec.update(over)
    return rec


def test_sn0735_honors_compared_no_revert():
    r = duplicate_pr_blobs.check(_good_dup_pr())
    assert r["pass"] is True, r["reasons"]


def test_sn0735_fires_on_revert_bomb():
    # The PR's bytes would move main backwards on this path.
    rec = _good_dup_pr()
    rec["blob_comparison"] = [
        {"path": "tools/gate.py", "pr_blob": B40, "main_blob": A40,
         "identical": False, "reverts_main": True},
    ]
    r = duplicate_pr_blobs.check(rec)
    assert r["pass"] is False
    assert any("REVERT BOMB" in x for x in r["reasons"])


def test_sn0735_fires_without_blob_comparison():
    r = duplicate_pr_blobs.check(_good_dup_pr(blob_comparison=[]))
    assert r["pass"] is False
    assert any("no blob comparison" in x for x in r["reasons"])


def test_sn0735_fires_on_abbreviated_sha():
    rec = _good_dup_pr()
    rec["blob_comparison"] = [
        {"path": "tools/gate.py", "pr_blob": "abc123", "main_blob": A40,
         "identical": False, "reverts_main": False},
    ]
    r = duplicate_pr_blobs.check(rec)
    assert r["pass"] is False
    assert any("abbreviated" in x for x in r["reasons"])


def test_sn0735_fires_on_claimed_identical_math_mismatch():
    # The math is checked, not trusted.
    rec = _good_dup_pr()
    rec["blob_comparison"] = [
        {"path": "tools/gate.py", "pr_blob": B40, "main_blob": A40,
         "identical": True, "reverts_main": False},
    ]
    r = duplicate_pr_blobs.check(rec)
    assert r["pass"] is False
    assert any("math is checked" in x for x in r["reasons"])


def test_sn0735_fires_on_stale_main_tip():
    r = duplicate_pr_blobs.check(_good_dup_pr(main_tip_sha="not-a-sha"))
    assert r["pass"] is False
    assert any("full 40-hex" in x for x in r["reasons"])


# ------------------------------------------------------- ingest-boundary law
def _good_ingest(**over):
    rec = {
        "existing": {"status": "authoritative", "score": 9.0,
                     "as_of": "2026-10-09T16:00:00Z", "pinned": False},
        "point": {"status": "history", "score": 8.0,
                  "as_of": "2026-10-09T15:00:00Z", "source": "worker-log"},
        "ingest_action": "skipped",
        "now": NOW,
    }
    rec.update(over)
    return rec


def test_ingest_boundary_honors_skipped_heuristic():
    r = ingest_boundary.check(_good_ingest())
    assert r["pass"] is True, r["reasons"]


def test_ingest_boundary_fires_on_heuristic_overwriting_authoritative():
    # The #1354 fourth-poison-path repro: heuristic claim overwrites an
    # AUTHORITATIVE score's VALUE while keeping the "authoritative" LABEL.
    r = ingest_boundary.check(_good_ingest(
        point={"status": "heuristic", "score": 2.0,
               "as_of": "2026-10-09T17:00:00Z", "source": "evil"},
        ingest_action="wrote"))
    assert r["pass"] is False
    assert any("label-guard" in x for x in r["reasons"])


def test_ingest_boundary_honors_authoritative_update_flow():
    # Authoritative updates still flow via authoritative points.
    r = ingest_boundary.check(_good_ingest(
        point={"status": "authoritative", "score": 9.5,
               "as_of": "2026-10-09T17:00:00Z", "source": "naya1"},
        ingest_action="wrote"))
    assert r["pass"] is True, r["reasons"]


def test_ingest_boundary_fires_on_future_dated_not_rejected():
    r = ingest_boundary.check(_good_ingest(
        point={"status": "heuristic", "score": 8.0,
               "as_of": "2026-10-09T20:35:00Z", "source": "worker-log"},
        ingest_action="skipped"))
    assert r["pass"] is False
    assert any("future-dated" in x for x in r["reasons"])


def test_ingest_boundary_honors_future_dated_rejected():
    r = ingest_boundary.check(_good_ingest(
        point={"status": "heuristic", "score": 8.0,
               "as_of": "2026-10-09T20:35:00Z", "source": "worker-log"},
        ingest_action="rejected"))
    assert r["pass"] is True, r["reasons"]


def test_ingest_boundary_fires_on_pin_mutation():
    # Pins keep real timestamps: a pin's as_of is never mutated by a later window.
    rec = _good_ingest()
    rec["existing"]["pinned"] = True
    rec["ingest_action"] = "wrote"
    rec["point"] = {"status": "heuristic", "score": 8.5,
                    "as_of": "2026-10-09T17:00:00Z", "source": "worker-log"}
    r = ingest_boundary.check(rec)
    assert r["pass"] is False
    assert any("PINNED" in x or "pin" in x for x in r["reasons"])


def test_ingest_boundary_honors_pin_immune_skip():
    rec = _good_ingest()
    rec["existing"]["pinned"] = True
    rec["ingest_action"] = "skipped"
    r = ingest_boundary.check(rec)
    assert r["pass"] is True, r["reasons"]


# ---------------------------------------------------------------- hardening
# Validator round 2 (comment 6086185213): fail closed on SHAPE, not just
# syntax. Five near-miss evasions — every field the law's hard line depends
# on is REQUIRED, not merely validated-when-present. Absence is the exploit.
def test_verification_law_fires_on_empty_request_direct_capture():
    # Empty request text classified the record "non-direct", so a QUEUED
    # disposition PASSED while printing "Verification Law honored".
    r = instant_activation.check(_good_capture(
        request="", disposition="queued", queued_for_verification=True))
    assert r["pass"] is False


def test_verification_law_fires_on_unparseable_activation_time():
    # activated_at: "soon" passed on presence alone. Presence is not proof.
    r = instant_activation.check(_good_capture(activated_at="soon"))
    assert r["pass"] is False


def test_triple_a_fires_on_unnamed_builder():
    # Empty builder skipped the scorer==builder independence check, so a
    # self-scored DONE passed by omission.
    r = triple_a.check(_good_deliverable(builder="", scorer="naya5"))
    assert r["pass"] is False


def test_sn0732_fires_on_reworded_dependent_trigger():
    # "Shawn said capture that" (spaces) evaded the exact-match ban.
    r = naya_identity.check(_good_lesson(capture_trigger="Shawn said capture that"))
    assert r["pass"] is False
    assert any("not compounded" in x for x in r["reasons"])


def test_sn0735_fires_on_omitted_reverts_main():
    # reverts_main omitted on a row passed silently as "delta, no revert".
    rec = _good_dup_pr()
    rec["blob_comparison"] = [
        {"path": "tools/gate.py", "pr_blob": B40, "main_blob": A40, "identical": False},
    ]
    r = duplicate_pr_blobs.check(rec)
    assert r["pass"] is False


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

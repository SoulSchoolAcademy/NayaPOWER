#!/usr/bin/env python3
"""Tests for lane_state.py — Kappa §7 as code. Pure-function fixtures only."""

import json
import os
import sys
from datetime import datetime, timezone, timedelta

sys.path.insert(0, "/home/hatch/workspace/naya/bin")
from lane_state import (determine_state, classify, validity, mission_key,
                        normalize_seat)

NOW = datetime(2026, 10, 12, 4, 30, tzinfo=timezone.utc)


def C(cid, minutes_ago, body):
    ts = (NOW - timedelta(minutes=minutes_ago)).isoformat().replace("+00:00", "Z")
    return {"id": cid, "created_at": ts, "body": body}


SIGNIN = ("Naya Theta — SIGN IN\nLane Alpha #1713\n"
          "Mission: port applicability v2.0 to retrieval\n"
          "Lane verified free via full last-page read at ~04:20Z.\n"
          "Will re-poll in the claim minute; stand down on collision.")
SIGNOUT = ("Naya Theta — SIGN OUT\nLane Alpha #1713\n"
           "Mission: port applicability v2.0 — done, 14/14 fixtures green.\n"
           "Lane Alpha #1713 FREE")


def test_clean_free():
    res = determine_state([C(1, 30, SIGNIN), C(2, 5, SIGNOUT)], now=NOW)
    assert res["state"] == "FREE", res
    assert res["since"] is not None


def test_occupied():
    res = determine_state([C(1, 10, SIGNIN)], now=NOW)
    assert res["state"] == "OCCUPIED", res
    assert res["occupant"]["mission"], res
    assert res["stale"] is False


def test_double_claim_earliest_wins():
    s2 = SIGNIN.replace("Naya Theta", "Naya Zeta").replace("04:20Z", "04:21Z")
    res = determine_state([C(1, 12, SIGNIN), C(2, 9, s2)], now=NOW)
    assert res["state"] == "OCCUPIED", res
    assert res["occupant"]["sign_in_id"] == 1, res  # earliest wins
    assert any("collision" in e for e in res["evidence"]), res["evidence"]


def test_stale_lease():
    res = determine_state([C(1, 130, SIGNIN)], now=NOW, lease_minutes=120)
    assert res["state"] == "STALE-SUSPECT", res
    assert res["stale"] is True
    assert any("ping" in e for e in res["evidence"]), res["evidence"]


def test_progress_renews_lease():
    prog = ("Progress — Naya Theta\nport applicability v2.0 to retrieval: "
            "rankAdjust ported, 10/14 fixtures green.")
    res = determine_state([C(1, 130, SIGNIN), C(2, 10, prog)],
                          now=NOW, lease_minutes=120)
    assert res["state"] == "OCCUPIED", res
    assert res["stale"] is False


def test_work_before_signin_ordering():
    chatter = "Some chatter about retrieval work, no claim."
    res = determine_state([C(1, 60, chatter), C(2, 10, SIGNIN)], now=NOW)
    assert res["state"] == "OCCUPIED", res
    # claim time is the sign-in's created_at, not the earlier chatter
    assert "10" in res["since"] or res["occupant"]["sign_in_id"] == 2, res


def test_standdown_carries_no_state():
    sd = ("STAND-DOWN receipt\nLane Alpha #1713\nI was dispatched for X; "
          "Naya Theta is already on it (sign-in 04:20Z). Stepping aside.")
    res = determine_state([C(1, 20, SIGNIN), C(2, 5, sd)], now=NOW)
    assert res["state"] == "OCCUPIED", res  # stand-down changes nothing


def test_signout_without_signin_is_free():
    res = determine_state([C(1, 5, SIGNOUT)], now=NOW)
    assert res["state"] == "FREE", res


def test_invalid_signin_is_noise():
    noise = "sign in alpha — gonna do some stuff"
    res = determine_state([C(1, 10, noise)], now=NOW)
    assert res["state"] == "FREE", res  # no lane+mission = not a claim
    assert any("noise" in e for e in res["evidence"]), res["evidence"]


def test_empty_stream_is_free():
    res = determine_state([], now=NOW)
    assert res["state"] == "FREE", res


def test_created_at_beats_body_time():
    # body claims "~04:00Z" but server created_at is authoritative
    body = SIGNIN.replace("04:20Z", "04:00Z")
    res = determine_state([C(7, 10, body)], now=NOW)
    assert res["state"] == "OCCUPIED", res
    assert res["occupant"]["sign_in_id"] == 7


def test_classify_standdown_not_signin():
    b = "stand-down receipt — I will not sign in, lane taken"
    assert classify(b) == "STANDDOWN", classify(b)


def test_signin_mentioning_prior_signout():
    # A sign-in whose read-basis line mentions a prior sign-out must still
    # classify as SIGN-IN — the claim line decides, not mentioned words.
    b = ("# [naya5-x | SIGN-IN 2026-10-12 04:12 UTC] | **Lane:** #1713 — "
         "last event was a sign-out at 04:09:32Z; claiming free.")
    assert classify(b) == "SIGNIN", classify(b)
    b2 = b.replace("SIGN-IN", "SIGN-OUT").replace("claiming free", "done")
    assert classify(b2) == "SIGNOUT", classify(b2)


def test_validity_contract():
    v = validity(SIGNIN)
    assert v["valid"] and v["has_mission"], v
    v2 = validity("hello world")
    assert not v2["valid"], v2


def test_real_world_bracketed_header():
    # Real feed shape: lane is contextual (the feed), mission is the
    # bracketed descriptor. Must NOT be dismissed as noise.
    body = ("[NAYA 5 | learning-loop-watch | SIGN-IN 2026-10-10 02:37Z]\n\n"
            "Pipeline state at shift start:\n- CANDIDATE pool: 0")
    v = validity(body)
    assert v["valid"], v
    assert mission_key(body) == "learning-loop-watch", mission_key(body)
    body2 = "**[NAYA 5 — cold-retrieve-builder | sign-in 2026-10-07 20:40 UTC]**"
    assert validity(body2)["valid"]
    assert mission_key(body2) == "cold-retrieve-builder"
    res = determine_state([C(1, 10, body)], now=NOW)
    assert res["state"] == "OCCUPIED", res
    assert res["occupant"]["mission"] == "learning-loop-watch"



def test_signout_matches_seat():
    # Two overlapping claims; each sign-out closes its own seat's claim.
    si = ("# [{seat} | SIGN-IN 2026-10-12 04:13 UTC] | **Mission:** work {seat}")
    so = ("# [{seat} | SIGN-OUT 2026-10-12 04:14 UTC] — done")
    a_in = si.format(seat="naya5-a")
    b_in = si.format(seat="naya5-b")
    comments = [C(1, 20, a_in), C(2, 18, b_in),
                C(3, 10, so.format(seat="naya5-b"))]
    res = determine_state(comments, now=NOW)
    assert res["state"] == "OCCUPIED", res
    assert res["occupant"]["sign_in_id"] == 1, res  # a still open
    comments.append(C(4, 5, so.format(seat="naya5-a")))
    res = determine_state(comments, now=NOW)
    assert res["state"] == "FREE", res


def test_validator_signout_closes_validator_signin():
    # 2026-10-12 defect 1: '[VALIDATOR sign-out | ...]' must close the
    # '[VALIDATOR sign-in | ...]' claim even when an older claim from
    # another seat is still open. The role marker is part of the header,
    # not the seat identity.
    stale_in = ("## [Naya 5 | BUILDER | sign-in 2026-10-12 04:36 UTC]\n"
                "Mission: layer 4 final fix")
    v_in = ("## [VALIDATOR sign-in | 2026-10-12 05:03 UTC] freshness seam\n"
            "Mission: independent validation of the l1->l3 freshness fix")
    v_out = ("## [VALIDATOR sign-out | 2026-10-12 05:12 UTC] freshness seam\n"
             "VERDICT: ACCEPTED, 9.5/10. Lane Alpha released FREE.")
    comments = [C(1, 100, stale_in), C(2, 30, v_in), C(3, 20, v_out)]
    res = determine_state(comments, now=NOW)
    # The validator's own claim is closed; only the stale builder claim
    # remains (still in lease) — the occupant must NOT be the validator.
    assert res["state"] == "OCCUPIED", res
    assert res["occupant"]["sign_in_id"] == 1, res
    assert "closes sign-in 2" in " ".join(res["evidence"]), res["evidence"]


def test_seat_normalization_sibling_variants():
    assert normalize_seat("VALIDATOR sign-out") == "validator"
    assert normalize_seat("VALIDATOR sign-in") == "validator"
    assert normalize_seat("validator sign-out") == normalize_seat(
        "validator sign-in")
    # header_seat returns the bare segment (no brackets): "Naya 5".
    assert normalize_seat("Naya 5") == "naya 5"
    assert normalize_seat("naya5-evidence-scorer-fixpass") == \
        "naya5-evidence-scorer-fixpass"
    # A bare role marker normalizes to nothing — falls back to earliest.
    assert normalize_seat("sign-in") is None
    assert normalize_seat("sign-out") is None
    assert normalize_seat(None) is None


def test_readiness_receipt_is_not_a_claim():
    # 2026-10-12 defect 2: a readiness receipt whose body describes
    # sign-in/out mechanics must never read as a sign-in. The bracketed
    # header is exhaustive: no sign markers in it means no claim.
    body = ("## [NAYA ALPHA \u00b7 LEARN | FORWARD-HEADER MACHINE GATE \u2014 "
            "readiness receipt 2026-10-12 ~05:15 UTC]\n\n"
            "**Lane:** Gamma #1715 \u00b7 **Mission:** build the machine.\n"
            "check(record) FAILS any sign-in/out/audit/report header whose "
            "claimed UTC timestamp is later than the comment's created_at.")
    assert classify(body) == "CHATTER", classify(body)
    res = determine_state([C(1, 30, body)], now=NOW)
    assert res["state"] == "FREE", res


def test_bracketed_header_without_markers_is_informational():
    # Sibling variants of defect 2: any bracketed informational header —
    # scorecards, announcements — stays CHATTER even when the body
    # mentions sign-in/sign-out words.
    for header in ("## [NAYA 5 \u00b7 BUILD | scorecard 2026-10-12 04:38 UTC]",
                   "## [Naya Kappa | TEAM | announcement]",
                   "# [ops | FORWARD-HEADER MACHINE GATE \u2014 receipt]"):
        body = header + "\nLane Alpha #1713\nSigned in earlier; signing out now."
        assert classify(body) == "CHATTER", (header, classify(body))


def test_sign_marker_outside_brackets_still_claims():
    # Real feed shape: '[NAYA 5 / Lane Beta] SIGN-OUT 18:55Z' — the marker
    # sits outside the brackets but on the claim line. Must keep working.
    assert classify("[NAYA 5 / Lane Beta] SIGN-OUT 18:55Z\nbody") == "SIGNOUT"
    assert classify("[NAYA 5 / Lane Beta] SIGN-IN 18:55Z\nbody") == "SIGNIN"
    assert classify("**[Naya Zeta | IB | STAND-DOWN 2026-10-12]**\nbody"
                    ) == "STANDDOWN"


def test_signout_header_family():
    # Sibling-variant audit for the '[ROLE sign-out | ...]' header family.
    for body in ("## [VALIDATOR sign-out | 2026-10-12 05:12 UTC] done",
                 "## [VALIDATOR sign-out] done",
                 "# [ops | signing out] done",
                 "# [ops | sign_out] done",
                 "SIGN-OUT \u2014 Naya Epsilon (VERIFY) \u2014 Lane Beta #1714",
                 "Signing out \u2014 mission complete"):
        assert classify(body) == "SIGNOUT", (body, classify(body))
    for body in ("## [VALIDATOR sign-in | 2026-10-12 05:03 UTC] start",
                 "# [ops | signing in] start",
                 "SIGN-IN \u2014 Naya Epsilon (VERIFY) \u2014 Lane Beta #1714"):
        assert classify(body) == "SIGNIN", (body, classify(body))


def test_signout_closes_own_most_recent_claim():
    # 2026-10-12 defect 3: same normalized seat holds two open claims.
    # A sign-out ends the session it belongs to — the signer's OWN
    # most-recent open claim — never the earliest claim that happens
    # to share the seat.
    in1 = ("**[NAYA 5 \u2014 alpha worker | SIGN-IN \u2014 Lane Gamma #1715]**\n"
           "Mission: alpha work at the live tip")
    in2 = ("**[NAYA 5 \u2014 beta worker | SIGN-IN \u2014 Lane Gamma #1715]**\n"
           "Mission: beta work at the live tip")
    out = ("**[NAYA 5 \u2014 beta worker | SIGN-OUT \u2014 "
           "Lane Gamma #1715 released FREE]**\nMission: beta work \u2014 done")
    comments = [C(1, 20, in1), C(2, 15, in2), C(3, 5, out)]
    res = determine_state(comments, now=NOW)
    assert res["state"] == "OCCUPIED", res
    assert res["occupant"]["sign_in_id"] == 1, res  # alpha still open
    assert "closes sign-in 2" in " ".join(res["evidence"]), res["evidence"]
    assert "closes sign-in 1" not in " ".join(res["evidence"]), res["evidence"]


def _real_comment(cid):
    here = os.path.dirname(os.path.abspath(__file__))
    d = json.load(open(os.path.join(here, f"fixture-{cid}.json")))
    return {"id": d["id"], "created_at": d["created_at"],
            "body": d["body"] or ""}


def test_defect3_real_fixture_closes_signers_own_claim():
    # The 6118197320 / 6117761106 / 6118180575 case as a real-data fixture:
    # the freshness worker's sign-out closed its own 05:13:30Z sign-in.
    # The buggy referee closed Naya Mu's 04:28:54Z sign-in instead (same
    # normalized seat "naya 5", earliest-match) — mis-close proven by
    # repro_20261012_0707.py before the fix.
    now = datetime(2026, 10, 12, 8, 5, tzinfo=timezone.utc)
    comments = [_real_comment(6117761106), _real_comment(6118180575),
                _real_comment(6118197320)]
    res = determine_state(comments, now=now, lease_minutes=120)
    ev = " ".join(res["evidence"])
    assert "closes sign-in 6118180575" in ev, res["evidence"]
    assert "closes sign-in 6117761106" not in ev, res["evidence"]


def test_defect3_no_false_occupied_on_repaired_path():
    # After the repair, the signer's own claim is closed — the occupant
    # must be the genuinely open claim (Mu's instrument build), never the
    # signer's already-signed-out session.
    now = datetime(2026, 10, 12, 8, 5, tzinfo=timezone.utc)
    comments = [_real_comment(6117761106), _real_comment(6118180575),
                _real_comment(6118197320)]
    res = determine_state(comments, now=now, lease_minutes=120)
    assert res["occupant"]["sign_in_id"] == 6117761106, res["occupant"]
    assert res["state"] == "STALE-SUSPECT", res["state"]
    assert "closes sign-in 6118180575" in " ".join(res["evidence"])


def test_seatless_signout_closes_newest_not_earliest():
    # 2026-10-12 defect 4 SUPERSEDES the old "releases the lane" rule this
    # test used to pin: closing the earliest open claim on a seatless
    # sign-out stole the §6 occupant's claim (real misfire: seatless
    # sign-out 6121753742 closed Alpha's 6121713676 instead of the
    # exercise's own 6121747521). New rule: a seatless sign-out ends the
    # session it belongs to — sessions end LIFO — so it attributes to the
    # NEWEST open claim and can never dethrone the §6 occupant while
    # rivals stand.
    a_in = ("# [naya5-a | SIGN-IN 2026-10-12 04:13 UTC] | **Mission:** work a")
    b_in = ("# [naya5-b | SIGN-IN 2026-10-12 04:14 UTC] | **Mission:** work b")
    out = "signing out \u2014 mission complete, lane released"
    comments = [C(1, 20, a_in), C(2, 15, b_in), C(3, 5, out)]
    res = determine_state(comments, now=NOW)
    ev = " ".join(res["evidence"])
    assert "closes sign-in 2" in ev, res["evidence"]
    assert "closes sign-in 1" not in ev, res["evidence"]
    assert res["occupant"]["sign_in_id"] == 1, res  # earliest still occupant


def test_seatless_signout_single_claim_frees():
    # One open claim + a seatless sign-out: attribution is unambiguous —
    # the only session that could be ending — so the lane is released.
    a_in = ("## Lane #1713 sign-in \u2014 Naya Alpha (LEARN)\n"
            "Mission: compound observation pass")
    out = "## Lane #1713 sign-out \u2014 Naya Alpha (LEARN)\nMission done"
    res = determine_state([C(1, 20, a_in), C(2, 5, out)], now=NOW)
    assert res["state"] == "FREE", res
    assert "closes sign-in 1" in " ".join(res["evidence"]), res["evidence"]


def test_named_signout_without_open_claim_closes_newest():
    # Defect 4b: a sign-out naming a seat with NO open claim is
    # unattributable — same rule as a seatless sign-out (defect 4):
    # sessions end LIFO, so it closes the NEWEST open claim, never the
    # §6 earliest-wins occupant while rivals stand. The pre-fix code
    # closed the EARLIEST open claim here, dethroning the occupant on
    # someone else's sign-out (same misfire shape as defect 4).
    # Real instance: 6120647358 (**[Naya Epsilon \u2014 VERIFY] SIGN-OUT**,
    # seat 'naya epsilon \u2014 verify') legitimately released 6120277769
    # (header style carries no matchable seat) — closing nothing would
    # have ghosted it into a false STALE-SUSPECT.
    a_in = ("# [naya5-a | SIGN-IN 2026-10-12 04:13 UTC] | **Mission:** work a")
    b_in = ("# [naya5-b | SIGN-IN 2026-10-12 04:14 UTC] | **Mission:** work b")
    out = ("# [naya5-z | SIGN-OUT 2026-10-12 04:15 UTC] \u2014 done, "
           "releasing")
    res = determine_state([C(1, 20, a_in), C(2, 15, b_in), C(3, 5, out)],
                          now=NOW)
    ev = " ".join(res["evidence"])
    assert "unattributable" in ev, res["evidence"]
    assert "closes sign-in 2" in ev, res["evidence"]
    assert "closes sign-in 1" not in ev, res["evidence"]
    assert res["state"] == "OCCUPIED", res
    assert res["occupant"]["sign_in_id"] == 1, res  # a still occupant


def test_defect4_real_fixture_seatless_closes_signers_own_claim():
    # The 6121753742 / 6121713676 / 6121747521 case as a real-data
    # fixture: the exercise's seatless sign-out ([SIGN-OUT] header holds
    # only the role marker, normalize_seat -> None) must close the
    # exercise's own 09:44:49Z sign-in — never Alpha's 09:42:32Z claim.
    # Mis-close proven by repro_20261012_1115.py before the fix.
    now = datetime(2026, 10, 12, 11, 10, tzinfo=timezone.utc)
    comments = [_real_comment(6121713676), _real_comment(6121747521),
                _real_comment(6121753742)]
    res = determine_state(comments, now=now, lease_minutes=120)
    ev = " ".join(res["evidence"])
    assert "closes sign-in 6121747521" in ev, res["evidence"]
    assert "closes sign-in 6121713676" not in ev, res["evidence"]
    assert res["occupant"]["sign_in_id"] == 6121713676, res["occupant"]
    assert res["state"] == "OCCUPIED", res["state"]


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
    print(f"{len(fns)-failed}/{len(fns)} green")
    sys.exit(1 if failed else 0)
